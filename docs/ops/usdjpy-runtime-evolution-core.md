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
