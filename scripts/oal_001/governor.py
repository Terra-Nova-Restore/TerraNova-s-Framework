"""Baseline-only Governor for OAL-001 candidate mutations."""

from __future__ import annotations

import fnmatch
import json
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


SHA256_PATTERN = re.compile(r"^[A-Fa-f0-9]{64}$")
EXPECTED_MUTABLE_PATHS = ("scripts/oal_001/observatory.py",)
EXPECTED_PROTECTED_PATHS = (
    ".codex",
    ".git",
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
)
EXPECTED_AUTHORIZING_TEST_PATHS = (
    "tests/test_oal_001_governor.py",
    "tests/test_oal_001_runtime.py",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
)


class PolicyError(ValueError):
    """Raised when the immutable policy is malformed."""


@dataclass(frozen=True)
class GovernorPolicy:
    policy_id: str
    schema_version: str
    mode: str
    branch_pattern: str
    mutable_paths: tuple[str, ...]
    protected_paths: tuple[str, ...]
    authorizing_test_paths: tuple[str, ...]
    fixture_path: str
    output_root: str
    minimum_exploration_share: float
    external_mutation_count: int
    historical_fixture_status: str


@dataclass(frozen=True)
class PatchSpec:
    cycle_id: str
    target_path: str
    changed_paths: tuple[str, ...]
    expected_before_sha256: str
    replacement_text: str
    trigger: str
    hypothesis: str
    expected_effect: str
    fallback_criterion: str


@dataclass(frozen=True)
class GovernorDecision:
    approved: bool
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "approved": self.approved,
            "reasons": list(self.reasons),
            "immutable_surface": "baseline_only",
        }


def _string_list(payload: dict[str, object], key: str) -> tuple[str, ...]:
    value = payload.get(key)
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item for item in value)
    ):
        raise PolicyError(f"{key} must be a non-empty string list")
    return tuple(value)


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def load_policy(repo_root: Path) -> GovernorPolicy:
    root = repo_root.resolve()
    path = root / "config" / "oal_001.json"
    current = root
    for part in ("config", "oal_001.json"):
        current = current / part
        if current.is_symlink() or _is_reparse_point(current):
            raise PolicyError(
                "immutable policy path must not contain links or reparse points"
            )
    try:
        path.resolve().relative_to(root)
    except ValueError as exc:
        raise PolicyError("immutable policy path escapes repository root") from exc
    if not path.is_file() or path.stat().st_nlink > 1:
        raise PolicyError("immutable policy must be one regular, non-hard-linked file")
    payload = json.loads(path.read_bytes().decode("utf-8"))
    if not isinstance(payload, dict):
        raise PolicyError("policy root must be an object")

    required_strings = (
        "policy_id",
        "schema_version",
        "mode",
        "branch_pattern",
        "fixture_path",
        "output_root",
        "historical_fixture_status",
    )
    for key in required_strings:
        if not isinstance(payload.get(key), str) or not payload[key]:
            raise PolicyError(f"{key} must be a non-empty string")

    minimum = payload.get("minimum_exploration_share")
    if (
        not isinstance(minimum, (int, float))
        or isinstance(minimum, bool)
        or not 0 <= float(minimum) <= 1
    ):
        raise PolicyError("minimum_exploration_share must be between 0 and 1")
    mutation_count = payload.get("external_mutation_count")
    if mutation_count != 0:
        raise PolicyError("external_mutation_count must be zero")

    policy = GovernorPolicy(
        policy_id=payload["policy_id"],
        schema_version=payload["schema_version"],
        mode=payload["mode"],
        branch_pattern=payload["branch_pattern"],
        mutable_paths=_string_list(payload, "mutable_paths"),
        protected_paths=_string_list(payload, "protected_paths"),
        authorizing_test_paths=_string_list(payload, "authorizing_test_paths"),
        fixture_path=payload["fixture_path"],
        output_root=payload["output_root"],
        minimum_exploration_share=float(minimum),
        external_mutation_count=mutation_count,
        historical_fixture_status=payload["historical_fixture_status"],
    )
    for candidate in (
        *policy.mutable_paths,
        *policy.protected_paths,
        *policy.authorizing_test_paths,
        policy.fixture_path,
        policy.output_root,
    ):
        normalize_relative_path(candidate)
    if set(policy.mutable_paths) & set(policy.protected_paths):
        raise PolicyError("mutable_paths and protected_paths must not overlap exactly")
    expected_scalars = {
        "policy_id": "OAL-001-GOVERNOR",
        "schema_version": "OAL-1.0",
        "mode": "local_dry_run",
        "branch_pattern": "codex/observatory-selfmod-*",
        "fixture_path": "tests/fixtures/observatory/synthetic_harmless_cycle.json",
        "output_root": "raw/exports/local-private/oal-001",
        "historical_fixture_status": "unavailable",
    }
    for field, expected in expected_scalars.items():
        if getattr(policy, field) != expected:
            raise PolicyError(f"{field} must remain {expected}")
    if policy.mutable_paths != EXPECTED_MUTABLE_PATHS:
        raise PolicyError("mutable_paths must remain the exact first-slice allowlist")
    if policy.protected_paths != EXPECTED_PROTECTED_PATHS:
        raise PolicyError(
            "protected_paths must remain the exact first-slice protected surface"
        )
    if policy.authorizing_test_paths != EXPECTED_AUTHORIZING_TEST_PATHS:
        raise PolicyError("authorizing_test_paths must remain independently protected")
    if policy.minimum_exploration_share != 0.25:
        raise PolicyError("minimum_exploration_share must remain 0.25")
    return policy


