# Strategy JSON USDJPY Backtest

QuantGod Perfect Edition starts by making Strategy JSON executable in a read-only research plane.

This module reads a safe `quantgod.strategy.v1` seed, runs a deterministic USDJPY H1 Strategy JSON backtest against local SQLite bars, and writes GA-readable evidence:

```text
runtime/backtest/usdjpy.sqlite
runtime/backtest/QuantGod_StrategyBacktestReport.json
runtime/backtest/QuantGod_StrategyTrades.csv
runtime/backtest/QuantGod_StrategyEquityCurve.csv
```

## What It Does

- Keeps scope fixed to `USDJPYc`.
- Validates Strategy JSON through the existing Strategy JSON validator.
- Runs the current RSI_Reversal LONG contract against local H1 bars.
- Produces `netR`, pips, profit factor, win rate, max drawdown R, Sharpe, Sortino, loss streak, MFE/MAE and profit capture ratio.
- Feeds the latest report into GA fitness as additional evidence.
- Exposes read-only API endpoints under `/api/usdjpy-strategy-lab/strategy-backtest/*`.

## Safety

The backtest layer does not:

- place orders
- close positions
- cancel orders
- mutate live preset
- write MT5 order requests
- connect a Polymarket wallet
- receive Telegram trade commands

It only writes local research evidence under `runtime/backtest`.

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sample --overwrite
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime run --write
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime status
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime telegram-text --refresh
```

## API

```text
GET  /api/usdjpy-strategy-lab/strategy-backtest/status
POST /api/usdjpy-strategy-lab/strategy-backtest/sample
POST /api/usdjpy-strategy-lab/strategy-backtest/run
GET  /api/usdjpy-strategy-lab/strategy-backtest/telegram-text
```

All endpoints are local, USDJPY-only, and research-only.

## Current Limits

This is not yet the full Perfect Edition backtest engine.

Current implementation is a first executable contract for `USDJPYc / RSI_Reversal / LONG` on H1 bars. Later phases should add full M1/M5/M15/H1 resampling, cost model, parity harness, Strategy JSON runner coverage for all shadow strategies, and equity curve analytics for GA cache.

