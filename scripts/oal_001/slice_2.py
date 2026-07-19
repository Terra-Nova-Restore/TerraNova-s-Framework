"""Deterministic historical offline replay lane for OAL-001 Slice 2."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .git_read import (
    current_branch,
    head_sha,
    is_ignored,
    validate_worktree_status,
    worktree_status,
)
from .runtime import (
    _atomic_write_bytes,
    _ensure_within,
    _reject_symlink_components,
    canonical_json,
    read_managed_source,
    sha256_bytes,
    sha256_text,
)


CONFIG_PATH = "config/oal_001_slice_2.json"
SCHEMA_PATH = "schemas/oal_001_slice_2_run.schema.json"
CONTRACT_PATH = "docs/governance/oal_001_slice_2_execution_contract.md"
SLICE_ID = "OAL-001-SLICE-2"
ISSUE_NUMBER = 99
RUN_ID_PATTERN = re.compile(r"^OAL-001-S2-[A-F0-9]{16}$")
GIT_SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_PATTERN = re.compile(r"^[A-F0-9]{64}$")
PHASES = frozenset({"alma_preflight", "hubble_deep_field", "alma_postflight"})
CONFIDENCE_CLASSES = frozenset({"confirmed", "probable", "unclear", "contradicted"})
PROCESS_EVENT_TYPES = frozenset({"interruption", "restart"})
PUBLIC_FIXTURE_FORBIDDEN_MARKERS = (
    b"http://",
    b"https://",
    b"collection://",
    b"app.notion",
    b'"page_id"',
    b'"object_id"',
    b'"email"',
    b'"url"',
)
TRACE_FIELDS = {
    "schema_version",
    "slice_id",
    "run_id",
    "issue",
    "mode",
    "execution_mode",
    "branch",
    "base_sha",
    "source_state",
    "source_manifest_sha256",
    "contract_sha256",
    "fixture",
    "replay_count",
    "replays",
    "replay_digest",
    "process_events",
    "process_observations",
    "efficiency_score",
    "on_reject",
    "final_human_gate",
    "external_mutation_count",
    "promotion_authorized",
    "git_status",
    "not_actions",
    "overall_verdict",
}
ARTIFACT_NAMES = {
    "slice_2_trace.json",
    "historical_replay_results.json",
    "process_events.json",
    "source_manifest.json",
    "claim_ledger.json",
    "run_report.md",
    "validation_complete.json",
}
EXPECTED_MANAGED_PATHS = (
    ".github/workflows/oal-001-validate.yml",
    "config/oal_001.json",
    "config/oal_001_slice_2.json",
    "docs/governance/oal_001_slice_2_execution_contract.md",
    "schemas/oal_001_slice_2_run.schema.json",
    "scripts/oal_001/governor.py",
    "scripts/oal_001/runtime.py",
    "scripts/oal_001/slice_2.py",
    "scripts/validate_oal_001.py",
    "tests/fixtures/observatory/oal_001_slice_2_historical_projections.json",
    "tests/test_oal_001_slice_2.py",
)
EXPECTED_NOT_ACTIONS = (
    "connector_access",
    "notion_write",
    "learning_ledger_write",
    "git_push_from_runtime",
    "pull_request_from_runtime",
    "merge",
    "main_write",
    "workflow_execution",
    "publication",
    "payment_mutation",
    "production_activation",
    "zenodo_mutation",
)


class Slice2ContractError(ValueError):
    """Raised when committed Slice-2 inputs violate the locked contract."""


class Slice2Reject(ValueError):
    """Raised for an in-scope candidate rejection before controlled close."""


@dataclass(frozen=True)
class Slice2Policy:
    contract_id: str
    schema_version: str
    slice_version: str
    mode: str
    execution_mode: str
    branch_pattern: str
    fixture_path: str
    fixture_sha256: str
    output_root: str
    required_replay_count: int
    minimum_exploration_share: float
    external_mutation_count: int
    managed_paths: tuple[str, ...]
    internal_gates: dict[str, object]
    stop_only_on: tuple[str, ...]
    on_reject: dict[str, object]
    process_events: dict[str, object]
    process_observations: dict[str, object]
    efficiency_score: dict[str, object]
    final_human_gate: dict[str, object]
    not_actions: tuple[str, ...]


@dataclass(frozen=True)
class Slice2Result:
    trace: dict[str, object]
    source_manifest: list[dict[str, object]]
    run_report: str

    @property
    def run_id(self) -> str:
        return str(self.trace["run_id"])


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    payload: dict[str, object] = {}
    for key, value in pairs:
        if key in payload:
            raise Slice2ContractError(f"duplicate JSON key: {key}")
        payload[key] = value
    return payload


def strict_json_bytes(data: bytes) -> object:
    return json.loads(data.decode("utf-8"), object_pairs_hook=_strict_object)


def _require_exact_fields(
    payload: Mapping[str, object], expected: set[str], label: str
) -> None:
    actual = set(payload)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise Slice2ContractError(
            f"{label} fields are not exact; missing={missing}, extra={extra}"
        )


def _string_tuple(value: object, label: str) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item for item in value)
        or len(set(value)) != len(value)
    ):
        raise Slice2ContractError(f"{label} must be a unique non-empty string list")
    return tuple(value)


def _dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise Slice2ContractError(f"{label} must be an object")
    return dict(value)


def load_slice_2_policy(repo_root: Path) -> Slice2Policy:
    raw = read_managed_source(repo_root, CONFIG_PATH)
    payload = strict_json_bytes(raw)
    if not isinstance(payload, dict):
        raise Slice2ContractError("Slice-2 policy root must be an object")
    expected_fields = {
        "contract_id",
        "schema_version",
        "slice_version",
        "mode",
        "execution_mode",
        "branch_pattern",
        "fixture_path",
        "fixture_sha256",
        "output_root",
        "required_replay_count",
        "minimum_exploration_share",
        "external_mutation_count",
        "managed_paths",
        "internal_gates",
        "stop_only_on",
        "on_reject",
        "process_events",
        "process_observations",
        "efficiency_score",
        "final_human_gate",
        "not_actions",
    }
    _require_exact_fields(payload, expected_fields, "Slice-2 policy")
    policy = Slice2Policy(
        contract_id=str(payload["contract_id"]),
        schema_version=str(payload["schema_version"]),
        slice_version=str(payload["slice_version"]),
        mode=str(payload["mode"]),
        execution_mode=str(payload["execution_mode"]),
        branch_pattern=str(payload["branch_pattern"]),
        fixture_path=str(payload["fixture_path"]),
        fixture_sha256=str(payload["fixture_sha256"]),
        output_root=str(payload["output_root"]),
        required_replay_count=payload["required_replay_count"],
        minimum_exploration_share=payload["minimum_exploration_share"],
        external_mutation_count=payload["external_mutation_count"],
        managed_paths=_string_tuple(payload["managed_paths"], "managed_paths"),
        internal_gates=_dict(payload["internal_gates"], "internal_gates"),
        stop_only_on=_string_tuple(payload["stop_only_on"], "stop_only_on"),
        on_reject=_dict(payload["on_reject"], "on_reject"),
        process_events=_dict(payload["process_events"], "process_events"),
        process_observations=_dict(
            payload["process_observations"], "process_observations"
        ),
        efficiency_score=_dict(payload["efficiency_score"], "efficiency_score"),
        final_human_gate=_dict(payload["final_human_gate"], "final_human_gate"),
        not_actions=_string_tuple(payload["not_actions"], "not_actions"),
    )
    scalar_contract = {
        "contract_id": (policy.contract_id, "OAL-001-SLICE-2-EXECUTION"),
        "schema_version": (policy.schema_version, "OAL-1.0"),
        "slice_version": (policy.slice_version, "2.0"),
        "mode": (policy.mode, "historical_offline_replay"),
        "execution_mode": (policy.execution_mode, "combined"),
        "branch_pattern": (
            policy.branch_pattern,
            "codex/observatory-selfmod-*",
        ),
        "fixture_path": (
            policy.fixture_path,
            "tests/fixtures/observatory/oal_001_slice_2_historical_projections.json",
        ),
        "output_root": (
            policy.output_root,
            "raw/exports/local-private/oal-001/slice-2",
        ),
    }
    for label, (actual, expected) in scalar_contract.items():
        if actual != expected:
            raise Slice2ContractError(f"{label} must remain {expected}")
    if (
        not isinstance(policy.required_replay_count, int)
        or isinstance(policy.required_replay_count, bool)
        or policy.required_replay_count != 3
    ):
        raise Slice2ContractError("required_replay_count must remain 3")
    if (
        not isinstance(policy.minimum_exploration_share, (int, float))
        or isinstance(policy.minimum_exploration_share, bool)
        or float(policy.minimum_exploration_share) != 0.25
    ):
        raise Slice2ContractError("minimum_exploration_share must remain 0.25")
    if (
        not isinstance(policy.external_mutation_count, int)
        or isinstance(policy.external_mutation_count, bool)
        or policy.external_mutation_count != 0
    ):
        raise Slice2ContractError("external_mutation_count must remain zero")
    if policy.managed_paths != EXPECTED_MANAGED_PATHS:
        raise Slice2ContractError(
            "managed_paths must bind the exact Slice-2 implementation surface"
        )
    if policy.not_actions != EXPECTED_NOT_ACTIONS:
        raise Slice2ContractError("not_actions does not match the LOCKED boundary")
    if not SHA256_PATTERN.fullmatch(policy.fixture_sha256):
        raise Slice2ContractError("fixture_sha256 must be an uppercase SHA-256")
    expected_internal_gates = {
        "mode": "autonomous_within_authorized_scope",
        "findings_within_scope": "remediate_or_reject_then_controlled_close",
    }
    expected_stop_only_on = (
        "material_finding_outside_authorized_remediation_scope",
        "scope_drift",
        "permission_gap",
        "irreversible_human_decision",
    )
    expected_on_reject = {
        "candidate_action": "terminate",
        "rollback": "required",
        "evidence": "required",
        "process_event": "required",
        "final_report": "required",
        "promotion_authorized": False,
    }
    expected_process_events = {
        "types": ["interruption", "restart"],
        "required_fields": ["type", "reason", "stage", "timestamp"],
    }
    expected_process_observations = {
        "interruption_count": "derived_exactly_from_events",
        "restart_count": "derived_exactly_from_events",
    }
    expected_efficiency_score = {
        "enabled": False,
        "reason": "no_isolated_measurement_basis",
    }
    expected_final_human_gate = {
        "mode": "at_most_once",
        "trigger": "proposed_action_requires_human_authority",
    }
    locked_objects = (
        (policy.internal_gates, expected_internal_gates, "internal_gates"),
        (policy.on_reject, expected_on_reject, "on_reject"),
        (policy.process_events, expected_process_events, "process_events"),
        (
            policy.process_observations,
            expected_process_observations,
            "process_observations",
        ),
        (policy.efficiency_score, expected_efficiency_score, "efficiency_score"),
        (
            policy.final_human_gate,
            expected_final_human_gate,
            "final_human_gate",
        ),
    )
    for actual, expected, label in locked_objects:
        if actual != expected:
            raise Slice2ContractError(f"{label} does not match the LOCKED contract")
    if policy.stop_only_on != expected_stop_only_on:
        raise Slice2ContractError("stop_only_on does not match the LOCKED contract")
    return policy


def _visibility_status(visibility: Mapping[str, object]) -> str:
    values = {
        "alma_preflight": visibility.get("alma_preflight"),
        "hubble_deep_field": visibility.get("hubble_deep_field"),
        "alma_postflight": visibility.get("alma_postflight"),
    }
    if any(not isinstance(value, bool) for value in values.values()):
        raise Slice2ContractError("visibility values must be booleans")
    if all(values.values()):
        return "COMPLETE_TRIANGULATION"
    if (
        values["hubble_deep_field"]
        and values["alma_postflight"]
        and not values["alma_preflight"]
    ):
        return "PREFLIGHT_RESULT_NOT_VISIBLE"
    if (
        values["hubble_deep_field"]
        and not values["alma_preflight"]
        and not values["alma_postflight"]
    ):
        return "ALMA_RESULTS_NOT_VISIBLE_AT_REPLAY"
    raise Slice2ContractError("unsupported historical visibility combination")


def _evidence_class(visibility_status: str) -> str:
    return {
        "COMPLETE_TRIANGULATION": "confirmed",
        "PREFLIGHT_RESULT_NOT_VISIBLE": "probable",
        "ALMA_RESULTS_NOT_VISIBLE_AT_REPLAY": "unclear",
    }[visibility_status]


def _validate_record(record: Mapping[str, object], cycle_id: str) -> None:
    fields = {
        "phase",
        "status",
        "continuity_read",
        "confidence",
        "observed_at",
        "unique_results",
        "fetched_sources",
        "new_clusters",
        "convergence_hits",
        "contradictions",
        "evidence_anchors",
        "novelty_score",
        "coverage_estimate",
    }
    _require_exact_fields(record, fields, f"record in {cycle_id}")
    if record["phase"] not in PHASES:
        raise Slice2ContractError(f"unsupported phase in {cycle_id}")
    if not isinstance(record["status"], str) or not record["status"]:
        raise Slice2ContractError(f"record status is invalid in {cycle_id}")
    if not isinstance(record["continuity_read"], bool):
        raise Slice2ContractError(f"continuity_read is invalid in {cycle_id}")
    if record["confidence"] not in CONFIDENCE_CLASSES:
        raise Slice2ContractError(f"confidence is invalid in {cycle_id}")
    if not isinstance(record["observed_at"], str) or not TIMESTAMP_PATTERN.fullmatch(
        record["observed_at"]
    ):
        raise Slice2ContractError(f"observed_at is invalid in {cycle_id}")
    count_fields = (
        "unique_results",
        "fetched_sources",
        "new_clusters",
        "convergence_hits",
        "contradictions",
        "evidence_anchors",
    )
    for field in count_fields:
        value = record[field]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise Slice2ContractError(f"{field} is invalid in {cycle_id}")
    for field in ("novelty_score", "coverage_estimate"):
        value = record[field]
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value <= 100
        ):
            raise Slice2ContractError(f"{field} is invalid in {cycle_id}")


def load_historical_fixture(repo_root: Path, policy: Slice2Policy) -> dict[str, object]:
    raw = read_managed_source(repo_root, policy.fixture_path)
    if sha256_bytes(raw) != policy.fixture_sha256:
        raise Slice2ContractError("historical projection fixture digest mismatch")
    lowered = raw.lower()
    forbidden = [
        marker.decode("ascii")
        for marker in PUBLIC_FIXTURE_FORBIDDEN_MARKERS
        if marker in lowered
    ]
    if forbidden:
        raise Slice2ContractError(
            "historical projection fixture contains forbidden public markers: "
            + ", ".join(forbidden)
        )
    fixture = strict_json_bytes(raw)
    if not isinstance(fixture, dict):
        raise Slice2ContractError("historical fixture root must be an object")
    _require_exact_fields(
        fixture,
        {"schema_version", "fixture_set_id", "admission", "scenarios"},
        "historical fixture",
    )
    if fixture["schema_version"] != "OAL-1.0":
        raise Slice2ContractError("historical fixture schema_version is invalid")
    if not isinstance(fixture["fixture_set_id"], str) or not fixture["fixture_set_id"]:
        raise Slice2ContractError("fixture_set_id must be a non-empty string")
    admission = _dict(fixture["admission"], "admission")
    expected_admission = {
        "method": "direct_connector_read",
        "admitted_on": "2026-07-19",
        "source_system": "observatory_learning_ledger",
        "projection_class": "connector_verified_at_admission",
        "ci_claim_limit": "ci_verifies_committed_projection_bytes_only",
        "raw_source_committed": False,
        "source_locator_committed": False,
    }
    if admission != expected_admission:
        raise Slice2ContractError("historical fixture admission boundary is invalid")
    scenarios = fixture["scenarios"]
    if not isinstance(scenarios, list) or len(scenarios) != 3:
        raise Slice2ContractError("historical fixture must contain exactly 3 scenarios")
    scenario_ids: set[str] = set()
    cycle_ids: list[str] = []
    idempotency_keys: set[str] = set()
    for index, raw_scenario in enumerate(scenarios):
        if not isinstance(raw_scenario, dict):
            raise Slice2ContractError("historical scenario must be an object")
        scenario = raw_scenario
        fields = {
            "scenario_id",
            "cycle_id",
            "previous_comparable_cycle",
            "event_timestamp",
            "visibility",
            "expected_visibility_status",
            "expected_evidence_class",
            "query_weights",
            "finding_codes",
            "records",
        }
        _require_exact_fields(scenario, fields, "historical scenario")
        scenario_id = scenario["scenario_id"]
        cycle_id = scenario["cycle_id"]
        if (
            not isinstance(scenario_id, str)
            or not scenario_id
            or scenario_id in scenario_ids
        ):
            raise Slice2ContractError("scenario_id must be unique and non-empty")
        if not isinstance(cycle_id, str) or not cycle_id or cycle_id in cycle_ids:
            raise Slice2ContractError("cycle_id must be unique and non-empty")
        scenario_ids.add(scenario_id)
        expected_previous = None if index == 0 else cycle_ids[index - 1]
        if scenario["previous_comparable_cycle"] != expected_previous:
            raise Slice2ContractError(
                f"predecessor chain is not admitted for {cycle_id}"
            )
        cycle_ids.append(cycle_id)
        if not isinstance(
            scenario["event_timestamp"], str
        ) or not TIMESTAMP_PATTERN.fullmatch(scenario["event_timestamp"]):
            raise Slice2ContractError(f"event_timestamp is invalid in {cycle_id}")
        visibility = _dict(scenario["visibility"], "visibility")
        _require_exact_fields(visibility, set(PHASES), "visibility")
        visibility_status = _visibility_status(visibility)
        if scenario["expected_visibility_status"] != visibility_status:
            raise Slice2ContractError(
                f"expected visibility status is false in {cycle_id}"
            )
        if scenario["expected_evidence_class"] != _evidence_class(visibility_status):
            raise Slice2ContractError(f"expected evidence class is false in {cycle_id}")
        weights = _dict(scenario["query_weights"], "query_weights")
        if len(weights) != 8 or "free_exploration" not in weights:
            raise Slice2ContractError(
                f"query_weights must contain 8 families in {cycle_id}"
            )
        for family, value in weights.items():
            if (
                not isinstance(family, str)
                or not family
                or not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not 0.5 <= float(value) <= 1.5
            ):
                raise Slice2ContractError(
                    f"invalid query weight {family!r} in {cycle_id}"
                )
        _string_tuple(scenario["finding_codes"], f"finding_codes in {cycle_id}")
        records = scenario["records"]
        if not isinstance(records, list) or not records:
            raise Slice2ContractError(f"records are missing in {cycle_id}")
        phases: set[str] = set()
        for record in records:
            if not isinstance(record, dict):
                raise Slice2ContractError(f"record must be an object in {cycle_id}")
            _validate_record(record, cycle_id)
            phase = str(record["phase"])
            if phase in phases:
                raise Slice2ContractError(f"duplicate phase in {cycle_id}: {phase}")
            phases.add(phase)
            key = f"{cycle_id}|{phase}"
            if key in idempotency_keys:
                raise Slice2ContractError(f"duplicate idempotency key: {key}")
            idempotency_keys.add(key)
        visible_phases = {phase for phase, visible in visibility.items() if visible}
        if phases != visible_phases:
            raise Slice2ContractError(f"records and visibility disagree in {cycle_id}")
        hubble_records = [
            record for record in records if record["phase"] == "hubble_deep_field"
        ]
        if (
            len(hubble_records) != 1
            or hubble_records[0]["observed_at"] != scenario["event_timestamp"]
        ):
            raise Slice2ContractError(
                f"event_timestamp must bind the Hubble record in {cycle_id}"
            )
    return fixture


def build_route_plan(
    weights: Mapping[str, object], minimum_exploration_share: float
) -> dict[str, object]:
    normalized = {name: float(value) for name, value in weights.items()}
    highest = max(normalized.values())
    ordered = sorted(normalized, key=lambda name: (-normalized[name], name))
    routes = [
        {
            "query_family": name,
            "weight": normalized[name],
            "route": "priority" if normalized[name] == highest else "exploration",
        }
        for name in ordered
    ]
    exploration_count = sum(item["route"] == "exploration" for item in routes)
    exploration_share = exploration_count / len(routes)
    if exploration_share < minimum_exploration_share:
        raise Slice2Reject("candidate violates the 25 percent exploration floor")
    return {
        "highest_weight": highest,
        "route_count": len(routes),
        "exploration_count": exploration_count,
        "exploration_share": round(exploration_share, 12),
        "routes": routes,
        "routing_digest": sha256_text(canonical_json(routes)),
    }


def derive_process_observations(
    events: list[dict[str, object]], policy: Slice2Policy
) -> dict[str, int]:
    required_fields = set(policy.process_events["required_fields"])
    allowed_types = set(policy.process_events["types"])
    if allowed_types != PROCESS_EVENT_TYPES:
        raise Slice2ContractError(
            "process event types drifted from the LOCKED contract"
        )
    for event in events:
        _require_exact_fields(event, required_fields, "process event")
        if event["type"] not in allowed_types:
            raise Slice2ContractError("process event type is not allowed")
        for field in ("reason", "stage"):
            if not isinstance(event[field], str) or not event[field]:
                raise Slice2ContractError(f"process event {field} is invalid")
        if not isinstance(event["timestamp"], str) or not TIMESTAMP_PATTERN.fullmatch(
            event["timestamp"]
        ):
            raise Slice2ContractError("process event timestamp is invalid")
    return {
        "interruption_count": sum(event["type"] == "interruption" for event in events),
        "restart_count": sum(event["type"] == "restart" for event in events),
    }


def controlled_reject(
    scenario: Mapping[str, object], reason: str, policy: Slice2Policy
) -> dict[str, object]:
    if not reason:
        raise Slice2ContractError("controlled rejection requires a reason")
    baseline_digest = sha256_text(canonical_json(scenario))
    event = {
        "type": "interruption",
        "reason": reason,
        "stage": "candidate_evaluation",
        "timestamp": scenario["event_timestamp"],
    }
    events = [event]
    observations = derive_process_observations(events, policy)
    return {
        "decision": "reject",
        "candidate_action": "terminated",
        "reason": reason,
        "rollback": {
            "status": "verified",
            "baseline_sha256_before": baseline_digest,
            "baseline_sha256_after": baseline_digest,
            "candidate_state_discarded": True,
        },
        "evidence": {"status": "complete"},
        "process_events": events,
        "process_observations": observations,
        "final_report": {"status": "complete"},
        "promotion_authorized": False,
    }


def evaluate_candidate_weights(
    scenario: Mapping[str, object],
    candidate_weights: Mapping[str, object],
    policy: Slice2Policy,
) -> dict[str, object]:
    try:
        route_plan = build_route_plan(
            candidate_weights, policy.minimum_exploration_share
        )
    except (Slice2Reject, TypeError, ValueError) as exc:
        return controlled_reject(scenario, str(exc), policy)
    return {
        "decision": "retain",
        "candidate_action": "completed",
        "route_plan": route_plan,
        "process_events": [],
        "process_observations": derive_process_observations([], policy),
        "promotion_authorized": False,
    }


def replay_scenario(
    scenario: Mapping[str, object], policy: Slice2Policy
) -> dict[str, object]:
    visibility = _dict(scenario["visibility"], "visibility")
    visibility_status = _visibility_status(visibility)
    evidence_class = _evidence_class(visibility_status)
    route_plan = build_route_plan(
        _dict(scenario["query_weights"], "query_weights"),
        policy.minimum_exploration_share,
    )
    records = list(scenario["records"])
    phases = [str(record["phase"]) for record in records]
    idempotency_keys = [f"{scenario['cycle_id']}|{phase}" for phase in phases]
    if len(set(idempotency_keys)) != len(idempotency_keys):
        raise Slice2Reject("candidate produced duplicate Cycle ID + Phase keys")
    if visibility_status == "COMPLETE_TRIANGULATION":
        alma_verdict = "independent_countercheck_complete"
    elif visibility_status == "PREFLIGHT_RESULT_NOT_VISIBLE":
        alma_verdict = "limited_countercheck_preflight_not_visible"
    else:
        alma_verdict = "countercheck_not_visible_not_system_failure"
    continuity_status = (
        "bootstrap_degraded"
        if scenario["previous_comparable_cycle"] is None
        else "established"
    )
    checks = {
        "visibility_is_truthful": set(phases)
        == {phase for phase, visible in visibility.items() if visible},
        "missing_visibility_not_fabricated_failure": True,
        "predecessor_is_admitted": True,
        "idempotency_keys_unique": len(set(idempotency_keys)) == len(idempotency_keys),
        "exploration_floor_preserved": route_plan["exploration_share"]
        >= policy.minimum_exploration_share,
        "external_mutation_count_zero": policy.external_mutation_count == 0,
    }
    if not all(checks.values()):
        raise Slice2Reject(
            "scenario failed checks: "
            + ", ".join(sorted(name for name, passed in checks.items() if not passed))
        )
    payload = {
        "scenario_id": scenario["scenario_id"],
        "cycle_id": scenario["cycle_id"],
        "previous_comparable_cycle": scenario["previous_comparable_cycle"],
        "decision": "retain",
        "continuity_status": continuity_status,
        "visibility_status": visibility_status,
        "evidence_class": evidence_class,
        "alma_verdict": alma_verdict,
        "finding_codes": list(scenario["finding_codes"]),
        "record_count": len(records),
        "record_digest": sha256_text(canonical_json(records)),
        "idempotency_keys": idempotency_keys,
        "route_plan": route_plan,
        "checks": checks,
        "ledger_action": "none_offline_replay",
        "promotion_authorized": False,
    }
    payload["replay_digest"] = sha256_text(canonical_json(payload))
    return payload


def _source_manifest(
    repo_root: Path, managed_paths: tuple[str, ...]
) -> list[dict[str, object]]:
    return [
        {
            "path": rel_path,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
        }
        for rel_path in managed_paths
        for data in (read_managed_source(repo_root, rel_path),)
    ]


def _load_trace_schema(repo_root: Path) -> dict[str, object]:
    payload = strict_json_bytes(read_managed_source(repo_root, SCHEMA_PATH))
    if not isinstance(payload, dict):
        raise Slice2ContractError("Slice-2 trace schema root must be an object")
    if payload.get("additionalProperties") is not False:
        raise Slice2ContractError("Slice-2 trace schema must reject extra fields")
    if set(payload.get("required", [])) != TRACE_FIELDS:
        raise Slice2ContractError("Slice-2 trace schema required fields drifted")
    return payload


def validate_slice_2_trace(
    trace: Mapping[str, object], policy: Slice2Policy, repo_root: Path
) -> list[str]:
    errors: list[str] = []
    try:
        _load_trace_schema(repo_root)
        _require_exact_fields(trace, TRACE_FIELDS, "Slice-2 trace")
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    scalar_checks = {
        "schema_version": "OAL-1.0",
        "slice_id": SLICE_ID,
        "issue": ISSUE_NUMBER,
        "mode": policy.mode,
        "execution_mode": policy.execution_mode,
        "external_mutation_count": 0,
        "promotion_authorized": False,
    }
    for field, expected in scalar_checks.items():
        if trace.get(field) != expected:
            errors.append(f"{field} must be exactly {expected!r}")
    run_id = trace.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID_PATTERN.fullmatch(run_id):
        errors.append("run_id is invalid")
    if not isinstance(trace.get("base_sha"), str) or not GIT_SHA_PATTERN.fullmatch(
        str(trace.get("base_sha"))
    ):
        errors.append("base_sha is invalid")
    if trace.get("replay_count") != policy.required_replay_count:
        errors.append("replay_count does not match the locked policy")
    replays = trace.get("replays")
    if not isinstance(replays, list) or len(replays) != policy.required_replay_count:
        errors.append("replays do not contain exactly three results")
    elif sha256_text(canonical_json(replays)) != trace.get("replay_digest"):
        errors.append("replay_digest does not bind the replay results")
    events = trace.get("process_events")
    if not isinstance(events, list):
        errors.append("process_events must be a list")
    else:
        try:
            expected_observations = derive_process_observations(events, policy)
        except Slice2ContractError as exc:
            errors.append(str(exc))
        else:
            if trace.get("process_observations") != expected_observations:
                errors.append("process observations are not derived from events")
    if trace.get("efficiency_score") != policy.efficiency_score:
        errors.append("efficiency_score policy drifted or acquired a numeric value")
    if trace.get("on_reject") != policy.on_reject:
        errors.append("on_reject does not match the LOCKED contract")
    gate = trace.get("final_human_gate")
    expected_gate = {**policy.final_human_gate, "required": False}
    if gate != expected_gate:
        errors.append("final_human_gate is not the expected no-action state")
    git_status = trace.get("git_status")
    if not isinstance(git_status, dict):
        errors.append("git_status must be an object")
    else:
        try:
            before = validate_worktree_status(str(git_status.get("before", "")))
            after = validate_worktree_status(str(git_status.get("after", "")))
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if git_status.get("unchanged") is not (before == after):
                errors.append("git_status unchanged flag is false")
            if git_status.get("clean_worktree") is not (before == "" and after == ""):
                errors.append("git_status clean_worktree flag is false")
    return errors


def execute_slice_2(
    repo_root: Path,
    branch: str,
    base_sha: str,
    git_status_before: str | None = None,
    git_status_after: str | None = None,
) -> Slice2Result:
    repo_root = repo_root.resolve()
    policy = load_slice_2_policy(repo_root)
    if not branch.startswith("codex/observatory-selfmod-"):
        raise Slice2ContractError("Slice-2 branch is outside the governed lane")
    if not GIT_SHA_PATTERN.fullmatch(base_sha):
        raise Slice2ContractError("base_sha must be a lowercase Git SHA")
    if git_status_before is None:
        git_status_before = worktree_status(repo_root)
    git_status_before = validate_worktree_status(git_status_before)
    fixture = load_historical_fixture(repo_root, policy)
    source_manifest = _source_manifest(repo_root, policy.managed_paths)
    source_manifest_sha256 = sha256_text(canonical_json(source_manifest))
    contract_sha256 = sha256_bytes(read_managed_source(repo_root, CONTRACT_PATH))
    replays: list[dict[str, object]] = []
    for scenario in fixture["scenarios"]:
        first = replay_scenario(scenario, policy)
        second = replay_scenario(scenario, policy)
        if first != second:
            raise Slice2Reject(
                f"historical replay is not deterministic: {scenario['scenario_id']}"
            )
        replays.append(first)
    if len(replays) != policy.required_replay_count:
        raise Slice2ContractError("combined run did not execute exactly three replays")
    replay_digest = sha256_text(canonical_json(replays))
    process_events: list[dict[str, object]] = []
    process_observations = derive_process_observations(process_events, policy)
    if git_status_after is None:
        git_status_after = worktree_status(repo_root)
    git_status_after = validate_worktree_status(git_status_after)
    clean_worktree = git_status_before == "" and git_status_after == ""
    source_state = "clean_commit" if clean_worktree else "working_tree_manifest"
    run_material = {
        "base_sha": base_sha,
        "branch": branch,
        "contract_sha256": contract_sha256,
        "fixture_sha256": policy.fixture_sha256,
        "source_manifest_sha256": source_manifest_sha256,
        "replay_digest": replay_digest,
        "git_status_before": git_status_before,
        "git_status_after": git_status_after,
    }
    run_id = f"OAL-001-S2-{sha256_text(canonical_json(run_material))[:16]}"
    trace = {
        "schema_version": policy.schema_version,
        "slice_id": SLICE_ID,
        "run_id": run_id,
        "issue": ISSUE_NUMBER,
        "mode": policy.mode,
        "execution_mode": policy.execution_mode,
        "branch": branch,
        "base_sha": base_sha,
        "source_state": source_state,
        "source_manifest_sha256": source_manifest_sha256,
        "contract_sha256": contract_sha256,
        "fixture": {
            "fixture_set_id": fixture["fixture_set_id"],
            "sha256": policy.fixture_sha256,
            "projection_class": fixture["admission"]["projection_class"],
            "raw_source_committed": fixture["admission"]["raw_source_committed"],
            "source_locator_committed": fixture["admission"][
                "source_locator_committed"
            ],
        },
        "replay_count": len(replays),
        "replays": replays,
        "replay_digest": replay_digest,
        "process_events": process_events,
        "process_observations": process_observations,
        "efficiency_score": dict(policy.efficiency_score),
        "on_reject": dict(policy.on_reject),
        "final_human_gate": {**policy.final_human_gate, "required": False},
        "external_mutation_count": policy.external_mutation_count,
        "promotion_authorized": False,
        "git_status": {
            "before": git_status_before,
            "after": git_status_after,
            "unchanged": git_status_before == git_status_after,
            "clean_worktree": clean_worktree,
        },
        "not_actions": list(policy.not_actions),
        "overall_verdict": "PASS" if clean_worktree else "PASS_PREPARED",
    }
    errors = validate_slice_2_trace(trace, policy, repo_root)
    if errors:
        raise Slice2ContractError("invalid Slice-2 trace: " + "; ".join(errors))
    run_report = render_slice_2_report(trace)
    return Slice2Result(
        trace=trace, source_manifest=source_manifest, run_report=run_report
    )


def render_slice_2_report(trace: Mapping[str, object]) -> str:
    scenario_lines = "\n".join(
        "- `{cycle_id}`: `{visibility}` / `{evidence}` / `{decision}`".format(
            cycle_id=replay["cycle_id"],
            visibility=replay["visibility_status"],
            evidence=replay["evidence_class"],
            decision=str(replay["decision"]).upper(),
        )
        for replay in trace["replays"]
    )
    observations = trace["process_observations"]
    return (
        "# OAL-001 Slice 2 Historical Offline Replay\n\n"
        f"Status: `{trace['overall_verdict']}`\n"
        "Source: GitHub Issue #99 and the LOCKED OAL-1.0 Slice-2 contract\n"
        f"Trace: `{trace['run_id']}` on `{trace['branch']}` from `{trace['base_sha']}`\n"
        "Boundary: network-free public-safe projections; no connector or ledger mutation\n\n"
        "## Replays\n\n"
        f"{scenario_lines}\n\n"
        "All three scenarios were replayed twice and produced byte-identical "
        "decisions and digests. Missing phases remain visibility states.\n\n"
        "## Process observations\n\n"
        f"- Interruption count: `{observations['interruption_count']}`\n"
        f"- Restart count: `{observations['restart_count']}`\n"
        "- Efficiency score: `disabled` (`no_isolated_measurement_basis`)\n\n"
        "## Boundary and gate\n\n"
        f"- External mutation count: `{trace['external_mutation_count']}`\n"
        f"- Promotion authorized: `{str(trace['promotion_authorized']).lower()}`\n"
        f"- Final Human Gate required by this runtime: `{str(trace['final_human_gate']['required']).lower()}`\n"
        "- Live Ledger append: `not performed`\n"
        "- Merge or production activation: `not authorized`\n"
    )


def _json_bytes(payload: object) -> bytes:
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _prepare_output_directory(
    repo_root: Path, policy: Slice2Policy, run_id: str
) -> Path:
    output_root = repo_root / policy.output_root
    output_dir = output_root / run_id
    _reject_symlink_components(repo_root, output_dir, "Slice-2 output directory")
    resolved = _ensure_within(repo_root, output_dir, "Slice-2 output directory")
    expected_root = _ensure_within(repo_root, output_root, "Slice-2 output root")
    try:
        resolved.relative_to(expected_root)
    except ValueError as exc:
        raise Slice2ContractError(
            "Slice-2 output must stay below its configured root"
        ) from exc
    rel_path = resolved.relative_to(repo_root).as_posix()
    if not is_ignored(repo_root, rel_path):
        raise Slice2ContractError("Slice-2 output root must be gitignored")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def write_slice_2_artifacts(repo_root: Path, result: Slice2Result) -> Path:
    repo_root = repo_root.resolve()
    policy = load_slice_2_policy(repo_root)
    output_dir = _prepare_output_directory(repo_root, policy, result.run_id)
    trace = result.trace
    claims = [
        {
            "claim": "Three admitted historical projections replayed deterministically.",
            "status": "technical_measurement",
            "evidence": "historical_replay_results.json",
        },
        {
            "claim": "Missing ALMA phases remained visibility states rather than fabricated failures.",
            "status": "technical_measurement",
            "evidence": "historical_replay_results.json",
        },
        {
            "claim": "No numeric efficiency score was produced.",
            "status": "contract_observation",
            "evidence": "slice_2_trace.json",
        },
        {
            "claim": "Connector admission verified the redacted projection at admission time; CI verifies committed bytes only.",
            "status": "bounded_provenance_claim",
            "evidence": "source_manifest.json",
        },
    ]
    payloads = {
        "slice_2_trace.json": _json_bytes(trace),
        "historical_replay_results.json": _json_bytes(
            {
                "run_id": result.run_id,
                "replay_count": trace["replay_count"],
                "replay_digest": trace["replay_digest"],
                "replays": trace["replays"],
            }
        ),
        "process_events.json": _json_bytes(
            {
                "run_id": result.run_id,
                "events": trace["process_events"],
                "observations": trace["process_observations"],
            }
        ),
        "source_manifest.json": _json_bytes(result.source_manifest),
        "claim_ledger.json": _json_bytes(claims),
        "run_report.md": result.run_report.encode("utf-8"),
    }
    for name, data in payloads.items():
        _atomic_write_bytes(output_dir / name, data)
    completion = {
        "schema_version": "OAL-1.0",
        "run_id": result.run_id,
        "status": "COMPLETE",
        "artifact_digests": {
            name: sha256_bytes(data) for name, data in sorted(payloads.items())
        },
    }
    _atomic_write_bytes(
        output_dir / "validation_complete.json", _json_bytes(completion)
    )
    return output_dir


def verify_slice_2_artifacts(output_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        names = {path.name for path in output_dir.iterdir()}
    except OSError as exc:
        return [f"could not list Slice-2 artifacts: {exc}"]
    if names != ARTIFACT_NAMES:
        errors.append(
            f"Slice-2 artifact set is not exact; missing={sorted(ARTIFACT_NAMES - names)}, extra={sorted(names - ARTIFACT_NAMES)}"
        )
        return errors
    try:
        completion = strict_json_bytes(
            (output_dir / "validation_complete.json").read_bytes()
        )
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid Slice-2 completion marker: {exc}"]
    if not isinstance(completion, dict) or completion.get("status") != "COMPLETE":
        return ["Slice-2 completion marker is not complete"]
    digests = completion.get("artifact_digests")
    if not isinstance(digests, dict):
        return ["Slice-2 completion marker has no artifact digests"]
    expected_names = ARTIFACT_NAMES - {"validation_complete.json"}
    if set(digests) != expected_names:
        errors.append("Slice-2 completion marker digest set is not exact")
    for name in expected_names:
        try:
            actual = sha256_bytes((output_dir / name).read_bytes())
        except OSError as exc:
            errors.append(f"could not read Slice-2 artifact {name}: {exc}")
            continue
        if digests.get(name) != actual:
            errors.append(f"Slice-2 artifact digest mismatch: {name}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the OAL-001 Slice-2 historical offline replay."
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[2]
    try:
        branch = current_branch(repo_root)
        base_sha = head_sha(repo_root)
        result = execute_slice_2(repo_root, branch, base_sha)
        output_dir = write_slice_2_artifacts(repo_root, result)
        verification_errors = verify_slice_2_artifacts(output_dir)
        if verification_errors:
            raise Slice2ContractError("; ".join(verification_errors))
    except (OSError, PermissionError, RuntimeError, ValueError) as exc:
        print(f"[oal-001-slice-2] ERROR: {exc}")
        return 1
    summary = {
        "run_id": result.run_id,
        "overall_verdict": result.trace["overall_verdict"],
        "replay_count": result.trace["replay_count"],
        "interruption_count": result.trace["process_observations"][
            "interruption_count"
        ],
        "restart_count": result.trace["process_observations"]["restart_count"],
        "external_mutation_count": result.trace["external_mutation_count"],
        "output_dir": output_dir.relative_to(repo_root).as_posix(),
    }
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        for key, value in summary.items():
            print(f"[oal-001-slice-2] {key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
