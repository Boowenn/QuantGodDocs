# Backend 安全边界

QuantGod 的核心价值是本地优先、安全受控和逐步治理。安全边界优先级高于功能上线速度。

## 不可突破规则

- AI Analysis V1/V2 只能作为 advisory evidence。
- Vibe Coding 生成策略只能进入 research-only backtest。
- Telegram 只能 push-only，不能接受交易命令。
- Frontend 不能直接读 runtime JSON/CSV，也不能写 runtime 文件。
- Backend 新增 endpoint 默认 read-only，除非明确标记为 guarded-control。
- guarded-control 仍必须受 Backend、EA、dryRun、Kill Switch 和手动授权约束。

## MT5 / HFM 边界

MT5 read-only bridge 可以读取账户、持仓、订单、quote、symbols、kline 和 snapshot。它不能：

- 下单。
- 平仓。
- 撤单。
- symbol select。
- 存储凭据。
- 修改 live preset。

MT5 trading bridge 即使存在 action route，也必须默认被 dryRun、Kill Switch 和 authorization lock 锁住。

## AI 边界

AI Analysis 的输出可以写入 Governance evidence 文件，但不能修改 Governance 决策，也不能改变 keep/demote/promote 结果。

Phase 1 的 Technical/Risk/Decision 三智能体是 advisory-only；Phase 3 的 News/Sentiment/Bull/Bear/Decision V2 也是 advisory-only。Bull/Bear 辩论只能辅助 DecisionAgent reasoning，不能成为交易触发器。

## Vibe Coding 边界

自然语言生成的 Python 策略必须经过：

```text
生成 -> 安全检查 -> research-only backtest -> ParamLab -> Governance -> Version Gate -> 手动授权
```

禁止从 Vibe Coding 直接进入 live preset 或 EA 交易参数。

## Telegram 边界

Telegram Bot 只负责推送：

- AI 分析摘要。
- 风控事件。
- 交易记录。
- Daily digest。
- Governance 状态。

Telegram 不能接受 `/buy`、`/sell`、`/close`、`/cancel` 或任何交易命令。
