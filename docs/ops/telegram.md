# Telegram 通知

Telegram 在 QuantGod 中只做 push-only 通知，不接收交易命令。

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

## 配置

配置只允许来自本机环境变量或安全的 secret 管理，不写入 Git。

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
QG_NOTIFY_ENABLED
NOTIFY_TRADE_SIGNAL
NOTIFY_RISK_ALERT
NOTIFY_AI_SUMMARY
NOTIFY_DAILY_DIGEST
NOTIFY_GOVERNANCE
```

## 安全边界

Telegram 不接受 `/buy`、`/sell`、`/close`、`/unlock`、`/promote` 这类命令。任何通知都不能触发 broker order、live preset mutation、Kill Switch override 或 Governance mutation。
