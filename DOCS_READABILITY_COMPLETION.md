# QuantGodDocs 可读性完成补丁

本补丁用于完成 P2 的第一项：`Docs 重新格式化成可读 Markdown`。

它不会添加 LICENSE、SECURITY、CONTRIBUTING，也不会进入 SQLite、Docker、Webhook 或 broker adapter 阶段。

## 新增内容

```text
scripts/check_docs_quality_gate.py
tests/test_docs_quality_gate.py
docs/maintenance/docs-completion-matrix.md
```

## 检查内容

`check_docs_quality_gate.py` 会验证：

1. 核心文档存在。
2. 核心 Markdown 不是一两行压缩文件。
3. Markdown 有 H1 和多个小节。
4. `api-contract.json` 可解析，endpoint 数量不低于 100。
5. 执行/变更类安全默认值保持 `false`。
6. Phase 文档包含交付物和安全边界。
7. 文档内不包含常见 token/key 模式。

## 本地验证

```bash
python scripts/check_docs_quality_gate.py --root .
python scripts/check_docs_links.py --root .
python scripts/check_api_contract_matches_backend.py --contract docs/contracts/api-contract.json
python -m unittest discover tests -v
```

如果本地同时有 Backend 仓库：

```bash
python scripts/check_api_contract_matches_backend.py \
  --contract docs/contracts/api-contract.json \
  --backend ../QuantGodBackend
```
