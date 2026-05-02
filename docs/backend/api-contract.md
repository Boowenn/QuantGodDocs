# 后端 API 契约

## 通用响应 envelope

统一 API 应尽量返回以下结构：

```json
{
  "ok": true,
  "endpoint": "/api/example",
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

## Phase 1 endpoints

```text
POST /api/ai-analysis/run
GET  /api/ai-analysis/latest
GET  /api/ai-analysis/history
GET  /api/ai-analysis/history/:id
GET  /api/ai-analysis/config
GET  /api/mt5-readonly/kline
GET  /api/mt5-readonly/trades
GET  /api/shadow-signals
```

## Phase 2 endpoints

```text
GET  /api/governance/advisor
GET  /api/governance/version-registry
GET  /api/governance/promotion-gate
GET  /api/governance/optimizer-v2
GET  /api/paramlab/status
GET  /api/paramlab/results
GET  /api/paramlab/scheduler
GET  /api/paramlab/recovery
GET  /api/paramlab/report-watcher
GET  /api/paramlab/tester-window
GET  /api/trades/journal
GET  /api/trades/close-history
GET  /api/trades/outcome-labels
GET  /api/trades/trading-audit
GET  /api/research/stats
GET  /api/research/stats-ledger
GET  /api/research/strategy-evaluation
GET  /api/research/regime-evaluation
GET  /api/research/manual-alpha
GET  /api/shadow/signals
GET  /api/shadow/outcomes
GET  /api/shadow/candidates
GET  /api/shadow/candidate-outcomes
GET  /api/dashboard/state
GET  /api/dashboard/backtest-summary
GET  /api/notify/config
GET  /api/notify/history
POST /api/notify/test
```

## Phase 3 endpoints

```text
POST /api/vibe-coding/generate
POST /api/vibe-coding/iterate
POST /api/vibe-coding/backtest
POST /api/vibe-coding/analyze
GET  /api/vibe-coding/strategies
GET  /api/vibe-coding/strategy/:id
GET  /api/vibe-coding/config
POST /api/ai-analysis-v2/run
GET  /api/ai-analysis-v2/latest
GET  /api/ai-analysis-v2/history
GET  /api/ai-analysis-v2/history/:id
GET  /api/ai-analysis-v2/config
GET  /api/kline/ai-overlays
GET  /api/kline/vibe-indicators
GET  /api/kline/realtime-config
```

## 前端规则

Frontend 不得直接 fetch `QuantGod_*.json` 或 `QuantGod_*.csv`。所有展示数据都应通过 `/api/*` facade 获取。
