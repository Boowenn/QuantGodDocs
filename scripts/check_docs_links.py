#!/usr/bin/env python3
"""QuantGodDocs Markdown, JSON, and link hygiene checker.

This script intentionally lives in QuantGodDocs, not Backend or Frontend.
It catches the repository-split documentation failure mode where Markdown or
Python files are accidentally collapsed into one giant line.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)
IGNORED_LINK_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "#",
)
IGNORED_DIRS = {".git", "node_modules", "dist", "__pycache__"}
REQUIRED_FILES = [
    "README.md",
    "docs/contracts/api-contract.json",
    "docs/contracts/repo-manifest.schema.json",
    "docs/backend/api-contract.md",
    "docs/backend/safety-boundaries.md",
    "docs/frontend/api-client.md",
    "docs/infra/workspace-automation.md",
    "docs/architecture/repo-split.md",
    "docs/architecture/linkage-contract.md",
    "docs/ops/runbook-local.md",
    "docs/phases/phase1.md",
    "docs/phases/phase2.md",
    "docs/phases/phase3.md",
]


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if not should_skip(path):
            yield path


def iter_json(root: Path):
    for path in sorted(root.rglob("*.json")):
        if not should_skip(path):
            yield path


def iter_python(root: Path):
    for path in sorted(root.rglob("*.py")):
        if not should_skip(path):
            yield path


def check_required(root: Path) -> list[str]:
    return [
        f"missing required file: {rel}"
        for rel in REQUIRED_FILES
        if not (root / rel).exists()
    ]


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

        lines = text.splitlines()
        if len(text) > 800 and len(lines) < 5:
            errors.append(f"{rel}: appears compressed into {len(lines)} long line(s)")
        longest = max((len(line) for line in lines), default=0)
        if longest > 1800:
            errors.append(f"{rel}: line too long ({longest} chars); use readable Markdown line breaks")

        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(IGNORED_LINK_PREFIXES):
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
    for path in iter_json(root):
        rel = path.relative_to(root)
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel}: invalid JSON: {exc}")
    return errors


def check_python_not_collapsed(root: Path) -> list[str]:
    errors: list[str] = []
    for path in iter_python(root):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(text) > 500 and len(lines) < 5:
            errors.append(f"{rel}: Python file appears collapsed into one long line")
        if text.startswith("#!/") and len(lines) == 1 and "def " in text:
            errors.append(f"{rel}: code appears to be commented out by shebang line")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Docs repository root")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    errors: list[str] = []
    errors.extend(check_required(root))
    errors.extend(check_markdown(root))
    errors.extend(check_json(root))
    errors.extend(check_python_not_collapsed(root))

    if errors:
        print("QuantGodDocs check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("QuantGodDocs link/content check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
