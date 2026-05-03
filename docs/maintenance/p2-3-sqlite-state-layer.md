# P2-3 SQLite 状态层阶段门

P2-3 是 P2 治理与数据层的第三个阶段门。P2-2 治理文件完成后，只能进入 P2-3，不能跳到 P3。

## 完成标准

P2-3 完成需要满足：

```text
Backend SQLite schema 初始化成功
CLI init/status/ingest/query 可用
/api/state/* 只读端点可用
Backend Python tests 通过
Backend Node route tests 通过
Docs 有 SQLite 状态层说明
Docs API contract 包含 p2-3-sqlite-state-layer
所有安全默认值保持 non-execution / non-mutation
```

## Backend 文件

```text
Dashboard/state_api_routes.js
tools/run_state_store.py
tools/state_store/__init__.py
tools/state_store/config.py
tools/state_store/db.py
tools/state_store/ingest.py
tools/state_store/safety.py
tests/test_state_store.py
tests/node/test_state_api_routes.mjs
```

`Dashboard/dashboard_server.js` 需要挂载 `state_api_routes.js`。挂载顺序放在 Phase 3、Phase 2、Phase 1 route 前后均可，但建议放在 Phase 3 前，避免 `/api/state/*` 被 legacy fallback 处理。

## Docs 文件

```text
docs/backend/sqlite-state.md
docs/maintenance/p2-3-sqlite-state-layer.md
docs/contracts/api-contract.json
```

`api-contract.json` 需要新增 endpoint group：

```text
name: p2-3-sqlite-state-layer
phase: phase2
```

端点：

```text
GET /api/state
GET /api/state/status
GET /api/state/config
GET /api/state/events
GET /api/state/ai-analysis
GET /api/state/vibe-strategies
GET /api/state/notifications
```

## 验证命令

Backend：

```powershell
cd QuantGodBackend
python -m py_compile tools\run_state_store.py tools\state_store\config.py tools\state_store\db.py tools\state_store\ingest.py tools\state_store\safety.py
python -m unittest discover tests -v
node --check Dashboard\state_api_routes.js
npm test
python tools\run_state_store.py init
python tools\run_state_store.py status
python tools\run_state_store.py ingest --sources all
```

Docs：

```powershell
cd QuantGodDocs
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 下一阶段

P2-3 完成后，阶段门进入 P3-1 Docker/local-dev stack。
