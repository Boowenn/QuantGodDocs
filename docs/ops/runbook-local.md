# 本地运行 Runbook

本 runbook 用于本地四仓库工作区日常检查。

## 拉取四仓库

```powershell
cd C:\QuantGod
foreach ($repo in 'QuantGodBackend','QuantGodFrontend','QuantGodInfra','QuantGodDocs') {
  cd C:\QuantGod\$repo
  git checkout main
  git pull origin main
}
```

## 验证 Backend

```powershell
cd C:\QuantGod\QuantGodBackend
python -m unittest discover tests -v
python tools\ci_guard.py
npm test
```

## 验证 Frontend

```powershell
cd C:\QuantGod\QuantGodFrontend
npm install
npm run contract
npm test
npm run build
```

## 验证 Infra

```powershell
cd C:\QuantGod\QuantGodInfra
python -m unittest discover tests -v
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## 验证 Docs

```powershell
cd C:\QuantGod\QuantGodDocs
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json
python -m unittest discover tests -v
```
