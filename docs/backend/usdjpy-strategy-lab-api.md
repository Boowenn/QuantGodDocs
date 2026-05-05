# USDJPY 策略实验室 API

`/api/usdjpy-strategy-lab/*` 是 USDJPY 单品种策略工厂的数据面。它只读或生成本地研究证据，不执行交易。

## 主要端点

| 端点 | 说明 |
|---|---|
| `GET /api/usdjpy-strategy-lab/status` | 当前 USDJPY 策略政策状态 |
| `POST /api/usdjpy-strategy-lab/run` | 重新生成策略政策 |
| `GET /api/usdjpy-strategy-lab/catalog` | 三条新增 shadow 策略目录 |
| `GET /api/usdjpy-strategy-lab/signals` | 最近 shadow 候选信号 |
| `POST /api/usdjpy-strategy-lab/signals/run` | 刷新候选信号 |
| `GET /api/usdjpy-strategy-lab/backtest-plan` | 新策略回测计划 |
| `POST /api/usdjpy-strategy-lab/backtest-plan/build` | 重新生成回测计划 |
| `GET /api/usdjpy-strategy-lab/imported-backtests` | 已导入的 USDJPY 回测结果 |
| `POST /api/usdjpy-strategy-lab/import-backtest` | 导入本机 CSV/JSON 回测结果，只写研究证据 |
| `GET /api/usdjpy-strategy-lab/risk-check` | 运行快照、快通道、新闻和隔离状态检查 |
| `GET /api/usdjpy-strategy-lab/evidence` | 策略评分与候选信号合并视图 |
| `GET /api/usdjpy-strategy-lab/candidate-policy` | 候选策略政策 |
| `POST /api/usdjpy-strategy-lab/candidate-policy/build` | 生成候选策略政策 |

## 返回原则

返回内容必须中文优先，并明确显示：

- 新策略是否 shadow-only
- 是否允许真实下单
- 当前候选信号来自哪条路线
- 缺少哪些证据
- 下一步是回测、等待采样还是治理复核

## 禁止事项

这些端点不得：

- 下单
- 平仓
- 撤单
- 修改订单
- 修改 live preset
- 接收 Telegram 交易命令
- 写入凭据

新增策略想进入实盘，必须另走人工试点复核流程。
