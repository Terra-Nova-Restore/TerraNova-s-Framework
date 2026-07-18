from __future__ import annotations

import ast
import copy
import json
import os
import stat
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch as mock_patch

from scripts.oal_001 import git_read
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
    git_status_is_clean,
    load_fixture,
    parse_strategy_source,
    read_managed_source,
    sha256_bytes,
    validate_trace_payload,
    write_cycle_artifacts,
)
from scripts.validate_oal_001 import (
    EXIT_NOT_PROMOTION_READY,
    EXIT_RUNTIME_GAP,
    MINIMUM_OAL_TEST_COUNT,
    PROTECTED_IMPORT_FILES,
    STATUS_PASS,
    STATUS_RUNTIME_GAP,
    VALIDATOR_PATH,
    _artifact_digest_map,
    _atomic_write_bytes,
    _atomic_write_json,
    _build_test_result,
    _capture_artifact_snapshot,
    _dispatch as validator_dispatch,
    _finalize_evidence,
    _finalized_snapshot,
    _import_path_boundary_errors,
    _pull_request_trigger_errors,
    _runtime_isolation_errors,
    _replace_snapshot_bytes,
    _snapshot_promotion_eligible,
    _subprocess_boundary_errors,
    main as validator_main,
    python_shadowing_errors,
    run_dry_run,
    run_unit_tests,
    unit_test_gate_errors,
    validate_artifact_snapshot,
    validate_artifacts,
    validate_completion_marker,
    verify_existing_evidence,
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
            git_status_before="",
            git_status_after="",
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

    def test_legacy_branch_header_evidence_returns_controlled_errors(self) -> None:
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
            result = self.execute()
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
            snapshot = _capture_artifact_snapshot(output_dir)
            legacy_trace = copy.deepcopy(result.trace)
            legacy_trace["git_status"]["before"] = "## synthetic-test"
            legacy_trace["git_status"]["after"] = "## synthetic-test"
            legacy_snapshot = _replace_snapshot_bytes(
                snapshot,
                "mutation_trace.json",
                (json.dumps(legacy_trace, sort_keys=True) + "\n").encode("utf-8"),
            )

            errors = validate_artifact_snapshot(
                legacy_snapshot, output_dir, lifecycle="prepared"
            )

        self.assertTrue(
            any("trace Git status cannot derive a run ID" in item for item in errors)
        )

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
                        git_status_before="",
                        git_status_after="",
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

    def _prepared_evidence(self, temp_dir: str):
        output_root = Path(temp_dir)
        policy = replace(
            self.policy,
            output_root=output_root.relative_to(REPO_ROOT).as_posix(),
        )
        result = self._live_cycle()
        output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
        snapshot = _capture_artifact_snapshot(output_dir)
        self.assertEqual(
            validate_artifact_snapshot(snapshot, output_dir, lifecycle="prepared"),
            [],
        )
        return result, output_dir, snapshot

    def _test_result(
        self,
        run_id: str,
        python_version: str = "3.11.9",
        python_version_info: tuple[int, int] = (3, 11),
        promotion_eligible: bool = True,
    ) -> dict[str, object]:
        return _build_test_result(
            run_id=run_id,
            test_count=MINIMUM_OAL_TEST_COUNT,
            test_outcomes={},
            test_returncode=0,
            dry_run_returncode=0,
            artifact_errors=[],
            python_version=python_version,
            python_version_info=python_version_info,
            promotion_eligible=promotion_eligible,
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

    def test_validation_status_requires_python_3_11_for_pass(self) -> None:
        passing = self._test_result("OAL-001-" + "A" * 16)
        prepared = self._test_result("OAL-001-" + "A" * 16, promotion_eligible=False)
        runtime_gap = self._test_result(
            "OAL-001-" + "A" * 16,
            python_version="3.12.10",
            python_version_info=(3, 12),
        )
        failing = _build_test_result(
            run_id="OAL-001-" + "A" * 16,
            test_count=MINIMUM_OAL_TEST_COUNT,
            test_outcomes={},
            test_returncode=0,
            dry_run_returncode=0,
            artifact_errors=["synthetic failure"],
            python_version="3.11.9",
            python_version_info=(3, 11),
            promotion_eligible=True,
        )

        self.assertEqual(passing["status"], STATUS_PASS)
        self.assertTrue(passing["promotion_ready"])
        self.assertEqual(prepared["status"], STATUS_PASS)
        self.assertFalse(prepared["evidence_complete"])
        self.assertFalse(prepared["promotion_ready"])
        self.assertEqual(runtime_gap["status"], STATUS_RUNTIME_GAP)
        self.assertFalse(runtime_gap["evidence_complete"])
        self.assertFalse(runtime_gap["promotion_ready"])
        self.assertEqual(failing["status"], "FAIL")

    def test_dirty_final_bundle_is_not_promotion_ready_and_rejects_forgery(
        self,
    ) -> None:
        dirty_status = " M scripts/oal_001/runtime.py"
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)

        def synthetic_git_read(command: list[str]) -> str:
            mapping = {
                ("git", "branch", "--show-current"): BRANCH,
                ("git", "rev-parse", "HEAD"): BASE_SHA,
                (
                    "git",
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                    "--ignore-submodules=none",
                    "--no-renames",
                ): dirty_status,
            }
            return mapping[tuple(command)]

        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            output_root = Path(temp_dir)
            policy = replace(
                self.policy,
                output_root=output_root.relative_to(REPO_ROOT).as_posix(),
            )
            result = execute_cycle(
                REPO_ROOT,
                policy,
                BRANCH,
                BASE_SHA,
                git_status_before=dirty_status,
                git_status_after=dirty_status,
            )
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
            prepared_snapshot = _capture_artifact_snapshot(output_dir)
            with mock_patch(
                "scripts.validate_oal_001._git_read",
                side_effect=synthetic_git_read,
            ):
                self.assertEqual(
                    validate_artifact_snapshot(
                        prepared_snapshot, output_dir, lifecycle="prepared"
                    ),
                    [],
                )

                promotion_eligible = _snapshot_promotion_eligible(prepared_snapshot)
                self.assertFalse(promotion_eligible)
                test_result = self._test_result(
                    result.run_id, promotion_eligible=promotion_eligible
                )
                finalized = _finalized_snapshot(prepared_snapshot, test_result)
                self.assertEqual(
                    validate_artifact_snapshot(
                        finalized, output_dir, lifecycle="complete"
                    ),
                    [],
                )
                self.assertEqual(
                    _finalize_evidence(output_dir, prepared_snapshot, test_result),
                    [],
                )
                with (
                    mock_patch(
                        "scripts.validate_oal_001.static_errors", return_value=[]
                    ),
                    mock_patch(
                        "scripts.validate_oal_001._existing_output_dir",
                        return_value=output_dir,
                    ),
                ):
                    return_code = validator_dispatch(
                        ["--verify-existing", result.run_id]
                    )
                self.assertEqual(return_code, EXIT_NOT_PROMOTION_READY)

                forged = copy.deepcopy(test_result)
                forged["evidence_complete"] = True
                forged["promotion_ready"] = True
                forged_snapshot = _finalized_snapshot(prepared_snapshot, forged)
                errors = validate_artifact_snapshot(
                    forged_snapshot, output_dir, lifecycle="complete"
                )

            self.assertIn(
                "final promotion readiness does not match validation status", errors
            )
            self.assertIn(
                "final evidence completeness does not match validation status", errors
            )

    def test_clean_bundle_verifies_without_upstream_tracking_metadata(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)

        def canonical_git_read(command: list[str]) -> str:
            mapping = {
                ("git", "branch", "--show-current"): BRANCH,
                ("git", "rev-parse", "HEAD"): BASE_SHA,
                (
                    "git",
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                    "--ignore-submodules=none",
                    "--no-renames",
                ): "",
            }
            return mapping[tuple(command)]

        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            output_root = Path(temp_dir)
            policy = replace(
                self.policy,
                output_root=output_root.relative_to(REPO_ROOT).as_posix(),
            )
            result = self.execute()
            output_dir = write_cycle_artifacts(REPO_ROOT, policy, result)
            prepared_snapshot = _capture_artifact_snapshot(output_dir)
            test_result = self._test_result(
                result.run_id,
                promotion_eligible=_snapshot_promotion_eligible(prepared_snapshot),
            )
            with mock_patch(
                "scripts.validate_oal_001._git_read",
                side_effect=canonical_git_read,
            ):
                self.assertEqual(
                    validate_artifact_snapshot(
                        prepared_snapshot, output_dir, lifecycle="prepared"
                    ),
                    [],
                )
                self.assertEqual(
                    _finalize_evidence(output_dir, prepared_snapshot, test_result),
                    [],
                )
                self.assertEqual(verify_existing_evidence(output_dir), [])

    def test_finalized_snapshot_records_runtime_gap_without_pass(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            runtime_gap = self._test_result(
                result.run_id,
                python_version="3.12.10",
                python_version_info=(3, 12),
            )
            finalized = _finalized_snapshot(prepared, runtime_gap)

            self.assertEqual(
                validate_artifact_snapshot(finalized, output_dir, lifecycle="complete"),
                [],
            )
            completion = json.loads(
                dict(finalized)["validation_complete.json"].decode("utf-8")
            )
            self.assertEqual(completion["status"], STATUS_RUNTIME_GAP)
            self.assertNotEqual(completion["status"], STATUS_PASS)

    def test_finalization_rejects_tamper_between_validation_and_binding(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            original_writer = _atomic_write_bytes

            def racing_writer(path: Path, data: bytes) -> None:
                original_writer(path, data)
                if path.name == "test_result.json":
                    replay = json.loads(
                        (output_dir / "replay_after.json").read_text(encoding="utf-8")
                    )
                    replay["route_counts"]["exploration"] = 999
                    (output_dir / "replay_after.json").write_text(
                        json.dumps(replay, indent=2) + "\n", encoding="utf-8"
                    )

            with mock_patch(
                "scripts.validate_oal_001._atomic_write_bytes",
                side_effect=racing_writer,
            ):
                errors = _finalize_evidence(
                    output_dir,
                    prepared,
                    self._test_result(
                        result.run_id,
                        promotion_eligible=_snapshot_promotion_eligible(prepared),
                    ),
                )

            self.assertTrue(any("candidate replay" in item for item in errors))
            self.assertNotEqual(verify_existing_evidence(output_dir), [])

    def test_verify_existing_rejects_semantic_tamper_with_matching_digests(
        self,
    ) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            self.assertEqual(
                _finalize_evidence(
                    output_dir,
                    prepared,
                    self._test_result(
                        result.run_id,
                        promotion_eligible=_snapshot_promotion_eligible(prepared),
                    ),
                ),
                [],
            )
            replay = json.loads(
                (output_dir / "replay_after.json").read_text(encoding="utf-8")
            )
            replay["route_counts"]["exploration"] = 999
            (output_dir / "replay_after.json").write_text(
                json.dumps(replay, indent=2) + "\n", encoding="utf-8"
            )
            changed = _capture_artifact_snapshot(output_dir)
            marker = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": STATUS_PASS,
                "artifact_sha256": _artifact_digest_map(changed),
            }
            _atomic_write_json(output_dir / "validation_complete.json", marker)

            errors = verify_existing_evidence(output_dir)

            self.assertTrue(any("candidate replay" in item for item in errors))
            self.assertFalse(any("does not bind" in item for item in errors))

    def test_verify_existing_rejects_pass_when_python_3_11_was_not_run(
        self,
    ) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            runtime_gap = self._test_result(
                result.run_id,
                python_version="3.12.10",
                python_version_info=(3, 12),
            )
            self.assertEqual(_finalize_evidence(output_dir, prepared, runtime_gap), [])
            forged = copy.deepcopy(runtime_gap)
            forged["status"] = STATUS_PASS
            forged["evidence_complete"] = True
            forged["promotion_ready"] = True
            _atomic_write_json(output_dir / "test_result.json", forged)
            changed = _capture_artifact_snapshot(output_dir)
            marker = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": STATUS_PASS,
                "artifact_sha256": _artifact_digest_map(changed),
            }
            _atomic_write_json(output_dir / "validation_complete.json", marker)

            errors = verify_existing_evidence(output_dir)

            self.assertIn(
                "final validation status does not match Python 3.11 execution",
                errors,
            )

    def test_verify_existing_mode_is_read_only_and_reports_runtime_gap(self) -> None:
        self.assertTrue(sys.dont_write_bytecode)
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            runtime_gap = self._test_result(
                result.run_id,
                python_version="3.12.10",
                python_version_info=(3, 12),
            )
            self.assertEqual(_finalize_evidence(output_dir, prepared, runtime_gap), [])
            before = {
                path.name: sha256_bytes(path.read_bytes())
                for path in output_dir.iterdir()
            }
            with (
                mock_patch("scripts.validate_oal_001.static_errors", return_value=[]),
                mock_patch(
                    "scripts.validate_oal_001._existing_output_dir",
                    return_value=output_dir,
                ),
                mock_patch(
                    "scripts.validate_oal_001.run_unit_tests",
                    side_effect=AssertionError("unit tests must not run"),
                ),
                mock_patch(
                    "scripts.validate_oal_001.run_dry_run",
                    side_effect=AssertionError("dry-run must not run"),
                ),
                mock_patch(
                    "scripts.validate_oal_001._atomic_write_bytes",
                    side_effect=AssertionError("verifier must not write"),
                ),
            ):
                return_code = validator_dispatch(["--verify-existing", result.run_id])
            after = {
                path.name: sha256_bytes(path.read_bytes())
                for path in output_dir.iterdir()
            }

            self.assertEqual(return_code, EXIT_RUNTIME_GAP)
            self.assertEqual(before, after)
            self.assertEqual(
                validator_dispatch(["--verify-existing", "not-a-run-id"]), 2
            )

    def test_completion_marker_detects_post_validation_tampering(self) -> None:
        local_private = REPO_ROOT / "raw" / "exports" / "local-private"
        local_private.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="oal-001-test-", dir=local_private
        ) as temp_dir:
            result, output_dir, prepared = self._prepared_evidence(temp_dir)
            pass_test_result = self._test_result(
                result.run_id,
                promotion_eligible=_snapshot_promotion_eligible(prepared),
            )
            self.assertEqual(
                _finalize_evidence(output_dir, prepared, pass_test_result), []
            )
            self.assertEqual(validate_completion_marker(output_dir), [])

            fail_test_result = copy.deepcopy(pass_test_result)
            fail_test_result["status"] = "FAIL"
            fail_test_result["evidence_complete"] = False
            fail_test_result["artifact_validation"] = {
                "status": "FAIL",
                "errors": ["synthetic failure"],
            }
            _atomic_write_json(output_dir / "test_result.json", fail_test_result)
            changed_snapshot = _capture_artifact_snapshot(output_dir)
            relabelled = {
                "schema_version": "OAL-1.0",
                "run_id": result.run_id,
                "status": "PASS",
                "artifact_sha256": _artifact_digest_map(changed_snapshot),
            }
            _atomic_write_json(output_dir / "validation_complete.json", relabelled)
            self.assertTrue(
                any(
                    "final validation status" in item or "completion marker" in item
                    for item in validate_completion_marker(output_dir)
                )
            )

            finalized = _finalized_snapshot(prepared, pass_test_result)
            _atomic_write_bytes(
                output_dir / "test_result.json",
                dict(finalized)["test_result.json"],
            )
            _atomic_write_bytes(
                output_dir / "validation_complete.json",
                dict(finalized)["validation_complete.json"],
            )
            (output_dir / "replay_after.json").write_text("{}\n", encoding="utf-8")

            errors = validate_completion_marker(output_dir)

            self.assertTrue(any("candidate replay" in item for item in errors))
            self.assertTrue(any("completion marker" in item for item in errors))

    def test_git_read_uses_hardened_absolute_process_context(self) -> None:
        executable = Path(r"C:\Program Files\Git\cmd\git.exe")
        completed = SimpleNamespace(
            returncode=0,
            stdout=BRANCH + "\n",
            stderr="",
        )
        with (
            mock_patch.object(
                git_read, "_resolve_git_executable", return_value=executable
            ),
            mock_patch.object(
                git_read.subprocess, "run", return_value=completed
            ) as mocked_run,
            mock_patch.dict(os.environ, {"OAL_TEST_SECRET": "do-not-forward"}),
        ):
            self.assertEqual(git_read.current_branch(REPO_ROOT), BRANCH)

        command = mocked_run.call_args.args[0]
        options = mocked_run.call_args.kwargs
        self.assertEqual(command[0], str(executable))
        self.assertTrue(executable.is_absolute())
        self.assertIn("--no-optional-locks", command)
        self.assertIn("core.fsmonitor=false", command)
        self.assertEqual(options["env"]["GIT_OPTIONAL_LOCKS"], "0")
        self.assertNotIn("OAL_TEST_SECRET", options["env"])
        self.assertNotIn("shell", options)

    def test_worktree_status_preserves_porcelain_columns_without_tracking_data(
        self,
    ) -> None:
        executable = Path(r"C:\Program Files\Git\cmd\git.exe")
        completed = SimpleNamespace(
            returncode=0,
            stdout=" M scripts/oal_001/runtime.py\n?? untracked.txt\n",
            stderr="",
        )
        with (
            mock_patch.object(
                git_read, "_resolve_git_executable", return_value=executable
            ),
            mock_patch.object(
                git_read.subprocess, "run", return_value=completed
            ) as mocked_run,
        ):
            status = git_read.worktree_status(REPO_ROOT)

        self.assertEqual(status, " M scripts/oal_001/runtime.py\n?? untracked.txt")
        self.assertFalse(git_status_is_clean(status))
        command = mocked_run.call_args.args[0]
        self.assertIn("--porcelain=v1", command)
        self.assertIn("--untracked-files=all", command)
        self.assertIn("--ignore-submodules=none", command)
        self.assertIn("--no-renames", command)
        self.assertIn("status.branch=false", command)
        self.assertNotIn("--branch", command)

    def test_clean_status_is_empty_and_legacy_branch_header_is_rejected(self) -> None:
        self.assertTrue(git_status_is_clean(""))
        with self.assertRaisesRegex(RuntimeError, "invalid payload"):
            git_read.validate_worktree_status(
                "## codex/observatory-selfmod-001...origin/branch"
            )
        with self.assertRaisesRegex(RuntimeError, "invalid payload"):
            git_read.validate_worktree_status(" M tracked.py\n")
        with self.assertRaisesRegex(RuntimeError, "invalid payload"):
            execute_cycle(
                REPO_ROOT,
                self.policy,
                BRANCH,
                BASE_SHA,
                git_status_before="## synthetic-test",
                git_status_after="## synthetic-test",
            )

    def test_dirty_porcelain_entries_are_prepared_not_clean(self) -> None:
        for status in ("M  tracked.py", " M tracked.py", "?? untracked.py"):
            with self.subTest(status=status):
                result = execute_cycle(
                    REPO_ROOT,
                    self.policy,
                    BRANCH,
                    BASE_SHA,
                    git_status_before=status,
                    git_status_after=status,
                )

                self.assertFalse(result.trace["git_status"]["clean_worktree"])
                self.assertEqual(result.trace["source_state"], "working_tree_manifest")
                self.assertEqual(result.boundary_report["status"], "PASS_PREPARED")

    def test_porcelain_submodule_worktree_states_are_canonical(self) -> None:
        for status in (
            " m submodule",
            " ? submodule",
            "Mm submodule",
            "M? submodule",
        ):
            with self.subTest(status=status):
                self.assertEqual(git_read.validate_worktree_status(status), status)
                self.assertFalse(git_status_is_clean(status))

    def test_git_read_api_rejects_mutation_and_path_traversal(self) -> None:
        with self.assertRaisesRegex(ValueError, "typed read-only API"):
            git_read._run_git(REPO_ROOT, ("push", "origin", "main"))
        for unsafe_path in (
            "../escape",
            "/absolute",
            r"..\escape",
            "C:/outside",
            "C:outside",
            "raw/*",
            ":(top)raw/exports",
        ):
            with self.subTest(path=unsafe_path):
                with self.assertRaises(ValueError):
                    git_read.is_ignored(REPO_ROOT, unsafe_path)

    def test_git_check_ignore_distinguishes_results_and_errors(self) -> None:
        self.assertTrue(
            git_read.is_ignored(REPO_ROOT, "raw/exports/local-private/oal-001")
        )
        executable = Path(r"C:\Program Files\Git\cmd\git.exe")
        with mock_patch.object(
            git_read, "_resolve_git_executable", return_value=executable
        ):
            with mock_patch.object(
                git_read.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=0, stdout="", stderr=""),
            ) as mocked_run:
                self.assertTrue(git_read.is_ignored(REPO_ROOT, "raw/exports"))
                self.assertIn("--", mocked_run.call_args.args[0])
            with mock_patch.object(
                git_read.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=1, stdout="", stderr=""),
            ):
                self.assertFalse(git_read.is_ignored(REPO_ROOT, "README.md"))
            with mock_patch.object(
                git_read.subprocess,
                "run",
                return_value=SimpleNamespace(
                    returncode=2, stdout="", stderr="synthetic Git failure"
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "synthetic Git failure"):
                    git_read.is_ignored(REPO_ROOT, "README.md")

    def test_git_executable_inside_repository_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            synthetic_repo = Path(temp_dir)
            local_git = synthetic_repo / "git.exe"
            local_git.write_bytes(b"not an executable")
            with mock_patch.object(
                git_read, "TRUSTED_GIT_CANDIDATES", (str(local_git),)
            ):
                with self.assertRaisesRegex(
                    RuntimeError, "no fixed trusted Git executable"
                ):
                    git_read._resolve_git_executable(synthetic_repo)

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

    def test_workflow_and_validator_use_isolated_import_bootstrap(self) -> None:
        workflow = (REPO_ROOT / ".github/workflows/oal-001-validate.yml").read_text(
            encoding="utf-8"
        )
        validator_source = (REPO_ROOT / "scripts/validate_oal_001.py").read_text(
            encoding="utf-8"
        )
        validator_tree = ast.parse(validator_source)

        self.assertIn("python -I -S -B - <<'PY'", workflow)
        self.assertIn("run: python -I -S -B scripts/validate_oal_001.py", workflow)
        preflight_index = workflow.index("Confirm isolated runtime and import topology")
        classification_index = workflow.index("Classify governed OAL changes")
        branch_gate_index = workflow.index("Bind governed changes to an OAL branch")
        validator_index = workflow.index("Run complete OAL validator")
        self.assertLess(
            preflight_index,
            classification_index,
        )
        self.assertLess(classification_index, branch_gate_index)
        self.assertLess(branch_gate_index, validator_index)
        self.assertEqual(
            workflow.count("if: steps.oal_scope.outputs.oal_changed == 'true'"),
            2,
        )
        self.assertIn("scripts/oal_001/*", workflow)
        self.assertIn("scripts/validate_oal_001.py", workflow)
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn('merge_base="$(git merge-base ', workflow)
        self.assertIn('"$merge_base" "$OAL_SOURCE_SHA" --', workflow)
        self.assertNotIn('"$OAL_BASE_SHA" "$OAL_SOURCE_SHA" -- >', workflow)
        direct_imports = [
            node for node in validator_tree.body if isinstance(node, ast.Import)
        ]
        self.assertEqual(direct_imports[0].names[0].name, "sys")
        self.assertEqual(
            _import_path_boundary_errors("scripts/validate_oal_001.py", validator_tree),
            [],
        )
        unsafe_tree = ast.parse(
            "import sys\n"
            "REPO_ROOT = 'synthetic'\n"
            "if str(REPO_ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(REPO_ROOT))\n"
        )
        self.assertTrue(
            _import_path_boundary_errors("scripts/validate_oal_001.py", unsafe_tree)
        )

    def test_workflow_trigger_is_unfiltered_and_fail_closed(self) -> None:
        workflow_source = (
            REPO_ROOT / ".github/workflows/oal-001-validate.yml"
        ).read_bytes()

        self.assertEqual(_pull_request_trigger_errors(workflow_source), [])
        workflow = workflow_source.decode("utf-8")
        canonical_trigger = "on:\n  pull_request: {}"
        filtered_or_indirect_triggers = (
            "on:\n  pull_request:\n    paths:\n      - 'scripts/**'",
            "on:\n  pull_request:\n    paths-ignore:\n      - 'docs/**'",
            "on:\n  pull_request:\n    branches:\n      - main",
            "on:\n  pull_request:\n    branches-ignore:\n      - legacy",
            "on:\n  pull_request:\n    types: [opened]",
            "on:\n  pull_request_target: {}",
            "on:\n  push: {}\n  # pull_request: {}",
            "on:\n  pull_request:",
        )
        trigger_error = [
            "OAL workflow trigger must be exactly one unfiltered pull_request event"
        ]
        for replacement in filtered_or_indirect_triggers:
            source = workflow.replace(canonical_trigger, replacement, 1).encode()
            with self.subTest(replacement=replacement):
                self.assertEqual(_pull_request_trigger_errors(source), trigger_error)

        duplicate_or_alternative_keys = (
            "on:\n  push: {}",
            "on: {push: {}}",
            '"on": {push: {}}',
            "'on': {push: {}}",
            "on : {push: {}}",
            "!!str on: {push: {}}",
            "? on\n: {push: {}}",
            "{on: {push: {}}}",
        )
        top_level_error = [
            "OAL workflow top-level mapping does not match the exact contract"
        ]
        for extra_key in duplicate_or_alternative_keys:
            source = workflow.replace(
                canonical_trigger,
                f"{canonical_trigger}\n{extra_key}",
                1,
            ).encode()
            with self.subTest(extra_key=extra_key):
                self.assertEqual(_pull_request_trigger_errors(source), top_level_error)
        aliased_source = workflow.replace(
            canonical_trigger,
            "on: &events\n  pull_request: {}",
            1,
        ).encode()
        self.assertEqual(_pull_request_trigger_errors(aliased_source), top_level_error)

    def test_imported_main_refuses_untrusted_import_state(self) -> None:
        self.assertTrue(_runtime_isolation_errors())
        with (
            mock_patch("scripts.validate_oal_001._dispatch") as dispatch,
            mock_patch("scripts.validate_oal_001.error") as emit_error,
        ):
            return_code = validator_main(
                ["--verify-existing", "OAL-001-DECOY00000000000"]
            )

        self.assertEqual(return_code, 1)
        dispatch.assert_not_called()
        emit_error.assert_called()

    def test_import_state_aliases_and_mutations_are_rejected(self) -> None:
        validator_source = (REPO_ROOT / "scripts/validate_oal_001.py").read_text(
            encoding="utf-8"
        )
        bypasses = (
            "from sys import path\npath.insert(0, 'scripts/oal_001')\n",
            "import sys\np = sys.path\np.insert(0, 'scripts/oal_001')\n",
            "import sys\nsys.path_hooks.append(lambda value: None)\n",
            "import sys\nsys.meta_path.clear()\n",
            "import sys\nsys.path_importer_cache.clear()\n",
            "import sys\nsys.modules.clear()\n",
            "import sys\nforwarded = sys\nforwarded.path.insert(0, '.')\n",
            "import sys as system\nsystem.path.insert(0, '.')\n",
            "import sys\nsys.__getattribute__('path').insert(0, '.')\n",
            "import os\nos.sys.path.insert(0, '.')\n",
            "from os import sys as system\nsystem.path.insert(0, '.')\n",
            "from os import *\nsys.path.insert(0, '.')\n",
            "import pathlib\nsystem = pathlib.__dict__['sys']\n"
            "system.path.insert(0, '.')\n",
            "import pathlib\nsystem = pathlib.__getattribute__('sys')\n"
            "system.path.insert(0, '.')\n",
            "import pathlib\nsystem = getattr(pathlib, 'sys')\n"
            "system.path.insert(0, '.')\n",
        )
        for bypass in bypasses:
            with self.subTest(bypass=bypass):
                modified_tree = ast.parse(f"{validator_source}\n{bypass}")
                self.assertTrue(
                    _import_path_boundary_errors(
                        "scripts/validate_oal_001.py", modified_tree
                    )
                )
        decoy_body = (
            "for raw_path in sys.path:\n"
            "    pass\n"
            "if str(REPO_ROOT) not in sys.path:\n"
            "    sys.path.append(str(REPO_ROOT))\n"
            "if sys.path.count(str(REPO_ROOT)) != 1 or "
            "sys.path[-1] != str(REPO_ROOT):\n"
            "    pass\n"
        )
        decoy_sources = (
            "import sys\nREPO_ROOT = 'synthetic'\ndef decoy():\n"
            + "".join(f"    {line}\n" for line in decoy_body.splitlines()),
            "import sys\nREPO_ROOT = 'synthetic'\nif False:\n"
            + "".join(f"    {line}\n" for line in decoy_body.splitlines()),
        )
        for decoy_source in decoy_sources:
            with self.subTest(decoy_source=decoy_source):
                self.assertTrue(
                    _import_path_boundary_errors(
                        "scripts/validate_oal_001.py", ast.parse(decoy_source)
                    )
                )
        disabled_bootstraps = (
            validator_source.replace(
                "if str(REPO_ROOT) not in sys.path:\n",
                "if False and str(REPO_ROOT) not in sys.path:\n",
                1,
            ),
            validator_source.replace(
                "if sys.path.count(str(REPO_ROOT)) != 1 or "
                "sys.path[-1] != str(REPO_ROOT):\n",
                "if False and (sys.path.count(str(REPO_ROOT)) != 1 or "
                "sys.path[-1] != str(REPO_ROOT)):\n",
                1,
            ),
        )
        for disabled_source in disabled_bootstraps:
            with self.subTest(disabled_source=disabled_source):
                self.assertTrue(
                    _import_path_boundary_errors(
                        "scripts/validate_oal_001.py", ast.parse(disabled_source)
                    )
                )

    def test_python_shadowing_paths_are_rejected_before_repo_imports(self) -> None:
        cases = (
            "scripts/ArgParse.py",
            "hashlib.py",
            "json.pyc",
            "fractions/__init__.py",
            "scripts.py",
            "tests.py",
            "scripts/oal_001.py",
            "scripts/oal_001/git_read/__init__.py",
            "scripts/oal_001/runtime.pyc",
            "scripts/oal_001/__pycache__/git_read.cpython-311.pyc",
            "tests/test_oal_001_runtime/__init__.py",
            "tests/__pycache__/test_oal_001_runtime.cpython-311.pyc",
            "scripts/__init__.py",
            "tests/__init__.py",
        )
        for relative_path in cases:
            with self.subTest(relative_path=relative_path):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    for protected_file in PROTECTED_IMPORT_FILES:
                        path = root / protected_file
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text("", encoding="utf-8")
                    self.assertEqual(python_shadowing_errors(root), [])
                    target = root / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.suffix == ".pyc":
                        target.write_bytes(b"synthetic")
                    else:
                        target.write_text("raise SystemExit(0)\n", encoding="utf-8")

                    errors = python_shadowing_errors(root)

                expected = relative_path.replace("\\", "/").removesuffix("/__init__.py")
                self.assertTrue(any(expected in item for item in errors), errors)

    def test_internal_modes_recheck_shadowing_before_repo_imports(self) -> None:
        for option, internal_target in (
            ("--_internal-unit-tests", "_internal_unit_tests"),
            ("--_internal-dry-run", "_internal_dry_run"),
        ):
            with self.subTest(option=option):
                with (
                    mock_patch(
                        "scripts.validate_oal_001.python_shadowing_errors",
                        return_value=["synthetic import shadow"],
                    ),
                    mock_patch(
                        f"scripts.validate_oal_001.{internal_target}"
                    ) as internal,
                ):
                    return_code = validator_dispatch([option])

                self.assertEqual(return_code, 1)
                internal.assert_not_called()

    def test_dry_run_uses_isolated_validator_child(self) -> None:
        completed = SimpleNamespace(
            returncode=0,
            stdout='{"synthetic": true}\n',
            stderr="",
        )
        with mock_patch(
            "scripts.validate_oal_001.subprocess.run", return_value=completed
        ) as mocked_run:
            return_code, output = run_dry_run()

        self.assertEqual(return_code, 0)
        self.assertEqual(output, '{"synthetic": true}')
        self.assertEqual(
            mocked_run.call_args.args[0],
            [
                sys.executable,
                "-I",
                "-S",
                "-B",
                VALIDATOR_PATH,
                "--_internal-dry-run",
            ],
        )

    def test_unit_test_gate_rejects_zero_tests(self) -> None:
        errors = unit_test_gate_errors(return_code=0, count=0, outcome_details={})

        self.assertIn(
            f"unit test count must be at least {MINIMUM_OAL_TEST_COUNT}, got 0",
            errors,
        )

    def test_unit_test_parser_uses_anchored_final_skip_summary(self) -> None:
        output = (
            "test_noise ... skipped=0\n"
            "----------------------------------------------------------------------\n"
            f"Ran {MINIMUM_OAL_TEST_COUNT} tests in 0.100s\n\n"
            "OK (skipped=1)\n"
        )
        completed = SimpleNamespace(returncode=0, stdout=output)
        with mock_patch(
            "scripts.validate_oal_001.subprocess.run", return_value=completed
        ) as mocked_run:
            return_code, _, count, outcomes = run_unit_tests()

        self.assertEqual(return_code, 0)
        self.assertEqual(count, MINIMUM_OAL_TEST_COUNT)
        self.assertEqual(outcomes, {"skipped": 1})
        self.assertTrue(unit_test_gate_errors(return_code, count, outcomes))
        self.assertEqual(
            mocked_run.call_args.args[0],
            [
                sys.executable,
                "-I",
                "-S",
                "-B",
                VALIDATOR_PATH,
                "--_internal-unit-tests",
            ],
        )

        expected_failure_output = output.replace(
            "OK (skipped=1)",
            f"OK (expected failures={MINIMUM_OAL_TEST_COUNT})",
        )
        completed = SimpleNamespace(returncode=0, stdout=expected_failure_output)
        with mock_patch(
            "scripts.validate_oal_001.subprocess.run", return_value=completed
        ):
            return_code, _, count, outcomes = run_unit_tests()
        self.assertEqual(outcomes, {"expected failures": MINIMUM_OAL_TEST_COUNT})
        self.assertTrue(unit_test_gate_errors(return_code, count, outcomes))


if __name__ == "__main__":
    unittest.main()
