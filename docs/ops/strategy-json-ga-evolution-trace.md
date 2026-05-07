# Strategy JSON GA Evolution Trace

QuantGod v2.6 adds an auditable Strategy JSON evolution trace for USDJPY research. The goal is not to let GA trade; the goal is to make every generation, seed, fitness score, blocker, mutation, crossover, and elite decision visible to the operator.

## Scope

This system is USDJPY-only and writes local research evidence under:

```text
runtime/ga/
```

It may create and score Strategy JSON candidates for:

```text
MT5 Shadow Lane
Tester-only validation
Paper-live simulation
Daily Autopilot research tasks
```

It must not affect:

```text
USDJPY Live Lane execution
MT5 OrderSend / CTrade
close / cancel / order modification
live preset mutation
Polymarket real-money wallet
Telegram trade commands
```

## Trace Files

The GA runner writes:

```text
QuantGod_GAStatus.json
QuantGod_GAGenerationLatest.json
QuantGod_GAGenerationLedger.jsonl
QuantGod_GACandidateRuns.jsonl
QuantGod_GAEliteStrategies.json
QuantGod_GABlockerSummary.json
QuantGod_GAEvolutionPath.json
```

Each candidate run records:

```text
generationId
seedId
strategyId
source
replayStatus
walkForwardStatus
fitness
fitnessBreakdown
rank
blockerCode
reasonZh
promotionStage
strategyJson
```

## Strategy JSON Safety

Every seed must validate as `quantgod.strategy.v1`. The validator rejects:

```text
non-USDJPY symbols
live stages such as MICRO_LIVE / LIVE_LIMITED
maxLot above 2.0
OrderSend / CTrade / TRADE_ACTION_DEAL
eval / exec / import / function bodies
privateKey / wallet / Telegram command execution
Polymarket real-money permissions
```

The validator accepts explicit `false` safety fields, for example `orderSendAllowed=false`. Those fields are required as safety declarations and must not be confused with permission grants.

## Fitness

Fitness is not pure profit. It combines:

```text
netR
profitCaptureRatio
missedOpportunityReduction
maxAdverseR penalty
drawdown / instability / overfit penalties
sample-count penalty
trade-frequency penalty
```

Candidates with insufficient evidence remain `NEEDS_MORE_DATA` or `SHADOW`; they are not promoted to live.

## Frontend

The Evolution workspace must show the full process:

```text
generation timeline
candidate table
seed detail drawer
Strategy JSON preview
fitness breakdown
blocker summary
elite / mutation / crossover source
```

The page must make it clear that GA only enters shadow/tester/paper research and cannot directly trade.

## Telegram

The GA Telegram report is Chinese and push-only. It summarizes:

```text
current generation
population size
best seed / best fitness
elite count
blocked candidate count
main blockers
next action
safety boundary
```

Telegram still cannot receive or execute trading commands.

