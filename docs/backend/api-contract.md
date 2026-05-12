# QuantGod Backend API Contract

本文由 `docs/contracts/api-contract.json` 渲染生成，用于人工 review。
机器可读版本仍以 JSON contract 为准。

## Contract 摘要

- Endpoint 总数：`256`。
- Backend API base：`http://127.0.0.1:8080/api`。
- 任何新增、删除或重命名 `/api/*` route，都必须同步更新 JSON contract、本文档和 Frontend service wrapper。

## 通用安全语义

Phase 1/2/3 的 API contract 必须保持本地优先和安全受控：

| 字段 | 期望值 | 含义 |
|---|---:|---|
| `localOnly` | `true` | Contract default |
| `advisoryOnly` | `true` | Contract default |
| `readOnlyDataPlane` | `true` | Contract default |
| `orderSendAllowed` | `false` | Contract default |
| `closeAllowed` | `false` | Contract default |
| `cancelAllowed` | `false` | Contract default |
| `credentialStorageAllowed` | `false` | Contract default |
| `livePresetMutationAllowed` | `false` | Contract default |
| `canOverrideKillSwitch` | `false` | Contract default |
| `canMutateGovernanceDecision` | `false` | Contract default |
| `telegramCommandExecutionAllowed` | `false` | Contract default |

`guarded-control` 不代表开放交易权限。它只表示 endpoint 是受控动作面，
仍必须受 Backend、EA、dryRun、Kill Switch 和手动授权约束。

## Endpoint Groups

### backend-core-and-control

- Phase / Domain：`backend-core`。
- Endpoint 数量：`23`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/latest` | `read-only` | Latest local dashboard state with service metadata. |
| GET | `/api/daily-review` | `read-only` | Daily review API wrapper. |
| GET | `/api/daily-autopilot` | `read-only` | Daily autopilot API wrapper. |
| GET | `/api/phase1` | `read-only` | Phase 1 workspace route/config alias. |
| GET | `/api/mt5-readonly` | `read-only` | MT5 read-only bridge snapshot alias. |
| GET | `/api/mt5-readonly/:endpoint` | `read-only` | Legacy MT5 read-only bridge endpoint wrapper. |
| GET | `/api/mt5-symbol-registry` | `read-only` | MT5 symbol registry. |
| GET | `/api/mt5-symbol-registry/:endpoint` | `read-only` | MT5 symbol registry sub-endpoint. |
| GET | `/api/mt5-backtest-loop` | `research-only` | Backend backtest loop status/result. |
| GET | `/api/mt5-backtest-loop/run` | `research-only` | Trigger research-only backend backtest loop. |
| POST | `/api/paramlab/auto-tester` | `guarded-control` | ParamLab auto-tester base route alias; action routes remain guarded. |
| POST | `/api/paramlab/auto-tester/:action` | `guarded-control` | ParamLab auto-tester actions; must not bypass Version Gate or live authorization. |
| GET | `/api/mt5-pending-worker/status` | `read-only` | Pending worker status. |
| POST | `/api/mt5-pending-worker/run` | `guarded-control` | Run pending worker under backend safety controls. |
| GET | `/api/mt5-adaptive-control/status` | `read-only` | Adaptive control status. |
| POST | `/api/mt5-adaptive-control/run` | `guarded-control` | Run adaptive control under backend safety controls. |
| GET | `/api/mt5-platform` | `read-only` | MT5 platform store base endpoint. |
| ANY | `/api/mt5-platform/:endpoint` | `guarded-control` | MT5 platform store sub-endpoints; not a direct order API. |
| GET | `/api/mt5-trading` | `guarded-control` | MT5 trading bridge status; defaults locked by dryRun/killSwitch. |
| ANY | `/api/mt5-trading/:endpoint` | `guarded-control` | MT5 trading bridge sub-endpoint; must remain guarded by backend and EA controls. |
| GET | `/api/mt5` | `guarded-control` | Compatibility alias for MT5 trading status. |
| ANY | `/api/mt5/:endpoint` | `guarded-control` | Compatibility alias for MT5 trading bridge sub-endpoints. |
| DELETE | `/api/mt5/order/:ticket` | `guarded-control` | Order cancel route; must remain blocked/guarded unless explicitly authorized. |

### polymarket-research

- Phase / Domain：`backend-core`。
- Endpoint 数量：`28`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/polymarket/history` | `read-only` | Polymarket research history. |
| GET | `/api/polymarket/real-trades` | `read-only` | Polymarket real/canary trades view. |
| GET | `/api/polymarket/radar` | `read-only` | Market radar JSON. |
| GET | `/api/polymarket/radar-ledger` | `read-only-csv` | Polymarket radar ledger. |
| GET | `/api/polymarket/markets` | `read-only` | Market search/list. |
| GET | `/api/polymarket/market` | `read-only` | Market detail. |
| GET | `/api/polymarket/book` | `read-only` | Order book / book snapshot. |
| GET | `/api/polymarket/asset-opportunities` | `read-only` | Asset opportunity list. |
| GET | `/api/polymarket/radar-worker` | `read-only` | Radar worker status. |
| GET | `/api/polymarket/radar-worker-ledger` | `read-only-csv` | Radar worker ledger. |
| GET | `/api/polymarket/cross-linkage` | `read-only` | Cross-market linkage output. |
| GET | `/api/polymarket/cross-market-linkage-ledger` | `read-only-csv` | Cross-market linkage ledger. |
| GET | `/api/polymarket/canary-executor-contract` | `read-only` | Canary executor contract/status. |
| GET | `/api/polymarket/canary-executor-ledger` | `read-only-csv` | Canary executor ledger. |
| GET | `/api/polymarket/auto-governance` | `read-only` | Polymarket auto-governance evidence. |
| GET | `/api/polymarket/auto-governance-ledger` | `read-only-csv` | Polymarket auto-governance ledger. |
| GET | `/api/polymarket/canary-executor-run` | `read-only` | Canary executor run output. |
| GET | `/api/polymarket/ai-score` | `read-only` | Polymarket AI score. |
| GET | `/api/polymarket/ai-score-ledger` | `read-only-csv` | Polymarket AI score ledger. |
| GET | `/api/polymarket/canary-exit-ledger` | `read-only-csv` | Canary exit ledger. |
| GET | `/api/polymarket/canary-order-audit-ledger` | `read-only-csv` | Canary order audit ledger. |
| GET | `/api/polymarket/canary-position-ledger` | `read-only-csv` | Canary position ledger. |
| GET | `/api/polymarket/analyze/history` | `read-only` | Single-market analysis history. |
| GET | `/api/polymarket/search` | `read-only` | Polymarket search endpoint. |
| POST | `/api/polymarket/single-market-request` | `research-only` | Queue/request single-market research analysis. |
| POST | `/api/polymarket/analyze` | `research-only` | Compatibility alias for single-market research request. |
| GET | `/api/polymarket/single-market-analysis` | `read-only` | Latest single-market analysis output. |
| GET | `/api/polymarket/single-market-analysis-ledger` | `read-only-csv` | Single-market analysis ledger. |

