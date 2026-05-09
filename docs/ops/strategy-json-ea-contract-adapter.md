# Strategy JSON → MQL5 EA Contract Adapter

QuantGod v2.8 closes the Strategy JSON contract loop into MT5 without granting execution permission.

Flow:

```text
GA / Strategy JSON candidate
→ Strategy JSON validator and safety scan
→ QuantGod_StrategyJsonEAContract_EA.txt
→ QuantGod_MultiStrategy.mq5 read-only adapter
→ QuantGod_StrategyJsonEAContractEAStatus.json
→ Frontend / Telegram audit
```

The adapter is deliberately read-only:

- contract mode is limited to `SHADOW_EVALUATION_ONLY`, `TESTER_EVALUATION_ONLY`, or `PAPER_LIVE_SIM_EVALUATION_ONLY`;
- EA may read seed id, fingerprint, strategy family, RSI/exit/risk parameters, and lane;
- EA writes a status/ack file so the frontend can confirm the contract is visible to MT5;
- the adapter does not call `OrderSend`, does not write an `OrderRequest`, and does not mutate the live preset.

Main runtime files:

```text
QuantGod_StrategyJsonEAContract.json
QuantGod_StrategyJsonEAContract_EA.txt
QuantGod_StrategyJsonEAContractStatus.json
QuantGod_StrategyJsonEAContractEAStatus.json
```

API:

```text
GET  /api/usdjpy-strategy-lab/strategy-contract/status
POST /api/usdjpy-strategy-lab/strategy-contract/build
GET  /api/usdjpy-strategy-lab/strategy-contract/telegram-text
```

This completes the first production bridge for the design principle:

```text
one Strategy JSON can drive backtest, GA, EA shadow/tester/paper evaluation, frontend, and Telegram.
```

