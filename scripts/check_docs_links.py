#!/usr/bin/env python3
"""QuantGodDocs Markdown, JSON, Python, and link hygiene checker.

This checker intentionally lives in QuantGodDocs.  It catches the repository
split failure mode where Markdown, Python, JSON, or YAML files are accidentally
collapsed into one or two very long lines, which can make CI appear green while
actual checks become ineffective.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)

IGNORED_LINK_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "#",
)

IGNORED_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "dist",
    "__pycache__",
}

REQUIRED_FILES = [
    "README.md",
    ".github/workflows/ci.yml",
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
    "scripts/check_docs_links.py",
    "scripts/check_api_contract_matches_backend.py",
    "scripts/render_api_contract_markdown.py",
]

PYTHON_SCRIPTS_THAT_MUST_NOT_COLLAPSE = [
    "scripts/check_docs_links.py",
    "scripts/check_api_contract_matches_backend.py",
    "scripts/render_api_contract_markdown.py",
    "tests/test_docs_contract.py",
]

WORKFLOW_FILES_THAT_MUST_NOT_COLLAPSE = [
    ".github/workflows/ci.yml",
]


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def iter_files(root: Path, pattern: str) -> Iterable[Path]:
    for path in sorted(root.rglob(pattern)):
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
    for path in iter_files(root, "*.md"):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root)

        if not text.strip():
            errors.append(f"{rel}: empty markdown file")
            continue

        if not HEADING_RE.search(text):
            errors.append(f"{rel}: missing markdown heading")

        lines = text.splitlines()
        longest = max((len(line) for line in lines), default=0)

        if len(text) > 800 and len(lines) < 6:
            errors.append(
                f"{rel}: appears compressed into {len(lines)} long line(s); "
                "run scripts/format_docs_readability.py"
            )

        if longest > 1800:
            errors.append(
                f"{rel}: line too long ({longest} chars); "
                "use readable Markdown line breaks"
            )

        errors.extend(check_markdown_links(root, path, text))

    return errors


def check_markdown_links(root: Path, path: Path, text: str) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(root)

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
    for path in iter_files(root, "*.json"):
        rel = path.relative_to(root)
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel}: invalid JSON: {exc}")
    return errors


def check_python_not_collapsed(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in PYTHON_SCRIPTS_THAT_MUST_NOT_COLLAPSE:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        if len(text) > 500 and len(lines) < 10:
            errors.append(f"{rel}: Python file appears collapsed into long line(s)")

        if text.startswith("#!/") and lines and "def " in lines[0]:
            errors.append(f"{rel}: code appears commented out by shebang line")

        if "\n" not in text and len(text) > 500:
            errors.append(f"{rel}: file has no real newline characters")

    return errors


def check_workflow_not_collapsed(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in WORKFLOW_FILES_THAT_MUST_NOT_COLLAPSE:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        if len(lines) < 15:
            errors.append(f"{rel}: workflow appears collapsed into {len(lines)} line(s)")
        if "\n  " not in text:
            errors.append(f"{rel}: workflow lacks expected YAML indentation")

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
    errors.extend(check_workflow_not_collapsed(root))

    if errors:
        print("QuantGodDocs check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("QuantGodDocs link/content check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
