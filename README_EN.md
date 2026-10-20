# Quiet Hours: total silence in a configured window

> AstrBot plugin · Zero calls, zero memory writes, zero messages

## The problem

Responding to every message at 3 a.m. is one of the clearest bot signatures.

This plugin drops events entirely during the window — zero traffic, rather than "received but ignored".

## Features

- Single highest-priority hook (10001)
- Supports windows crossing midnight, e.g. `23:00-08:00`
- `scope` = `all` (groups + private) or `group`
- One log line per day when entering the window
- `start == end` disables the plugin

## Install

### Option 1: Plugin marketplace (recommended)

Search "深夜静默" in the AstrBot WebUI plugin marketplace.

### Option 2: Download from Releases

Grab the zip from [Releases](../../releases), then WebUI → Plugins → Upload.

### Option 3: Clone manually

```bash
cd AstrBot/data/plugins
git clone https://github.com/RandyLuaW/astrbot_plugin_quiet_hours.git
```

No extra Python dependencies.

## Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `enabled` | bool | `true` | See Chinese README |
| `start_hour` | int | `0` | See Chinese README |
| `start_minute` | int | `0` | See Chinese README |
| `end_hour` | int | `8` | See Chinese README |
| `end_minute` | int | `0` | See Chinese README |
| `scope` | string | `all` | See Chinese README |
| `log_once_per_day` | bool | `true` | See Chinese README |

## Notes

- `scope=all` also silences private chat
- Midnight-crossing windows are handled natively

## License

MIT
