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

### MT5 全中文报告格式

MT5 智能推送采用全中文报告式结构，避免只发一行日志，也避免在用户侧暴露 `HOLD`、`Bid`、`Kill Switch`、`live preset` 这类半英文状态。符号名和产品名例如 `USDJPYc`、`MT5` 保持原样，其他说明尽量中文化。

```text
【QuantGod MT5 智能监控报告】
品种、方向、信号等级、置信度、一句话结论

【一、报告信息】
触发原因、报告时间、观察周期、证据质量

【二、行情与账户快照】
买价、卖价、最新价、点差、数据来源、证据状态、证据年龄、当前持仓、熔断状态

【三、盘面结构】
15分钟、1小时、4小时、日线趋势、均线信号、相对强弱、关键压力、关键支撑

【四、智能综合评分】
综合方向、技术方向、风险等级、多头强度、空头强度、新闻风险、情绪仓位

【五、多空推演】
多头剧本、空头剧本、关键因子

【六、交易计划】
建议方向、入场区间、目标一、目标二、目标三、防守位置、盈亏比、仓位上限、失效条件、模型说明

【七、风险明细】
本地风险因子与阻断原因

【八、执行与风控边界】
执行状态、消息系统边界、系统不会下单/平仓/撤单/修改实盘参数/解除熔断/放宽风控门禁
```

这条消息可以给出交易建议，但建议只作为观察证据。实际是否入场仍由程序、交易时段、新闻过滤、点差、风控门禁、熔断、治理规则和实盘参数共同决定。

### DeepSeek 分析层

MT5 Telegram 报告可以接入 DeepSeek 做中文研判。配置只放在本地未提交文件：

```text
.env.deepseek.local
```

推荐 MT5 报告使用轻量模型：

```text
QG_MT5_AI_DEEPSEEK_ENABLED=1
QG_MT5_AI_DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com/anthropic
DEEPSEEK_API_KEY=<本机密钥>
```

如果 DeepSeek 可用，Telegram 会显示“分析来源：DeepSeek 大模型研判”，并使用 DeepSeek 返回的中文结论、计划、目标、防守、风险备注。发送给 DeepSeek 的 payload 只包含脱敏行情、技术、风险、新闻、情绪和本地多空摘要；不包含账号密码、订单 ticket、token、授权文件或任何实盘参数修改指令。

如果 DeepSeek 不可用，报告会明确显示“本地兜底研判”，不会伪装成大模型分析。

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

## MT5 runtime evidence bridge

P3-2.1 adds a read-only runtime evidence bridge so Telegram advisory messages can use HFM/MT5 EA-written JSON snapshots instead of `mt5_python_unavailable` fallback data. See [MT5 runtime evidence bridge](mt5-runtime-evidence-bridge.md).
