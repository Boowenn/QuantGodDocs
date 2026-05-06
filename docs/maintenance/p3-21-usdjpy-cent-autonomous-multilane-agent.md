# P3-21 维护记录：USDJPY 美分账户三车道自主 Agent

P3-21 将 QuantGod 从单一 USDJPY 自主治理门扩展为三车道自主生命周期：

```text
Live Lane              USDJPYc / RSI_Reversal / LONG / cent account
MT5 Shadow Lane        USDJPY 多策略模拟、回放、tester 和 ranking
Polymarket Shadow Lane 模拟账本、跟单模拟和事件风险上下文
```

## 本阶段新增

```text
tools/autonomous_lifecycle/
tools/daily_autopilot_v2/
tools/run_daily_autopilot_v2.py
```

新增 API：

```text
GET  /api/usdjpy-strategy-lab/autonomous-agent/lifecycle
GET  /api/usdjpy-strategy-lab/autonomous-agent/lanes
GET  /api/usdjpy-strategy-lab/autonomous-agent/mt5-shadow
GET  /api/usdjpy-strategy-lab/autonomous-agent/polymarket-shadow
GET  /api/usdjpy-strategy-lab/autonomous-agent/ea-repro
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/status
POST /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/run
GET  /api/usdjpy-strategy-lab/autonomous-agent/daily-autopilot-v2/telegram-text
```

## 字段语义

旧的人工审批语义被替换为自主治理字段：

```text
patchWritable=true
liveMutationAllowed=false
executionStage=SHADOW / FAST_SHADOW / TESTER_ONLY / PAPER_LIVE_SIM / MICRO_LIVE / LIVE_LIMITED
requiresManualReview=false
requiresAutonomousGovernance=true
autoApplyAllowed=stage_gated
```

`patchWritable` 只表示 Agent 可以写受控 patch 文件；`liveMutationAllowed=false` 表示 Agent 不能直接修改 live preset。

## 安全边界

- Live Lane 只允许 USDJPYc / RSI_Reversal / LONG；
- MT5 Shadow Lane 可以多策略模拟，但不能直接进真钱实盘；
- Polymarket 永远不连接真实钱包，不下单；
- 最大 2.0 是上限，不是固定仓位；
- Agent 不修改 `.mq5` 源码；
- Agent 不写 MT5 OrderRequest；
- Telegram 只推送，不接交易命令；
- Daily Autopilot 只生成中文计划和复盘，不越权交易。

## 验证

```powershell
cd C:\QuantGod\QuantGodBackend

python -m unittest tests.test_autonomous_lifecycle tests.test_usdjpy_autonomous_agent -v
node --test tests\node\test_autonomous_lifecycle_guard.mjs tests\node\test_usdjpy_autonomous_agent_guard.mjs

cd C:\QuantGod\QuantGodFrontend
npm run usdjpy-evolution
npm run test:usdjpy-evolution
```
