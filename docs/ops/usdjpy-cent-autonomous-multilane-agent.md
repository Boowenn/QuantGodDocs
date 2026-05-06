# QuantGod v2.3 三车道自主 Agent

QuantGod v2.3 的总纲是：实盘要窄，模拟要宽，升降级要快，回滚要硬。

这版把 USDJPY 美分账户主线、自主治理 Agent、MT5 多策略模拟、Polymarket 模拟账本和 Daily Autopilot 2.0 收到同一套生命周期里。取消人工审核不等于取消风控；Agent 只能写受控 patch，不能改源码、不能改 live preset，也不能绕过硬门禁。

## 三车道

### Live Lane

实盘车道只允许：

```text
USDJPYc
RSI_Reversal
LONG
cent account
MICRO_LIVE / LIVE_LIMITED
```

禁止 USDJPY SELL 实盘、非 RSI 实盘、非 USDJPY 实盘、前端 Quick Trade、Telegram 交易命令、DeepSeek 直接批准交易。

### MT5 Shadow Lane

MT5 模拟车道继续跑多策略，至少包括：

```text
RSI_Reversal
MA_Cross
BB_Triple
MACD_Divergence
SR_Breakout
USDJPY_TOKYO_RANGE_BREAKOUT
USDJPY_NIGHT_REVERSION_SAFE
USDJPY_H4_TREND_PULLBACK
```

这些策略可以进入 shadow、fast shadow、tester-only 和 paper live sim，但不能抢 `topLiveEligiblePolicy`。影子第一名只代表研究价值，不代表实盘资格。

### Polymarket Shadow Lane

Polymarket 只做模拟账本、跟单模拟、事件概率和宏观风险上下文。它不连接真实钱包，不签名交易，不使用真实 USDC，不下单、不撤单、不赎回。

前端统一展示为“真实资金折算 / 模拟账本”，避免误解成钱包真实亏损。

## 美分账户加速

默认配置：

```text
QG_ACCOUNT_MODE=cent
QG_ACCOUNT_CURRENCY_UNIT=USC
QG_CENT_ACCOUNT_ACCELERATION=1
QG_CENT_FAST_PROMOTION=1
QG_AUTO_MAX_LOT=2.0
QG_CENT_MICRO_LIVE_LOT=0.05
QG_CENT_OPPORTUNITY_LOT=0.10
QG_CENT_STANDARD_LOT=0.35
```

`2.0` 是系统仓位上限，不是固定下单手数。Agent 会按阶段、风险预算和硬风控计算当前允许仓位。

## 输出文件

```text
runtime/agent/QuantGod_AutonomousLifecycle.json
runtime/agent/QuantGod_MT5ShadowStrategyRanking.json
runtime/agent/QuantGod_MT5ShadowStrategyLedger.csv
runtime/agent/QuantGod_PolymarketShadowLane.json
runtime/agent/QuantGod_EABuildReproducibility.json
runtime/daily/QuantGod_DailyAutopilotV2.json
```

## 命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lifecycle --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime lanes --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime mt5-shadow --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime polymarket-shadow --write
python tools\run_usdjpy_autonomous_agent.py --runtime-dir .\runtime ea-repro --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime build --write
python tools\run_daily_autopilot_v2.py --runtime-dir .\runtime telegram-text --refresh --write
```

## 硬风控

以下条件不能被 AI、前端或 Telegram 放宽：

- 非 USDJPY；
- 非 RSI LONG 进入实盘；
- runtime 缺失、fallback 或陈旧；
- 快通道不是 `FAST` / `EA_DASHBOARD_OK`；
- 点差异常；
- news block；
- 连续亏损达到阈值；
- 当日亏损达到阈值；
- Polymarket 真实资金交易；
- 修改 EA 源码或 live preset。

## Frontend

前端只做 operator workbench，不做交易按钮。Dashboard / Evolution 应显示：

- Live Lane；
- MT5 Shadow Lane；
- Polymarket Shadow Lane；
- 美分账户状态；
- 当前执行阶段；
- 自动回滚状态；
- Daily Autopilot 2.0；
- EA source / preset / input hash 对账。

## DeepSeek 角色

DeepSeek 只解释晋级、回滚、参数变化和日报，不批准 live，不取消回滚，不提高 `maxLot`，不放宽 news、spread、runtime 或 fastlane 硬门禁。
