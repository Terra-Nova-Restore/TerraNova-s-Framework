#!/usr/bin/env python3
"""Validate OAL-001 boundaries, tests, dry-run and cross-artifact evidence."""
# ruff: noqa: E402 -- isolation checks intentionally precede remaining imports

from __future__ import annotations

import sys


INTERPRETER_ISOLATED = (
    sys.flags.isolated
    and sys.flags.no_site
    and sys.flags.safe_path
    and sys.flags.dont_write_bytecode
)
if __name__ == "__main__" and not INTERPRETER_ISOLATED:
    print(
        "[validate-oal-001] ERROR: validator requires python -I -S -B",
        file=sys.stderr,
    )
    raise SystemExit(1)

import ast
import argparse
import difflib
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from importlib.machinery import all_suffixes
from pathlib import Path
from typing import Literal, Mapping


VALIDATOR_PATH = Path(__file__).resolve(strict=True)
REPO_ROOT = VALIDATOR_PATH.parents[1]
forbidden_import_roots = {
    REPO_ROOT,
    VALIDATOR_PATH.parent,
    Path.cwd().resolve(),
}
unsafe_import_path = False
for raw_path in sys.path:
    if not raw_path:
        unsafe_import_path = True
        break
    try:
        if Path(raw_path).resolve() in forbidden_import_roots:
            unsafe_import_path = True
            break
    except OSError:
        unsafe_import_path = True
        break
if __name__ == "__main__" and unsafe_import_path:
    print(
        "[validate-oal-001] ERROR: repository paths precede the isolated import boundary",
        file=sys.stderr,
    )
    raise SystemExit(1)
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))
repository_import_root_isolated = True
if sys.path.count(str(REPO_ROOT)) != 1 or sys.path[-1] != str(REPO_ROOT):
    repository_import_root_isolated = False
    if __name__ == "__main__":
        print(
            "[validate-oal-001] ERROR: repository import root is not isolated",
            file=sys.stderr,
        )
        raise SystemExit(1)
RUNTIME_ISOLATION_READY = (
    INTERPRETER_ISOLATED and not unsafe_import_path and repository_import_root_isolated
)

