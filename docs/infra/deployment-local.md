# Local deployment

## Dev mode

1. Start backend dashboard server.
2. Start frontend Vite dev server.
3. Browser talks to Vite; Vite proxies API calls to backend.

## Backend-served mode

1. Build frontend.
2. Sync frontend dist into backend.
3. Start backend dashboard server.
4. Browser opens `http://localhost:8080/vue/`.

Commands:

```powershell
cd QuantGodFrontend
npm run build
cd ..\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
cd ..\QuantGodBackend
Dashboard\start_dashboard.bat
```
