from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "preflight.py"


def load_module():
    spec = importlib.util.spec_from_file_location("tnv_preflight", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, body):
        self._body = body

    def json(self):
        return self._body

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self, get_response=None, post_response=None):
        self.headers = {}
        self.get_response = get_response
        self.post_response = post_response
        self.get_calls = []
        self.post_calls = []

    def get(self, url, **kwargs):
        self.get_calls.append((url, kwargs))
        return self.get_response

    def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        return self.post_response


class GitHubValidatorTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    @staticmethod
    def repo_body(push):
        return {
            "full_name": "owner/repo",
            "private": True,
            "permissions": {"push": push},
        }

    def validator_with_response(self, push):
        validator = self.mod.GitHubValidator("github-token")
        session = FakeSession(get_response=FakeResponse(self.repo_body(push)))
        validator.session = session
        return validator, session

    def assert_repository_get(self, session):
        self.assertEqual(
            session.get_calls,
            [("https://api.github.com/repos/owner/repo", {})],
        )
        self.assertEqual(session.post_calls, [])

    def test_pat_without_push_permission_fails(self):
        validator, session = self.validator_with_response(push=False)

        with patch.dict(
            os.environ,
            {
                "GH_PAT": "pat-token",
                "GITHUB_TOKEN": "actions-token",
                "GITHUB_ACTIONS": "true",
            },
            clear=True,
        ):
            with self.assertRaisesRegex(
                self.mod.PreflightError, "lacks write permission"
            ):
                validator.test_repo_access("owner/repo")

        self.assert_repository_get(session)

    def test_actions_token_without_push_permission_uses_workflow_permissions(self):
        notion_session = FakeSession(
            post_response=FakeResponse({"object": "list", "results": []})
        )
        github_session = FakeSession(
            get_response=FakeResponse(self.repo_body(push=False))
        )

        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "config.json"
            config_path.write_text('{"github_repo":"owner/repo"}', encoding="utf-8")
            lock_path = Path(tmp) / "sync.lock"

            with patch.dict(
                os.environ,
                {
                    "NOTION_TOKEN": "notion-token",
                    "GITHUB_TOKEN": "actions-token",
                    "GITHUB_ACTIONS": "true",
                },
                clear=True,
            ), patch.object(
                self.mod.requests,
                "Session",
                side_effect=[notion_session, github_session],
            ):
                results, concurrency = self.mod.PreflightChecker().run(
                    "database-id", config_path, lock_path
                )

            concurrency.release()

        self.assertEqual(
            results["checks"]["github_access"]["permission_validation"],
            {
                "method": "github_actions_workflow_permissions",
                "repository_push": False,
            },
        )
        self.assert_repository_get(github_session)

    def test_local_github_token_without_push_permission_fails(self):
        validator, session = self.validator_with_response(push=False)

        with patch.dict(
            os.environ,
            {"GITHUB_TOKEN": "local-token"},
            clear=True,
        ):
            with self.assertRaisesRegex(
                self.mod.PreflightError, "lacks write permission"
            ):
                validator.test_repo_access("owner/repo")

        self.assert_repository_get(session)

    def test_push_permission_metadata_remains_successful(self):
        validator, session = self.validator_with_response(push=True)

        with patch.dict(os.environ, {"GH_PAT": "pat-token"}, clear=True):
            result = validator.test_repo_access("owner/repo")

        self.assertTrue(result["push_permission"])
        self.assertEqual(
            result["permission_validation"],
            {
                "method": "repository_push_metadata",
                "repository_push": True,
            },
        )
        self.assert_repository_get(session)


if __name__ == "__main__":
    unittest.main()
