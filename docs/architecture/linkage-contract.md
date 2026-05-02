# 跨仓库联动契约

## 契约摘要

| 链路 | 生产者 | 消费者 | 机制 |
|---|---|---|---|
| Backend REST API | `QuantGodBackend` | `QuantGodFrontend` | localhost `/api/*` |
| Frontend static dist | `QuantGodFrontend` | `QuantGodBackend` | Infra sync 到 `Dashboard/vue-dist` |
| Cloudflare remote assets | `QuantGodInfra` | 可选远程展示 | Wrangler deploy |
| 文档 | `QuantGodDocs` | 四个仓库 | README 指针和 Markdown 链接 |
| 工作区自动化 | `QuantGodInfra` | 四个仓库 | `scripts/qg-workspace.py` |

## Backend API base

默认后端 API：

```text
http://127.0.0.1:8080/api
```

Frontend 源码应使用相对路径 `/api/*`。Vite dev server 通过 proxy 转发到 backend；backend-served 模式下，UI 和 API 同源。

## Frontend 构建同步

Frontend 构建输出：

```text
QuantGodFrontend/dist
```

Infra 同步目标：

```text
QuantGodBackend/Dashboard/vue-dist
```

同步后，后端 server 页面入口：

```text
http://localhost:8080/vue/
```

## Workspace 命令

```powershell
cd QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## 版本顺序

UI 小改只提交到 `QuantGodFrontend`。Backend API 改动要同时更新 backend tests 和 Docs。涉及前端消费的 API 变化建议顺序：

1. Backend 先增加兼容字段或新 endpoint。
2. Docs 更新 API contract。
3. Frontend 消费新字段或 endpoint。
4. Infra 只有构建/同步/部署方式改变时才改。

## 破坏性 API 变化

尽量避免破坏性变化。确实需要时：

1. 先增加新 endpoint 或 versioned field。
2. 旧 endpoint 至少保留一个前端版本周期。
3. 更新 Docs 和 Frontend。
4. 确认前端不再使用后，再删除旧 endpoint。
