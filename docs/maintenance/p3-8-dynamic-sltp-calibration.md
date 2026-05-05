# P3-8 维护记录：动态止盈止损校准

## 阶段位置

P3-8 接在 P3-7 MT5 Runtime Fast Lane 之后。P3-7 负责提高运行证据质量，P3-8 负责把影子样本中的 MFE/MAE 分布转成动态止损止盈建议。

## 范围

允许：

- 读取本地 runtime CSV/JSON 证据。
- 计算 MFE/MAE 分位数。
- 生成动态初始止损、分批目标和移动保护建议。
- 生成中文 Telegram 摘要。
- 写入本地 adaptive evidence 文件。

禁止：

- MT5 下单。
- 平仓、撤单、改仓。
- 修改 live preset。
- 保存凭据。
- 接收 Telegram 命令。
- Webhook receiver。
- Broker 执行。

## 验证命令

```powershell
python -m py_compile tools\run_dynamic_sltp.py tools\dynamic_sltp\schema.py tools\dynamic_sltp\data_loader.py tools\dynamic_sltp\calibrator.py tools\dynamic_sltp\telegram_text.py
python -m unittest discover tests -v
node --test tests\node\test_dynamic_sltp_guard.mjs
python tools\run_dynamic_sltp.py --runtime-dir .\runtime sample --overwrite
python tools\run_dynamic_sltp.py --runtime-dir .\runtime build --symbols USDJPYc
python tools\run_dynamic_sltp.py --runtime-dir .\runtime telegram-text --symbol USDJPYc
```

## 预期产物

```text
runtime/adaptive/QuantGod_DynamicSLTPCalibration.json
runtime/adaptive/QuantGod_DynamicSLTPCalibrationLedger.csv
```

## 运维说明

不要把这些数值直接接到 MT5 订单修改逻辑。它们只用于影子复盘、Telegram 报告和后续 policy gate。
