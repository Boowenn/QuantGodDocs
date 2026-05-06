# USDJPY 实盘闭环与每日自动复盘

## 目的

USDJPY 实盘闭环把“策略政策、EA 干跑、HFM live preset、运行快照”合并成一份中文运营证据。它回答三个问题：

- 现在 RSI_Reversal 买入路线是否已经恢复给现有 MT5 EA 判断。
- 如果没有入场，原因是行情、证据缺失、policy 阻断，还是 preset 未恢复。
- 每日待办和每日复盘是否已经把 USDJPY 自动链路跑完。

## 安全边界

该闭环只写本地 evidence 和 Telegram 中文说明，不下单、不平仓、不撤单、不修改订单、不修改 live preset。真实入场仍由已挂载的 MT5 EA 和 preset 风控决定。

## 主要文件

Backend 会写入：

- `runtime/live/QuantGod_USDJPYLiveLoopStatus.json`
- `runtime/live/QuantGod_USDJPYLiveIntent.json`
- `runtime/live/QuantGod_USDJPYDailyAutopilot.json`
- `runtime/live/QuantGod_USDJPYLiveLoopLedger.csv`

每日自动任务会在 `QuantGod_DailyAutopilot.json` 中附带 `usdJpyLiveLoopSummary`，前端可直接显示“为什么没入场”和“下一步自动动作”。

## 手动验证

```bash
python tools/run_usdjpy_live_loop.py --runtime-dir ./runtime once --write
python tools/run_usdjpy_live_loop.py --runtime-dir ./runtime telegram-text --refresh
python tools/run_daily_autopilot.py --runtime-dir ./runtime --once
```

## 判断规则

- `READY_FOR_EXISTING_EA`：运行快照新鲜、策略政策允许 RSI_Reversal 买入、live preset 只恢复 RSI 买入路线。
- `POLICY_BLOCKED`：证据存在但策略政策仍阻断，需要继续 retune/backtest。
- `POLICY_READY_PRESET_BLOCKED`：策略政策已就绪，但 live preset 未恢复或配置漂移。
- `EVIDENCE_MISSING`：运行快照或核心 evidence 缺失，系统 fail-closed。

