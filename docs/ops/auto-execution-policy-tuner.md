# P3-11 自动执行策略调参器

## 目标

P3-11 用来解决两个运营问题：

1. 入场过严，导致 EA 长时间不入场、错失机会。
2. 出场太早，导致本来能继续盈利的单子被过早保护或抛出。

这一步不会直接下单，也不会修改 MT5 preset。它只生成 EA 可读取的策略政策文件：

```text
runtime/adaptive/QuantGod_AutoExecutionPolicy.json
runtime/adaptive/QuantGod_AutoExecutionPolicyLedger.csv
```

## 核心思路

原来的入场逻辑容易变成：

```text
全部条件 100% 通过才允许入场
```

这会非常安全，但也会错过很多机会。P3-11 改成三档：

| 状态 | 含义 | 仓位 |
|---|---|---|
| 标准入场 | 核心安全和入场确认都通过 | 按风险预算，最大不超过 2 |
| 机会入场 | 核心安全通过，但战术确认缺一项 | 小仓试探 |
| 阻断 | 核心安全缺失或历史方向为负 | 0 |

## 不能放宽的核心安全

下面任一项失败，必须阻断：

- runtime 快照缺失或陈旧
- fallback=true
- 快通道质量降级或缺失
- 动态止盈止损计划缺失
- 历史方向明显负期望
- 自适应入场闸门包含核心阻断原因

也就是说，P3-11 不是“乱放宽”，而是允许在核心安全通过时，把 M1/M5 二次确认、bar close、回踩确认这类战术项降一级处理。

## 仓位为什么不能固定 2

系统支持最大仓位设为 2：

```text
QG_AUTO_MAX_LOT=2.0
```

但不会无条件每次 2 手。实际建议仓位由这些参数共同决定：

- 最大仓位
- 单笔风险百分比
- 入场等级
- 综合评分
- 机会入场折扣

机会入场默认只使用小仓：

```text
QG_AUTO_OPPORTUNITY_LOT_MULTIPLIER=0.35
```

这样可以减少“错失机会”，但不会把弱确认机会直接变成满仓。

## 出场调参

P3-11 会根据影子样本表现输出出场参数：

- 保本延后 R 值
- 移动止损启动 R 值
- 时间止损 K 线数量
- 出场模式

如果近期样本为正，会倾向于：

```text
保本延后半档，移动止损延后半档，让盈利单多跑一段
```

如果只是机会入场，则仍然更快保护本金。

## 命令

```powershell
python tools\run_auto_execution_policy.py --runtime-dir .\runtime config

python tools\run_auto_execution_policy.py --runtime-dir .\runtime build `
  --symbols USDJPYc,EURUSDc,XAUUSDc `
  --write

python tools\run_auto_execution_policy.py --runtime-dir .\runtime plan `
  --symbol USDJPYc `
  --direction LONG

python tools\run_auto_execution_policy.py --runtime-dir .\runtime telegram-text `
  --symbols USDJPYc,EURUSDc,XAUUSDc
```

发送中文 Telegram：

```powershell
python tools\run_auto_execution_policy.py --runtime-dir .\runtime telegram-text `
  --symbols USDJPYc `
  --send
```

## 本地配置

复制：

```powershell
Copy-Item .env.auto.local.example .env.auto.local
```

常用参数：

```text
QG_AUTO_MAX_LOT=2.0
QG_AUTO_RISK_PER_TRADE_PCT=0.5
QG_AUTO_OPPORTUNITY_LOT_MULTIPLIER=0.35
QG_AUTO_STANDARD_LOT_MULTIPLIER=1.0
QG_AUTO_MIN_LOT=0.01
QG_AUTO_LOT_STEP=0.01
QG_AUTO_ACCOUNT_EQUITY=1000.0
```

## 安全边界

P3-11 不做：

- 下单
- 平仓
- 撤单
- 修改订单 SL/TP
- 修改 live preset
- 写 MT5 OrderRequest
- 接收 Telegram 交易命令
- 开放 webhook 执行入口
- 存储密码、token、private key

EA 后续如果读取 `QuantGod_AutoExecutionPolicy.json`，也必须再次做 MT5 侧保证金、最小手数、最大手数、手数步进和止损距离校验。
