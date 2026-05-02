# Phase 3 总结

Phase 3 增加更高层的研究能力，但仍不改变实盘安全链路。

## Module H：Vibe Coding

Vibe Coding 把自然语言策略想法转换为 sandboxed Python strategy code，然后进入 research-only backtest 和 AI 分析。

实盘晋级路径仍然固定为：

```text
Backtest -> ParamLab -> Governance -> Version Gate -> manual authorization
```

任何 generated strategy 都不能直接进入 live preset，也不能生成交易命令。

## Module I：AI Analysis V2

已落地方向：

- `NewsAgent`
- `SentimentAgent`
- `BullAgent`
- `BearAgent`
- `DecisionAgentV2`
- 本地 RAG-like memory。
- debate-style reasoning。

Bull / Bear debate 只为 DecisionAgent 提供 evidence。它不能触发交易、修改 Governance 决策或绕过 Kill Switch。

## Module J：K-line Enhancement

已落地方向：

- AI BUY / SELL / HOLD overlay 数据。
- Vibe indicator overlay descriptors。
- realtime polling config。

这些增强只影响展示和研究，不影响 MT5 live execution。

## 安全边界

Vibe Coding 生成代码不能实盘交易。RAG memory 只保存分析案例和 reasoning，不保存账户信息、API key、Telegram token 或 MT5 凭据。
