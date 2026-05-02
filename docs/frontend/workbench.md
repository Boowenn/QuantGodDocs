# Vue Workbench

## 功能域

Vue Workbench 应按功能域拆分：

- Dashboard overview
- MT5 monitor
- Governance Advisor
- ParamLab
- Trades and journal
- Research / Shadow / Candidate
- AI Analysis V1
- AI Analysis V2 Debate
- Kline workspace
- Vibe Coding workspace
- Notify / Telegram status

## 维护原则

1. UI 组件不直接 `fetch()`，应调用 `src/services/*`。
2. 数据加载、错误处理、fallback 和 response normalization 应在 service layer 完成。
3. 新增 API 先更新 docs contract，再更新 service wrapper。
4. 大组件逐步拆分，不再把所有页面堆到 `App.vue`。
5. Ant Design Vue 是标准 UI 基础；KlineCharts 和 Monaco Editor 是专业组件，不要重写底层。
