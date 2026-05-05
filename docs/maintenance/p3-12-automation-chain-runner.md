# P3-12 维护记录：自动化链路运行器

## 目标

把 P3-7、P3-6、P3-8、P3-9、P3-11 串成固定顺序的本地自动化链路，让 runtime 证据连续产出，并让 Telegram / Dashboard 能直接显示阻断原因和机会入场状态。

## 阶段门

完成后应满足：

- `python tools/run_automation_chain.py once` 能顺序运行链路；
- `runtime/automation/QuantGod_AutomationChainLatest.json` 会写出最新状态；
- 缺证据时 fail-closed，不会误显示机会入场；
- Telegram 文案是中文；
- Dashboard 可以显示缺证据、阻断原因、机会入场；
- 不触碰真实交易执行。

## 验证命令

Backend：

```powershell
python -m py_compile tools\run_automation_chain.py tools\automation_chain\schema.py tools\automation_chain\runner.py tools\automation_chain\telegram_text.py
python -m unittest discover tests -v
node --test tests\node\test_automation_chain_guard.mjs
python tools\run_automation_chain.py --runtime-dir .\runtime status
python tools\run_automation_chain.py --runtime-dir .\runtime once
python tools\run_automation_chain.py --runtime-dir .\runtime telegram-text --refresh
```

Frontend：

```powershell
npm run automation-chain
npm run test:automation-chain
npm test
npm run build
```

Docs：

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 禁止范围

- 不新增下单 API；
- 不新增平仓/撤单/改单；
- 不写 MT5 OrderRequest；
- 不修改 live preset；
- 不接收 Telegram 交易命令；
- 不接 webhook 执行入口；
- 不存储凭据。
