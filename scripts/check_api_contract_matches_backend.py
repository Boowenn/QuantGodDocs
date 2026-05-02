#!/usr/bin/env python3
"""Validate QuantGodDocs API contract and optionally compare it to Backend.

Standalone mode checks schema shape and safety defaults. With ``--backend`` it
also scans Dashboard route files for ``/api/*`` paths and ensures Docs covers
those backend route surfaces.
"""
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
    "/api/paramlab/auto-tester/:action",
    "/api/mt5-platform/:endpoint",
    "/api/mt5-trading/:endpoint",
    "/api/mt5/:endpoint",
    "/api/mt5/order/:ticket",
    "/api/mt5-readonly/:endpoint",
    "/api/mt5-symbol-registry/:endpoint",
}
REQUIRED_SAFETY_FALSE = [
    "orderSendAllowed",
    "closeAllowed",
    "cancelAllowed",
    "credentialStorageAllowed",
    "livePresetMutationAllowed",
    "canOverrideKillSwitch",
]


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract root must be object")
    return data


def contract_endpoints(contract: dict) -> set[str]:
    endpoints: set[str] = set()
    groups = contract.get("endpointGroups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("endpointGroups must be a non-empty list")

    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("endpoint group must be object")
        name = group.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("endpoint group missing name")
        endpoints_raw = group.get("endpoints")
        if not isinstance(endpoints_raw, list) or not endpoints_raw:
            raise ValueError(f"endpoint group {name!r} has no endpoints")
        for endpoint in endpoints_raw:
            if not isinstance(endpoint, dict):
                raise ValueError(f"invalid endpoint entry in group {name!r}")
            path = endpoint.get("path")
            method = endpoint.get("method")
            if not isinstance(path, str) or not path.startswith("/api/"):
                raise ValueError(f"invalid endpoint path: {path!r}")
            if not isinstance(method, str) or method.upper() not in {
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "ANY",
            }:
                raise ValueError(f"invalid method for {path}: {method!r}")
            endpoints.add(path.rstrip("/") or path)
    return endpoints


def normalize_backend_path(path: str) -> str:
    clean = path.rstrip("/") or path
    prefix_map = {
        "/api/ai-analysis/history/": "/api/ai-analysis/history/:id",
        "/api/ai-analysis-v2/history/": "/api/ai-analysis-v2/history/:id",
        "/api/vibe-coding/strategy/": "/api/vibe-coding/strategy/:id",
        "/api/paramlab/auto-tester/": "/api/paramlab/auto-tester/:action",
        "/api/mt5-platform/": "/api/mt5-platform/:endpoint",
        "/api/mt5-trading/": "/api/mt5-trading/:endpoint",
        "/api/mt5/order/": "/api/mt5/order/:ticket",
        "/api/mt5-readonly/": "/api/mt5-readonly/:endpoint",
        "/api/mt5-symbol-registry/": "/api/mt5-symbol-registry/:endpoint",
        "/api/mt5/": "/api/mt5/:endpoint",
    }
    for prefix, replacement in prefix_map.items():
        if clean.startswith(prefix):
            return replacement
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
            found.add(normalize_backend_path(match.group(0)))
    return found


def check_safety(contract: dict) -> list[str]:
    errors: list[str] = []
    safety = contract.get("safetyDefaults", {})
    if not isinstance(safety, dict):
        return ["safetyDefaults must be an object"]
    for key in REQUIRED_SAFETY_FALSE:
        if safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false")
    if safety.get("localOnly") is not True:
        errors.append("safetyDefaults.localOnly must be true")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="docs/contracts/api-contract.json")
    parser.add_argument("--backend", default=None, help="Optional QuantGodBackend root for route comparison")
    parser.add_argument("--strict-extra", action="store_true", help="Fail when docs contains paths not observed in backend files")
    parser.add_argument("--min-endpoints", type=int, default=100)
    args = parser.parse_args(argv)

    contract_path = Path(args.contract).resolve()
    errors: list[str] = []

    try:
        contract = load_contract(contract_path)
        documented = contract_endpoints(contract)
    except Exception as exc:  # noqa: BLE001
        print(f"QuantGod API contract check failed: {exc}")
        return 1

    if len(documented) < args.min_endpoints:
        errors.append(f"contract looks too small: only {len(documented)} endpoints; expected >= {args.min_endpoints}")
    errors.extend(check_safety(contract))

    if args.backend:
        backend_root = Path(args.backend).resolve()
        actual = backend_paths(backend_root)
        missing = sorted(path for path in actual if path not in documented)
        if missing:
            errors.append("backend route(s) missing from docs contract: " + ", ".join(missing[:60]))
        if args.strict_extra:
            extra = sorted(path for path in documented if path not in actual and path not in PLACEHOLDER_PATHS)
            if extra:
                errors.append("docs contract path(s) not observed in backend route files: " + ", ".join(extra[:60]))

    if errors:
        print("QuantGod API contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"QuantGod API contract check OK ({len(documented)} documented endpoints)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
