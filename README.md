# QuantGodDocs

QuantGodDocs is the documentation and contract hub for the QuantGod four-repository system.

This repository is the source of truth for architecture, API contracts, runbooks, safety boundaries, and phase history. It does not contain backend runtime code, Vue source, deployment automation, credentials, MT5 account data, Telegram tokens, DeepSeek keys, wallet keys, or generated runtime evidence.

## System Summary

QuantGod v2.5 is a local-first USDJPY autonomous research and execution-governance system:

```text
Live Lane: USDJPYc / RSI_Reversal / LONG / cent account
MT5 Shadow Lane: USDJPY multi-strategy simulation and tester research
Polymarket Shadow Lane: simulated ledger and event-risk context
Agent: autonomous daily todo, daily review, promotion, demotion, rollback
Hard guards: runtime freshness, fastlane quality, spread, news, loss, and rollback
```

Core principle:

```text
Live narrow. Simulation broad. Promotion fast. Rollback hard.
```

## Repository Map

| Repository | Responsibility | Must not contain |
|---|---|---|
| `QuantGodBackend` | MT5 assets, local API, Agent tools, USDJPY replay/walk-forward/lifecycle, Telegram push | Vue source, Cloudflare source, long-form docs hub |
| `QuantGodFrontend` | Vue operator workbench and `/api/*` client modules | MT5 source, Python tools, direct runtime file reads |
| `QuantGodInfra` | Workspace automation, launchd, Docker local, dist sync, optional Cloudflare/Cloud Sync | Trading logic, live preset policy, product docs hub |
| `QuantGodDocs` | Architecture, API contracts, runbooks, safety, maintenance records | Runtime output, credentials, execution code |

## Start Reading

| Topic | Document |
|---|---|
| Four-repo architecture | [Repo split architecture](docs/architecture/repo-split.md) |
| Module boundaries | [Module boundaries](docs/architecture/module-boundaries.md) |
| Repo linkage contract | [Linkage contract](docs/architecture/linkage-contract.md) |
| API contract | [Backend API contract](docs/backend/api-contract.md) |
| Safety boundaries | [Backend safety boundaries](docs/backend/safety-boundaries.md) |
| Local runbook | [Local runbook](docs/ops/runbook-local.md) |
| Frontend workbench | [Frontend workbench](docs/frontend/workbench.md) |
| Infra automation | [Workspace automation](docs/infra/workspace-automation.md) |

## Current v2.5 Operating Documents

| Area | Document |
|---|---|
| Autonomous multi-lane Agent | [QuantGod v2.5 three-lane Agent](docs/ops/usdjpy-cent-autonomous-multilane-agent.md) |
| USDJPY autonomous governance | [USDJPY autonomous Agent](docs/ops/usdjpy-autonomous-agent.md) |
| USDJPY live loop and daily autopilot | [USDJPY live loop daily autopilot](docs/ops/usdjpy-live-loop-daily-autopilot.md) |
| USDJPY strategy policy lab | [USDJPY strategy policy lab](docs/ops/usdjpy-strategy-policy-lab.md) |
| USDJPY runtime evolution core | [USDJPY runtime evolution core](docs/ops/usdjpy-runtime-evolution-core.md) |
| Causal replay simulator | [USDJPY bar replay simulator](docs/ops/usdjpy-bar-replay-simulator.md) |
| Strategy lab API | [USDJPY strategy lab API](docs/backend/usdjpy-strategy-lab-api.md) |
| EA lab runbook | [USDJPY EA lab runbook](docs/ops/usdjpy-ea-lab-runbook.md) |

## Phase and Maintenance Records

| Phase | Document |
|---|---|
| Phase 1 | [Phase 1](docs/phases/phase1.md) |
| Phase 2 | [Phase 2](docs/phases/phase2.md) |
| Phase 3 | [Phase 3](docs/phases/phase3.md) |
| USDJPY strategy factory | [USDJPY EA strategy factory](docs/phases/usdjpy-ea-strategy-factory.md) |
| Completion matrix | [Docs completion matrix](docs/maintenance/docs-completion-matrix.md) |
| Changelog | [Changelog](docs/maintenance/changelog.md) |

Recent maintenance records:

- [P3-17 USDJPY evolution core](docs/maintenance/p3-17-usdjpy-evolution-core.md)
- [P3-18 replay fidelity hardening](docs/maintenance/p3-18-replay-fidelity-hardening.md)
- [P3-19 bar replay simulator](docs/maintenance/p3-19-usdjpy-bar-replay-simulator.md)
- [P3-20 autonomous walk-forward promotion gate](docs/maintenance/p3-20-autonomous-walk-forward-promotion-gate.md)
- [P3-21 three-lane autonomous lifecycle](docs/maintenance/p3-21-usdjpy-cent-autonomous-multilane-agent.md)

## API and Contract Files

- [API contract JSON](docs/contracts/api-contract.json)
- [API contract markdown](docs/backend/api-contract.md)
- [Repo manifest schema](docs/contracts/repo-manifest.schema.json)

When a backend `/api/*` endpoint changes, update:

1. `docs/contracts/api-contract.json`
2. `docs/backend/api-contract.md`
3. Any affected frontend or ops documentation

## Safety Doctrine

Documentation should consistently reflect these constraints:

- Live Lane is limited to `USDJPYc / RSI_Reversal / LONG`.
- MT5 Shadow Lane may simulate and rank multiple USDJPY strategies, but cannot seize the live route.
- Polymarket is shadow-only and event-context-only; no real wallet, signing, USDC order, redeem, or private key.
- Telegram is push-only; Telegram command execution is out of scope.
- DeepSeek explains, summarizes, and reviews; it does not approve live execution or override rollback.
- `QG_AUTO_MAX_LOT=2.0` is an upper bound, not a fixed lot size.
- Runtime stale, fastlane degraded, news block, abnormal spread, daily loss, and loss streak gates remain hard stops.
- Agent may write controlled patch evidence through staged governance; it must not mutate source code or live preset directly.

## Local Checks

```bash
cd /Users/bowen/Desktop/Quard/QuantGodDocs
python3 scripts/check_docs_quality_gate.py --root .
python3 scripts/check_docs_links.py --root .
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python3 -m unittest discover tests -v
```

For contract-only validation:

```bash
python3 scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json
```

## Maintenance Rules

1. Use readable multi-line Markdown and Python; do not compress whole files into one long line.
2. Keep relative links valid.
3. Keep contract JSON parseable and synchronized with backend routes.
4. Safety documentation takes precedence over feature descriptions.
5. Do not document future work as completed. Strategy JSON DSL, GA Evolution, and Telegram Gateway must remain next-phase tasks until implemented.
6. Do not include credentials, runtime evidence, account identifiers, wallet keys, or tokens.
7. Prefer natural-language operator wording over internal endpoint names in user-facing docs.
