# Strategy GA Factory

P4-4 productionizes the Strategy JSON GA trace as a factory layer. It does not create a new trading strategy. It organizes existing GA candidates, Case Memory seeds, fitness results, elite selections, blocker outcomes, and lineage into stable archives.

## Flow

```text
Strategy JSON seeds
→ GA generation trace
→ fitness and blocker evidence
→ elite archive
→ strategy graveyard
→ lineage tree
→ next generation production status
```

## Runtime Outputs

```text
runtime/ga_factory/QuantGod_GAFactoryState.json
runtime/ga_factory/QuantGod_GAEliteArchive.json
runtime/ga_factory/QuantGod_GAStrategyGraveyard.json
runtime/ga_factory/QuantGod_GALineageTree.json
runtime/ga_factory/QuantGod_GAFactoryLedger.csv
```

The factory reads from:

```text
runtime/ga/QuantGod_GAStatus.json
runtime/ga/QuantGod_GACandidateRuns.jsonl
runtime/ga/QuantGod_GAEliteStrategies.json
runtime/ga/QuantGod_GALineage.json
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime status
python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime build --write
python3 tools/run_strategy_ga_factory.py --runtime-dir ./runtime telegram-text --refresh
```

Smoke test:

```bash
tmp="$(mktemp -d)"
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" sample --overwrite
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" build --write
python3 tools/run_strategy_ga_factory.py --runtime-dir "$tmp" telegram-text --refresh
```

## API

```text
GET  /api/strategy-ga-factory/status
POST /api/strategy-ga-factory/build
GET  /api/strategy-ga-factory/telegram-text
```

The `/api/ga-factory/*` routes are aliases for the same factory state.

## Safety

GA Factory can only classify candidates into:

```text
SHADOW
FAST_SHADOW
TESTER_ONLY
PAPER_LIVE_SIM
```

It cannot place orders, close positions, cancel orders, modify MT5 live presets, write MT5 `OrderRequest`, receive Telegram trading commands, or connect a Polymarket real-money wallet.
