# Frontend 文档

Frontend 是 QuantGod 的 Vue operator workbench。它只负责 UI 和用户交互，不直接接触 MT5 runtime 文件，不保存凭据，也不触发交易控制面。

## 关键入口

- [工作台结构](workbench.md)
- [API Client 规则](api-client.md)

## 前端维护原则

1. 所有数据都通过 `src/services/*` 调用 `/api/*`。
2. UI component 不直接读取 `/QuantGod_*.json` 或 `/QuantGod_*.csv`。
3. UI 可以展示文件名文本，但不能把文件名作为本地 fetch 路径。
4. 大型页面逐步拆成 workspaces，避免继续扩大 `App.vue`。
5. 前端 CI 必须包含 API contract guard 和 build。
