from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_api_contract_matches_backend as api_check
from scripts import check_docs_links as docs_check


class DocsContractTests(unittest.TestCase):
    def test_overlay_scripts_are_not_collapsed(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for rel in [
            "scripts/check_docs_links.py",
            "scripts/check_api_contract_matches_backend.py",
            "scripts/render_api_contract_markdown.py",
        ]:
            text = (root / rel).read_text(encoding="utf-8")
            self.assertGreater(len(text.splitlines()), 20, rel)
            self.assertIn("def main", text, rel)

    def test_contract_endpoint_counter(self) -> None:
        contract = {
            "endpointGroups": [
                {
                    "name": "core",
                    "endpoints": [
                        {"method": "GET", "path": "/api/latest"},
                        {"method": "POST", "path": "/api/notify/test"},
                    ],
                }
            ]
        }
        self.assertEqual(api_check.contract_endpoints(contract), {"/api/latest", "/api/notify/test"})

    def test_safety_defaults_require_false_for_trading_fields(self) -> None:
        errors = api_check.check_safety(
            {
                "safetyDefaults": {
                    "localOnly": True,
                    "orderSendAllowed": False,
                    "closeAllowed": False,
                    "cancelAllowed": False,
                    "credentialStorageAllowed": False,
                    "livePresetMutationAllowed": False,
                    "canOverrideKillSwitch": False,
                }
            }
        )
        self.assertEqual(errors, [])

    def test_docs_checker_detects_collapsed_python(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# README\n\nOK\n", encoding="utf-8")
            (root / "docs/contracts").mkdir(parents=True)
            (root / "docs/contracts/api-contract.json").write_text("{}", encoding="utf-8")
            bad = root / "bad.py"
            bad.write_text("#!/usr/bin/env python3 def main(): return 0", encoding="utf-8")
            errors = docs_check.check_python_not_collapsed(root)
            self.assertTrue(any("commented out by shebang" in error for error in errors))

    def test_json_roundtrip_contract_shape(self) -> None:
        payload = {
            "schemaVersion": 1,
            "safetyDefaults": {
                "localOnly": True,
                "orderSendAllowed": False,
                "closeAllowed": False,
                "cancelAllowed": False,
                "credentialStorageAllowed": False,
                "livePresetMutationAllowed": False,
                "canOverrideKillSwitch": False,
            },
            "endpointGroups": [
                {"name": "x", "endpoints": [{"method": "GET", "path": "/api/x"}]},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "api-contract.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            loaded = api_check.load_contract(path)
            self.assertEqual(api_check.contract_endpoints(loaded), {"/api/x"})


if __name__ == "__main__":
    unittest.main()
