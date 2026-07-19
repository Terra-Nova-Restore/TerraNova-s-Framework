from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from scripts.oal_001.slice_2 import (
    ARTIFACT_NAMES,
    EXPECTED_MANAGED_PATHS,
    EXPECTED_NOT_ACTIONS,
    PUBLIC_FIXTURE_FORBIDDEN_MARKERS,
    TRACE_FIELDS,
    Slice2ContractError,
    build_route_plan,
    controlled_reject,
    derive_process_observations,
    evaluate_candidate_weights,
    execute_slice_2,
    load_historical_fixture,
    load_slice_2_policy,
    replay_scenario,
    sha256_bytes,
    strict_json_bytes,
    verify_slice_2_artifacts,
    write_slice_2_artifacts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "a" * 40
BRANCH = "codex/observatory-selfmod-002"


class Oal001Slice2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_slice_2_policy(REPO_ROOT)
        cls.fixture = load_historical_fixture(REPO_ROOT, cls.policy)

    def test_locked_contract_is_exact(self) -> None:
        self.assertEqual(self.policy.execution_mode, "combined")
        self.assertEqual(
            self.policy.internal_gates,
            {
                "mode": "autonomous_within_authorized_scope",
                "findings_within_scope": "remediate_or_reject_then_controlled_close",
            },
        )
        self.assertEqual(self.policy.final_human_gate["mode"], "at_most_once")
        self.assertFalse(self.policy.efficiency_score["enabled"])
        self.assertNotIn("value", self.policy.efficiency_score)
        self.assertEqual(self.policy.managed_paths, EXPECTED_MANAGED_PATHS)
        self.assertEqual(self.policy.not_actions, EXPECTED_NOT_ACTIONS)

    def test_fixture_is_connector_admitted_and_public_safe(self) -> None:
        raw = (REPO_ROOT / self.policy.fixture_path).read_bytes()
        self.assertEqual(sha256_bytes(raw), self.policy.fixture_sha256)
        self.assertEqual(
            self.fixture["admission"]["projection_class"],
            "connector_verified_at_admission",
        )
        self.assertFalse(self.fixture["admission"]["raw_source_committed"])
        self.assertFalse(self.fixture["admission"]["source_locator_committed"])
        lowered = raw.lower()
        self.assertFalse(
            [marker for marker in PUBLIC_FIXTURE_FORBIDDEN_MARKERS if marker in lowered]
        )

    def test_fixture_has_three_chained_visibility_scenarios(self) -> None:
        scenarios = self.fixture["scenarios"]
        self.assertEqual(len(scenarios), 3)
        self.assertIsNone(scenarios[0]["previous_comparable_cycle"])
        self.assertEqual(
            scenarios[1]["previous_comparable_cycle"], scenarios[0]["cycle_id"]
        )
        self.assertEqual(
            scenarios[2]["previous_comparable_cycle"], scenarios[1]["cycle_id"]
        )
        self.assertEqual(
            [item["expected_visibility_status"] for item in scenarios],
            [
                "COMPLETE_TRIANGULATION",
                "PREFLIGHT_RESULT_NOT_VISIBLE",
                "ALMA_RESULTS_NOT_VISIBLE_AT_REPLAY",
            ],
        )

    def test_each_replay_is_deterministic(self) -> None:
        for scenario in self.fixture["scenarios"]:
            first = replay_scenario(scenario, self.policy)
            second = replay_scenario(scenario, self.policy)
            self.assertEqual(first, second)
            self.assertEqual(first["decision"], "retain")
            self.assertFalse(first["promotion_authorized"])

    def test_visibility_is_not_converted_to_system_failure(self) -> None:
        replays = [
            replay_scenario(scenario, self.policy)
            for scenario in self.fixture["scenarios"]
        ]
        self.assertEqual(
            replays[1]["alma_verdict"],
            "limited_countercheck_preflight_not_visible",
        )
        self.assertEqual(
            replays[2]["alma_verdict"],
            "countercheck_not_visible_not_system_failure",
        )
        self.assertTrue(
            all(
                replay["checks"]["missing_visibility_not_fabricated_failure"]
                for replay in replays
            )
        )

    def test_exploration_floor_is_derived_from_routes(self) -> None:
        for scenario in self.fixture["scenarios"]:
            plan = build_route_plan(
                scenario["query_weights"], self.policy.minimum_exploration_share
            )
            exploration_count = sum(
                route["route"] == "exploration" for route in plan["routes"]
            )
            self.assertEqual(exploration_count, plan["exploration_count"])
            self.assertGreaterEqual(plan["exploration_share"], 0.25)

    def test_idempotency_keys_are_unique_across_all_records(self) -> None:
        keys = [
            key
            for scenario in self.fixture["scenarios"]
            for key in replay_scenario(scenario, self.policy)["idempotency_keys"]
        ]
        self.assertEqual(len(keys), len(set(keys)))

    def test_combined_run_executes_exactly_three_replays(self) -> None:
        result = execute_slice_2(
            REPO_ROOT, BRANCH, BASE_SHA, git_status_before="", git_status_after=""
        )
        self.assertEqual(result.trace["replay_count"], 3)
        self.assertEqual(result.trace["overall_verdict"], "PASS")
        self.assertEqual(result.trace["source_state"], "clean_commit")
        self.assertEqual(result.trace["process_events"], [])
        self.assertEqual(
            result.trace["process_observations"],
            {"interruption_count": 0, "restart_count": 0},
        )
        self.assertEqual(set(result.trace), TRACE_FIELDS)
        self.assertEqual(
            tuple(item["path"] for item in result.source_manifest),
            EXPECTED_MANAGED_PATHS,
        )

    def test_dirty_run_is_prepared_but_never_promoted(self) -> None:
        status = "?? bounded-slice-2-change"
        result = execute_slice_2(
            REPO_ROOT,
            BRANCH,
            BASE_SHA,
            git_status_before=status,
            git_status_after=status,
        )
        self.assertEqual(result.trace["overall_verdict"], "PASS_PREPARED")
        self.assertEqual(result.trace["source_state"], "working_tree_manifest")
        self.assertFalse(result.trace["promotion_authorized"])

    def test_process_counts_are_exactly_derived_from_events(self) -> None:
        events = [
            {
                "type": "interruption",
                "reason": "candidate_rejected",
                "stage": "candidate_evaluation",
                "timestamp": "2026-07-17T04:03:00Z",
            },
            {
                "type": "restart",
                "reason": "bounded_retry",
                "stage": "historical_replay",
                "timestamp": "2026-07-17T10:01:00Z",
            },
        ]
        self.assertEqual(
            derive_process_observations(events, self.policy),
            {"interruption_count": 1, "restart_count": 1},
        )

    def test_controlled_reject_terminates_candidate_then_closes(self) -> None:
        scenario = self.fixture["scenarios"][0]
        rejected = controlled_reject(
            scenario, "candidate violates the exploration floor", self.policy
        )
        self.assertEqual(rejected["decision"], "reject")
        self.assertEqual(rejected["candidate_action"], "terminated")
        self.assertEqual(rejected["rollback"]["status"], "verified")
        self.assertTrue(rejected["rollback"]["candidate_state_discarded"])
        self.assertEqual(rejected["evidence"]["status"], "complete")
        self.assertEqual(rejected["final_report"]["status"], "complete")
        self.assertEqual(
            rejected["process_observations"],
            {"interruption_count": 1, "restart_count": 0},
        )
        self.assertFalse(rejected["promotion_authorized"])

    def test_invalid_candidate_weights_take_controlled_reject_path(self) -> None:
        scenario = self.fixture["scenarios"][0]
        all_priority = {name: 1.0 for name in scenario["query_weights"]}
        first = evaluate_candidate_weights(scenario, all_priority, self.policy)
        second = evaluate_candidate_weights(scenario, all_priority, self.policy)
        self.assertEqual(first, second)
        self.assertEqual(first["decision"], "reject")
        self.assertEqual(first["candidate_action"], "terminated")

    def test_tampered_fixture_digest_is_rejected(self) -> None:
        raw = (REPO_ROOT / self.policy.fixture_path).read_bytes() + b"\n"
        with mock.patch(
            "scripts.oal_001.slice_2.read_managed_source", return_value=raw
        ):
            with self.assertRaisesRegex(Slice2ContractError, "digest mismatch"):
                load_historical_fixture(REPO_ROOT, self.policy)

    def test_invented_predecessor_is_rejected(self) -> None:
        payload = json.loads(
            (REPO_ROOT / self.policy.fixture_path).read_text(encoding="utf-8")
        )
        payload["scenarios"][1]["previous_comparable_cycle"] = "INVENTED"
        raw = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        policy = replace(self.policy, fixture_sha256=sha256_bytes(raw))
        with mock.patch(
            "scripts.oal_001.slice_2.read_managed_source", return_value=raw
        ):
            with self.assertRaisesRegex(Slice2ContractError, "predecessor chain"):
                load_historical_fixture(REPO_ROOT, policy)

    def test_duplicate_phase_is_rejected(self) -> None:
        payload = json.loads(
            (REPO_ROOT / self.policy.fixture_path).read_text(encoding="utf-8")
        )
        duplicate = dict(payload["scenarios"][0]["records"][0])
        payload["scenarios"][0]["records"].append(duplicate)
        raw = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        policy = replace(self.policy, fixture_sha256=sha256_bytes(raw))
        with mock.patch(
            "scripts.oal_001.slice_2.read_managed_source", return_value=raw
        ):
            with self.assertRaisesRegex(Slice2ContractError, "duplicate phase"):
                load_historical_fixture(REPO_ROOT, policy)

    def test_trace_schema_is_strict_and_matches_runtime(self) -> None:
        schema = strict_json_bytes(
            (REPO_ROOT / "schemas/oal_001_slice_2_run.schema.json").read_bytes()
        )
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), TRACE_FIELDS)
        self.assertNotIn(
            "value", schema["properties"]["efficiency_score"]["properties"]
        )

    def test_artifact_bundle_is_exact_and_digest_bound(self) -> None:
        result = execute_slice_2(
            REPO_ROOT, BRANCH, BASE_SHA, git_status_before="", git_status_after=""
        )
        output_dir = write_slice_2_artifacts(REPO_ROOT, result)
        self.assertEqual({path.name for path in output_dir.iterdir()}, ARTIFACT_NAMES)
        self.assertEqual(verify_slice_2_artifacts(output_dir), [])
        report = output_dir / "run_report.md"
        original = report.read_bytes()
        try:
            report.write_bytes(original + b"tamper")
            self.assertIn(
                "Slice-2 artifact digest mismatch: run_report.md",
                verify_slice_2_artifacts(output_dir),
            )
        finally:
            write_slice_2_artifacts(REPO_ROOT, result)


if __name__ == "__main__":
    unittest.main()
