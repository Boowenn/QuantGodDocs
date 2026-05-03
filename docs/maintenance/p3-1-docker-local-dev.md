# P3-1 maintenance note: Docker/local-dev stack

## Purpose

P3-1 gives the four-repository QuantGod workspace a reproducible local Docker development stack.

The stack is intentionally narrow:

- Backend local API and SQLite state layer.
- Frontend Vite operator workbench.
- Infra-owned Compose orchestration and static guard.
- Docs-owned runbook and completion gate.

## Non-goals

P3-1 must not add:

- Webhook or email notification delivery.
- Multi-market broker adapter.
- Live trading execution path.
- Credential storage or secrets in Compose.
- Public internet ingress.
- User system, billing, or credits.
- Postgres, MySQL, Redis, or other non-SQLite state service.

Those items remain outside P3-1 and belong to later phase gates if approved.

## Safety invariants

The Compose file must keep these invariants:

```text
host ports bound to 127.0.0.1 only
QG_LOCAL_ONLY=1
QG_DRY_RUN=1
QG_KILL_SWITCH_LOCKED=1
QG_ORDER_SEND_ALLOWED=0
QG_LIVE_PRESET_MUTATION_ALLOWED=0
QG_CREDENTIAL_STORAGE_ALLOWED=0
QG_TELEGRAM_COMMANDS_ALLOWED=0
```

The Docker helper must run `static-check` before invoking Compose operations. The static check is the P3-1 guardrail that prevents accidental public binding or out-of-scope service creep.

## Ownership

| Repo | Ownership |
| --- | --- |
| `QuantGodBackend` | Backend local Docker image and SQLite init entrypoint |
| `QuantGodFrontend` | Frontend local Docker image and Docker-only Vite config |
| `QuantGodInfra` | Compose file, Docker helper, CI static guard |
| `QuantGodDocs` | Runbook and maintenance note |

## Verification

Run these checks before committing P3-1:

```powershell
cd QuantGodBackend
node --check Dashboard\dashboard_server.js
node --check Dashboard\state_api_routes.js
npm test
python -m unittest discover tests -v

cd ..\QuantGodFrontend
node --check vite.config.local.js
npm test
npm run build

cd ..\QuantGodInfra
python -m py_compile scripts\qg-docker-local.py
python -m unittest discover tests -v
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py doctor

cd ..\QuantGodDocs
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

Optional runtime smoke test from `QuantGodInfra`:

```powershell
Copy-Item docker\.env.local.example docker\.env.local
python scripts\qg-docker-local.py build
python scripts\qg-docker-local.py up
python scripts\qg-docker-local.py ps
python scripts\qg-docker-local.py logs
python scripts\qg-docker-local.py down
```

Use `python scripts\qg-docker-local.py down --volumes` only when intentionally deleting the local SQLite runtime volume.