OAL_CI_WORKFLOW_PATH = ".github/workflows/oal-001-validate.yml"
EXPECTED_OAL_CI_WORKFLOW_SHA256 = (
    "FE26F0AEBCE82D61126AF83A17193C6E8EBCDD34A80E9B33D1E4BB00887D9725"
)
ISOLATED_UNIT_TEST_COMMAND = (
    "python -I -S -B scripts/validate_oal_001.py --_internal-unit-tests"
)
PYTHON_IMPORT_SUFFIXES = tuple(
    sorted(
        {suffix.casefold() for suffix in all_suffixes()}
        | {".py", ".pyc", ".pyd", ".pyw", ".so"},
        key=len,
        reverse=True,
    )
)
PYTHON_SHADOW_MODULES = frozenset(
    {name.casefold() for name in sys.stdlib_module_names}
    | {"sitecustomize", "usercustomize"}
)
PROTECTED_SYS_IMPORT_STATE = frozenset(
    {"__dict__", "meta_path", "modules", "path", "path_hooks", "path_importer_cache"}
)
ALLOWED_SYS_ATTRIBUTES = frozenset(
    {
        "argv",
        "dont_write_bytecode",
        "executable",
        "flags",
        "path",
        "stderr",
        "stdlib_module_names",
        "version",
        "version_info",
    }
)
EXPECTED_VALIDATOR_SYS_PATH_CONTEXTS = (
    "scan",
    "membership",
    "append",
    "count",
    "last",
)
EXPECTED_VALIDATOR_SYS_PATH_STATEMENTS = (
    """for raw_path in sys.path:
    if not raw_path:
        unsafe_import_path = True
        break
    try:
        if Path(raw_path).resolve() in forbidden_import_roots:
            unsafe_import_path = True
            break
    except OSError:
        unsafe_import_path = True
        break
""",
    """if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))
""",
    """if sys.path.count(str(REPO_ROOT)) != 1 or sys.path[-1] != str(REPO_ROOT):
    repository_import_root_isolated = False
    if __name__ == "__main__":
        print(
            "[validate-oal-001] ERROR: repository import root is not isolated",
            file=sys.stderr,
        )
        raise SystemExit(1)
""",
)
FORBIDDEN_REFLECTIVE_ATTRIBUTES = frozenset(
    {"__builtins__", "__dict__", "__getattr__", "__getattribute__", "__globals__"}
)
EXPECTED_REPARSE_POINT_GETATTR_FILES = frozenset(
    {
        "scripts/oal_001/git_read.py",
        "scripts/oal_001/governor.py",
        "scripts/oal_001/runtime.py",
        "scripts/validate_oal_001.py",
    }
)
EXPECTED_SUBPROCESS_IMPORT_FILES = frozenset(
    {
        "scripts/oal_001/git_read.py",
        "scripts/validate_oal_001.py",
    }
)
EXPECTED_REPARSE_POINT_FUNCTION_AST = ast.dump(
    ast.parse(
        """def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
""",
        feature_version=(3, 11),
    ).body[0],
    include_attributes=False,
)
PACKAGE_FILES = (
    "scripts/oal_001/__init__.py",
    "scripts/oal_001/__main__.py",
    "scripts/oal_001/git_read.py",
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
PROTECTED_IMPORT_DIRECTORIES = ("scripts", "tests", "scripts/oal_001")
PROTECTED_IMPORT_FILES = PYTHON_FILES
REQUIRED_FILES = (
    ".codex/safety_policy.yaml",
    OAL_CI_WORKFLOW_PATH,
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
    ".github/workflows/oal-001-validate.yml",
    ".gitignore",
    "config/oal_001.json",
    "docs/governance",
    "raw/exports",
    "schemas/oal_001_mutation_trace.schema.json",
    "scripts/oal_001/__init__.py",
    "scripts/oal_001/__main__.py",
    "scripts/oal_001/git_read.py",
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
MINIMUM_OAL_TEST_COUNT = 68
TARGET_PYTHON = (3, 11)
STATUS_PASS = "PASS"
STATUS_RUNTIME_GAP = "PASS_WITH_RUNTIME_GAP"
STATUS_FAIL = "FAIL"
EXIT_RUNTIME_GAP = 3
EXIT_NOT_PROMOTION_READY = 4
ArtifactSnapshot = tuple[tuple[str, bytes], ...]


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


def _module_name_from_import_path(name: str) -> str | None:
    lowered = name.casefold()
    for suffix in PYTHON_IMPORT_SUFFIXES:
        if lowered.endswith(suffix) and len(lowered) > len(suffix):
            return lowered[: -len(suffix)].split(".", 1)[0]
    return None


def _module_name_from_cached_bytecode(name: str) -> str | None:
    lowered = name.casefold()
    if not lowered.endswith(".pyc") or len(lowered) <= len(".pyc"):
        return None
    return lowered[: -len(".pyc")].split(".", 1)[0]


def _has_package_initializer(path: Path) -> bool:
    try:
        return any(
            _module_name_from_import_path(child.name) == "__init__"
            for child in path.iterdir()
            if child.is_file() or child.is_symlink() or _is_reparse_point(child)
        )
    except OSError:
        return True


def python_shadowing_errors(repo_root: Path) -> list[str]:
    """Reject import-shadowing files before any repository module is imported."""

    try:
        root = repo_root.resolve(strict=True)
    except OSError as exc:
        return [f"could not resolve Python import root: {exc}"]
    if not root.is_dir():
        return ["Python import root is not a directory"]

    layout_errors: list[str] = []
    for rel_path in PROTECTED_IMPORT_DIRECTORIES:
        path = root / rel_path
        if not path.is_dir() or path.is_symlink() or _is_reparse_point(path):
            layout_errors.append(f"invalid Python import topology: {rel_path}")

    for rel_path in PROTECTED_IMPORT_FILES:
        path = root / rel_path
        try:
            invalid_file = (
                not path.is_file()
                or path.is_symlink()
                or _is_reparse_point(path)
                or path.stat().st_nlink != 1
            )
        except OSError:
            invalid_file = True
        if invalid_file:
            layout_errors.append(f"invalid Python import topology: {rel_path}")

    protected_slots: dict[str, dict[str, str]] = {}
    for rel_path in PROTECTED_IMPORT_DIRECTORIES:
        path = Path(rel_path)
        parent = "" if path.parent.as_posix() == "." else path.parent.as_posix()
        protected_slots.setdefault(parent, {})[path.name.casefold()] = rel_path
    for rel_path in PROTECTED_IMPORT_FILES:
        path = Path(rel_path)
        parent = "" if path.parent.as_posix() == "." else path.parent.as_posix()
        protected_slots.setdefault(parent, {})[path.stem.casefold()] = rel_path

    problems: set[str] = set()
    for base_rel, expected_slots in protected_slots.items():
        base = root / base_rel
        if not base.is_dir() or base.is_symlink() or _is_reparse_point(base):
            continue
        try:
            entries = tuple(base.iterdir())
        except OSError:
            layout_errors.append(
                f"could not inspect Python import topology: {base_rel or '.'}"
            )
            continue
        for entry in entries:
            module_name = _module_name_from_import_path(entry.name)
            relative = entry.relative_to(root).as_posix()
            directory_name = entry.name.casefold()
            if base_rel in {"", "scripts"}:
                if module_name in PYTHON_SHADOW_MODULES:
                    problems.add(relative)
                if directory_name in PYTHON_SHADOW_MODULES and (
                    entry.is_symlink()
                    or _is_reparse_point(entry)
                    or (entry.is_dir() and _has_package_initializer(entry))
                ):
                    problems.add(relative)

            slot_candidates = {module_name}
            if entry.is_dir() or entry.is_symlink() or _is_reparse_point(entry):
                slot_candidates.add(directory_name)
            for slot in slot_candidates - {None}:
                expected_path = expected_slots.get(slot)
                if expected_path is not None and relative != expected_path:
                    problems.add(relative)

            if directory_name != "__pycache__":
                continue
            if entry.is_symlink() or _is_reparse_point(entry) or not entry.is_dir():
                problems.add(relative)
                continue
            try:
                cache_entries = tuple(entry.iterdir())
            except OSError:
                layout_errors.append(
                    f"could not inspect Python bytecode cache: {relative}"
                )
                continue
            for cache_entry in cache_entries:
                cached_module = _module_name_from_cached_bytecode(cache_entry.name)
                if cached_module in expected_slots:
                    problems.add(cache_entry.relative_to(root).as_posix())

    for namespace_rel in ("scripts", "tests"):
        namespace = root / namespace_rel
        if (
            not namespace.is_dir()
            or namespace.is_symlink()
            or _is_reparse_point(namespace)
        ):
            continue
        try:
            namespace_entries = tuple(namespace.iterdir())
        except OSError:
            layout_errors.append(
                f"could not inspect Python namespace topology: {namespace_rel}"
            )
            continue
        for entry in namespace_entries:
            if _module_name_from_import_path(entry.name) == "__init__":
                problems.add(entry.relative_to(root).as_posix())

    return layout_errors + [
        f"forbidden Python import-shadowing path: {path}" for path in sorted(problems)
    ]


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


def _pull_request_trigger_errors(workflow_source: bytes) -> list[str]:
    try:
        lines = workflow_source.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        return [f"OAL workflow is not valid UTF-8: {exc}"]

    top_level_lines = [line for line in lines if line and not line[0].isspace()]
    if top_level_lines != [
        "name: Validate OAL-001",
        "on:",
        "permissions:",
        "jobs:",
    ]:
        return ["OAL workflow top-level mapping does not match the exact contract"]

    trigger_indexes = [index for index, line in enumerate(lines) if line == "on:"]
    if len(trigger_indexes) != 1:
        return ["OAL workflow must define exactly one top-level on block"]

    trigger_lines: list[str] = []
    for line in lines[trigger_indexes[0] + 1 :]:
        if line and not line[0].isspace():
            break
        if line.strip():
            trigger_lines.append(line)
    if trigger_lines != ["  pull_request: {}"]:
        return [
            "OAL workflow trigger must be exactly one unfiltered pull_request event"
        ]
    return []


def _pull_request_merge_base_errors(workflow_source: bytes) -> list[str]:
    try:
        workflow = workflow_source.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"OAL workflow is not valid UTF-8: {exc}"]

    exact_contract = """          merge_base="$(git merge-base --all "$OAL_BASE_SHA" "$OAL_SOURCE_SHA")"
          if [[ ! "$merge_base" =~ ^[0-9a-f]{40}$ ]]; then
            echo "Could not resolve exactly one pull-request merge base" >&2
            exit 1
          fi"""
    if workflow.count(exact_contract) != 1:
        return [
            "OAL workflow must fail closed unless exactly one pull-request merge base exists"
        ]
    return []


def _sys_import_state_attribute(node: ast.AST) -> str | None:
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "sys"
        and node.attr in PROTECTED_SYS_IMPORT_STATE
    ):
        return node.attr
    return None


