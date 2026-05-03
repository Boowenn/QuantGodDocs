# Infra 文档

Infra 负责四仓库联动、workspace 自动化、部署配置和前端构建产物同步。

## 关键入口

- [Workspace 自动化](workspace-automation.md)
- [本地部署](deployment-local.md)

## Infra 维护原则

1. Infra 只编排，不包含交易策略和 Vue 页面实现。
2. Workspace helper 的 `test` 和 `verify` 必须在关键失败时硬失败。
3. 前端 dist 同步必须清晰显示源路径和目标路径。
4. 本地 workspace 配置使用 `.gitignored` local file，example 使用 portable relative path。

## P3-1 Docker/local-dev stack

- [Docker 本地开发栈](docker-local-dev.md)
