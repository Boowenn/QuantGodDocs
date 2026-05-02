# MT5 RSI Exit Review 2026-04-28

这是从旧后端仓库导入的历史文档，已整理为中文版本。完整演进细节可通过 Git 历史追溯；当前维护以 `QuantGodDocs/docs/` 下的正式文档为准。

## 文档用途

记录 RSI live 样本、退出保护、sell side 降级和复盘结论。

## 相关入口

- `RSI_Reversal_H1`
- `QuantGod_CloseHistory.csv`

## 当前结论

- 该主题已经纳入四仓库拆分后的维护体系。
- 涉及后端逻辑的内容归 `QuantGodBackend`。
- 涉及界面展示的内容归 `QuantGodFrontend`。
- 涉及部署和同步的内容归 `QuantGodInfra`。
- 涉及长期说明、Runbook、API contract 和安全边界的内容归 `QuantGodDocs`。

## 安全提醒

任何历史文档都不能作为绕过当前安全链路的依据。当前系统仍必须遵守 Kill Switch、authorization lock、dryRun、news/session/cooldown、live preset mutation guard 和人工授权要求。