def _is_repo_root_string(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "str"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "REPO_ROOT"
        and not node.keywords
    )


def _is_negative_one(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and node.operand.value == 1
    )


def _module_statement(
    node: ast.AST, parents: Mapping[ast.AST, ast.AST]
) -> ast.stmt | None:
    current = node
    parent = parents.get(current)
    while parent is not None and not isinstance(parent, ast.Module):
        current = parent
        parent = parents.get(current)
    if isinstance(current, ast.stmt) and isinstance(parent, ast.Module):
        return current
    return None


def _has_forbidden_name_binding(
    tree: ast.AST, name: str, *, allowed_import: ast.Import | None = None
) -> bool:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Name)
            and node.id == name
            and not isinstance(node.ctx, ast.Load)
        ):
            return True
        if isinstance(node, ast.arg) and node.arg == name:
            return True
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.name == name
        ):
            return True
        if isinstance(node, ast.Import):
            if node is allowed_import:
                continue
            for alias in node.names:
                if (alias.asname or alias.name.partition(".")[0]) == name:
                    return True
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*" or (alias.asname or alias.name) == name:
                    return True
        if isinstance(node, ast.ExceptHandler) and node.name == name:
            return True
        if isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name == name:
            return True
        if isinstance(node, ast.MatchMapping) and node.rest == name:
            return True
        if isinstance(node, (ast.Global, ast.Nonlocal)) and name in node.names:
            return True
    return False


def _canonical_reparse_getattr_contract(
    rel_path: str, tree: ast.AST
) -> tuple[frozenset[ast.Call], list[str]]:
    if rel_path not in EXPECTED_REPARSE_POINT_GETATTR_FILES:
        return frozenset(), []

    contract_error = (
        f"canonical reparse-point getattr contract does not match in {rel_path}"
    )
    if not isinstance(tree, ast.Module):
        return frozenset(), [contract_error]

    top_level_functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_is_reparse_point"
    ]
    all_named_functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "_is_reparse_point"
    ]
    direct_getattr_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
    ]
    stat_imports = [
        node
        for node in tree.body
        if isinstance(node, ast.Import)
        and len(node.names) == 1
        and node.names[0].name == "stat"
        and node.names[0].asname is None
    ]
    if not (
        len(top_level_functions) == 1
        and all_named_functions == top_level_functions
        and len(direct_getattr_calls) == 1
        and len(stat_imports) == 1
    ):
        return frozenset(), [contract_error]

    function = top_level_functions[0]
    call = direct_getattr_calls[0]
    stat_import = stat_imports[0]
    getattr_names = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "getattr"
    ]
    stat_names = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "stat"
    ]
    exact_call = (
        isinstance(call.func, ast.Name)
        and call.func.id == "getattr"
        and not call.keywords
        and len(call.args) == 3
        and isinstance(call.args[0], ast.Name)
        and call.args[0].id == "stat"
        and isinstance(call.args[1], ast.Constant)
        and type(call.args[1].value) is str
        and call.args[1].value == "FILE_ATTRIBUTE_REPARSE_POINT"
        and isinstance(call.args[2], ast.Constant)
        and type(call.args[2].value) is int
        and call.args[2].value == 0
    )
    contract_matches = (
        ast.dump(function, include_attributes=False)
        == EXPECTED_REPARSE_POINT_FUNCTION_AST
        and exact_call
        and len(getattr_names) == 1
        and getattr_names[0] is call.func
        and len(stat_names) == 1
        and stat_names[0] is call.args[0]
        and not _has_forbidden_name_binding(tree, "getattr")
        and not _has_forbidden_name_binding(tree, "stat", allowed_import=stat_import)
    )
    if not contract_matches:
        return frozenset(), [contract_error]
    return frozenset({call}), []


def _is_allowlisted_getattr_call(
    node: ast.Call, allowed_calls: frozenset[ast.Call]
) -> bool:
    return node in allowed_calls


def _validator_sys_path_context(
    node: ast.Attribute, parents: Mapping[ast.AST, ast.AST]
) -> str | None:
    parent = parents.get(node)
    if (
        isinstance(parent, ast.For)
        and parent.iter is node
        and isinstance(parent.target, ast.Name)
        and parent.target.id == "raw_path"
    ):
        return "scan"
    if (
        isinstance(parent, ast.Compare)
        and _is_repo_root_string(parent.left)
        and len(parent.ops) == 1
        and isinstance(parent.ops[0], ast.NotIn)
        and len(parent.comparators) == 1
        and parent.comparators[0] is node
    ):
        return "membership"
    if (
        isinstance(parent, ast.Attribute)
        and parent.value is node
        and parent.attr in {"append", "count"}
    ):
        call = parents.get(parent)
        if (
            isinstance(call, ast.Call)
            and call.func is parent
            and len(call.args) == 1
            and _is_repo_root_string(call.args[0])
            and not call.keywords
        ):
            return parent.attr
    if (
        isinstance(parent, ast.Subscript)
        and parent.value is node
        and _is_negative_one(parent.slice)
    ):
        comparison = parents.get(parent)
        if (
            isinstance(comparison, ast.Compare)
            and comparison.left is parent
            and len(comparison.ops) == 1
            and isinstance(comparison.ops[0], ast.NotEq)
            and len(comparison.comparators) == 1
            and _is_repo_root_string(comparison.comparators[0])
        ):
            return "last"
    return None


