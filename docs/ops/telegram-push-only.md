# Telegram push-only 设置

P3-2 只做 Telegram push-only 通知关联和测试发送。它不新增 Email、不新增入站 Webhook、不接收 Telegram 交易命令、不接 broker adapter、不保存凭据、不开放 public ingress、不引入用户系统 / billing / credits，也不修改 live preset。

## 安全边界

- Telegram 只做出站推送。
- `QG_TELEGRAM_COMMANDS_ALLOWED` 必须保持 `0`。
- `QG_WEBHOOK_RECEIVER_ALLOWED` 必须保持未设置或 false。
- `QG_EMAIL_DELIVERY_ALLOWED` 必须保持未设置或 false。
- 交易控制继续关闭：order send、close、cancel、live preset mutation、credential storage、Kill Switch override 都不属于 P3-2 范围。
- Docker local 只透传环境变量；token 和 chat ID 不写入 image、compose 文件或 example 文件。

## 为什么桌面 Telegram 登录不够

Telegram Desktop 登录态只能帮我们打开 @BotFather 和 bot 聊天窗口。Bot API 仍然需要 @BotFather 生成的 bot token。本地 linker 也只能在目标聊天主动给 bot 发 `/start` 或频道产生可见更新后发现 `chat_id`。

如果目标是频道 `QuardGod`，需要额外确认 bot 已加入频道并拥有发消息权限。公共频道可以直接使用 `@channel_username` 作为 `QG_TELEGRAM_CHAT_ID`；私有频道通常需要通过 bot 可见的 channel post 或管理员信息拿到负数 chat id。

## Backend 本地设置

在 `QuantGodBackend` 运行：

```powershell
python tools\run_telegram_notifier.py open-botfather
Copy-Item .env.telegram.local.example .env.telegram.local
notepad .env.telegram.local
```

在 @BotFather 创建或复用一个 bot，然后把 token 写入 `.env.telegram.local`：

```text
QG_TELEGRAM_BOT_TOKEN=<token from BotFather>
QG_TELEGRAM_COMMANDS_ALLOWED=0
QG_TELEGRAM_PUSH_ALLOWED=0
```

验证 token：

```powershell
python tools\run_telegram_notifier.py status
python tools\run_telegram_notifier.py get-me
```

发现并写入 private chat ID。命令可以打开 bot 聊天窗口；它轮询时给 bot 发送 `/start`：

```powershell
python tools\run_telegram_notifier.py link --open --poll-seconds 60 --write-env --enable-push
```

发送 push-only 测试消息：

```powershell
python tools\run_telegram_notifier.py test
python tools\run_state_store.py notifications --limit 10
```

## MT5 AI 监听建议推送

`tools/run_mt5_ai_telegram_monitor.py` 提供类似 Web3 监控系统的本地闭环：

```text
MT5 read-only snapshot / runtime ledger
→ AI Analysis V2 多智能体分析
→ 去重与最小间隔
→ Telegram push-only advisory message
→ SQLite notification evidence
```

它只读本地 MT5/QuantGod 证据，不下单、不平仓、不撤单、不修改 live preset，也不会接收 Telegram 命令。默认是 dry-run，只记录 evidence；必须显式加 `--send`，且 `.env.telegram.local` 里 `QG_TELEGRAM_PUSH_ALLOWED=1` 后才会发到 Telegram。

Dry-run 验证：

```powershell
python tools\run_mt5_ai_telegram_monitor.py scan-once `
  --symbols USDJPYc,EURUSDc,XAUUSDc `
  --min-interval-seconds 0
```

真实发送一次 advisory：

```powershell
python tools\run_mt5_ai_telegram_monitor.py scan-once `
  --symbols USDJPYc,EURUSDc,XAUUSDc `
  --send `
  --force
```

本地轮询三次：

```powershell
python tools\run_mt5_ai_telegram_monitor.py loop `
  --symbols USDJPYc,EURUSDc,XAUUSDc `
  --cycles 3 `
  --interval-seconds 60 `
  --send
```

可选默认符号：

```text
QG_MT5_AI_MONITOR_SYMBOLS=USDJPYc,EURUSDc,XAUUSDc
```

如果 `link` 报告 webhook 冲突，只有在这个 bot 是 QuantGod 专用 bot 时才清理 webhook：

```powershell
python tools\run_telegram_notifier.py webhook-info
python tools\run_telegram_notifier.py clear-webhook
python tools\run_telegram_notifier.py link --open --poll-seconds 60 --write-env --enable-push
```

## Docker local 设置

在 `QuantGodInfra` 运行：

```powershell
Copy-Item docker\.env.local.example docker\.env.local
notepad docker\.env.local
```

只在未提交的 `docker\.env.local` 里设置这些 Telegram 值：

```text
QG_TELEGRAM_PUSH_ALLOWED=1
QG_TELEGRAM_COMMANDS_ALLOWED=0
QG_TELEGRAM_BOT_TOKEN=<token from BotFather>
QG_TELEGRAM_CHAT_ID=<Backend CLI 发现的 chat id 或公共频道 @username>
```

Then run:

```powershell
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py config
python scripts\qg-docker-local.py up
```

## 验证

Backend:

```powershell
cd C:\QuantGod\QuantGodBackend
python -m py_compile tools\run_telegram_notifier.py tools\telegram_notifier\config.py tools\telegram_notifier\client.py tools\telegram_notifier\records.py tools\telegram_notifier\safety.py
python -m unittest discover tests -v
node --test tests\node\test_telegram_push_only.mjs
python tools\run_telegram_notifier.py status
```

Infra:

```powershell
cd C:\QuantGod\QuantGodInfra
python -m py_compile scripts\qg-docker-local.py
python -m unittest discover tests -v
python scripts\qg-docker-local.py static-check
python scripts\qg-docker-local.py doctor
```

Docs:

```powershell
cd C:\QuantGod\QuantGodDocs
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 回滚

先删除本地未提交的 secret 文件：

```powershell
Remove-Item C:\QuantGod\QuantGodBackend\.env.telegram.local -ErrorAction SilentlyContinue
Remove-Item C:\QuantGod\QuantGodInfra\docker\.env.local -ErrorAction SilentlyContinue
```

然后回滚 Backend、Infra、Docs 的 P3-2 提交。本次 Telegram-only 范围不应该存在 Frontend 提交。
