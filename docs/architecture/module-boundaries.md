# Module boundaries

## Backend-owned modules

Backend owns all code that can touch MT5 runtime data, HFM local files, strategy evaluation, Governance, or AI analysis outputs.

Backend-owned examples:

- MT5 EA source under `MQL5/`
- Node dashboard/API server under `Dashboard/`
- MT5 read-only bridge and trading bridge guard tools
- Governance Advisor
- ParamLab Runner, Auto Scheduler, Report Watcher, Recovery
- Strategy Version Registry and Version Promotion Gate
- Backend Backtest Loop
- AI Analysis V1/V2 agents and evidence writer
- Vibe Coding strategy generation, safety checker, registry, and backtest connector
- Telegram notification service

## Frontend-owned modules

Frontend owns visual workspaces and UI-only state:

- Vue shell
- Ant Design Vue layout/cards/tables/forms
- KlineCharts rendering
- AI/Vibe Coding panels
- API service wrappers
- Monaco editor shell

Frontend must not contain MT5 credentials, broker credentials, Python strategy execution, or local MQL5 Files scraping logic.

## Infra-owned modules

Infra owns glue and deployment:

- Cloudflare worker files
- workspace helper scripts
- dist sync from frontend to backend
- multi-repo pull/build/test commands
- optional remote dashboard deployment automation

Infra must not contain trading strategy logic.

## Docs-owned modules

Docs owns explanations, contracts, runbooks, phase designs, and maintenance guides.

Docs should be the first place to update when a code change modifies:

- API shape
- repo boundaries
- operator workflow
- safety gates
- CI rules
- phase implementation status
