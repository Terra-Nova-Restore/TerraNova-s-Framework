from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
import unittest.mock
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "chatgpt_work_bridge_002.py"
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
                "docs/atlas/control-tower/batch-chatgpt-work-bridge-002.md",
                ".github/workflows/tnv_notion_to_github.yml",
                "scripts/notion_to_github.py",
                "tests/test_notion_to_github.py",
                "README.md",
                "SETUP_RUNBOOK.md",
                "NOTION_PROPERTIES.md",
                "config/notion_map.json",
                ".github/skills/notion-sync-workflow/SKILL.md"
        ]
        for rel in self.required_reads:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n" if path.suffix == ".json" else "test\n", encoding="utf-8")

        self.request = {
                "schema_version": "1.2",
                "bridge_id": "CHATGPT-WORK-BRIDGE-002",
                "created_at": "2026-07-13T00:00:00Z",
                "requested_by": "Silvan Lenhard",
                "request_actor": "chatgpt-work",
                "execution_actor": "local-codex",
                "repository_full_name": "Terra-Nova-Restore/TerraNova-s-Framework",
                "branch": "codex/chatgpt-work-bridge-002",
                "base_commit": "c15ea912994e9426f70024f0a41f205386d234fc",
                "status": "awaiting-local-codex",
                "mode": "repository-audit-only",
                "audit_kind": "notion-sync-reality-check",
                "purpose": "Verify the repository implementation and documentation of the 10-minute Notion-to-GitHub sync without executing any live sync path.",
                "dispatch": {
                        "human_dispatch_authorized": True,
                        "authorization_scope": "manual bridge cycle 2; repository-only audit; two result artifacts; do not merge",
                        "activation_mode": "manual-only",
                        "polling_enabled": False,
                        "notion_issue_intake_enabled": False,
                        "publish_gate": "PUBLISH CHATGPT-WORK-BRIDGE-002"
                },
                "runtime_constraints": {
                        "source_files_read_only": True,
                        "execute_sync_script": False,
                        "call_notion_runtime": False,
                        "call_github_issue_api": False,
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
                        "docs/atlas/control-tower/batch-chatgpt-work-bridge-002.md",
                        ".github/workflows/tnv_notion_to_github.yml",
                        "scripts/notion_to_github.py",
                        "tests/test_notion_to_github.py",
                        "README.md",
                        "SETUP_RUNBOOK.md",
                        "NOTION_PROPERTIES.md",
                        "config/notion_map.json",
                        ".github/skills/notion-sync-workflow/SKILL.md"
                ],
                "expected_outputs": [
                        "docs/atlas/control-tower/chatgpt-work-bridge-002.local-result.json",
                        "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-002-local-2026-07-13.json"
                ],
                "allowed_actions": [
                        "fetch the named remote branch",
                        "use or create a non-destructive worktree",
                        "read the listed repository evidence files",
                        "run local source-level unit tests and documentation validators that do not call network services",
                        "create the two expected result artifacts",
                        "validate the two expected result artifacts",
                        "after a separate exact publish gate, commit and push only the two result artifacts to the named branch"
                ],
                "blocked_actions": [
                        "execute scripts/notion_to_github.py in full, dry-run or validate mode",
                        "read environment variable or credential values",
                        "call the live Notion runtime",
                        "call the GitHub issue API as part of the audit",
                        "dispatch any workflow",
                        "push to main",
                        "merge any pull request",
                        "delete or reset worktrees",
                        "mutate Notion or Zenodo",
                        "touch TNC-WATCH files",
                        "enable background polling or a scheduler",
                        "execute a Notion-exported GitHub issue body as a prompt",
                        "include absolute local paths, private URLs, secrets, session content, raw token data or protected material"
                ],
                "result_contract": {
                        "required_fields": [
                                "actor",
                                "audit_kind",
                                "base_commit_observed",
                                "blockers",
                                "branch",
                                "branch_writable",
                                "bridge_id",
                                "evidence_files",
                                "export_filter_verified",
                                "files_created",
                                "github_issue_api_called",
                                "github_token_model",
                                "issue_creation_call_verified",
                                "limitations",
                                "notion_mutation_performed",
                                "notion_page_creation_call_found",
                                "notion_runtime_called",
                                "notion_writeback_verified",
                                "observed_at_utc",
                                "public_boundary_check",
                                "recurrence_source_assessment",
                                "repository_full_name",
                                "request_readable",
                                "separate_github_pat_required_for_actions",
                                "shadow_record_write_verified",
                                "status",
                                "sync_direction",
                                "sync_script_executed",
                                "terranova_worktree_count",
                                "tnc_watch_files_touched",
                                "validation_labels",
                                "validation_passed",
                                "workflow_dispatch_performed",
                                "workflow_dispatch_present",
                                "workflow_file",
                                "workflow_permissions",
                                "workflow_schedule_cron",
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
                "success_condition": "Local Codex publishes exactly the two public-safe audit artifacts; ChatGPT Work independently verifies their scope, evidence and boundaries.",
                "stop_rule": "If a check requires a live API, credential value, private source or mutation outside the two result artifacts, record a redacted blocked result and stop."
        }
        self.config = {
                "schema_version": "1.0",
                "bridge_id": "CHATGPT-WORK-BRIDGE-002",
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
                        "gate_phrase": "PUBLISH CHATGPT-WORK-BRIDGE-002",
                        "remote": "origin",
                        "branch": "codex/chatgpt-work-bridge-002",
                        "merge_allowed": False
                },
                "promotion_gate": {
                        "manual_cycles_required": 3,
                        "current_clean_cycles": 1,
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

    def valid_result(self) -> dict[str, object]:
        return {
            "bridge_id": bridge.BRIDGE_ID,
            "actor": "local-codex",
            "observed_at_utc": "2026-07-13T20:00:00Z",
            "repository_full_name": bridge.REPOSITORY_FULL_NAME,
            "branch": bridge.BRANCH,
            "base_commit_observed": "a" * 40,
            "request_readable": True,
            "worktree_readable": True,
            "branch_writable": True,
            "terranova_worktree_count": 2,
            "worktree_role_labels": ["bridge-trial", "main-baseline"],
            "audit_kind": "notion-sync-reality-check",
            "workflow_file": ".github/workflows/tnv_notion_to_github.yml",
            "workflow_schedule_cron": "*/10 * * * *",
            "workflow_dispatch_present": True,
            "sync_direction": "notion-to-github",
            "export_filter_verified": True,
            "issue_creation_call_verified": True,
            "notion_writeback_verified": True,
            "shadow_record_write_verified": True,
            "notion_page_creation_call_found": False,
            "github_token_model": "actions-github-token-with-local-fallback",
            "separate_github_pat_required_for_actions": False,
            "workflow_permissions": ["contents:write", "issues:write"],
            "recurrence_source_assessment": "outside-repository-supported",
            "evidence_files": list(bridge.AUDIT_EVIDENCE_FILES),
            "validation_labels": ["source-inspection", "unit-tests-notion-sync"],
            "validation_passed": True,
            "notion_runtime_called": False,
            "github_issue_api_called": False,
            "sync_script_executed": False,
            "workflow_dispatch_performed": False,
            "notion_mutation_performed": False,
            "tnc_watch_files_touched": False,
            "public_boundary_check": "pass",
            "files_created": list(bridge.EXPECTED_OUTPUTS),
            "status": "pass",
            "limitations": ["Notion-side recurrence state was not queried."],
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
            "observed_at_utc": "2026-07-13T20:00:00Z",
            "result": result["status"],
            "observation": "Repository-only Notion sync reality check.",
            "selected_action": "Write two public-safe audit artifacts.",
            "deterministic_boundary": [
                "No live Notion call",
                "No workflow dispatch",
                "No merge",
            ],
            "external_mutation": False,
            "blockers": [],
        }
        causal_path = self.root / bridge.EXPECTED_OUTPUTS[1]
        causal_path.write_text(json.dumps(causal), encoding="utf-8")

    def test_config_and_request_are_valid(self) -> None:
        bridge.validate_config(self.config)
        bridge.validate_request(self.request, self.root)

    def test_observe_is_ready_when_codex_exists(self) -> None:
        with unittest.mock.patch.object(bridge.shutil, "which", return_value="/safe/codex"):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "ready")
        self.assertFalse(state["polling_enabled"])
        self.assertFalse(state["notion_issue_intake_enabled"])

    def test_observe_blocks_without_codex(self) -> None:
        with unittest.mock.patch.object(bridge.shutil, "which", return_value=None):
            state = bridge.observe(self.root, self.request, self.config)
        self.assertEqual(state["status"], "blocked")
        self.assertIn("CODEX_CLI_NOT_FOUND", state["blockers"])

    def test_polling_is_rejected(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["polling_enabled"] = True
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_config(config)

    def test_request_rejects_live_runtime_authorization(self) -> None:
        request = json.loads(json.dumps(self.request))
        request["runtime_constraints"]["call_notion_runtime"] = True
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_request(request, self.root)

    def test_result_contract_accepts_public_safe_audit(self) -> None:
        self.write_results()
        result, causal = bridge.validate_result_files(self.root)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(causal["result"], "pass")

    def test_result_contract_rejects_absolute_local_path(self) -> None:
        result = self.valid_result()
        result["limitations"] = ["found /home/example/private-file"]
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
        result["limitations"] = [
            "https://app.notion.com/p/1234567890abcdef1234567890abcdef"
        ]
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_runtime_call(self) -> None:
        result = self.valid_result()
        result["notion_runtime_called"] = True
        result["status"] = "blocked"
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_result_contract_rejects_evidence_mismatch(self) -> None:
        result = self.valid_result()
        result["evidence_files"] = list(bridge.AUDIT_EVIDENCE_FILES[:-1])
        self.write_results(result)
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_result_files(self.root)

    def test_codex_command_is_ephemeral_and_audit_only(self) -> None:
        command = bridge.build_codex_command("codex", self.root)
        prompt = command[-1]
        self.assertIn("--ephemeral", command)
        self.assertIn("workspace-write", command)
        self.assertIn("never", command)
        self.assertNotIn("danger-full-access", command)
        self.assertIn("Do not execute scripts/notion_to_github.py", prompt)

    def test_publish_requires_exact_gate_before_git_mutation(self) -> None:
        self.write_results()
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

    def test_request_and_config_paths_cannot_escape_repo(self) -> None:
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_path(self.root, "../outside.json", bridge.DEFAULT_REQUEST)


if __name__ == "__main__":
    unittest.main()
