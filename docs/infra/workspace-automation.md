# Workspace 自动化

`qg-workspace.py` 是四仓库的本地联动入口。

## 命令说明

- `status`：查看四个仓库的 Git 状态。
- `pull`：对四个仓库执行 `git pull --ff-only`。
- `test`：运行 backend tests、frontend build、docs link check。
- `build-frontend`：安装/更新前端依赖并执行 `npm run build`。
- `sync-frontend-dist`：把 `QuantGodFrontend/dist` 复制到 `QuantGodBackend/Dashboard/vue-dist`。
- `verify`：检查仓库边界是否符合拆分约定。

## 本地配置

`workspace/quantgod.workspace.example.json` 可以提交。`workspace/quantgod.workspace.json` 是本机路径配置，默认被 `.gitignore` 忽略。

## 使用建议

每次跨仓库改动后至少执行：

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

如果改了前端并需要后端 `/vue/` 立即使用，再执行：

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```
