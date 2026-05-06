# P3-17 维护记录：USDJPY 自学习闭环

P3-17 把 USDJPY-only 主线从“状态解释”推进到“每日自学习证据”。本阶段新增运行数据集、回放复盘、参数候选和实盘配置提案。

## 设计目标

- 只处理 `USDJPYc`；
- 自动整理 EA 守门、阻断、入场、出场和模拟结果；
- 自动找出错失机会和过早出场；
- 生成 tester-only 参数候选；
- 生成需要自主治理门评估的 live config proposal；
- 接入 Daily Autopilot 和 Daily Review；
- 前端只做只读展示。

## 后端入口

```text
tools/run_usdjpy_runtime_dataset.py
tools/usdjpy_runtime_dataset/
```

新增 API：

```text
GET  /api/usdjpy-strategy-lab/evolution/status
POST /api/usdjpy-strategy-lab/evolution/build
GET  /api/usdjpy-strategy-lab/evolution/replay
POST /api/usdjpy-strategy-lab/evolution/replay
GET  /api/usdjpy-strategy-lab/evolution/tune
POST /api/usdjpy-strategy-lab/evolution/tune
GET  /api/usdjpy-strategy-lab/evolution/proposal
POST /api/usdjpy-strategy-lab/evolution/proposal
GET  /api/usdjpy-strategy-lab/evolution/telegram-text
```

## 自动化接入

`run_daily_autopilot.py` 现在会连续运行：

```text
USDJPY runtime dataset
USDJPY replay report
USDJPY parameter tuning
USDJPY live config proposal
```

`build_daily_review.py` 会读取这些结果。如果已经有 fresh 参数候选或配置提案，不再继续把同一事项显示成未处理待办。

## 安全边界

P3-17 不会：

- 下单；
- 平仓；
- 撤单；
- 修改订单；
- 修改 MT5 live preset；
- 接收 Telegram 交易命令；
- 自动应用参数提案。

P3-20 之后，配置提案不再等待人工审批，而是进入自主治理门；Agent 只允许写受控 patch，不允许改源码、live preset 或发单。
