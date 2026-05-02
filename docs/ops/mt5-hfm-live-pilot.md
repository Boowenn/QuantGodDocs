# MT5 / HFM Live Pilot 运维

QuantGod 的 MT5/HFM live pilot 应保持小资金、强约束和人工授权优先。

## 运行原则

- live lot size 必须保持低风险。
- Pilot route 不能绕过 EA 内部 guard。
- Kill Switch 状态必须在 Dashboard 中可见。
- Governance、ParamLab、Version Gate 的状态必须作为 live route 前置条件。

## 不允许

- AI 直接发单。
- Vibe Coding 策略直接进入 live preset。
- Telegram 指令触发交易。
- Frontend 直接写入 MT5 runtime 文件。

## 日常检查

```powershell
cd C:\QuantGod\QuantGodBackend
python tools\ci_guard.py
python tools\run_ai_analysis.py latest
python tools\run_ai_analysis_v2.py latest
python tools\run_notify.py history --limit 20
```
