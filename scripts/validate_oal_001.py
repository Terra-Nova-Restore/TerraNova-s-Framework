#!/usr/bin/env python3
"""Validate OAL-001 boundaries, tests, dry-run and cross-artifact evidence."""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PACKAGE_FILES = (
    "scripts/oal_001/__init__.py",
    "scripts/oal_001/__main__.py",
    "scripts/oal_001/governor.py",
    "scripts/oal_001/observatory.py",
    "scripts/oal_001/runtime.py",
)
PYTHON_FILES = (
    *PACKAGE_FILES,
    "scripts/validate_oal_001.py",
    "tests/test_oal_001_governor.py",
    "tests/test_oal_001_runtime.py",
)
REQUIRED_FILES = (
    ".codex/safety_policy.yaml",
    ".gitignore",
    "config/oal_001.json",
    "docs/governance/oal_001_self_modification_policy.md",
    "schemas/oal_001_mutation_trace.schema.json",
    "tests/fixtures/observatory/synthetic_harmless_cycle.json",
    *PYTHON_FILES,
)
EVIDENCE_ARTIFACTS = {
    "mutation_trace.json",
    "replay_before.json",
    "replay_after.json",
    "baseline_candidate_comparison.json",
    "rollback_proof.json",
    "boundary_report.json",
    "risk_report.json",
    "source_manifest.json",
    "claim_ledger.json",
    "run_report.md",
    "test_result.json",
    "validation_complete.json",
}
EXPECTED_MUTABLE_PATHS = ["scripts/oal_001/observatory.py"]
EXPECTED_PROTECTED_PATHS = [
    ".codex",
    ".git",
    ".gitignore",
    "config/oal_001.json",
    "docs/governance",
    "raw/exports",
    "schemas/oal_001_mutation_trace.schema.json",
    "scripts/oal_001/__init__.py",
    "scripts/oal_001/__main__.py",
    "scripts/oal_001/governor.py",
    "scripts/oal_001/runtime.py",
    "scripts/validate_oal_001.py",
    "tests/test_oal_001_governor.py",
    "tests/test_oal_001_runtime.py",
]
EXPECTED_AUTHORIZING_TEST_PATHS = [
    "tests/test_oal_001_governor.py",
    "tests/test_oal_001_runtime.py",
]
EXPECTED_POLICY = {
    "policy_id": "OAL-001-GOVERNOR",
    "schema_version": "OAL-1.0",
    "mode": "local_dry_run",
    "branch_pattern": "codex/observatory-selfmod-*",
    "mutable_paths": EXPECTED_MUTABLE_PATHS,
    "protected_paths": EXPECTED_PROTECTED_PATHS,
    "authorizing_test_paths": EXPECTED_AUTHORIZING_TEST_PATHS,
    "fixture_path": "tests/fixtures/observatory/synthetic_harmless_cycle.json",
    "output_root": "raw/exports/local-private/oal-001",
    "minimum_exploration_share": 0.25,
    "external_mutation_count": 0,
    "historical_fixture_status": "unavailable",
}
EXPECTED_TRACE_FIELDS = {
    "schema_version",
    "run_id",
    "cycle_id",
    "mode",
    "base_sha",
    "branch",
    "source_state",
    "source_manifest_sha256",
    "fixture",
    "trigger",
    "hypothesis",
    "expected_effect",
    "fallback_criterion",
    "target_path",
    "changed_paths",
    "baseline_sha256",
    "candidate_sha256",
    "diff_sha256",
    "diff",
    "governor",
    "isolation",
    "replay",
    "evaluation",
    "rollback",
    "git_status",
    "external_mutation_count",
    "not_actions",
}
EXPECTED_EVALUATION_CHECKS = {
    "governor_approved",
    "baseline_deterministic",
    "candidate_deterministic",
    "baseline_expected_share",
    "candidate_expected_share",
    "exploration_floor_preserved",
    "expected_replay_delta",
    "baseline_unchanged",
    "synthetic_fixture_only",
    "external_mutation_count_zero",
    "rollback_verified",
    "managed_baseline_unchanged",
    "candidate_workspace_removed",
}
EXPECTED_SAFETY_SCALARS = {
    "default_external_mutation": "deny",
    "default_git_remote_mutation": "deny",
    "default_notion_mutation": "deny",
    "default_publication": "deny",
    "default_payment_mutation": "deny",
}
BLOCKED_NETWORK_MODULES = {"requests", "urllib", "http.client", "socket"}
FORBIDDEN_SOURCE_SNIPPETS = (
    "copytree(",
    "raw/exports/private",
    ".env",
    "os.environ",
    "exec(",
)
RUN_ID_PATTERN = re.compile(r"^OAL-001-[A-F0-9]{16}$")
MINIMUM_OAL_TEST_COUNT = 37
VALIDATOR_FIXED_GIT_READ_COMMANDS = {
    ("git", "branch", "--show-current"),
    ("git", "rev-parse", "HEAD"),
    ("git", "status", "--short", "--branch"),
}


