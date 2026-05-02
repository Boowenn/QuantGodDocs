# Docs 可读性完成矩阵

本文件用于把 `QuantGodDocs` 从“文档仓库已初始化”推进到“可读、可检查、可作为四仓库 contract hub 使用”的完成状态。

## 当前阶段门

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| P0 Backend CI guard | 已完成 | Backend 不再检查 Frontend 源码，拆分边界已固定。 |
| P1 Infra workspace test | 已完成 | Workspace test/verify 对 Node/API test 使用硬失败。 |
| P1 Frontend 模块化 | 已完成 | AppShell、workspace、domain parity、Legacy slim、deep-link、统一 API client 已完成。 |
| P1 Frontend API contract guard | 已完成 | Frontend 已禁止直接读取 `/QuantGod_*.json` 和 `/QuantGod_*.csv`。 |
| P2 Docs 可读 Markdown | 本轮完成目标 | 文档必须可读、可链接、可校验，并和 API contract 保持一致。 |

## 完成定义

Docs 可读性阶段只有同时满足以下条件才算完成：

1. 所有核心文档存在，并且不是压缩成一行的 Markdown。
2. `README.md` 能说明四仓库职责、阅读入口、本地检查命令和维护规则。
3. `docs/contracts/api-contract.json` 可解析，endpoint 数量不低于当前 backend route surface。
4. `docs/backend/api-contract.md` 与 contract JSON 同步维护。
5. Phase 1 / Phase 2 / Phase 3 文档分别说明交付物和安全边界。
6. 文档仓库 CI 至少包含链接检查、API contract 检查、Docs quality gate 和单元测试。
7. 文档中不保存 token、API key、账号凭据、Telegram bot token 或 MT5 登录信息。

## 下一阶段门

只有 Docs 可读性阶段完成后，才进入下一个 P2 项：

```text
四仓库补 LICENSE / SECURITY / CONTRIBUTING
```

在此之前，不应改动 license、开源策略、贡献流程或 security policy。
