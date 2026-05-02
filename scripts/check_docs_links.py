#!/usr/bin/env python3
"""QuantGodDocs Markdown and contract hygiene checker."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)

IGNORED_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "#",
)


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", "node_modules", "dist"} for part in path.parts):
            continue
        yield path


def check_markdown(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)
        if not text.strip():
            errors.append(f"{rel}: empty markdown file")
            continue
        if not HEADING_RE.search(text):
            errors.append(f"{rel}: missing markdown heading")
        if len(text) > 500 and "\n" not in text[:500]:
            errors.append(f"{rel}: appears to be compressed into one long line")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(IGNORED_PREFIXES):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            target_path = (path.parent / clean_target).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{rel}: link escapes repository: {target}")
                continue
            if not target_path.exists():
                errors.append(f"{rel}: broken relative link: {target}")
    return errors


def check_json(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.json")):
        if any(part in {".git", "node_modules", "dist"} for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Docs repository root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    required = [
        root / "README.md",
        root / "docs" / "contracts" / "api-contract.json",
        root / "docs" / "backend" / "api-contract.md",
        root / "docs" / "backend" / "safety-boundaries.md",
        root / "docs" / "frontend" / "api-client.md",
        root / "docs" / "infra" / "workspace-automation.md",
    ]
    errors = [f"missing required file: {path.relative_to(root)}" for path in required if not path.exists()]
    errors.extend(check_markdown(root))
    errors.extend(check_json(root))
    if errors:
        print("QuantGodDocs check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("QuantGodDocs link/content check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