class DuplicateJsonKeyError(ValueError):
    """Raised when evidence or control JSON contains duplicate object keys."""


def error(message: str) -> None:
    print(f"[validate-oal-001] ERROR: {message}", file=sys.stderr)


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(data: bytes) -> object:
    return json.loads(data.decode("utf-8"), object_pairs_hook=_strict_object)


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _reject_link_components(root: Path, path: Path, label: str) -> None:
    absolute_root = root.absolute()
    try:
        relative = path.absolute().relative_to(absolute_root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root") from exc
    current = absolute_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or _is_reparse_point(current):
            raise ValueError(f"{label} contains a link or reparse-point component")


def _regular_file(path: Path, root: Path, label: str) -> Path:
    _reject_link_components(root, path, label)
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError(f"{label} is missing or outside repository root") from exc
    if not resolved.is_file():
        raise ValueError(f"{label} is not a regular file")
    if resolved.stat().st_nlink > 1:
        raise ValueError(f"{label} must not be hard-linked")
    return resolved


def _read_repo_file(rel_path: str) -> bytes:
    return _regular_file(REPO_ROOT / rel_path, REPO_ROOT, rel_path).read_bytes()


def _load_repo_json(rel_path: str) -> object:
    return strict_json_bytes(_read_repo_file(rel_path))


def _blocked_network_imports(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.append(node.module)
        for module in modules:
            if any(
                module == blocked or module.startswith(f"{blocked}.")
                for blocked in BLOCKED_NETWORK_MODULES
            ):
                found.append(module)
    return sorted(set(found))


def _call_signature(argument: ast.AST) -> tuple[str, ...] | None:
    if isinstance(argument, ast.Name):
        return (f"${argument.id}",)
    if not isinstance(argument, (ast.List, ast.Tuple)):
        return None
    values: list[str] = []
    for element in argument.elts:
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            values.append(element.value)
        elif isinstance(element, ast.Name):
            values.append(f"${element.id}")
        elif isinstance(element, ast.Attribute) and isinstance(element.value, ast.Name):
            values.append(f"${element.value.id}.{element.attr}")
        else:
            return None
    return tuple(values)


def _is_process_api_name(name: str) -> bool:
    return (
        name in {"fork", "forkpty", "popen", "startfile", "system"}
        or name.startswith("exec")
        or name.startswith("posix_spawn")
        or name.startswith("spawn")
    )


def _subprocess_boundary_errors(rel_path: str, tree: ast.AST) -> list[str]:
    errors: list[str] = []
    signatures: list[tuple[str, ...] | None] = []
    parents: dict[ast.AST, ast.AST] = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess" and alias.asname not in {
                    None,
                    "subprocess",
                }:
                    errors.append(f"subprocess import alias is forbidden in {rel_path}")
                if alias.name == "os" and alias.asname not in {None, "os"}:
                    errors.append(f"os import alias is forbidden in {rel_path}")
                if alias.name == "sys" and alias.asname not in {None, "sys"}:
                    errors.append(f"sys import alias is forbidden in {rel_path}")
                if alias.name == "importlib":
                    errors.append(f"dynamic import support is forbidden in {rel_path}")
                if alias.name == "builtins":
                    errors.append(f"builtins import is forbidden in {rel_path}")
        elif isinstance(node, ast.ImportFrom):
            if node.module == "subprocess":
                errors.append(f"from-subprocess imports are forbidden in {rel_path}")
            if node.module == "os" and any(
                _is_process_api_name(alias.name) for alias in node.names
            ):
                errors.append(f"process imports from os are forbidden in {rel_path}")
            if node.module == "sys" and any(
                alias.name in {"modules", "__dict__"} for alias in node.names
            ):
                errors.append(
                    f"process-capable sys imports are forbidden in {rel_path}"
                )
            if node.module == "importlib":
                errors.append(f"dynamic import support is forbidden in {rel_path}")
            if node.module == "builtins":
                errors.append(f"builtins imports are forbidden in {rel_path}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {
                "__import__",
                "compile",
                "eval",
                "exec",
                "globals",
                "locals",
                "vars",
            }:
                errors.append(
                    f"dynamic execution or namespace access is forbidden in {rel_path}"
                )
            if (
                node.func.id == "getattr"
                and node.args
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id in {"os", "subprocess", "sys"}
            ):
                errors.append(f"indirect process API access is forbidden in {rel_path}")
        elif isinstance(node, ast.Name) and node.id == "__builtins__":
            errors.append(f"__builtins__ access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "sys"
            and node.attr in {"__dict__", "modules"}
        ):
            errors.append(f"dynamic sys namespace access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "os"
            and node.attr == "__dict__"
        ):
            errors.append(f"dynamic os namespace access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Name)
            and node.id == "subprocess"
            and isinstance(node.ctx, ast.Load)
        ):
            attribute = parents.get(node)
            direct_call = parents.get(attribute) if attribute is not None else None
            keyword = parents.get(attribute) if attribute is not None else None
            keyword_call = parents.get(keyword) if keyword is not None else None
            is_direct_run = (
                isinstance(attribute, ast.Attribute)
                and attribute.attr == "run"
                and isinstance(direct_call, ast.Call)
                and direct_call.func is attribute
            )
            is_safe_run_constant = (
                isinstance(attribute, ast.Attribute)
                and attribute.attr in {"DEVNULL", "PIPE", "STDOUT"}
                and isinstance(keyword, ast.keyword)
                and isinstance(keyword_call, ast.Call)
                and isinstance(keyword_call.func, ast.Attribute)
                and isinstance(keyword_call.func.value, ast.Name)
                and keyword_call.func.value.id == "subprocess"
                and keyword_call.func.attr == "run"
            )
            if not is_direct_run and not is_safe_run_constant:
                errors.append(f"indirect subprocess access is forbidden in {rel_path}")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        owner = node.func.value
        if isinstance(owner, ast.Name) and owner.id == "subprocess":
            if node.func.attr != "run" or not node.args:
                errors.append(f"non-allowlisted subprocess API in {rel_path}")
            else:
                signatures.append(_call_signature(node.args[0]))
        if (
            isinstance(owner, ast.Name)
            and owner.id == "os"
            and _is_process_api_name(node.func.attr)
        ):
            errors.append(f"process execution API is forbidden in {rel_path}")

    expected: dict[str, list[tuple[str, ...]]] = {
        "scripts/oal_001/__main__.py": [("$command",)],
        "scripts/oal_001/runtime.py": [
            ("git", "check-ignore", "-q", "$rel_path"),
            ("git", "status", "--short", "--branch"),
        ],
        "scripts/validate_oal_001.py": [
            ("git", "check-ignore", "-q", "$rel_path"),
            ("$command",),
            (
                "$sys.executable",
                "-m",
                "unittest",
                "tests.test_oal_001_governor",
                "tests.test_oal_001_runtime",
                "-v",
            ),
            ("$sys.executable", "-m", "scripts.oal_001", "--json"),
        ],
    }
    if signatures != expected.get(rel_path, []):
        errors.append(
            f"subprocess calls do not match the fixed read-only allowlist in {rel_path}"
        )
    if rel_path == "scripts/oal_001/__main__.py":
        fixed_commands: object | None = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "FIXED_GIT_READ_COMMANDS"
                for target in node.targets
            ):
                fixed_commands = ast.literal_eval(node.value)
        if fixed_commands != {
            ("git", "branch", "--show-current"),
            ("git", "rev-parse", "HEAD"),
        }:
            errors.append("CLI Git reads do not match the exact fixed allowlist")
    if rel_path == "scripts/validate_oal_001.py":
        fixed_commands = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name)
                and target.id == "VALIDATOR_FIXED_GIT_READ_COMMANDS"
                for target in node.targets
            ):
                fixed_commands = ast.literal_eval(node.value)
        if fixed_commands != {
            ("git", "branch", "--show-current"),
            ("git", "rev-parse", "HEAD"),
            ("git", "status", "--short", "--branch"),
        }:
            errors.append("validator Git reads do not match the exact fixed allowlist")
    return errors


