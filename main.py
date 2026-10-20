"""深夜静默：在指定时段内彻底不响应消息。

设计要点
--------
1. 单个最高优先级消息钩子（10001，高于 msg_debounce 的 9999），静默期内直接
   stop_event()，后续所有插件（防抖、iris 记忆、主动回复、sticker）都收不到事件。
2. 静默期不做任何 LLM 调用、不记录记忆、不发任何消息——深夜零流量，
   避免"账号凌晨仍在活跃"这类机器行为特征。
3. 支持跨午夜时段（如 23:00-08:00），start == end 视为关闭。
4. 每天首次进入静默期只写一条日志，避免刷屏。
"""

from __future__ import annotations

import time
from datetime import datetime

from astrbot import logger
from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

PLUGIN_NAME = "astrbot_plugin_quiet_hours"
HANDLER_PRIORITY = 10001


class QuietHoursPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig | None = None):
        super().__init__(context)
        self.config = config or {}
        self._last_log_day = ""

    # ------------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------------

    def _int(self, key: str, default: int) -> int:
        try:
            return int(self.config.get(key, default))
        except (TypeError, ValueError):
            return default

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled", True))

    @property
    def scope(self) -> str:
        return str(self.config.get("scope", "all") or "all")

    def _period(self) -> tuple[int, int, int, int]:
        return (
            self._int("start_hour", 0),
            self._int("start_minute", 0),
            self._int("end_hour", 8),
            self._int("end_minute", 0),
        )

    def _is_quiet(self, now: datetime | None = None) -> bool:
        now = now or datetime.now()
        sh, sm, eh, em = self._period()
        start = (sh % 24) * 60 + min(max(sm, 0), 59)
        end = (eh % 24) * 60 + min(max(em, 0), 59)
        if start == end:
            return False
        cur = now.hour * 60 + now.minute
        if start < end:
            return start <= cur < end
        return cur >= start or cur < end

    # ------------------------------------------------------------------
    # 主钩子
    # ------------------------------------------------------------------

    @filter.event_message_type(filter.EventMessageType.ALL, priority=HANDLER_PRIORITY)
    async def on_message(self, event: AstrMessageEvent):
        if not self.enabled:
            return
        if self.scope == "group" and not event.get_group_id():
            return
        if not self._is_quiet():
            return

        self._log_once()
        event.stop_event()

    def _log_once(self) -> None:
        if not bool(self.config.get("log_once_per_day", True)):
            return
        day = time.strftime("%Y-%m-%d")
        if day == self._last_log_day:
            return
        self._last_log_day = day
        sh, sm, eh, em = self._period()
        logger.info(
            f"[{PLUGIN_NAME}] 进入静默期 {sh:02d}:{sm:02d}-{eh:02d}:{em:02d}，"
            f"期间不响应任何消息"
        )
