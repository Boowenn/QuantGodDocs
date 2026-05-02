# QuantGod 四仓库拆分架构

## 拆分目标

QuantGod 原始仓库同时包含 MT5/MQL5、Node dashboard server、Python tools、Vue frontend、Cloudflare/Infra 和大量文档。随着 Phase 1、Phase 2、Phase 3 功能加入，单仓库维护成本开始变高。

四仓库拆分的目标是：

1. 让后端交易/研究/治理逻辑和前端 UI 解耦。
2. 让 Infra 可以单独维护部署、同步和批量测试。
3. 让文档成为独立 contract hub，避免 README 越来越长。
4. 降低小模块改动的 blast radius。
5. 让 CI 护栏按仓库职责分别执行。

## 仓库拓扑

```text
QuantGodBackend
  ├─ exposes localhost /api/*
  ├─ serves Dashboard/vue-dist for operator workbench
  └─ writes/reads MT5 runtime artifacts under local runtime directories

QuantGodFrontend
  ├─ builds Vue app into dist/
  ├─ calls QuantGodBackend /api/* only
  └─ never reads QuantGod_*.json/csv files directly

QuantGodInfra
  ├─ pulls/tests four repos
  ├─ builds QuantGodFrontend
  ├─ syncs dist/ into QuantGodBackend/Dashboard/vue-dist
  └─ manages Cloudflare/docs/deploy helper scripts

QuantGodDocs
  ├─ stores architecture docs
  ├─ stores API contract
  ├─ stores runbooks and safety docs
  └─ validates links and contract JSON
```

## Local-first 原则

QuantGod 不是公网交易 API。Backend API 应该保持 localhost operator 面板用途。Telegram 只推送，不接受命令。AI 和 Vibe Coding 都是 advisory/research-only。MT5/HFM live pilot 仍由 EA 内部 safety guard、Kill Switch、授权锁和 dryRun 边界保护。

## 提交顺序建议

涉及四仓库联动时，建议顺序是：

1. `QuantGodBackend`：新增兼容 endpoint 或调整 envelope。
2. `QuantGodDocs`：更新 `api-contract.json` 和 Markdown 文档。
3. `QuantGodFrontend`：消费新 endpoint。
4. `QuantGodInfra`：如果 build/sync/test 方式变化，再更新 workspace 脚本。

这样能避免前端先调用不存在的 endpoint，或者 Infra 同步一个 contract 未定义的页面。
