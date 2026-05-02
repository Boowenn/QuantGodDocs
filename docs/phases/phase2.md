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

Phase 2 已验收。后续维护重点是保持 Frontend 零直接文件读取和 Telegram push-only。
