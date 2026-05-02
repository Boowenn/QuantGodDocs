# QuantGod 安全边界

本文档记录 QuantGod 四仓库拆分后仍必须保持的安全边界。它优先于功能说明、页面文案和临时实验需求。

## 不可突破的边界

1. AI 分析只提供 advisory evidence，不能直接下单、平仓、撤单或修改实盘配置。
2. Vibe Coding 只用于 research-only 策略生成与回测；进入实盘前必须经过 Backtest、ParamLab、Governance、Version Gate 和人工授权。
3. Telegram 只允许 push-only 通知，不接收任何交易命令。
4. Frontend 不得直接读取 `QuantGod_*.json` 或 `QuantGod_*.csv` runtime 文件，必须通过 `/api/*` service layer 获取数据。
5. Backend 的文件 facade API 默认是 read-only；除非 endpoint 明确标记为 push-only 通知或 research-only 生成，否则不得产生运行时写入副作用。
6. Kill Switch、authorization lock、dryRun、news filter、EA 内部 OrderSend guard 始终是实盘交易的最后边界。

## 各功能面禁止行为

| 功能面 | 禁止行为 |
|---|---|
| AI V1 / AI V2 | 发送订单、关闭订单、修改 lot size、修改 live preset、覆盖 Governance 决策。 |
| Vibe Coding | 直接控制 MT5、导入危险 Python 模块、任意读写文件、访问网络、保存凭据。 |
| Telegram | 接收 `/buy`、`/sell`、`/close`、`/disable-kill-switch` 或类似命令。 |
| Frontend | 直接 fetch `/QuantGod_*.json`、直接 fetch `/QuantGod_*.csv`、写本地文件、调用 MT5 trading command。 |
| Infra | 在 build、sync、deploy 过程中修改交易配置、live preset 或授权锁。 |
| Docs | 保存 token、密码、运行时快照、真实账户凭据或可复用交易密钥。 |

## Evidence 与 Execution 的分离

QuantGod 有意把“证据生成”和“交易执行”拆开：

- AI 报告可以成为 Governance evidence。
- Vibe backtest 可以成为 candidate evidence。
- ParamLab 可以生成优化 evidence。
- Governance 可以给出 keep、demote、promote 建议。

这些结果都不能自动绕过人工授权，也不能绕过 EA 安全 gate。任何“自动推到实盘”的能力都必须先落到可审计的候选状态，再经过显式授权链路。
