# Cross-repo linkage contract

## Contract summary

| Link | Producer | Consumer | Mechanism |
|---|---|---|---|
| Backend REST API | `QuantGodBackend` | `QuantGodFrontend` | `/api/*` over localhost |
| Frontend static dist | `QuantGodFrontend` | `QuantGodBackend` | Infra sync to `Dashboard/vue-dist` |
| Cloudflare remote assets | `QuantGodInfra` | optional operator | Wrangler deploy |
| Documentation | `QuantGodDocs` | all repos | Markdown links and repo README pointers |
| Workspace automation | `QuantGodInfra` | all repos | `scripts/qg-workspace.py` |

## Backend API base

Default backend API:

```text
http://127.0.0.1:8080/api
```

Frontend source should call relative `/api/*` URLs. In Vite development, the proxy forwards those requests to backend. In backend-served production/local mode, the UI and API share the same origin.

## Frontend build sync

Frontend builds to:

```text
QuantGodFrontend/dist
```

Infra sync copies that directory into:

```text
QuantGodBackend/Dashboard/vue-dist
```

The backend server then serves the UI at:

```text
http://localhost:8080/vue/
```

## Workspace commands

```powershell
cd QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## Versioning policy

Small UI-only changes can be committed only to `QuantGodFrontend`. Backend API changes should update backend tests and docs. Any API contract change that affects frontend should be merged in this order:

1. Backend adds backwards-compatible API field or endpoint.
2. Docs update records the contract.
3. Frontend consumes the new field or endpoint.
4. Infra only changes if build/sync/deploy behavior changes.

## Breaking API changes

Avoid breaking API changes. When unavoidable:

1. Add a new endpoint or versioned field first.
2. Keep the old endpoint alive for at least one frontend release.
3. Update docs and frontend.
4. Remove old endpoint only after frontend no longer uses it.
