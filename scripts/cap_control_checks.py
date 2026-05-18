#!/usr/bin/env python3
"""Run no-credit CAP control checks.

This script validates the local CAP control tower artifacts and can optionally
read the public Zenodo API. It never writes to Notion or Zenodo.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"
ZENODO_REFERENCE = REPO_ROOT / "docs" / "references" / "zenodo.md"

EXPECTED_CSV_ROWS = {
    "cap-0.3.workstream-map.csv": 7,
    "canon-source-tier-map.csv": 8,
    "canon-elevation-queue.csv": 9,
    "cap-rt-001.action-queue.csv": 6,
    "cap-rt-001.dashboard-lanes.csv": 8,
    "cap-rt-001.guardrails.csv": 10,
    "cap-rt-001.source-routing.csv": 7,
    "dup-002.verification-manifest.csv": 8,
    "mmd-002.graphs.csv": 11,
    "mmd-002.nodes.csv": 277,
    "mmd-002.edges.csv": 363,
    "mmd-002.guard-conditions.csv": 363,
    "mmd-002.extraction-gaps.csv": 4,
    "mmd-003.visual-trigger-candidates.csv": 53,
    "mmd-003.guard-bridge.csv": 140,
    "mmd-003.sensitivity-review.csv": 20,
    "mmd-004.candidate-review.csv": 53,
    "mmd-004.guard-review.csv": 140,
    "mmd-004.module-record-candidates.csv": 14,
    "mmd-004.lane-summary.csv": 8,
    "mmd-005.cap-module-drafts.csv": 5,
    "mmd-005.module-evidence.csv": 33,
    "mmd-005.module-relation-map.csv": 21,
    "mmd-005.hash-ledger.csv": 5,
    "mmd-006.registry-package.csv": 5,
    "mmd-006.registry-field-map.csv": 27,
    "mmd-006.view-package.csv": 2,
    "mmd-006.notion-mutation-package.csv": 4,
    "mmd-006.registry-updates.csv": 8,
    "mmd-007.source-index.csv": 5,
    "mmd-007.canon-admission-levels.csv": 5,
    "mmd-007.source-review.csv": 5,
    "mmd-007.canon-decision-queue.csv": 5,
    "mmd-001.diagram-inventory.csv": 14,
    "mmd-001.relation-map.csv": 14,
    "ninf-001.registry-updates.csv": 5,
    "prism-002.next-release-checklist.csv": 7,
    "prism-002.release-readiness-gate.csv": 10,
    "registry-002.field-package.csv": 9,
    "registry-002.module-canon-updates.csv": 5,
    "registry-002.notion-mutation-package.csv": 4,
    "registry-002.registry-updates.csv": 8,
    "sens-002.protected-lane-review.csv": 7,
    "sens-002.elevation-gate.csv": 5,
    "sens-002.notion-mutation-package.csv": 3,
    "source-520.source-ledger.csv": 10,
    "source-520.claim-review.csv": 9,
    "source-520.elevation-decision.csv": 3,
    "source-520.bounded-test-gate.csv": 5,
    "source-520.notion-mutation-package.csv": 4,
    "source-520.registry-updates.csv": 4,
    "source-521.source-ledger.csv": 9,
    "source-521.claim-review.csv": 9,
    "source-521.elevation-decision.csv": 3,
    "source-521.notion-mutation-package.csv": 4,
    "source-521.registry-updates.csv": 4,
    "dash-zen-001.notion-mutation-package.csv": 5,
    "dash-zen-001.registry-updates.csv": 4,
    "dash-zen-002.source-review.csv": 7,
    "dash-zen-002.sensitivity-review.csv": 7,
    "dash-zen-002.elevation-decision.csv": 7,
    "dash-zen-002.notion-mutation-package.csv": 5,
    "dash-zen-002.registry-updates.csv": 5,
    "dash-zen-003.anchor-review.csv": 3,
    "dash-zen-003.elevation-decision.csv": 3,
    "dash-zen-003.registry-package.csv": 3,
    "dash-zen-003.notion-mutation-package.csv": 4,
    "dash-zen-003.registry-updates.csv": 4,
    "dash-zen-004.release-state-matrix.csv": 6,
    "dash-zen-004.authority-map.csv": 4,
    "dash-zen-004.reconciliation-rules.csv": 6,
    "dash-zen-004.registry-package.csv": 1,
    "dash-zen-004.notion-mutation-package.csv": 2,
    "dash-zen-004.registry-updates.csv": 2,
    "pause-001.next-actions.csv": 6,
    "sync-003.git-trace-manifest.csv": 8,
    "sync-004.git-trace-manifest.csv": 12,
    "sync-002.registry-updates.csv": 5,
    "test-520.test-cases.csv": 5,
    "test-520.results.csv": 5,
    "trigger-001.control-crosswalk.csv": 14,
    "trigger-001.blocked-actions.csv": 12,
    "trigger-001.test-cases.csv": 12,
}

REQUIRED_FILES = [
    "batch-auto-001.md",
    "batch-canon-002.md",
    "batch-cap-rt-001.md",
    "batch-dup-002.md",
    "batch-mmd-001.md",
    "batch-mmd-002.md",
    "batch-mmd-003.md",
    "batch-mmd-004.md",
    "batch-mmd-005.md",
    "batch-mmd-006.md",
    "batch-mmd-007.md",
    "batch-ninf-001.md",
    "batch-prism-002.md",
    "batch-registry-002.md",
    "batch-sens-002.md",
    "batch-source-520.md",
    "batch-source-521.md",
    "batch-dash-zen-001.md",
    "batch-dash-zen-002.md",
    "batch-dash-zen-003.md",
    "batch-dash-zen-004.md",
    "batch-pause-001.md",
    "batch-pr-048-human-review.md",
    "batch-pr-048-ready-gate.md",
    "batch-pr-048-review-decision.md",
    "batch-sync-003.md",
    "batch-sync-004.md",
    "batch-sync-002.md",
    "batch-test-520.md",
    "batch-trigger-001.md",
    "causal-log.auto-001-plan-2026-05-17.json",
    "causal-log.cap-rt-001-plan-2026-05-18.json",
    "causal-log.cap-0.4-iperka-2026-05-17.json",
    "causal-log.dup-002-plan-2026-05-17.json",
    "causal-log.mmd-001-readpass-2026-05-17.json",
    "causal-log.mmd-002-extraction-2026-05-17.json",
    "causal-log.mmd-003-bridge-2026-05-17.json",
    "causal-log.mmd-004-canon-gate-2026-05-17.json",
    "causal-log.mmd-005-module-drafts-2026-05-17.json",
    "causal-log.mmd-006-registry-package-2026-05-17.json",
    "causal-log.mmd-006-mutation-2026-05-17.json",
    "causal-log.mmd-007-source-review-2026-05-17.json",
    "causal-log.ninf-001-mutation-2026-05-17.json",
    "causal-log.prism-002-plan-2026-05-17.json",
    "causal-log.registry-002-plan-2026-05-17.json",
    "causal-log.registry-002-mutation-2026-05-17.json",
    "causal-log.sens-002-plan-2026-05-17.json",
    "causal-log.source-520-primary-source-pass-2026-05-18.json",
    "causal-log.source-520-mutation-2026-05-18.json",
    "causal-log.source-521-primary-source-pass-2026-05-17.json",
    "causal-log.source-521-mutation-2026-05-18.json",
    "causal-log.dash-zen-001-mutation-2026-05-18.json",
    "causal-log.dash-zen-002-mutation-2026-05-18.json",
    "causal-log.dash-zen-003-mutation-2026-05-18.json",
    "causal-log.dash-zen-004-mutation-2026-05-18.json",
    "causal-log.pause-001-handoff-2026-05-18.json",
    "causal-log.pr-048-human-review-2026-05-18.json",
    "causal-log.pr-048-ready-gate-2026-05-18.json",
    "causal-log.pr-048-review-decision-2026-05-18.json",
    "causal-log.sync-003-github-trace-closure-2026-05-18.json",
    "causal-log.sync-004-github-trace-closure-2026-05-18.json",
    "causal-log.sync-002-mutation-2026-05-17.json",
    "causal-log.test-520-bounded-sessionstart-2026-05-18.json",
    "causal-log.trigger-001-plan-2026-05-17.json",
    "mmd-001.mermaid-universe-readpass.md",
    "mmd-002.graph-extraction.md",
    "mmd-002.extraction-summary.json",
    "mmd-003.visual-trigger-bridge.md",
    "mmd-003.bridge-summary.json",
    "mmd-004.candidate-review-and-canon-gate.md",
    "mmd-004.review-summary.json",
    "mmd-005.cap-module-drafts.md",
    "mmd-005.hash-material.json",
    "mmd-005.review-summary.json",
    "mmd-006.apply-gate.md",
    "mmd-006.registry-package.md",
    "mmd-006.review-summary.json",
    "mmd-007.cap-module-source-review.md",
    "mmd-007.review-summary.json",
    "cap-0.4-canon-admission-iperka.md",
    "cap-rt-001.bedienungshandbuch.md",
    "cap-rt-001.runtime-contract.md",
    "canon-admission-rulebook.md",
    "prism-002.zenodo-live-delta-2026-05-17.json",
    "registry-002.apply-gate.md",
    "registry-002.review-summary.json",
    "sens-002.preflight-boundary.md",
    "sens-002.review-summary.json",
    "source-520.primary-source-pass.md",
    "source-520.review-summary.json",
    "source-521.primary-source-pass.md",
    "source-521.review-summary.json",
    "dash-zen-001.review-summary.json",
    "dash-zen-002.review-summary.json",
    "dash-zen-003.review-summary.json",
    "dash-zen-004.review-summary.json",
    "pause-001.review-summary.json",
    "pause-001.solo-operating-playbook.md",
    "cap-rt-001.review-summary.json",
    "pr-048-human-review.review-summary.json",
    "pr-048-ready-gate.review-summary.json",
    "pr-048-review-decision.review-summary.json",
    "test-520.sessionstart-bounded-test.md",
    "test-520.review-summary.json",
    "trigger-001.command-surface.md",
]

EXPECTED_ZENODO = {
    "record_id": "20073579",
    "doi": "10.5281/zenodo.20073579",
    "conceptdoi": "10.5281/zenodo.19774446",
    "version": "RC01-v12",
    "publication_date": "2026-05-17",
    "file_key": "main (44).pdf",
    "file_checksum": "md5:d791d480e75f3d89f9a103a28a5c5001",
    "file_size": 2943457,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_required_files(errors: list[str]) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for name in REQUIRED_FILES:
        exists = (CONTROL_DIR / name).is_file()
        results[name] = exists
        if not exists:
            add_error(errors, f"missing required file: {name}")
    return results


def check_csvs(errors: list[str]) -> dict[str, int | None]:
    results: dict[str, int | None] = {}
    for name, expected in EXPECTED_CSV_ROWS.items():
        path = CONTROL_DIR / name
        if not path.is_file():
            results[name] = None
            add_error(errors, f"missing CSV: {name}")
            continue
        count = csv_row_count(path)
        results[name] = count
        if count != expected:
            add_error(errors, f"{name}: expected {expected} rows, got {count}")
    return results


def check_causal_logs(errors: list[str]) -> dict[str, Any]:
    logs = sorted(path for path in CONTROL_DIR.glob("causal-log.*.json") if path.name != "causal-log.schema.json")
    parsed = 0
    legacy_missing_ids: list[str] = []
    external_mutations = 0

    for path in logs:
        try:
            data = read_json(path)
        except json.JSONDecodeError as exc:
            add_error(errors, f"{path.name}: invalid JSON: {exc}")
            continue
        parsed += 1
        if not data.get("log_id") and not data.get("event_id"):
            legacy_missing_ids.append(path.name)
        if data.get("external_mutation") is True:
            external_mutations += 1

    return {
        "count": len(logs),
        "parsed": parsed,
        "legacy_missing_ids": legacy_missing_ids,
        "external_mutation_logs": external_mutations,
    }


def check_zenodo_reference(errors: list[str]) -> dict[str, bool]:
    text = ZENODO_REFERENCE.read_text(encoding="utf-8") if ZENODO_REFERENCE.is_file() else ""
    checks = {
        "has_current_title": "FerrAI-Terra'Nova CIC Framework" in text
        or "FerrAI–Terra'Nova CIC Framework" in text,
        "has_current_publication_date": "2026-05-17" in text,
        "has_current_doi": EXPECTED_ZENODO["doi"] in text,
        "has_live_delta": "PRISM-002 Live Metadata Delta" in text,
    }
    for key, passed in checks.items():
        if not passed:
            add_error(errors, f"zenodo reference check failed: {key}")
    return checks


def check_live_delta(errors: list[str]) -> dict[str, Any]:
    path = CONTROL_DIR / "prism-002.zenodo-live-delta-2026-05-17.json"
    if not path.is_file():
        add_error(errors, "missing prism-002 live delta file")
        return {}
    data = read_json(path)
    checks = {
        "record_id": str(data.get("record_id")) == EXPECTED_ZENODO["record_id"],
        "doi": data.get("doi") == EXPECTED_ZENODO["doi"],
        "conceptdoi": data.get("conceptdoi") == EXPECTED_ZENODO["conceptdoi"],
        "version": data.get("version") == EXPECTED_ZENODO["version"],
        "publication_date": data.get("publication_date") == EXPECTED_ZENODO["publication_date"],
        "file_checksum": data.get("file", {}).get("checksum") == EXPECTED_ZENODO["file_checksum"],
        "file_size": data.get("file", {}).get("size") == EXPECTED_ZENODO["file_size"],
    }
    for key, passed in checks.items():
        if not passed:
            add_error(errors, f"live delta check failed: {key}")
    return {"checks": checks, "title": data.get("title")}


def fetch_live_zenodo(errors: list[str]) -> dict[str, Any]:
    url = f"https://zenodo.org/api/records/{EXPECTED_ZENODO['record_id']}"
    with urllib.request.urlopen(url, timeout=20) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    files = data.get("files", [])
    first_file = files[0] if files else {}
    checks = {
        "record_id": str(data.get("id")) == EXPECTED_ZENODO["record_id"],
        "doi": data.get("doi") == EXPECTED_ZENODO["doi"],
        "conceptdoi": data.get("conceptdoi") == EXPECTED_ZENODO["conceptdoi"],
        "version": data.get("metadata", {}).get("version") == EXPECTED_ZENODO["version"],
        "publication_date": data.get("metadata", {}).get("publication_date")
        == EXPECTED_ZENODO["publication_date"],
        "file_key": first_file.get("key") == EXPECTED_ZENODO["file_key"],
        "file_checksum": first_file.get("checksum") == EXPECTED_ZENODO["file_checksum"],
        "file_size": first_file.get("size") == EXPECTED_ZENODO["file_size"],
    }
    for key, passed in checks.items():
        if not passed:
            add_error(errors, f"live Zenodo API check failed: {key}")
    return {
        "url": url,
        "checks": checks,
        "title": data.get("metadata", {}).get("title"),
        "updated": data.get("updated"),
    }


def build_report(live_zenodo: bool) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    report: dict[str, Any] = {
        "check_id": "AUTO-001",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(REPO_ROOT),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "checks": {},
    }

    report["checks"]["required_files"] = check_required_files(errors)
    report["checks"]["csv_rows"] = check_csvs(errors)
    report["checks"]["causal_logs"] = check_causal_logs(errors)
    report["checks"]["zenodo_reference"] = check_zenodo_reference(errors)
    report["checks"]["zenodo_live_delta"] = check_live_delta(errors)
    if live_zenodo:
        report["checks"]["zenodo_live_api"] = fetch_live_zenodo(errors)

    report["status"] = "pass" if not errors else "fail"
    report["errors"] = errors
    return report, errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run no-credit CAP control checks.")
    parser.add_argument(
        "--live-zenodo",
        action="store_true",
        help="Read the public Zenodo API and verify the current record state.",
    )
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args(argv[1:])

    report, errors = build_report(args.live_zenodo)

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = REPO_ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
