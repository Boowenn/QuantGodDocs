# Phase 3 scope

Phase 3 implemented optional enhancements:

- Module H: Vibe Coding strategy workbench.
- Module I: AI multi-agent V2 with Bull/Bear debate and RAG-style memory.
- Module J: Kline enhancements for AI overlays, Vibe indicators, and polling config.

## Vibe Coding

Natural language idea → Python BaseStrategy code → safety validation → strategy registry → research-only backtest → AI analysis → iteration.

Generated strategies cannot directly control MT5. Live path must pass backtest, ParamLab, Governance, Version Gate, and manual authorization.

## AI V2

Flow:

```text
Technical + Risk + News + Sentiment
→ BullAgent + BearAgent debate
→ DecisionAgentV2
→ Governance evidence + local memory
```

Debate and memory are context only; they cannot trigger orders.

## Kline enhancements

Kline overlays expose AI decisions and Vibe indicators while preserving read-only chart behavior.
