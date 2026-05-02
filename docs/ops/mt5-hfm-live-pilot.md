# MT5 HFM Live Pilot 运维

## 账户与运行边界

Live Pilot 只允许在明确授权、正确账户、正确 server、正确 symbol universe 下运行。任何 live 变更必须保留 `0.01`、单仓、SL/TP、session/news/cooldown/order-send 风控。

## 核心证据

- `QuantGod_Dashboard.json`
- `QuantGod_MT5_ShadowStatus.txt`
- `QuantGod_TradeJournal.csv`
- `QuantGod_CloseHistory.csv`
- `QuantGod_GovernanceAdvisor.json`
- `QuantGod_ParamLabStatus.json`
- `QuantGod_MT5PendingOrderWorker.json`
- `MQL5/Logs`
- live preset：`QuantGod_MT5_HFM_LivePilot.set`

## 安全检查

- Dashboard snapshot 新鲜。
- Build 版本不降级。
- live preset 未漂移。
- open positions 数量、volume、SL/TP、magic 合规。
- pending order worker 保持 dryRun/killSwitch/orderSendAllowed=false，除非人工明确授权且代码路径允许。
- 非 RSI legacy route 不得绕过第二授权锁。

## 操作限制

LLM 或自动化不能替用户下单、平仓、撤单、解除 Kill Switch、修改 live preset、放宽 gate、关闭 news block 或强行开放 session。
