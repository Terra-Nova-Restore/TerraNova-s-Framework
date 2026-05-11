from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_prism_atlas.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_prism_atlas", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RenderPrismAtlasTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def write_manifest(self, output_dir: Path):
        manifest = {
            "source_dir": str(self.mod.DEFAULT_SOURCE_DIR),
            "generated_at": "2026-05-07T19:19:00+00:00",
            "source_files": [
                {
                    "source": "README.md",
                    "title": "Source Pack README",
                    "type": "md",
                    "size_bytes": 42,
                    "sha256": "deadbeef",
                    "category": "source note",
                    "sensitivity": [],
                    "headings": ["Source Pack README"],
                }
            ],
            "diagrams": [],
        }
        (output_dir / "source_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def test_missing_default_source_dir_uses_manifest_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            self.mod.DEFAULT_SOURCE_DIR = output_dir / "default-source-dir"
            self.write_manifest(output_dir)

            artifacts, diagrams, source_dir, generated_at = self.mod.resolve_render_inputs(
                self.mod.DEFAULT_SOURCE_DIR,
                output_dir,
            )

            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].title, "Source Pack README")
            self.assertEqual(diagrams, [])
            self.assertEqual(source_dir, self.mod.DEFAULT_SOURCE_DIR)
            self.assertEqual(generated_at, "2026-05-07T19:19:00+00:00")

    def test_missing_explicit_source_dir_raises_instead_of_using_manifest_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            self.write_manifest(output_dir)

            with self.assertRaisesRegex(SystemExit, "Source directory not found"):
                self.mod.resolve_render_inputs(output_dir / "missing-source-dir", output_dir)


if __name__ == "__main__":
    unittest.main()
