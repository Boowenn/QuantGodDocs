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

环境变量通过本地 `.env` 文件注入，格式参考：

```
TELEGRAM_BOT_TOKEN — 通过 @BotFather 获取
TELEGRAM_CHAT_ID   — 目标群组或频道的数字 ID
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