def _parse_strategy_static(source: bytes) -> dict[str, float]:
    tree = ast.parse(source.decode("utf-8"), filename="observatory.py")
    assignment: ast.AST | None = None
    for index, node in enumerate(tree.body):
        if (
            index == 0
            and isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            continue
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "STRATEGY_WEIGHTS"
            and assignment is None
        ):
            assignment = node.value
            continue
        raise ValueError("mutable Observatory must contain data-only strategy weights")
    if assignment is None:
        raise ValueError("mutable Observatory is missing STRATEGY_WEIGHTS")
    value = ast.literal_eval(assignment)
    if value != {"primary": 0.75, "exploration": 0.25}:
        raise ValueError("baseline strategy weights must remain 0.75/0.25")
    return {key: float(item) for key, item in value.items()}


def _top_level_yaml_scalars(data: bytes) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    errors: list[str] = []
    for line_number, raw_line in enumerate(data.decode("utf-8").splitlines(), 1):
        if not raw_line or raw_line.lstrip().startswith("#") or raw_line[0].isspace():
            continue
        match = re.fullmatch(r"([A-Za-z0-9_]+):(?:\s*(.*))?", raw_line)
        if not match:
            errors.append(f"invalid top-level safety YAML at line {line_number}")
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in values:
            errors.append(f"duplicate top-level safety key: {key}")
        values[key] = value
    return values, errors


