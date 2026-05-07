# USDJPY Evidence OS

USDJPY Evidence OS is the first Perfect Edition evidence layer. It connects the Strategy JSON backtest, Python replay, MQL5 EA diagnostics, live execution feedback, Case Memory, and a push-only Telegram Gateway into one auditable chain.

It is still a research and audit plane. It does not send orders, close positions, cancel orders, mutate live presets, connect Polymarket real money, or receive Telegram trading commands.

## Evidence Flow

```text
QuantGod_MT5RuntimeSnapshot_USDJPYc.json
→ SQLite K-line ingest
→ Strategy JSON backtest
→ Strategy JSON / Python Replay / MQL5 EA parity
→ Live execution feedback
→ Case Memory
→ GA fitness evidence
→ Telegram Gateway push-only summary
```

## Runtime Outputs

```text
runtime/backtest/usdjpy.sqlite
runtime/backtest/QuantGod_USDJPYKlineIngestReport.json
runtime/backtest/QuantGod_StrategyBacktestReport.json
runtime/evidence_os/QuantGod_StrategyParityReport.json
runtime/evidence_os/QuantGod_LiveExecutionQualityReport.json
runtime/evidence_os/QuantGod_LiveExecutionFeedback.jsonl
runtime/evidence_os/QuantGod_CaseMemory.jsonl
runtime/evidence_os/QuantGod_CaseMemorySummary.json
runtime/evidence_os/QuantGod_USDJPYEvidenceOSStatus.json
runtime/notifications/QuantGod_TelegramGatewayStatus.json
runtime/notifications/QuantGod_TelegramGatewayLedger.jsonl
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime sync-klines
python3 tools/run_usdjpy_strategy_backtest.py --runtime-dir ./runtime run --write
python3 tools/run_usdjpy_evidence_os.py --runtime-dir ./runtime once --write
python3 tools/run_usdjpy_evidence_os.py --runtime-dir ./runtime telegram-text --refresh
```

## Safety

- Focus symbol is `USDJPYc`.
- Strategy JSON is used as an audit contract, not a direct order instruction.
- Telegram Gateway is push-only and records a delivery ledger.
- `QG_TELEGRAM_COMMANDS_ALLOWED=1` is rejected by the gateway sender.
- Parity failures block promotion evidence; they do not place or cancel trades.

