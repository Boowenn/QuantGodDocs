# QuantGodDocs 格式与 CI 检查修复

这次修复用于解决四仓库拆分后 Docs 仓库中出现的两个问题：

1. 部分 Markdown 被压成一行，可读性差，也违反文档维护规则。
2. 部分 Python 检查脚本被压成单行后，`#!/usr/bin/env python3` 之后的代码会被当成注释，导致 CI 实际没有执行检查。

## 修复内容

- 重写 `scripts/check_docs_links.py`，增加 Markdown、JSON、Python collapsed-file 检查。
- 重写 `scripts/check_api_contract_matches_backend.py`，保留 100+ endpoint contract 下限和 safety defaults 校验。
- 新增 `scripts/render_api_contract_markdown.py`，从 JSON contract 生成人工 review 版 `docs/backend/api-contract.md`。
- 重新格式化关键中文 Markdown 文档。
- 将 `docs/contracts/api-contract.json` pretty-print，保留本地已有 endpoint 内容。
- 增加单元测试，防止检查脚本再次被压成一行。

## 本地验证

```powershell
cd C:\QuantGod\QuantGodDocs
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json
python -m unittest discover tests -v
```

有 Backend 本地仓库时：

```powershell
python scripts\check_api_contract_matches_backend.py `
  --contract docs\contracts\api-contract.json `
  --backend ..\QuantGodBackend
```

## 安全边界

本修复只修改文档、文档检查脚本和 Docs CI，不修改交易逻辑，不接触 MT5 preset，不发送订单，不平仓，不绕过 Kill Switch、authorization lock 或 dry-run 边界。
