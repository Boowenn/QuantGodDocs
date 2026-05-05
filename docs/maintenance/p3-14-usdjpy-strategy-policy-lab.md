# P3-14 维护记录：USDJPY 单品种多策略实验室

## 范围

P3-14 将自动化研究范围从多品种收窄为 USDJPY 单品种多策略：

```text
USDJPYc + RSI_Reversal
USDJPYc + MA_Cross
USDJPYc + BB_Triple
USDJPYc + MACD_Divergence
USDJPYc + SR_Breakout
```

其他品种不参与自动策略政策和 Telegram 主报告。

## 新增 Backend

```text
tools/usdjpy_strategy_lab/
tools/run_usdjpy_strategy_lab.py
Dashboard/usdjpy_strategy_lab_api_routes.js
```

## 新增 Frontend

```text
src/services/usdjpyStrategyLabApi.js
src/components/USDJPYStrategyPolicyPanel.vue
```

## 验收

Backend：

```powershell
python -m py_compile tools\run_usdjpy_strategy_lab.py tools\usdjpy_strategy_lab\schema.py tools\usdjpy_strategy_lab\data_loader.py tools\usdjpy_strategy_lab\strategy_scoreboard.py tools\usdjpy_strategy_lab\policy_builder.py tools\usdjpy_strategy_lab\dry_run_bridge.py tools\usdjpy_strategy_lab\telegram_text.py
python -m unittest discover tests -v
node --test tests\node\test_usdjpy_strategy_lab_guard.mjs
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime_usdjpy_test sample --overwrite
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime_usdjpy_test build --write
python tools\run_usdjpy_strategy_lab.py --runtime-dir .\runtime_usdjpy_test telegram-text --refresh
```

Frontend：

```powershell
npm run usdjpy-strategy-lab
npm run test:usdjpy-strategy-lab
npm test
npm run build
npm run responsive:check
```

Docs：

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 过门标准

- 只允许 USDJPYc 参与策略评分。
- 非 USDJPY 品种不参与 policy。
- 缺运行快照或快通道质量时必须阻断。
- 机会入场只能在核心证据通过时出现。
- 仓位上限可以为 2.0，但推荐仓位必须由评分和模式计算。
- 不出现下单、平仓、撤单或 OrderRequest 写入。


## EA 干跑文件

```text
tools/usdjpy_strategy_lab/QuantGodUSDJPYPolicyDryRun.mq5
```

把它复制到 MT5 的 `MQL5/Experts` 后编译挂载，它只读取 `QuantGod_USDJPYAutoExecutionPolicy.json` 并写出干跑决策，不会调用下单、平仓或改单函数。
