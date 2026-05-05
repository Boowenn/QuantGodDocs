# P3-9 入场触发实验室

P3-9 用来把“setup 通过”再细分成“是否等待二次确认”。

它只读取本地 MT5 runtime、自适应策略闸门、快通道质量和影子样本，不会下单、不会平仓、不会撤单、不会修改 live preset。

## 目标

- 运行快照必须新鲜。
- MT5 快通道质量必须通过。
- P3-6 自适应入场闸门必须通过。
- 影子样本不能显示明显负期望。
- 通过后也只输出“等待 M1/M5 二次确认”，不会变成交易执行。

## CLI

```powershell
python tools\run_entry_trigger_lab.py --runtime-dir .\runtime status

python tools\run_entry_trigger_lab.py --runtime-dir .\runtime build `
  --symbols USDJPYc,EURUSDc,XAUUSDc

python tools\run_entry_trigger_lab.py --runtime-dir .\runtime plan --symbol USDJPYc

python tools\run_entry_trigger_lab.py --runtime-dir .\runtime telegram-text --symbol USDJPYc
```

## 输出文件

```text
runtime/adaptive/QuantGod_EntryTriggerPlan.json
```

## 安全边界

禁止 OrderSend / OrderModify / PositionClose、live preset mutation、OrderRequest 写入、Telegram 命令接收、broker execution 和 credential storage。
