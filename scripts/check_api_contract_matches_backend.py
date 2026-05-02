#!/usr/bin/env python3
"""Validate QuantGodDocs API contract and optionally compare it to backend route files."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATH_RE = re.compile(r"/api/[A-Za-z0-9_./:-]+")
PLACEHOLDER_PATHS = {
    "/api/ai-analysis/history/:id",
    "/api/ai-analysis-v2/history/:id",
    "/api/vibe-coding/strategy/:id",
}

IGNORED_BACKEND_PREFIXES: set[str] = set()


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract root must be object")
    return data


def contract_endpoints(contract: dict) -> set[str]:
    endpoints: set[str] = set()
    groups = contract.get("endpointGroups")
    if not isinstance(groups, list):
        raise ValueError("endpointGroups must be a list")
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("endpoint group must be object")
        for endpoint in group.get("endpoints", []):
            path = endpoint.get("path")
            method = endpoint.get("method")
            if not isinstance(path, str) or not path.startswith("/api/"):
                raise ValueError(f"invalid endpoint path: {path!r}")
            if not isinstance(method, str) or method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE", "ANY"}:
                raise ValueError(f"invalid method for {path}: {method!r}")
            endpoints.add(path)
    return endpoints


def normalize_backend_path(path: str) -> str:
    clean = path.rstrip("/") or path
    if path.startswith("/api/ai-analysis/history/"):
        return "/api/ai-analysis/history/:id"
    if path.startswith("/api/ai-analysis-v2/history/"):
        return "/api/ai-analysis-v2/history/:id"
    if path.startswith("/api/vibe-coding/strategy/"):
        return "/api/vibe-coding/strategy/:id"
    if path.startswith("/api/paramlab/auto-tester/"):
        return "/api/paramlab/auto-tester/:action"
    if path.startswith("/api/mt5-platform/"):
        return "/api/mt5-platform/:endpoint"
    if path.startswith("/api/mt5-trading/"):
        return "/api/mt5-trading/:endpoint"
    if path.startswith("/api/mt5/order/"):
        return "/api/mt5/order/:ticket"
    if path.startswith("/api/mt5-readonly/"):
        return "/api/mt5-readonly/:endpoint"
    if path.startswith("/api/mt5-symbol-registry/"):
        return "/api/mt5-symbol-registry/:endpoint"
    if path.startswith("/api/mt5/"):
        return "/api/mt5/:endpoint"
    return clean


def backend_paths(backend_root: Path) -> set[str]:
    candidates = [
        backend_root / "Dashboard" / "phase1_api_routes.js",
        backend_root / "Dashboard" / "phase2_api_routes.js",
        backend_root / "Dashboard" / "phase3_api_routes.js",
        backend_root / "Dashboard" / "dashboard_server.js",
    ]
    found: set[str] = set()
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in PATH_RE.finditer(text):
            value = normalize_backend_path(match.group(0))
            if any(value.startswith(prefix) for prefix in IGNORED_BACKEND_PREFIXES):
                continue
            found.add(value)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="docs/contracts/api-contract.json")
    parser.add_argument("--backend", default=None, help="Optional QuantGodBackend root for route comparison")
    parser.add_argument("--strict-extra", action="store_true", help="Also fail when contract contains paths not seen in backend")
    args = parser.parse_args(argv)

    contract_path = Path(args.contract).resolve()
    contract = load_contract(contract_path)
    documented = contract_endpoints(contract)

    errors: list[str] = []
    if len(documented) < 20:
        errors.append(f"contract looks too small: only {len(documented)} endpoints")

    safety = contract.get("safetyDefaults", {})
    for key in ["orderSendAllowed", "closeAllowed", "cancelAllowed", "credentialStorageAllowed", "livePresetMutationAllowed", "canOverrideKillSwitch"]:
        if safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false")

    if args.backend:
        backend_root = Path(args.backend).resolve()
        actual = backend_paths(backend_root)
        missing = sorted(path for path in actual if path not in documented)
        if missing:
            errors.append("backend route(s) missing from docs contract: " + ", ".join(missing[:40]))
        if args.strict_extra:
            extra = sorted(path for path in documented if path not in actual and path not in PLACEHOLDER_PATHS)
            if extra:
                errors.append("docs contract path(s) not observed in backend route files: " + ", ".join(extra[:40]))

    if errors:
        print("QuantGod API contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"QuantGod API contract check OK ({len(documented)} documented endpoints)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
