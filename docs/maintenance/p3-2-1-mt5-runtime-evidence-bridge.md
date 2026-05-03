# P3-2.1 MT5 Runtime Evidence Bridge

## Purpose

P3-2.1 completes the Telegram-only advisory loop by making AI Analysis V2 consume local HFM/MT5 EA runtime files before mock fallback data.

The desired loop is:

```text
HFM/MT5 EA read-only JSON snapshot
→ MT5 runtime evidence bridge
→ AI Analysis V2 snapshot
→ MT5 AI Telegram advisory monitor
→ Telegram push-only message
→ SQLite notification evidence
```

## Phase boundary

P3-2.1 is a P3-2 hardening step, not P3-3 broker adapter work.

Allowed:

- Local runtime JSON reads.
- Schema and freshness validation.
- Advisory-only AI snapshot normalization.
- Telegram push-only notification using existing P3-2 notifier.
- SQLite notification evidence through the existing state layer.

Forbidden:

- Order submission.
- Close or cancel requests.
- Broker adapter abstraction.
- Webhook receiver.
- Telegram command execution.
- Email delivery.
- Credential storage.
- Live preset mutation.
- Kill Switch override.

## Backend files

```text
tools/mt5_runtime_bridge/__init__.py
tools/mt5_runtime_bridge/freshness.py
tools/mt5_runtime_bridge/schema.py
tools/mt5_runtime_bridge/reader.py
tools/run_mt5_runtime_bridge.py
tools/ai_analysis/market_data_collector.py
tests/test_mt5_runtime_bridge.py
tests/node/test_mt5_runtime_bridge_guard.mjs
```

`tools/ai_analysis/analysis_service_v2.py` is patched so `MarketDataCollector` receives `self.runtime_dir` from `AnalysisServiceV2(runtime_dir=...)`. This makes `run_mt5_ai_telegram_monitor.py --runtime-dir ...` affect the actual snapshot collector.

`tools/run_mt5_ai_telegram_monitor.py` is patched to include `fallback`, `runtimeFresh` and `runtimeAgeSeconds` in its source summary/message.

## Validation

Backend:

```powershell
cd C:\QuantGod\QuantGodBackend

python -m py_compile tools\run_mt5_runtime_bridge.py tools\mt5_runtime_bridge\freshness.py tools\mt5_runtime_bridge\schema.py tools\mt5_runtime_bridge\reader.py tools\ai_analysis\market_data_collector.py
python -m unittest discover tests -v
node --test tests\node\test_mt5_runtime_bridge_guard.mjs

python tools\run_mt5_runtime_bridge.py sample --runtime-dir .\runtime --symbols USDJPYc --overwrite
python tools\run_mt5_runtime_bridge.py status --runtime-dir .\runtime --symbols USDJPYc --max-age-seconds 0
python tools\run_mt5_runtime_bridge.py snapshot --runtime-dir .\runtime --symbol USDJPYc --max-age-seconds 0
python tools\run_mt5_ai_telegram_monitor.py scan-once --runtime-dir .\runtime --symbols USDJPYc --force
```

Docs:

```powershell
cd C:\QuantGod\QuantGodDocs

python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## Acceptance criteria

P3-2.1 is complete when:

```text
python tools/run_mt5_runtime_bridge.py status
```

shows `runtimeFound=true` and at least one fresh symbol, and:

```text
python tools/run_mt5_ai_telegram_monitor.py scan-once --symbols USDJPYc --send --force
```

sends a Telegram advisory message whose source is `hfm_ea_runtime` or `dashboard_runtime`, with `fallback: False`. The message must not be based on `mt5_python_unavailable` when fresh runtime files exist.

## Secret hygiene

Runtime JSON files must never include:

```text
password
token
apiKey
secret
authorization
bearer
```

Example files may contain redacted fields such as `loginRedacted` or `serverRedacted`.
