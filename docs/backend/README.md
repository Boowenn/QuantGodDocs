# Backend 文档入口

Backend 是 QuantGod 的本地 API、MT5 runtime、AI 分析、Vibe Coding、Governance 和 ParamLab 中心。

核心文档：

- [API Contract / 接口契约](api-contract.md)
- [安全边界](safety-boundaries.md)

核心原则：

1. API local-first，不作为公网交易 API。
2. 读数据和 advisory 分析可以通过 `/api/*` 暴露给 Vue。
3. 下单、平仓、撤单、preset 修改不能由 AI、Telegram、Vibe Coding 或前端触发。
4. Backend CI guard 只检查 backend/MQL5/API/safety，不再检查 Vue 源码。
