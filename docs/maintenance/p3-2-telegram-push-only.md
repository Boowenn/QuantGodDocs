# P3-2 Telegram push-only 维护记录

## 范围

本阶段只实现 Telegram push-only 通知关联和测试发送。

包含：

- Backend 本地 Telegram notifier CLI。
- 只使用标准库实现的 Bot API client。
- 默认关闭 push 的 `.env.telegram.local.example`。
- 阻止 Telegram command mode 和 webhook receiver mode 的安全 guard。
- 通过 P2-3 state layer 可选写入 SQLite notification evidence。
- Infra Docker local 对 Telegram token 和 chat ID 只做环境变量透传。
- Docs 中新增本地关联 runbook。

不包含：

- Email delivery。
- 入站 webhook receiver。
- Telegram command parsing 或 command execution。
- Broker adapter。
- Credential storage。
- Public ingress。
- 用户系统、billing 或 credits。

## 预期仓库改动

Backend:

```text
.env.telegram.local.example
Dockerfile.local
tools/run_telegram_notifier.py
tools/telegram_notifier/__init__.py
tools/telegram_notifier/config.py
tools/telegram_notifier/client.py
tools/telegram_notifier/records.py
tools/telegram_notifier/safety.py
tests/test_telegram_notifier.py
tests/node/test_telegram_push_only.mjs
```

Infra:

```text
docker/compose.local.yml
docker/.env.local.example
scripts/qg-docker-local.py
tests/test_docker_local.py
```

Docs:

```text
docs/ops/telegram-push-only.md
docs/maintenance/p3-2-telegram-push-only.md
README.md
```

Frontend:

```text
无预期改动。
```

## 验收检查

Backend:

```powershell
python -m py_compile tools\run_telegram_notifier.py tools\telegram_notifier\config.py tools\telegram_notifier\client.py tools\telegram_notifier\records.py tools\telegram_notifier\safety.py
python -m unittest discover tests -v
node --test tests\node\test_telegram_push_only.mjs
python tools\run_telegram_notifier.py status
```

Infra:

```powershell
python -m py_compile scripts\qg-docker-local.py
python -m unittest discover tests -v
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py doctor
```

Docs:

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 安全不变量

- `QG_TELEGRAM_PUSH_ALLOWED` defaults to `0`.
- `QG_TELEGRAM_COMMANDS_ALLOWED` is forced to `0`.
- Bot token 和 chat ID 只作为本地环境变量透传。
- CLI 可以调用 `getMe`、`getUpdates`、`deleteWebhook` 和 `sendMessage`。
- CLI 不得调用 `setWebhook`。
- CLI 不得暴露 HTTP server。
- CLI 不得解析 `/buy`、`/sell`、`/close`、`/cancel` 或任何类似交易命令。

## 操作备注

个人 Telegram Desktop 关联时，按下面顺序使用 Backend CLI：

```powershell
python tools\run_telegram_notifier.py open-botfather
python tools\run_telegram_notifier.py get-me
python tools\run_telegram_notifier.py link --open --poll-seconds 60 --write-env --enable-push
python tools\run_telegram_notifier.py test
```

如果同一个 bot 已经设置 webhook，基于 `getUpdates` 的本地关联会失败。只有这个 bot 是 QuantGod 专用 bot 时，才允许清理 webhook。

如果目标是频道 `QuardGod`，还需要把 bot 加入频道并授予发消息权限。公共频道可优先使用 `@channel_username`；私有频道需要让 bot 能看到频道更新或由管理员提供 channel id。
