# P4-4 GA Factory Productionization

Date: 2026-05-12

## Summary

P4-4 turns GA trace output into a factory layer that can be monitored and audited every day. It is the bridge between P4-3 Case Memory candidates and future GA factory operation.

## Productionized Artifacts

The new factory layer separates four responsibilities:

```text
Factory State      -> current production status and next generation action
Elite Archive      -> seeds worth reusing for mutation / crossover
Strategy Graveyard -> blocked seeds and blocker reasons to avoid repeating
Lineage Tree       -> parent, mutation, crossover, and Case Memory origin
```

## Frontend Impact

The Evolution workspace now has a GA Factory panel showing:

- candidates;
- elite archive;
- strategy graveyard;
- lineage nodes;
- next generation production status;
- allowed promotion stages.

## API Surface

```text
GET  /api/strategy-ga-factory/status
POST /api/strategy-ga-factory/build
GET  /api/strategy-ga-factory/telegram-text

GET  /api/ga-factory/status
POST /api/ga-factory/build
GET  /api/ga-factory/telegram-text
```

## Next Step

After P4-4, the next useful step is P4-5 Telegram Gateway Management / Observability:

```text
queue health
dedupe state
rate limit state
delivery ledger
topic-level delivery history
operator-visible failure reasons
```

P4-5 should remain push-only. It should not add Telegram trade commands.