def _import_path_boundary_errors(rel_path: str, tree: ast.AST) -> list[str]:
    errors: list[str] = []
    parents: dict[ast.AST, ast.AST] = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    allowed_getattr_calls, getattr_contract_errors = (
        _canonical_reparse_getattr_contract(rel_path, tree)
    )
    errors.extend(getattr_contract_errors)
    if _has_forbidden_name_binding(tree, "getattr"):
        errors.append(f"getattr rebinding is forbidden in {rel_path}")
    import_state_references: list[ast.Attribute] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound_name = alias.asname or alias.name.partition(".")[0]
                if alias.name == "sys":
                    if alias.asname is not None:
                        errors.append(f"sys import alias is forbidden in {rel_path}")
                elif alias.name.startswith("sys.") or bound_name == "sys":
                    errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, ast.ImportFrom):
            if node.module == "sys" or (
                node.module is not None and node.module.startswith("sys.")
            ):
                errors.append(f"from-sys imports are forbidden in {rel_path}")
            if any(
                alias.name in {"*", "__dict__", "__globals__", "sys", "_sys"}
                or (alias.asname or alias.name) == "sys"
                for alias in node.names
            ):
                errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, ast.Name) and node.id == "sys":
            parent = parents.get(node)
            if not (
                isinstance(node.ctx, ast.Load)
                and isinstance(parent, ast.Attribute)
                and parent.value is node
            ):
                errors.append(f"indirect sys access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "sys"
        ):
            if not isinstance(node.ctx, ast.Load):
                errors.append(
                    f"sys attribute {node.attr!r} mutation is forbidden in {rel_path}"
                )
            elif node.attr not in ALLOWED_SYS_ATTRIBUTES:
                errors.append(f"sys attribute {node.attr!r} is forbidden in {rel_path}")
        elif isinstance(node, ast.Attribute) and node.attr in {"sys", "_sys"}:
            errors.append(f"indirect sys attribute access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Attribute)
            and node.attr in FORBIDDEN_REFLECTIVE_ATTRIBUTES
        ):
            errors.append(f"reflective attribute access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"getattr", "setattr"}
            and not _is_allowlisted_getattr_call(node, allowed_getattr_calls)
        ):
            errors.append(f"reflective attribute call is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Name)
            and node.id == "getattr"
            and isinstance(node.ctx, ast.Load)
        ):
            parent = parents.get(node)
            if not (
                isinstance(parent, ast.Call)
                and parent.func is node
                and _is_allowlisted_getattr_call(parent, allowed_getattr_calls)
            ):
                errors.append(f"indirect getattr reference is forbidden in {rel_path}")
        elif isinstance(node, ast.arg) and node.arg == "sys":
            errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == "sys":
                errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, ast.ExceptHandler) and node.name == "sys":
            errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name == "sys":
            errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, ast.MatchMapping) and node.rest == "sys":
            errors.append(f"sys rebinding is forbidden in {rel_path}")
        elif isinstance(node, (ast.Global, ast.Nonlocal)) and "sys" in node.names:
            errors.append(f"sys rebinding is forbidden in {rel_path}")

        if isinstance(node, ast.Attribute) and _sys_import_state_attribute(node):
            import_state_references.append(node)

    if rel_path != "scripts/validate_oal_001.py":
        if import_state_references:
            errors.append(f"Python import-state access is forbidden in {rel_path}")
        return sorted(set(errors))

    contexts: list[str] = []
    context_statements: dict[str, ast.stmt] = {}
    for node in sorted(
        import_state_references,
        key=lambda item: (item.lineno, item.col_offset),
    ):
        attribute = _sys_import_state_attribute(node)
        context = _validator_sys_path_context(node, parents)
        if attribute != "path" or context is None:
            errors.append(
                "validator may access sys.path only in the exact isolated bootstrap"
            )
        else:
            contexts.append(context)
            statement = _module_statement(node, parents)
            if statement is not None:
                context_statements[context] = statement
    if tuple(contexts) != EXPECTED_VALIDATOR_SYS_PATH_CONTEXTS:
        errors.append(
            "validator import path must append REPO_ROOT exactly once after interpreter paths"
        )
    elif isinstance(tree, ast.Module):
        scan_statement = context_statements.get("scan")
        membership_statement = context_statements.get("membership")
        append_statement = context_statements.get("append")
        count_statement = context_statements.get("count")
        last_statement = context_statements.get("last")
        try:
            statement_indexes = (
                tree.body.index(scan_statement),
                tree.body.index(membership_statement),
                tree.body.index(count_statement),
            )
        except ValueError:
            statement_indexes = (-1, -1, -1)
        if not (
            isinstance(scan_statement, ast.For)
            and isinstance(membership_statement, ast.If)
            and membership_statement is append_statement
            and isinstance(count_statement, ast.If)
            and count_statement is last_statement
            and len(
                {
                    id(item)
                    for item in (
                        scan_statement,
                        membership_statement,
                        count_statement,
                    )
                }
            )
            == 3
            and statement_indexes[0] < statement_indexes[1] < statement_indexes[2]
        ):
            errors.append(
                "validator sys.path bootstrap must use three ordered top-level statements"
            )
        else:
            actual_shapes = tuple(
                ast.dump(statement, include_attributes=False)
                for statement in (
                    scan_statement,
                    membership_statement,
                    count_statement,
                )
            )
            expected_shapes = tuple(
                ast.dump(
                    ast.parse(source, feature_version=(3, 11)).body[0],
                    include_attributes=False,
                )
                for source in EXPECTED_VALIDATOR_SYS_PATH_STATEMENTS
            )
            if actual_shapes != expected_shapes:
                errors.append(
                    "validator sys.path bootstrap statements do not match the exact AST contract"
                )
    return sorted(set(errors))


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
    canonical_imports = (
        [
            node
            for node in tree.body
            if isinstance(node, ast.Import)
            and len(node.names) == 1
            and node.names[0].name == "subprocess"
            and node.names[0].asname is None
        ]
        if isinstance(tree, ast.Module)
        else []
    )
    expected_import_count = int(rel_path in EXPECTED_SUBPROCESS_IMPORT_FILES)
    if len(canonical_imports) != expected_import_count:
        errors.append(
            f"canonical subprocess import contract does not match in {rel_path}"
        )
    allowed_subprocess_import = (
        canonical_imports[0]
        if expected_import_count == 1 and len(canonical_imports) == 1
        else None
    )
    if _has_forbidden_name_binding(
        tree, "subprocess", allowed_import=allowed_subprocess_import
    ):
        errors.append(f"subprocess rebinding is forbidden in {rel_path}")
    parents: dict[ast.AST, ast.AST] = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    allowed_getattr_calls, _ = _canonical_reparse_getattr_contract(rel_path, tree)
    if _has_forbidden_name_binding(tree, "getattr"):
        errors.append(f"getattr rebinding is forbidden in {rel_path}")
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
            if node.func.id == "getattr" and not _is_allowlisted_getattr_call(
                node, allowed_getattr_calls
            ):
                errors.append(f"indirect process API access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Name)
            and node.id == "getattr"
            and isinstance(node.ctx, ast.Load)
        ):
            parent = parents.get(node)
            if not (
                isinstance(parent, ast.Call)
                and parent.func is node
                and _is_allowlisted_getattr_call(parent, allowed_getattr_calls)
            ):
                errors.append(f"indirect process API access is forbidden in {rel_path}")
        elif isinstance(node, ast.Name) and node.id == "__builtins__":
            errors.append(f"__builtins__ access is forbidden in {rel_path}")
        elif (
            isinstance(node, ast.Attribute)
            and node.attr in FORBIDDEN_REFLECTIVE_ATTRIBUTES
        ):
            errors.append(f"reflective process access is forbidden in {rel_path}")
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
        "scripts/oal_001/__main__.py": [],
        "scripts/oal_001/git_read.py": [("$command",)],
        "scripts/oal_001/runtime.py": [],
        "scripts/validate_oal_001.py": [
            (
                "$sys.executable",
                "-I",
                "-S",
                "-B",
                "$VALIDATOR_PATH",
                "--_internal-unit-tests",
            ),
            (
                "$sys.executable",
                "-I",
                "-S",
                "-B",
                "$VALIDATOR_PATH",
                "--_internal-dry-run",
            ),
        ],
    }
    if signatures != expected.get(rel_path, []):
        errors.append(
            f"subprocess calls do not match the fixed read-only allowlist in {rel_path}"
        )
    if rel_path == "scripts/oal_001/git_read.py":
        fixed_commands: object | None = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "FIXED_GIT_READ_ARGUMENTS"
                for target in node.targets
            ):
                fixed_commands = ast.literal_eval(node.value)
        if fixed_commands != {
            ("branch", "--show-current"),
            ("rev-parse", "HEAD"),
            (
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--ignore-submodules=none",
                "--no-renames",
            ),
        }:
            errors.append("typed Git reads do not match the exact fixed allowlist")
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
    from scripts.oal_001.git_read import is_ignored

    return is_ignored(REPO_ROOT, rel_path)


