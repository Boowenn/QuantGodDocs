# P3-4 Maintenance: AI Provider Router

## Gate definition

P3-4 adds a shared local AI provider router for the single-user QuantGod workflow.

```text
MT5/HFM runtime evidence
+ local AI Analysis V2
+ DeepSeek Telegram fusion
+ shared AI provider config/health layer
```

This gate does not introduce multi-user accounts, billing, broker execution, Telegram commands, webhook receivers, or credential storage.

## Files owned by this gate

Backend:

```text
.env.ai.local.example
tools/ai_analysis/providers/__init__.py
tools/ai_analysis/providers/base.py
tools/ai_analysis/providers/deepseek_provider.py
tools/ai_analysis/providers/mock_provider.py
tools/ai_analysis/providers/openrouter_provider.py
tools/ai_analysis/providers/router.py
tools/run_ai_provider.py
tests/test_ai_provider_router.py
tests/node/test_ai_provider_router_guard.mjs
.gitignore # patched only to allow the example file while ignoring local env
```

Docs:

```text
docs/ops/ai-provider-router.md
docs/maintenance/p3-4-ai-provider-router.md
README.md # link only
```

## Acceptance criteria

Backend:

```powershell
python -m py_compile tools\run_ai_provider.py tools\ai_analysis\providers\base.py tools\ai_analysis\providers\deepseek_provider.py tools\ai_analysis\providers\mock_provider.py tools\ai_analysis\providers\openrouter_provider.py tools\ai_analysis\providers\router.py
python -m unittest discover tests -v
node --test tests\node\test_ai_provider_router_guard.mjs
python tools\run_ai_provider.py status
python tools\run_ai_provider.py health
```

Docs:

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## Forbidden scope

P3-4 must not add:

```text
MT5 order send
position close/cancel/modify
broker adapter execution
wallet/private-key integration
Telegram command execution
Telegram webhook receiver
email delivery
public ingress
multi-user auth
billing/credits
live preset mutation
Kill Switch override
```

## Rollback

Remove the files listed above and remove the README link. No database migration is required.