### mt5-readonly

- Phase / Domain：`phase1`。
- Endpoint 数量：`11`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/mt5-readonly/status` | `read-only` | MT5 read-only bridge status. |
| GET | `/api/mt5-readonly/account` | `read-only` | Account snapshot, no credentials. |
| GET | `/api/mt5-readonly/positions` | `read-only` | Open positions snapshot. |
| GET | `/api/mt5-readonly/orders` | `read-only` | Open/pending orders snapshot. |
| GET | `/api/mt5-readonly/symbols` | `read-only` | MT5 symbol list. |
| GET | `/api/mt5-readonly/quote` | `read-only` | Quote for one symbol. |
| GET | `/api/mt5-readonly/snapshot` | `read-only` | Combined MT5 monitor snapshot. |
| GET | `/api/mt5-readonly/kline` | `read-only` | K-line bars for KlineCharts. |
| GET | `/api/mt5-readonly/trades` | `read-only` | Trade markers for chart overlay. |
| GET | `/api/mt5-readonly/shadow-signals` | `read-only` | Shadow signal markers for chart overlay. |
| GET | `/api/shadow-signals` | `read-only` | Compatibility alias for shadow signal overlay. |

### ai-analysis-v1

- Phase / Domain：`phase1`。
- Endpoint 数量：`8`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/ai-analysis` | `advisory` | AI Analysis V1 config/status alias. |
| POST | `/api/ai-analysis/run` | `advisory` | Run Technical/Risk/Decision V1 analysis. |
| GET | `/api/ai-analysis/latest` | `read-only` | Latest AI V1 report. |
| GET | `/api/ai-analysis/history` | `read-only` | AI V1 report history list. |
| GET | `/api/ai-analysis/history/:id` | `read-only` | One AI V1 report by id. |
| GET | `/api/ai-analysis/config` | `read-only` | AI V1 local config/status. |
| GET | `/api/ai-analysis/agent-health` | `read-only` | Latest local AI agent health evidence. |
| GET | `/api/ai-analysis/agent-health/history` | `read-only` | Historical local AI agent health evidence. |

