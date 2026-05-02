# Backend safety boundaries

## Non-negotiable rules

1. AI analysis is advisory only.
2. Vibe Coding strategies are research/backtest-only until manually promoted through the full chain.
3. Telegram is push-only and cannot accept trading commands.
4. Unified `/api/*` data endpoints are local-first and must not expose credentials.
5. Kill Switch, authorization locks, dry-run state, news filter, and live preset mutation guards must not be bypassed.

## Vibe Coding to live chain

A generated strategy must pass:

```text
Vibe Coding idea
→ Python research backtest
→ ParamLab/tester-only validation
→ Governance Advisor evidence review
→ Version Promotion Gate
→ manual authorization lock
→ guarded live preset update
```

No Vibe Coding endpoint is allowed to create live broker orders.

## Telegram boundary

Telegram may emit:

- trade event alerts
- Kill Switch alerts
- news block alerts
- AI summary alerts
- Governance summary alerts
- daily digest

Telegram must not receive or execute commands.
