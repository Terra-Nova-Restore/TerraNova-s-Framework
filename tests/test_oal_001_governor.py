from __future__ import annotations

import unittest
from dataclasses import replace
from pathlib import Path

from scripts.oal_001.governor import Governor, PatchSpec, load_policy
from scripts.oal_001.runtime import (
    CYCLE_ID,
    EXPECTED_EFFECT,
    FALLBACK_CRITERION,
    TARGET_PATH,
    TRIGGER,
    build_harmless_patch,
    read_managed_source,
    sha256_bytes,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class Oal001GovernorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_policy(REPO_ROOT)
        source = read_managed_source(REPO_ROOT, TARGET_PATH)
        self.patch = build_harmless_patch(source.decode("utf-8"), sha256_bytes(source))
        self.governor = Governor(self.policy)

    def test_policy_has_one_exact_mutable_path(self) -> None:
        self.assertEqual(self.policy.mutable_paths, (TARGET_PATH,))
        self.assertEqual(self.policy.external_mutation_count, 0)
        self.assertEqual(self.policy.historical_fixture_status, "unavailable")

    def test_harmless_patch_is_approved_on_allowed_branch(self) -> None:
        decision = self.governor.review(self.patch, "codex/observatory-selfmod-001")

        self.assertTrue(decision.approved)
        self.assertEqual(decision.reasons, ())

    def test_governor_change_is_automatically_rejected(self) -> None:
        patch = replace(
            self.patch,
            target_path="scripts/oal_001/governor.py",
            changed_paths=("scripts/oal_001/governor.py",),
        )

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn("protected_path:scripts/oal_001/governor.py", decision.reasons)
        self.assertIn("path_not_mutable:scripts/oal_001/governor.py", decision.reasons)

    def test_every_protected_surface_is_rejected(self) -> None:
        concrete_paths = {
            ".codex": ".codex/safety_policy.yaml",
            ".git": ".git/config",
            "docs/governance": "docs/governance/proposed.md",
            "raw/exports": "raw/exports/proposed.json",
        }
        for protected in self.policy.protected_paths:
            path = concrete_paths.get(protected, protected)
            with self.subTest(path=path):
                patch = replace(
                    self.patch,
                    target_path=path,
                    changed_paths=(path,),
                )

                decision = self.governor.review(patch, "codex/observatory-selfmod-001")

                self.assertFalse(decision.approved)
                self.assertIn(f"protected_path:{path}", decision.reasons)
                self.assertIn(f"path_not_mutable:{path}", decision.reasons)

    def test_same_cycle_control_and_authorizing_test_is_rejected(self) -> None:
        paths = ("scripts/oal_001/governor.py", "tests/test_oal_001_governor.py")
        patch = replace(self.patch, target_path=paths[0], changed_paths=paths)

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn(
            "same_cycle_control_and_authorizing_test_change", decision.reasons
        )

    def test_wrong_branch_is_rejected(self) -> None:
        decision = self.governor.review(self.patch, "main")

        self.assertFalse(decision.approved)
        self.assertIn("branch_outside_allowed_lane", decision.reasons)

    def test_traversal_path_is_rejected(self) -> None:
        patch = replace(
            self.patch,
            target_path="../scripts/oal_001/observatory.py",
            changed_paths=("../scripts/oal_001/observatory.py",),
        )

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertTrue(
            any(reason.startswith("invalid_path:") for reason in decision.reasons)
        )

    def test_absolute_path_is_rejected(self) -> None:
        path = "C:/candidate/observatory.py"
        patch = replace(self.patch, target_path=path, changed_paths=(path,))

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn(f"invalid_path:{path}", decision.reasons)

    def test_authorizing_test_alone_is_protected_but_not_same_cycle(self) -> None:
        path = "tests/test_oal_001_governor.py"
        patch = replace(self.patch, target_path=path, changed_paths=(path,))

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn(f"protected_path:{path}", decision.reasons)
        self.assertNotIn(
            "same_cycle_control_and_authorizing_test_change", decision.reasons
        )

    def test_missing_required_metadata_is_rejected(self) -> None:
        patch = PatchSpec(
            cycle_id=CYCLE_ID,
            target_path=TARGET_PATH,
            changed_paths=(TARGET_PATH,),
            expected_before_sha256=self.patch.expected_before_sha256,
            replacement_text=self.patch.replacement_text,
            trigger=TRIGGER,
            hypothesis="",
            expected_effect=EXPECTED_EFFECT,
            fallback_criterion=FALLBACK_CRITERION,
        )

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn("missing_metadata:hypothesis", decision.reasons)

    def test_secret_like_replacement_is_rejected(self) -> None:
        secret_like = 'password = "' + ("x" * 12) + '"\n'
        patch = replace(self.patch, replacement_text=secret_like)

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn("secret_like_content", decision.reasons)

    def test_duplicate_changed_path_is_rejected(self) -> None:
        patch = replace(self.patch, changed_paths=(TARGET_PATH, TARGET_PATH))

        decision = self.governor.review(patch, "codex/observatory-selfmod-001")

        self.assertFalse(decision.approved)
        self.assertIn("duplicate_changed_path", decision.reasons)


if __name__ == "__main__":
    unittest.main()
