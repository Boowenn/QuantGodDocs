# 前端 API Client

前端 API client 只负责调用后端 facade，不直接读取本地文件。

## 基本规则

- 浏览器代码使用相对路径 `/api/*`。
- Vite dev server 通过 proxy 转发到 `QG_BACKEND_URL`。
- backend-served 模式下，UI 与 API 同源。
- 对旧 `/QuantGod_*.json` fallback 的使用应逐步减少，只作为兼容兜底。

## Service modules

- `src/services/api.js`：主工作台数据读取。
- `src/services/phase1Api.js`：AI Analysis V1 与 K 线基础。
- `src/services/phase2Api.js`：统一 API 与通知。
- `src/services/phase3Api.js`：策略工坊、AI V2、K 线增强。

## 错误处理

API 调用失败时，前端应显示“证据缺失/证据过期/读取失败”的可解释状态，而不是空白卡片或不明 `undefined`。如果后端返回 safety envelope，前端应保留关键安全字段用于展示和审计。
