# 本地运行 Runbook

本文档用于四仓库拆分后的本地日常操作。推荐目录结构：

```text
QuantGod/
  QuantGodBackend/
  QuantGodFrontend/
  QuantGodInfra/
  QuantGodDocs/
```

## 拉取四个仓库

```powershell
cd C:\QuantGod\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
```

## 运行联动测试

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
```

该命令会串联 backend unittest、backend Node/API contract test、`tools/ci_guard.py`、frontend build/contract、infra 自检等关键步骤。任何一环失败都应该先修复，不要继续同步 dist。

## 构建并同步前端

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

同步方向固定为：

```text
QuantGodFrontend/dist
-> QuantGodBackend/Dashboard/vue-dist
```

Frontend 仓库保留源码，Backend 仓库只保留可服务的构建产物。

## 启动本地 Dashboard

在 `QuantGodBackend` 中使用 backend README 记录的启动脚本或 Node server，然后打开：

```text
http://127.0.0.1:8080/vue/
```

## 常用 Smoke Test

```powershell
# Backend
python tools\run_ai_analysis.py config
python tools\run_ai_analysis_v2.py config
python tools\run_vibe_coding.py config
python tools\run_notify.py config

# Frontend
npm run contract
npm test
npm run build

# Docs
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
```

## 处理失败的顺序

1. 先看失败仓库的 CI guard 或 contract guard 输出。
2. 如果是 `/api/*` route 变化，先更新 Backend，再更新 Docs contract，最后更新 Frontend service。
3. 如果是前端样式或组件问题，只改 `QuantGodFrontend`，不要把源码重新放回 Backend。
4. 如果是 workspace 同步问题，只改 `QuantGodInfra`。
