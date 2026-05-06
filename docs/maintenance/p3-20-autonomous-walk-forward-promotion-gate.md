# P3-20 维护记录：自主 Walk-forward 晋级门

P3-20 新增 USDJPY 自主治理 Agent，把 P3-19 的因果回放结果继续推进到 train / validation / forward 三段筛选，再由机器硬风控决定候选进入 `SHADOW_ONLY`、`TESTER_ONLY`、`PAPER_LIVE_SIM`、`MICRO_LIVE` 或 `LIVE_LIMITED`。

## 本阶段新增

```text
tools/usdjpy_walk_forward/
tools/run_usdjpy_walk_forward.py
tools/usdjpy_autonomous_agent/
tools/run_usdjpy_autonomous_agent.py
```

新增 API：

```text
GET  /api/usdjpy-strategy-lab/walk-forward/status
POST /api/usdjpy-strategy-lab/walk-forward/build
GET  /api/usdjpy-strategy-lab/walk-forward/selection
GET  /api/usdjpy-strategy-lab/walk-forward/proposal
GET  /api/usdjpy-strategy-lab/autonomous-agent/state
POST /api/usdjpy-strategy-lab/autonomous-agent/run
GET  /api/usdjpy-strategy-lab/autonomous-agent/decision
GET  /api/usdjpy-strategy-lab/autonomous-agent/patch
```

## 安全边界

- `requiresAutonomousGovernance=true`；
- `completedByAgent=true`；
- `requiresAutonomousGovernance=true`；
- `autoApplyAllowed=stage_gated`；
- Agent 只写受控 patch；
- 不下单、不平仓、不撤单；
- 不修改 MT5 live preset；
- 不写 MT5 OrderRequest；
- Telegram 只推送，不接命令。

## 验证

```powershell
cd C:\QuantGod\QuantGodBackend

python -m unittest tests.test_usdjpy_runtime_dataset tests.test_usdjpy_bar_replay tests.test_usdjpy_autonomous_agent -v
node --test tests\node\test_usdjpy_runtime_dataset_guard.mjs tests\node\test_usdjpy_bar_replay_guard.mjs tests\node\test_usdjpy_autonomous_agent_guard.mjs

cd C:\QuantGod\QuantGodFrontend
npm run usdjpy-evolution
npm run test:usdjpy-evolution
```
