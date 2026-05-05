# P3-9 维护说明：入场触发实验室

## 阶段定位

P3-9 不是交易执行层。它是 P3-6 自适应策略闸门和 P3-7 快通道质量之后的二次确认层。

```text
MT5 runtime / fast lane
→ adaptive policy entry gate
→ shadow outcome score
→ entry trigger lab
→ 中文 Telegram 复核文本
```

## 验收标准

- `python -m unittest discover tests -v` 通过。
- `node --test tests/node/test_entry_trigger_lab_guard.mjs` 通过。
- `telegram-text` 输出中文。
- 代码中不含 MT5 执行函数。
- 输出安全字段中 execution flags 全部为 false。

## 推荐观察指标

- 哪些品种长期处于“暂停触发”。
- 哪些方向经常卡在快通道质量。
- 哪些方向卡在影子样本负期望。
- 通过二次确认后的后续 1h/4h/24h journal 表现。
