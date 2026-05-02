# 本地运维 Runbook

## 日常启动

1. 确认 HFM MT5 已登录正确账户。
2. 确认 EA 写入 `MQL5/Files` 的 dashboard snapshot。
3. 启动 `QuantGodBackend` dashboard server。
4. 打开 `/vue/` 工作台。
5. 检查 Evidence Freshness、MT5 连接、daily review、todo、Polymarket 状态。

## 每日复盘

每日复盘应回答三件事：

- 今天为什么入场或没有入场。
- 哪些任务已经完成，哪些需要延后。
- 是否需要代码迭代、策略降级、模拟研究或人工确认。

复盘可以生成建议，但不能自动绕过 live preset、Kill Switch 或授权锁。

## 出现异常时

- 先看 dashboard snapshot 是否新鲜。
- 再看 `MQL5/Logs` 和后端 API envelope。
- 如果是前端展示异常，去 `QuantGodFrontend` 修。
- 如果是证据/API/策略逻辑异常，去 `QuantGodBackend` 修。
- 如果是同步/部署异常，去 `QuantGodInfra` 修。
- 如果是说明或流程不清楚，去 `QuantGodDocs` 修。
