# Backend guide

## Repository

`Boowenn/QuantGodBackend`

## Main responsibilities

- MT5 EA and HFM live/shadow/backtest launchers
- Node dashboard/API server
- Python tools for Governance, ParamLab, research stats, AI analysis, Vibe Coding, notification, and bridge contracts
- Backend CI and API contract tests

## Local commands

```powershell
python -m unittest discover tests -v
python -m pytest tests -q --cov=tools --cov-report=term-missing
node --test tests/node/*.mjs
Dashboard\start_dashboard.bat
```

## Runtime folders

Typical HFM runtime path:

```text
C:\Program Files\HFM Metatrader 5\MQL5\Files\
```

The backend reads local runtime JSON/CSV from the HFM Files folder and serves normalized data via `/api/*`.

## API groups

- `/api/mt5-readonly/*`
- `/api/mt5-symbol-registry/*`
- `/api/ai-analysis/*`
- `/api/ai-analysis-v2/*`
- `/api/governance/*`
- `/api/paramlab/*`
- `/api/trades/*`
- `/api/research/*`
- `/api/shadow/*`
- `/api/dashboard/*`
- `/api/notify/*`
- `/api/vibe-coding/*`
- `/api/kline/*`

## Safety review checklist

Before merging backend changes, verify:

- no direct live-preset mutation unless a documented manual authorization flow exists;
- no API endpoint stores broker credentials;
- no AI/Vibe/Telegram path can send broker orders;
- all trading bridge operations remain guarded by dry-run, Kill Switch, and authorization locks;
- API contract tests are updated when response shape changes.
