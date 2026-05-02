# 前端 API Client 规则

Frontend 必须把所有运行时数据访问封装在 `src/services/*` 中。

## 允许

```js
await fetch('/api/governance/advisor')
await fetch('/api/ai-analysis/latest')
await fetch('/api/vibe-coding/strategies')
```

## 禁止

```js
await fetch('/QuantGod_GovernanceAdvisor.json')
await fetch('/QuantGod_TradeJournal.csv')
await fetch('/MQL5/Files/QuantGod_Dashboard.json')
```

## 组件约束

Vue component 只调用 service function，不直接写 raw fetch。这样做可以统一：

- base URL。
- error handling。
- retry / timeout。
- loading state。
- API contract guard。

## Contract 更新顺序

当 Backend route 变化时：

1. Backend 新增或修改 route。
2. Docs 更新 `docs/contracts/api-contract.json`。
3. Docs 重新生成 `docs/backend/api-contract.md`。
4. Frontend service wrapper 消费新 endpoint。
5. Frontend CI 运行 contract guard。
