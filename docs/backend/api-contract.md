# QuantGod Backend API Contract

本文由 `docs/contracts/api-contract.json` 渲染生成，用于人工 review。机器可读版本仍以 JSON contract 为准。

## Contract 摘要

- Endpoint 总数：`120`。
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

`guarded-control` 不代表开放交易权限。它只表示 endpoint 是受控动作面，仍必须受 Backend、EA、dryRun、Kill Switch 和手动授权约束。

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
- Endpoint 数量：`6`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/ai-analysis` | `advisory` | AI Analysis V1 config/status alias. |
| POST | `/api/ai-analysis/run` | `advisory` | Run Technical/Risk/Decision V1 analysis. |
| GET | `/api/ai-analysis/latest` | `read-only` | Latest AI V1 report. |
| GET | `/api/ai-analysis/history` | `read-only` | AI V1 report history list. |
| GET | `/api/ai-analysis/history/:id` | `read-only` | One AI V1 report by id. |
| GET | `/api/ai-analysis/config` | `read-only` | AI V1 local config/status. |

### phase2-file-facade

- Phase / Domain：`phase2`。
- Endpoint 数量：`30`。

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
| GET | `/api/research/strategy-evaluation` | `read-only-csv` | QuantGod_StrategyEvaluationReport.csv |
| GET | `/api/research/regime-evaluation` | `read-only-csv` | QuantGod_RegimeEvaluationReport.csv |
| GET | `/api/research/manual-alpha` | `read-only-csv` | QuantGod_ManualAlphaLedger.csv |

### notify

- Phase / Domain：`phase2`。
- Endpoint 数量：`3`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/notify/config` | `read-only` | Notification config status; no secret values. |
| GET | `/api/notify/history` | `read-only` | Notification delivery history. |
| POST | `/api/notify/test` | `push-only` | Send one test notification; never accepts trading commands. |

### phase3-vibe-ai-kline

- Phase / Domain：`phase3`。
- Endpoint 数量：`19`。

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/vibe-coding` | `research-only` | Vibe Coding config alias. |
| GET | `/api/vibe-coding/config` | `research-only` | Vibe Coding config. |
| POST | `/api/vibe-coding/generate` | `research-only` | Generate sandboxed Python strategy code from natural language. |
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

## 更新清单

Backend route surface 变化时，按下面顺序维护：

1. 先更新 Backend route 和 Node/Python contract tests。
2. 再更新 `docs/contracts/api-contract.json`。
3. 运行 `python scripts/render_api_contract_markdown.py` 重新生成本文。
4. 更新 Frontend service wrapper，确保前端仍只走 `/api/*`。
5. 运行 `python scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend`。
