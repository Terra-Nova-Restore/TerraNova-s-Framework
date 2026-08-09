from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "zenodo_v16_read_stats.py"
SPEC = importlib.util.spec_from_file_location("zenodo_v16_read_stats", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    status = 200

    def __init__(self, payload: dict | str) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        if isinstance(self.payload, str):
            return self.payload.encode("utf-8")
        return json.dumps(self.payload).encode("utf-8")


class ZenodoV16ReadStatsTests(unittest.TestCase):
    def sample_record(self) -> dict:
        return {
            "id": 20732376,
            "doi": MODULE.EXPECTED_DOI,
            "conceptdoi": MODULE.EXPECTED_CONCEPT_DOI,
            "updated": "2026-08-09T00:00:00+00:00",
            "metadata": {"version": MODULE.EXPECTED_VERSION},
            "stats": {
                "downloads": 686,
                "unique_downloads": 530,
                "views": 824,
                "unique_views": 679,
                "version_downloads": 39,
                "version_unique_downloads": 31,
                "version_views": 123,
                "version_unique_views": 107,
            },
        }

    def sample_landing_html(self) -> str:
        return """
        <section>
          <span>Data volume</span>
          <div>All versions</div><strong>1.8 GB</strong>
          <div>This version</div><strong>115.4 MB</strong>
        </section>
        """

    def test_rejects_every_non_get_method(self) -> None:
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                with self.assertRaises(RuntimeError):
                    MODULE.assert_read_only_method(method)

    def test_request_uses_get_and_bearer_without_printing_token(self) -> None:
        record = self.sample_record()
        with patch.object(MODULE.urllib.request, "urlopen", return_value=FakeResponse(record)) as mocked:
            result = MODULE.request_json("https://zenodo.org/api/records/20732376", "secret-token")
        self.assertEqual(result, record)
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.headers.get("Authorization"), "Bearer secret-token")

    def test_landing_request_is_also_get_only(self) -> None:
        page = self.sample_landing_html()
        with patch.object(MODULE.urllib.request, "urlopen", return_value=FakeResponse(page)) as mocked:
            result = MODULE.request_text("https://zenodo.org/records/20732376", "secret-token")
        self.assertIn("Data volume", result)
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.headers.get("Authorization"), "Bearer secret-token")

    def test_validates_current_v16_identity_when_version_is_present(self) -> None:
        MODULE.validate_record(self.sample_record(), "20732376")

    def test_allows_missing_optional_metadata_version_with_strong_identity_anchors(self) -> None:
        record = self.sample_record()
        record["metadata"].pop("version")
        MODULE.validate_record(record, "20732376")
        snapshot = MODULE.build_snapshot(record, authenticated=True)
        self.assertIsNone(snapshot["metadata_version"])
        self.assertEqual(snapshot["expected_version"], "v16")
        self.assertEqual(snapshot["version_binding"], "record_id+doi+conceptdoi")

    def test_rejects_conflicting_metadata_version_when_present(self) -> None:
        record = self.sample_record()
        record["metadata"]["version"] = "v15"
        with self.assertRaises(RuntimeError):
            MODULE.validate_record(record, "20732376")

    def test_extracts_exact_eight_statistics(self) -> None:
        stats = MODULE.extract_stats(self.sample_record())
        self.assertEqual(tuple(stats), MODULE.STAT_KEYS)
        self.assertEqual(stats["unique_views"], 679)
        self.assertEqual(stats["version_unique_downloads"], 31)

    def test_fails_closed_on_stats_schema_drift(self) -> None:
        record = self.sample_record()
        del record["stats"]["version_unique_views"]
        with self.assertRaises(RuntimeError):
            MODULE.extract_stats(record)

    def test_extracts_directly_displayed_data_volume_without_reconstruction(self) -> None:
        volume = MODULE.extract_data_volume(self.sample_landing_html())
        self.assertTrue(volume["available"])
        self.assertEqual(volume["all_versions"], "1.8 GB")
        self.assertEqual(volume["this_version"], "115.4 MB")
        self.assertEqual(volume["source"], "zenodo_record_landing_page")

    def test_data_volume_unavailable_is_explicit_not_invented(self) -> None:
        volume = MODULE.extract_data_volume("<html><body>No usage block</body></html>")
        self.assertFalse(volume["available"])
        self.assertIsNone(volume["all_versions"])
        self.assertIsNone(volume["this_version"])

    def test_snapshot_marks_remote_path_read_only(self) -> None:
        data_volume = MODULE.extract_data_volume(self.sample_landing_html())
        snapshot = MODULE.build_snapshot(self.sample_record(), authenticated=True, data_volume=data_volume)
        self.assertTrue(snapshot["read_only"])
        self.assertTrue(snapshot["authenticated"])
        self.assertEqual(snapshot["remote_method"], "GET")
        self.assertEqual(snapshot["record_id"], "20732376")
        self.assertEqual(snapshot["version_binding"], "metadata.version")
        self.assertEqual(snapshot["collector_schema"], "1.2")
        self.assertEqual(snapshot["data_volume"]["all_versions"], "1.8 GB")
        self.assertEqual(snapshot["data_volume"]["this_version"], "115.4 MB")


if __name__ == "__main__":
    unittest.main()
