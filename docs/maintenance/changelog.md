# Changelog

## 2026-05-02

- 将 QuantGod 拆分为 `QuantGodBackend`、`QuantGodFrontend`、`QuantGodInfra`、`QuantGodDocs` 四个仓库。
- 修复 Backend CI guard：拆分后不再检查 frontend 源码，只保留 backend、MQL5、API 与安全边界检查。
- 加固 Infra workspace：联动测试对 backend Node/API contract test 硬失败，并使用 portable workspace 配置。
- 加固 Frontend API contract guard：禁止前端直接读取 runtime JSON/CSV，强制通过 `/api/*` service layer。
- 初始化 Docs contract hub：补齐架构、API contract、runbook、phase 文档和自检脚本。
