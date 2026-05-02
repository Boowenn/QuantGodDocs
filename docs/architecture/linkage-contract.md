# 仓库联动 Contract

四仓库通过明确的 contract 联动，而不是互相直接读文件。

## Frontend ↔ Backend

Frontend 只能通过 `/api/*` 访问 Backend 数据。

```text
Frontend service wrapper
  -> http://127.0.0.1:8080/api/*
  -> Backend Dashboard route
  -> Python tool / runtime JSON / runtime CSV / MT5 bridge
```

Frontend CI 必须禁止：

- `fetch('/QuantGod_*.json')`
- `fetch('/QuantGod_*.csv')`
- UI component 内直接绕过 service layer 的 raw fetch

## Infra ↔ Frontend ↔ Backend

Infra 负责把前端构建产物同步到 Backend：

```text
QuantGodFrontend/dist
  -> QuantGodBackend/Dashboard/vue-dist
```

Backend 仍通过本地 Node server 提供：

```text
http://127.0.0.1:8080/vue/
```

## Docs ↔ Backend

Docs 的 `docs/contracts/api-contract.json` 必须覆盖 Backend 当前 route surface。新增 Backend route 后，应执行：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```

## Safety linkage

所有仓库都必须遵守同一套安全默认值：

- `localOnly=true`
- `orderSendAllowed=false`
- `closeAllowed=false`
- `cancelAllowed=false`
- `credentialStorageAllowed=false`
- `livePresetMutationAllowed=false`
- `canOverrideKillSwitch=false`
- `telegramCommandExecutionAllowed=false`
