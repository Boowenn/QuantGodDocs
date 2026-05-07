# v2.6.1 Strategy JSON USDJPY Backtest

This maintenance step adds the first executable Strategy JSON backtest evidence layer for QuantGod Perfect Edition.

## Added

- Backend module `tools/usdjpy_strategy_backtest`.
- CLI `tools/run_usdjpy_strategy_backtest.py`.
- API endpoints under `/api/usdjpy-strategy-lab/strategy-backtest/*`.
- Frontend Evolution panel card and action for Strategy JSON backtest.
- GA fitness integration that reads `runtime/backtest/QuantGod_StrategyBacktestReport.json`.
- Python and Node guards for USDJPY-only and read-only safety.

## Output Files

```text
runtime/backtest/usdjpy.sqlite
runtime/backtest/QuantGod_StrategyBacktestReport.json
runtime/backtest/QuantGod_StrategyTrades.csv
runtime/backtest/QuantGod_StrategyEquityCurve.csv
```

## Safety Boundary

No live execution path was added.

```text
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
livePresetMutationAllowed=false
telegramCommandExecutionAllowed=false
polymarketRealMoneyAllowed=false
```

The module is a local Strategy JSON research plane only.

## Validation

Backend:

```text
python3 -m unittest discover tests -v
node --test tests/node/*.mjs
```

Frontend:

```text
npm run usdjpy-evolution
npm test
npm run build
```

Docs:

```text
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```

