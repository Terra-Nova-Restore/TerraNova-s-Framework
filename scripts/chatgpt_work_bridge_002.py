#!/usr/bin/env python3
"""Bounded local receiver for CHATGPT-WORK-BRIDGE-002.

The receiver validates a repository-local request, can invoke ``codex exec``
with an ephemeral workspace-write sandbox, validates the two public-safe result
artifacts, and can publish only those artifacts after an exact human gate.

It is deliberately not a daemon. Polling and Notion-issue intake remain off
until separate promotion gates are satisfied.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable


BRIDGE_ID = "CHATGPT-WORK-BRIDGE-002"
REPOSITORY_FULL_NAME = "Terra-Nova-Restore/TerraNova-s-Framework"
BRANCH = "codex/chatgpt-work-bridge-002"
PUBLISH_GATE = "PUBLISH CHATGPT-WORK-BRIDGE-002"

DEFAULT_REQUEST = Path(
    "docs/atlas/control-tower/chatgpt-work-bridge-002.request.json"
)
DEFAULT_CONFIG = Path(".codex/chatgpt-work-bridge-002.json")
EXPECTED_OUTPUTS = (
    "docs/atlas/control-tower/chatgpt-work-bridge-002.local-result.json",
    "docs/atlas/control-tower/causal-log.chatgpt-work-bridge-002-local-2026-07-13.json",
)
AUDIT_EVIDENCE_FILES = (
    ".github/workflows/tnv_notion_to_github.yml",
    "scripts/notion_to_github.py",
    "tests/test_notion_to_github.py",
    "README.md",
    "SETUP_RUNBOOK.md",
    "NOTION_PROPERTIES.md",
    "config/notion_map.json",
    ".github/skills/notion-sync-workflow/SKILL.md",
)
RESULT_STATUSES = {"pass", "partial", "blocked"}
PUBLIC_BOUNDARY_STATUSES = {"pass", "blocked"}
REQUIRED_RESULT_FIELDS = {
    "bridge_id",
    "actor",
    "observed_at_utc",
    "repository_full_name",
    "branch",
    "base_commit_observed",
    "request_readable",
    "worktree_readable",
    "branch_writable",
    "terranova_worktree_count",
    "worktree_role_labels",
    "audit_kind",
    "workflow_file",
    "workflow_schedule_cron",
    "workflow_dispatch_present",
    "sync_direction",
    "export_filter_verified",
    "issue_creation_call_verified",
    "notion_writeback_verified",
    "shadow_record_write_verified",
    "notion_page_creation_call_found",
    "github_token_model",
    "separate_github_pat_required_for_actions",
    "workflow_permissions",
    "recurrence_source_assessment",
    "evidence_files",
    "validation_labels",
    "validation_passed",
    "notion_runtime_called",
    "github_issue_api_called",
    "sync_script_executed",
    "workflow_dispatch_performed",
    "notion_mutation_performed",
    "tnc_watch_files_touched",
    "public_boundary_check",
    "files_created",
    "status",
    "limitations",
    "blockers",
}
FORBIDDEN_KEYS = {
    "absolute_path",
    "absolute_paths",
    "device_id",
    "environment",
    "environment_variables",
    "hostname",
    "password",
    "session_history",
    "token_value",
    "username",
}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?:^|\s)(?:[A-Za-z]:[\\/]|\\\\[^\\\s]+[\\/]|/(?:home|Users|workspace|root|mnt|tmp|private/tmp)/)"
    ),
    re.compile(r"\b(?:ghp_|github_pat_|secret_|sk-[A-Za-z0-9])"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~-]+", re.IGNORECASE),
    re.compile(
        r"https?://(?:(?:www\.)?notion\.so/|app\.notion\.com/p/)[A-Za-z0-9_-]{20,}",
        re.IGNORECASE,
    ),
    re.compile(r"https?://[^\s]*\.notion\.site/[A-Za-z0-9_-]{20,}", re.IGNORECASE),
)


class BridgeError(RuntimeError):
    """A public-safe bridge refusal or validation failure."""


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BridgeError(f"missing JSON file: {path.as_posix()}") from exc
    except json.JSONDecodeError as exc:
        raise BridgeError(f"invalid JSON file: {path.as_posix()}") from exc
    if not isinstance(payload, dict):
        raise BridgeError(f"JSON root must be an object: {path.as_posix()}")
    return payload


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise BridgeError(f"git command failed: {' '.join(args[:2])}")
    return result


def ensure_repo_relative(path: str) -> None:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise BridgeError(f"request contains non-relative path: {path}")


def current_branch(root: Path) -> str:
    return run_git(root, "branch", "--show-current").stdout.strip()


def assert_git_repository(root: Path) -> None:
    result = run_git(root, "rev-parse", "--is-inside-work-tree", check=False)
    if result.returncode != 0 or result.stdout.strip() != "true":
        raise BridgeError("receiver must run inside a Git worktree")


def validate_config(config: dict[str, Any]) -> None:
    if config.get("bridge_id") != BRIDGE_ID:
        raise BridgeError("config bridge_id mismatch")
    if config.get("activation_mode") != "manual-only":
        raise BridgeError("initial activation must remain manual-only")
    if config.get("polling_enabled") is not False:
        raise BridgeError("polling must remain disabled for the initial trial")

    notion = config.get("notion_issue_intake")
    if not isinstance(notion, dict):
        raise BridgeError("missing notion_issue_intake config")
    if notion.get("enabled") is not False or notion.get("execute_issue_body") is not False:
        raise BridgeError("Notion issue intake must remain disabled and non-executable")

    codex = config.get("codex_exec")
    if not isinstance(codex, dict):
        raise BridgeError("missing codex_exec config")
    expected_codex = {
        "ephemeral": True,
        "sandbox": "workspace-write",
        "approval_policy": "never",
        "danger_full_access": False,
        "load_user_config": True,
        "load_project_rules": True,
    }
    for key, expected in expected_codex.items():
        if codex.get(key) != expected:
            raise BridgeError(f"unsafe or unsupported codex_exec setting: {key}")

    publish = config.get("publish")
    if not isinstance(publish, dict):
        raise BridgeError("missing publish config")
    if publish.get("enabled_by_default") is not False:
        raise BridgeError("publish must be disabled by default")
    if publish.get("gate_phrase") != PUBLISH_GATE:
        raise BridgeError("publish gate mismatch")
    if publish.get("branch") != BRANCH or publish.get("merge_allowed") is not False:
        raise BridgeError("publish boundary mismatch")

    promotion = config.get("promotion_gate")
    if not isinstance(promotion, dict):
        raise BridgeError("missing promotion_gate config")
    if promotion.get("manual_cycles_required") != 3:
        raise BridgeError("initial promotion gate requires three manual cycles")
    if promotion.get("current_clean_cycles") != 1:
        raise BridgeError("bridge 002 must start after exactly one verified clean cycle")
    if promotion.get("automatic_activation_allowed") is not False:
        raise BridgeError("automatic activation is not authorized")


def validate_request(request: dict[str, Any], root: Path) -> None:
    exact = {
        "bridge_id": BRIDGE_ID,
        "request_actor": "chatgpt-work",
        "execution_actor": "local-codex",
        "repository_full_name": REPOSITORY_FULL_NAME,
        "branch": BRANCH,
        "status": "awaiting-local-codex",
        "mode": "repository-audit-only",
    }
    for key, expected in exact.items():
        if request.get(key) != expected:
            raise BridgeError(f"request field mismatch: {key}")
    if request.get("audit_kind") != "notion-sync-reality-check":
        raise BridgeError("request audit_kind mismatch")
    expected_constraints = {
        "source_files_read_only": True,
        "execute_sync_script": False,
        "call_notion_runtime": False,
        "call_github_issue_api": False,
        "dispatch_workflow": False,
        "mutate_notion": False,
        "mutate_tnc_watch": False,
    }
    if request.get("runtime_constraints") != expected_constraints:
        raise BridgeError("request runtime constraints mismatch")

    dispatch = request.get("dispatch")
    if not isinstance(dispatch, dict):
        raise BridgeError("request is missing dispatch gate")
    if dispatch.get("human_dispatch_authorized") is not True:
        raise BridgeError("human dispatch is not authorized")
    if dispatch.get("activation_mode") != "manual-only":
        raise BridgeError("request activation must remain manual-only")
    if dispatch.get("polling_enabled") is not False:
        raise BridgeError("request polling must remain disabled")
    if dispatch.get("notion_issue_intake_enabled") is not False:
        raise BridgeError("request Notion intake must remain disabled")

    required_reads = request.get("required_reads")
    if not isinstance(required_reads, list) or not required_reads:
        raise BridgeError("request required_reads must be a non-empty list")
    for rel in required_reads:
        if not isinstance(rel, str):
            raise BridgeError("required_reads entries must be strings")
        ensure_repo_relative(rel)
        if not (root / rel).is_file():
            raise BridgeError(f"required read is missing: {rel}")
    if not set(AUDIT_EVIDENCE_FILES).issubset(set(required_reads)):
        raise BridgeError("request omits required audit evidence files")

    outputs = request.get("expected_outputs")
    if tuple(outputs or ()) != EXPECTED_OUTPUTS:
        raise BridgeError("request expected_outputs mismatch")
    for rel in EXPECTED_OUTPUTS:
        ensure_repo_relative(rel)

    contract = request.get("result_contract")
    if not isinstance(contract, dict):
        raise BridgeError("request result_contract is missing")
    if set(contract.get("required_fields") or ()) != REQUIRED_RESULT_FIELDS:
        raise BridgeError("request result required_fields mismatch")
    if set(contract.get("status_enum") or ()) != RESULT_STATUSES:
        raise BridgeError("request status_enum mismatch")
    if contract.get("absolute_paths_allowed") is not False:
        raise BridgeError("absolute paths must remain blocked")
    if contract.get("secrets_allowed") is not False:
        raise BridgeError("secrets must remain blocked")
    if contract.get("private_content_allowed") is not False:
        raise BridgeError("private content must remain blocked")


def iter_payload_items(value: Any, key: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            yield child_key, child_value
            yield from iter_payload_items(child_value, child_key)
    elif isinstance(value, list):
        for child_value in value:
            yield key, child_value
            yield from iter_payload_items(child_value, key)


def validate_public_safe_payload(payload: dict[str, Any]) -> None:
    for key, value in iter_payload_items(payload):
        if key.lower() in FORBIDDEN_KEYS:
            raise BridgeError(f"forbidden result field: {key}")
        if isinstance(value, str):
            if any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
                raise BridgeError("result contains a forbidden path, credential shape or private URL")


def validate_result_payload(payload: dict[str, Any]) -> None:
    missing = REQUIRED_RESULT_FIELDS - set(payload)
    if missing:
        raise BridgeError("result is missing required fields: " + ", ".join(sorted(missing)))
    exact = {
        "bridge_id": BRIDGE_ID,
        "actor": "local-codex",
        "repository_full_name": REPOSITORY_FULL_NAME,
        "branch": BRANCH,
        "audit_kind": "notion-sync-reality-check",
        "workflow_file": ".github/workflows/tnv_notion_to_github.yml",
    }
    for key, expected in exact.items():
        if payload.get(key) != expected:
            raise BridgeError(f"result field mismatch: {key}")
    if payload.get("status") not in RESULT_STATUSES:
        raise BridgeError("invalid result status")
    if payload.get("public_boundary_check") not in PUBLIC_BOUNDARY_STATUSES:
        raise BridgeError("invalid public_boundary_check")
    if not re.fullmatch(r"[0-9a-f]{40}", str(payload.get("base_commit_observed", ""))):
        raise BridgeError("base_commit_observed must be a full lowercase SHA-1")

    boolean_fields = (
        "request_readable",
        "worktree_readable",
        "branch_writable",
        "workflow_dispatch_present",
        "export_filter_verified",
        "issue_creation_call_verified",
        "notion_writeback_verified",
        "shadow_record_write_verified",
        "notion_page_creation_call_found",
        "separate_github_pat_required_for_actions",
        "validation_passed",
        "notion_runtime_called",
        "github_issue_api_called",
        "sync_script_executed",
        "workflow_dispatch_performed",
        "notion_mutation_performed",
        "tnc_watch_files_touched",
    )
    for key in boolean_fields:
        if not isinstance(payload.get(key), bool):
            raise BridgeError(f"result field must be boolean: {key}")

    forbidden_runtime_truths = (
        "notion_runtime_called",
        "github_issue_api_called",
        "sync_script_executed",
        "workflow_dispatch_performed",
        "notion_mutation_performed",
        "tnc_watch_files_touched",
    )
    if any(payload.get(key) is not False for key in forbidden_runtime_truths):
        raise BridgeError("result reports a prohibited runtime action or mutation")

    count = payload.get("terranova_worktree_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise BridgeError("terranova_worktree_count must be a non-negative integer")
    labels = payload.get("worktree_role_labels")
    if not isinstance(labels, list) or not all(
        isinstance(label, str) and re.fullmatch(r"[a-z0-9._-]{1,64}", label)
        for label in labels
    ):
        raise BridgeError("worktree_role_labels must contain public-safe labels")

    cron = payload.get("workflow_schedule_cron")
    if not isinstance(cron, str) or not cron or len(cron) > 64:
        raise BridgeError("workflow_schedule_cron must be a short string")
    if payload.get("sync_direction") not in {
        "notion-to-github",
        "github-to-notion",
        "bidirectional",
        "unknown",
    }:
        raise BridgeError("invalid sync_direction")
    if payload.get("github_token_model") not in {
        "actions-github-token-with-local-fallback",
        "actions-github-token",
        "separate-pat",
        "mixed",
        "unknown",
    }:
        raise BridgeError("invalid github_token_model")
    if payload.get("recurrence_source_assessment") not in {
        "outside-repository-supported",
        "repository-controlled",
        "mixed",
        "not-verifiable-from-repository",
        "unknown",
    }:
        raise BridgeError("invalid recurrence_source_assessment")

    permissions = payload.get("workflow_permissions")
    if not isinstance(permissions, list) or not all(
        isinstance(item, str) and re.fullmatch(r"[a-z0-9._:-]{1,64}", item)
        for item in permissions
    ):
        raise BridgeError("workflow_permissions must contain public-safe labels")
    if tuple(payload.get("evidence_files") or ()) != AUDIT_EVIDENCE_FILES:
        raise BridgeError("evidence_files mismatch")
    validation_labels = payload.get("validation_labels")
    if not isinstance(validation_labels, list) or not validation_labels or not all(
        isinstance(item, str) and re.fullmatch(r"[a-z0-9._:-]{1,64}", item)
        for item in validation_labels
    ):
        raise BridgeError("validation_labels must contain public-safe labels")
    if tuple(payload.get("files_created") or ()) != EXPECTED_OUTPUTS:
        raise BridgeError("files_created mismatch")
    for key in ("limitations", "blockers"):
        values = payload.get(key)
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise BridgeError(f"{key} must be a list of strings")
    if payload.get("status") == "pass":
        if payload.get("validation_passed") is not True:
            raise BridgeError("pass requires validation_passed=true")
        if payload.get("public_boundary_check") != "pass":
            raise BridgeError("pass requires public_boundary_check=pass")
    validate_public_safe_payload(payload)


def validate_causal_log(payload: dict[str, Any]) -> None:
    expected = {
        "bridge_id": BRIDGE_ID,
        "actor": "local-codex",
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise BridgeError(f"causal log field mismatch: {key}")
    if payload.get("result") not in RESULT_STATUSES:
        raise BridgeError("causal log result is invalid")
    if payload.get("external_mutation") is not False:
        raise BridgeError("causal log must precede publish and report no external mutation")
    if not isinstance(payload.get("observed_at_utc"), str):
        raise BridgeError("causal log observed_at_utc is missing")
    validate_public_safe_payload(payload)


def validate_result_files(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    result = load_json(root / EXPECTED_OUTPUTS[0])
    causal = load_json(root / EXPECTED_OUTPUTS[1])
    validate_result_payload(result)
    validate_causal_log(causal)
    if causal.get("result") != result.get("status"):
        raise BridgeError("result and causal log statuses disagree")
    return result, causal


def observe(root: Path, request: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    assert_git_repository(root)
    validate_config(config)
    validate_request(request, root)
    branch = current_branch(root)
    blockers: list[str] = []
    if branch != BRANCH:
        blockers.append("WRONG_BRANCH")
    if shutil.which("codex") is None:
        blockers.append("CODEX_CLI_NOT_FOUND")
    if not os.access(root, os.R_OK | os.W_OK):
        blockers.append("WORKTREE_NOT_READ_WRITE")
    return {
        "bridge_id": BRIDGE_ID,
        "mode": "manual-observe",
        "request_readable": True,
        "config_valid": True,
        "branch_correct": branch == BRANCH,
        "codex_cli_available": "CODEX_CLI_NOT_FOUND" not in blockers,
        "polling_enabled": False,
        "notion_issue_intake_enabled": False,
        "publish_enabled_by_default": False,
        "status": "ready" if not blockers else "blocked",
        "blockers": blockers,
    }


def build_codex_prompt() -> str:
    result_path, causal_path = EXPECTED_OUTPUTS
    return f"""Execute {BRIDGE_ID} from the repository-local request contract.

