# 后端安全边界

## 不可妥协规则

1. AI Analysis 只做 advisory evidence。
2. Vibe Coding 生成策略只允许 research/backtest-only，进入实盘必须走完整链路。
3. Telegram 只允许 push-only 通知，不能接受交易命令。
4. Frontend 不能直接写 runtime 文件，也不能触发 order-send。
5. Kill Switch、authorization lock、dryRun、live preset mutation guard 不得被绕过。

## 允许的自动化

- 读取 runtime JSON/CSV。
- 汇总 daily review、todo、backtest evidence。
- 生成研究建议和人工复核项。
- 写入 advisory evidence 文件。
- dry-run 或 tester-only 的本地研究流程。

## 禁止的自动化

- 自动下单、平仓、撤单。
- 自动修改 live preset。
- 自动关闭 Kill Switch。
- 自动解除 cooldown 或 news block。
- 自动保存 broker credentials。
- 通过 Telegram 或前端绕过人工授权。

## live route 升级链路

任何策略从候选/模拟进入实盘前，必须至少经过：

```text
backtest evidence → ParamLab → Governance Advisor → Version Gate → manual authorization
```

这条链路只能被加强，不能被缩短。
