"""Deterministic candidate, replay, evaluation and rollback runtime for OAL-001."""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .governor import Governor, GovernorDecision, GovernorPolicy, PatchSpec
from .git_read import is_ignored, worktree_status


TARGET_PATH = "scripts/oal_001/observatory.py"
CYCLE_ID = "OAL-001-SYNTHETIC-CURRENT-SLICE-001"
TRIGGER = "GitHub Issue #97 first-slice controlled self-modification dry-run"
HYPOTHESIS = (
    "Increasing the synthetic exploration share from 0.25 to 0.30 improves secondary-path "
    "coverage while preserving deterministic routing and all Governor boundaries."
)
EXPECTED_EFFECT = "One additional synthetic observation is routed to exploration in a 20-observation replay."
FALLBACK_CRITERION = (
    "Reject and restore the candidate if parsing, determinism, the 25 percent floor, the expected replay delta, "
    "baseline integrity or any Governor boundary fails."
)
NOT_ACTIONS = (
    "git_push",
    "pull_request",
    "merge",
    "main_write",
    "remote_branch_mutation",
    "notion_write",
    "learning_ledger_write",
    "workflow_execution",
    "publication",
    "payment_mutation",
    "zenodo_mutation",
)
MANAGED_SOURCE_PATHS = (
    ".codex/safety_policy.yaml",
    ".gitignore",
    "config/oal_001.json",
    "docs/governance/oal_001_self_modification_policy.md",
    "schemas/oal_001_mutation_trace.schema.json",
    "scripts/oal_001/__init__.py",
    "scripts/oal_001/__main__.py",
    "scripts/oal_001/git_read.py",
    "scripts/oal_001/governor.py",
    TARGET_PATH,
    "scripts/oal_001/runtime.py",
    "scripts/validate_oal_001.py",
    "tests/fixtures/observatory/synthetic_harmless_cycle.json",
    "tests/test_oal_001_governor.py",
    "tests/test_oal_001_runtime.py",
)
TRACE_REQUIRED_FIELDS = {
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
EVALUATION_CHECK_NAMES = {
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
SHA256_PATTERN = re.compile(r"^[A-F0-9]{64}$")
GIT_SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")


class CandidateBoundaryError(ValueError):
    """Raised before unsafe candidate filesystem access."""


@dataclass(frozen=True)
class ReplayResult:
    fixture_id: str
    fixture_kind: str
    historical_evidence: bool
    source_sha256: str
    observation_count: int
    strategy_weights: dict[str, float]
    route_counts: dict[str, int]
    routing_digest: str

    def as_dict(self) -> dict[str, object]:
        return {
            "fixture_id": self.fixture_id,
            "fixture_kind": self.fixture_kind,
            "historical_evidence": self.historical_evidence,
            "source_sha256": self.source_sha256,
            "observation_count": self.observation_count,
            "strategy_weights": self.strategy_weights,
            "route_counts": self.route_counts,
            "routing_digest": self.routing_digest,
        }


@dataclass(frozen=True)
class EvaluationResult:
    decision: str
    reasons: tuple[str, ...]
    checks: dict[str, bool]

    def as_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision,
            "reasons": list(self.reasons),
            "checks": self.checks,
        }


@dataclass(frozen=True)
class CycleResult:
    trace: dict[str, object]
    source_manifest: list[dict[str, object]]
    replay_before: dict[str, object]
    replay_after: dict[str, object]
    comparison: dict[str, object]
    rollback_proof: dict[str, object]
    boundary_report: dict[str, object]
    risk_report: dict[str, object]
    run_report: str

    @property
    def run_id(self) -> str:
        return str(self.trace["run_id"])


def canonical_json(payload: object) -> str:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path.name}")
    return payload


def _ensure_within(root: Path, path: Path, label: str) -> Path:
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise CandidateBoundaryError(f"{label} escapes its allowed root") from exc
    return resolved_path


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _reject_symlink_components(root: Path, path: Path, label: str) -> None:
    resolved_root = root.resolve()
    try:
        relative = path.absolute().relative_to(resolved_root)
    except ValueError as exc:
        raise CandidateBoundaryError(f"{label} escapes its allowed root") from exc
    current = resolved_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or _is_reparse_point(current):
            raise CandidateBoundaryError(
                f"{label} must not contain links or reparse-point components"
            )


def read_managed_source(repo_root: Path, rel_path: str) -> bytes:
    source = repo_root / rel_path
    _reject_symlink_components(repo_root, source, "managed source")
    resolved = _ensure_within(repo_root, source, "managed source")
    if not resolved.is_file():
        raise CandidateBoundaryError(
            f"managed source is not a regular file: {rel_path}"
        )
    if resolved.stat().st_nlink > 1:
        raise CandidateBoundaryError(
            f"managed source must not be hard-linked: {rel_path}"
        )
    return resolved.read_bytes()


def _validate_writable_target(root: Path, path: Path, label: str) -> Path:
    _reject_symlink_components(root, path, label)
    resolved = _ensure_within(root, path, label)
    if resolved.exists():
        if not resolved.is_file():
            raise CandidateBoundaryError(f"{label} is not a regular file")
        if resolved.stat().st_nlink > 1:
            raise CandidateBoundaryError(f"{label} must not be hard-linked")
    return resolved


