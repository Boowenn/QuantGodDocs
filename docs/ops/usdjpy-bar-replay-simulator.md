# USDJPY 因果回放模拟器

P3-19 把 USDJPY 自学习闭环从“后验样本估算”推进到因果回放比较。它只做 USDJPYc，只读本地运行证据，不下单、不平仓、不撤单、不修改 MT5 live preset。

## 核心原则

回放必须是 causal replay：

- 每一步只能使用当时那根 bar / tick 已经存在的数据；
- RSI、时段、点差、新闻、冷却、启动保护和仓位容量都是当时守门；
- 15 / 30 / 60 / 120 分钟后验窗口只能用于评分；
- 后验结果不能决定当时是否入场；
- DeepSeek 只能解释报告，不能覆盖回放评分。

## 比较对象

```text
current
  当前真实规则。

relaxed_entry_v1
  只放宽 RSI / 战术确认一档。
  session、spread、news、runtime freshness、fastlane 和 cooldown 仍必须通过。

let_profit_run_v1
  只调整出场持有：保本延后、trailing 延后、MFE 回吐容忍提高。
```

## 输出文件

```text
runtime/replay/usdjpy/QuantGod_USDJPYBarReplayReport.json
runtime/replay/usdjpy/QuantGod_USDJPYEntryVariantComparison.json
runtime/replay/usdjpy/QuantGod_USDJPYExitVariantComparison.json
runtime/replay/usdjpy/QuantGod_USDJPYReplayLedger.csv
```

## 命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_bar_replay.py --runtime-dir .\runtime status --write
python tools\run_usdjpy_bar_replay.py --runtime-dir .\runtime entry --write
python tools\run_usdjpy_bar_replay.py --runtime-dir .\runtime exit --write
python tools\run_usdjpy_bar_replay.py --runtime-dir .\runtime telegram-text --refresh
```

## 结论等级

```text
REJECTED
SHADOW_ONLY
TESTER_ONLY
LIVE_CONFIG_PROPOSAL_ELIGIBLE
```

即使进入 `LIVE_CONFIG_PROPOSAL_ELIGIBLE`，也只是进入实盘配置提案审查，不会自动改 preset。

## Telegram

Telegram 文案必须是中文，并且必须包含：

- 主口径 R；
- 实盘修改：无；
- 入场候选对比；
- 出场候选对比；
- 因果边界；
- 安全边界。

## 安全边界

```text
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
livePresetMutationAllowed=false
autoApplyAllowed=false
telegramCommandExecutionAllowed=false
posteriorMayAffectTrigger=false
```