### phase2-file-facade

- Phase / Domain：`phase2`。
- Endpoint 数量：`32`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/governance/advisor` | `read-only` | QuantGod_GovernanceAdvisor.json |
| GET | `/api/governance/version-registry` | `read-only` | QuantGod_StrategyVersionRegistry.json |
| GET | `/api/governance/promotion-gate` | `read-only` | QuantGod_VersionPromotionGate.json |
| GET | `/api/governance/optimizer-v2` | `read-only` | QuantGod_OptimizerV2Plan.json |
| GET | `/api/paramlab/status` | `read-only` | QuantGod_ParamLabStatus.json |
| GET | `/api/paramlab/results` | `read-only` | QuantGod_ParamLabResults.json |
| GET | `/api/paramlab/scheduler` | `read-only` | QuantGod_ParamLabAutoScheduler.json |
| GET | `/api/paramlab/recovery` | `read-only` | QuantGod_ParamLabRunRecovery.json |
| GET | `/api/paramlab/report-watcher` | `read-only` | QuantGod_ParamLabReportWatcher.json |
| GET | `/api/paramlab/tester-window` | `read-only` | QuantGod_AutoTesterWindow.json |
| GET | `/api/research/stats` | `read-only` | QuantGod_MT5ResearchStats.json |
| GET | `/api/research/entry-blockers` | `read-only` | QuantGod_MT5EntryBlockers.json |
| GET | `/api/dashboard/state` | `read-only` | QuantGod_Dashboard.json |
| GET | `/api/dashboard/backtest-summary` | `read-only` | QuantGod_BacktestSummary.json |
| GET | `/api/trades/journal` | `read-only-csv` | QuantGod_TradeJournal.csv |
| GET | `/api/trades/close-history` | `read-only-csv` | QuantGod_CloseHistory.csv |
| GET | `/api/trades/outcome-labels` | `read-only-csv` | QuantGod_TradeOutcomeLabels.csv |
| GET | `/api/trades/trading-audit` | `read-only-csv` | QuantGod_MT5TradingAuditLedger.csv |
| GET | `/api/shadow/signals` | `read-only-csv` | QuantGod_ShadowSignalLedger.csv |
| GET | `/api/shadow/outcomes` | `read-only-csv` | QuantGod_ShadowOutcomeLedger.csv |
| GET | `/api/shadow/candidates` | `read-only-csv` | QuantGod_ShadowCandidateLedger.csv |
| GET | `/api/shadow/candidate-outcomes` | `read-only-csv` | QuantGod_ShadowCandidateOutcomeLedger.csv |
| GET | `/api/paramlab/results-ledger` | `read-only-csv` | QuantGod_ParamLabResultsLedger.csv |
| GET | `/api/paramlab/scheduler-ledger` | `read-only-csv` | QuantGod_ParamLabAutoSchedulerLedger.csv |
| GET | `/api/paramlab/report-watcher-ledger` | `read-only-csv` | QuantGod_ParamLabReportWatcherLedger.csv |
| GET | `/api/paramlab/recovery-ledger` | `read-only-csv` | QuantGod_ParamLabRunRecoveryLedger.csv |
| GET | `/api/paramlab/tester-window-ledger` | `read-only-csv` | QuantGod_AutoTesterWindowLedger.csv |
| GET | `/api/research/stats-ledger` | `read-only-csv` | QuantGod_MT5ResearchStatsLedger.csv |
| GET | `/api/research/entry-blockers-ledger` | `read-only-csv` | QuantGod_MT5EntryBlockersLedger.csv |
| GET | `/api/research/strategy-evaluation` | `read-only-csv` | QuantGod_StrategyEvaluationReport.csv |
| GET | `/api/research/regime-evaluation` | `read-only-csv` | QuantGod_RegimeEvaluationReport.csv |
| GET | `/api/research/manual-alpha` | `read-only-csv` | QuantGod_ManualAlphaLedger.csv |

### notify

- Phase / Domain：`phase2`。
- Endpoint 数量：`7`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/notify/config` | `read-only` | Notification config status; no secret values. |
| GET | `/api/notify/history` | `read-only` | Notification delivery history. |
| POST | `/api/notify/test` | `push-only` | Send one test notification; never accepts trading commands. |
| POST | `/api/notify/daily-digest` | `push-only` | Trigger AI ops daily digest push; advisory-only output. |
| POST | `/api/notify/runtime-scan` | `push-only` | Trigger runtime scan notification; never accepts trading commands. |
| GET | `/api/notify/mt5-ai-monitor/config` | `read-only` | MT5 AI monitor config status; no secret values. |
| POST | `/api/notify/mt5-ai-monitor/run` | `push-only` | Run MT5 AI monitor analysis; advisory-only, push-only. |