def git_check_ignored(rel_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", rel_path],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _git_read(command: list[str]) -> str:
    if tuple(command) not in VALIDATOR_FIXED_GIT_READ_COMMANDS:
        raise ValueError("validator Git command is outside the read-only allowlist")
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def static_errors() -> list[str]:
    errors: list[str] = []
    for rel_path in REQUIRED_FILES:
        try:
            _regular_file(REPO_ROOT / rel_path, REPO_ROOT, rel_path)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        return errors

    try:
        policy = _load_repo_json("config/oal_001.json")
        if policy != EXPECTED_POLICY:
            errors.append(
                "immutable policy does not match the exact first-slice contract"
            )
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"invalid immutable policy: {exc}")

    if not git_check_ignored(EXPECTED_POLICY["output_root"]):
        errors.append("configured local-private output root is not gitignored")

    safety, safety_errors = _top_level_yaml_scalars(
        _read_repo_file(".codex/safety_policy.yaml")
    )
    errors.extend(safety_errors)
    for key, expected in EXPECTED_SAFETY_SCALARS.items():
        if safety.get(key) != expected:
            errors.append(f"safety policy {key} must be exactly {expected}")

    for rel_path in PYTHON_FILES:
        try:
            source = _read_repo_file(rel_path).decode("utf-8")
            tree = ast.parse(source, filename=rel_path, feature_version=(3, 11))
        except (OSError, UnicodeDecodeError, SyntaxError, ValueError) as exc:
            errors.append(f"Python 3.11 grammar check failed for {rel_path}: {exc}")
            continue
        network_modules = _blocked_network_imports(tree)
        if network_modules:
            errors.append(
                f"network imports are forbidden in {rel_path}: {', '.join(network_modules)}"
            )
        if rel_path in PACKAGE_FILES:
            source_errors = [
                snippet for snippet in FORBIDDEN_SOURCE_SNIPPETS if snippet in source
            ]
            for snippet in source_errors:
                errors.append(f"forbidden source operation in {rel_path}: {snippet}")
        errors.extend(_subprocess_boundary_errors(rel_path, tree))

    try:
        _parse_strategy_static(_read_repo_file("scripts/oal_001/observatory.py"))
    except (OSError, UnicodeDecodeError, SyntaxError, ValueError) as exc:
        errors.append(f"invalid baseline mutable Observatory: {exc}")

    for rel_path in (
        "schemas/oal_001_mutation_trace.schema.json",
        "tests/fixtures/observatory/synthetic_harmless_cycle.json",
    ):
        try:
            payload = _load_repo_json(rel_path)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {rel_path}: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"JSON root must be an object in {rel_path}")

    try:
        schema = _load_repo_json("schemas/oal_001_mutation_trace.schema.json")
        if not isinstance(schema, dict):
            raise ValueError("schema root must be an object")
        if schema.get("additionalProperties") is not False:
            errors.append("trace schema must reject additional properties")
        if set(schema.get("required", [])) != EXPECTED_TRACE_FIELDS:
            errors.append(
                "trace schema required fields do not match the runtime contract"
            )
        checks_schema = schema["properties"]["evaluation"]["properties"]["checks"]
        if (
            checks_schema.get("additionalProperties") is not False
            or set(checks_schema.get("required", [])) != EXPECTED_EVALUATION_CHECKS
        ):
            errors.append("trace schema evaluation checks are not exact")
    except (KeyError, TypeError, OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"invalid trace schema structure: {exc}")
    return errors


def run_unit_tests() -> tuple[int, str, int | None, dict[str, int] | None]:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_oal_001_governor",
            "tests.test_oal_001_runtime",
            "-v",
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    count_matches = re.findall(
        r"^Ran (\d+) tests? in [^\r\n]+$", result.stdout, flags=re.MULTILINE
    )
    result_matches = re.findall(
        r"^OK(?: \(([^\r\n()]*)\))?$", result.stdout, flags=re.MULTILINE
    )
    count = int(count_matches[0]) if len(count_matches) == 1 else None
    outcome_details: dict[str, int] | None = None
    if len(result_matches) == 1:
        details = result_matches[0]
        outcome_details = {}
        if details:
            for item in details.split(", "):
                key, separator, value = item.rpartition("=")
                if (
                    not separator
                    or key
                    not in {"expected failures", "skipped", "unexpected successes"}
                    or not value.isdigit()
                    or key in outcome_details
                ):
                    outcome_details = None
                    break
                outcome_details[key] = int(value)
    return result.returncode, result.stdout, count, outcome_details


def unit_test_gate_errors(
    return_code: int,
    count: int | None,
    outcome_details: Mapping[str, int] | None,
) -> list[str]:
    errors: list[str] = []
    if return_code != 0:
        errors.append("unit test process returned a non-zero status")
    if count is None or count < MINIMUM_OAL_TEST_COUNT:
        errors.append(
            f"unit test count must be at least {MINIMUM_OAL_TEST_COUNT}, got {count}"
        )
    if outcome_details is None:
        errors.append("unit test result summary is missing or malformed")
    elif outcome_details:
        errors.append(
            "unit tests must end with a clean OK summary, got "
            + ", ".join(f"{key}={value}" for key, value in outcome_details.items())
        )
    return errors


