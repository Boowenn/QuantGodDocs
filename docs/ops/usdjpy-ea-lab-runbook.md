# USDJPY EA 实验室 Runbook

本 Runbook 用于确认 USDJPY 新策略是否已经开始模拟采样，以及如何读取结果。

## 1. 生成本地样本

```bash
cd ../QuantGodBackend
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime_usdjpy_test sample --overwrite
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime_usdjpy_test build --write
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime_usdjpy_test signals
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime_usdjpy_test backtest-plan
```

## 2. 导入回测结果

Strategy Tester 或外部回测输出为 CSV/JSON 后，可以导入到 USDJPY 实验室：

```bash
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime import-backtest \
  --source /absolute/path/to/usdjpy_tester_result.csv

python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime imported-backtests
```

导入只接受本机文件，只写 `runtime/adaptive/QuantGod_USDJPYBacktestImports*.json*`。它不会启动 tester、不会下单、不会修改实盘参数。

## 3. 查看真实 runtime

```bash
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime catalog
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime signals --limit 20
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime risk-check
python tools/run_usdjpy_strategy_lab.py --runtime-dir ./runtime candidate-policy --write
```

## 4. 前端检查

打开 Vue 工作台 Dashboard，查看“USDJPY 单品种策略实验室”：

- 策略工厂目录应显示三条 shadow 策略
- 实时候选信号应显示最近采样
- 回测计划应说明每条策略该怎么验证
- 已导入回测应显示 PF、胜率和交易数
- 风险检查应显示 runtime、快通道、新闻和 shadow 隔离状态

## 5. 实盘状态

现有 RSI live 策略保持恢复状态。三条新增策略只做模拟采样，不会进入实盘自动下单。

## 6. 升级条件

新增策略进入下一阶段前至少需要：

- 样本量足够
- 胜率和 Profit Factor 达标
- MFE/MAE 支持合理止盈止损
- 高影响 USD/JPY 新闻过滤有效
- 通过 ParamLab、治理复核和版本门禁
