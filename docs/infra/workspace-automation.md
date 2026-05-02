# Workspace automation

## Workspace file

`QuantGodInfra/workspace/quantgod.workspace.json` defines paths:

```json
{
  "backend": "C:/QuantGod/QuantGodBackend",
  "frontend": "C:/QuantGod/QuantGodFrontend",
  "infra": "C:/QuantGod/QuantGodInfra",
  "docs": "C:/QuantGod/QuantGodDocs"
}
```

## Commands

- `status` — show Git status for all repos.
- `pull` — fast-forward pull all repos.
- `test` — run backend tests, frontend build, docs link check.
- `build-frontend` — install/build frontend.
- `sync-frontend-dist` — copy frontend `dist/` into backend `Dashboard/vue-dist`.
- `verify` — confirm split boundaries.

## CI relationship

Each repo runs its own CI. Cross-repo release coordination is done locally through this workspace helper.