def _git_read(command: list[str]) -> str:
    from scripts.oal_001.git_read import current_branch, head_sha, worktree_status

    readers = {
        ("git", "branch", "--show-current"): current_branch,
        ("git", "rev-parse", "HEAD"): head_sha,
        (
            "git",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--ignore-submodules=none",
            "--no-renames",
        ): worktree_status,
    }
    reader = readers.get(tuple(command))
    if reader is None:
        raise ValueError("validator Git command is outside the typed read-only API")
    return reader(REPO_ROOT)


def static_errors() -> list[str]:
    errors = python_shadowing_errors(REPO_ROOT)
    for rel_path in REQUIRED_FILES:
        try:
            _regular_file(REPO_ROOT / rel_path, REPO_ROOT, rel_path)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        return errors

    workflow_source = _read_repo_file(OAL_CI_WORKFLOW_PATH)
    normalized_workflow = workflow_source.replace(b"\r\n", b"\n")
    errors.extend(_pull_request_trigger_errors(normalized_workflow))
    errors.extend(_pull_request_merge_base_errors(normalized_workflow))
    if (
        b"\r" in normalized_workflow
        or hashlib.sha256(normalized_workflow).hexdigest().upper()
        != EXPECTED_OAL_CI_WORKFLOW_SHA256
    ):
        errors.append("OAL Python 3.11 workflow does not match the exact contract")

    try:
        policy = _load_repo_json("config/oal_001.json")
        if policy != EXPECTED_POLICY:
            errors.append(
                "immutable policy does not match the exact first-slice contract"
            )
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"invalid immutable policy: {exc}")

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
        errors.extend(_import_path_boundary_errors(rel_path, tree))

    if not errors and not git_check_ignored(str(EXPECTED_POLICY["output_root"])):
        errors.append("configured local-private output root is not gitignored")

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
        expected_git_status_snapshots = {
            "before": {
                "type": "string",
                "description": (
                    "Branch-header-free Git porcelain v1 dirty entries before "
                    "the cycle; empty means clean."
                ),
                "not": {"pattern": "(^|\\n)## "},
            },
            "after": {
                "type": "string",
                "description": (
                    "Branch-header-free Git porcelain v1 dirty entries after "
                    "the cycle; empty means clean."
                ),
                "not": {"pattern": "(^|\\n)## "},
            },
        }
        git_status_properties = schema["properties"]["git_status"]["properties"]
        if any(
            git_status_properties.get(name) != expected
            for name, expected in expected_git_status_snapshots.items()
        ):
            errors.append("trace schema Git status snapshots are not canonical")
    except (KeyError, TypeError, OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"invalid trace schema structure: {exc}")
    return errors


