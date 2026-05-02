# Telegram 通知

Telegram 模块是 push-only 通知系统，只负责发送事件摘要，不接受交易命令。

## 支持事件

- `TRADE_OPEN`
- `TRADE_CLOSE`
- `KILL_SWITCH`
- `NEWS_BLOCK`
- `AI_ANALYSIS`
- `CONSECUTIVE_LOSS`
- `DAILY_DIGEST`
- `GOVERNANCE`
- `TEST`

## 环境变量

```powershell
$env:TELEGRAM_BOT_TOKEN = "<bot-token>"
$env:TELEGRAM_CHAT_ID = "<chat-id>"
```

不要把 token 或 chat id 提交到 Git。

## Smoke test

```powershell
cd C:\QuantGod\QuantGodBackend
python tools\run_notify.py config
python tools\run_notify.py test --message "QuantGod smoke" --dry-run
python tools\run_notify.py history --limit 10
```

## 安全边界

Telegram 不能触发下单、平仓、撤单、preset 修改、Kill Switch 修改或任何 live route promotion。
