# P3-10 实盘试点安全锁

P3-10 的目标是：在本机已经出现 `executionEnabled=true`、`readOnlyMode=false` 这类环境状态时，给 QuantGod 增加一个 fail-closed 的实盘试点前置锁。

它不是交易执行器，也不会发单。它只回答一个问题：

> 当前证据是否足够进入“人工最小仓位试点复核”？

## 默认结论

默认永远是阻断。

即使 runtime、快通道、自适应入场闸门、入场触发计划、动态止盈止损全部通过，如果没有人工本地确认，仍然阻断。

需要同时满足：

- `QG_PILOT_EXECUTION_ALLOWED=1`
- `QG_PILOT_CONFIRMATION_PHRASE=我确认仅允许最小仓位试点，禁止自动扩大风险`
- 最大手数不超过 `0.01`
- 日内最多次数不超过 `3`
- 日内最大亏损不超过 `1R`
- 品种和策略都在白名单内
- runtime snapshot 存在、非 fallback、新鲜
- MT5 fast lane quality 通过
- P3-6 自适应入场闸门通过
- P3-9 入场触发处于复核态
- P3-8 动态止盈止损计划存在且可复核

## 命令

```powershell
python tools\run_pilot_safety_lock.py config

python tools\run_pilot_safety_lock.py --runtime-dir .\runtime --symbol USDJPYc --direction LONG check --write

python tools\run_pilot_safety_lock.py --runtime-dir .\runtime status

python tools\run_pilot_safety_lock.py --runtime-dir .\runtime --symbol USDJPYc --direction LONG telegram-text --refresh --write
```

发送中文 Telegram 文案：

```powershell
python tools\run_pilot_safety_lock.py --runtime-dir .\runtime --symbol USDJPYc --direction LONG telegram-text --refresh --write --send
```

## 本地 env

复制 example：

```powershell
Copy-Item .env.pilot.local.example .env.pilot.local
notepad .env.pilot.local
```

示例默认阻断：

```text
QG_PILOT_EXECUTION_ALLOWED=0
QG_TELEGRAM_COMMANDS_ALLOWED=0
```

如果人工试点复核，必须显式写入确认短语。这个文件只留在本机，不提交。

## 输出文件

```text
runtime/safety/QuantGod_PilotSafetyLock.json
```

## 安全边界

P3-10 不做：

- 不下单
- 不平仓
- 不撤单
- 不修改订单
- 不修改 MT5 SL/TP
- 不修改 live preset
- 不写 MT5 OrderRequest
- 不接收 Telegram 交易命令
- 不开放 webhook 执行入口
- 不存储密码、token、private key

P3-10 只是实盘前置检查和中文 Telegram 复核文本。
