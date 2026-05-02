# Phase 3：Vibe Coding、AI V2 与 K 线增强

Phase 3 是可选增强阶段，包含 Vibe Coding 策略工作台、AI 多智能体 V2 和 K 线增强。

## Module H：Vibe Coding 策略工作台

核心流程：

```text
自然语言描述
  -> AI 生成 Python BaseStrategy
  -> 安全检查
  -> Monaco Editor 微调
  -> research-only backtest
  -> AI 回测分析
  -> 迭代
```

Vibe Coding 到实盘必须经过：

```text
回测 -> ParamLab -> Governance -> Version Gate -> 手动授权
```

## Module I：AI 多智能体 V2

V2 从 3 Agent 扩展为多 Agent：

- TechnicalAgent
- RiskAgent
- NewsAgent
- SentimentAgent
- BullAgent
- BearAgent
- DecisionAgent V2

编排分为采集、辩论、决策三轮。Bull/Bear 辩论只能作为 DecisionAgent 的参考。

## Module J：K 线增强

K 线增强包括：

- AI BUY/SELL/HOLD overlay。
- Vibe Coding 指标 overlay。
- 30s 轮询实时行情配置。

## 验收状态

Phase 3 已进入可用状态。后续维护重点是 strategy snapshot、backtest run versioning 和 Frontend 工作台模块化。
