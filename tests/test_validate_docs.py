from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_docs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_docs", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateDocsTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_validate_file_requires_explicit_marker_lines(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.mod.REPO_ROOT = repo_root
            path = repo_root / "docs" / "codex" / "example.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "# Example\n\n"
                "This prose mentions Status, Source, Trace, Boundary and Mode,\n"
                "but it does not define the required marker lines.\n",
                encoding="utf-8",
            )

            errors = self.mod.validate_file(path)

            self.assertEqual(
                errors,
                [
                    "docs/codex/example.md: missing required marker(s): "
                    "Status, Source, Trace, Boundary, Mode, GitHub sync state, Notion source awareness"
                ],
            )

    def test_validate_file_accepts_explicit_marker_lines(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.mod.REPO_ROOT = repo_root
            path = repo_root / "docs" / "codex" / "example.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "# Example\n\n"
                "Status: BIZ / Example\n"
                "Source: Notion\n"
                "Trace: `docs/architecture/example.md`\n"
                "Boundary: Example boundary.\n"
                "GitHub sync state: tracked in this repository.\n"
                "Notion source awareness: required for canonical rule changes.\n"
                "Mode: BIZ\n",
                encoding="utf-8",
            )

            self.assertEqual(self.mod.validate_file(path), [])


if __name__ == "__main__":
    unittest.main()
