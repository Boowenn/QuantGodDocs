# Infra guide

## Repository

`Boowenn/QuantGodInfra`

## Responsibilities

- Multi-repo workspace commands
- Frontend dist sync to backend
- Cloudflare optional deployment
- Local deployment helpers
- Linkage verification

## Workspace commands

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## Cloudflare

Cloudflare remains optional and should not be part of the default live HFM workflow. Use it only for remote read-only viewing.