### phase3-vibe-ai-kline

- Phase / Domain：`phase3`。
- Endpoint 数量：`23`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/ai-analysis/deepseek-telegram/config` | `read-only` | DeepSeek-Telegram fusion config status. |
| POST | `/api/ai-analysis/deepseek-telegram/run` | `advisory` | Run DeepSeek-Telegram fusion analysis. |
| GET | `/api/ai-analysis/deepseek-telegram/latest` | `read-only` | Latest DeepSeek-Telegram fusion result. |
| GET | `/api/vibe-coding` | `research-only` | Vibe Coding config alias. |
| GET | `/api/vibe-coding/config` | `research-only` | Vibe Coding config. |
| POST | `/api/vibe-coding/generate` | `research-only` | Generate sandboxed Python strategy code from natural language. |
| POST | `/api/vibe-coding/import-library` | `research-only` | Import a research-only strategy library candidate into the Vibe Coding sandbox. |
| POST | `/api/vibe-coding/iterate` | `research-only` | Iterate a generated strategy. |
| POST | `/api/vibe-coding/backtest` | `research-only` | Run local research-only backtest. |
| POST | `/api/vibe-coding/analyze` | `advisory` | Analyze backtest result. |
| GET | `/api/vibe-coding/strategies` | `read-only` | List generated strategy versions. |
| GET | `/api/vibe-coding/strategy` | `read-only` | Vibe Coding strategy detail base route alias. |
| GET | `/api/vibe-coding/strategy/:id` | `read-only` | Fetch generated strategy detail. |
| GET | `/api/ai-analysis-v2` | `advisory` | AI Analysis V2 config alias. |
| GET | `/api/ai-analysis-v2/config` | `read-only` | AI Analysis V2 config. |
| POST | `/api/ai-analysis-v2/run` | `advisory` | Run V2 multi-agent debate analysis. |
| GET | `/api/ai-analysis-v2/latest` | `read-only` | Latest AI V2 analysis. |
| GET | `/api/ai-analysis-v2/history` | `read-only` | AI V2 history list. |
| GET | `/api/ai-analysis-v2/history/:id` | `read-only` | One AI V2 report. |
| GET | `/api/kline` | `read-only` | K-line enhancement config alias. |
| GET | `/api/kline/ai-overlays` | `read-only` | AI BUY/SELL/HOLD overlay markers. |
| GET | `/api/kline/vibe-indicators` | `read-only` | Vibe indicator overlay descriptors. |
| GET | `/api/kline/realtime-config` | `read-only` | K-line polling config. |

### p2-3-sqlite-state-layer

- Phase / Domain：`phase2`。
- Endpoint 数量：`7`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/state` | `read-only` | SQLite state layer status alias; local evidence persistence only. |
| GET | `/api/state/status` | `read-only` | SQLite state layer schema, table counts, and safety defaults. |
| GET | `/api/state/config` | `read-only` | Resolved local SQLite state configuration; no secrets. |
| GET | `/api/state/events` | `read-only` | Normalized local evidence events from SQLite. |
| GET | `/api/state/ai-analysis` | `read-only` | Advisory-only AI analysis run index from SQLite. |
| GET | `/api/state/vibe-strategies` | `read-only` | Research-only Vibe strategy index from SQLite. |
| GET | `/api/state/notifications` | `read-only` | Push-only notification event index from SQLite. |

### p3-12-automation-chain-runner

