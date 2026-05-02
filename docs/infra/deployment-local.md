# Local Deployment

## Build and Sync Frontend

```powershell
cd C:\QuantGod\QuantGodFrontend
npm install
npm run build

cd C:\QuantGod\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

Frontend `dist/` 会同步到：

```text
QuantGodBackend/Dashboard/vue-dist
```

然后由 backend dashboard server 提供：

```text
http://127.0.0.1:8080/vue/
```

## Localhost Boundary

QuantGod operator dashboard 是 localhost/local-first 系统。不要把 backend dashboard server 暴露为公网交易 API。
