# 前端指南

## 仓库

`Boowenn/QuantGodFrontend`

## 职责

前端负责 QuantGod operator workbench 的视觉体验、导航、图表、表格、策略工坊界面和 API 展示层。它不拥有 MT5 runtime、不执行策略、不保存凭据。

## 本地开发

```powershell
cd ..\QuantGodBackend
Dashboard\start_dashboard.bat

cd ..\QuantGodFrontend
npm install
npm run dev
```

入口：

```text
http://127.0.0.1:5173/vue/
```

## 构建

```powershell
npm run build
```

构建产物在 `dist/`。需要由 `QuantGodInfra` 同步到后端：

```powershell
cd ..\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

## UI 要求

- 深色 QuantGod 工作台风格。
- 页面应适配 Mac、桌面、平板、窄屏和 in-app browser。
- 文本不能溢出容器。
- 卡片不应无限拉高或出现无意义大空白。
- 工具栏、表格、队列、图表必须有明确滚动边界。
- 不使用白底默认组件破坏整体视觉。

## 数据规则

前端只通过 `/api/*` 获取数据，不直接读本地 JSON/CSV。所有交易、治理、策略升级和通知动作都必须由后端安全契约决定。
