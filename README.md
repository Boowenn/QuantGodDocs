# QuantGodDocs

QuantGodDocs 是 QuantGod 四仓库体系的文档中心。它只保存架构、API、运维、Phase 状态、安全边界和维护规则，不承载后端运行代码、前端源码、Cloudflare 部署脚本，也不保存 MT5 账号信息、Telegram token、OpenRouter key 或其他凭据。

## 四仓库职责

| 仓库 | 角色 | 主要内容 | 不应该包含 |
|---|---|---|---|
| `QuantGodBackend` | 后端 / MT5 / API / AI / Governance | `MQL5/`、`Dashboard/`、`tools/`、`tests/`、本地 `/api/*` | Vue 源码、Cloudflare 源码、长篇文档中心 |
| `QuantGodFrontend` | Vue 工作台 | `src/`、`public/`、Vite、Ant Design Vue、KlineCharts、Monaco | `MQL5/`、`Dashboard/`、`tools/`、直接读取 `QuantGod_*.json/csv` |
| `QuantGodInfra` | 联动 / 部署 / 同步 | workspace helper、Cloudflare、dist 同步、批量测试 | 交易代码、Vue 页面、MT5 preset |
| `QuantGodDocs` | 文档 / Contract / Runbook | 架构文档、API contract、Phase 文档、运维指南 | runtime 文件、凭据、交易执行代码 |

## 阅读入口

- [四仓库拆分架构](docs/architecture/repo-split.md)
- [模块边界](docs/architecture/module-boundaries.md)
- [仓库联动 Contract](docs/architecture/linkage-contract.md)
- [后端 API Contract](docs/backend/api-contract.md)
- [后端安全边界](docs/backend/safety-boundaries.md)
- [前端工作台](docs/frontend/workbench.md)
- [前端 API Client 规则](docs/frontend/api-client.md)
- [Infra workspace 自动化](docs/infra/workspace-automation.md)
- [本地运行 Runbook](docs/ops/runbook-local.md)
- [Telegram push-only 通知](docs/ops/telegram-push-only.md)
- [Phase 1](docs/phases/phase1.md)
- [Phase 2](docs/phases/phase2.md)
- [Phase 3](docs/phases/phase3.md)

## Contract 文件

- [API Contract JSON](docs/contracts/api-contract.json)
- [Repo Manifest Schema](docs/contracts/repo-manifest.schema.json)

`docs/contracts/api-contract.json` 是前端、后端、Infra 和文档对齐的轻量 contract。Backend 新增、删除或重命名 `/api/*` endpoint 时，必须同步更新这个文件和 `docs/backend/api-contract.md`。

## 本地检查

```powershell
python scripts/check_docs_links.py --root .
python scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json
python -m unittest discover tests -v
```

如果本地同时 clone 了 `QuantGodBackend`，可以做跨仓库 route 对齐检查：

```powershell
python scripts/check_api_contract_matches_backend.py `
  --contract docs/contracts/api-contract.json `
  --backend ..\QuantGodBackend
```

## 文档维护规则

1. 文档必须使用多行 Markdown，不要把整篇文档压成一行。
2. 文档中的相对链接必须能解析到真实文件。
3. API contract 必须保持 JSON 可解析。
4. 安全边界文档优先级高于功能文档。
5. 任何新功能都不能突破 Kill Switch、授权锁、dryRun、只读数据面和 push-only 通知边界。
6. 如果改动影响前端调用路径，先改 Backend contract，再更新 Docs，最后改 Frontend。

## P3-2.1 MT5 runtime evidence bridge

- [MT5 runtime evidence bridge](docs/ops/mt5-runtime-evidence-bridge.md)

## Ops
- [AI Provider Router](docs/ops/ai-provider-router.md)


- [DeepSeek Telegram Fusion](docs/ops/deepseek-telegram-fusion.md)

## Operations

- [AI advisory outcome journal](docs/ops/ai-advisory-outcome-journal.md)

- [P3-6 自适应策略引擎](docs/ops/adaptive-policy-engine.md) — MT5 运行质量、路线评分、入场闸门和动态止损止盈建议。
- [MT5 运行快通道](docs/ops/mt5-runtime-fast-lane.md) — 只读 EA 证据导出器和运行质量监控。
- [P3-8 动态止盈止损校准](docs/ops/dynamic-sltp-calibration.md) — 根据影子 MFE/MAE 证据生成只读动态止损止盈建议。

- [P3-9 入场触发实验室](docs/ops/entry-trigger-lab.md)
- [P3-11 自动执行策略调参器](docs/ops/auto-execution-policy-tuner.md) — 在核心安全不变的前提下，把入场分为标准入场、机会入场和阻断。

## P3-10 Pilot Safety Lock

- [P3-10 实盘试点安全锁](docs/ops/pilot-safety-lock.md)
- [P3-12 自动化链路运行器](docs/ops/automation-chain-runner.md)
- [前端响应式运营台加固](docs/frontend/responsive-operator-hardening.md)
- [P3-14 USDJPY 单品种多策略实验室](docs/ops/usdjpy-strategy-policy-lab.md)
- [USDJPY 实盘闭环与每日自动复盘](docs/ops/usdjpy-live-loop-daily-autopilot.md)
- [USDJPY 自学习闭环](docs/ops/usdjpy-runtime-evolution-core.md)
- [P3-19 USDJPY 因果回放模拟器](docs/ops/usdjpy-bar-replay-simulator.md)
- [USDJPY 自主治理 Agent](docs/ops/usdjpy-autonomous-agent.md)
- [P3-18 USDJPY 回放精度加固](docs/maintenance/p3-18-replay-fidelity-hardening.md)
- [P3-19 USDJPY bar/tick 回放模拟器](docs/maintenance/p3-19-usdjpy-bar-replay-simulator.md)
- [P3-20 自主 Walk-forward 晋级门](docs/maintenance/p3-20-autonomous-walk-forward-promotion-gate.md)
- [QuantGod v2.5 三车道自主 Agent](docs/ops/usdjpy-cent-autonomous-multilane-agent.md)
- [P3-21 三车道自主生命周期](docs/maintenance/p3-21-usdjpy-cent-autonomous-multilane-agent.md)
- [USDJPY EA 策略工厂](docs/phases/usdjpy-ea-strategy-factory.md)
- [USDJPY 策略实验室 API](docs/backend/usdjpy-strategy-lab-api.md)
- [USDJPY EA 实验室 Runbook](docs/ops/usdjpy-ea-lab-runbook.md)
