# Phase 1 scope

Phase 1 implemented:

- Module A: AI multi-agent analysis engine V1.
- Module B: Kline chart integration.
- Module C: CI/CD baseline.

## AI V1

Data flow:

```text
MT5 market snapshot
→ TechnicalAgent + RiskAgent in parallel
→ DecisionAgent
→ latest/history JSON
→ Governance evidence
```

Safety: AI recommendations are advisory and cannot execute orders, bypass Kill Switch, mutate live presets, or alter Governance decisions by themselves.

## Kline

KlineCharts renders MT5 OHLCV data, indicators, trades, and shadow signals through backend read-only APIs.

## CI

CI runs Python tests, Node/API contract tests, static guards, and frontend build in the original monorepo. After repo split, those checks are separated by repository.
