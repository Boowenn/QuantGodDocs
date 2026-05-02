# MT5 / HFM Live Pilot Runbook

Live Pilot 是 QuantGod 在 HFM MT5 上的小风险实盘模式。它必须同时受到 EA guard、live preset、Kill Switch、authorization lock、dryRun 默认值、news filter 和 dashboard 只读边界保护。

## 实盘前检查

1. `QuantGodBackend` CI 必须通过。
2. `python tools\ci_guard.py` 必须通过。
3. HFM live preset 中的 lot size、symbol universe、session、news block、SL/TP、startup guard 等值必须符合预期。
4. MT5 read-only bridge 能读取账户、持仓、订单和 symbol registry。
5. Frontend 必须从 `Dashboard/vue-dist` 服务，而不是从 Backend 残留的 Vue 源码服务。
6. Telegram 必须保持 push-only，不允许任何 command execution。

## 运行中需要监控

- 当前 open positions 和 pending orders。
- 当日 realized / floating PnL。
- Kill Switch 状态。
- news filter 状态。
- consecutive loss cooldown。
- AI advisory output。
- Governance Advisor evidence。
- ParamLab / backend backtest 的 candidate 结果。

## 需要暂停或人工确认的情况

出现以下任一情况时，应暂停或进入人工复核：

- Kill Switch 触发。
- `ci_guard.py` 发现 live preset drift。
- Backend API 暴露了未设计的写入面。
- Telegram 出现可执行交易命令入口。
- Frontend 再次直接读取 runtime JSON/CSV。
- EA 日志出现 order-send failure、未知 magic、缺失 SL/TP 或异常频繁保护触发。

## 明确禁止

- 不通过文档、前端按钮或通知入口绕过 Kill Switch。
- 不用 Docs 或 Infra 脚本修改 live preset。
- 不把真实账号密码、只读密码、交易密码写进仓库。
- 不把 Strategy Tester 的实验配置误同步到 HFM live preset。
