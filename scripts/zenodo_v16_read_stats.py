#!/usr/bin/env python3
"""Read Zenodo v16 statistics without permitting any remote mutation."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_API_BASE = "https://zenodo.org/api"
DEFAULT_RECORD_ID = "20732376"
EXPECTED_DOI = "10.5281/zenodo.20732376"
EXPECTED_CONCEPT_DOI = "10.5281/zenodo.19774446"
EXPECTED_VERSION = "v16"
READ_ONLY_METHOD = "GET"
STAT_KEYS = (
    "downloads",
    "unique_downloads",
    "views",
    "unique_views",
    "version_downloads",
    "version_unique_downloads",
    "version_views",
    "version_unique_views",
)


def assert_read_only_method(method: str) -> None:
    if method.upper() != READ_ONLY_METHOD:
        raise RuntimeError(f"Remote mutation blocked: HTTP method {method!r} is not allowed")


def normalize_token(value: str | None) -> str:
    if not value:
        return ""
    token = value.replace("\r", "").replace("\n", "").strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    return token


def request_json(url: str, token: str, attempts: int = 4) -> dict[str, Any]:
    assert_read_only_method("GET")
    headers = {
        "Accept": "application/json",
        "User-Agent": "TerraNova-Zenodo-ReadStats/1.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    raise RuntimeError(f"Unexpected Zenodo response: HTTP {response.status}")
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts:
                body = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"Zenodo GET failed: HTTP {exc.code}: {body[:500]}") from exc
            time.sleep(2 ** (attempt - 1))
        except urllib.error.URLError as exc:
            if attempt == attempts:
                raise RuntimeError(f"Zenodo GET failed: {exc}") from exc
            time.sleep(2 ** (attempt - 1))

    raise RuntimeError("Zenodo GET failed after retries")


def metadata_version(record: dict[str, Any]) -> str | None:
    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        return None
    value = metadata.get("version")
    return value if isinstance(value, str) and value.strip() else None


def validate_record(record: dict[str, Any], record_id: str) -> None:
    """Validate immutable v16 identity anchors.

    Zenodo publication records do not necessarily expose ``metadata.version``.
    The record is therefore bound primarily by the exact record id, DOI and
    concept DOI. If Zenodo does expose a version string, it must still match
    the expected v16 label; a conflicting value fails closed.
    """
    if str(record.get("id")) != record_id:
        raise RuntimeError(f"Unexpected record id: {record.get('id')!r}")
    if record.get("doi") != EXPECTED_DOI:
        raise RuntimeError(f"Unexpected DOI: {record.get('doi')!r}")
    if record.get("conceptdoi") != EXPECTED_CONCEPT_DOI:
        raise RuntimeError(f"Unexpected concept DOI: {record.get('conceptdoi')!r}")

    version = metadata_version(record)
    if version is not None and version != EXPECTED_VERSION:
        raise RuntimeError(f"Unexpected version: {version!r}")


def extract_stats(record: dict[str, Any]) -> dict[str, int]:
    stats = record.get("stats")
    if not isinstance(stats, dict):
        raise RuntimeError("Zenodo response has no stats object")

    result: dict[str, int] = {}
    missing: list[str] = []
    for key in STAT_KEYS:
        value = stats.get(key)
        if isinstance(value, bool) or not isinstance(value, int):
            missing.append(key)
        else:
            result[key] = value

    if missing:
        raise RuntimeError(f"Zenodo stats schema drift: missing/non-integer keys: {', '.join(missing)}")
    return result


def build_snapshot(record: dict[str, Any], authenticated: bool) -> dict[str, Any]:
    stats = extract_stats(record)
    observed_version = metadata_version(record)
    return {
        "collector": "ZENODO-V16-READ-STATS-001",
        "collector_schema": "1.1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "remote_method": "GET",
        "read_only": True,
        "authenticated": authenticated,
        "record_id": str(record["id"]),
        "doi": record.get("doi"),
        "conceptdoi": record.get("conceptdoi"),
        "expected_version": EXPECTED_VERSION,
        "metadata_version": observed_version,
        "version_binding": "metadata.version" if observed_version else "record_id+doi+conceptdoi",
        "updated": record.get("updated"),
        "stats": stats,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect authenticated read-only Zenodo v16 statistics.")
    parser.add_argument("--record-id", default=os.environ.get("ZENODO_RECORD_ID", DEFAULT_RECORD_ID))
    parser.add_argument("--api-base", default=os.environ.get("ZENODO_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-auth", action="store_true")
    args = parser.parse_args()

    token = normalize_token(os.environ.get("ZENODO_ACCESS_TOKEN"))
    if args.require_auth and not token:
        raise SystemExit("ZENODO_ACCESS_TOKEN is required but empty")

    url = f"{args.api_base.rstrip('/')}/records/{args.record_id}"
    record = request_json(url, token)
    validate_record(record, args.record_id)
    snapshot = build_snapshot(record, authenticated=bool(token))
    rendered = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
