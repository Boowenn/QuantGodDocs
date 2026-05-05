# P3-11 维护记录：自动执行策略调参器

## 阶段目标

把系统从“全部条件满足才入场”升级为“核心安全必须满足，战术确认分级处理”。

## 新增能力

- 标准入场 / 机会入场 / 阻断 三档输出。
- 最大仓位支持 2，但实际仓位按风险预算和机会等级计算。
- 机会入场只允许小仓试探。
- 出场参数支持保本延后、移动止损延后和时间止损建议。
- Telegram 文案为中文运营说明。

## 生成文件

```text
runtime/adaptive/QuantGod_AutoExecutionPolicy.json
runtime/adaptive/QuantGod_AutoExecutionPolicyLedger.csv
```

## 输入证据

- MT5 runtime snapshot
- MT5 fast lane quality
- P3-6 DynamicEntryGate
- P3-8 DynamicSLTPPlan 或 DynamicSLTPCalibration
- ShadowCandidateOutcomeLedger

## Fail-closed 规则

缺少以下任一核心证据，必须阻断：

- runtime snapshot
- fast lane quality
- dynamic SLTP plan
- entry gate core safety

## Forbidden scope

本阶段禁止：

- 真实下单
- 平仓、撤单、修改订单
- 修改 MT5 SL/TP
- 修改 live preset
- 写 OrderRequest
- Telegram 命令交易
- webhook 交易入口
- 多用户、billing、broker adapter

## 验证命令

```powershell
python -m py_compile tools\run_auto_execution_policy.py tools\auto_execution_policy\schema.py tools\auto_execution_policy\data_loader.py tools\auto_execution_policy\strictness_tuner.py tools\auto_execution_policy\lot_sizer.py tools\auto_execution_policy\exit_tuner.py tools\auto_execution_policy\policy_engine.py tools\auto_execution_policy\telegram_text.py
python -m unittest discover tests -v
node --test tests\node\test_auto_execution_policy_guard.mjs
python tools\run_auto_execution_policy.py --runtime-dir .\runtime_auto_policy_test sample --overwrite
python tools\run_auto_execution_policy.py --runtime-dir .\runtime_auto_policy_test build --symbols USDJPYc --write
python tools\run_auto_execution_policy.py --runtime-dir .\runtime_auto_policy_test telegram-text --symbols USDJPYc
```
