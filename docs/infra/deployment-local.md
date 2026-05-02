# 本地部署

QuantGod 当前是 local-first 架构。MT5/HFM 终端仍运行在本机，Backend Node server 提供本地 API 和 Vue dist。

## 本地链路

```text
MT5 / HFM Terminal
  -> MQL5/Files runtime JSON/CSV
  -> QuantGodBackend Dashboard server
  -> http://127.0.0.1:8080/api/*
  -> QuantGodFrontend Vue workbench
```

## 前端发布到 Backend

```powershell
cd C:\QuantGod\QuantGodFrontend
npm install
npm run build

cd C:\QuantGod\QuantGodInfra
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
```

同步后 Backend 应提供：

```text
http://127.0.0.1:8080/vue/
```

## 外网暴露原则

默认不要把 Backend API 暴露到外网。即使使用 Cloudflare，也应只暴露静态文档或经过明确隔离的页面，不暴露交易控制面。
