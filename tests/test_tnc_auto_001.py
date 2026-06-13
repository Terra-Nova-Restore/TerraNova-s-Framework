from __future__ import annotations

import ast
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

    def test_run_controller_refuses_empty_source_dir_before_reports(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            (root / "raw" / "exports" / "local-private").mkdir(parents=True)
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"

            with self.assertRaisesRegex(ValueError, "at least one matching local-private input"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse(output_dir.exists())

    def test_run_controller_refuses_missing_source_dir_before_reports(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"

            with self.assertRaisesRegex(ValueError, "at least one matching local-private input"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private/missing"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse(output_dir.exists())

    def test_run_controller_refuses_non_ignored_source_input_before_reports(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            (root / ".gitignore").write_text("raw/exports/local-private/tnc-auto-001-dry-run\n", encoding="utf-8")
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)
            (source_dir / "terra-nova-leak.md").write_text("Codex #77 material", encoding="utf-8")
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"

            with self.assertRaisesRegex(ValueError, "source inputs must be gitignored before reading"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse(output_dir.exists())

    def test_run_controller_refuses_source_dir_outside_local_private(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            outside = root / "logs"
            outside.mkdir(parents=True)
            (outside / "tncic-debug.md").write_text("Codex #77 log material", encoding="utf-8")
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"

            with self.assertRaisesRegex(ValueError, "source directory must stay under"):
                self.mod.run_controller(
                    root,
                    Path("logs"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse(output_dir.exists())

    def test_claim_ledger_marks_local_private_path_as_not_public_safe(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)
            output_dir = source_dir / "tnc-auto-001-dry-run"
            (source_dir / "tncic-neutral.md").write_text("A neutral note, no blocker terms.", encoding="utf-8")

            self.mod.run_controller(
                root,
                Path("raw/exports/local-private"),
                Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                None,
            )
            with (output_dir / "claim_ledger.csv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rows[0]["public_safe"], "false")

    def test_run_controller_refuses_source_symlink_escaping_local_private(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)
            tracked_target = root / "tracked-source.md"
            tracked_target.write_text("Codex #77 material", encoding="utf-8")
            source_link = source_dir / "tncic-link.md"
            try:
                source_link.symlink_to(tracked_target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            output_dir = root / "raw" / "exports" / "local-private" / "tnc-auto-001-dry-run"

            with self.assertRaisesRegex(ValueError, "source inputs must resolve under"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertFalse(output_dir.exists())

    def test_run_controller_refuses_symlinked_report_target_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            init_gitignore(root)
            source_dir = root / "raw" / "exports" / "local-private"
            source_dir.mkdir(parents=True)
            (source_dir / "tncic-neutral.md").write_text("A neutral note, no blocker terms.", encoding="utf-8")
            output_dir = source_dir / "tnc-auto-001-dry-run"
            output_dir.mkdir(parents=True)
            tracked_target = root / "tracked-report.md"
            tracked_target.write_text("keep me", encoding="utf-8")
            try:
                (output_dir / "claim_ledger.csv").symlink_to(tracked_target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            with self.assertRaisesRegex(ValueError, "report targets must not be symlinks before writing"):
                self.mod.run_controller(
                    root,
                    Path("raw/exports/local-private"),
                    Path("raw/exports/local-private/tnc-auto-001-dry-run"),
                    None,
                )

            self.assertEqual(tracked_target.read_text(encoding="utf-8"), "keep me")


class ValidateTncAuto001Tests(unittest.TestCase):
    def setUp(self):
        self.mod = load_validate_module()

    def blocked_imports(self, source: str) -> list[str]:
        return self.mod.blocked_network_imports_from_tree(ast.parse(source))

    def test_blocked_network_module_preserves_dotted_names(self):
        self.assertTrue(self.mod.is_blocked_network_module("http.client"))
        self.assertTrue(self.mod.is_blocked_network_module("http.client.extra"))
        self.assertTrue(self.mod.is_blocked_network_module("urllib.request"))
        self.assertTrue(self.mod.is_blocked_network_module("requests.sessions"))
        self.assertFalse(self.mod.is_blocked_network_module("http"))
        self.assertFalse(self.mod.is_blocked_network_module("pathlib"))

    def test_blocked_network_import_forms_are_detected(self):
        cases = {
            "import http.client\n": ["http.client"],
            "import http.client as c\n": ["http.client"],
            "from http.client import HTTPConnection\n": ["http.client"],
            "from http import client\n": ["http.client"],
            "from http import client as c\n": ["http.client"],
        }
        for source, expected in cases.items():
            with self.subTest(source=source.strip()):
                self.assertEqual(self.blocked_imports(source), expected)

    def test_blocked_network_import_forms_cover_all_configured_roots(self):
        cases = {
            "import requests\n": ["requests"],
            "import requests.sessions as sessions\n": ["requests.sessions"],
            "from requests import Session\n": ["requests"],
            "from urllib import request\n": ["urllib"],
            "from urllib.request import urlopen\n": ["urllib.request"],
            "from http import client\n": ["http.client"],
            "from http.client import HTTPConnection\n": ["http.client"],
        }
        for source, expected in cases.items():
            with self.subTest(source=source.strip()):
                self.assertEqual(self.blocked_imports(source), expected)

    def test_network_import_detector_allows_unblocked_siblings_and_relative_imports(self):
        source = "\n".join(
            [
                "import http",
                "from http import server",
                "from urllibish import request",
                "from .http import client",
                "from pathlib import Path",
            ]
        )
        self.assertEqual(self.blocked_imports(source), [])


if __name__ == "__main__":
    unittest.main()