def parse_strategy_bytes(
    source_bytes: bytes, filename: str = "observatory.py"
) -> dict[str, float]:
    source = source_bytes.decode("utf-8")
    tree = ast.parse(source, filename=filename)
    weights_node: ast.AST | None = None
    for index, node in enumerate(tree.body):
        if (
            index == 0
            and isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
        ):
            if isinstance(node.value.value, str):
                continue
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "STRATEGY_WEIGHTS"
        ):
            if weights_node is not None:
                raise ValueError("STRATEGY_WEIGHTS must be assigned exactly once")
            weights_node = node.value
            continue
        raise ValueError(
            "candidate Observatory source contains executable or unsupported syntax"
        )

    if weights_node is None:
        raise ValueError("candidate Observatory source is missing STRATEGY_WEIGHTS")
    value = ast.literal_eval(weights_node)
    if not isinstance(value, dict) or set(value) != {"primary", "exploration"}:
        raise ValueError("STRATEGY_WEIGHTS must contain only primary and exploration")
    if not all(
        isinstance(item, (int, float)) and not isinstance(item, bool)
        for item in value.values()
    ):
        raise ValueError("strategy weights must be numeric")
    weights = {key: float(item) for key, item in value.items()}
    if any(item < 0 or item > 1 for item in weights.values()):
        raise ValueError("strategy weights must be between zero and one")
    if abs(sum(weights.values()) - 1.0) > 1e-12:
        raise ValueError("strategy weights must sum to one")
    return weights


def parse_strategy_source(path: Path) -> dict[str, float]:
    return parse_strategy_bytes(path.read_bytes(), filename=path.name)


def load_fixture(repo_root: Path, rel_path: str) -> dict[str, object]:
    raw = read_managed_source(repo_root, rel_path)
    fixture = json.loads(raw.decode("utf-8"))
    if not isinstance(fixture, dict):
        raise ValueError("fixture root must be an object")
    required = {
        "fixture_id",
        "fixture_kind",
        "historical_evidence",
        "observations",
        "expected_baseline_exploration_share",
        "expected_candidate_exploration_share",
    }
    if set(fixture) != required:
        raise ValueError(
            "synthetic fixture fields do not match the first-slice contract"
        )
    if (
        fixture["fixture_kind"] != "synthetic_current_slice"
        or fixture["historical_evidence"] is not False
    ):
        raise ValueError("fixture must be explicitly synthetic and non-historical")
    observations = fixture["observations"]
    if (
        not isinstance(observations, list)
        or not observations
        or not all(isinstance(item, str) for item in observations)
    ):
        raise ValueError("fixture observations must be a non-empty string list")
    if len(set(observations)) != len(observations):
        raise ValueError("fixture observations must be unique")
    return fixture


class ReplayHarness:
    def __init__(self, fixture: Mapping[str, object]):
        self.fixture = fixture

    def replay(self, source_path: Path) -> ReplayResult:
        return self.replay_bytes(source_path.read_bytes(), filename=source_path.name)

    def replay_bytes(
        self, source_bytes: bytes, filename: str = "observatory.py"
    ) -> ReplayResult:
        weights = parse_strategy_bytes(source_bytes, filename=filename)
        observations = list(self.fixture["observations"])
        exploration_count = round(len(observations) * weights["exploration"])
        primary_count = len(observations) - exploration_count
        routes = [
            {
                "observation": observation,
                "route": "primary" if index < primary_count else "exploration",
            }
            for index, observation in enumerate(observations)
        ]
        return ReplayResult(
            fixture_id=str(self.fixture["fixture_id"]),
            fixture_kind=str(self.fixture["fixture_kind"]),
            historical_evidence=bool(self.fixture["historical_evidence"]),
            source_sha256=sha256_bytes(source_bytes),
            observation_count=len(observations),
            strategy_weights=weights,
            route_counts={"primary": primary_count, "exploration": exploration_count},
            routing_digest=sha256_text(canonical_json(routes)),
        )


