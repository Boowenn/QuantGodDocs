# P3-7 维护记录：MT5 运行快通道

## 阶段边界

P3-7 是运行证据质量和采集速度升级，不是交易执行升级。它只负责让系统更快判断 MT5 数据是否新鲜，不能改变实盘策略开关，也不能绕过 kill switch、新闻过滤、授权锁或 dry-run 边界。

## 新增能力

- `QuantGodRuntimeFastLane.mq5`：只读 EA exporter，写入心跳、tick、指标、诊断和交易事件证据。
- `tools/run_mt5_fastlane.py`：Backend CLI，生成状态、质量报告和中文 Telegram 文案。
- `tools/mt5_fastlane/*`：读取、校验和评分快通道证据。
- 自适应策略闸门会读取 `quality/QuantGod_MT5FastLaneQuality.json`。如果快通道已启用但品种降级，对应方向会暂停观察建议。

## 验证命令

Backend：

```bash
python -m py_compile \
  tools/run_mt5_fastlane.py \
  tools/mt5_fastlane/schema.py \
  tools/mt5_fastlane/reader.py \
  tools/mt5_fastlane/quality.py

python -m unittest discover tests -v
node --test tests/node/test_mt5_fastlane_guard.mjs
python tools/run_mt5_fastlane.py --runtime-dir ./runtime sample --symbols USDJPYc
python tools/run_mt5_fastlane.py --runtime-dir ./runtime quality --symbols USDJPYc
python tools/run_mt5_fastlane.py --runtime-dir ./runtime telegram-text --symbols USDJPYc
```

Docs：

```bash
python scripts/check_docs_quality_gate.py --root .
python scripts/check_docs_links.py --root .
python scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json --backend ../QuantGodBackend
python -m unittest discover tests -v
```

## 安全检查清单

- `tools/mt5_fastlane/QuantGodRuntimeFastLane.mq5` 不包含交易执行调用。
- Backend safety payload 中所有执行类字段保持 `false`。
- Telegram 文案中文优先。
- 运行证据不包含密码、token、API key、authorization header、private key 或钱包密钥。
- `QG_TickFlushEvery` 必须真正限制 OnTick 写入频率，避免 tick 文件无界膨胀。

## 运维说明

1. 把 EA 文件安装到 MT5 `MQL5/Experts`。
2. 编译并挂载到 chart。
3. 确认 `MQL5/Files` 出现快通道文件。
4. Backend 的 `--runtime-dir` 指向该 Files 目录，或由同步任务镜像到 Backend runtime。
5. 先观察质量报告，不要把快通道当成交易授权。

实盘 MT5 终端不要随意重启。需要重启或挂载新 EA 时，应先确认持仓、新闻隔离窗口、EA 状态和当日风险状态。
