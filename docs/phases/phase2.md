# Phase 2：统一 API 与通知

## 范围

Phase 2 把前端数据访问从直接文件读取推进到统一 `/api/*` facade，并加入 Telegram push-only 通知和 CI 增强。

主要模块：

- Vue 收尾与工作台整合。
- Backend API facade。
- Telegram notify service。
- Node API contract tests 与 coverage。

## 安全定位

Phase 2 的通知系统只推送消息，不接收命令；统一 API 只读读取 runtime 文件，不新增交易执行能力。

## 后端入口

- `Dashboard/phase2_api_routes.js`
- `tools/notify/`
- `tools/run_notify.py`
- `tests/node/test_phase2_api_routes.mjs`

## 前端入口

- `src/components/phase2/Phase2OperationsWorkspace.vue`
- `src/services/phase2Api.js`

## 验收重点

- `/api/governance/*`、`/api/paramlab/*`、`/api/trades/*`、`/api/research/*`、`/api/shadow/*`、`/api/dashboard/*` 可返回统一 envelope。
- Telegram 配置不进入 Git。
- 前端不再直接依赖旧 JSON/CSV 路径作为主数据源。