def run_dry_run() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "scripts.oal_001", "--json"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = (
        result.stdout.strip()
        if result.returncode == 0
        else (result.stderr.strip() or result.stdout.strip())
    )
    return result.returncode, output


def _validated_output_dir(summary: Mapping[str, object]) -> Path:
    if set(summary) != {
        "run_id",
        "decision",
        "rollback_status",
        "external_mutation_count",
        "output_dir",
    }:
        raise ValueError("dry-run summary fields do not match the exact contract")
    run_id = summary.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("dry-run summary has an invalid run_id")
    if summary.get("decision") != "retain":
        raise ValueError("dry-run evaluator did not retain the harmless candidate")
    if summary.get("rollback_status") != "verified":
        raise ValueError("dry-run rollback was not verified")
    if summary.get("external_mutation_count") != 0:
        raise ValueError("dry-run external mutation count is not zero")
    expected_rel = f"{EXPECTED_POLICY['output_root']}/{run_id}"
    if summary.get("output_dir") != expected_rel:
        raise ValueError("dry-run output path is not exactly bound to its run_id")
    output_dir = REPO_ROOT / expected_rel
    _reject_link_components(REPO_ROOT, output_dir, "output directory")
    resolved = output_dir.resolve(strict=True)
    output_root = (REPO_ROOT / str(EXPECTED_POLICY["output_root"])).resolve(strict=True)
    if (
        resolved.parent != output_root
        or resolved.name != run_id
        or not resolved.is_dir()
    ):
        raise ValueError("dry-run output directory is outside the fixed evidence root")
    if not git_check_ignored(expected_rel):
        raise ValueError("dry-run output directory is not gitignored")
    return resolved


def _load_artifact_json(output_dir: Path, name: str) -> object:
    path = _regular_file(output_dir / name, REPO_ROOT, f"artifact {name}")
    return strict_json_bytes(path.read_bytes())


def _artifact_digest_map(output_dir: Path) -> dict[str, str]:
    digests: dict[str, str] = {}
    for name in sorted(EVIDENCE_ARTIFACTS - {"validation_complete.json"}):
        path = _regular_file(output_dir / name, REPO_ROOT, f"artifact {name}")
        digests[name] = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    return digests


def validate_completion_marker(output_dir: Path) -> list[str]:
    try:
        actual_names = {path.name for path in output_dir.iterdir()}
    except OSError as exc:
        return [f"could not enumerate completed artifacts: {exc}"]
    if actual_names != EVIDENCE_ARTIFACTS:
        return ["completed artifact set does not match the exact evidence contract"]
    try:
        marker = _load_artifact_json(output_dir, "validation_complete.json")
        trace = _load_artifact_json(output_dir, "mutation_trace.json")
        test_result = _load_artifact_json(output_dir, "test_result.json")
        current_digests = _artifact_digest_map(output_dir)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not verify completion marker: {exc}"]
    if not all(isinstance(item, dict) for item in (marker, trace, test_result)):
        return [
            "completion marker, mutation trace and test result must be JSON objects"
        ]
    unit_tests = test_result.get("unit_tests")
    artifact_validation = test_result.get("artifact_validation")
    semantic_pass = (
        test_result.get("schema_version") == "OAL-1.0"
        and test_result.get("run_id") == trace.get("run_id")
        and test_result.get("status") == "PASS"
        and test_result.get("evidence_complete") is True
        and test_result.get("static_checks") == {"status": "PASS"}
        and isinstance(unit_tests, dict)
        and unit_tests.get("status") == "PASS"
        and isinstance(unit_tests.get("count"), int)
        and unit_tests["count"] >= MINIMUM_OAL_TEST_COUNT
        and unit_tests.get("skipped") == 0
        and unit_tests.get("outcome_details") == {}
        and unit_tests.get("return_code") == 0
        and test_result.get("dry_run") == {"status": "PASS", "return_code": 0}
        and isinstance(artifact_validation, dict)
        and artifact_validation.get("status") == "PASS"
        and artifact_validation.get("errors") == []
        and test_result.get("external_mutation_count") == 0
    )
    expected_status = "PASS" if semantic_pass else "FAIL"
    expected = {
        "schema_version": "OAL-1.0",
        "run_id": trace.get("run_id"),
        "status": expected_status,
        "artifact_sha256": current_digests,
    }
    errors: list[str] = []
    if marker.get("status") != expected_status:
        errors.append("completion marker status does not match bound test semantics")
    if marker != expected:
        errors.append("completion marker artifact digests do not match current bytes")
    return errors


def _expected_diff(target_path: str, baseline: bytes, candidate: str) -> str:
    baseline_text = baseline.decode("utf-8")
    return "".join(
        difflib.unified_diff(
            baseline_text.splitlines(keepends=True),
            candidate.splitlines(keepends=True),
            fromfile=f"a/{target_path}",
            tofile=f"b/{target_path}",
        )
    )


