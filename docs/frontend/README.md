# Frontend guide

## Repository

`Boowenn/QuantGodFrontend`

## Stack

- Vue 3
- Vite
- Ant Design Vue
- KlineCharts
- Monaco Editor

## Dev mode

```powershell
cd QuantGodBackend
Dashboard\start_dashboard.bat

cd ..\QuantGodFrontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173/vue/
```

## API calls

Frontend should use relative API paths:

```js
fetch('/api/governance/advisor')
```

The Vite proxy forwards to backend in dev. Backend-served mode shares the same origin.

## Build

```powershell
npm run build
```

The output is `dist/`. Infra sync copies it into backend.

## Component ownership

- Workspaces and cards are frontend-owned.
- API shape belongs to backend and docs.
- Any direct file read should be replaced with `/api/*`.
