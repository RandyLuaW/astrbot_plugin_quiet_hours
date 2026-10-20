# 深夜静默：指定时段彻底不响应，降低夜间活跃特征

> AstrBot 插件 · 指定时段彻底不响应，降低夜间活跃特征

## 它解决什么问题

深夜仍然逐条响应，是账号最明显的机器行为特征之一。

这个插件在指定时段内直接掐掉事件，不调用模型、不写记忆、不发消息——零流量，而不是「收到了但不回」。

## 功能

- 单个最高优先级钩子（10001，高于防抖的 9999），静默期内直接 `stop_event()`
- 支持跨午夜时段，例如 `23:00-08:00`
- `scope` 可选 `all`（群聊+私聊）或 `group`（只静默群聊）
- 每天首次进入静默期只写一条日志，不刷屏
- `start == end` 视为关闭，避免误配置

## 工作机制

每条消息 → quiet_gate(priority=10001)
    ├─ 当前时间在静默区间内 → stop_event()，后续所有插件收不到事件
    └─ 区间外 → 放行

静默期内零 LLM 调用、零记忆写入、零消息发送。

## 安装

### 方式一：插件市场（推荐）

WebUI 插件市场搜索「深夜静默」。

### 方式二：Releases 下载

从 [Releases](../../releases) 下载 zip，WebUI → 插件 → 上传安装。

### 方式三：手动克隆

```bash
cd AstrBot/data/plugins
git clone https://github.com/RandyLuaW/astrbot_plugin_quiet_hours.git
```

无额外 Python 依赖。

## 配置项

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `enabled` | bool | `true` | 启用深夜静默 |
| `start_hour` | int | `0` | 静默开始-小时（0-23） |
| `start_minute` | int | `0` | 静默开始-分钟（0-59） |
| `end_hour` | int | `8` | 静默结束-小时（0-23） |
| `end_minute` | int | `0` | 静默结束-分钟（0-59） |
| `scope` | string | `all` | 生效范围：all 群聊和私聊都静默，group 只静默群聊。 |
| `log_once_per_day` | bool | `true` | 每天首次进入静默期时写一条日志（不发群消息） |

## 注意事项

- `scope=all` 连私聊也静默，深夜不想被打扰时用
- 跨午夜区间（如 23:00-08:00）已处理，不需要拆成两段

## License

MIT
