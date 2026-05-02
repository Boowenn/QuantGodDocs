# Phase 1：AI 分析、K 线与 CI 基础

Phase 1 交付了三条基础能力：AI 多智能体分析 V1、KlineCharts 图表、CI/CD 流水线。

## Module A：AI 多智能体分析引擎 V1

V1 使用三智能体结构：

```text
Market snapshot
  -> TechnicalAgent + RiskAgent 并行
  -> DecisionAgent 串行综合
  -> FullAnalysisReport
  -> Governance evidence
```

AI 结果只能作为参考和 Governance evidence，不能直接执行交易，不能绕过 Kill Switch、授权锁、dryRun 或新闻过滤器。

## Module B：K 线图表

K 线基础能力包括：

- `/api/mt5-readonly/kline`
- `/api/mt5-readonly/trades`
- `/api/shadow-signals`
- MA、RSI、MACD、Bollinger、Volume 指标。
- 交易点和 Shadow signal overlay。

## Module C：CI/CD

Phase 1 建立了 push/PR 自动测试基础，包括 Python tests、Node API tests、Vue build 和 static guard。

## 验收状态

Phase 1 已验收。后续维护重点是保持 AI advisory-only 和 K 线 read-only 数据边界。
