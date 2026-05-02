# Telegram 通知 Runbook

Telegram 在 QuantGod 中只用于 push-only 通知。它可以提醒 AI 分析结果、风险事件、每日摘要、交易开平仓报告和 Governance 变化，但不能接收或执行交易命令。

## 环境变量

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

不要把 token、chat id 或任何 webhook secret 提交到 Git。生产环境变量只能放在本机 shell、系统服务配置或安全的 secret manager 中。

## Smoke Test

```powershell
python tools\run_notify.py config
python tools\run_notify.py test --message "QuantGod notify smoke" --dry-run
python tools\run_notify.py history --limit 10
```

`--dry-run` 只能验证格式化、路由和历史记录逻辑，不代表已经真实发送 Telegram 消息。

## 安全规则

1. `/api/notify/*` endpoint 不得实现 buy、sell、close、cancel 或 disable-kill-switch。
2. Telegram bot 不处理用户命令，不把消息转成 trading intent。
3. 通知失败只能降级为日志或本地 history，不能影响交易 gate。
4. AI summary 通知只能引用 advisory evidence，不能附带“自动执行”语义。
