# 模块边界

## Backend 边界

Backend 负责：

- MT5/MQL5 EA 和 preset 安全检查。
- Node dashboard server。
- `/api/*` 本地 API。
- Python tools：AI analysis、Vibe Coding、ParamLab、Governance、Notify、Kline overlay。
- CI 中的 backend safety guard、API contract tests、Python unittest/pytest。

Backend 不负责：

- Vue 源码维护。
- Cloudflare 或 workspace 自动化。
- 文档中心的长文档维护。

## Frontend 边界

Frontend 负责：

- Vue 3 operator workbench。
- Ant Design Vue layout。
- KlineCharts。
- Monaco Editor。
- `src/services/*` API client。
- 前端 contract guard：禁止直接读 `QuantGod_*.json/csv`。

Frontend 不负责：

- 读取本地 runtime 文件。
- 写 MT5 preset。
- 发送订单、平仓、撤单。
- 直接读取 backend repo 内部文件路径。

## Infra 边界

Infra 负责：

- 四仓库 workspace 配置。
- 批量 pull/status/test/verify。
- frontend `dist/` 到 backend `Dashboard/vue-dist` 的同步。
- Cloudflare 或静态发布配置。

Infra 不负责：

- 交易逻辑。
- UI 组件业务细节。
- 后端 API handler 实现。

## Docs 边界

Docs 负责：

- 架构说明。
- API contract。
- 安全边界。
- Phase 文档。
- 运维 runbook。
- 文档链接和 contract 检查。

Docs 不负责：

- 可执行交易代码。
- runtime artifact。
- 账号、token、API key。
