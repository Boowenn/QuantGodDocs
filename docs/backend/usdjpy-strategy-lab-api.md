# USDJPY 策略实验室 API

`/api/usdjpy-strategy-lab/*` 是 USDJPY 单品种策略工厂的数据面。它只读或生成本地研究证据，不执行交易。

## 主要端点

| 端点 | 说明 |
|---|---|
| `GET /api/usdjpy-strategy-lab/status` | 当前 USDJPY 策略政策状态 |
| `POST /api/usdjpy-strategy-lab/run` | 重新生成策略政策 |
| `GET /api/usdjpy-strategy-lab/catalog` | 三条新增 shadow 策略目录 |
| `GET /api/usdjpy-strategy-lab/signals` | 最近 shadow 候选信号 |
| `POST /api/usdjpy-strategy-lab/signals/run` | 刷新候选信号 |
| `GET /api/usdjpy-strategy-lab/backtest-plan` | 新策略回测计划 |
| `POST /api/usdjpy-strategy-lab/backtest-plan/build` | 重新生成回测计划 |
| `GET /api/usdjpy-strategy-lab/imported-backtests` | 已导入的 USDJPY 回测结果 |
| `POST /api/usdjpy-strategy-lab/import-backtest` | 导入本机 CSV/JSON 回测结果，只写研究证据 |
| `GET /api/usdjpy-strategy-lab/risk-check` | 运行快照、快通道、新闻和隔离状态检查 |
| `GET /api/usdjpy-strategy-lab/evidence` | 策略评分与候选信号合并视图 |
| `GET /api/usdjpy-strategy-lab/candidate-policy` | 候选策略政策 |
| `POST /api/usdjpy-strategy-lab/candidate-policy/build` | 生成候选策略政策 |
| `GET /api/usdjpy-strategy-lab/bar-replay` | USDJPY 因果 bar/tick 回放总报告别名 |
| `GET /api/usdjpy-strategy-lab/bar-replay/status` | USDJPY 因果 bar/tick 回放总报告 |
| `POST /api/usdjpy-strategy-lab/bar-replay/build` | 重建因果回放报告和 replay ledger |
| `GET /api/usdjpy-strategy-lab/bar-replay/entry` | current vs relaxed_entry_v1 入场候选对比 |
| `GET /api/usdjpy-strategy-lab/bar-replay/exit` | current vs let_profit_run_v1 出场候选对比 |
| `GET /api/usdjpy-strategy-lab/bar-replay/telegram-text` | 因果回放中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/walk-forward/status` | USDJPY walk-forward 稳定性筛选报告 |
| `POST /api/usdjpy-strategy-lab/walk-forward/build` | 重建 walk-forward 报告、参数选择和治理提案 |
| `GET /api/usdjpy-strategy-lab/walk-forward/selection` | 读取 train / validation / forward 后的参数选择 |
| `GET /api/usdjpy-strategy-lab/walk-forward/proposal` | 读取 stage-gated live config proposal |
| `GET /api/usdjpy-strategy-lab/walk-forward/telegram-text` | walk-forward 中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/state` | USDJPY 自主治理 Agent 当前阶段和 patch 状态 |
| `POST /api/usdjpy-strategy-lab/autonomous-agent/run` | 运行自主治理门；只写受控 patch 和回滚证据 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/decision` | 读取自主晋级决策 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/patch` | 读取受控 config patch |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/telegram-text` | 自主治理中文 Telegram 文案 |

## P3-19 因果回放端点

`bar-replay` 端点必须保持因果约束：

- 后验窗口只用于评分，不能决定当时是否入场；
- `relaxed_entry_v1` 只放宽 RSI / 战术确认一档；
- session、spread、news、runtime freshness、fastlane、cooldown 和仓位容量不能被放宽；
- 输出以 `R` 为主口径，`pips` 辅助，`USC` 只作账面参考。

## P3-20 自主治理端点

`walk-forward` 和 `autonomous-agent` 端点取消人工审批语义，但仍保持机器硬风控：

- `autoApplyAllowed=stage_gated`；
- `requiresManualReview=false`；
- `requiresAutonomousGovernance=true`；
- Agent 只能写 `QuantGod_AutonomousConfigPatch.json`；
- 连续亏损、日亏损、runtime 陈旧、快通道异常、点差异常和 news block 会自动暂停或回滚；
- DeepSeek 只解释，不批准 live、不取消回滚、不提高仓位上限；
- Polymarket 永远 shadow-only。

## 返回原则

返回内容必须中文优先，并明确显示：

- 新策略是否 shadow-only
- 是否允许真实下单
- 当前候选信号来自哪条路线
- 缺少哪些证据
- 下一步是回测、等待采样还是治理复核

## 禁止事项

这些端点不得：

- 下单
- 平仓
- 撤单
- 修改订单
- 修改 live preset
- 接收 Telegram 交易命令
- 写入凭据

新增策略想进入实盘，必须先通过 USDJPY 自主治理门和受控 patch 阶梯；这些 API 本身不会执行交易。
