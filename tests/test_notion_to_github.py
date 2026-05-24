from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "notion_to_github.py"
SCRIPTS_DIR = ROOT / "scripts"


def load_module():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("notion_to_github", MODULE_PATH)
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


class PagedSession:
    def __init__(self, pages):
        self.pages = list(pages)
        self.headers = {}
        self.calls = 0

    def get(self, *args, **kwargs):
        page = self.pages[self.calls]
        self.calls += 1
        return FakeResponse(page)


class FakeConcurrency:
    def __init__(self):
        self.released = False

    def release(self):
        self.released = True


class FakeLog:
    def info(self, *args, **kwargs):
        return None

    def error(self, *args, **kwargs):
        return None


class NotionToGitHubTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_valid_modes_are_explicit(self):
        self.assertEqual(self.mod.VALID_MODES, {"full", "dry-run", "validate"})

    def test_find_issue_by_title_exact_skips_pull_requests_and_paginates(self):
        gh = self.mod.GH("token", "owner/repo")
        first_page = [
            {
                "title": "Change-001",
                "html_url": "https://example/pr",
                "pull_request": {"url": "https://example/pr"},
            }
        ]
        first_page.extend({"title": f"Other-{idx}", "html_url": f"https://example/{idx}"} for idx in range(99))
        gh.s = PagedSession(
            [
                first_page,
                [
                    {"title": "Change-001", "html_url": "https://example/issue"},
                ],
            ]
        )

        issue = gh.find_issue_by_title_exact("Change-001")

        self.assertEqual(issue["html_url"], "https://example/issue")
        self.assertEqual(gh.s.calls, 2)

    def test_validate_mode_counts_pending_and_skips_github_writes(self):
        concurrency = FakeConcurrency()

        class FakeNC:
            def __init__(self, token):
                self.token = token

            def query(self, *args, **kwargs):
                return [{"id": "page-1", "properties": {}}]

            def update(self, *args, **kwargs):
                raise AssertionError("validate mode must not update Notion")

        class FakeGH:
            def __init__(self, *args, **kwargs):
                pass

            def find_issue_by_title_exact(self, *args, **kwargs):
                raise AssertionError("validate mode must not inspect GitHub issues")

            def issue(self, *args, **kwargs):
                raise AssertionError("validate mode must not create GitHub issues")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config.json"
            config.write_text('{"github_repo":"owner/repo"}', encoding="utf-8")
            args = SimpleNamespace(
                mode="validate",
                shadow=str(root / "shadow"),
                log=str(root / "logs"),
                hash_out=str(root / "hash"),
                config=str(config),
                lock_file=str(root / "sync.lock"),
            )

            with patch.dict(
                os.environ,
                {
                    "NOTION_DATABASE_ID_CHANGES": "db-id",
                    "NOTION_TOKEN": "notion-token",
                    "GH_PAT": "github-token",
                },
                clear=True,
            ), patch.object(
                self.mod, "preflight_check", return_value=({"passed": 5}, concurrency)
            ), patch.object(self.mod, "NC", FakeNC), patch.object(
                self.mod, "GH", FakeGH
            ), patch.object(self.mod, "setup_logging", return_value=FakeLog()):
                self.mod.main(args)

            self.assertTrue((root / "hash").read_text(encoding="utf-8"))
            self.assertTrue(concurrency.released)

    def test_dry_run_reuses_existing_issue_without_creating_or_updating(self):
        concurrency = FakeConcurrency()
        calls = {"created": 0, "updated": 0}

        class FakeNC:
            def __init__(self, token):
                self.token = token

            def query(self, *args, **kwargs):
                return [
                    {
                        "id": "page-1",
                        "properties": {
                            "Change_ID": {
                                "type": "title",
                                "title": [{"plain_text": "Change-001"}],
                            }
                        },
                    }
                ]

            def update(self, *args, **kwargs):
                calls["updated"] += 1

        class FakeGH:
            def __init__(self, *args, **kwargs):
                pass

            def find_issue_by_title_exact(self, title):
                return {"html_url": f"https://github.com/owner/repo/issues/{title}"}

            def issue(self, *args, **kwargs):
                calls["created"] += 1
                raise AssertionError("dry-run dedupe must not create issues")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config.json"
            config.write_text(
                '{"github_repo":"owner/repo","title_field":"Change_ID"}',
                encoding="utf-8",
            )
            args = SimpleNamespace(
                mode="dry-run",
                shadow=str(root / "shadow"),
                log=str(root / "logs"),
                hash_out=str(root / "hash"),
                config=str(config),
                lock_file=str(root / "sync.lock"),
            )

            with patch.dict(
                os.environ,
                {
                    "NOTION_DATABASE_ID_CHANGES": "db-id",
                    "NOTION_TOKEN": "notion-token",
                    "GH_PAT": "github-token",
                },
                clear=True,
            ), patch.object(
                self.mod, "preflight_check", return_value=({"passed": 5}, concurrency)
            ), patch.object(self.mod, "NC", FakeNC), patch.object(
                self.mod, "GH", FakeGH
            ), patch.object(self.mod, "setup_logging", return_value=FakeLog()):
                self.mod.main(args)

            self.assertTrue((root / "hash").read_text(encoding="utf-8"))
            self.assertEqual(calls, {"created": 0, "updated": 0})
            self.assertTrue(concurrency.released)


if __name__ == "__main__":
    unittest.main()
