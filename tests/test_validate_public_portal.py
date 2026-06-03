from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_public_portal.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_public_portal", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidatePublicPortalTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def write_repo(self, root: Path) -> None:
        for rel_path in self.mod.REQUIRED_PUBLIC_DOCS:
            path = root / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {path.stem}\n", encoding="utf-8")

        site_index = root / self.mod.SITE_INDEX
        site_index.parent.mkdir(parents=True, exist_ok=True)
        site_index.write_text(
            "\n".join(
                [
                    "<html>",
                    "<body>",
                    *self.mod.REQUIRED_SITE_STRINGS,
                    *self.mod.REQUIRED_SITE_LINKS,
                    "</body>",
                    "</html>",
                ]
            ),
            encoding="utf-8",
        )

    def test_validate_repo_accepts_required_public_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.write_repo(repo_root)

            self.assertEqual(self.mod.validate_repo(repo_root), [])

    def test_validate_repo_rejects_placeholder_entry_pack_link(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.write_repo(repo_root)
            placeholder = repo_root / self.mod.ENTRY_PACK_LINK
            placeholder.parent.mkdir(parents=True, exist_ok=True)
            placeholder.write_text(
                "Entry Pack live route placeholder for portal CTA.",
                encoding="utf-8",
            )

            self.assertEqual(
                self.mod.validate_repo(repo_root),
                ["site/entry-pack-link.txt still contains placeholder text"],
            )

    def test_validate_repo_rejects_empty_entry_pack_link(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.write_repo(repo_root)
            entry_pack_link = repo_root / self.mod.ENTRY_PACK_LINK
            entry_pack_link.parent.mkdir(parents=True, exist_ok=True)
            entry_pack_link.write_text("  \n", encoding="utf-8")

            self.assertEqual(
                self.mod.validate_repo(repo_root),
                ["site/entry-pack-link.txt is empty"],
            )

    def test_validate_repo_rejects_non_https_entry_pack_link(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.write_repo(repo_root)
            entry_pack_link = repo_root / self.mod.ENTRY_PACK_LINK
            entry_pack_link.parent.mkdir(parents=True, exist_ok=True)
            entry_pack_link.write_text("http://example.test/entry-pack", encoding="utf-8")

            self.assertEqual(
                self.mod.validate_repo(repo_root),
                ["site/entry-pack-link.txt must contain exactly one https URL when present"],
            )

    def test_validate_repo_rejects_missing_public_document(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            self.write_repo(repo_root)
            missing_doc = repo_root / self.mod.REQUIRED_PUBLIC_DOCS[0]
            missing_doc.unlink()

            self.assertIn(
                "missing required public document: docs/public/entry_pack_architecture_v0_1.md",
                self.mod.validate_repo(repo_root),
            )


if __name__ == "__main__":
    unittest.main()
