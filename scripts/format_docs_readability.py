#!/usr/bin/env python3
"""Repair collapsed Markdown / JSON files in QuantGodDocs.

This is intentionally conservative. It does not try to be a full Markdown
formatter; it only restores real line breaks around headings, lists, tables, code
fences, and Windows/PowerShell continuation examples when a file has clearly
been collapsed into one or two very long lines.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "dist", "__pycache__"}


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def repair_markdown_text(text: str) -> str:
    original = text
    lines = text.splitlines()
    if len(original) < 500 or len(lines) >= 6:
        return original

    repaired = original.strip()

    # Restore common block boundaries.
    repaired = re.sub(r"\s+(#{1,6}\s+)", r"\n\n\1", repaired)
    repaired = re.sub(r"\s+(```[A-Za-z0-9_-]*)(\s+)", r"\n\n\1\n", repaired)
    repaired = re.sub(r"\s+```", r"\n```", repaired)

    # Lists and numbered lists.
    repaired = re.sub(r"\s+(\d+\.\s+)", r"\n\1", repaired)
    repaired = re.sub(r"\s+(-\s+\[[^\]]+\]\([^)]*\))", r"\n\1", repaired)
    repaired = re.sub(r"\s+(-\s+`[^`]+`)", r"\n\1", repaired)

    # Markdown tables: add line breaks before rows when they are glued together.
    repaired = repaired.replace(" | |---", "\n|---")
    repaired = re.sub(r"\s+(\|[^\n]+?\|)(?=\s+\|)", r"\n\1", repaired)
    repaired = re.sub(r"(\|---[^\n]*?\|)\s+", r"\1\n", repaired)

    # Common Chinese section boundaries in the generated docs.
    repaired = repaired.replace("。 ## ", "。\n\n## ")
    repaired = repaired.replace("。 ### ", "。\n\n### ")
    repaired = repaired.replace("。 - ", "。\n- ")
    repaired = repaired.replace("。 1. ", "。\n1. ")

    # Powershell line continuations sometimes get glued to the next line.
    repaired = repaired.replace(" ` --", " `\n  --")

    # Avoid excessive blank lines.
    repaired = re.sub(r"\n{3,}", "\n\n", repaired)
    return repaired.rstrip() + "\n"


def repair_markdown_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    repaired = repair_markdown_text(text)
    if repaired != text:
        path.write_text(repaired, encoding="utf-8")
        return True
    return False


def pretty_print_json(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except Exception:  # noqa: BLE001
        return False
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if rendered != text:
        path.write_text(rendered, encoding="utf-8")
        return True
    return False


def repair_repo(root: Path) -> list[str]:
    changed: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if not should_skip(path) and repair_markdown_file(path):
            changed.append(str(path.relative_to(root)))
    for path in sorted(root.rglob("*.json")):
        if not should_skip(path) and pretty_print_json(path):
            changed.append(str(path.relative_to(root)))
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="QuantGodDocs repository root")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    changed = repair_repo(root)
    if changed:
        print("Repaired docs readability:")
        for rel in changed:
            print(f"- {rel}")
    else:
        print("No collapsed docs needed repair")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
