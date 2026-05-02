# Workspace Automation

## 推荐目录结构

```text
C:\QuantGod\
  QuantGodBackend\
  QuantGodFrontend\
  QuantGodInfra\
  QuantGodDocs\
```

## 常用命令

```powershell
cd C:\QuantGod\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## test 命令应该覆盖

- Backend Python unittest。
- Backend Node/API contract tests。
- Backend `tools/ci_guard.py`。
- Frontend contract guard。
- Frontend unit tests。
- Frontend build。
- Docs link/contract checks。

Node/API contract tests 必须硬失败，不能 `check=False`。
