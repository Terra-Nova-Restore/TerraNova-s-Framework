from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "tnc_auto_001.py"


def load_module():
    spec = importlib.util.spec_from_file_location("tnc_auto_001", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TncAuto001Tests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_classify_text_routes_private_and_github_material(self):
        counts = self.mod.classify_text(
            "Codex found #77 and GitHub branch material. Metarotik stays private."
        )

        self.assertGreater(counts["github_governance"], 0)
        self.assertGreater(counts["codex_internal"], 0)
        self.assertGreater(counts["private_sensitive"], 0)

    def test_boundary_counts_flags_protected_material(self):
        counts = self.mod.boundary_counts("CAP-II and FERR token material cannot be public.")

        self.assertGreater(counts["protected_ip"], 0)

    def test_run_controller_writes_expected_outputs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source_dir = root / "raw" / "exports" / "local-private"
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"
            source_dir.mkdir(parents=True)
            (source_dir / "tncic-quartet-concordance-automation-closure-2026-06-04.md").write_text(
                "Codex, Notion, Gemini, GPT, #77, CAP-II, Metarotik, Zenodo",
                encoding="utf-8",
            )

            result = self.mod.run_controller(
                root,
                Path("raw/exports/local-private"),
                Path("raw/exports/local-private/tnc-auto-001-dry-run"),
            )

            self.assertEqual(result["external_mutation_count"], 0)
            self.assertFalse(result["commit_safe"])
            self.assertTrue((output_dir / "source_manifest.json").exists())
            self.assertTrue((output_dir / "claim_ledger.csv").exists())
            manifest = json.loads((output_dir / "source_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest), 1)


if __name__ == "__main__":
    unittest.main()
