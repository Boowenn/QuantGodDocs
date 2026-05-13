# P4-8B Execution Feedback Sampling Coverage

P4-8B strengthens Production Evidence Validation by turning execution feedback from a coarse "sample insufficient" warning into a quantified coverage report.

It remains part of the existing Production Evidence endpoint family:

```text
GET  /api/production-evidence-validation/status
POST /api/production-evidence-validation/run
GET  /api/production-evidence-validation/telegram-text?refresh=1
```

No separate truth source is introduced.

## Coverage Fields

The audit measures these required fields:

```text
strategyId
eventType
expectedPrice
fillPrice
slippagePips
latencyMs
spreadAtEntry
profitR
mfeR
maeR
```

It also tracks core fields:

```text
strategyId
eventType
profitR
mfeR
maeR
```

## Output

The coverage is embedded in:

```text
runtime/production_validation/QuantGod_ProductionEvidenceValidationReport.json
runtime/production_validation/QuantGod_LiveExecutionFeedbackCoverage.json
```

Important fields:

```text
sampleCount
completeSamples
coreCompleteSamples
fieldCoverage
coreCoverage
coverageGrade
evidenceUsability
missingFieldCounts
modeCounts
eventTypeCounts
strategyCoverage
numericSummary
recommendationsZh
```

## Interpretation

```text
NO_SAMPLES          No usable execution feedback yet.
CORE_FIELD_GAPS     Required R / event / strategy fields are missing.
FIELD_GAPS          Optional production fields are incomplete.
USABLE_BUT_THIN     Fields are usable, but sample count is still thin.
PRODUCTION_READY    Enough samples and field coverage for production observation.
```

## Safety

This audit is read-only. It does not place orders, close positions, cancel orders, mutate live presets, connect wallets, or receive Telegram trading commands.