def normalize_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise PolicyError(f"path must be a non-empty POSIX relative path: {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or re.match(r"^[A-Za-z]:/", value)
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise PolicyError(f"path must not be absolute or contain traversal: {value}")
    normalized = path.as_posix()
    if normalized != value:
        raise PolicyError(f"path is not normalized: {value}")
    return normalized


def path_is_within(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix}/")


def contains_secret_marker(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


class Governor:
    """Review candidate metadata and paths before any candidate write."""

    def __init__(self, policy: GovernorPolicy):
        self.policy = policy

    def review(self, patch: PatchSpec, branch: str) -> GovernorDecision:
        reasons: list[str] = []
        metadata = {
            "cycle_id": patch.cycle_id,
            "trigger": patch.trigger,
            "hypothesis": patch.hypothesis,
            "expected_effect": patch.expected_effect,
            "fallback_criterion": patch.fallback_criterion,
        }
        for key, value in metadata.items():
            if not isinstance(value, str) or not value.strip():
                reasons.append(f"missing_metadata:{key}")

        if not fnmatch.fnmatchcase(branch, self.policy.branch_pattern):
            reasons.append("branch_outside_allowed_lane")
        if not SHA256_PATTERN.fullmatch(patch.expected_before_sha256):
            reasons.append("invalid_expected_before_sha256")
        if not patch.replacement_text:
            reasons.append("empty_replacement")
        elif contains_secret_marker(patch.replacement_text):
            reasons.append("secret_like_content")

        paths = tuple(dict.fromkeys(patch.changed_paths))
        if patch.target_path not in paths:
            reasons.append("target_missing_from_changed_paths")
        if len(paths) != len(patch.changed_paths):
            reasons.append("duplicate_changed_path")

        normalized_paths: list[str] = []
        for value in paths:
            try:
                normalized_paths.append(normalize_relative_path(value))
            except PolicyError:
                reasons.append(f"invalid_path:{value}")

        protected_changed = [
            value
            for value in normalized_paths
            if any(
                path_is_within(value, prefix) for prefix in self.policy.protected_paths
            )
        ]
        authorizing_test_changed = [
            value
            for value in normalized_paths
            if any(
                path_is_within(value, prefix)
                for prefix in self.policy.authorizing_test_paths
            )
        ]
        control_changed = [
            value
            for value in protected_changed
            if not any(
                path_is_within(value, prefix)
                for prefix in self.policy.authorizing_test_paths
            )
        ]
        if control_changed and authorizing_test_changed:
            reasons.append("same_cycle_control_and_authorizing_test_change")

        for value in normalized_paths:
            if any(
                path_is_within(value, prefix) for prefix in self.policy.protected_paths
            ):
                reasons.append(f"protected_path:{value}")
            if value not in self.policy.mutable_paths:
                reasons.append(f"path_not_mutable:{value}")

        return GovernorDecision(
            approved=not reasons, reasons=tuple(sorted(set(reasons)))
        )

    def require_approval(self, patch: PatchSpec, branch: str) -> GovernorDecision:
        decision = self.review(patch, branch)
        if not decision.approved:
            raise PermissionError(
                "Governor rejected candidate: " + ", ".join(decision.reasons)
            )
        return decision


def protected_changes(policy: GovernorPolicy, paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        path
        for path in paths
        if any(path_is_within(path, prefix) for prefix in policy.protected_paths)
    )
