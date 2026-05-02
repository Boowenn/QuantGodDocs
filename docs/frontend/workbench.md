# Vue 工作台

QuantGodFrontend 是唯一 active operator frontend。旧 Dashboard 只保留归档或重定向，不再作为 active fallback。

## 推荐结构

```text
src/
├── app/
│   ├── AppShell.vue
│   ├── navigation.js
│   └── routes.js
├── workspaces/
│   ├── ai-analysis/
│   ├── ai-v2/
│   ├── kline/
│   ├── vibe-coding/
│   ├── governance/
│   ├── paramlab/
│   ├── mt5-monitor/
│   └── research/
├── services/
├── stores/
├── components/
└── styles/
```

## 模块化目标

- `App.vue` 只保留 app shell 和全局状态入口。
- 每个 workspace 单独维护自己的组件、状态和 API wrapper。
- 图表、表格、卡片、编辑器等通用 UI 放到 shared components。
- service 层统一错误处理和 loading 状态。

## 安全展示

前端可以展示 AI、Governance、ParamLab 和 MT5 状态，但不能修改 live preset 或绕过后端 guard。任何受控动作必须由 Backend 明确暴露 endpoint，并在 UI 上显示安全状态。
