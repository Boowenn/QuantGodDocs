# HFM MT5 live pilot notes

## Source of truth

Use the official HFM MT5 client path for HFM Cent live-account work:

```text
C:\Program Files\HFM Metatrader 5
```

Generic MetaTrader installations may contain stale smoke-test data and should not be treated as live source of truth.

## Safety constraints

- Keep live pilot at micro-lot scale.
- Preserve one-position caps and hard SL/TP.
- Keep Kill Switch and news filter active.
- Do not promote routes without evidence and manual authorization.
- Do not let AI/Vibe/Telegram paths alter live preset state.
