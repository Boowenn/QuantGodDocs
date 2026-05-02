# 贡献与维护指南

本文档用于判断改动应该进入哪个仓库，以及提交前必须检查哪些安全边界。

## 改动归属

| 改动类型 | 仓库 |
|---|---|
| MQL5、Python tools、Dashboard API route、AI / Governance / ParamLab | `QuantGodBackend` |
| Vue component、service wrapper、UI state、KlineCharts、Ant Design Vue、Monaco | `QuantGodFrontend` |
| workspace script、Cloudflare、dist sync、部署与联动测试 | `QuantGodInfra` |
| 架构说明、API contract、runbook、phase 状态、安全边界文档 | `QuantGodDocs` |

## API 改动 Checklist

1. Backend 先新增或调整 route，并补测试。
2. Docs 更新 `docs/contracts/api-contract.json` 和相关 Markdown。
3. Frontend 通过 `src/services/*` 消费新 endpoint，不直接读 runtime 文件。
4. 如果联动方式变化，再更新 Infra workspace test / verify。

## 安全复核 Checklist

提交前必须确认：

- 是否新增了 order-send 能力？
- 是否新增了 close / cancel 能力？
- 是否修改 live preset？
- 是否保存或打印凭据？
- 是否让 Telegram 能接收命令？
- 是否绕过 Kill Switch、authorization lock 或 dryRun？
- 是否让 Frontend 直接读取 `QuantGod_*.json` 或 `QuantGod_*.csv`？

如果任何答案是“是”，这不是普通功能改动，必须重新设计或进入显式人工安全评审。

## 文档要求

- Docs 仓库正文默认中文，必要技术字段保留英文。
- 文档必须是多行 Markdown，避免整篇压成一行。
- 任何相对链接必须能在仓库内解析。
- Contract JSON 必须能被 CI 校验脚本解析。
