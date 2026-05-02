# 本地部署流程

本地部署的目标是：后端 server 在 `8080` 提供 API 和 `/vue/` 页面，前端源码仍由 `QuantGodFrontend` 独立维护。

## 步骤

1. 在 `QuantGodFrontend` 构建：

```powershell
npm run build
```

2. 在 `QuantGodInfra` 同步 dist：

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

3. 在 `QuantGodBackend` 启动 dashboard：

```powershell
Dashboard\start_dashboard.bat
```

macOS 可按本机脚本或 Node server 方式启动。

4. 打开页面：

```text
http://127.0.0.1:8080/vue/
```

## 回滚

如果前端 dist 有问题，重新从稳定的 `QuantGodFrontend` commit 构建并同步即可。`QuantGodBackend/Dashboard/vue-dist` 是本机 ignored 运行产物，不再作为 backend Git 提交内容回滚。
