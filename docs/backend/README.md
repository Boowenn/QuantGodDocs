# 后端指南

## 仓库

`Boowenn/QuantGodBackend`

## 主要职责

- MT5 EA、HFM live/shadow/backtest 启动器。
- Node dashboard/API server。
- Governance、ParamLab、research stats、AI analysis、Vibe Coding、notification、bridge contracts 等 Python tools。
- 后端 CI 与 API contract tests。

## 本地命令

```powershell
python -m unittest discover tests -v
python -m pytest tests -q --cov=tools --cov-report=term-missing
node --test tests/node/*.mjs
Dashboard\start_dashboard.bat
```

## Runtime 文件

典型 HFM runtime path：

```text
C:\Program Files\HFM Metatrader 5\MQL5\Files\
```

后端从 HFM Files 读取本地 runtime JSON/CSV，并通过 `/api/*` 提供规范化数据。

## API 分组

- `/api/mt5-readonly/*`
- `/api/mt5-symbol-registry/*`
- `/api/ai-analysis/*`
- `/api/ai-analysis-v2/*`
- `/api/governance/*`
- `/api/paramlab/*`
- `/api/trades/*`
- `/api/research/*`
- `/api/shadow/*`
- `/api/dashboard/*`
- `/api/notify/*`
- `/api/vibe-coding/*`
- `/api/kline/*`

## 后端合并前检查

- 不新增未受控的 live preset mutation。
- API 不保存 broker credentials。
- AI、Vibe、Telegram 路径不能发送 broker orders。
- trading bridge 仍受 dryRun、Kill Switch、authorization locks 保护。
- response shape 改动时同步 API contract tests 和 Docs。
