# Changelog

## 2026-05-02

- 完成 QuantGod 四仓库拆分：Backend、Frontend、Infra、Docs。
- Backend 修复拆分后的 CI guard，不再检查 frontend 源码。
- Infra 加固 workspace test/verify，使 backend Node/API contract test 硬失败。
- Frontend 增加 API contract guard，禁止直接读取 `/QuantGod_*.json` 和 `/QuantGod_*.csv`。
- Docs 初始化 contract hub，并修复 Markdown / Python 检查脚本被压成一行的问题。

## Phase 状态

- Phase 1：已验收。
- Phase 2：已验收。
- Phase 3：已实现可用版本，后续继续模块化和状态层建设。