- Phase / Domain：`phase3`。
- Endpoint 数量：`4`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/automation-chain` | `read-only` | Automation chain status alias; no trading execution. |
| GET | `/api/automation-chain/status` | `read-only` | Latest automation chain status and missing evidence. |
| GET | `/api/automation-chain/telegram-text` | `push-preview` | Chinese Telegram preview text for automation chain. |
| POST | `/api/automation-chain/run` | `local-advisory-control` | Run local evidence chain; writes runtime evidence but does not place orders. |

### P3-14 USDJPY 单品种多策略实验室

- Phase / Domain：`unknown`。
- Endpoint 数量：`113`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/usdjpy-strategy-lab` | `read-only` | USDJPY 策略实验室基础状态别名。 |
| GET | `/api/usdjpy-strategy-lab/status` | `read-only` | 读取 USDJPY-only 策略政策状态。 |
| GET | `/api/usdjpy-strategy-lab/scoreboard` | `read-only` | 读取 USDJPY 多策略评分矩阵。 |
| GET | `/api/usdjpy-strategy-lab/dry-run` | `read-only` | 生成或读取 USDJPY EA 干跑决策。 |
| GET | `/api/usdjpy-strategy-lab/telegram-text` | `read-only` | 生成 USDJPY 策略政策的中文 Telegram 文案。 |
| POST | `/api/usdjpy-strategy-lab/run` | `read-only` | 运行 USDJPY 策略政策生成；不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/catalog` | `read-only` | 读取 USDJPY 策略工厂目录，包含东京突破、夜盘回归和 H4 回调三条新增 shadow 策略。 |
| GET | `/api/usdjpy-strategy-lab/signals` | `read-only` | 读取 USDJPY shadow 候选信号，用于确认新增策略是否正在采样。 |
| POST | `/api/usdjpy-strategy-lab/signals/run` | `read-only` | 刷新 USDJPY shadow 候选信号；只解析证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/backtest-plan` | `read-only` | 读取 USDJPY 新策略回测计划。 |
| POST | `/api/usdjpy-strategy-lab/backtest-plan/build` | `read-only` | 生成 USDJPY 新策略回测计划；不会启动真实交易。 |
| GET | `/api/usdjpy-strategy-lab/candidate-policy` | `read-only` | 读取 USDJPY 候选策略政策。 |
| POST | `/api/usdjpy-strategy-lab/candidate-policy/build` | `read-only` | 生成 USDJPY 候选策略政策；新策略仍保持 shadow-only。 |
| GET | `/api/usdjpy-strategy-lab/evidence` | `read-only` | 读取 USDJPY 策略评分和候选信号的证据合并视图。 |
| GET | `/api/usdjpy-strategy-lab/risk-check` | `read-only` | 读取 USDJPY 策略工厂风险检查结果。 |
| GET | `/api/usdjpy-strategy-lab/imported-backtests` | `read-only` | 读取已导入的 USDJPY 回测结果账本。 |
| POST | `/api/usdjpy-strategy-lab/import-backtest` | `read-only` | 导入本机 USDJPY 回测 CSV/JSON 结果；只写研究证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/live-loop` | `read-only` | 读取 USDJPY 实盘 EA 恢复状态、阻断原因和下一步自动动作。 |
| POST | `/api/usdjpy-strategy-lab/live-loop/run` | `read-only` | 重建 USDJPY 实盘闭环 evidence；只写本地状态和 intent，不直接执行交易。 |
| GET | `/api/usdjpy-strategy-lab/live-loop/telegram-text` | `read-only` | 生成或发送 USDJPY 实盘闭环中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/evolution` | `read-only` | 读取 USDJPY 自学习闭环状态别名，包含数据集、回放、参数候选和配置提案。 |
| GET | `/api/usdjpy-strategy-lab/evolution/status` | `read-only` | 读取 USDJPY 自学习闭环状态，包含数据集、回放、参数候选和配置提案。 |
| POST | `/api/usdjpy-strategy-lab/evolution/build` | `read-only` | 重建 USDJPY 运行数据集、回放、参数候选和配置提案；只写本地研究证据。 |
| GET | `/api/usdjpy-strategy-lab/evolution/replay` | `read-only` | 读取或刷新 USDJPY 回放复盘，解释错失机会和过早出场。 |
| GET | `/api/usdjpy-strategy-lab/evolution/tune` | `read-only` | 读取或刷新 USDJPY tester-only 参数候选；不会自动应用到实盘。 |
| GET | `/api/usdjpy-strategy-lab/evolution/proposal` | `read-only` | 读取或刷新 USDJPY 实盘配置提案；提案进入自主治理门，stage-gated，不再等待人工审批。 |
| GET | `/api/usdjpy-strategy-lab/evolution/telegram-text` | `read-only` | 生成或发送 USDJPY 自学习闭环中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay` | `read-only` | 读取 USDJPY 因果 bar/tick 回放报告别名；等同 status。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/status` | `read-only` | 读取 USDJPY 因果 bar/tick 回放报告；后验窗口只用于评分，不参与入场触发。 |
| POST | `/api/usdjpy-strategy-lab/bar-replay/build` | `read-only` | 重建 USDJPY 因果回放报告、入场候选对比、出场候选对比和 replay ledger；不会执行交易。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/entry` | `read-only` | 读取 USDJPY current vs relaxed_entry_v1 入场候选对比；硬门禁不会放宽。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/exit` | `read-only` | 读取 USDJPY current vs let_profit_run_v1 出场持有候选对比；只重估已发生入场的出场表现。 |
| GET | `/api/usdjpy-strategy-lab/bar-replay/telegram-text` | `read-only` | 生成或发送 USDJPY 因果回放中文 Telegram 文案；后续由 P3-20 自主治理门评估。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward` | `read-only` | 读取 USDJPY walk-forward 稳定性筛选报告别名。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/status` | `read-only` | 读取 USDJPY train / validation / forward 三段稳定性筛选报告。 |
| POST | `/api/usdjpy-strategy-lab/walk-forward/build` | `read-only` | 重建 USDJPY walk-forward 报告、参数选择和 stage-gated 提案；不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/selection` | `read-only` | 读取 USDJPY walk-forward 参数选择结果。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/proposal` | `read-only` | 读取 USDJPY stage-gated live config proposal。 |
| GET | `/api/usdjpy-strategy-lab/walk-forward/telegram-text` | `read-only` | 生成或发送 USDJPY walk-forward 中文 Telegram 文案。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent` | `read-only` | 读取 USDJPY 自主治理 Agent 状态别名。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/state` | `read-only` | 读取 USDJPY 自主治理 Agent 当前阶段、受控 patch 和回滚状态。 |
| POST | `/api/usdjpy-strategy-lab/autonomous-agent/run` | `read-only` | 运行 USDJPY 自主治理门；只写受控 patch 和回滚证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/decision` | `read-only` | 读取 USDJPY 自主晋级决策。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/patch` | `read-only` | 读取 USDJPY 受控 config patch。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/lifecycle` | `read-only` | 读取 QuantGod v2.5 三车道自主生命周期，包含 Live Lane、MT5 Shadow Lane、Polymarket Shadow Lane、美分账户、EA 对账摘要和下一阶段任务状态。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/lanes` | `read-only` | 读取 Live / MT5 Shadow / Polymarket Shadow 三车道摘要；实盘只允许 USDJPY RSI LONG，模拟继续多策略。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow` | `read-only` | 读取 MT5 多策略模拟车道排名和升降级阶段；shadow 策略不能直接进入实盘路线。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/polymarket-shadow` | `read-only` | 读取 Polymarket 模拟账本和事件风险车道；只做 shadow / paper context，不连接真实钱包。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/ea-repro` | `read-only` | 读取 EA source、preset、input 和 ex5 hash 对账证据，帮助确认当前实盘 EA 是否来自受控版本。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2` | `read-only` | 读取 Daily Autopilot 2.0 中文早盘计划、夜盘复盘、三车道今日动作，以及 Strategy JSON GA Trace 状态和 Telegram Gateway 下一阶段任务。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/status` | `read-only` | 读取 Daily Autopilot 2.0 状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run` | `read-only` | 重建 Daily Autopilot 2.0 中文计划、复盘和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text` | `read-only` | 生成或发送 Daily Autopilot 2.0 中文 Telegram 文案，并说明 Strategy JSON / GA Trace 已进入 shadow/tester 过程审计，Telegram Gateway 等待下一阶段；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测状态别名；只展示本地研究证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/status` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测状态、K线数量、最新报告和只读安全边界。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/sample` | `read-only` | 写入确定性 USDJPY H1 示例 K线到本地 SQLite，用于本地 smoke 和测试；不触达 MT5 交易。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/run` | `read-only` | 运行 USDJPY Strategy JSON 回测，输出 report、trades、equity curve 和 GA 可读 fitness evidence。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/telegram-text` | `read-only` | 生成或发送中文 Strategy JSON 回测摘要；Telegram 仍只推送，不接命令。 |
| POST | `/api/usdjpy-strategy-lab/strategy-backtest/sync-klines` | `read-only` | 从 MT5 Python 或 MQL5 CopyRates CSV 增量同步 USDJPY M1/M5/M15/H1 K线到本地 SQLite；只写回测证据。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/production-status` | `read-only` | 读取 USDJPY SQLite 历史数据生产验收状态，包含 M1/M5/M15/H1 覆盖深度、K线密度、最新延迟和后台同步来源。 |
| GET | `/api/usdjpy-strategy-lab/strategy-backtest/quality` | `read-only` | 读取 USDJPY Strategy JSON SQLite 回测质量状态，包含历史覆盖、数据来源和同步目标满足情况；只展示回测证据。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os` | `read-only` | 读取 USDJPY Evidence OS 审计状态；与 /evidence-os/status 保持兼容。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/status` | `read-only` | 读取 USDJPY Strategy JSON / Python Replay / MQL5 EA parity、执行反馈、Case Memory 和 Telegram Gateway 审计状态。 |
| POST | `/api/usdjpy-strategy-lab/evidence-os/run` | `read-only` | 生成 USDJPY evidence OS 审计包：parity、execution feedback、case memory 和 push-only notification ledger。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/parity` | `read-only` | 重建并读取 Strategy JSON / Python Replay / MQL5 EA parity report。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/execution-feedback` | `read-only` | 重建并读取 USDJPY live execution feedback / execution quality report。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/case-memory` | `read-only` | 重建并读取 USDJPY Case Memory，总结错失机会、早出、执行偏差和下一代 GA 线索。 |
| GET | `/api/usdjpy-strategy-lab/evidence-os/telegram-text` | `read-only` | 生成 USDJPY evidence OS 中文 Telegram 文案；走 push-only Gateway，不接命令。 |
| GET | `/api/case-memory` | `read-only` | 读取 P4-7 Case Memory → shadow Strategy JSON candidate / GA seed hint 状态别名；不执行交易。 |
| GET | `/api/case-memory/status` | `read-only` | 读取 Case Memory strategy structure report、parity gate、shadow Strategy JSON candidate 和 GA seed 线索。 |
| POST | `/api/case-memory/build` | `read-only` | 把 Case Memory root cause 转成 proposed mutation、shadow Strategy JSON candidate 和 GA seed hint；PARITY_FAIL 会阻断。 |
| GET | `/api/case-memory/telegram-text` | `push-preview` | 生成 Case Memory 策略结构候选中文 Telegram 文案；push-only，不接交易命令。 |
| GET | `/api/usdjpy-strategy-lab/ga` | `read-only` | 读取 USDJPY Strategy JSON GA 总状态别名；只展示 GA 过程审计，不直接进入实盘。 |
| GET | `/api/usdjpy-strategy-lab/ga/status` | `read-only` | 读取 USDJPY Strategy JSON GA 当前代数、种群、最佳 fitness、阻断数量和下一步动作。 |
| POST | `/api/usdjpy-strategy-lab/ga/run-generation` | `read-only` | 运行一代 USDJPY Strategy JSON GA，写入 generation、candidate、elite、blocker 和 evolution path 证据；不下单、不改 preset。 |
| GET | `/api/usdjpy-strategy-lab/ga/generations` | `read-only` | 读取 GA generation ledger，用于展示每一代如何生成、评分、保留和淘汰。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidates` | `read-only` | 读取 GA candidate runs，包含 seedId、Strategy JSON、fitness 分解、rank、阶段和阻断原因。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidate` | `read-only` | GA candidate 详情路由前缀；实际查询使用 seedId 子路径，不读取或修改交易状态。 |
| GET | `/api/usdjpy-strategy-lab/ga/candidate/:seedId` | `read-only` | 读取单个 GA seed 的 Strategy JSON、父代来源、fitness 分解、replay/walk-forward 状态和阻断解释。 |
| GET | `/api/usdjpy-strategy-lab/ga/evolution-path` | `read-only` | 读取 GA 进化路径，展示每代 bestFitness、bestStrategy、avgFitness 和阻断趋势。 |
| GET | `/api/usdjpy-strategy-lab/ga/blockers` | `read-only` | 读取 GA blocker summary，解释 schema、safety、样本、walk-forward、过拟合、max adverse 等失败原因。 |
| GET | `/api/usdjpy-strategy-lab/ga/telegram-text` | `read-only` | 生成或发送中文 GA 进化报告；Telegram 仍只推送，不接收交易命令。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo` | `read-only` | 读取 Agent 今日待办，含车道、状态、指标、升降级、回滚状态和下一阶段任务；无需人工回灌。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo/status` | `read-only` | 读取 Agent 今日待办状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/daily-todo/run` | `read-only` | 由 Agent 重建并写入今日待办和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/daily-todo/telegram-text` | `read-only` | 生成或发送 Agent 今日待办中文 Telegram 文案，包含下一阶段任务；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/daily-review` | `read-only` | 读取 Agent 每日复盘，含净 R、最大不利 R、错失机会、早出场、升降级、回滚状态和下一阶段任务。 |
| GET | `/api/usdjpy-strategy-lab/daily-review/status` | `read-only` | 读取 Agent 每日复盘状态别名，包含下一阶段任务等待状态。 |
| POST | `/api/usdjpy-strategy-lab/daily-review/run` | `read-only` | 由 Agent 重建并写入每日复盘和下一阶段任务；只写本地证据，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/daily-review/telegram-text` | `read-only` | 生成或发送 Agent 每日复盘中文 Telegram 文案，包含下一阶段任务；Telegram 仍只推送，不接命令。 |
| GET | `/api/usdjpy-strategy-lab/autonomous-agent/telegram-text` | `read-only` | 生成或发送 USDJPY 自主治理中文 Telegram 文案。 |
| GET | `/api/telegram-gateway` | `read-only` | 读取 P4-5 Telegram Gateway 运维观测状态别名；只做 push-only 队列、去重、限频、ledger 观测。 |
| GET | `/api/telegram-gateway/status` | `read-only` | 读取 P4-5 Telegram Gateway 运维观测状态，包含队列、待投递、真实发送、抑制、失败和 topic 视图。 |
| POST | `/api/telegram-gateway/collect` | `push-preview` | 收集 Daily Autopilot、GA、Agent 和 Polymarket 报告进入 push-only Gateway 队列；不接收 Telegram 命令。 |
| GET | `/api/telegram-gateway/telegram-text` | `push-preview` | 生成 Telegram Gateway 运维中文预览；仍只推送，不接 Telegram 命令。 |
| GET | `/api/usdjpy-strategy-lab/agent-ops-health` | `read-only` | 读取 USDJPY Agent operations health 状态别名；只汇总本地证据与心跳，不执行交易。 |
| GET | `/api/usdjpy-strategy-lab/agent-ops-health/status` | `read-only` | 读取 USDJPY Agent loop、Evidence OS、Telegram Gateway 和本地 runtime 健康状态。 |
| GET | `/api/strategy-ga-factory` | `read-only` | 读取 P4-4 Strategy JSON GA Factory 状态别名；只做工厂归档，不执行交易。 |
| GET | `/api/strategy-ga-factory/status` | `read-only` | 读取 GA Factory state、elite archive、strategy graveyard 和 lineage tree 摘要。 |
| POST | `/api/strategy-ga-factory/build` | `read-only` | 生成 GA Factory state、elite archive、strategy graveyard、lineage tree 和 ledger；不下单、不改 preset。 |
| GET | `/api/strategy-ga-factory/telegram-text` | `push-preview` | 生成 GA Factory 中文 Telegram 文案；push-only，不接交易命令。 |
| GET | `/api/ga-factory` | `read-only` | 读取 GA Factory 状态短别名；等同 /api/strategy-ga-factory。 |
| GET | `/api/ga-factory/status` | `read-only` | 读取 GA Factory 状态短别名；等同 /api/strategy-ga-factory/status。 |
| POST | `/api/ga-factory/build` | `read-only` | 构建 GA Factory 短别名；等同 /api/strategy-ga-factory/build。 |
| GET | `/api/ga-factory/telegram-text` | `push-preview` | 生成 GA Factory 中文 Telegram 文案短别名。 |
| GET | `/api/usdjpy-strategy-lab/telegram-gateway/status` | `read-only` | 读取独立 Telegram Gateway 队列、ledger、去重、限频和 push-only 状态。 |
| POST | `/api/usdjpy-strategy-lab/telegram-gateway/test-event` | `read-only` | 写入中文测试 NotificationEvent 到 Gateway 队列；不发送交易命令。 |
| POST | `/api/usdjpy-strategy-lab/telegram-gateway/dispatch` | `read-only` | 处理 Gateway 队列；默认只写 ledger，send=1 时仍要求 push allowed 且 commands disabled。 |
| GET | `/api/usdjpy-strategy-lab/telegram-gateway` | `read-only` | 读取独立 Telegram Gateway 状态兼容别名。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract` | `read-only` | 读取 Strategy JSON → MQL5 EA 只读契约状态兼容别名；只用于 shadow/tester/paper lane 评估。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract/status` | `read-only` | 读取 Strategy JSON → MQL5 EA 只读契约状态、所选 seed、fingerprint 和 EA 回执；只用于 shadow/tester/paper lane 评估。 |
| POST | `/api/usdjpy-strategy-lab/strategy-contract/build` | `read-only` | 生成 EA 可读取的 Strategy JSON contract 文件；不下单、不改 live preset。 |
| GET | `/api/usdjpy-strategy-lab/strategy-contract/telegram-text` | `read-only` | 生成 Strategy JSON → EA 只读契约中文摘要；Telegram 仍只推送，不接命令。 |

## 更新清单

Backend route surface 变化时，按下面顺序维护：

1. 先更新 Backend route 和 Node/Python contract tests。
2. 再更新 `docs/contracts/api-contract.json`。
3. 运行 `python scripts/render_api_contract_markdown.py` 重新生成本文。
4. 更新 Frontend service wrapper，确保前端仍只走 `/api/*`。
5. 运行跨仓库对齐检查：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```
