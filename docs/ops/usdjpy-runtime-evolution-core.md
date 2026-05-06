# USDJPY 自学习闭环

USDJPY 自学习闭环把 MT5/EA 的运行证据整理成可复盘的数据集，再自动生成回放报告、参数候选和实盘配置提案。它的目标不是直接改实盘，而是每天用证据回答：

- 为什么 EA 没买；
- 哪些阻断是合理的；
- 哪些机会可能被错过；
- 哪些盈利单可能被过早保护出场；
- 明天应该拿哪些参数进入 tester-only / shadow 验证。

## 输出文件

```text
runtime/datasets/usdjpy/QuantGod_USDJPYRuntimeDataset.json
runtime/datasets/usdjpy/QuantGod_USDJPYDecisionSamples.jsonl
runtime/replay/usdjpy/QuantGod_USDJPYReplayReport.json
runtime/replay/usdjpy/QuantGod_USDJPYMissedOpportunityReport.json
runtime/replay/usdjpy/QuantGod_USDJPYExitHoldReport.json
runtime/adaptive/QuantGod_USDJPYParamCandidates.json
runtime/adaptive/QuantGod_USDJPYParamTuningReport.json
runtime/adaptive/QuantGod_USDJPYLiveConfigProposal.json
```

## P3-18 回放精度口径

P3-18 把回放从“粗略事项列表”升级为“可比较的研究证据”。核心变化：

- 主计量口径统一为 `R` 倍数，辅助口径为 `pips`；
- `USC` 金额只保留为账面参考，不再和 `MFE/MAE` 混算；
- 错失机会会尽量记录 15 / 30 / 60 / 120 分钟后验表现；
- 盈利早出会计算 `profitCaptureRatio`，判断利润捕获比例；
- 回放报告新增候选对比：`current`、`relaxed_entry_v1`、`let_profit_run_v1`。

这仍然不是完整 tick/bar 级策略优化器。如果后验路径不足，报告会明确写成：

```text
NEEDS_BAR_REPLAY
```

这类结论只能进入 replay / tester-only / shadow 验证，不能直接修改实盘 preset。

## 日常命令

```powershell
cd C:\QuantGod\QuantGodBackend

python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime status --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime replay --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime tune --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime proposal --write
python tools\run_usdjpy_runtime_dataset.py --runtime-dir .\runtime telegram-text --refresh
```

## 安全边界

这条链路只写本地研究证据，不会下单、平仓、撤单，也不会修改 MT5 live preset。所有 `QuantGod_USDJPYLiveConfigProposal.json` 都必须保持：

```text
autoApplyAllowed=false
requiresManualReview=true
```

参数候选只能进入 replay、tester-only 或 shadow 验证；不能直接进入实盘。

## 前端位置

Dashboard 会显示 “USDJPY 自学习闭环” 面板。它展示数据集样本、错失机会、过早出场、参数候选和配置提案状态。这个面板是只读运营视图，按钮只触发证据重建，不触发交易。

前端会额外展示“回放候选对比”和“预期影响 / 风险变化”。这些字段来自：

```text
QuantGod_USDJPYReplayReport.json
QuantGod_USDJPYParamTuningReport.json
QuantGod_USDJPYLiveConfigProposal.json
```
