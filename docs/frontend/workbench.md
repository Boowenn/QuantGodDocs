# Vue 工作台

QuantGod Vue 工作台是当前唯一 active operator frontend。旧 HTML 页面已经退役，只做 `/vue/` 重定向或 fallback。

## 主要工作区

- 总控台：机会雷达、今日待办、每日复盘、Watchlist。
- AI 工作台：AI Analysis V1、K 线基础、历史分析。
- 策略工坊：Vibe Coding、AI V2 辩论、K 线增强。
- 运维通知：统一 API 状态、Telegram push-only。
- MT5 总览：执行雷达、路线、图表、交易只读、证据报表。
- Polymarket：治理总览、市场浏览、机会雷达、单市场分析、执行模拟、重调账本。
- ParamLab：tester-only 队列、报告回灌、恢复风险。

## 设计原则

工作台首先是操作面板，不是营销页。信息密度可以高，但必须有层次、可扫描、可定位。所有 badge、状态、队列和风险项都应能解释“为什么显示”和“下一步做什么”。

## 响应式要求

新增组件必须通过 `QuantGodFrontend/scripts/responsive_check.mjs` 覆盖：

```powershell
npm run responsive:check
```

重点检查：

- `320px` 窄屏。
- 手机宽度。
- iPad/in-app browser。
- MacBook 宽度。
- 大桌面宽度。

不允许依赖浏览器横向滚动来隐藏排版问题。
