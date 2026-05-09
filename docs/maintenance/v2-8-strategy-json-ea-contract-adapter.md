# v2.8 Strategy JSON → EA Contract Adapter

This maintenance step adds a read-only MQL5 contract adapter for Strategy JSON candidates.

Scope:

- Backend contract builder under `tools/strategy_contract_adapter`;
- CLI `tools/run_strategy_contract_adapter.py`;
- USDJPY strategy-lab API endpoints for status/build/telegram text;
- MQL5 read-only adapter inside `QuantGod_MultiStrategy.mq5`;
- frontend Evolution status card and detail section.

Safety:

- no MT5 order execution;
- no close/cancel/modify action;
- no live preset mutation;
- no Telegram command receiver;
- no Polymarket real-money path;
- GA candidates remain limited to shadow/tester/paper lane evaluation.

Verification:

```bash
python3 -m py_compile tools/run_strategy_contract_adapter.py tools/strategy_contract_adapter/*.py
python3 -m unittest tests.test_strategy_contract_adapter -v
node --test tests/node/test_strategy_contract_adapter_guard.mjs
python3 tools/run_strategy_contract_adapter.py --runtime-dir runtime build
```

