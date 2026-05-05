# P3-12 自动化链路运行器

P3-12 把当前已经完成的几个只读/影子模块串成一条本地自动化链路：

```text
P3-7 快通道质量
→ P3-6 自适应策略
→ P3-8 动态止盈止损
→ P3-9 入场触发
→ P3-11 自动执行政策
→ 中文 Telegram 巡检
→ Dashboard 可视化
```

它解决的问题不是“直接下单”，而是让每一轮运行都自动写出最新证据，让你能看到：

- 为什么阻断；
- 缺哪个证据；
- 哪些方向进入标准入场；
- 哪些方向进入机会入场；
- 当前建议仓位是多少；
- Telegram 中文摘要是否已经推送。

## 安全边界

P3-12 不会：

- 下单；
- 平仓；
- 撤单；
- 修改订单；
- 修改 MT5 SL/TP；
- 修改 live preset；
- 写 MT5 OrderRequest；
- 接收 Telegram 交易命令；
- 开放 webhook 执行入口；
- 存储密码、token、private key。

P3-12 只会生成：

```text
runtime/automation/QuantGod_AutomationChainLatest.json
runtime/automation/QuantGod_AutomationChainRun.json
runtime/automation/QuantGod_AutomationChainLedger.csv
```

## 命令

运行一次：

```powershell
python tools\run_automation_chain.py --runtime-dir .\runtime --symbols USDJPYc,EURUSDc,XAUUSDc once
```

运行一次并发送 Telegram 中文摘要：

```powershell
python tools\run_automation_chain.py --runtime-dir .\runtime --symbols USDJPYc,EURUSDc,XAUUSDc once --send
```

查看状态：

```powershell
python tools\run_automation_chain.py --runtime-dir .\runtime status
```

只生成 Telegram 文案：

```powershell
python tools\run_automation_chain.py --runtime-dir .\runtime telegram-text --refresh
```

循环运行：

```powershell
python tools\run_automation_chain.py --runtime-dir .\runtime --symbols USDJPYc,EURUSDc,XAUUSDc loop --interval-seconds 300 --send
```

## Dashboard API

新增本地 API：

```text
GET  /api/automation-chain/status
GET  /api/automation-chain/telegram-text?refresh=1
POST /api/automation-chain/run
```

这些 API 仍然只面向本机 Dashboard。`POST /api/automation-chain/run` 只运行证据链和政策生成，不触发交易。

## 前端显示

Dashboard 新增“自动化链路”面板，显示：

- 链路步骤；
- 缺失证据；
- 阻断原因；
- 标准入场数量；
- 机会入场数量；
- 当前建议仓位；
- 运行一次按钮。

前端仍然只能通过 `/api/*` 读取，不允许直接读取 `QuantGod_*.json/csv`。