Read every file listed in {DEFAULT_REQUEST.as_posix()} before acting. Perform the
repository-only Notion sync reality check described there. Inspect source,
workflow, tests and documentation, and run only local tests that do not call a
network service.

Do not execute scripts/notion_to_github.py in full, dry-run or validate mode:
all three paths can query the live Notion runtime. Do not read credential values,
call Notion, call the GitHub issue API, dispatch a workflow, mutate Notion or
Zenodo, touch TNC-WATCH files, clean worktrees, commit, push or merge.

Create exactly these two public-safe JSON artifacts:
- {result_path}
- {causal_path}

The result artifact must contain every required field from result_contract.
Use actor "local-codex", repository "{REPOSITORY_FULL_NAME}", branch
"{BRANCH}", and a full lowercase 40-character SHA-1 for
base_commit_observed. Evidence must use only repository-relative paths and
public-safe labels. Record limitations explicitly; absence of a repository
page-creation call is evidence about this repository, not proof of current
Notion-side automation state.

The causal log must contain bridge_id, actor, observed_at_utc, result,
observation, selected_action, deterministic_boundary, external_mutation=false,
and blockers. Its result must equal the result artifact status.

If any required check would cross the public boundary or require a live API,
write status/result "blocked" with a redacted blocker and stop. Leave publishing
to the deterministic receiver.
"""


def build_codex_command(codex_bin: str, root: Path) -> list[str]:
    return [
        codex_bin,
        "--ask-for-approval",
        "never",
        "exec",
        "--ephemeral",
        "--sandbox",
        "workspace-write",
        "--cd",
        str(root),
        build_codex_prompt(),
    ]


def execute_codex(root: Path, codex_bin: str, timeout_seconds: int) -> None:
    resolved = shutil.which(codex_bin)
    if resolved is None:
        raise BridgeError("Codex CLI is not available")
    command = build_codex_command(resolved, root)
    with tempfile.TemporaryDirectory(prefix="chatgpt-work-bridge-002-") as temp_dir:
        final_message = Path(temp_dir) / "last-message.txt"
        command[-1:-1] = ["--output-last-message", str(final_message)]
        result = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    if result.returncode != 0:
        raise BridgeError(f"Codex execution failed with exit code {result.returncode}")
    validate_result_files(root)


def changed_paths(root: Path) -> set[str]:
    result = run_git(root, "status", "--porcelain=v1", "--untracked-files=all")
    paths: set[str] = set()
    for line in result.stdout.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path)
    return paths


def publish_results(root: Path, gate: str) -> str:
    if gate != PUBLISH_GATE:
        raise BridgeError("exact publish gate is required")
    assert_git_repository(root)
    if current_branch(root) != BRANCH:
        raise BridgeError("publish is allowed only from the bridge branch")
    validate_result_files(root)

    staged_before = {
        line for line in run_git(root, "diff", "--cached", "--name-only").stdout.splitlines() if line
    }
    if staged_before:
        raise BridgeError("refusing publish because unrelated staged changes exist")
    dirty = changed_paths(root)
    unexpected = dirty - set(EXPECTED_OUTPUTS)
    if unexpected:
        raise BridgeError("refusing publish because unrelated worktree changes exist")
    if dirty:
        if not set(EXPECTED_OUTPUTS).issubset(dirty):
            raise BridgeError("expected result artifacts are not both pending publication")
        run_git(root, "add", "--", *EXPECTED_OUTPUTS)
        staged = {
            line
            for line in run_git(root, "diff", "--cached", "--name-only").stdout.splitlines()
            if line
        }
        if staged != set(EXPECTED_OUTPUTS):
            raise BridgeError("staged publication scope mismatch")
        run_git(root, "commit", "-m", "docs(control-tower): record local bridge result")
    else:
        # A previous push may have failed after the exact result commit was
        # created. Permit a gated retry only when HEAD contains exactly the two
        # expected result paths.
        head_paths = {
            line
            for line in run_git(
                root, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
            ).stdout.splitlines()
            if line
        }
        if head_paths != set(EXPECTED_OUTPUTS):
            raise BridgeError("no pending or retryable exact-scope result commit found")
    commit_sha = run_git(root, "rev-parse", "HEAD").stdout.strip()
    try:
        run_git(root, "push", "origin", f"HEAD:{BRANCH}")
    except BridgeError as exc:
        raise BridgeError("local result committed but push failed; retry publish after review") from exc
    return commit_sha


def resolve_path(root: Path, value: str | None, default: Path) -> Path:
    path = root / default if value is None else Path(value)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise BridgeError("request and config paths must stay inside the repository") from exc
    return resolved


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--repo-root", help="Repository root; defaults to the script repository")
    command.add_argument("--request", help="Request JSON path relative to the repository")
    command.add_argument("--config", help="Receiver config JSON path relative to the repository")
    sub = command.add_subparsers(dest="action", required=True)

    sub.add_parser("observe", help="Validate the bridge and report readiness without mutation")

    run = sub.add_parser("run", help="Invoke Codex locally, validate outputs, and stop before publish")
    run.add_argument("--codex-bin", default="codex")
    run.add_argument("--timeout-seconds", type=int, default=1800)

    sub.add_parser("validate-result", help="Validate existing local result artifacts")

    publish = sub.add_parser("publish", help="Commit and push only validated result artifacts")
    publish.add_argument("--gate", required=True)
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.repo_root).resolve() if args.repo_root else repo_root_from_script()
    request_path = resolve_path(root, args.request, DEFAULT_REQUEST)
    config_path = resolve_path(root, args.config, DEFAULT_CONFIG)

    try:
        request = load_json(request_path)
        config = load_json(config_path)
        validate_config(config)
        validate_request(request, root)

        if args.action == "observe":
            payload = observe(root, request, config)
        elif args.action == "run":
            state = observe(root, request, config)
            if state["status"] != "ready":
                raise BridgeError("bridge is not ready: " + ", ".join(state["blockers"]))
            execute_codex(root, args.codex_bin, args.timeout_seconds)
            result, _ = validate_result_files(root)
            payload = {
                "bridge_id": BRIDGE_ID,
                "status": "local-result-ready",
                "result_status": result["status"],
                "publish_performed": False,
                "next_gate": PUBLISH_GATE,
            }
        elif args.action == "validate-result":
            result, _ = validate_result_files(root)
            payload = {
                "bridge_id": BRIDGE_ID,
                "status": "valid",
                "result_status": result["status"],
                "publish_performed": False,
            }
        else:
            commit_sha = publish_results(root, args.gate)
            payload = {
                "bridge_id": BRIDGE_ID,
                "status": "published",
                "commit_sha": commit_sha,
                "branch": BRANCH,
                "merge_performed": False,
            }
    except (BridgeError, subprocess.TimeoutExpired) as exc:
        payload = {
            "bridge_id": BRIDGE_ID,
            "status": "blocked",
            "blocker": str(exc) if isinstance(exc, BridgeError) else "Codex execution timed out",
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
