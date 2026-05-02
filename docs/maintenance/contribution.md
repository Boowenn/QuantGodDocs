# 贡献与维护规则

## 改动归属

- 改 MT5、Python tools、API、AI、Governance、ParamLab：提交到 `QuantGodBackend`。
- 改 Vue 页面、Kline、Ant Design Vue、Monaco、样式：提交到 `QuantGodFrontend`。
- 改 Cloudflare、workspace、同步脚本、部署：提交到 `QuantGodInfra`。
- 改说明、API 文档、Runbook、Phase 状态：提交到 `QuantGodDocs`。

## API 变更顺序

1. Backend 先加兼容字段或 endpoint。
2. Docs 更新 API contract。
3. Frontend 再消费。
4. Infra 只有构建/部署方式变了才改。

## 提交前检查

- 不提交 token、密码、HFM 凭据、钱包私钥。
- 不把 `node_modules/`、`dist/`、runtime ledger、tester 大文件提交进 Git。
- Backend tests、Frontend build、Docs link check 至少跑过相关部分。
- 涉及安全边界时，文档必须同步说明。
