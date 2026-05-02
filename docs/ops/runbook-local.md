# Local operator runbook

## Normal research startup

```powershell
cd QuantGodBackend
Start_QuantGod_MT5_HFM_Shadow.bat
```

## Live pilot startup

Use only when the live pilot preset and broker environment are intentionally selected:

```powershell
cd QuantGodBackend
Start_QuantGod_MT5_HFM_LivePilot.bat
```

## Frontend update after UI change

```powershell
cd QuantGodFrontend
npm run build
cd ..\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

## Before merging backend changes

```powershell
cd QuantGodBackend
python -m unittest discover tests -v
python -m pytest tests -q --cov=tools --cov-report=term-missing
node --test tests/node/*.mjs
```

## Before merging frontend changes

```powershell
cd QuantGodFrontend
npm install
npm run build
```
