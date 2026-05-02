# 基础设施指南

## 仓库

`Boowenn/QuantGodInfra`

## 职责

Infra 负责四仓库联动、Cloudflare 可选部署、前端 dist 同步和 workspace 级别验证。它不写策略逻辑，不拥有 Vue 源码，也不修改 MT5 live preset。

## 关键脚本

```text
scripts/qg-workspace.py
scripts/qg-workspace.ps1
```

## 常用命令

```powershell
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json status
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json pull
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json test
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json build-frontend
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json sync-frontend-dist
python scripts\qg-workspace.py --workspace workspace\quantgod.workspace.json verify
```

## Secret 规则

Cloudflare token、Wrangler secret、Telegram token、OpenRouter key、HFM/MT5 凭据都不能进入 Git。Infra 只能保存示例配置和本地路径模板。
