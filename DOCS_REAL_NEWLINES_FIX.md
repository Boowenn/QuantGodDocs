# QuantGodDocs 真实换行与 CI 有效性修复

这次修复针对 Docs 仓库中仍然存在的单行压缩问题：

1. `scripts/check_docs_links.py`、`scripts/check_api_contract_matches_backend.py`、`tests/test_docs_contract.py` 等文件如果被压成一行，可能导致 shebang 注释吞掉主体逻辑，或者让 CI 检查失效。
2. `.github/workflows/ci.yml` 如果被压成少数长行，YAML 可读性和可靠性都会下降。
3. Markdown 文档如果被压成一两行，虽然页面可能还能显示，但 review 和维护成本很高。

## 修复内容

- 重写 Docs 检查脚本为真实多行 Python。
- 新增 `scripts/format_docs_readability.py`，用于修复明显被压缩的 Markdown，并 pretty-print JSON。
- 保留现有 `docs/contracts/api-contract.json`，不会回滚你已补齐的 endpoint。
- 重新渲染 `docs/backend/api-contract.md`。
- 重写 Docs CI workflow 为真实多行 YAML。
- 新增单元测试，防止脚本、测试和 workflow 再次被压成少数长行。

## 本地验证

```powershell
cd C:\QuantGod\QuantGodDocs

python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json
python -m unittest discover tests -v
```

如果本地同时有 Backend 仓库，再跑跨仓库 route 对齐：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```

## 安全边界

本修复只修改 Docs 仓库的文档、检查脚本、测试和 CI，不修改 Backend、Frontend、Infra，不接触 MT5 preset，不发送订单，不平仓，不绕过 Kill Switch、authorization lock 或 dry-run 边界。
