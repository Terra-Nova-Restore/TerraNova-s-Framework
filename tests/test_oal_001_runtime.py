from __future__ import annotations

import ast
import copy
import json
import os
import stat
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch as mock_patch

from scripts.oal_001.governor import Governor, load_policy
from scripts.oal_001.__main__ import git_branch, git_head
from scripts.oal_001.runtime import (
    CandidateBoundaryError,
    CandidateWorkspace,
    PatchEvaluator,
    ReplayHarness,
    TARGET_PATH,
    _is_reparse_point,
    _git_status,
    build_harmless_patch,
    execute_cycle,
    load_fixture,
    parse_strategy_source,
    read_managed_source,
    sha256_bytes,
    validate_trace_payload,
    write_cycle_artifacts,
)
from scripts.validate_oal_001 import (
    _artifact_digest_map,
    _atomic_write_json,
    _subprocess_boundary_errors,
    run_unit_tests,
    unit_test_gate_errors,
    validate_artifacts,
    validate_completion_marker,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "e" * 40
BRANCH = "codex/observatory-selfmod-001"


class Oal001RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_policy(REPO_ROOT)

    def execute(self, temp_parent: Path | None = None):
        return execute_cycle(
            REPO_ROOT,
            self.policy,
            BRANCH,
            BASE_SHA,
            git_status_before="## synthetic-test",
            git_status_after="## synthetic-test",
            temp_parent=temp_parent,
        )

    def test_baseline_strategy_is_data_only_and_meets_floor(self) -> None:
        weights = parse_strategy_source(REPO_ROOT / TARGET_PATH)

        self.assertEqual(weights, {"primary": 0.75, "exploration": 0.25})
        self.assertGreaterEqual(
            weights["exploration"], self.policy.minimum_exploration_share
        )

    def test_fixture_is_explicitly_synthetic_not_historical(self) -> None:
        fixture = load_fixture(REPO_ROOT, self.policy.fixture_path)

        self.assertEqual(fixture["fixture_kind"], "synthetic_current_slice")
        self.assertFalse(fixture["historical_evidence"])

    def test_replay_is_deterministic_for_same_input(self) -> None:
        fixture = load_fixture(REPO_ROOT, self.policy.fixture_path)
        harness = ReplayHarness(fixture)

        first = harness.replay(REPO_ROOT / TARGET_PATH)
        second = harness.replay(REPO_ROOT / TARGET_PATH)

        self.assertEqual(first, second)
        self.assertEqual(first.route_counts, {"primary": 15, "exploration": 5})

    def test_end_to_end_candidate_is_retained_then_rolled_back(self) -> None:
        baseline_before = sha256_bytes(read_managed_source(REPO_ROOT, TARGET_PATH))

        result = self.execute()

        baseline_after = sha256_bytes(read_managed_source(REPO_ROOT, TARGET_PATH))
        self.assertEqual(result.trace["evaluation"]["decision"], "retain")
        self.assertEqual(result.replay_after["route_counts"]["exploration"], 6)
        self.assertEqual(result.comparison["delta"]["exploration_routes"], 1)
        self.assertEqual(result.rollback_proof["status"], "verified")
        self.assertTrue(result.rollback_proof["candidate_workspace_removed"])
        self.assertEqual(baseline_before, baseline_after)

    def test_two_runs_produce_same_id_and_replay(self) -> None:
        first = self.execute()
        second = self.execute()

        self.assertEqual(first.run_id, second.run_id)
        self.assertEqual(first.replay_before, second.replay_before)
        self.assertEqual(first.replay_after, second.replay_after)
        self.assertEqual(first.trace["evaluation"], second.trace["evaluation"])

    def test_trace_satisfies_runtime_contract(self) -> None:
        result = self.execute()

        self.assertEqual(validate_trace_payload(result.trace), [])
        self.assertEqual(result.trace["external_mutation_count"], 0)
        self.assertFalse(result.trace["isolation"]["running_version_overwritten"])

    def test_trace_tampering_is_detected(self) -> None:
        trace = copy.deepcopy(self.execute().trace)
        trace["external_mutation_count"] = 1

        errors = validate_trace_payload(trace)

        self.assertIn("external_mutation_count must be zero", errors)

    def test_invented_evaluation_check_is_rejected(self) -> None:
        trace = copy.deepcopy(self.execute().trace)
        trace["evaluation"]["checks"] = {"invented_check": True}

        errors = validate_trace_payload(trace)

        self.assertIn(
            "evaluation checks must match the exact first-slice check set", errors
        )

    def test_rejected_governor_requires_a_reason(self) -> None:
        trace = copy.deepcopy(self.execute().trace)
        trace["governor"] = {
            "approved": False,
            "reasons": [],
            "immutable_surface": "baseline_only",
        }
        trace["evaluation"]["decision"] = "reject"
        trace["evaluation"]["reasons"] = ["governor_approved"]
        trace["evaluation"]["checks"]["governor_approved"] = False

        errors = validate_trace_payload(trace)

        self.assertIn("rejected Governor trace must contain rejection reasons", errors)

    def test_candidate_hash_mismatch_fails_before_write(self) -> None:
        source = read_managed_source(REPO_ROOT, TARGET_PATH)
        patch = build_harmless_patch(source.decode("utf-8"), sha256_bytes(source))
        patch = replace(patch, expected_before_sha256="0" * 64)

        with CandidateWorkspace(REPO_ROOT, TARGET_PATH) as workspace:
            before = workspace.path.read_bytes()
            with self.assertRaisesRegex(CandidateBoundaryError, "hash does not match"):
                workspace.apply(patch)
            after = workspace.path.read_bytes()

        self.assertEqual(before, after)

    def test_governor_rejection_happens_before_workspace_creation(self) -> None:
        source = read_managed_source(REPO_ROOT, TARGET_PATH)
        patch = build_harmless_patch(source.decode("utf-8"), sha256_bytes(source))
        patch = replace(
            patch,
            target_path="scripts/oal_001/governor.py",
            changed_paths=("scripts/oal_001/governor.py",),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_parent = Path(temp_dir)
            with mock_patch(
                "scripts.oal_001.runtime.build_harmless_patch", return_value=patch
            ):
                with self.assertRaises(PermissionError):
                    execute_cycle(
                        REPO_ROOT,
                        self.policy,
                        BRANCH,
                        BASE_SHA,
                        git_status_before="## synthetic-test",
                        git_status_after="## synthetic-test",
                        temp_parent=temp_parent,
                    )

            self.assertEqual(list(temp_parent.iterdir()), [])

    def test_candidate_parser_rejects_executable_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "observatory.py"
            path.write_text(
                "import pathlib\nSTRATEGY_WEIGHTS = {'primary': 0.7, 'exploration': 0.3}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "executable or unsupported"):
                parse_strategy_source(path)

    def test_candidate_parser_rejects_invalid_weight_sum(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "observatory.py"
            path.write_text(
                "STRATEGY_WEIGHTS = {'primary': 0.8, 'exploration': 0.3}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "sum to one"):
                parse_strategy_source(path)

    def test_source_symlink_is_rejected_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / TARGET_PATH
            target.parent.mkdir(parents=True)
            real = root / "real.py"
            real.write_text(
                "STRATEGY_WEIGHTS = {'primary': 0.75, 'exploration': 0.25}\n",
                encoding="utf-8",
            )
            try:
                target.symlink_to(real)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            with self.assertRaisesRegex(CandidateBoundaryError, "links or reparse"):
                read_managed_source(root, TARGET_PATH)

    def test_broken_source_symlink_is_rejected_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / TARGET_PATH
            target.parent.mkdir(parents=True)
            try:
                target.symlink_to(root / "missing.py")
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")

            with self.assertRaisesRegex(CandidateBoundaryError, "links or reparse"):
                read_managed_source(root, TARGET_PATH)

    def test_windows_reparse_attribute_is_rejected(self) -> None:
        attributes = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        fake_stat = SimpleNamespace(st_file_attributes=attributes)
        with mock_patch.object(Path, "lstat", return_value=fake_stat):
            self.assertTrue(_is_reparse_point(Path("synthetic-junction")))

    def test_source_hardlink_is_rejected_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / TARGET_PATH
            target.parent.mkdir(parents=True)
            real = root / "real.py"
            real.write_text(
                "STRATEGY_WEIGHTS = {'primary': 0.75, 'exploration': 0.25}\n",
                encoding="utf-8",
            )
            try:
                os.link(real, target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"hardlink creation unavailable: {exc}")

            with self.assertRaisesRegex(CandidateBoundaryError, "hard-linked"):
                read_managed_source(root, TARGET_PATH)

    def test_evaluator_rejects_candidate_below_exploration_floor(self) -> None:
        fixture = load_fixture(REPO_ROOT, self.policy.fixture_path)
        harness = ReplayHarness(fixture)
        baseline = harness.replay(REPO_ROOT / TARGET_PATH)
        below_floor = replace(
            baseline,
            strategy_weights={"primary": 0.8, "exploration": 0.2},
            route_counts={"primary": 16, "exploration": 4},
        )
        decision = PatchEvaluator(self.policy, fixture).evaluate(
            Governor(self.policy).review(
                build_harmless_patch(
                    read_managed_source(REPO_ROOT, TARGET_PATH).decode("utf-8"),
                    sha256_bytes(read_managed_source(REPO_ROOT, TARGET_PATH)),
                ),
                BRANCH,
            ),
            baseline,
            baseline,
            below_floor,
            below_floor,
            True,
        )

        self.assertEqual(decision.decision, "reject")
        self.assertIn("exploration_floor_preserved", decision.reasons)

    def test_boundary_and_risk_reports_mark_deferred_scope(self) -> None:
        result = self.execute()

        self.assertEqual(result.boundary_report["status"], "PASS")
        self.assertEqual(result.risk_report["status"], "PASS_WITH_DEFERRED_SCOPE")
        self.assertIn("ledger_writer", result.risk_report["deferred_scope"])

    def _live_cycle(self):
        status = _git_status(REPO_ROOT)
        return execute_cycle(
            REPO_ROOT,
            self.policy,
            git_branch(),
            git_head(),
            git_status_before=status,
            git_status_after=status,
        )

    def test_cross_artifact_replay_tampering_is_rejected(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            output_root = Path(temp_dir)
            policy = replace(
                self.policy,
                output_root=output_root.relative_to(REPO_ROOT).as_posix(),
            )
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, self._live_cycle())
            self.assertEqual(validate_artifacts(output_dir), [])
            replay_after = json.loads(
                (output_dir / "replay_after.json").read_text(encoding="utf-8")
            )
            replay_after["route_counts"]["exploration"] = 999
            (output_dir / "replay_after.json").write_text(
                json.dumps(replay_after, indent=2) + "\n", encoding="utf-8"
            )

            errors = validate_artifacts(output_dir)

            self.assertIn(
                "candidate replay does not match the reconstructed replay", errors
            )

    def test_rewriting_cycle_resets_stale_completion_state(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            output_root = Path(temp_dir)
            policy = replace(
                self.policy,
                output_root=output_root.relative_to(REPO_ROOT).as_posix(),
            )
            result = self._live_cycle()
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
            (output_dir / "test_result.json").write_text(
                '{"status":"PASS"}\n', encoding="utf-8"
            )
            (output_dir / "validation_complete.json").write_text(
                '{"status":"PASS"}\n', encoding="utf-8"
            )

            write_cycle_artifacts(REPO_ROOT, policy, result)

            test_result = json.loads(
                (output_dir / "test_result.json").read_text(encoding="utf-8")
            )
            completion = json.loads(
                (output_dir / "validation_complete.json").read_text(encoding="utf-8")
            )
            self.assertEqual(test_result["status"], "NOT_RUN")
            self.assertFalse(test_result["evidence_complete"])
            self.assertEqual(completion["status"], "INCOMPLETE")

    def test_completion_marker_detects_post_validation_tampering(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            output_root = Path(temp_dir)
            policy = replace(
                self.policy,
                output_root=output_root.relative_to(REPO_ROOT).as_posix(),
            )
            result = self._live_cycle()
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
            pass_test_result = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": "PASS",
                "evidence_complete": True,
                "static_checks": {"status": "PASS"},
                "unit_tests": {
                    "status": "PASS",
                    "count": 37,
                    "skipped": 0,
                    "outcome_details": {},
                    "return_code": 0,
                },
                "dry_run": {"status": "PASS", "return_code": 0},
                "artifact_validation": {"status": "PASS", "errors": []},
                "external_mutation_count": 0,
            }
            _atomic_write_json(output_dir / "test_result.json", pass_test_result)
            completion = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": "PASS",
                "artifact_sha256": _artifact_digest_map(output_dir),
            }
            _atomic_write_json(output_dir / "validation_complete.json", completion)
            self.assertEqual(validate_completion_marker(output_dir), [])

            fail_test_result = copy.deepcopy(pass_test_result)
            fail_test_result["status"] = "FAIL"
            fail_test_result["evidence_complete"] = False
            fail_test_result["artifact_validation"] = {
                "status": "FAIL",
                "errors": ["synthetic failure"],
            }
            _atomic_write_json(output_dir / "test_result.json", fail_test_result)
            relabelled = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": "PASS",
                "artifact_sha256": _artifact_digest_map(output_dir),
            }
            _atomic_write_json(output_dir / "validation_complete.json", relabelled)
            self.assertIn(
                "completion marker status does not match bound test semantics",
                validate_completion_marker(output_dir),
            )

            _atomic_write_json(output_dir / "test_result.json", pass_test_result)
            completion["artifact_sha256"] = _artifact_digest_map(output_dir)
            _atomic_write_json(output_dir / "validation_complete.json", completion)
            (output_dir / "replay_after.json").write_text("{}\n", encoding="utf-8")

            errors = validate_completion_marker(output_dir)

            self.assertIn(
                "completion marker artifact digests do not match current bytes", errors
            )

    def test_subprocess_alias_bypass_is_rejected(self) -> None:
        tree = ast.parse(
            "import subprocess as sp\nsp.run(['git', 'push', 'origin', 'main'])\n"
        )

        errors = _subprocess_boundary_errors("synthetic.py", tree)

        self.assertIn("subprocess import alias is forbidden in synthetic.py", errors)
        namespace_tree = ast.parse(
            "globals()['subprocess'].run(['git', 'push', 'origin', 'main'])\n"
        )
        namespace_errors = _subprocess_boundary_errors("synthetic.py", namespace_tree)
        self.assertIn(
            "dynamic execution or namespace access is forbidden in synthetic.py",
            namespace_errors,
        )
        process_bypasses = (
            "import sys as s\ns.modules['subprocess'].run(['git', 'push'])\n",
            "from sys import modules as m\nm['subprocess'].run(['git', 'push'])\n",
            "import os\nos.spawnlp(os.P_WAIT, 'git', 'git', 'push')\n",
        )
        for source in process_bypasses:
            with self.subTest(source=source):
                bypass_errors = _subprocess_boundary_errors(
                    "synthetic.py", ast.parse(source)
                )
                self.assertTrue(bypass_errors)

    def test_unit_test_gate_rejects_zero_tests(self) -> None:
        errors = unit_test_gate_errors(return_code=0, count=0, outcome_details={})

        self.assertIn("unit test count must be at least 37, got 0", errors)

    def test_unit_test_parser_uses_anchored_final_skip_summary(self) -> None:
        output = (
            "test_noise ... skipped=0\n"
            "----------------------------------------------------------------------\n"
            "Ran 37 tests in 0.100s\n\n"
            "OK (skipped=1)\n"
        )
        completed = SimpleNamespace(returncode=0, stdout=output)
        with mock_patch(
            "scripts.validate_oal_001.subprocess.run", return_value=completed
        ):
            return_code, _, count, outcomes = run_unit_tests()

        self.assertEqual(return_code, 0)
        self.assertEqual(count, 37)
        self.assertEqual(outcomes, {"skipped": 1})
        self.assertTrue(unit_test_gate_errors(return_code, count, outcomes))

        expected_failure_output = output.replace(
            "OK (skipped=1)", "OK (expected failures=37)"
        )
        completed = SimpleNamespace(returncode=0, stdout=expected_failure_output)
        with mock_patch(
            "scripts.validate_oal_001.subprocess.run", return_value=completed
        ):
            return_code, _, count, outcomes = run_unit_tests()
        self.assertEqual(outcomes, {"expected failures": 37})
        self.assertTrue(unit_test_gate_errors(return_code, count, outcomes))


if __name__ == "__main__":
    unittest.main()