def _internal_unit_tests() -> int:
    import unittest

    suite = unittest.defaultTestLoader.loadTestsFromNames(
        (
            "tests.test_oal_001_governor",
            "tests.test_oal_001_runtime",
        )
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def _internal_dry_run() -> int:
    from scripts.oal_001.__main__ import main as oal_main

    return oal_main(["--json"])


def run_unit_tests() -> tuple[int, str, int | None, dict[str, int] | None]:
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-S",
            "-B",
            VALIDATOR_PATH,
            "--_internal-unit-tests",
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
        [
            sys.executable,
            "-I",
            "-S",
            "-B",
            VALIDATOR_PATH,
            "--_internal-dry-run",
        ],
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


def _artifact_set_errors(names: set[str]) -> list[str]:
    errors: list[str] = []
    missing = sorted(EVIDENCE_ARTIFACTS - names)
    extra = sorted(names - EVIDENCE_ARTIFACTS)
    if missing:
        errors.append("missing artifacts: " + ", ".join(missing))
    if extra:
        errors.append("unexpected artifacts: " + ", ".join(extra))
    return errors


def _capture_artifact_snapshot(output_dir: Path) -> ArtifactSnapshot:
    try:
        names = {path.name for path in output_dir.iterdir()}
    except OSError as exc:
        raise ValueError(f"could not enumerate artifacts: {exc}") from exc
    set_errors = _artifact_set_errors(names)
    if set_errors:
        raise ValueError("; ".join(set_errors))
    return tuple(
        (
            name,
            _regular_file(
                output_dir / name, REPO_ROOT, f"artifact {name}"
            ).read_bytes(),
        )
        for name in sorted(EVIDENCE_ARTIFACTS)
    )


def _snapshot_mapping(snapshot: ArtifactSnapshot) -> dict[str, bytes]:
    mapping = dict(snapshot)
    if len(mapping) != len(snapshot) or set(mapping) != EVIDENCE_ARTIFACTS:
        raise ValueError("artifact snapshot does not match the exact evidence contract")
    if not all(isinstance(data, bytes) for data in mapping.values()):
        raise ValueError("artifact snapshot values must be immutable bytes")
    return mapping


def _snapshot_bytes(snapshot: ArtifactSnapshot, name: str) -> bytes:
    try:
        return _snapshot_mapping(snapshot)[name]
    except KeyError as exc:
        raise ValueError(f"artifact snapshot is missing {name}") from exc


def _replace_snapshot_bytes(
    snapshot: ArtifactSnapshot, name: str, data: bytes
) -> ArtifactSnapshot:
    mapping = _snapshot_mapping(snapshot)
    if name not in mapping or not isinstance(data, bytes):
        raise ValueError("snapshot replacement must target one evidence artifact")
    mapping[name] = data
    return tuple(sorted(mapping.items()))


def _json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _artifact_digest_map(snapshot: ArtifactSnapshot) -> dict[str, str]:
    mapping = _snapshot_mapping(snapshot)
    return {
        name: hashlib.sha256(mapping[name]).hexdigest().upper()
        for name in sorted(EVIDENCE_ARTIFACTS - {"validation_complete.json"})
    }


def _load_snapshot_json(snapshot: ArtifactSnapshot, name: str) -> object:
    return strict_json_bytes(_snapshot_bytes(snapshot, name))


def _snapshot_promotion_eligible(snapshot: ArtifactSnapshot) -> bool:
    """Derive promotion eligibility only from one captured evidence snapshot."""

    try:
        trace = _load_snapshot_json(snapshot, "mutation_trace.json")
        boundary = _load_snapshot_json(snapshot, "boundary_report.json")
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return False
    if not isinstance(trace, dict) or not isinstance(boundary, dict):
        return False
    git_status = trace.get("git_status")
    return (
        boundary.get("status") == STATUS_PASS
        and trace.get("source_state") == "clean_commit"
        and isinstance(git_status, dict)
        and git_status.get("clean_worktree") is True
    )


def _validation_status(artifact_errors: list[str], runtime_status: str) -> str:
    if artifact_errors:
        return STATUS_FAIL
    if runtime_status == STATUS_PASS:
        return STATUS_PASS
    if runtime_status == "NOT_RUN":
        return STATUS_RUNTIME_GAP
    raise ValueError("Python 3.11 runtime status is invalid")


def _build_test_result(
    run_id: str,
    test_count: int,
    test_outcomes: Mapping[str, int],
    test_returncode: int,
    dry_run_returncode: int,
    artifact_errors: list[str],
    python_version: str,
    python_version_info: tuple[int, int],
    promotion_eligible: bool,
) -> dict[str, object]:
    runtime_status = STATUS_PASS if python_version_info == TARGET_PYTHON else "NOT_RUN"
    status = _validation_status(artifact_errors, runtime_status)
    promotion_ready = status == STATUS_PASS and promotion_eligible is True
    return {
        "schema_version": "OAL-1.0",
        "run_id": run_id,
        "status": status,
        "evidence_complete": promotion_ready,
        "promotion_ready": promotion_ready,
        "static_checks": {"status": STATUS_PASS},
        "unit_tests": {
            "status": STATUS_PASS,
            "command": ISOLATED_UNIT_TEST_COMMAND,
            "count": test_count,
            "skipped": test_outcomes.get("skipped", 0),
            "outcome_details": dict(test_outcomes),
            "return_code": test_returncode,
        },
        "python_runtime": {
            "version": python_version,
            "status": STATUS_PASS,
        },
        "python_3_11_target": {
            "grammar": STATUS_PASS,
            "runtime": runtime_status,
            "reason": (
                None
                if runtime_status == STATUS_PASS
                else "validator interpreter is not Python 3.11"
            ),
        },
        "dry_run": {"status": STATUS_PASS, "return_code": dry_run_returncode},
        "artifact_validation": {
            "status": STATUS_PASS if not artifact_errors else STATUS_FAIL,
            "errors": list(artifact_errors),
        },
        "external_mutation_count": 0,
    }


def _final_test_result_errors(
    test_result: object, expected_run_id: str, promotion_eligible: bool
) -> list[str]:
    if not isinstance(test_result, dict):
        return ["final test result must be a JSON object"]
    errors: list[str] = []
    expected_keys = {
        "schema_version",
        "run_id",
        "status",
        "evidence_complete",
        "promotion_ready",
        "static_checks",
        "unit_tests",
        "python_runtime",
        "python_3_11_target",
        "dry_run",
        "artifact_validation",
        "external_mutation_count",
    }
    if set(test_result) != expected_keys:
        errors.append("final test result fields do not match the exact contract")
    if test_result.get("schema_version") != "OAL-1.0":
        errors.append("final test result schema version is invalid")
    if test_result.get("run_id") != expected_run_id:
        errors.append("final test result run ID is invalid")
    if test_result.get("static_checks") != {"status": STATUS_PASS}:
        errors.append("final static-check result is not PASS")

    unit_tests = test_result.get("unit_tests")
    expected_unit_keys = {
        "status",
        "command",
        "count",
        "skipped",
        "outcome_details",
        "return_code",
    }
    if not isinstance(unit_tests, dict) or set(unit_tests) != expected_unit_keys:
        errors.append("final unit-test result fields do not match the exact contract")
    else:
        if unit_tests.get("status") != STATUS_PASS:
            errors.append("final unit-test status is not PASS")
        if unit_tests.get("command") != ISOLATED_UNIT_TEST_COMMAND:
            errors.append("final unit-test command is invalid")
        count = unit_tests.get("count")
        if not isinstance(count, int) or count < MINIMUM_OAL_TEST_COUNT:
            errors.append("final unit-test count is below the required minimum")
        if unit_tests.get("skipped") != 0:
            errors.append("final unit-test result contains skipped tests")
        if unit_tests.get("outcome_details") != {}:
            errors.append("final unit-test outcome details are not empty")
        if unit_tests.get("return_code") != 0:
            errors.append("final unit-test return code is not zero")

    python_runtime = test_result.get("python_runtime")
    target_runtime = test_result.get("python_3_11_target")
    recorded_version: tuple[int, int] | None = None
    if not isinstance(python_runtime, dict) or set(python_runtime) != {
        "version",
        "status",
    }:
        errors.append("final Python runtime fields do not match the exact contract")
    else:
        version = python_runtime.get("version")
        if not isinstance(version, str) or not re.fullmatch(
            r"\d+\.\d+\.\d+(?:[A-Za-z0-9.+-]*)?", version
        ):
            errors.append("final Python runtime version is invalid")
        else:
            major, minor, *_ = version.split(".")
            recorded_version = (int(major), int(minor))
        if python_runtime.get("status") != STATUS_PASS:
            errors.append("final Python runtime status is not PASS")
    if not isinstance(target_runtime, dict) or set(target_runtime) != {
        "grammar",
        "runtime",
        "reason",
    }:
        errors.append("Python 3.11 target fields do not match the exact contract")
        runtime_status = None
    else:
        runtime_status = target_runtime.get("runtime")
        if target_runtime.get("grammar") != STATUS_PASS:
            errors.append("Python 3.11 grammar status is not PASS")
        if runtime_status not in {STATUS_PASS, "NOT_RUN"}:
            errors.append("Python 3.11 runtime status is invalid")
        elif runtime_status == STATUS_PASS:
            if (
                recorded_version != TARGET_PYTHON
                or target_runtime.get("reason") is not None
            ):
                errors.append(
                    "Python 3.11 PASS is not supported by the recorded runtime"
                )
        elif (
            recorded_version == TARGET_PYTHON
            or target_runtime.get("reason")
            != "validator interpreter is not Python 3.11"
        ):
            errors.append("Python 3.11 NOT_RUN reason is inconsistent")

    expected_status = (
        STATUS_PASS if runtime_status == STATUS_PASS else STATUS_RUNTIME_GAP
    )
    if test_result.get("status") != expected_status:
        errors.append("final validation status does not match Python 3.11 execution")
    promotion_ready = expected_status == STATUS_PASS and promotion_eligible is True
    if test_result.get("promotion_ready") is not promotion_ready:
        errors.append("final promotion readiness does not match validation status")
    if test_result.get("evidence_complete") is not promotion_ready:
        errors.append("final evidence completeness does not match validation status")
    if test_result.get("dry_run") != {"status": STATUS_PASS, "return_code": 0}:
        errors.append("final dry-run result is not PASS")
    if test_result.get("artifact_validation") != {
        "status": STATUS_PASS,
        "errors": [],
    }:
        errors.append("final artifact validation result is not PASS")
    if test_result.get("external_mutation_count") != 0:
        errors.append("final external mutation count is not zero")
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


def validate_artifact_snapshot(
    snapshot: ArtifactSnapshot,
    output_dir: Path,
    lifecycle: Literal["prepared", "complete"],
) -> list[str]:
    errors: list[str] = []
    if lifecycle not in {"prepared", "complete"}:
        return ["artifact lifecycle must be prepared or complete"]
    try:
        _snapshot_mapping(snapshot)
        payload = {
            name: _load_snapshot_json(snapshot, name)
            for name in EVIDENCE_ARTIFACTS
            if name.endswith(".json")
        }
        run_report = _snapshot_bytes(snapshot, "run_report.md").decode("utf-8")
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not safely load artifact snapshot: {exc}"]

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
        current_status = _git_read(
            [
                "git",
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--ignore-submodules=none",
                "--no-renames",
            ]
        )
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

    try:
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
    except RuntimeError as exc:
        errors.append(f"trace Git status cannot derive a run ID: {exc}")
        return errors
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
    if lifecycle == "prepared":
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
            errors.append(
                "completion marker must remain INCOMPLETE until final validation"
            )
    else:
        promotion_eligible = (
            expected_boundary["status"] == STATUS_PASS
            and clean_worktree
            and trace.get("source_state") == "clean_commit"
        )
        errors.extend(
            _final_test_result_errors(test_result, expected_run_id, promotion_eligible)
        )
        final_status = (
            test_result.get("status") if isinstance(test_result, dict) else STATUS_FAIL
        )
        expected_completion = {
            "schema_version": "OAL-1.0",
            "run_id": expected_run_id,
            "status": final_status,
            "artifact_sha256": _artifact_digest_map(snapshot),
        }
        if completion != expected_completion:
            errors.append(
                "completion marker does not bind the semantically validated snapshot"
            )
    return errors


def validate_artifacts(output_dir: Path) -> list[str]:
    try:
        snapshot = _capture_artifact_snapshot(output_dir)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    return validate_artifact_snapshot(snapshot, output_dir, lifecycle="prepared")


def verify_existing_evidence(output_dir: Path) -> list[str]:
    """Fully reconstruct one final evidence bundle without writing or executing it."""

    try:
        snapshot = _capture_artifact_snapshot(output_dir)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    return validate_artifact_snapshot(snapshot, output_dir, lifecycle="complete")


def validate_completion_marker(output_dir: Path) -> list[str]:
    """Compatibility wrapper for the full semantic final-bundle verifier."""

    return verify_existing_evidence(output_dir)


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    _regular_file(path.parent / "mutation_trace.json", REPO_ROOT, "artifact anchor")
    _reject_link_components(REPO_ROOT, path, path.name)
    if path.exists():
        _regular_file(path, REPO_ROOT, path.name)
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


def _atomic_write_json(path: Path, payload: object) -> None:
    _atomic_write_bytes(path, _json_bytes(payload))


def _finalized_snapshot(
    prepared_snapshot: ArtifactSnapshot, test_result: Mapping[str, object]
) -> ArtifactSnapshot:
    bound_snapshot = _replace_snapshot_bytes(
        prepared_snapshot, "test_result.json", _json_bytes(test_result)
    )
    status = test_result.get("status")
    if status not in {STATUS_PASS, STATUS_RUNTIME_GAP}:
        raise ValueError("only successful or runtime-gap evidence can be finalized")
    trace = _load_snapshot_json(bound_snapshot, "mutation_trace.json")
    if not isinstance(trace, dict):
        raise ValueError("mutation trace must be a JSON object")
    completion = {
        "schema_version": "OAL-1.0",
        "run_id": trace.get("run_id"),
        "status": status,
        "artifact_sha256": _artifact_digest_map(bound_snapshot),
    }
    return _replace_snapshot_bytes(
        bound_snapshot, "validation_complete.json", _json_bytes(completion)
    )


def _finalize_evidence(
    output_dir: Path,
    prepared_snapshot: ArtifactSnapshot,
    test_result: Mapping[str, object],
) -> list[str]:
    try:
        if _capture_artifact_snapshot(output_dir) != prepared_snapshot:
            return ["artifact set changed after semantic validation"]
        finalized_snapshot = _finalized_snapshot(prepared_snapshot, test_result)
        errors = validate_artifact_snapshot(
            finalized_snapshot, output_dir, lifecycle="complete"
        )
        if errors:
            return errors
        _atomic_write_bytes(
            output_dir / "test_result.json",
            _snapshot_bytes(finalized_snapshot, "test_result.json"),
        )
        _atomic_write_bytes(
            output_dir / "validation_complete.json",
            _snapshot_bytes(finalized_snapshot, "validation_complete.json"),
        )
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not atomically finalize evidence: {exc}"]
    return verify_existing_evidence(output_dir)


def _run_id_argument(value: str) -> str:
    if not RUN_ID_PATTERN.fullmatch(value):
        raise argparse.ArgumentTypeError("must be an OAL-001 run ID")
    return value


def _existing_output_dir(run_id: str) -> Path:
    output_root = REPO_ROOT / str(EXPECTED_POLICY["output_root"])
    output_dir = output_root / run_id
    _reject_link_components(REPO_ROOT, output_dir, "existing evidence directory")
    resolved_root = output_root.resolve(strict=True)
    resolved = output_dir.resolve(strict=True)
    if (
        resolved.parent != resolved_root
        or resolved.name != run_id
        or not resolved.is_dir()
    ):
        raise ValueError("existing evidence directory is outside the fixed output root")
    rel_path = resolved.relative_to(REPO_ROOT.resolve()).as_posix()
    if not git_check_ignored(rel_path):
        raise ValueError("existing evidence directory is not gitignored")
    return resolved


def _verify_existing(run_id: str) -> int:
    static_validation_errors = static_errors()
    if static_validation_errors:
        for item in static_validation_errors:
            error(item)
        return 1
    try:
        output_dir = _existing_output_dir(run_id)
        snapshot = _capture_artifact_snapshot(output_dir)
        verification_errors = validate_artifact_snapshot(
            snapshot, output_dir, lifecycle="complete"
        )
        test_result = _load_snapshot_json(snapshot, "test_result.json")
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        error(f"could not verify existing evidence: {exc}")
        return 1
    if verification_errors:
        for item in verification_errors:
            error(item)
        return 1
    if not isinstance(test_result, dict):
        error("final test result must be a JSON object")
        return 1
    status = test_result.get("status")
    target = test_result.get("python_3_11_target")
    runtime_status = target.get("runtime") if isinstance(target, dict) else None
    if status == STATUS_RUNTIME_GAP:
        print(
            f"[validate-oal-001] VERIFIED_WITH_RUNTIME_GAP run_id={run_id} "
            f"status={status} python_3_11_runtime={runtime_status}"
        )
        return EXIT_RUNTIME_GAP
    if status != STATUS_PASS:
        error("final evidence status is not recognized")
        return 1
    if test_result.get("promotion_ready") is not True:
        print(
            f"[validate-oal-001] VERIFIED_NOT_PROMOTION_READY run_id={run_id} "
            f"status={status}"
        )
        return EXIT_NOT_PROMOTION_READY
    print(f"[validate-oal-001] VERIFIED run_id={run_id} status={status}")
    return 0


def _run_validation() -> int:

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

    try:
        prepared_snapshot = _capture_artifact_snapshot(output_dir)
    except (OSError, ValueError) as exc:
        error(str(exc))
        return 1
    errors = validate_artifact_snapshot(
        prepared_snapshot, output_dir, lifecycle="prepared"
    )
    if errors:
        for item in errors:
            error(item)
        return 1
    promotion_eligible = _snapshot_promotion_eligible(prepared_snapshot)
    test_result = _build_test_result(
        run_id=str(summary["run_id"]),
        test_count=int(test_count),
        test_outcomes=test_outcomes or {},
        test_returncode=test_returncode,
        dry_run_returncode=dry_run_returncode,
        artifact_errors=[],
        python_version=sys.version.split()[0],
        python_version_info=sys.version_info[:2],
        promotion_eligible=promotion_eligible,
    )
    errors = _finalize_evidence(output_dir, prepared_snapshot, test_result)

    if errors:
        for item in errors:
            error(item)
        return 1

    status = str(test_result["status"])
    if status == STATUS_RUNTIME_GAP:
        label = "OK_WITH_RUNTIME_GAP"
    elif test_result["promotion_ready"] is True:
        label = "OK"
    else:
        label = "OK_NOT_PROMOTION_READY"
    print(
        f"[validate-oal-001] {label} run_id={summary['run_id']} status={status} "
        f"tests={test_count} skipped={(test_outcomes or {}).get('skipped', 0)}"
    )
    print(f"[validate-oal-001] output_dir={summary['output_dir']}")
    print("[validate-oal-001] external_mutation_count=0")
    if status == STATUS_RUNTIME_GAP:
        return EXIT_RUNTIME_GAP
    if test_result["promotion_ready"] is not True:
        return EXIT_NOT_PROMOTION_READY
    return 0


def _dispatch(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate or read-only verify OAL-001 local evidence."
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--verify-existing",
        metavar="RUN_ID",
        type=_run_id_argument,
        help="Verify one finalized run without tests, dry-run or writes.",
    )
    modes.add_argument(
        "--_internal-unit-tests",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    modes.add_argument(
        "--_internal-dry-run",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if args._internal_unit_tests or args._internal_dry_run:
        import_errors = python_shadowing_errors(REPO_ROOT)
        if import_errors:
            for item in import_errors:
                error(item)
            return 1
        if args._internal_unit_tests:
            return _internal_unit_tests()
        return _internal_dry_run()
    if args.verify_existing:
        return _verify_existing(args.verify_existing)
    return _run_validation()


def _runtime_isolation_errors() -> list[str]:
    errors: list[str] = []
    if not INTERPRETER_ISOLATED:
        errors.append("validator requires python -I -S -B")
    if unsafe_import_path:
        errors.append("repository paths precede the isolated import boundary")
    if not repository_import_root_isolated:
        errors.append("repository import root is not isolated")
    return errors


def main(argv: list[str] | None = None) -> int:
    isolation_errors = _runtime_isolation_errors()
    if isolation_errors:
        for item in isolation_errors:
            error(item)
        return 1
    return _dispatch(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
