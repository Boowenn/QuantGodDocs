# Phase 2 总结

Phase 2 把 QuantGod 从混合页面和散落数据读取，推进到更清晰的 operator platform。

## Module D：Vue 收尾

已落地方向：

- Vue workbench 成为唯一 active operator frontend。
- 旧 HTML dashboard 由 Backend 策略冻结或重定向。
- Frontend 代码迁移到 `QuantGodFrontend`，Backend 只保留构建产物。
- Ant Design Vue 作为后续统一组件方向，但必须遵守 QuantGod 现有深色工作台视觉。

## Module E：API 统一

已落地范围：

- file facade API。
- `/api/governance/*`
- `/api/paramlab/*`
- `/api/trades/*`
- `/api/research/*`
- `/api/shadow/*`
- `/api/dashboard/*`

Frontend 不再直接读取 JSON/CSV runtime artifacts。所有页面数据必须通过 `/api/*` 和 `src/services/*` 获取。

## Module F：Telegram

已落地方向：

- push-only notification。
- 不接受 command execution。
- 不通过 Telegram 触发交易动作。
- token 与 chat id 只能来自环境变量，不能进入 Git。

## Module G：CI/CD 增强

已落地方向：

- integration tests。
- coverage visibility。
- API contract checks。
- frontend API contract guard。
- split boundary guard。
- PR / branch protection 方向。

## 安全边界

Phase 2 的重点不是新增交易能力，而是把数据面和通知面收口。任何 `/api/*` 统一都不能扩大 order-send、close、cancel、preset mutation 或 credential storage 能力。
