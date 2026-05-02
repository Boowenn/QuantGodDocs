# 模块边界

## Backend 拥有的模块

Backend 拥有所有会接触 MT5 runtime、HFM 本地文件、策略评估、Governance 或 AI evidence 写入的代码。

包括：

- `MQL5/` 下的 MT5 EA 源码和 preset。
- `Dashboard/` 下的 Node API server。
- MT5 read-only bridge 与受控 trading bridge。
- Governance Advisor。
- ParamLab Runner、Auto Scheduler、Report Watcher、Recovery。
- Strategy Version Registry 与 Version Promotion Gate。
- Backend Backtest Loop。
- AI Analysis V1/V2 agents 与 evidence writer。
- Vibe Coding 策略生成、安全校验、registry、backtest connector。
- Telegram push-only notify service。

## Frontend 拥有的模块

Frontend 只拥有视觉工作台和 UI 状态：

- Vue shell。
- Ant Design Vue 页面层。
- KlineCharts 渲染。
- AI/Vibe Coding 面板。
- API service wrappers。
- Monaco editor UI。

Frontend 不得包含 MT5 凭据、broker 凭据、Python 策略执行逻辑或本地 `MQL5/Files` 抓取逻辑。

## Infra 拥有的模块

Infra 负责胶水和部署：

- Cloudflare worker 文件。
- workspace helper。
- Frontend dist 到 Backend 静态目录的同步。
- 多仓库 pull/build/test 命令。
- 可选远程 dashboard 部署自动化。

Infra 不写策略逻辑，不改 Governance，不碰 live preset。

## Docs 拥有的模块

Docs 负责说明、契约、Runbook、Phase 设计和维护规则。以下变化必须同步文档：

- API shape 改动。
- 仓库边界改动。
- operator workflow 改动。
- 安全 gate 改动。
- CI 或发布流程改动。
- Phase 实装状态变化。
