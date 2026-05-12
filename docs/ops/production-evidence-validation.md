# P4-6 Production Evidence Validation

P4-6 verifies whether the current QuantGod production evidence is strong enough to trust the autonomous USDJPY workflow.

It validates four evidence areas:

1. USDJPY historical data production status.
2. Strategy JSON / Python / EA parity coverage by strategy family.
3. Live and shadow execution feedback field coverage.
4. GA multi-generation stability evidence.

This stage is read-only. It does not place orders, close positions, cancel orders, mutate live presets, connect Polymarket wallets, or receive Telegram trading commands.

## CLI

```powershell
python tools\run_production_evidence_validation.py --runtime-dir .\runtime build --write
python tools\run_production_evidence_validation.py --runtime-dir .\runtime telegram-text --refresh
```

## API

```text
GET  /api/production-evidence-validation/status
POST /api/production-evidence-validation/run
GET  /api/production-evidence-validation/telegram-text?refresh=1
```

## Outputs

```text
runtime/production_validation/QuantGod_ProductionEvidenceValidationReport.json
runtime/production_validation/QuantGod_StrategyFamilyParityMatrix.json
runtime/production_validation/QuantGod_LiveExecutionFeedbackCoverage.json
runtime/production_validation/QuantGod_GAMultiGenerationStabilityReport.json
```

## Safety

The report is advisory and read-only. Any `PARITY_FAIL` must block promotion. Missing execution feedback should keep candidates in observation until more samples are collected.
