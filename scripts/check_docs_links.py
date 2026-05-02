#!/usr/bin/env python3
"""Simple docs sanity check: verify Markdown files are readable and key docs exist."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
required = [
    ROOT / "README.md",
    ROOT / "docs" / "architecture" / "repo-split.md",
    ROOT / "docs" / "architecture" / "linkage-contract.md",
    ROOT / "docs" / "backend" / "api-contract.md",
    ROOT / "docs" / "frontend" / "README.md",
    ROOT / "docs" / "infra" / "README.md",
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    print("Missing required docs:")
    print("\n".join(missing))
    sys.exit(1)
for md in ROOT.rglob("*.md"):
    try:
        md.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Cannot read {md}: {exc}")
        sys.exit(1)
print(f"docs check OK: {len(list(ROOT.rglob('*.md')))} markdown files")
