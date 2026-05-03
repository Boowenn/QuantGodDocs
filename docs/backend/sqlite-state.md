# P2-3 SQLite 状态层

P2-3 只补本地 SQLite 状态持久化，不进入 Docker、Webhook、broker adapter、用户系统、billing 或 credits。

SQLite 状态层的目标是把已经存在的本地 evidence 做索引，方便 Dashboard 和维护脚本读取状态。它不是交易执行层，也不替代 MT5 runtime JSON/CSV。

## 默认位置

Backend 默认数据库路径：

```text
runtime/quantgod_state.sqlite
```

可通过环境变量或 CLI 参数覆盖：

```text
QG_STATE_DB
python tools/run_state_store.py --db runtime/custom_state.sqlite status
```

## 表

核心表如下：

```text
schema_migrations
qg_events
ai_analysis_runs
vibe_strategies
vibe_backtest_runs
notification_events
api_contract_versions
frontend_dist_releases
state_ingest_runs
```

这些表只保存本地 evidence 的索引、元数据和 JSON payload。它们不保存 broker credential，不发送订单，不修改 live preset，不改变 Governance 结论。

## CLI

初始化 schema：

```powershell
python tools\run_state_store.py init
```

查看状态：

```powershell
python tools\run_state_store.py status
```

导入本地 evidence：

```powershell
python tools\run_state_store.py ingest --sources all
```

按类型查询：

```powershell
python tools\run_state_store.py events --limit 20
python tools\run_state_store.py ai-runs --limit 20
python tools\run_state_store.py vibe-strategies --limit 20
python tools\run_state_store.py notifications --limit 20
```

## HTTP API

HTTP API 只读，不提供 ingest/write endpoint：

```text
GET /api/state
GET /api/state/status
GET /api/state/config
GET /api/state/events
GET /api/state/ai-analysis
GET /api/state/vibe-strategies
GET /api/state/notifications
```

`/api/state/*` 只会调用 CLI 的 status/config/query 命令。写入和导入必须通过本地 CLI 完成。

## 安全默认值

SQLite 状态层固定保持：

```text
localOnly=true
statePersistenceOnly=true
researchOnly=true
advisoryOnly=true
readOnlyDataPlane=true
notificationPushOnly=true
canExecuteTrade=false
orderSendAllowed=false
closeAllowed=false
cancelAllowed=false
credentialStorageAllowed=false
livePresetMutationAllowed=false
canOverrideKillSwitch=false
canMutateGovernanceDecision=false
canPromoteOrDemoteRoute=false
telegramCommandExecutionAllowed=false
fundTransferAllowed=false
withdrawalAllowed=false
```

## 不做的事

P2-3 不做以下内容：

```text
Docker/local-dev stack
Webhook / Email 通知
多市场 broker adapter
用户系统 / billing / credits
交易下单、平仓、撤单
live preset mutation
Kill Switch 或授权锁绕过
Telegram command 执行
```
