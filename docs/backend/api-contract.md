# QuantGod Backend API Contract

`docs/contracts/api-contract.json` 是机器可读版本；本文是人工 review 版本。

## 通用 Envelope

Phase 2/3 API 推荐返回：

```json
{
  "ok": true,
  "endpoint": "/api/...",
  "data": {},
  "source": {},
  "safety": {
    "localOnly": true,
    "readOnlyDataPlane": true,
    "orderSendAllowed": false,
    "closeAllowed": false,
    "cancelAllowed": false,
    "credentialStorageAllowed": false,
    "livePresetMutationAllowed": false,
    "canOverrideKillSwitch": false
  }
}
```

Endpoint 可以返回自己的业务字段，但必须保留安全语义。

## Phase 1：AI Analysis V1

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/ai-analysis` | V1 配置 / 状态 alias。 |
| POST | `/api/ai-analysis/run` | Run Technical/Risk/Decision V1 analysis. |
| GET | `/api/ai-analysis/latest` | Latest V1 report. |
| GET | `/api/ai-analysis/history` | V1 history list. |
| GET | `/api/ai-analysis/history/:id` | V1 report detail. |
| GET | `/api/ai-analysis/config` | V1 config/status. |

AI V1 只能作为 Governance evidence，不直接执行交易。

## Phase 1：K-line Data

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/mt5-readonly/kline` | OHLCV bars for KlineCharts. |
| GET | `/api/mt5-readonly/trades` | Trade markers. |
| GET | `/api/shadow-signals` | Shadow signal markers. |
| GET | `/api/mt5-readonly/shadow-signals` | Shadow marker alias. |

## Phase 2：File Facade API

这些 endpoint 把 runtime JSON/CSV 包装为 API。Frontend 不应该直接读取 runtime 文件。

### Governance

| Method | Path | Source |
|---|---|---|
| GET | `/api/governance/advisor` | `QuantGod_GovernanceAdvisor.json` |
| GET | `/api/governance/version-registry` | `QuantGod_StrategyVersionRegistry.json` |
| GET | `/api/governance/promotion-gate` | `QuantGod_VersionPromotionGate.json` |
| GET | `/api/governance/optimizer-v2` | `QuantGod_OptimizerV2Plan.json` |

### ParamLab

| Method | Path | Source |
|---|---|---|
| GET | `/api/paramlab/status` | `QuantGod_ParamLabStatus.json` |
| GET | `/api/paramlab/results` | `QuantGod_ParamLabResults.json` |
| GET | `/api/paramlab/scheduler` | `QuantGod_ParamLabAutoScheduler.json` |
| GET | `/api/paramlab/recovery` | `QuantGod_ParamLabRunRecovery.json` |
| GET | `/api/paramlab/report-watcher` | `QuantGod_ParamLabReportWatcher.json` |
| GET | `/api/paramlab/tester-window` | `QuantGod_AutoTesterWindow.json` |
| GET | `/api/paramlab/results-ledger` | `QuantGod_ParamLabResultsLedger.csv` |
| GET | `/api/paramlab/scheduler-ledger` | `QuantGod_ParamLabAutoSchedulerLedger.csv` |
| GET | `/api/paramlab/report-watcher-ledger` | `QuantGod_ParamLabReportWatcherLedger.csv` |
| GET | `/api/paramlab/recovery-ledger` | `QuantGod_ParamLabRunRecoveryLedger.csv` |
| GET | `/api/paramlab/tester-window-ledger` | `QuantGod_AutoTesterWindowLedger.csv` |

### Trades / Shadow / Research

| Method | Path | Source |
|---|---|---|
| GET | `/api/trades/journal` | `QuantGod_TradeJournal.csv` |
| GET | `/api/trades/close-history` | `QuantGod_CloseHistory.csv` |
| GET | `/api/trades/outcome-labels` | `QuantGod_TradeOutcomeLabels.csv` |
| GET | `/api/trades/trading-audit` | `QuantGod_MT5TradingAuditLedger.csv` |
| GET | `/api/shadow/signals` | `QuantGod_ShadowSignalLedger.csv` |
| GET | `/api/shadow/outcomes` | `QuantGod_ShadowOutcomeLedger.csv` |
| GET | `/api/shadow/candidates` | `QuantGod_ShadowCandidateLedger.csv` |
| GET | `/api/shadow/candidate-outcomes` | `QuantGod_ShadowCandidateOutcomeLedger.csv` |
| GET | `/api/research/stats` | `QuantGod_MT5ResearchStats.json` |
| GET | `/api/research/stats-ledger` | `QuantGod_MT5ResearchStatsLedger.csv` |
| GET | `/api/research/strategy-evaluation` | `QuantGod_StrategyEvaluationReport.csv` |
| GET | `/api/research/regime-evaluation` | `QuantGod_RegimeEvaluationReport.csv` |
| GET | `/api/research/manual-alpha` | `QuantGod_ManualAlphaLedger.csv` |