def validate_artifacts(output_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        actual_names = {path.name for path in output_dir.iterdir()}
    except OSError as exc:
        return [f"could not enumerate artifacts: {exc}"]
    if actual_names != EVIDENCE_ARTIFACTS:
        missing = sorted(EVIDENCE_ARTIFACTS - actual_names)
        extra = sorted(actual_names - EVIDENCE_ARTIFACTS)
        if missing:
            errors.append("missing artifacts: " + ", ".join(missing))
        if extra:
            errors.append("unexpected artifacts: " + ", ".join(extra))
        return errors

    try:
        payload = {
            name: _load_artifact_json(output_dir, name)
            for name in EVIDENCE_ARTIFACTS
            if name.endswith(".json")
        }
        report_path = _regular_file(
            output_dir / "run_report.md", REPO_ROOT, "artifact run_report.md"
        )
        run_report = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not safely load artifacts: {exc}"]

    trace = payload["mutation_trace.json"]
    before = payload["replay_before.json"]
    after = payload["replay_after.json"]
    comparison = payload["baseline_candidate_comparison.json"]
    rollback = payload["rollback_proof.json"]
    boundary = payload["boundary_report.json"]
    risk = payload["risk_report.json"]
    manifest = payload["source_manifest.json"]
    claims = payload["claim_ledger.json"]
    test_result = payload["test_result.json"]
    completion = payload["validation_complete.json"]
    if not all(
        isinstance(item, dict)
        for item in (trace, before, after, comparison, rollback, boundary, risk)
    ):
        return ["core evidence artifacts must have JSON object roots"]

    from scripts.oal_001.governor import Governor, load_policy
    from scripts.oal_001.runtime import (
        CYCLE_ID,
        EXPECTED_EFFECT,
        FALLBACK_CRITERION,
        HYPOTHESIS,
        NOT_ACTIONS,
        TARGET_PATH,
        TRACE_REQUIRED_FIELDS,
        TRIGGER,
        ReplayHarness,
        build_harmless_patch,
        canonical_json,
        derive_run_id,
        load_fixture,
        read_managed_source,
        render_run_report,
        sha256_bytes,
        sha256_text,
        source_manifest_for_repo,
        validate_trace_payload,
    )

    errors.extend(validate_trace_payload(trace))
    if TRACE_REQUIRED_FIELDS != EXPECTED_TRACE_FIELDS:
        errors.append("runtime trace field set diverges from the bootstrap validator")

    try:
        policy = load_policy(REPO_ROOT)
        branch = _git_read(["git", "branch", "--show-current"])
        base_sha = _git_read(["git", "rev-parse", "HEAD"])
        current_status = _git_read(["git", "status", "--short", "--branch"])
        baseline_bytes = read_managed_source(REPO_ROOT, TARGET_PATH)
        baseline_sha = sha256_bytes(baseline_bytes)
        patch = build_harmless_patch(baseline_bytes.decode("utf-8"), baseline_sha)
        expected_diff = _expected_diff(
            TARGET_PATH, baseline_bytes, patch.replacement_text
        )
        candidate_bytes = patch.replacement_text.encode("utf-8")
        candidate_sha = sha256_bytes(candidate_bytes)
        fixture = load_fixture(REPO_ROOT, policy.fixture_path)
        harness = ReplayHarness(fixture)
        expected_before = harness.replay_bytes(baseline_bytes).as_dict()
        expected_after = harness.replay_bytes(candidate_bytes).as_dict()
        expected_manifest = source_manifest_for_repo(REPO_ROOT)
        manifest_sha = sha256_text(canonical_json(expected_manifest))
        governor = Governor(policy).review(patch, branch).as_dict()
    except (OSError, UnicodeDecodeError, ValueError, RuntimeError) as exc:
        return errors + [f"could not reconstruct expected evidence: {exc}"]

    trace_git = trace.get("git_status")
    if not isinstance(trace_git, dict):
        errors.append("trace git status is not an object")
        trace_git = {}
    if trace.get("branch") != branch:
        errors.append("trace branch does not match the current local branch")
    if trace.get("base_sha") != base_sha:
        errors.append("trace base SHA does not match current local HEAD")
    if (
        trace_git.get("before") != current_status
        or trace_git.get("after") != current_status
    ):
        errors.append("trace Git snapshots do not match the current worktree status")

    expected_run_id = derive_run_id(
        base_sha,
        branch,
        str(trace_git.get("before", "")),
        str(trace_git.get("after", "")),
        CYCLE_ID,
        TARGET_PATH,
        baseline_sha,
        candidate_sha,
        str(fixture["fixture_id"]),
        expected_manifest,
    )
    run_ids = {
        trace.get("run_id"),
        comparison.get("run_id"),
        rollback.get("run_id"),
        boundary.get("run_id"),
        risk.get("run_id"),
    }
    if run_ids != {expected_run_id}:
        errors.append("artifact run IDs do not equal the independently derived run ID")
    if output_dir.name != expected_run_id:
        errors.append("artifact directory leaf does not match the derived run ID")

    expected_checks = {name: True for name in EXPECTED_EVALUATION_CHECKS}
    expected_evaluation = {
        "decision": "retain",
        "reasons": ["all_first_slice_checks_passed"],
        "checks": expected_checks,
    }
    expected_comparison = {
        "run_id": expected_run_id,
        "baseline": expected_before,
        "candidate": expected_after,
        "delta": {"exploration_share": 0.05, "exploration_routes": 1},
        "evaluation": expected_evaluation,
    }
    if before != expected_before:
        errors.append("baseline replay does not match the reconstructed replay")
    if after != expected_after:
        errors.append("candidate replay does not match the reconstructed replay")
    if comparison != expected_comparison:
        errors.append(
            "baseline/candidate comparison is not derivable from replay evidence"
        )

    expected_trace_values = {
        "cycle_id": CYCLE_ID,
        "trigger": TRIGGER,
        "hypothesis": HYPOTHESIS,
        "expected_effect": EXPECTED_EFFECT,
        "fallback_criterion": FALLBACK_CRITERION,
        "target_path": TARGET_PATH,
        "changed_paths": [TARGET_PATH],
        "baseline_sha256": baseline_sha,
        "candidate_sha256": candidate_sha,
        "diff": expected_diff,
        "diff_sha256": sha256_text(expected_diff),
        "source_manifest_sha256": manifest_sha,
        "governor": governor,
        "evaluation": expected_evaluation,
        "external_mutation_count": 0,
        "not_actions": list(NOT_ACTIONS),
    }
    for key, expected in expected_trace_values.items():
        if trace.get(key) != expected:
            errors.append(f"trace {key} does not match reconstructed evidence")

    expected_rollback = {
        "status": "verified",
        "candidate_restored": True,
        "restored_sha256": baseline_sha,
        "baseline_sha256_before": baseline_sha,
        "baseline_sha256_after": baseline_sha,
        "managed_manifest_sha256_before": manifest_sha,
        "managed_manifest_sha256_after": manifest_sha,
        "baseline_unchanged": True,
        "candidate_workspace_removed": True,
        "run_id": expected_run_id,
    }
    if rollback != expected_rollback:
        errors.append("rollback proof does not match baseline and manifest hashes")
    if trace.get("rollback") != {
        "status": "verified",
        "candidate_restored": True,
        "baseline_unchanged": True,
        "candidate_workspace_removed": True,
    }:
        errors.append(
            "trace rollback summary does not match verified rollback evidence"
        )

    clean_worktree = bool(trace_git.get("clean_worktree"))
    expected_boundary_checks = {
        "governor_approved": True,
        "exact_mutable_allowlist": True,
        "candidate_workspace_removed": True,
        "running_version_overwritten": False,
        "baseline_unchanged": True,
        "candidate_source_executed": False,
        "external_mutation_count_zero": True,
        "historical_claim_fabricated": False,
        "git_status_unchanged": True,
        "clean_worktree": clean_worktree,
    }
    expected_boundary = {
        "run_id": expected_run_id,
        "status": "PASS" if clean_worktree else "PASS_PREPARED",
        "checks": expected_boundary_checks,
        "external_mutation_count": 0,
    }
    if boundary != expected_boundary:
        errors.append("boundary status and checks do not match reconstructed evidence")

    remaining_risks = [
        "No verified historical Hubble or ALMA fixture is admitted to the configured runtime slice.",
        "Candidate source is AST-parsed but not executed; executable candidate sandboxing is deferred.",
        "Broad Observatory engines, connector operations and ledger writing are not implemented.",
        "Cross-platform filesystem checks reduce but cannot eliminate check/open race conditions.",
        "A retain decision is technical evidence only and does not promote or activate the candidate.",
    ]
    if not clean_worktree:
        remaining_risks.insert(
            0,
            "Managed sources are bound by manifest but are not yet represented by the recorded Git HEAD.",
        )
    expected_risk = {
        "run_id": expected_run_id,
        "status": (
            "PASS_WITH_DEFERRED_SCOPE"
            if clean_worktree
            else "PREPARED_WITH_DEFERRED_SCOPE"
        ),
        "remaining_risks": remaining_risks,
        "deferred_scope": [
            "continuity_reader",
            "hubble_engine",
            "alma_engine",
            "evidence_classifier",
            "patch_generator",
            "ledger_writer",
            "three_controlled_cycles",
            "live_ledger_append",
        ],
    }
    if risk != expected_risk:
        errors.append(
            "risk report does not match the derived status and deferred scope"
        )
    if manifest != expected_manifest:
        errors.append("source manifest does not match current managed sources")

    expected_claims = [
        {
            "claim": "The synthetic candidate increased exploration routing by one observation.",
            "status": "technical_measurement",
            "evidence": "baseline_candidate_comparison.json",
        },
        {
            "claim": "The managed running-source manifest remained byte-identical and the candidate workspace was removed.",
            "status": "technical_measurement",
            "evidence": "rollback_proof.json",
        },
        {
            "claim": "No historical Hubble or ALMA fixture is admitted to this configured runtime slice.",
            "status": "configuration_observation",
            "evidence": "source_manifest.json",
        },
    ]
    if claims != expected_claims:
        errors.append("claim ledger does not match the narrow evidence claims")
    expected_report = render_run_report(
        trace, expected_comparison, expected_rollback, expected_boundary, expected_risk
    )
    if run_report != expected_report:
        errors.append("run report is not exactly reproducible from validated evidence")
    if test_result != {
        "schema_version": "OAL-1.0",
        "run_id": expected_run_id,
        "status": "NOT_RUN",
        "evidence_complete": False,
    }:
        errors.append("test result placeholder is stale or malformed")
    if completion != {
        "schema_version": "OAL-1.0",
        "run_id": expected_run_id,
        "status": "INCOMPLETE",
    }:
        errors.append("completion marker must remain INCOMPLETE until final validation")
    return errors


def _atomic_write_json(path: Path, payload: object) -> None:
    _regular_file(path.parent / "mutation_trace.json", REPO_ROOT, "artifact anchor")
    _reject_link_components(REPO_ROOT, path, path.name)
    if path.exists():
        _regular_file(path, REPO_ROOT, path.name)
    data = (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main(argv: list[str] | None = None) -> int:
    if argv:
        error("this validator accepts no arguments")
        return 2

    errors = static_errors()
    if errors:
        for item in errors:
            error(item)
        return 1

    test_returncode, test_output, test_count, test_outcomes = run_unit_tests()
    test_gate_errors = unit_test_gate_errors(test_returncode, test_count, test_outcomes)
    if test_gate_errors:
        error(
            "OAL-001 unit test gate failed, was incomplete or skipped coverage "
            f"(return_code={test_returncode}, count={test_count}, "
            f"minimum={MINIMUM_OAL_TEST_COUNT}, outcomes={test_outcomes})"
        )
        for item in test_gate_errors:
            error(item)
        print(test_output, file=sys.stderr)
        return 1

    dry_run_returncode, dry_run_output = run_dry_run()
    if dry_run_returncode != 0:
        error("OAL-001 dry-run failed: " + dry_run_output)
        return 1
    try:
        summary = strict_json_bytes(dry_run_output.encode("utf-8"))
        if not isinstance(summary, dict):
            raise ValueError("dry-run summary root must be an object")
        output_dir = _validated_output_dir(summary)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        error(f"dry-run summary is invalid: {exc}")
        return 1

    errors = validate_artifacts(output_dir)
    runtime_status = "PASS" if sys.version_info[:2] == (3, 11) else "NOT_RUN"
    test_result = {
        "schema_version": "OAL-1.0",
        "run_id": summary["run_id"],
        "status": "PASS" if not errors else "FAIL",
        "evidence_complete": not errors,
        "static_checks": {"status": "PASS"},
        "unit_tests": {
            "status": "PASS",
            "command": "python -m unittest tests.test_oal_001_governor tests.test_oal_001_runtime -v",
            "count": test_count,
            "skipped": (test_outcomes or {}).get("skipped", 0),
            "outcome_details": test_outcomes,
            "return_code": test_returncode,
        },
        "python_runtime": {
            "version": sys.version.split()[0],
            "status": "PASS",
        },
        "python_3_11_target": {
            "grammar": "PASS",
            "runtime": runtime_status,
            "reason": (
                None
                if runtime_status == "PASS"
                else "validator interpreter is not Python 3.11"
            ),
        },
        "dry_run": {"status": "PASS", "return_code": dry_run_returncode},
        "artifact_validation": {
            "status": "PASS" if not errors else "FAIL",
            "errors": errors,
        },
        "external_mutation_count": 0,
    }
    try:
        _validated_output_dir(summary)
        _atomic_write_json(output_dir / "test_result.json", test_result)
        completion = {
            "schema_version": "OAL-1.0",
            "run_id": summary["run_id"],
            "status": "PASS" if not errors else "FAIL",
            "artifact_sha256": _artifact_digest_map(output_dir),
        }
        _atomic_write_json(output_dir / "validation_complete.json", completion)
        completion_errors = validate_completion_marker(output_dir)
        errors.extend(completion_errors)
    except (OSError, ValueError) as exc:
        errors.append(f"could not atomically finalize evidence: {exc}")

    if errors:
        for item in errors:
            error(item)
        return 1

    print(
        f"[validate-oal-001] OK run_id={summary['run_id']} "
        f"tests={test_count} skipped={(test_outcomes or {}).get('skipped', 0)}"
    )
    print(f"[validate-oal-001] output_dir={summary['output_dir']}")
    print("[validate-oal-001] external_mutation_count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
