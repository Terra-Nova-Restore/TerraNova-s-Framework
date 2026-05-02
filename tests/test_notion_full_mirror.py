from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "notion_full_mirror.py"


def load_module():
    spec = importlib.util.spec_from_file_location("notion_full_mirror", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, status_code: int, body: dict | None = None, text: str = ""):
        self.status_code = status_code
        self._body = body
        self.text = text
        self.headers = {}

    def json(self):
        if self._body is None:
            raise ValueError("no json")
        return self._body

    def raise_for_status(self):
        raise AssertionError("raise_for_status should not be called for handled statuses")


class FakeSession:
    def __init__(self, response: FakeResponse):
        self.response = response
        self.headers = {}
        self.calls = 0

    def request(self, *args, **kwargs):
        self.calls += 1
        return self.response


class NotionFullMirrorTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def test_permanent_4xx_is_not_retried_and_ids_are_redacted(self):
        notion_id = "123456781234123412341234567890ab"
        response = FakeResponse(
            403,
            {"message": f"Could not access database {notion_id}", "code": "restricted_resource"},
        )
        client = self.mod.NotionClient(
            "token",
            retry=self.mod.RetryConfig(max_attempts=5, base_backoff_s=0, max_backoff_s=0),
        )
        client.s = FakeSession(response)
        client._sleep = lambda seconds: None

        with self.assertRaisesRegex(RuntimeError, "HTTP 403") as raised:
            client.request("GET", f"https://api.notion.com/v1/databases/{notion_id}")

        self.assertEqual(client.s.calls, 1)
        self.assertNotIn(notion_id, str(raised.exception))
        self.assertIn("<redacted-id>", str(raised.exception))

    def test_database_query_stops_at_max_pages(self):
        client = self.mod.NotionClient("token")
        bodies = []

        def fake_request(method, url, *, params=None, json_body=None):
            bodies.append(json_body)
            return {
                "results": [{"id": "p1"}, {"id": "p2"}],
                "has_more": True,
                "next_cursor": "cursor",
            }

        client.request = fake_request

        pages, source_has_more = client.query_database_pages("db-id", max_pages=2)

        self.assertEqual([p["id"] for p in pages], ["p1", "p2"])
        self.assertTrue(source_has_more)
        self.assertEqual(len(bodies), 1)
        self.assertEqual(bodies[0]["page_size"], 2)

    def test_child_fetch_failure_fails_the_page_tree(self):
        class Client:
            def get_block_children_all(self, block_id, page_size=100):
                if block_id == "root":
                    return [{"id": "child", "type": "paragraph", "has_children": True}]
                raise RuntimeError("child fetch failed")

        with self.assertRaisesRegex(RuntimeError, "Failed to fetch children for block child"):
            self.mod.fetch_block_tree(Client(), "root")

    def test_manifest_separates_failed_skipped_and_unprocessed_pages(self):
        class Client:
            def query_database_pages(self, database_id, max_pages=None):
                return [{"id": "p1"}, {"id": "p2"}, {}], True

            def get_page(self, page_id):
                if page_id == "p2":
                    raise RuntimeError("page fetch failed")
                return {
                    "id": page_id,
                    "url": "https://notion.example/page",
                    "parent": None,
                    "archived": False,
                    "created_time": "2026-01-01T00:00:00.000Z",
                    "last_edited_time": "2026-01-01T00:00:00.000Z",
                    "properties": {
                        "Name": {
                            "type": "title",
                            "title": [{"plain_text": page_id, "annotations": {}, "href": None}],
                        }
                    },
                }

            def get_block_children_all(self, block_id, page_size=100):
                return []

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.mod.OUT_PAGES_DIR = root / "pages"
            self.mod.OUT_MANIFEST_PATH = root / "manifest.json"
            self.mod.LOG_DIR = root / "logs"

            manifest = self.mod.export_database_phase1(Client(), "db-id", max_pages=3)

        self.assertEqual(manifest["exported_page_count"], 1)
        self.assertEqual(manifest["queried_page_count"], 3)
        self.assertEqual(manifest["processed_page_count"], 3)
        self.assertEqual(len(manifest["failed_pages"]), 1)
        self.assertEqual(len(manifest["skipped_pages"]), 1)
        self.assertEqual(manifest["remaining_pages"], 0)
        self.assertTrue(manifest["source_has_more"])


if __name__ == "__main__":
    unittest.main()
