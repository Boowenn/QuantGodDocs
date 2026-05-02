# QuantGodDocs

QuantGod 四仓库工作区的中文文档中心。这里是架构、API、运维、Phase 状态、安全边界和维护规则的唯一主文档仓库。

代码仓库：

- Backend：<https://github.com/Boowenn/QuantGodBackend>
- Frontend：<https://github.com/Boowenn/QuantGodFrontend>
- Infra：<https://github.com/Boowenn/QuantGodInfra>
- Docs：<https://github.com/Boowenn/QuantGodDocs>

## 推荐阅读顺序

1. [仓库拆分架构](docs/architecture/repo-split.md)
2. [模块边界](docs/architecture/module-boundaries.md)
3. [跨仓库联动契约](docs/architecture/linkage-contract.md)
4. [后端指南](docs/backend/README.md)
5. [前端指南](docs/frontend/README.md)
6. [基础设施指南](docs/infra/README.md)
7. [本地运维 Runbook](docs/ops/runbook-local.md)

## Phase 文档

- [Phase 1：AI 分析与 K 线基础](docs/phases/phase1.md)
- [Phase 2：统一 API 与通知](docs/phases/phase2.md)
- [Phase 3：策略工坊与 AI V2](docs/phases/phase3.md)

## 文档归属

详细说明统一写在本仓库。代码仓库只保留短 README 和指向本仓库的入口，避免同一套规则散落多份、越写越不一致。

## 写作规范

正文以中文为主；API path、命令、文件名、字段名、class/function 名称保持原文。涉及交易安全、凭据、live preset、Kill Switch、Telegram、Vibe Coding 的文档必须明确只读或受控边界。
