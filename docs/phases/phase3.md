# Phase 3：策略工坊与 AI V2

## 范围

Phase 3 增加策略研究和更完整的 AI 辩论能力：

- 策略工坊（Vibe Coding）。
- 自然语言生成 Python `BaseStrategy`。
- AST 安全检查。
- research-only local backtest。
- AI Analysis V2：News、Sentiment、Bull、Bear、Decision V2。
- 本地 RAG memory。
- K 线 AI overlay 与 Vibe indicator overlay。

## 安全定位

Phase 3 是研究层，不是实盘执行层。生成策略进入 live 必须经过：

```text
backtest → ParamLab → Governance → Version Gate → manual authorization
```

AI V2 的多空辩论只能作为 DecisionAgent 的参考，不能直接触发 order-send、preset mutation 或 Governance mutation。

## 后端入口

- `Dashboard/phase3_api_routes.js`
- `tools/vibe_coding/`
- `tools/run_vibe_coding.py`
- `tools/ai_analysis/analysis_service_v2.py`
- `tools/run_ai_analysis_v2.py`
- `tools/kline_phase3_overlays.py`

## 前端入口

- `src/components/phase3/Phase3Workspace.vue`
- `src/components/phase3/vibe/*`
- `src/components/phase3/ai/*`
- `src/components/phase3/kline/*`
- `src/services/phase3Api.js`

## 验收重点

- 生成策略不能 import 危险模块。
- Vibe backtest 不依赖真实交易终端。
- AI V2 evidence 明确 `advisoryOnly=true`。
- 前端显示名称为“策略工坊”，不暴露工程化 Phase 命名。
- 页面保持 QuantGod 深色风格和响应式。
