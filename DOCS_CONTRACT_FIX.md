# QuantGodDocs 文档与 API Contract 加固

这次修复用于四仓库拆分后的 Docs 仓库，让 Docs 不再只是 README 占位，而是成为 backend/frontend/infra/docs 的 contract hub。

## 新增内容

- 多行可读 Markdown 文档体系。
- `docs/contracts/api-contract.json`。
- `docs/contracts/repo-manifest.schema.json`。
- `scripts/check_docs_links.py`。
- `scripts/check_api_contract_matches_backend.py`。
- `tests/test_docs_contract.py`。
- Docs CI。

## 本地验证

```powershell
cd C:\QuantGod\QuantGodDocs
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json
python -m unittest discover tests -v
```

如果本地有 Backend 仓库：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```

## 安全边界

本修复只新增文档和检查脚本，不修改交易逻辑，不接触 MT5 preset，不发送订单，不平仓，不绕过 Kill Switch、authorization lock 或 dry-run 边界。
