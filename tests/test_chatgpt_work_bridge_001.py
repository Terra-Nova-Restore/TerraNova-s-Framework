from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "chatgpt_work_bridge_001.py"
SPEC = importlib.util.spec_from_file_location("bridge", SCRIPT)
assert SPEC and SPEC.loader
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


def run(*args: str, cwd: Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class BridgeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        run("git", "init", "-q", cwd=self.root)
        run("git", "config", "user.name", "Bridge Test", cwd=self.root)
        run("git", "config", "user.email", "bridge@example.invalid", cwd=self.root)
        run("git", "checkout", "-q", "-b", bridge.BRANCH, cwd=self.root)

        required_reads = [
            "docs/governance/public_boundary.md",
            "docs/governance/chatgpt_connector_runtime_policy.md",
            "docs/atlas/control-tower/README.md",
            "docs/atlas/control-tower/local-worktree-cleanup-001.md",
            "docs/atlas/control-tower/causal-log.pause-001-handoff-2026-05-18.json",
            "docs/atlas/control-tower/batch-chatgpt-work-bridge-001.md",
        ]
        for rel in required_reads:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n" if path.suffix == ".json" else "test\n", encoding="utf-8")

        self.request = {
            "schema_version": "1.1",
            "bridge_id": bridge.BRIDGE_ID,
            "created_at": "2026-07-13T00:00:00Z",
            "requested_by": "Silvan Lenhard",
            "request_actor": "chatgpt-work",
            "execution_actor": "local-codex",
            "repository_full_name": bridge.REPOSITORY_FULL_NAME,
            "branch": bridge.BRANCH,
            "base_commit": "e5ddb0e15e342593d5ead8f0e92ffd89a93463ca",
            "status": "awaiting-local-codex",
            "mode": "github-trace-only",
            "purpose": "test",
            "dispatch": {
                "human_dispatch_authorized": True,
                "authorization_scope": "reversible bridge trial; no merge",
                "activation_mode": "manual-only",
                "polling_enabled": False,
                "notion_issue_intake_enabled": False,
                "publish_gate": bridge.PUBLISH_GATE,
            },
            "required_reads": required_reads,
            "expected_outputs": list(bridge.EXPECTED_OUTPUTS),
            "allowed_actions": ["read"],
            "blocked_actions": ["merge"],
            "result_contract": {
                "required_fields": sorted(bridge.REQUIRED_RESULT_FIELDS),
                "status_enum": sorted(bridge.RESULT_STATUSES),
                "absolute_paths_allowed": False,
                "secrets_allowed": False,
                "private_content_allowed": False,
            },
            "success_condition": "test",
            "stop_rule": "stop",
        }
        self.config = {
            "schema_version": "1.0",
            "bridge_id": bridge.BRIDGE_ID,
            "activation_mode": "manual-only",
            "poll_interval_minutes": 10,
            "polling_enabled": False,
            "notion_issue_intake": {
                "enabled": False,
                "transport": "existing Notion to GitHub issue exporter",
                "execute_issue_body": False,
            },
            "codex_exec": {
                "ephemeral": True,
                "sandbox": "workspace-write",
                "approval_policy": "never",
                "danger_full_access": False,
                "load_user_config": True,
                "load_project_rules": True,
            },
            "publish": {
                "enabled_by_default": False,
                "gate_phrase": bridge.PUBLISH_GATE,
                "remote": "origin",
                "branch": bridge.BRANCH,
                "merge_allowed": False,
            },
            "promotion_gate": {
                "manual_cycles_required": 3,
                "current_clean_cycles": 0,
                "automatic_activation_allowed": False,
            },
        }
        request_path = self.root / bridge.DEFAULT_REQUEST
        request_path.parent.mkdir(parents=True, exist_ok=True)
        request_path.write_text(json.dumps(self.request), encoding="utf-8")
        config_path = self.root / bridge.DEFAULT_CONFIG
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        run("git", "add", ".", cwd=self.root)
        run("git", "commit", "-qm", "fixture", cwd=self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def valid_result(self) -> dict[str, object]:
        return {
            "bridge_id": bridge.BRIDGE_ID,
            "actor": "local-codex",
            "observed_at_utc": "2026-07-13T18:00:00Z",
            "repository_full_name": bridge.REPOSITORY_FULL_NAME,
            "branch": bridge.BRANCH,
            "base_commit_observed": "a" * 40,
            "request_readable": True,
            "worktree_readable": True,
            "branch_writable": True,
            "terranova_worktree_count": 2,
            "worktree_role_labels": ["bridge-trial", "main-baseline"],
            "public_boundary_check": "pass",
            "files_created": list(bridge.EXPECTED_OUTPUTS),
            "status": "pass",
            "blockers": [],
        }

    def write_results(self, result: dict[str, object] | None = None) -> None:
        result = result or self.valid_result()
        result_path = self.root / bridge.EXPECTED_OUTPUTS[0]
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(result), encoding="utf-8")
        causal = {
            "bridge_id": bridge.BRIDGE_ID,
            "actor": "local-codex",
            "observed_at_utc": "2026-07-13T18:00:00Z",
            "result": result["status"],
            "observation": "bounded local metadata check",
            "selected_action": "write public-safe result",
            "deterministic_boundary": ["no merge", "no Notion mutation"],
            "external_mutation": False,
            "blockers": [],
        }
        causal_path = self.root / bridge.EXPECTED_OUTPUTS[1]
        causal_path.write_text(json.dumps(causal), encoding="utf-8")

    def test_config_and_request_are_valid(self) -> None:
        bridge.validate_config(self.config)
        bridge.validate_request(self.request, self.root)

    def test_observe_is_ready_when_codex_exists(self) -> None:
        with mock.patch.object(bridge.shutil, "which", return_value="/safe/codex"):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "ready")
        self.assertFalse(state["polling_enabled"])
        self.assertFalse(state["publish_enabled_by_default"])

    def test_observe_blocks_without_codex(self) -> None:
        with mock.patch.object(bridge.shutil, "which", return_value=None):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "blocked")
        self.assertIn("CODEX_CLI_NOT_FOUND", state["blockers"])

    def test_automatic_polling_is_rejected(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["polling_enabled"] = True
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_config(config)

    def test_request_requires_human_dispatch(self) -> None:
        request = json.loads(json.dumps(self.request))
        request["dispatch"]["human_dispatch_authorized"] = False
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_request(request, self.root)

    def test_result_contract_accepts_public_safe_result(self) -> None:
        self.write_results()
        result, causal = bridge.validate_result_files(self.root)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(causal["result"], "pass")

    def test_result_contract_rejects_absolute_local_path(self) -> None:
        result = self.valid_result()
        result["blockers"] = ["found /home/example/private-file"]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_credential_shape(self) -> None:
        result = self.valid_result()
        result["blockers"] = ["secret_example"]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_private_notion_url(self) -> None:
        result = self.valid_result()
        result["blockers"] = [
            "https://app.notion.com/p/1234567890abcdef1234567890abcdef"
        ]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_codex_command_is_ephemeral_and_least_privilege(self) -> None:
        command = bridge.build_codex_command("codex", self.root)
        self.assertIn("--ephemeral", command)
        self.assertIn("workspace-write", command)
        self.assertIn("never", command)
        self.assertNotIn("danger-full-access", command)
        self.assertNotIn("--ignore-rules", command)
        self.assertNotIn("--ignore-user-config", command)

    def test_publish_requires_exact_gate_before_git_mutation(self) -> None:
        self.write_results()
        with self.assertRaises(bridge.BridgeError):
            bridge.publish_results(self.root, "los Codex")
        self.assertEqual(
            subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.root,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout,
            "",
        )

    def test_request_and_config_paths_cannot_escape_repo(self) -> None:
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_path(self.root, "../outside.json", bridge.DEFAULT_REQUEST)


if __name__ == "__main__":
    unittest.main()
