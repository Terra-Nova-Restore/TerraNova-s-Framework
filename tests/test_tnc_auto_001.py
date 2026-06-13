from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "tnc_auto_001.py"
VALIDATE_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_tnc_auto_001.py"


def load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_module():
    return load_module_from_path("tnc_auto_001", MODULE_PATH)


def load_validate_module():
    return load_module_from_path("validate_tnc_auto_001", VALIDATE_MODULE_PATH)


def init_gitignore(root: Path) -> None:
    subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
    (root / ".gitignore").write_text("raw/exports/local-private/\n", encoding="utf-8")


def write_local_lexicon(root: Path) -> Path:
    lexicon = root / "raw" / "exports" / "local-private" / "tnc-auto-001" / "lane_lexicon.local.json"
    lexicon.parent.mkdir(parents=True)
    lexicon.write_text(
        json.dumps(
            {
                "version": 1,
                "lane_patterns": {
                    "protected_ip_token": [r"\bLOCAL_PROTECTED_MARKER\b"],
                    "private_sensitive": [r"\bLOCAL_OPERATOR_MARKER\b"],
                },
                "public_blockers": {
                    "protected_ip": [r"\bLOCAL_PROTECTED_MARKER\b"],
                    "private_sensitive": [r"\bLOCAL_OPERATOR_MARKER\b"],
                    "raw_private_export": [r"\bLOCAL_RAW_MARKER\b"],
                },
                "tracked_public_deny_terms": [],
                "tracked_public_deny_paths": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return Path("raw/exports/local-private/tnc-auto-001/lane_lexicon.local.json")


class TncAuto001Tests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_classify_text_routes_private_and_github_material(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            lexicon = write_local_lexicon(root)
            counts = self.mod.classify_text(
                "Codex found #77 and GitHub branch material. LOCAL_OPERATOR_MARKER stays gated.",
                root=root,
                lexicon_path=lexicon,
            )

        self.assertGreater(counts["github_governance"], 0)
        self.assertGreater(counts["codex_internal"], 0)
        self.assertGreater(counts["private_sensitive"], 0)

    def test_boundary_counts_flags_protected_material(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            lexicon = write_local_lexicon(root)
            counts = self.mod.boundary_counts(
                "LOCAL_PROTECTED_MARKER material cannot be public.",
                root=root,
                lexicon_path=lexicon,
            )

        self.assertGreater(counts["protected_ip"], 0)

    def test_run_controller_writes_expected_outputs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"
            source_dir.mkdir(parents=True)
            lexicon = write_local_lexicon(root)
            (source_dir / "tncic-quartet-concordance-automation-closure-2026-06-04.md").write_text(
                "Codex, Notion, Gemini, GPT, #77, LOCAL_PROTECTED_MARKER, LOCAL_OPERATOR_MARKER, Zenodo",
                encoding="utf-8",
            )

            result = self.mod.run_controller(
                root,
                Path("raw/exports/local-private"),
                Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                lexicon,
            )

            self.assertEqual(result["external_mutation_count"], 0)
            self.assertFalse(result["commit_safe"])
            self.assertTrue((output_dir / "source_manifest.json").exists())
            self.assertTrue((output_dir / "claim_ledger.csv").exists())
            with (output_dir / "claim_ledger.csv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["public_safe"], "false")
            manifest = json.loads((output_dir / "source_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest), 1)

    def test_run_controller_refuses_public_output_dir_before_mkdir(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)

            with self.assertRaisesRegex(ValueError, "output directory must stay under"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("docs/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse((root / "docs" / "tnc-auto-001-dry-run").exists())

    def test_run_controller_refuses_out_of_repo_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)

            with self.assertRaisesRegex(ValueError, "output directory must stay inside repo"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("..") / "tnc-auto-outside",
                    None,
                )


class ValidateTncAuto001Tests(unittest.TestCase):
    def setUp(self):
        self.mod = load_validate_module()

    def test_blocked_network_module_preserves_dotted_names(self):
        self.assertTrue(self.mod.is_blocked_network_module("http.client"))
        self.assertTrue(self.mod.is_blocked_network_module("http.client.extra"))
        self.assertTrue(self.mod.is_blocked_network_module("urllib.request"))
        self.assertTrue(self.mod.is_blocked_network_module("requests.sessions"))
        self.assertFalse(self.mod.is_blocked_network_module("http"))
        self.assertFalse(self.mod.is_blocked_network_module("pathlib"))


if __name__ == "__main__":
    unittest.main()
