# P3-1 Docker/local-dev stack

P3-1 adds a local Docker Compose development stack for the existing four-repository workspace.

This page documents only local development orchestration. It does not introduce webhook/email delivery, broker adapters, user accounts, billing, credits, public ingress, credential storage, or live preset mutation.

## Scope

The stack has two services:

| Service | Repo | Role | Host URL |
| --- | --- | --- | --- |
| `backend` | `QuantGodBackend` | Local Node dashboard API plus Python SQLite state CLI | `http://127.0.0.1:8080` |
| `frontend` | `QuantGodFrontend` | Vite operator workbench with `/api` proxy to backend | `http://127.0.0.1:5173` |

SQLite remains a backend-local runtime file under the backend container volume:

```text
/app/runtime/quantgod_state.sqlite
```

## Local-only defaults

The Compose file binds host ports to loopback only:

```text
127.0.0.1:${QG_BACKEND_PORT:-8080}:8080
127.0.0.1:${QG_FRONTEND_PORT:-5173}:5173
```

The backend container is started with explicit safety defaults:

```text
QG_LOCAL_ONLY=1
QG_DRY_RUN=1
QG_KILL_SWITCH_LOCKED=1
QG_ORDER_SEND_ALLOWED=0
QG_LIVE_PRESET_MUTATION_ALLOWED=0
QG_CREDENTIAL_STORAGE_ALLOWED=0
QG_TELEGRAM_COMMANDS_ALLOWED=0
```

No Docker service is added for webhook, email, broker adapter, billing, credits, Postgres, MySQL, or public gateway.

## Files

Backend:

```text
Dockerfile.local
docker/local-entrypoint.sh
.dockerignore
tests/node/test_docker_local_files.mjs
```

Frontend:

```text
Dockerfile.local
vite.config.local.js
.dockerignore
tests/docker_local_vite_config_guard.mjs
```

Infra:

```text
docker/compose.local.yml
docker/.env.local.example
scripts/qg-docker-local.py
tests/test_docker_local.py
.github/workflows/docker-local.yml
```

## Commands

Run from `QuantGodInfra`:

```powershell
Copy-Item docker\.env.local.example docker\.env.local
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py doctor
python scripts\qg-docker-local.py build
python scripts\qg-docker-local.py up
python scripts\qg-docker-local.py ps
python scripts\qg-docker-local.py logs
python scripts\qg-docker-local.py down
```

The `static-check` command must pass before the helper runs Docker Compose. It checks loopback-only host ports, required safety flags, and absence of out-of-scope P3-2/P3-3/P4 services.

## Health checks

Backend health uses:

```text
/api/state/status
```

Frontend waits for the backend health check before starting. The frontend Docker-specific Vite config proxies only `/api` to the backend service and does not proxy `/QuantGod_*.json` or `/QuantGod_*.csv`.

## Completion gate

P3-1 is complete when all of the following pass:

```powershell
# Backend
node --check Dashboard\dashboard_server.js
node --check Dashboard\state_api_routes.js
npm test
python -m unittest discover tests -v

# Frontend
node --check vite.config.local.js
npm test
npm run build

# Infra
python -m py_compile scripts\qg-docker-local.py
python -m unittest discover tests -v
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py doctor

# Docs
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```
