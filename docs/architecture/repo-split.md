# QuantGod repository split architecture

## Goal

QuantGod used to live in one mixed repository containing backend, frontend, infra, docs, MQL5 source, Python tools, Vue source, Cloudflare files, and deployment notes. The new structure splits ownership into four repositories so future changes can be smaller, safer, and easier to review.

## Repositories

| Repository | Responsibility | Should contain | Should not contain |
|---|---|---|---|
| `QuantGodBackend` | Trading/research backend | `MQL5/`, `Dashboard/`, `tools/`, `tests/`, local launchers | Vue source, Cloudflare worker source, full docs tree |
| `QuantGodFrontend` | Operator UI | Vue source, Vite config, UI components, frontend CI | MQL5, Python tools, backend runtime JSON/CSV |
| `QuantGodInfra` | Workspace and deployment automation | Cloudflare, multi-repo scripts, dist sync, deployment helpers | business logic, Vue components, strategy code |
| `QuantGodDocs` | Canonical documentation | Markdown docs for all repos, contracts, runbooks | runtime data, credentials, generated ledgers |

## Why this split

The split maps to actual maintenance boundaries:

- backend changes often affect safety, MT5 guards, data contracts, Governance, ParamLab, AI agents, and tests;
- frontend changes often affect layout, charts, workspaces, table rendering, and API presentation;
- infra changes affect deployment, Cloudflare, workspace orchestration, and local automation;
- docs changes must be allowed without touching runtime code.

## Required linkage

The split is not four unrelated repos. They are linked by a clear contract:

1. Backend exposes local REST APIs under `/api/*`.
2. Frontend never reads local JSON/CSV directly; it calls backend APIs.
3. Frontend builds to `dist/`.
4. Infra copies `QuantGodFrontend/dist` to `QuantGodBackend/Dashboard/vue-dist` when a single local backend server should serve the UI.
5. Docs records API contracts, runbooks, safety boundaries, and phase history.

## Default local topology

```text
MT5/HFM terminal
  ↓ writes JSON/CSV under MQL5/Files
QuantGodBackend
  ↓ local API at http://127.0.0.1:8080/api/*
QuantGodFrontend dev server
  ↓ Vite proxy to backend, or dist copied into backend Dashboard/vue-dist
Operator browser
```

## Safety invariants after split

The split must not relax any QuantGod trading guard:

- AI analysis remains advisory only.
- Telegram remains push-only.
- Vibe Coding remains research/backtest-only.
- Governance and Version Gate remain advisory unless manually authorized.
- Kill Switch, authorization locks, dry-run, live preset mutation guards, and broker credential boundaries are unchanged.
