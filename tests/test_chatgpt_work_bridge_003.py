from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
import unittest.mock
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "chatgpt_work_bridge_003.py"
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

        self.required_reads = [
                "docs/governance/public_boundary.md",
                "docs/governance/chatgpt_connector_runtime_policy.md",
                "docs/atlas/control-tower/README.md",
                "docs/atlas/control-tower/local-worktree-cleanup-001.md",
                "docs/atlas/control-tower/causal-log.pause-001-handoff-2026-05-18.json",
                "docs/atlas/control-tower/batch-chatgpt-work-bridge-003.md",
                "docs/atlas/control-tower/chatgpt-work-bridge-002.local-result.json",
                "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-002-local-2026-07-13.json",
                ".github/workflows/tnv_notion_to_github.yml",
                "scripts/notion_to_github.py",
                "tests/test_notion_to_github.py",
                "scripts/preflight.py",
                "README.md",
                "SETUP_RUNBOOK.md",
                "NOTION_PROPERTIES.md",
                "config/notion_map.json",
                ".github/skills/notion-sync-workflow/SKILL.md"
        ]
        for rel in self.required_reads:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n" if path.suffix == ".json" else "baseline\n", encoding="utf-8")

        self.request = {
                "schema_version": "1.3",
                "bridge_id": "CHATGPT-WORK-BRIDGE-003",
                "created_at": "2026-07-13T00:00:00Z",
                "requested_by": "Silvan Lenhard",
                "request_actor": "chatgpt-work",
                "execution_actor": "local-codex",
                "repository_full_name": "Terra-Nova-Restore/TerraNova-s-Framework",
                "branch": "codex/chatgpt-work-bridge-003",
                "base_commit": "17ccc08a6c0b01591dcefaf26c5cfbc0043a9222",
                "status": "awaiting-local-codex",
                "mode": "controlled-code-change",
                "change_kind": "offline-validator-implementation",
                "purpose": "Add and prove a truly network-free offline validation path for the Notion-to-GitHub sync without executing or changing existing live modes.",
                "dispatch": {
                        "human_dispatch_authorized": True,
                        "authorization_scope": "manual bridge cycle 3; exact two-path implementation plus two result artifacts; do not merge",
                        "activation_mode": "manual-only",
                        "polling_enabled": False,
                        "notion_issue_intake_enabled": False,
                        "publish_gate": "PUBLISH CHATGPT-WORK-BRIDGE-003"
                },
                "runtime_constraints": {
                        "implementation_scope_exact": True,
                        "execute_offline_mode": True,
                        "execute_live_sync_modes": False,
                        "call_notion_runtime": False,
                        "call_github_issue_api": False,
                        "read_credential_values": False,
                        "dispatch_workflow": False,
                        "mutate_notion": False,
                        "mutate_tnc_watch": False
                },
                "required_reads": [
                        "docs/governance/public_boundary.md",
                        "docs/governance/chatgpt_connector_runtime_policy.md",
                        "docs/atlas/control-tower/README.md",
                        "docs/atlas/control-tower/local-worktree-cleanup-001.md",
                        "docs/atlas/control-tower/causal-log.pause-001-handoff-2026-05-18.json",
                        "docs/atlas/control-tower/batch-chatgpt-work-bridge-003.md",
                        "docs/atlas/control-tower/chatgpt-work-bridge-002.local-result.json",
                        "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-002-local-2026-07-13.json",
                        ".github/workflows/tnv_notion_to_github.yml",
                        "scripts/notion_to_github.py",
                        "tests/test_notion_to_github.py",
                        "scripts/preflight.py",
                        "README.md",
                        "SETUP_RUNBOOK.md",
                        "NOTION_PROPERTIES.md",
                        "config/notion_map.json",
                        ".github/skills/notion-sync-workflow/SKILL.md"
                ],
                "implementation_paths": [
                        "scripts/notion_to_github.py",
                        "tests/test_notion_to_github_offline.py"
                ],
                "expected_outputs": [
                        "docs/atlas/control-tower/chatgpt-work-bridge-003.local-result.json",
                        "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-003-local-2026-07-13.json"
                ],
                "expected_publication_paths": [
                        "scripts/notion_to_github.py",
                        "tests/test_notion_to_github_offline.py",
                        "docs/atlas/control-tower/chatgpt-work-bridge-003.local-result.json",
                        "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-003-local-2026-07-13.json"
                ],
                "allowed_actions": [
                        "fetch the named remote branch",
                        "use or create a non-destructive worktree",
                        "read the listed repository evidence files",
                        "modify exactly scripts/notion_to_github.py",
                        "create exactly tests/test_notion_to_github_offline.py",
                        "run the new offline-validate mode with credentials absent",
                        "run local network-refusal tests and existing non-network unit or documentation tests",
                        "create the two expected result artifacts",
                        "validate the exact four-path publication",
                        "after a separate exact publish gate, commit and push only the four expected publication paths"
                ],
                "blocked_actions": [
                        "execute scripts/notion_to_github.py in full, dry-run or validate mode",
                        "call preflight_check from the offline control path",
                        "instantiate a requests session from the offline control path",
                        "read environment variable or credential values from the offline control path",
                        "create logs, hashes, locks, shadow records or other runtime artifacts from the offline control path",
                        "intentionally change existing full, dry-run or validate semantics",
                        "modify any file outside the two implementation paths and two result artifacts",
                        "call the live Notion runtime",
                        "call the GitHub issue API as part of the implementation or validation",
                        "dispatch any workflow",
                        "push to main",
                        "merge any pull request",
                        "delete or reset worktrees",
                        "mutate Notion or Zenodo",
                        "touch TNC-WATCH files",
                        "enable background polling or a scheduler",
                        "include absolute local paths, private URLs, secrets, session content, raw token data or protected material"
                ],
                "acceptance_criteria": [
                        "offline-validate is an explicit CLI mode",
                        "the offline branch returns before setup_logging, preflight_check, credential reads and network-client construction",
                        "offline validation checks repository-local sync config and workflow structure",
                        "offline validation emits only public-safe output and creates no runtime artifacts",
                        "network-refusal tests fail if preflight_check or requests.Session is used",
                        "offline CLI succeeds with credentials absent",
                        "existing full, dry-run and validate behavior is not intentionally changed",
                        "all existing relevant tests remain green"
                ],
                "result_contract": {
                        "required_fields": [
                                "actor",
                                "base_commit_observed",
                                "blockers",
                                "branch",
                                "branch_writable",
                                "bridge_id",
                                "change_kind",
                                "config_validation_present",
                                "credential_values_read",
                                "existing_live_modes_intentionally_changed",
                                "files_published",
                                "github_issue_api_called",
                                "implementation_paths",
                                "limitations",
                                "network_guard_tests_present",
                                "notion_mutation_performed",
                                "notion_runtime_called",
                                "observed_at_utc",
                                "offline_cli_exit_code",
                                "offline_cli_passed_without_credentials",
                                "offline_mode_added",
                                "offline_mode_name",
                                "offline_output_public_safe",
                                "offline_path_precedes_live_setup",
                                "offline_run_extra_files_created",
                                "public_boundary_check",
                                "repository_full_name",
                                "request_readable",
                                "result_files_created",
                                "status",
                                "sync_live_mode_executed",
                                "terranova_worktree_count",
                                "tests_passed",
                                "tnc_watch_files_touched",
                                "validation_labels",
                                "workflow_dispatch_performed",
                                "workflow_validation_present",
                                "worktree_readable",
                                "worktree_role_labels"
                        ],
                        "status_enum": [
                                "blocked",
                                "partial",
                                "pass"
                        ],
                        "absolute_paths_allowed": False,
                        "secrets_allowed": False,
                        "private_content_allowed": False
                },
                "success_condition": "Local Codex publishes one exact four-path commit containing the offline implementation, its refusal tests and the two public-safe result artifacts; ChatGPT Work independently verifies the patch, tests and boundaries.",
                "stop_rule": "If implementation or proof requires a live API, credential value, private source, extra file or mutation outside the exact four publication paths, record a redacted blocked result and stop."
        }
        self.config = {
                "schema_version": "1.0",
                "bridge_id": "CHATGPT-WORK-BRIDGE-003",
                "activation_mode": "manual-only",
                "poll_interval_minutes": 10,
                "polling_enabled": False,
                "notion_issue_intake": {
                        "enabled": False,
                        "transport": "existing Notion to GitHub issue exporter",
                        "execute_issue_body": False
                },
                "codex_exec": {
                        "ephemeral": True,
                        "sandbox": "workspace-write",
                        "approval_policy": "never",
                        "danger_full_access": False,
                        "load_user_config": True,
                        "load_project_rules": True
                },
                "publish": {
                        "enabled_by_default": False,
                        "gate_phrase": "PUBLISH CHATGPT-WORK-BRIDGE-003",
                        "remote": "origin",
                        "branch": "codex/chatgpt-work-bridge-003",
                        "merge_allowed": False
                },
                "promotion_gate": {
                        "manual_cycles_required": 3,
                        "current_clean_cycles": 2,
                        "automatic_activation_allowed": False
                }
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

    def write_implementation(self) -> None:
        source = self.root / bridge.IMPLEMENTATION_PATHS[0]
        source.write_text(
            "VALID_MODES = {'full', 'dry-run', 'validate', 'offline-validate'}\n"
            "def offline_validate(args):\n"
            "    return {'status': 'pass'}\n"
            "def setup_logging(value):\n"
            "    return value\n"
            "def main(args):\n"
            "    if args.mode == 'offline-validate':\n"
            "        return offline_validate(args)\n"
            "    log = setup_logging(args.log)\n"
            "    return log\n",
            encoding="utf-8",
        )
        tests = self.root / bridge.IMPLEMENTATION_PATHS[1]
        tests.parent.mkdir(parents=True, exist_ok=True)
        tests.write_text(
            "import unittest\n"
            "from unittest import mock\n"
            "class OfflineTest(unittest.TestCase):\n"
            "    def test_offline_validate_refuses_network(self):\n"
            "        preflight_check = mock.Mock(side_effect=AssertionError)\n"
            "        session = mock.Mock(name='requests.Session')\n"
            "        preflight_check.assert_not_called()\n"
            "        session.assert_not_called()\n"
            "        self.assertEqual('offline-validate', 'offline-validate')\n",
            encoding="utf-8",
        )

    def valid_result(self) -> dict[str, object]:
        return {
            "bridge_id": bridge.BRIDGE_ID,
            "actor": "local-codex",
            "observed_at_utc": "2026-07-13T21:00:00Z",
            "repository_full_name": bridge.REPOSITORY_FULL_NAME,
            "branch": bridge.BRANCH,
            "base_commit_observed": "a" * 40,
            "request_readable": True,
            "worktree_readable": True,
            "branch_writable": True,
            "terranova_worktree_count": 3,
            "worktree_role_labels": ["bridge-001", "bridge-002", "bridge-003"],
            "change_kind": "offline-validator-implementation",
            "offline_mode_name": "offline-validate",
            "implementation_paths": list(bridge.IMPLEMENTATION_PATHS),
            "result_files_created": list(bridge.EXPECTED_OUTPUTS),
            "files_published": list(bridge.EXPECTED_PUBLICATION_PATHS),
            "offline_mode_added": True,
            "offline_path_precedes_live_setup": True,
            "config_validation_present": True,
            "workflow_validation_present": True,
            "network_guard_tests_present": True,
            "offline_cli_passed_without_credentials": True,
            "offline_cli_exit_code": 0,
            "offline_run_extra_files_created": False,
            "offline_output_public_safe": True,
            "existing_live_modes_intentionally_changed": False,
            "notion_runtime_called": False,
            "github_issue_api_called": False,
            "credential_values_read": False,
            "sync_live_mode_executed": False,
            "workflow_dispatch_performed": False,
            "notion_mutation_performed": False,
            "tnc_watch_files_touched": False,
            "validation_labels": ["offline-cli", "network-refusal-tests", "existing-sync-tests"],
            "tests_passed": True,
            "public_boundary_check": "pass",
            "status": "pass",
            "limitations": [],
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
            "observed_at_utc": "2026-07-13T21:00:00Z",
            "result": result["status"],
            "observation": "Exact offline validation implementation.",
            "selected_action": "Publish two implementation paths and two result artifacts.",
            "deterministic_boundary": ["No live API", "No merge"],
            "external_mutation": False,
            "blockers": [],
        }
        causal_path = self.root / bridge.EXPECTED_OUTPUTS[1]
        causal_path.write_text(json.dumps(causal), encoding="utf-8")

    def prepare_valid_change(self) -> None:
        self.write_implementation()
        self.write_results()

    def test_config_and_request_are_valid(self) -> None:
        bridge.validate_config(self.config)
        bridge.validate_request(self.request, self.root)

    def test_observe_is_ready_when_codex_exists(self) -> None:
        with unittest.mock.patch.object(bridge.shutil, "which", return_value="/safe/codex"):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "ready")

    def test_observe_blocks_without_codex(self) -> None:
        with unittest.mock.patch.object(bridge.shutil, "which", return_value=None):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "blocked")

    def test_polling_is_rejected(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["polling_enabled"] = True
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_config(config)

    def test_request_rejects_live_mode_authorization(self) -> None:
        request = json.loads(json.dumps(self.request))
        request["runtime_constraints"]["execute_live_sync_modes"] = True
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_request(request, self.root)

    def test_implementation_contract_accepts_offline_branch(self) -> None:
        self.write_implementation()
        bridge.validate_implementation(self.root)

    def test_implementation_contract_rejects_missing_network_guard(self) -> None:
        self.write_implementation()
        path = self.root / bridge.IMPLEMENTATION_PATHS[1]
        path.write_text("mode = 'offline-validate'\n", encoding="utf-8")
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_implementation(self.root)

    def test_result_contract_accepts_public_safe_change(self) -> None:
        self.prepare_valid_change()
        result, causal = bridge.validate_result_files(self.root)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(causal["result"], "pass")

    def test_result_contract_rejects_runtime_call(self) -> None:
        self.write_implementation()
        result = self.valid_result()
        result["notion_runtime_called"] = True
        result["status"] = "blocked"
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_absolute_local_path(self) -> None:
        self.write_implementation()
        result = self.valid_result()
        result["limitations"] = ["found /home/example/private-file"]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_private_notion_url(self) -> None:
        self.write_implementation()
        result = self.valid_result()
        result["limitations"] = [
            "https://app.notion.com/p/1234567890abcdef1234567890abcdef"
        ]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_codex_command_is_ephemeral_and_exact_scope(self) -> None:
        command = bridge.build_codex_command("codex", self.root)
        prompt = command[-1]
        self.assertIn("--ephemeral", command)
        self.assertIn("workspace-write", command)
        self.assertIn("offline-validate", prompt)
        self.assertIn(bridge.IMPLEMENTATION_PATHS[1], prompt)

    def test_publish_requires_exact_gate_before_git_mutation(self) -> None:
        self.prepare_valid_change()
        with self.assertRaises(bridge.BridgeError):
            bridge.publish_results(self.root, "publish please")
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        self.assertEqual(staged, "")

    def test_publish_rejects_fifth_dirty_path(self) -> None:
        self.prepare_valid_change()
        (self.root / "unexpected.txt").write_text("no\n", encoding="utf-8")
        with self.assertRaises(bridge.BridgeError):
            bridge.publish_results(self.root, bridge.PUBLISH_GATE)

    def test_request_and_config_paths_cannot_escape_repo(self) -> None:
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_path(self.root, "../outside.json", bridge.DEFAULT_REQUEST)


if __name__ == "__main__":
    unittest.main()
