# Phase 1 总结

Phase 1 建立 QuantGod 的基础智能分析、K 线展示和 CI 护栏。

## Module A：AI Analysis V1

已落地内容：

- `TechnicalAgent`
- `RiskAgent`
- `DecisionAgent`
- `/api/ai-analysis/*`
- Governance evidence 输出

执行顺序是 Technical 与 Risk 并行，Decision 在两份 evidence 都准备好后再裁决。AI 输出只作为 advisory evidence，不能触发交易。

## Module B：K-line Charts

已落地内容：

- KlineCharts 集成。
- MT5 read-only K 线数据。
- trade markers。
- shadow signal overlays。
- 核心指标展示。

这些图表能力只消费 read-only 数据，不修改 MT5 状态。

## Module C：CI/CD

已落地内容：

- GitHub Actions。
- Python tests。
- Node/API tests。
- Vue build checks。
- safety guards。

## 安全边界

AI Analysis V1 不能绕过 Kill Switch、authorization lock、dryRun、news filter 或 live preset safety。所有分析结果只能进入证据链，不能直接进入执行链。
