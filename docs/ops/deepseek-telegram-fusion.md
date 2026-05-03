# DeepSeek Telegram Fusion

This runbook documents the QuantGod single-user AI advisory fusion layer.

The scope is intentionally narrow:

- MT5/HFM runtime evidence remains the market-data source.
- Local AI Analysis V2 remains the first-pass multi-agent decision engine.
- DeepSeek is used as a Chinese advisory reviewer and report writer.
- A code-level validator converts raw DeepSeek output into safe effective advice.
- Telegram remains push-only.
- SQLite notification evidence remains the delivery audit trail.

This feature does not add broker execution, multi-user accounts, billing, webhook
receivers, Telegram commands, credential storage, live preset mutation, or Kill
Switch override.

## Data flow

```text
HFM/MT5 EA runtime JSON
→ AnalysisServiceV2 local multi-agent report
→ DeepSeekMt5Advisor sanitized payload
→ deepseek_validator.py hard safety validation
→ advisory_fusion.py local-vs-DeepSeek agreement check
→ run_mt5_ai_telegram_monitor.py Telegram report
→ SQLite notification evidence
```

The DeepSeek prompt is still useful, but it is not the enforcement layer.  The
enforcement layer is the local validator.  If DeepSeek returns unsafe execution
language or a directional plan while the runtime evidence is stale/fallback, the
validator downgrades the effective advice to observation-only before Telegram
sees it.

## New Backend files

```text
tools/ai_analysis/deepseek_validator.py
tools/ai_analysis/advisory_fusion.py
tools/run_ai_advisory_fusion.py
tests/test_ai_advisory_fusion.py
tests/node/test_deepseek_telegram_guard.mjs
```

The overlay also patches `tools/run_mt5_ai_telegram_monitor.py` so the existing
MT5 Telegram loop calls the fusion layer after DeepSeek returns.

## Validator rules

The validator forces `HOLD` / observation-only when any of these are true:

```text
snapshot.fallback=true
snapshot.runtimeFresh=false
risk.kill_switch_active=true
DeepSeek output contains execution-like language
local multi-agent action conflicts with DeepSeek direction
DeepSeek is unavailable or returns malformed advice
```

Execution-like language includes direct order instructions, market buy/sell,
open/close/cancel commands, live preset mutation, Kill Switch override, bypassing
risk controls, and leverage escalation.  Explicit safety language such as
"不下单" or "advisory only" is not treated as a violation.

## Fusion output

Every fused report includes:

```json
{
  "schema": "quantgod.ai_advisory_fusion.v1",
  "finalAction": "HOLD",
  "agreement": "local_and_deepseek_compatible",
  "notifySeverity": "INFO",
  "riskOverride": false,
  "evidenceQualityScore": 1.0,
  "deepseek": {
    "provider": "deepseek",
    "model": "deepseek-v4-flash",
    "validationStatus": "pass"
  },
  "safety": {
    "advisoryOnly": true,
    "telegramPushOnly": true,
    "orderSendAllowed": false,
    "closeAllowed": false,
    "cancelAllowed": false,
    "livePresetMutationAllowed": false
  }
}
```

`finalAction` is not an execution command.  It is a Telegram advisory label:

```text
HOLD         observation only
WATCH_LONG   directional review, no execution
WATCH_SHORT  directional review, no execution
```

## CLI smoke test

```powershell
cd C:\QuantGod\QuantGodBackend

python -m py_compile `
  tools\ai_analysis\deepseek_validator.py `
  tools\ai_analysis\advisory_fusion.py `
  tools\run_ai_advisory_fusion.py

python -m unittest discover tests -v
node --test tests\node\test_deepseek_telegram_guard.mjs

python tools\run_ai_advisory_fusion.py config
python tools\run_ai_advisory_fusion.py scan-once `
  --runtime-dir .\runtime `
  --symbols USDJPYc `
  --no-deepseek `
  --delivery-preview
```

When DeepSeek credentials are configured locally:

```powershell
python tools\run_ai_advisory_fusion.py scan-once `
  --runtime-dir .\runtime `
  --symbols USDJPYc `
  --delivery-preview
```

The existing Telegram monitor now uses the same fusion layer:

```powershell
python tools\run_mt5_ai_telegram_monitor.py scan-once `
  --runtime-dir .\runtime `
  --symbols USDJPYc `
  --force
```

To send a real compact fusion smoke message:

```powershell
python tools\run_ai_advisory_fusion.py scan-once `
  --runtime-dir .\runtime `
  --symbols USDJPYc `
  --send
```

The normal production-style report should still use the existing monitor:

```powershell
python tools\run_mt5_ai_telegram_monitor.py scan-once `
  --runtime-dir .\runtime `
  --symbols USDJPYc `
  --force `
  --send
```

## Expected Telegram improvement

The Telegram message keeps the existing Chinese MT5 advisory format, but the
DeepSeek section is now the safe effective advice.  If validation passes, it can
show the DeepSeek report.  If validation fails, it shows a downgrade reason such
as:

```text
validator=downgraded/fallback_snapshot
fusionFinalAction=HOLD
计划状态：暂停，仅允许观察复核
入场区间：不生成，等待新鲜运行快照与程序风控确认
```

## Local secrets

DeepSeek and Telegram secrets stay in local uncommitted files only:

```text
.env.deepseek.local
.env.telegram.local
```

Do not commit API keys, bot tokens, wallet keys, MT5 credentials, account logins,
order tickets, or private runtime files.

## Safety boundary

This feature is advisory-only.  It must never:

- send, close, cancel, or modify orders;
- write live preset mutations;
- store credentials;
- receive Telegram trading commands;
- create webhook receivers;
- override Kill Switch or governance decisions;
- promote DeepSeek text to execution.