class CandidateWorkspace:
    """Temporary copy of one Governor-approved mutable path."""

    def __init__(
        self, repo_root: Path, target_path: str, temp_parent: Path | None = None
    ):
        self.repo_root = repo_root.resolve()
        self.target_path = target_path
        self.temp_parent = temp_parent
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self.root: Path | None = None
        self.baseline_bytes: bytes | None = None

    def __enter__(self) -> "CandidateWorkspace":
        self.baseline_bytes = read_managed_source(self.repo_root, self.target_path)
        if self.temp_parent is not None:
            self.temp_parent.mkdir(parents=True, exist_ok=True)
        self._temporary = tempfile.TemporaryDirectory(
            prefix="oal-001-candidate-", dir=self.temp_parent
        )
        self.root = Path(self._temporary.name)
        candidate = self.path
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_bytes(self.baseline_bytes)
        return self

    @property
    def path(self) -> Path:
        if self.root is None:
            raise RuntimeError("candidate workspace is not active")
        return self.root / self.target_path

    def apply(self, patch: PatchSpec) -> tuple[str, str]:
        if patch.target_path != self.target_path or patch.changed_paths != (
            self.target_path,
        ):
            raise CandidateBoundaryError(
                "candidate workspace accepts exactly one approved target"
            )
        if self.baseline_bytes is None or self.root is None:
            raise RuntimeError("candidate workspace is not active")
        actual = sha256_bytes(self.path.read_bytes())
        if actual != patch.expected_before_sha256.upper():
            raise CandidateBoundaryError(
                "candidate baseline hash does not match PatchSpec"
            )
        target = _validate_writable_target(self.root, self.path, "candidate target")
        target.write_text(patch.replacement_text, encoding="utf-8", newline="\n")
        candidate_text = target.read_text(encoding="utf-8")
        baseline_text = self.baseline_bytes.decode("utf-8")
        diff = "".join(
            difflib.unified_diff(
                baseline_text.splitlines(keepends=True),
                candidate_text.splitlines(keepends=True),
                fromfile=f"a/{self.target_path}",
                tofile=f"b/{self.target_path}",
            )
        )
        if not diff:
            raise ValueError("candidate patch produced no diff")
        return diff, sha256_bytes(target.read_bytes())

    def rollback(self) -> dict[str, object]:
        if self.baseline_bytes is None or self.root is None:
            raise RuntimeError("candidate workspace is not active")
        target = _validate_writable_target(
            self.root, self.path, "candidate rollback target"
        )
        target.write_bytes(self.baseline_bytes)
        restored = sha256_bytes(target.read_bytes()) == sha256_bytes(
            self.baseline_bytes
        )
        return {
            "candidate_restored": restored,
            "restored_sha256": sha256_bytes(target.read_bytes()),
        }

    def snapshot(self) -> bytes:
        if self.root is None:
            raise RuntimeError("candidate workspace is not active")
        target = _validate_writable_target(self.root, self.path, "candidate snapshot")
        return target.read_bytes()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._temporary is not None:
            self._temporary.cleanup()


class PatchEvaluator:
    def __init__(self, policy: GovernorPolicy, fixture: Mapping[str, object]):
        self.policy = policy
        self.fixture = fixture

    def evaluate(
        self,
        governor_decision: GovernorDecision,
        before_first: ReplayResult,
        before_second: ReplayResult,
        after_first: ReplayResult,
        after_second: ReplayResult,
        baseline_unchanged: bool,
    ) -> EvaluationResult:
        before_payload = before_first.as_dict()
        after_payload = after_first.as_dict()
        checks = {
            "governor_approved": governor_decision.approved,
            "baseline_deterministic": before_payload == before_second.as_dict(),
            "candidate_deterministic": after_payload == after_second.as_dict(),
            "baseline_expected_share": before_first.strategy_weights["exploration"]
            == float(self.fixture["expected_baseline_exploration_share"]),
            "candidate_expected_share": after_first.strategy_weights["exploration"]
            == float(self.fixture["expected_candidate_exploration_share"]),
            "exploration_floor_preserved": after_first.strategy_weights["exploration"]
            >= self.policy.minimum_exploration_share,
            "expected_replay_delta": after_first.route_counts["exploration"]
            == before_first.route_counts["exploration"] + 1,
            "baseline_unchanged": baseline_unchanged,
            "synthetic_fixture_only": after_first.fixture_kind
            == "synthetic_current_slice"
            and not after_first.historical_evidence,
            "external_mutation_count_zero": self.policy.external_mutation_count == 0,
        }
        failed = tuple(sorted(name for name, passed in checks.items() if not passed))
        if failed:
            return EvaluationResult("reject", failed, checks)
        return EvaluationResult("retain", ("all_first_slice_checks_passed",), checks)


def build_harmless_patch(source_text: str, baseline_sha256: str) -> PatchSpec:
    replacements = (
        ('"primary": 0.75', '"primary": 0.70'),
        ('"exploration": 0.25', '"exploration": 0.30'),
    )
    candidate = source_text
    for before, after in replacements:
        if candidate.count(before) != 1:
            raise ValueError(f"harmless patch marker must occur exactly once: {before}")
        candidate = candidate.replace(before, after)
    return PatchSpec(
        cycle_id=CYCLE_ID,
        target_path=TARGET_PATH,
        changed_paths=(TARGET_PATH,),
        expected_before_sha256=baseline_sha256,
        replacement_text=candidate,
        trigger=TRIGGER,
        hypothesis=HYPOTHESIS,
        expected_effect=EXPECTED_EFFECT,
        fallback_criterion=FALLBACK_CRITERION,
    )


def derive_run_id(
    base_sha: str,
    branch: str,
    git_status_before: str,
    git_status_after: str,
    cycle_id: str,
    target_path: str,
    baseline_sha256: str,
    candidate_sha256: str,
    fixture_id: str,
    source_manifest: list[dict[str, object]],
) -> str:
    material = {
        "base_sha": base_sha,
        "branch": branch,
        "git_status_before": git_status_before,
        "git_status_after": git_status_after,
        "cycle_id": cycle_id,
        "target_path": target_path,
        "baseline_sha256": baseline_sha256,
        "candidate_sha256": candidate_sha256,
        "fixture_id": fixture_id,
        "source_manifest": source_manifest,
    }
    digest = sha256_text(canonical_json(material))[:16]
    return f"OAL-001-{digest}"


