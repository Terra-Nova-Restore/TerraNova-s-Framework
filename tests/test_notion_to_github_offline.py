from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "notion_to_github.py"
SCRIPTS_DIR = ROOT / "scripts"
SPEC = importlib.util.spec_from_file_location("notion_to_github_offline", SCRIPT)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(SCRIPTS_DIR))
SPEC.loader.exec_module(module)


class ForbiddenEnvironment:
    def get(self, *args, **kwargs):
        raise AssertionError("offline validation must not read environment values")

    def __getitem__(self, key):
        raise AssertionError("offline validation must not read environment values")

    def __contains__(self, key):
        raise AssertionError("offline validation must not inspect environment values")


def offline_args(runtime_root: Path, *, config: Path | str | None = None, workflow: Path | str | None = None):
    return SimpleNamespace(
        mode=module.OFFLINE_MODE,
        config=str(config or ROOT / "config" / "notion_map.json"),
        workflow=str(workflow or ROOT / ".github" / "workflows" / "tnv_notion_to_github.yml"),
        log=str(runtime_root / "logs"),
        hash_out=str(runtime_root / "hash"),
        lock_file=str(runtime_root / "sync.lock"),
        shadow=str(runtime_root / "shadow"),
    )


def run_main(args):
    output = io.StringIO()
    with redirect_stdout(output):
        exit_code = module.main(args)
    return exit_code, json.loads(output.getvalue())


class OfflineValidationTests(unittest.TestCase):
    def test_live_mode_set_is_unchanged_and_offline_mode_is_separate(self):
        self.assertEqual(module.VALID_MODES, {"full", "dry-run", "validate"})
        self.assertEqual(module.OFFLINE_MODE, "offline-validate")

    def test_offline_path_refuses_preflight_network_and_credential_reads(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp)
            args = offline_args(runtime_root)
            with mock.patch.object(
                module, "setup_logging", side_effect=AssertionError("logging forbidden")
            ) as setup_logging, mock.patch.object(
                module, "preflight_check", side_effect=AssertionError("preflight forbidden")
            ) as preflight_check, mock.patch.object(
                module.requests,
                "Session",
                side_effect=AssertionError("requests.Session forbidden"),
            ) as requests_session, mock.patch.object(
                module.os, "environ", ForbiddenEnvironment()
            ):
                exit_code, payload = run_main(args)

            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["status"], "pass")
            self.assertFalse(payload["credential_values_read"])
            self.assertFalse(payload["network_calls_performed"])
            self.assertFalse(payload["runtime_artifacts_created"])
            setup_logging.assert_not_called()
            preflight_check.assert_not_called()
            requests_session.assert_not_called()
            self.assertEqual(list(runtime_root.iterdir()), [])

    def test_offline_cli_succeeds_without_credentials_or_runtime_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime_root = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--mode",
                    "offline-validate",
                    "--config",
                    "config/notion_map.json",
                    "--workflow",
                    ".github/workflows/tnv_notion_to_github.yml",
                    "--log",
                    str(runtime_root / "logs"),
                    "--hash-out",
                    str(runtime_root / "hash"),
                    "--lock-file",
                    str(runtime_root / "sync.lock"),
                    "--shadow",
                    str(runtime_root / "shadow"),
                ],
                cwd=ROOT,
                env={"PYTHONIOENCODING": "utf-8"},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "offline-validate")
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(list(runtime_root.iterdir()), [])

    def test_offline_validation_rejects_invalid_config_public_safely(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            fixture_root = Path(tmp)
            config = fixture_root / "config.json"
            config.write_text("{}\n", encoding="utf-8")
            runtime_root = fixture_root / "runtime"
            runtime_root.mkdir()
            exit_code, payload = run_main(offline_args(runtime_root, config=config))

            self.assertEqual(exit_code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertTrue(payload["error"].startswith("CONFIG_MAPPING_INVALID:"))
            self.assertNotIn(str(fixture_root), json.dumps(payload))
            self.assertEqual(list(runtime_root.iterdir()), [])

    def test_offline_validation_rejects_invalid_workflow_public_safely(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            fixture_root = Path(tmp)
            workflow = fixture_root / "workflow.yml"
            workflow.write_text("name: incomplete\n", encoding="utf-8")
            runtime_root = fixture_root / "runtime"
            runtime_root.mkdir()
            exit_code, payload = run_main(offline_args(runtime_root, workflow=workflow))

            self.assertEqual(exit_code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertTrue(payload["error"].startswith("WORKFLOW_STRUCTURE_INVALID:"))
            self.assertNotIn(str(fixture_root), json.dumps(payload))
            self.assertEqual(list(runtime_root.iterdir()), [])

    def test_offline_validation_rejects_spoofed_workflow_snippets(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            fixture_root = Path(tmp)
            workflow = fixture_root / "workflow.yml"
            workflow.write_text(
                "name: spoofed evidence\n"
                "workflow_dispatch:\n"
                "schedule:\n"
                "- cron: \"*/10 * * * *\"\n"
                "contents: write\n"
                "issues: write\n"
                "# python scripts/notion_to_github.py\n"
                "# --config config/notion_map.json\n",
                encoding="utf-8",
            )
            runtime_root = fixture_root / "runtime"
            runtime_root.mkdir()
            exit_code, payload = run_main(offline_args(runtime_root, workflow=workflow))

            self.assertEqual(exit_code, 1)
            self.assertEqual(payload["status"], "blocked")
            self.assertTrue(payload["error"].startswith("WORKFLOW_STRUCTURE_INVALID:"))
            self.assertNotIn(str(fixture_root), json.dumps(payload))
            self.assertEqual(list(runtime_root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
