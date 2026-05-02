# Phase 2：Vue 收尾、统一 API、Telegram 与 CI 增强

Phase 2 目标是把 Phase 1 的散装能力整合成干净的工作台和统一 API。

## Module D：Vue 前端迁移收尾

Vue workbench 成为唯一 active operator frontend。旧 Dashboard 归档或重定向，不再作为 active fallback。

## Module E：后端 API 轻量统一

Backend 将 runtime JSON/CSV 包装成 `/api/*`，Frontend 不再直接读取本地文件。

典型 endpoint：

- `/api/governance/*`
- `/api/paramlab/*`
- `/api/trades/*`
- `/api/research/*`
- `/api/shadow/*`
- `/api/dashboard/*`

## Module F：Telegram 通知

Telegram 是 push-only，不接受命令，不触发交易。

## Module G：CI/CD 增强

Phase 2 增加 integration test、coverage summary、API contract tests 和 split boundary guard。

## 验收状态

## 安全边界

- Frontend 所有数据访问必须通过 `/api/*`，禁止直接读取本地 JSON/CSV 文件。
- `apiClient.js` 强制校验路径前缀、拒绝绝对 URL 和运行时文件路径。
- Telegram 为 push-only，不接受交易命令，不能绕过 Kill Switch 或授权锁。
- CI guard 矩阵覆盖 API contract、workspace boundary、domain workspace 等 18 个检查。
- 不引入 SQLite、Docker、Webhook 等新基础设施组件之前，API 安全边界不得弱化。

## 验收状态

Phase 2 已验收。
