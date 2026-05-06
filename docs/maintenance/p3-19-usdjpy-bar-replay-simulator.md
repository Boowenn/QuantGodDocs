# P3-19 USDJPY Bar/Tick Replay Simulator

## 范围

P3-19 只实现 USDJPYc 因果回放模拟器，比较 `current`、`relaxed_entry_v1` 和 `let_profit_run_v1`。它不接真实交易执行，不修改 EA preset，不让 AI 直接决定交易。

## 已落地能力

- 新增 `tools/usdjpy_bar_replay/*`；
- 新增 `tools/run_usdjpy_bar_replay.py`；
- 新增 `/api/usdjpy-strategy-lab/bar-replay/*` 只读接口；
- Dashboard 的 USDJPY 自学习面板展示因果回放；
- 中文 Telegram 报告说明入场与出场候选；
- 单测和 Node guard 防止后验窗口进入触发逻辑。

## 设计重点

```text
后验窗口只评分，不触发。
硬门禁不放宽。
R 是主口径。
USC 只做账面参考。
所有候选都必须先进入 replay / tester-only / shadow 验证。
```

## 后续

P3-20 才进入 walk-forward 参数选择。P3-19 的结论即使变成 `LIVE_CONFIG_PROPOSAL_ELIGIBLE`，也只能生成审查提案，不能自动应用。

