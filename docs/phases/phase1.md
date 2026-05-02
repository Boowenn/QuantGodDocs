# Phase 1：AI 分析与 K 线基础

## 范围

Phase 1 建立了 QuantGod 的第一层 AI/图表能力：

- AI Analysis V1。
- 多 agent 初步证据采集。
- 本地 analysis history。
- KlineCharts 基础图表。
- MT5 read-only kline/trades/shadow signal API。
- CI 与基础测试。

## 安全定位

Phase 1 只写 advisory evidence，不能触发交易，不能修改 live preset，不能绕过 Kill Switch、authorization lock、dryRun 或 Governance。

## 前端入口

Phase 1 的前端能力现在由 `QuantGodFrontend` 维护，主要位于 AI 工作台和 K 线相关组件。

## 后端入口

后端能力仍在 `QuantGodBackend`：

- `tools/ai_analysis/`
- `tools/run_ai_analysis.py`
- `tools/mt5_chart_readonly.py`
- `Dashboard/phase1_api_routes.js`

## 验收重点

- 无 OpenRouter key 时可 fallback，保证 UI/API/CI 可跑通。
- AI 输出必须带 safety envelope。
- K 线、交易、shadow signal 端点保持 read-only。