def execute_cycle(
    repo_root: Path,
    policy: GovernorPolicy,
    branch: str,
    base_sha: str,
    git_status_before: str | None = None,
    git_status_after: str | None = None,
    temp_parent: Path | None = None,
) -> CycleResult:
    repo_root = repo_root.resolve()
    if not GIT_SHA_PATTERN.fullmatch(base_sha):
        raise ValueError("base_sha must be a lowercase 40-character Git SHA")
    if git_status_before is None:
        git_status_before = _git_status(repo_root)
    source_manifest_before = source_manifest_for_repo(repo_root)
    managed_manifest_sha256_before = sha256_text(canonical_json(source_manifest_before))
    fixture = load_fixture(repo_root, policy.fixture_path)
    source_bytes = read_managed_source(repo_root, TARGET_PATH)
    baseline_sha256 = sha256_bytes(source_bytes)
    patch = build_harmless_patch(source_bytes.decode("utf-8"), baseline_sha256)
    governor_decision = Governor(policy).require_approval(patch, branch)
    harness = ReplayHarness(fixture)
    before_first = harness.replay_bytes(source_bytes)
    before_second = harness.replay_bytes(source_bytes)
    active_hash_before = sha256_bytes(read_managed_source(repo_root, TARGET_PATH))

    workspace_root: Path | None = None
    with CandidateWorkspace(
        repo_root, TARGET_PATH, temp_parent=temp_parent
    ) as workspace:
        workspace_root = workspace.root
        diff, candidate_sha256 = workspace.apply(patch)
        candidate_snapshot = workspace.snapshot()
        after_first = harness.replay_bytes(candidate_snapshot)
        after_second = harness.replay_bytes(candidate_snapshot)
        active_hash_during = sha256_bytes(read_managed_source(repo_root, TARGET_PATH))
        source_manifest_during = source_manifest_for_repo(repo_root)
        provisional_evaluation = PatchEvaluator(policy, fixture).evaluate(
            governor_decision,
            before_first,
            before_second,
            after_first,
            after_second,
            active_hash_before == active_hash_during,
        )
        rollback_partial = workspace.rollback()

    workspace_removed = bool(workspace_root is not None and not workspace_root.exists())
    active_hash_after = sha256_bytes(read_managed_source(repo_root, TARGET_PATH))
    source_manifest_after = source_manifest_for_repo(repo_root)
    managed_manifest_sha256_after = sha256_text(canonical_json(source_manifest_after))
    managed_baseline_unchanged = (
        source_manifest_before == source_manifest_during == source_manifest_after
    )
    if git_status_after is None:
        git_status_after = _git_status(repo_root)
    rollback_proof = {
        "status": "verified"
        if rollback_partial["candidate_restored"]
        and active_hash_before == active_hash_after
        and managed_baseline_unchanged
        and workspace_removed
        else "failed",
        "candidate_restored": bool(rollback_partial["candidate_restored"]),
        "restored_sha256": rollback_partial["restored_sha256"],
        "baseline_sha256_before": active_hash_before,
        "baseline_sha256_after": active_hash_after,
        "managed_manifest_sha256_before": managed_manifest_sha256_before,
        "managed_manifest_sha256_after": managed_manifest_sha256_after,
        "baseline_unchanged": managed_baseline_unchanged,
        "candidate_workspace_removed": workspace_removed,
    }
    final_checks = dict(provisional_evaluation.checks)
    final_checks.update(
        {
            "rollback_verified": rollback_proof["status"] == "verified",
            "managed_baseline_unchanged": managed_baseline_unchanged,
            "candidate_workspace_removed": workspace_removed,
        }
    )
    failed_checks = tuple(
        sorted(name for name, passed in final_checks.items() if not passed)
    )
    evaluation = (
        EvaluationResult("reject", failed_checks, final_checks)
        if failed_checks
        else EvaluationResult(
            "retain", ("all_first_slice_checks_passed",), final_checks
        )
    )
    git_status_unchanged = git_status_before == git_status_after
    clean_worktree = git_status_is_clean(git_status_before) and git_status_is_clean(
        git_status_after
    )
    source_state = "clean_commit" if clean_worktree else "working_tree_manifest"
    source_manifest_sha256 = sha256_text(canonical_json(source_manifest_before))
    run_id = derive_run_id(
        base_sha,
        branch,
        git_status_before,
        git_status_after,
        patch.cycle_id,
        patch.target_path,
        patch.expected_before_sha256,
        candidate_sha256,
        str(fixture["fixture_id"]),
        source_manifest_before,
    )
    rollback_proof["run_id"] = run_id
    comparison = {
        "run_id": run_id,
        "baseline": before_first.as_dict(),
        "candidate": after_first.as_dict(),
        "delta": {
            "exploration_share": round(
                after_first.strategy_weights["exploration"]
                - before_first.strategy_weights["exploration"],
                12,
            ),
            "exploration_routes": after_first.route_counts["exploration"]
            - before_first.route_counts["exploration"],
        },
        "evaluation": evaluation.as_dict(),
    }
    trace = {
        "schema_version": policy.schema_version,
        "run_id": run_id,
        "cycle_id": patch.cycle_id,
        "mode": policy.mode,
        "base_sha": base_sha,
        "branch": branch,
        "source_state": source_state,
        "source_manifest_sha256": source_manifest_sha256,
        "fixture": {
            "fixture_id": fixture["fixture_id"],
            "fixture_kind": fixture["fixture_kind"],
            "historical_evidence": fixture["historical_evidence"],
            "historical_fixture_status": policy.historical_fixture_status,
        },
        "trigger": patch.trigger,
        "hypothesis": patch.hypothesis,
        "expected_effect": patch.expected_effect,
        "fallback_criterion": patch.fallback_criterion,
        "target_path": patch.target_path,
        "changed_paths": list(patch.changed_paths),
        "baseline_sha256": baseline_sha256,
        "candidate_sha256": candidate_sha256,
        "diff_sha256": sha256_text(diff),
        "diff": diff,
        "governor": governor_decision.as_dict(),
        "isolation": {
            "candidate_workspace": "temporary_allowlist_copy",
            "managed_paths": list(patch.changed_paths),
            "running_version_overwritten": False,
        },
        "replay": {
            "baseline_deterministic": before_first.as_dict() == before_second.as_dict(),
            "candidate_deterministic": after_first.as_dict() == after_second.as_dict(),
            "before_artifact": "replay_before.json",
            "after_artifact": "replay_after.json",
        },
        "evaluation": evaluation.as_dict(),
        "rollback": {
            "status": rollback_proof["status"],
            "candidate_restored": rollback_proof["candidate_restored"],
            "baseline_unchanged": rollback_proof["baseline_unchanged"],
            "candidate_workspace_removed": rollback_proof[
                "candidate_workspace_removed"
            ],
        },
        "git_status": {
            "before": git_status_before,
            "after": git_status_after,
            "unchanged": git_status_unchanged,
            "clean_worktree": clean_worktree,
        },
        "external_mutation_count": policy.external_mutation_count,
        "not_actions": list(NOT_ACTIONS),
    }
    boundary_checks = {
        "governor_approved": governor_decision.approved,
        "exact_mutable_allowlist": patch.changed_paths == policy.mutable_paths,
        "candidate_workspace_removed": workspace_removed,
        "running_version_overwritten": False,
        "baseline_unchanged": managed_baseline_unchanged,
        "candidate_source_executed": False,
        "external_mutation_count_zero": policy.external_mutation_count == 0,
        "historical_claim_fabricated": False,
        "git_status_unchanged": git_status_unchanged,
        "clean_worktree": clean_worktree,
    }
    boundary_pass = all(
        boundary_checks[name]
        for name in (
            "governor_approved",
            "exact_mutable_allowlist",
            "candidate_workspace_removed",
            "baseline_unchanged",
            "external_mutation_count_zero",
            "git_status_unchanged",
        )
    ) and not any(
        boundary_checks[name]
        for name in (
            "running_version_overwritten",
            "candidate_source_executed",
            "historical_claim_fabricated",
        )
    )
    boundary_report = {
        "run_id": run_id,
        "status": (
            "PASS"
            if boundary_pass and clean_worktree
            else "PASS_PREPARED"
            if boundary_pass
            else "FAIL"
        ),
        "checks": boundary_checks,
        "external_mutation_count": policy.external_mutation_count,
    }
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
    risk_report = {
        "run_id": run_id,
        "status": (
            "FAIL"
            if not boundary_pass
            or evaluation.decision != "retain"
            or rollback_proof["status"] != "verified"
            else "PASS_WITH_DEFERRED_SCOPE"
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
    run_report = render_run_report(
        trace, comparison, rollback_proof, boundary_report, risk_report
    )
    errors = validate_trace_payload(trace)
    if errors:
        raise ValueError("invalid mutation trace: " + "; ".join(errors))
    return CycleResult(
        trace=trace,
        source_manifest=source_manifest_before,
        replay_before=before_first.as_dict(),
        replay_after=after_first.as_dict(),
        comparison=comparison,
        rollback_proof=rollback_proof,
        boundary_report=boundary_report,
        risk_report=risk_report,
        run_report=run_report,
    )


def render_run_report(
    trace: Mapping[str, object],
    comparison: Mapping[str, object],
    rollback: Mapping[str, object],
    boundary: Mapping[str, object],
    risk: Mapping[str, object],
) -> str:
    evaluation = trace["evaluation"]
    before = comparison["baseline"]
    after = comparison["candidate"]
    final_pass = (
        evaluation["decision"] == "retain"
        and rollback["status"] == "verified"
        and boundary["status"] in {"PASS", "PASS_PREPARED"}
    )
    clean_commit = trace["source_state"] == "clean_commit"
    if not final_pass:
        status_line = "Status: BLOCKED / failed local dry-run evidence"
        mode_line = "Mode: STUDIO / blocked"
        sync_line = (
            "GitHub sync state: no commit recommendation; repair and revalidate locally"
        )
        next_gate = "`FIX_OAL_001_LOCAL_FAILURE` — repair the failed evaluator, boundary or rollback proof before any commit."
    elif clean_commit:
        status_line = "Status: BIZ / clean local dry-run evidence"
        mode_line = "Mode: BIZ / local dry-run"
        sync_line = "GitHub sync state: local commit evidence; no push or pull request"
        next_gate = "`REVIEW_OAL_001_LOCAL_COMMIT` — review the local commit, trace, test results and rollback proof."
    else:
        status_line = "Status: STUDIO / manifest-bound pre-commit evidence"
        mode_line = "Mode: STUDIO / local dry-run bootstrap"
        sync_line = "GitHub sync state: prepared but not yet represented by the recorded Git HEAD"
        next_gate = "`COMPLETE_OAL_001_LOCAL_COMMIT` — commit the exact validated scope, then rerun on the clean local commit."
    return (
        "# OAL-001 Local Self-Modification Run Report\n\n"
        f"{status_line}\n"
        "Source: GitHub Issue #97 and the inspected OAL-1.0 Notion design baseline\n"
        f"Trace: `{trace['run_id']}` on `{trace['branch']}` from `{trace['base_sha']}`\n"
        "Boundary: Local candidate sandbox only; no external, remote, Notion, ledger, publication or payment mutation\n"
        f"{mode_line}\n"
        f"{sync_line}\n"
        "Notion source awareness: read-only design alignment; no Notion write\n\n"
        "## Outcome\n\n"
        f"- Governor: `{'APPROVED' if trace['governor']['approved'] else 'REJECTED'}`\n"
        f"- Evaluator: `{evaluation['decision'].upper()}`\n"
        f"- Boundary report: `{boundary['status']}`\n"
        f"- Rollback: `{rollback['status'].upper()}`\n"
        f"- Source state: `{trace['source_state']}`\n"
        f"- External mutation count: `{trace['external_mutation_count']}` "
        "(static allowlisted runtime-path observation)\n\n"
        "## Baseline vs Candidate\n\n"
        f"- Baseline exploration: `{before['strategy_weights']['exploration']}` "
        f"({before['route_counts']['exploration']} of {before['observation_count']} synthetic observations)\n"
        f"- Candidate exploration: `{after['strategy_weights']['exploration']}` "
        f"({after['route_counts']['exploration']} of {after['observation_count']} synthetic observations)\n"
        f"- Exploration delta: `{comparison['delta']['exploration_share']}` / "
        f"`{comparison['delta']['exploration_routes']}` route\n"
        f"- Baseline SHA-256: `{trace['baseline_sha256']}`\n"
        f"- Candidate SHA-256: `{trace['candidate_sha256']}`\n"
        f"- Diff SHA-256: `{trace['diff_sha256']}`\n\n"
        "## Isolation and Rollback\n\n"
        f"- Running baseline overwritten: `{str(trace['isolation']['running_version_overwritten']).lower()}`\n"
        f"- Baseline unchanged: `{str(rollback['baseline_unchanged']).lower()}`\n"
        f"- Candidate restored: `{str(rollback['candidate_restored']).lower()}`\n"
        f"- Candidate workspace removed: `{str(rollback['candidate_workspace_removed']).lower()}`\n"
        "- Candidate source executed: `false` (AST-constrained data replay only)\n\n"
        "## Evidence Status\n\n"
        "The fixture is `synthetic_current_slice` with `historical_evidence=false`. "
        "No predecessor Hubble or ALMA cycle is claimed.\n\n"
        "## Remaining Scope\n\n"
        + "\n".join(f"- {item}" for item in risk["remaining_risks"])
        + "\n\n## Recommended Next Gate\n\n"
        + next_gate
        + " "
        "Any push, PR, executable candidate sandbox, historical fixture admission or live ledger work requires a new explicit gate.\n"
    )


def validate_trace_payload(trace: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    missing = sorted(TRACE_REQUIRED_FIELDS - set(trace))
    extra = sorted(set(trace) - TRACE_REQUIRED_FIELDS)
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if extra:
        errors.append("unexpected fields: " + ", ".join(extra))
    if trace.get("schema_version") != "OAL-1.0":
        errors.append("schema_version must be OAL-1.0")
    if not isinstance(trace.get("run_id"), str) or not re.fullmatch(
        r"OAL-001-[A-F0-9]{16}", str(trace.get("run_id"))
    ):
        errors.append("run_id must match the deterministic OAL-001 format")
    if trace.get("cycle_id") != CYCLE_ID:
        errors.append("cycle_id must match the first-slice cycle")
    if trace.get("mode") != "local_dry_run":
        errors.append("mode must be local_dry_run")
    if trace.get("external_mutation_count") != 0:
        errors.append("external_mutation_count must be zero")
    if not isinstance(trace.get("base_sha"), str) or not GIT_SHA_PATTERN.fullmatch(
        str(trace.get("base_sha"))
    ):
        errors.append("base_sha must be a Git SHA")
    if not isinstance(trace.get("branch"), str) or not re.fullmatch(
        r"codex/observatory-selfmod-.+", str(trace.get("branch"))
    ):
        errors.append("branch must stay in the observatory self-modification lane")
    if trace.get("source_state") not in {"clean_commit", "working_tree_manifest"}:
        errors.append("source_state must describe clean or manifest-bound sources")
    for field in (
        "source_manifest_sha256",
        "baseline_sha256",
        "candidate_sha256",
        "diff_sha256",
    ):
        if not isinstance(trace.get(field), str) or not SHA256_PATTERN.fullmatch(
            str(trace.get(field))
        ):
            errors.append(f"{field} must be an uppercase SHA-256")
    if trace.get("baseline_sha256") == trace.get("candidate_sha256"):
        errors.append("candidate SHA-256 must differ from baseline")
    if trace.get("target_path") != TARGET_PATH:
        errors.append("target_path must remain the one mutable Observatory path")
    if trace.get("changed_paths") != [TARGET_PATH]:
        errors.append("changed_paths must contain exactly the mutable Observatory path")
    for field in ("trigger", "hypothesis", "expected_effect", "fallback_criterion"):
        if not isinstance(trace.get(field), str) or not str(trace.get(field)).strip():
            errors.append(f"{field} must be a non-empty string")
    diff = trace.get("diff")
    if not isinstance(diff, str) or not diff:
        errors.append("diff must be a non-empty string")
    elif trace.get("diff_sha256") != sha256_text(diff):
        errors.append("diff_sha256 does not match diff content")

    fixture = trace.get("fixture")
    fixture_keys = {
        "fixture_id",
        "fixture_kind",
        "historical_evidence",
        "historical_fixture_status",
    }
    if not isinstance(fixture, dict) or set(fixture) != fixture_keys:
        errors.append("fixture fields do not match the trace contract")
    else:
        if fixture.get("fixture_id") != CYCLE_ID:
            errors.append("fixture_id must match the synthetic first-slice fixture")
        if fixture.get("fixture_kind") != "synthetic_current_slice":
            errors.append("fixture_kind must be synthetic_current_slice")
        if fixture.get("historical_evidence") is not False:
            errors.append("fixture must explicitly deny historical evidence")
        if fixture.get("historical_fixture_status") != "unavailable":
            errors.append("historical_fixture_status must be unavailable")

    governor = trace.get("governor")
    if not isinstance(governor, dict) or set(governor) != {
        "approved",
        "reasons",
        "immutable_surface",
    }:
        errors.append("governor fields do not match the trace contract")
    else:
        if not isinstance(governor.get("approved"), bool):
            errors.append("governor approved must be boolean")
        if not isinstance(governor.get("reasons"), list) or not all(
            isinstance(item, str) for item in governor.get("reasons", [])
        ):
            errors.append("governor reasons must be a string list")
        if governor.get("immutable_surface") != "baseline_only":
            errors.append("governor immutable_surface must be baseline_only")
        if governor.get("approved") is True and governor.get("reasons"):
            errors.append("approved Governor trace must not contain rejection reasons")
        if governor.get("approved") is False and not governor.get("reasons"):
            errors.append("rejected Governor trace must contain rejection reasons")

    isolation = trace.get("isolation")
    if not isinstance(isolation, dict) or set(isolation) != {
        "candidate_workspace",
        "managed_paths",
        "running_version_overwritten",
    }:
        errors.append("isolation fields do not match the trace contract")
    else:
        if isolation.get("candidate_workspace") != "temporary_allowlist_copy":
            errors.append("candidate workspace must be the temporary allowlist copy")
        if isolation.get("managed_paths") != [TARGET_PATH]:
            errors.append("isolation managed_paths must match the mutable allowlist")
        if isolation.get("running_version_overwritten") is not False:
            errors.append("running version must not be overwritten")

    replay = trace.get("replay")
    if not isinstance(replay, dict) or set(replay) != {
        "baseline_deterministic",
        "candidate_deterministic",
        "before_artifact",
        "after_artifact",
    }:
        errors.append("replay fields do not match the trace contract")
    else:
        if replay.get("before_artifact") != "replay_before.json":
            errors.append("before replay artifact name is invalid")
        if replay.get("after_artifact") != "replay_after.json":
            errors.append("after replay artifact name is invalid")
        if not isinstance(replay.get("baseline_deterministic"), bool) or not isinstance(
            replay.get("candidate_deterministic"), bool
        ):
            errors.append("replay determinism fields must be boolean")

    evaluation = trace.get("evaluation")
    if not isinstance(evaluation, dict) or set(evaluation) != {
        "decision",
        "reasons",
        "checks",
    }:
        errors.append("evaluation fields do not match the trace contract")
    else:
        decision = evaluation.get("decision")
        checks = evaluation.get("checks")
        reasons = evaluation.get("reasons")
        if decision not in {"retain", "reject"}:
            errors.append("evaluation decision must be retain or reject")
        if (
            not isinstance(reasons, list)
            or not reasons
            or not all(isinstance(item, str) for item in reasons)
        ):
            errors.append("evaluation reasons must be a non-empty string list")
        if not isinstance(checks, dict) or set(checks) != EVALUATION_CHECK_NAMES:
            errors.append(
                "evaluation checks must match the exact first-slice check set"
            )
        elif not all(
            isinstance(name, str) and isinstance(passed, bool)
            for name, passed in checks.items()
        ):
            errors.append("evaluation checks must be boolean")
        elif decision == "retain" and not all(checks.values()):
            errors.append("retain decision requires every evaluation check to pass")
        elif decision == "reject" and all(checks.values()):
            errors.append(
                "reject decision requires at least one failed evaluation check"
            )

    rollback = trace.get("rollback")
    rollback_keys = {
        "status",
        "candidate_restored",
        "baseline_unchanged",
        "candidate_workspace_removed",
    }
    if not isinstance(rollback, dict) or set(rollback) != rollback_keys:
        errors.append("rollback fields do not match the trace contract")
    else:
        flags = [
            rollback.get("candidate_restored"),
            rollback.get("baseline_unchanged"),
            rollback.get("candidate_workspace_removed"),
        ]
        if not all(isinstance(flag, bool) for flag in flags):
            errors.append("rollback proof flags must be boolean")
        if rollback.get("status") == "verified" and not all(flags):
            errors.append("verified rollback requires every rollback proof flag")
        if rollback.get("status") == "failed" and all(flags):
            errors.append("failed rollback requires at least one failed proof flag")
        if rollback.get("status") not in {"verified", "failed"}:
            errors.append("rollback status must be verified or failed")
        if isinstance(evaluation, dict) and evaluation.get("decision") == "retain":
            if rollback.get("status") != "verified":
                errors.append("retain decision requires verified rollback")

    git_status = trace.get("git_status")
    git_status_keys = {"before", "after", "unchanged", "clean_worktree"}
    if not isinstance(git_status, dict) or set(git_status) != git_status_keys:
        errors.append("git_status fields do not match the trace contract")
    else:
        before = git_status.get("before")
        after = git_status.get("after")
        if not isinstance(before, str) or not isinstance(after, str):
            errors.append("git status snapshots must be strings")
        else:
            expected_unchanged = before == after
            expected_clean = git_status_is_clean(before) and git_status_is_clean(after)
            if git_status.get("unchanged") is not expected_unchanged:
                errors.append("git_status unchanged flag does not match snapshots")
            if git_status.get("clean_worktree") is not expected_clean:
                errors.append("git_status clean_worktree flag does not match snapshots")
            expected_state = (
                "clean_commit" if expected_clean else "working_tree_manifest"
            )
            if trace.get("source_state") != expected_state:
                errors.append("source_state does not match git cleanliness")

    if trace.get("not_actions") != list(NOT_ACTIONS):
        errors.append(
            "not_actions must match the complete first-slice prohibition list"
        )
    if isinstance(evaluation, dict) and evaluation.get("decision") == "retain":
        if not isinstance(governor, dict) or governor.get("approved") is not True:
            errors.append("retain decision requires Governor approval")
        if not isinstance(replay, dict) or not (
            replay.get("baseline_deterministic") is True
            and replay.get("candidate_deterministic") is True
        ):
            errors.append(
                "retain decision requires deterministic baseline and candidate replay"
            )
    return errors


def _git_check_ignored(repo_root: Path, rel_path: str) -> bool:
    return is_ignored(repo_root, rel_path)


def _git_status(repo_root: Path) -> str:
    return worktree_status(repo_root)


def git_status_is_clean(status: str) -> bool:
    lines = [line for line in status.splitlines() if line]
    return len(lines) == 1 and lines[0].startswith("## ")


def _prepare_output_dir(repo_root: Path, policy: GovernorPolicy, run_id: str) -> Path:
    output_root = repo_root / policy.output_root
    output_dir = output_root / run_id
    _reject_symlink_components(repo_root, output_dir, "output directory")
    resolved = _ensure_within(repo_root, output_dir, "output directory")
    expected_root = _ensure_within(repo_root, output_root, "output root")
    try:
        resolved.relative_to(expected_root)
    except ValueError as exc:
        raise CandidateBoundaryError(
            "output directory must stay below configured output root"
        ) from exc
    rel_path = resolved.relative_to(repo_root.resolve()).as_posix()
    if not _git_check_ignored(repo_root, rel_path):
        raise CandidateBoundaryError(
            f"output directory must be gitignored before writing: {rel_path}"
        )
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    target = _validate_writable_target(path.parent, path, "evidence target")
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _write_json(path: Path, payload: object) -> None:
    content = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    _atomic_write_bytes(path, content.encode("utf-8"))


def _write_text(path: Path, content: str) -> None:
    _atomic_write_bytes(path, content.encode("utf-8"))


def source_manifest_for_repo(repo_root: Path) -> list[dict[str, object]]:
    manifest: list[dict[str, object]] = []
    for rel_path in MANAGED_SOURCE_PATHS:
        data = read_managed_source(repo_root, rel_path)
        manifest.append(
            {"path": rel_path, "bytes": len(data), "sha256": sha256_bytes(data)}
        )
    return manifest


def write_cycle_artifacts(
    repo_root: Path, policy: GovernorPolicy, result: CycleResult
) -> Path:
    output_dir = _prepare_output_dir(repo_root.resolve(), policy, result.run_id)
    _write_json(
        output_dir / "validation_complete.json",
        {
            "schema_version": "OAL-1.0",
            "run_id": result.run_id,
            "status": "INCOMPLETE",
        },
    )
    _write_json(
        output_dir / "test_result.json",
        {
            "schema_version": "OAL-1.0",
            "run_id": result.run_id,
            "status": "NOT_RUN",
            "evidence_complete": False,
        },
    )
    payloads = {
        "mutation_trace.json": result.trace,
        "replay_before.json": result.replay_before,
        "replay_after.json": result.replay_after,
        "baseline_candidate_comparison.json": result.comparison,
        "rollback_proof.json": result.rollback_proof,
        "boundary_report.json": result.boundary_report,
        "risk_report.json": result.risk_report,
        "source_manifest.json": result.source_manifest,
        "claim_ledger.json": [
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
        ],
    }
    for name, payload in payloads.items():
        _write_json(output_dir / name, payload)
    _write_text(output_dir / "run_report.md", result.run_report)
    return output_dir
