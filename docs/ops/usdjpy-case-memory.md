# USDJPY Case Memory Strategy Candidates

P4-3 turns existing Case Memory into shadow Strategy JSON candidates and GA seed hints. It is a learning and audit step, not a trading executor.

## Flow

```text
Replay / execution feedback / strategy contract shadow / GA blocker
→ Case Memory
→ root cause
→ proposed mutation
→ shadow Strategy JSON candidate
→ GA seed
```

If parity is `PARITY_FAIL`, candidate generation is blocked. The operator must fix Strategy JSON / Python replay / MQL5 EA consistency before the candidate can move into shadow or GA elite review.

## Runtime Outputs

```text
runtime/evidence_os/QuantGod_CaseMemory.jsonl
runtime/evidence_os/QuantGod_CaseMemorySummary.json
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidates.json
runtime/case_memory/QuantGod_CaseMemoryStrategyCandidateLedger.jsonl
```

## CLI

```bash
cd /Users/bowen/Desktop/Quard/QuantGodBackend

python3 tools/run_case_memory.py --runtime-dir ./runtime status
python3 tools/run_case_memory.py --runtime-dir ./runtime build --write
python3 tools/run_case_memory.py --runtime-dir ./runtime telegram-text --refresh
```

For a local smoke test:

```bash
tmp="$(mktemp -d)"
python3 tools/run_case_memory.py --runtime-dir "$tmp" sample --overwrite
python3 tools/run_case_memory.py --runtime-dir "$tmp" build --write
python3 tools/run_case_memory.py --runtime-dir "$tmp" telegram-text --refresh
```

## API

```text
GET  /api/case-memory/status
POST /api/case-memory/build
GET  /api/case-memory/telegram-text
```

The frontend uses `src/services/caseMemoryApi.js` and the Evolution workspace panel. It does not read runtime files directly.

## Safety

- No order send.
- No close.
- No cancel.
- No MT5 live preset mutation.
- No Telegram trading command.
- No Polymarket real-money path.
- Candidates remain `SHADOW_STRATEGY_JSON_CANDIDATE`.
- `PARITY_FAIL` blocks candidate generation and promotion evidence.