### Dashboard / Notify

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/dashboard/state` | Dashboard runtime state. |
| GET | `/api/dashboard/backtest-summary` | Backtest summary. |
| GET | `/api/notify/config` | Notification config without secrets. |
| GET | `/api/notify/history` | Notification history. |
| POST | `/api/notify/test` | Push-only test notification. |

## Phase 3：Vibe Coding / AI V2 / K-line Enhancements

| Method | Path | 用途 |
|---|---|---|
| GET | `/api/vibe-coding` | Vibe Coding 配置 alias。 |
| GET | `/api/vibe-coding/config` | Vibe Coding config. |
| POST | `/api/vibe-coding/generate` | Generate sandboxed strategy code. |
| POST | `/api/vibe-coding/iterate` | Iterate generated code. |
| POST | `/api/vibe-coding/backtest` | Research-only backtest. |
| POST | `/api/vibe-coding/analyze` | AI backtest analysis. |
| GET | `/api/vibe-coding/strategies` | Strategy registry list. |
| GET | `/api/vibe-coding/strategy/:id` | Strategy detail. |
| GET | `/api/ai-analysis-v2` | AI V2 配置 alias。 |
| GET | `/api/ai-analysis-v2/config` | AI V2 config. |
| POST | `/api/ai-analysis-v2/run` | Run V2 multi-agent debate. |
| GET | `/api/ai-analysis-v2/latest` | Latest V2 report. |
| GET | `/api/ai-analysis-v2/history` | V2 history list. |
| GET | `/api/ai-analysis-v2/history/:id` | V2 report detail. |
| GET | `/api/kline` | K-line 增强配置 alias。 |
| GET | `/api/kline/ai-overlays` | AI signal markers. |
| GET | `/api/kline/vibe-indicators` | Vibe indicator overlays. |
| GET | `/api/kline/realtime-config` | Polling config. |

## Update Checklist

When backend routes change:

1. Update backend route implementation and tests.
2. Update `docs/contracts/api-contract.json`.
3. Update this Markdown file.
4. Update frontend service wrappers.
5. Run docs contract check with `--backend`.

## Backend Core / Guarded Control Surfaces

Some existing backend routes are not pure file facade endpoints. They are documented because Frontend and Infra still need to understand their existence.

| Method | Path | Mode | Notes |
|---|---|---|---|
| GET | `/api/latest` | read-only | Latest dashboard state. |
| GET | `/api/daily-review` | read-only | Daily review wrapper. |
| GET | `/api/daily-autopilot` | read-only | Daily autopilot wrapper. |
| GET | `/api/phase1` | read-only | Phase 1 工作区配置 alias。 |
| GET | `/api/mt5-readonly` | read-only | MT5 read-only bridge base. |
| GET | `/api/mt5-readonly/:endpoint` | read-only | Status/account/positions/orders/symbols/quote/snapshot style endpoints. |
| GET | `/api/mt5-symbol-registry` | read-only | Symbol registry base. |
| GET | `/api/mt5-symbol-registry/:endpoint` | read-only | Symbol registry sub-endpoints. |
| GET | `/api/mt5-backtest-loop` | research-only | Backend backtest loop status/result. |
| GET | `/api/mt5-backtest-loop/run` | research-only | Trigger research-only backtest loop. |
| POST | `/api/paramlab/auto-tester/:action` | guarded-control | ParamLab auto-tester action surface. |
| GET | `/api/mt5-pending-worker/status` | read-only | Pending worker status. |
| POST | `/api/mt5-pending-worker/run` | guarded-control | Worker run action. |
| GET | `/api/mt5-adaptive-control/status` | read-only | Adaptive control status. |
| POST | `/api/mt5-adaptive-control/run` | guarded-control | Adaptive control action. |
| ANY | `/api/mt5-platform/:endpoint` | guarded-control | Platform store endpoint. |
| ANY | `/api/mt5-trading/:endpoint` | guarded-control | Trading bridge endpoint; must remain dryRun/KillSwitch guarded. |
| ANY | `/api/mt5/:endpoint` | guarded-control | Compatibility alias. |
| DELETE | `/api/mt5/order/:ticket` | guarded-control | Cancel route; must remain guarded and explicitly authorized. |

`guarded-control` does not mean open trading permission. It means the endpoint can be an action surface, but must still be constrained by backend, EA, dryRun, Kill Switch and manual authorization controls.

## Polymarket Research API

| Method | Path | Mode |
|---|---|---|
| GET | `/api/polymarket/history` | read-only |
| GET | `/api/polymarket/real-trades` | read-only |
| GET | `/api/polymarket/radar` | read-only |
| GET | `/api/polymarket/radar-ledger` | read-only-csv |
| GET | `/api/polymarket/markets` | read-only |
| GET | `/api/polymarket/market` | read-only |
| GET | `/api/polymarket/book` | read-only |
| GET | `/api/polymarket/asset-opportunities` | read-only |
| GET | `/api/polymarket/radar-worker` | read-only |
| GET | `/api/polymarket/radar-worker-ledger` | read-only-csv |
| GET | `/api/polymarket/cross-linkage` | read-only |
| GET | `/api/polymarket/cross-market-linkage-ledger` | read-only-csv |
| GET | `/api/polymarket/canary-executor-contract` | read-only |
| GET | `/api/polymarket/canary-executor-ledger` | read-only-csv |
| GET | `/api/polymarket/auto-governance` | read-only |
| GET | `/api/polymarket/auto-governance-ledger` | read-only-csv |
| GET | `/api/polymarket/canary-executor-run` | read-only |
| GET | `/api/polymarket/ai-score` | read-only |
| GET | `/api/polymarket/ai-score-ledger` | read-only-csv |
| GET | `/api/polymarket/canary-exit-ledger` | read-only-csv |
| GET | `/api/polymarket/canary-order-audit-ledger` | read-only-csv |
| GET | `/api/polymarket/canary-position-ledger` | read-only-csv |
| GET | `/api/polymarket/analyze/history` | read-only |
| GET | `/api/polymarket/search` | read-only |
| POST | `/api/polymarket/single-market-request` | research-only |
| POST | `/api/polymarket/analyze` | research-only |
| GET | `/api/polymarket/single-market-analysis` | read-only |
| GET | `/api/polymarket/single-market-analysis-ledger` | read-only-csv |
