#!/usr/bin/env python3
"""Validate QuantGodDocs API contract and optionally compare it to Backend routes."""

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
    "/api/mt5/order/:ticket",
    "/api/mt5-readonly/:endpoint",
    "/api/mt5-symbol-registry/:endpoint",
    "/api/mt5/:endpoint",
}

REQUIRED_SAFETY_FALSE_KEYS = [
    "orderSendAllowed",
    "closeAllowed",
    "cancelAllowed",
    "credentialStorageAllowed",
    "livePresetMutationAllowed",
    "canOverrideKillSwitch",
]

OPTIONAL_SAFETY_FALSE_KEYS = [
    "canMutateGovernanceDecision",
    "telegramCommandExecutionAllowed",
]

REQUIRED_ENDPOINT_GROUPS = {
    "backend-core-and-control",
    "polymarket-research",
    "mt5-readonly",
    "ai-analysis-v1",
    "phase2-file-facade",
    "notify",
    "phase3-vibe-ai-kline",
}

BACKEND_ROUTE_FILES = [
    "Dashboard/phase1_api_routes.js",
    "Dashboard/phase2_api_routes.js",
    "Dashboard/phase3_api_routes.js",
    "Dashboard/dashboard_server.js",
]


def load_contract(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract root must be object")
    return data


def endpoint_groups(contract: dict) -> list[dict]:
    groups = contract.get("endpointGroups")
    if not isinstance(groups, list):
        raise ValueError("endpointGroups must be a list")
    return groups


def contract_endpoints(contract: dict) -> set[str]:
    endpoints: set[str] = set()
    for group in endpoint_groups(contract):
        if not isinstance(group, dict):
            raise ValueError("endpoint group must be object")
        for endpoint in group.get("endpoints", []):
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
            endpoints.add(path)
    return endpoints


def check_required_groups(contract: dict) -> list[str]:
    group_names = {
        group.get("name")
        for group in endpoint_groups(contract)
        if isinstance(group, dict)
    }
    missing = sorted(REQUIRED_ENDPOINT_GROUPS - group_names)
    return [f"missing endpoint group: {name}" for name in missing]


def check_safety(contract: dict) -> list[str]:
    errors: list[str] = []
    safety = contract.get("safetyDefaults", {})
    if safety.get("localOnly") is not True:
        errors.append("safetyDefaults.localOnly must be true")

    for key in REQUIRED_SAFETY_FALSE_KEYS:
        if safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false")

    for key in OPTIONAL_SAFETY_FALSE_KEYS:
        if key in safety and safety.get(key) is not False:
            errors.append(f"safetyDefaults.{key} must be false when present")

    return errors


def normalize_backend_path(path: str) -> str:
    clean = path.rstrip("/") or path

    if clean.startswith("/api/ai-analysis/history/"):
        return "/api/ai-analysis/history/:id"
    if clean.startswith("/api/ai-analysis-v2/history/"):
        return "/api/ai-analysis-v2/history/:id"
    if clean.startswith("/api/vibe-coding/strategy/"):
        return "/api/vibe-coding/strategy/:id"
    if clean.startswith("/api/paramlab/auto-tester/"):
        return "/api/paramlab/auto-tester/:action"
    if clean.startswith("/api/mt5-platform/"):
        return "/api/mt5-platform/:endpoint"
    if clean.startswith("/api/mt5-trading/"):
        return "/api/mt5-trading/:endpoint"
    if clean.startswith("/api/mt5/order/"):
        return "/api/mt5/order/:ticket"
    if clean.startswith("/api/mt5-readonly/"):
        return "/api/mt5-readonly/:endpoint"
    if clean.startswith("/api/mt5-symbol-registry/"):
        return "/api/mt5-symbol-registry/:endpoint"
    if clean.startswith("/api/mt5/"):
        return "/api/mt5/:endpoint"

    return clean


def backend_paths(backend_root: Path) -> set[str]:
    found: set[str] = set()
    for rel in BACKEND_ROUTE_FILES:
        path = backend_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in PATH_RE.finditer(text):
            found.add(normalize_backend_path(match.group(0)))
    return found


def compare_backend_routes(contract: dict, backend_root: Path, strict_extra: bool) -> list[str]:
    documented = contract_endpoints(contract)
    actual = backend_paths(backend_root)
    errors: list[str] = []

    missing = sorted(path for path in actual if path not in documented)
    if missing:
        errors.append(
            "backend route(s) missing from docs contract: " + ", ".join(missing[:50])
        )

    if strict_extra:
        extra = sorted(
            path
            for path in documented
            if path not in actual and path not in PLACEHOLDER_PATHS
        )
        if extra:
            errors.append(
                "docs contract path(s) not observed in backend route files: "
                + ", ".join(extra[:50])
            )

    return errors


def validate_contract(contract: dict, min_endpoints: int = 100) -> list[str]:
    errors: list[str] = []
    documented = contract_endpoints(contract)

    if len(documented) < min_endpoints:
        errors.append(
            f"contract looks too small: only {len(documented)} endpoints; "
            f"expected at least {min_endpoints}"
        )

    errors.extend(check_required_groups(contract))
    errors.extend(check_safety(contract))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default="docs/contracts/api-contract.json")
    parser.add_argument(
        "--backend",
        default=None,
        help="Optional QuantGodBackend root for route comparison",
    )
    parser.add_argument(
        "--strict-extra",
        action="store_true",
        help="Also fail when contract contains paths not seen in backend route files",
    )
    parser.add_argument(
        "--min-endpoints",
        type=int,
        default=100,
        help="Minimum documented endpoint count expected in the contract",
    )
    args = parser.parse_args(argv)

    contract_path = Path(args.contract).resolve()
    contract = load_contract(contract_path)
    errors = validate_contract(contract, min_endpoints=args.min_endpoints)

    if args.backend:
        errors.extend(compare_backend_routes(contract, Path(args.backend).resolve(), args.strict_extra))

    if errors:
        print("QuantGod API contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "QuantGod API contract check OK "
        f"({len(contract_endpoints(contract))} documented endpoints)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
