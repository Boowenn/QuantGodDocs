# P3-18 维护记录：USDJPY 回放精度加固

P3-18 在 P3-17 自学习闭环基础上，修正回放证据的计量口径，避免把账面金额和交易质量指标混在一起。

## 本阶段完成

- 回放主口径统一为 `R` 倍数；
- `pips` 作为辅助口径；
- `USC` 只作为账面参考；
- 错失机会增加 15 / 30 / 60 / 120 分钟后验窗口；
- 盈利早出增加利润捕获比例；
- 新增 `current`、`relaxed_entry_v1`、`let_profit_run_v1` 三组候选对比；
- 参数候选新增 `expectedImpact`、`riskDelta`、`replayVariant` 和 `evidenceQuality`；
- 实盘配置提案透传预期影响和风险变化；
- 前端展示回放候选对比，但仍保持只读。

## 安全边界

P3-18 不会：

- 下单；
- 平仓；
- 撤单；
- 修改订单；
- 修改 MT5 live preset；
- 自动应用参数候选。

所有候选只能进入 replay、tester-only、shadow 或 P3-20 自主治理门。`autoApplyAllowed` 采用 `stage_gated`，不能直接绕过机器硬风控。

## 后续

P3-18 仍不是完整高保真 tick/bar 回放。后续 P3-19 应补：

- 逐 bar 重放 RSI、session、spread、news 和 cooldown；
- walk-forward 对比；
- 参数候选的收益、回撤和错失机会减少量；
- live config proposal 的量化预期影响。
