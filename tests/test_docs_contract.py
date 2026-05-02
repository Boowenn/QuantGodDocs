from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DocsContractTests(unittest.TestCase):
    def test_api_contract_has_required_endpoint_groups(self) -> None:
        contract = json.loads((ROOT / "docs/contracts/api-contract.json").read_text(encoding="utf-8"))
        names = {group["name"] for group in contract["endpointGroups"]}
        self.assertIn("ai-analysis-v1", names)
        self.assertIn("phase2-file-facade", names)
        self.assertIn("phase3-vibe-ai-kline", names)
        self.assertFalse(contract["safetyDefaults"]["orderSendAllowed"])

    def test_docs_link_checker_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_docs_links.py"), "--root", str(ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_contract_checker_passes_standalone(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_api_contract_matches_backend.py"), "--contract", str(ROOT / "docs/contracts/api-contract.json")],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_contract_checker_detects_missing_official_backend_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            backend = Path(tmp) / "QuantGodBackend"
            routes = backend / "Dashboard"
            routes.mkdir(parents=True)
            (routes / "phase1_api_routes.js").write_text("app.get('/api/not-documented', handler)", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/check_api_contract_matches_backend.py"),
                    "--contract",
                    str(ROOT / "docs/contracts/api-contract.json"),
                    "--backend",
                    str(backend),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("/api/not-documented", result.stdout)


if __name__ == "__main__":
    unittest.main()
