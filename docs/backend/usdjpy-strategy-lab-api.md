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
| `GET /api/usdjpy-strategy-lab/autonomous-agent/lifecycle` | 读取 v2.5 三车道自主生命周期 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/lanes` | 读取 Live / MT5 Shadow / Polymarket Shadow 三车道摘要 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow` | 读取 MT5 多策略模拟车道排名 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/polymarket-shadow` | 读取 Polymarket 模拟账本和事件风险车道 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/ea-repro` | 读取 EA source / preset / input / ex5 对账证据 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2` | 读取 Daily Autopilot 2.0 中文计划和复盘 |
| `POST /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run` | 重建 Daily Autopilot 2.0 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text` | Daily Autopilot 2.0 中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/daily-todo` | 读取 Agent 今日待办，含车道、状态、指标和回滚状态 |
| `GET /api/usdjpy-strategy-lab/daily-todo/status` | 读取 Agent 今日待办状态别名 |
| `POST /api/usdjpy-strategy-lab/daily-todo/run` | 由 Agent 重建并写入今日待办 |
| `GET /api/usdjpy-strategy-lab/daily-todo/telegram-text` | Agent 今日待办中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/daily-review` | 读取 Agent 每日复盘，含净 R、最大不利 R、错失机会、早出场和升降级 |
| `GET /api/usdjpy-strategy-lab/daily-review/status` | 读取 Agent 每日复盘状态别名 |
| `POST /api/usdjpy-strategy-lab/daily-review/run` | 由 Agent 重建并写入每日复盘 |
| `GET /api/usdjpy-strategy-lab/daily-review/telegram-text` | Agent 每日复盘中文 Telegram 文案 |
| `GET /api/usdjpy-strategy-lab/autonomous-agent/telegram-text` | 自主治理中文 Telegram 文案 |

## P3-19 因果回放端点

`bar-replay` 端点必须保持因果约束：

- 后验窗口只用于评分，不能决定当时是否入场；
- `relaxed_entry_v1` 只放宽 RSI / 战术确认一档；
- session、spread、runtime freshness、fastlane、cooldown、仓位容量和高冲击新闻不能被放宽；
- 普通新闻默认是软风险：只降仓或降级，不单独阻断 USDJPY RSI LONG；
- 输出以 `R` 为主口径，`pips` 辅助，`USC` 只作账面参考。

## P3-20 自主治理端点

`walk-forward` 和 `autonomous-agent` 端点取消人工审批语义，但仍保持机器硬风控：

- `autoApplyAllowed=stage_gated`；
- `requiresAutonomousGovernance=true`；
- `completedByAgent=true` 用于 Agent 待办和复盘；
- `autoAppliedByAgent=true/false` 表示 Agent 是否自动推动受控 patch 或阶段状态；
- Agent 只能写 `QuantGod_AutonomousConfigPatch.json`；
- 连续亏损、日亏损、runtime 陈旧、快通道异常、点差异常和高冲击新闻会自动暂停或回滚；
- 普通新闻风险进入 Daily Autopilot 和 replay 复盘，但不作为常态硬阻断；
- DeepSeek 只解释，不批准 live、不取消回滚、不提高仓位上限；
- Polymarket 永远 shadow-only。

## P3-21 三车道自主生命周期端点

`autonomous-agent/lifecycle` 系列端点把 v2.5 的三车道语义合并到同一个 operator view：

- Live Lane 只允许 `USDJPYc / RSI_Reversal / LONG` 进入 `MICRO_LIVE` 或 `LIVE_LIMITED`；
- MT5 Shadow Lane 继续跑多策略模拟、回放、tester 和 ranking；
- Polymarket Shadow Lane 只做模拟账本、跟单模拟和事件风险上下文；
- 美分账户加速允许更快采样，但不能绕过 runtime、fastlane、spread、高冲击新闻和亏损回滚；
- `patchWritable=true` 只表示 Agent 可以写受控 patch，`liveMutationAllowed=false` 表示不能直接改 live preset；
- Daily Autopilot 2.0 生成中文早盘计划、Agent 今日待办、Agent 每日复盘和 Telegram 文案，不执行交易。
- `strategyJsonTodo`、`gaEvolutionTodo`、`telegramGatewayTodo` 是下一阶段任务，状态保持 `WAITING_NEXT_PHASE`，不会被假装成已完成能力。

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
