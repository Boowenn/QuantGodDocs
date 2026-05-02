# Phase 2 scope

Phase 2 implemented:

- Module D: Vue migration finish and Ant Design Vue integration.
- Module E: backend API unification.
- Module F: Telegram push-only notification service.
- Module G: CI/CD integration and coverage enhancements.

## API unification

Vue should consume `/api/*`, not direct local JSON/CSV files.

## Telegram

Telegram is push-only. It may send trade/risk/AI/Governance/digest messages but cannot accept commands or trigger trading actions.

## CI

Coverage and integration tests make backend/API regressions visible.
