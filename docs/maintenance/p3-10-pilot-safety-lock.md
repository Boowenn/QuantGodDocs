# P3-10 维护说明：实盘试点安全锁

## 阶段定位

P3-10 是 P3-6/P3-7/P3-8/P3-9 之后的安全收口层。

当前本机可能出现：

```text
tradeStatus=READY
executionEnabled=true
readOnlyMode=false
pilotKillSwitch=false
```

这意味着环境层不是只读。P3-10 的任务是让后续任何试点前都必须经过 fail-closed 证据检查和人工确认。

## 过门条件

- Backend 单测通过
- Node guard 通过
- `run_pilot_safety_lock.py check --write` 能生成 `QuantGod_PilotSafetyLock.json`
- 默认无 env 时结论必须是 `BLOCKED`
- 缺 runtime / 快通道 / 自适应闸门 / 入场触发 / 动态止盈止损时必须阻断
- Telegram 文案必须中文优先
- 文案必须明确不会下单、不会平仓、不会撤单

## 禁止范围

- 禁止加入 `OrderSend`、`OrderSendAsync`、`CTrade`、`TRADE_ACTION_DEAL`
- 禁止写 MT5 OrderRequest
- 禁止改 live preset
- 禁止接 Telegram command receiver
- 禁止 webhook receiver
- 禁止 credential storage
- 禁止自动扩大手数或自动移除亏损限制

## 运维建议

P3-10 通过后，下一步不是打开自动交易，而是先做：

1. 只在 Telegram 推送 P3-10 检查结果。
2. 连续观察多天，确认所有 fail-closed 状态都正确。
3. 若进入人工最小仓位试点，必须保持 `0.01` 最大手数和日内亏损上限。
4. 任何一次 P3-10 阻断，都不能被 DeepSeek 或前端按钮覆盖。
