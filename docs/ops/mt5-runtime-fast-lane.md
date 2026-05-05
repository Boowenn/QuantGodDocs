# MT5 运行快通道

P3-7 增加一个只读的 MT5 运行证据快通道。它的目的不是交易，而是让 Backend 更快知道“现在 MT5 现场数据是否新鲜、指标是否可用、点差是否异常、交易事件是否同步”。

## 目标

现有每日复盘、自适应策略和 Telegram 建议已经能读历史 ledger，但它们仍然依赖运行证据质量。如果证据陈旧，系统很容易把“数据没同步”误判成“策略没效果”。快通道把 MT5 端的短周期证据写成本地文件，Backend 再生成质量报告，后续自适应策略会把快通道降级作为暂停观察建议的原因之一。

## 允许做什么

- 写入 MT5 心跳证据。
- 按品种追加 tick JSONL。
- 按品种写入 ATR、ADX、布林带宽和 K 线进度。
- 记录策略诊断事件。
- 记录脱敏后的交易事件。
- 生成 Backend 质量报告。
- 生成中文 Telegram 摘要。

## 禁止做什么

- 下单。
- 平仓。
- 撤单。
- 改单。
- 修改 live preset。
- 保存密码、token、API key、私钥或钱包密钥。
- 接收 Telegram 命令。
- 暴露 webhook receiver。
- 接入 broker execution。

## EA 写出的文件

EA 挂载后会写入当前 MT5 的 `MQL5/Files`：

```text
QuantGod_RuntimeHeartbeat.json
QuantGod_RuntimeTicks_USDJPYc.jsonl
QuantGod_RuntimeIndicators_USDJPYc.json
QuantGod_RuntimeStrategyDiagnostics.jsonl
QuantGod_RuntimeTradeEvents.jsonl
```

这些文件只是运行证据，不是策略命令，也不是订单请求。

## Backend 命令

```bash
python tools/run_mt5_fastlane.py --runtime-dir ./runtime sample --symbols USDJPYc
python tools/run_mt5_fastlane.py --runtime-dir ./runtime status --symbols USDJPYc
python tools/run_mt5_fastlane.py --runtime-dir ./runtime quality --symbols USDJPYc
python tools/run_mt5_fastlane.py --runtime-dir ./runtime telegram-text --symbols USDJPYc
```

真实运行时，`--runtime-dir` 应该指向 HFM MT5 的 `MQL5/Files`，或者指向同步后的 Backend `runtime`。

## 质量闸门

质量报告会检查：

- 心跳是否新鲜。
- 最新 tick 是否新鲜。
- 最新指标是否新鲜。
- tick 样本数是否足够。
- 点差是否过宽。
- 安全字段是否仍然是只读。

如果快通道质量降级，自适应策略闸门会把对应品种标为“暂停该方向建议”，避免用陈旧数据生成看起来很确定的建议。

## Telegram 摘要

快通道摘要使用中文，例如：

```text
【QuantGod MT5 快通道质量审查】
心跳：新鲜；年龄：1秒
品种质量：
- USDJPYc｜状态：快速｜tick年龄：1秒｜指标年龄：1秒｜点差：2点
安全边界：
仅采集运行证据；不会下单、不会平仓、不会撤单、不会修改实盘 preset。
```

## 安装步骤

1. 把 `tools/mt5_fastlane/QuantGodRuntimeFastLane.mq5` 放到 MT5 的 `MQL5/Experts`。
2. 用 MetaEditor 编译。
3. 挂到任意 chart。
4. 输入品种列表，例如 `USDJPYc,EURUSDc,XAUUSDc`。
5. 确认 `MQL5/Files` 中出现心跳、tick 和指标文件。
6. 用 Backend CLI 读取该目录并生成质量报告。

不要为了挂载快通道贸然重启实盘 MT5。最好在维护窗口处理，并确认当前持仓、新闻窗口和 EA 状态。
