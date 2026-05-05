# P3-6 MT5 运行质量与自适应策略引擎

P3-6 把 MT5 运行快照、影子盘结果、AI 建议流水和策略评估表转成一份本地自适应策略审查。它的目标不是替 EA 下单，而是回答：

- 哪个品种、策略、方向和行情环境仍值得继续影子观察；
- 哪些方向因为近期影子结果太弱，应该暂停建议；
- 当前运行快照是否通过动态入场闸门；
- 动态止损、止盈和时间止损应该给人工复核提供什么参考；
- 是否需要推送一条中文 Telegram 摘要。

## 常用命令

在 `QuantGodBackend` 仓库执行：

```powershell
python tools\run_adaptive_policy.py --runtime-dir .\runtime build --symbols USDJPYc,XAUUSDc
python tools\run_adaptive_policy.py --runtime-dir .\runtime score --symbol USDJPYc
python tools\run_adaptive_policy.py --runtime-dir .\runtime gate --symbol USDJPYc
python tools\run_adaptive_policy.py --runtime-dir .\runtime sltp --symbol USDJPYc
python tools\run_adaptive_policy.py --runtime-dir .\runtime telegram-text --symbol USDJPYc
```

如果要把中文摘要推送到 Telegram，必须显式开启 push，并保持命令接收关闭：

```powershell
$env:QG_TELEGRAM_PUSH_ALLOWED="1"
$env:QG_TELEGRAM_COMMANDS_ALLOWED="0"
python tools\run_adaptive_policy.py --runtime-dir .\runtime telegram-text --symbol USDJPYc --send
```

## 输出文件

```text
runtime/adaptive/QuantGod_AdaptivePolicy.json
runtime/adaptive/QuantGod_DynamicEntryGate.json
runtime/adaptive/QuantGod_DynamicSLTPPlan.json
runtime/adaptive/QuantGod_AdaptivePolicyLedger.csv
```

## 读取的数据

引擎只读取本地证据文件：

```text
QuantGod_MT5RuntimeSnapshot_*.json
QuantGod_Dashboard.json
ShadowCandidateOutcomeLedger.csv
QuantGod_CloseHistory*.csv
QuantGod_StrategyEvaluationReport.csv
journal/QuantGod_AIAdvisoryJournal.jsonl
journal/QuantGod_AIAdvisoryOutcomes.jsonl
```

缺文件时只会降级为“样本不足”或“仅观察”，不会打开交易权限。

## 路线状态

| 状态 | 中文含义 |
|---|---|
| `ACTIVE_SHADOW_OK` | 影子证据较好，可以继续观察 |
| `WATCH_ONLY` | 证据一般，只观察不升级 |
| `INSUFFICIENT_DATA` | 样本不足 |
| `PAUSED` | 近期影子结果太弱，暂停该方向建议 |

## 安全边界

P3-6 只能本地读取和生成建议：

```text
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
modifyAllowed=false
credentialStorageAllowed=false
livePresetMutationAllowed=false
telegramCommandExecutionAllowed=false
webhookReceiverAllowed=false
brokerExecutionAllowed=false
writesMt5Preset=false
writesMt5OrderRequest=false
```

Telegram 文案必须明确写出：QuantGod 不会下单、平仓、撤单或修改实盘 preset。
