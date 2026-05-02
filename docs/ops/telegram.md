# Telegram notification runbook

## Purpose

Telegram is a push-only notification channel.

## Allowed messages

- TRADE_OPEN
- TRADE_CLOSE
- KILL_SWITCH
- NEWS_BLOCK
- AI_ANALYSIS
- CONSECUTIVE_LOSS
- DAILY_DIGEST
- GOVERNANCE

## Forbidden behavior

- No command processing.
- No order send/close/cancel.
- No preset mutation.
- No credential storage in Git.

## Environment variables

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
