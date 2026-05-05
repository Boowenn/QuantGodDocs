# P3-8 动态止盈止损校准

P3-8 增加一层本地只读校准逻辑，用来把影子模拟里的 MFE/MAE 分布转换成动态止损、分批止盈和移动保护建议。它只生成证据和建议，不会修改 MT5 持仓、订单或实盘 preset。

## 目标

不同品种、策略、方向和行情环境下，固定止损止盈很容易失真。P3-8 会按 `symbol / strategy / direction / regime` 聚合最近影子结果，计算 MFE、MAE、胜率、平均收益和快通道质量，然后给出“已校准、仅观察、样本不足、暂停”四类结论。

## 输入证据

校准器只读取本地 runtime 证据：

- `ShadowCandidateOutcomeLedger.csv`
- `QuantGod_StrategyEvaluationReport.csv`
- `quality/QuantGod_MT5FastLaneQuality.json`

## 输出文件

校准器会写出：

- `runtime/adaptive/QuantGod_DynamicSLTPCalibration.json`
- `runtime/adaptive/QuantGod_DynamicSLTPCalibrationLedger.csv`

## 常用命令

```powershell
python tools\run_dynamic_sltp.py --runtime-dir .\runtime sample --overwrite
python tools\run_dynamic_sltp.py --runtime-dir .\runtime build --symbols USDJPYc,EURUSDc,XAUUSDc
python tools\run_dynamic_sltp.py --runtime-dir .\runtime plan --symbol USDJPYc --strategy RSI_Reversal --direction LONG
python tools\run_dynamic_sltp.py --runtime-dir .\runtime telegram-text --symbol USDJPYc
```

## 计划状态

| 状态 | 中文含义 | 判断逻辑 |
|---|---|---|
| `CALIBRATED` | 已校准 | 样本达到最低要求，MFE/MAE 分布有效，平均收益不为负。 |
| `WATCH_ONLY` | 仅观察 | 证据偏弱、平均收益偏差，或 MT5 快通道质量降级。 |
| `INSUFFICIENT_DATA` | 样本不足 | 该分组样本数量不足，不能生成可靠建议。 |
| `PAUSED` | 暂停 | 历史影子结果明显为负，或 MFE/MAE 分布不可用。 |

## 安全边界

P3-8 不是交易执行引擎。

它不会：

- 下单
- 平仓
- 撤单
- 修改 MT5 订单止损止盈
- 修改 live preset
- 保存凭据
- 接收 Telegram 命令
- 写入 MT5 order request 文件

所有 Telegram 摘要都是中文优先，并明确标注“只做影子评估和人工复核，不执行交易”。
