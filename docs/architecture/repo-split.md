# QuantGod 仓库拆分架构

## 目标

QuantGod 原来是一个混合仓库：后端、前端、Cloudflare、文档、MQL5、Python tools、Vue source 和部署说明都放在一起。现在拆成四个仓库，是为了让每次变更更小、更可审查，也避免“改一个页面却带出后端和文档大面积变化”。

## 四个仓库

| 仓库 | 职责 | 应包含 | 不应包含 |
|---|---|---|---|
| `QuantGodBackend` | 交易/研究后端 | `MQL5/`、`Dashboard/`、`tools/`、`tests/`、本地启动脚本 | Vue source、Cloudflare worker、完整文档树 |
| `QuantGodFrontend` | operator UI | Vue source、Vite、UI 组件、前端 CI | MQL5、Python tools、后端 runtime JSON/CSV |
| `QuantGodInfra` | 工作区和部署自动化 | Cloudflare、multi-repo scripts、dist sync、部署 helper | 策略逻辑、Vue 组件、业务后端逻辑 |
| `QuantGodDocs` | 中文文档中心 | 架构、API、Runbook、Phase、维护规范 | runtime 数据、凭据、生成 ledger |

## 拆分原因

后端变更通常影响 MT5 安全、数据契约、Governance、ParamLab、AI agents 和测试。前端变更通常影响布局、图表、表格、工作台体验和响应式。Infra 变更影响部署、Cloudflare、workspace orchestration。Docs 变更应该可以独立完成，不必跟代码一起搅在一个提交里。

## 联动方式

1. Backend 暴露本地 REST API：`/api/*`。
2. Frontend 不直接读本地 JSON/CSV，只调用 backend API。
3. Frontend 构建到 `dist/`。
4. Infra 把 `QuantGodFrontend/dist` 同步到 `QuantGodBackend/Dashboard/vue-dist`。
5. Backend 继续通过 `http://localhost:8080/vue/` 提供本地工作台。
6. Docs 记录 API、架构、安全边界、Phase 状态和运维步骤。

## 默认本地拓扑

```text
MT5/HFM terminal
  ↓ 写入 MQL5/Files 下的 JSON/CSV
QuantGodBackend
  ↓ http://127.0.0.1:8080/api/*
QuantGodFrontend dev server 或 backend-served dist
  ↓
Operator browser
```

## 不可破坏的安全边界

- AI Analysis 只做 advisory evidence。
- Telegram 只允许 push-only 通知。
- Vibe Coding 只允许 research/backtest-only。
- Governance 与 Version Gate 不能被前端或通知系统绕过。
- Kill Switch、authorization lock、dryRun、live preset mutation guard、broker credential boundary 保持不变。
