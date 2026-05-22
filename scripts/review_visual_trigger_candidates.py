#!/usr/bin/env python3
"""Review MMD-003 visual trigger candidates for MMD-004 canon gates."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"

SAFE_NUMERIC_MODULES = {
    "516": "Inspiration",
    "520": "SessionStart",
    "521": "Preflight",
    "540": "Observable Momentum",
    "544": "Synchronization Node",
}

CAUTION_NUMERIC_MODULES = {
    "517": "AutoFlow",
}

SOURCE_NEEDED_REFS = {
    "174-210": "Silvi/Codex139 range",
    "600": "Trigger list / trigger field",
}

SENS_HELD_REFS = {
    "777": "Schattenarchiv",
    "988": "Snapshot Lockpoint",
    "989": "Token Sync Beacon",
    "990": "Trigger Audit Engine",
    "991": "ZIP Integrity Pulse",
    "992": "TriggerMap Echo Sync",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (CONTROL_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def refs(row: dict[str, str]) -> list[str]:
    return [ref for ref in (row.get("Trigger References") or "").split(";") if ref]


def decide_candidate(row: dict[str, str]) -> tuple[str, str, str, str]:
    row_refs = refs(row)
    sensitivity = row.get("Sensitivity", "")
    klass = row.get("Candidate Class", "")

    if sensitivity == "Restricted" or any(ref in SENS_HELD_REFS for ref in row_refs):
        return "SENS-HELD", "hold_restricted_or_sensitive", "blocked", "SENS-001 before expansion"
    if sensitivity == "Sensitive":
        return "SENS-HELD", "hold_sensitive", "blocked", "SENS-001 before expansion"

    if any(ref in CAUTION_NUMERIC_MODULES for ref in row_refs):
        return "CAUTION-AUTOFLOW", "observer_required", "defer", "AutoFlow is not normalized as routine work"
    if any(ref in SAFE_NUMERIC_MODULES for ref in row_refs):
        return "CAP-MODULE-CANDIDATE", "promote_module_candidate", "candidate", "Safe internal anchor candidate"
    if any(ref in SOURCE_NEEDED_REFS for ref in row_refs):
        return "CANON-SOURCE-NEEDED", "needs_source_review", "defer", "Visible reference requires source review"

    if klass == "sync_surface":
        return "CONTROL-SURFACE", "promote_control_surface", "candidate", "Useful for CAP routing, not a TRG assignment"
    if klass == "audit_surface":
        return "CONTROL-SURFACE", "promote_audit_surface", "candidate", "Useful for CAP audit routing, not a TRG assignment"
    if klass in {"trigger_surface", "codex_surface"}:
        return "CONTEXT-SURFACE", "route_context_surface", "context", "Visual context only"

    return "CONTEXT-SURFACE", "route_context_surface", "context", "Visual context only"


def decide_guard(row: dict[str, str]) -> tuple[str, str, str]:
    row_refs = refs(row)
    sensitivity = row.get("Sensitivity", "")
    if sensitivity in {"Sensitive", "Restricted"} or any(ref in SENS_HELD_REFS for ref in row_refs):
        return "SENS-HELD", "blocked", "Relation held behind SENS-001"
    if any(ref in CAUTION_NUMERIC_MODULES for ref in row_refs):
        return "CAUTION-AUTOFLOW", "defer", "AutoFlow guard needs observer framing"
    if row.get("Guard Condition"):
        return "GUARD-CANDIDATE", "candidate", "Guard can support route understanding"
    return "STRUCTURAL-RELATION", "context", "Unlabeled visual relation"


def build_candidate_review(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in candidates:
        lane, decision, gate_status, reason = decide_candidate(row)
        rows.append(
            {
                "Review ID": f"MMD4-C{len(rows) + 1:03d}",
                "Bridge ID": row["Bridge ID"],
                "Graph ID": row["Graph ID"],
                "Node ID": row["Node ID"],
                "Label": row["Label"],
                "Trigger References": row["Trigger References"],
                "Candidate Class": row["Candidate Class"],
                "Sensitivity": row["Sensitivity"],
                "Lane": lane,
                "Gate Decision": decision,
                "Gate Status": gate_status,
                "Reason": reason,
                "Canonical TRG Status": "not assigned",
                "Boundary": "Visual evidence only; canon remains separate.",
            }
        )
    return rows


def build_guard_review(guards: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in guards:
        lane, gate_status, reason = decide_guard(row)
        rows.append(
            {
                "Review ID": f"MMD4-G{len(rows) + 1:03d}",
                "Bridge Edge ID": row["Bridge Edge ID"],
                "Graph ID": row["Graph ID"],
                "Source Node": row["Source Node"],
                "Target Node": row["Target Node"],
                "Guard Condition": row["Guard Condition"],
                "Trigger References": row["Trigger References"],
                "Sensitivity": row["Sensitivity"],
                "Lane": lane,
                "Gate Status": gate_status,
                "Reason": reason,
                "Boundary": "Guard relation only; not execution permission.",
            }
        )
    return rows


def build_module_records(candidate_review: list[dict[str, str]]) -> list[dict[str, str]]:
    evidence_by_ref: dict[str, list[str]] = defaultdict(list)
    lane_by_ref: dict[str, str] = {}
    status_by_ref: dict[str, str] = {}
    reason_by_ref: dict[str, str] = {}

    for row in candidate_review:
        for ref in refs(row):
            if ref not in SAFE_NUMERIC_MODULES and ref not in CAUTION_NUMERIC_MODULES and ref not in SOURCE_NEEDED_REFS and ref not in SENS_HELD_REFS:
                continue
            evidence_by_ref[ref].append(f"{row['Graph ID']}::{row['Node ID']}::{row['Label']}")
            if ref in SAFE_NUMERIC_MODULES:
                lane_by_ref[ref] = "CAP-MODULE-CANDIDATE"
                status_by_ref[ref] = "candidate"
                reason_by_ref[ref] = "Known safe internal anchor in visual evidence and canon reference."
            elif ref in CAUTION_NUMERIC_MODULES:
                lane_by_ref[ref] = "CAUTION-AUTOFLOW"
                status_by_ref[ref] = "defer"
                reason_by_ref[ref] = "AutoFlow requires observer framing and must not be normalized."
            elif ref in SOURCE_NEEDED_REFS:
                lane_by_ref[ref] = "CANON-SOURCE-NEEDED"
                status_by_ref[ref] = "defer"
                reason_by_ref[ref] = "Visible reference/range requires source review before module record."
            else:
                lane_by_ref[ref] = "SENS-HELD"
                status_by_ref[ref] = "blocked"
                reason_by_ref[ref] = "Sensitive or restricted trigger reference."

    rows: list[dict[str, str]] = []
    for ref in sorted(evidence_by_ref, key=lambda item: int(item.split("-", 1)[0])):
        title = SAFE_NUMERIC_MODULES.get(ref) or CAUTION_NUMERIC_MODULES.get(ref) or SOURCE_NEEDED_REFS.get(ref) or SENS_HELD_REFS.get(ref) or f"Trigger {ref}"
        rows.append(
            {
                "Module Candidate ID": f"CAP-TRG-CAND-{len(rows) + 1:03d}",
                "Visible Reference": ref,
                "Working Name": title,
                "Lane": lane_by_ref[ref],
                "Gate Status": status_by_ref[ref],
                "Canonical TRG ID": "",
                "Evidence Count": str(len(evidence_by_ref[ref])),
                "Evidence": " | ".join(evidence_by_ref[ref][:5]),
                "Reason": reason_by_ref[ref],
                "Next Action": "eligible for CAP module registry draft" if status_by_ref[ref] == "candidate" else "hold for source or sensitivity review",
            }
        )
    return rows


def build_lane_summary(candidate_review: list[dict[str, str]], guard_review: list[dict[str, str]]) -> list[dict[str, str]]:
    candidate_counts = Counter(row["Lane"] for row in candidate_review)
    guard_counts = Counter(row["Lane"] for row in guard_review)
    lanes = sorted(set(candidate_counts) | set(guard_counts))
    rows: list[dict[str, str]] = []
    for lane in lanes:
        rows.append(
            {
                "Lane": lane,
                "Candidate Rows": str(candidate_counts.get(lane, 0)),
                "Guard Rows": str(guard_counts.get(lane, 0)),
                "Gate Meaning": {
                    "CAP-MODULE-CANDIDATE": "Safe visible numeric anchor can become a CAP module candidate.",
                    "CAUTION-AUTOFLOW": "Autoflow-related material requires observer framing.",
                    "CANON-SOURCE-NEEDED": "Visible reference exists but source review is required.",
                    "CONTEXT-SURFACE": "Useful context, not a trigger module.",
                    "CONTROL-SURFACE": "Useful CAP routing/control surface.",
                    "GUARD-CANDIDATE": "Guard relation can support route understanding.",
                    "SENS-HELD": "Blocked behind SENS-001.",
                    "STRUCTURAL-RELATION": "Unlabeled structural relation.",
                }.get(lane, "Review lane."),
            }
        )
    return rows


def main() -> int:
    candidates = read_csv("mmd-003.visual-trigger-candidates.csv")
    guards = read_csv("mmd-003.guard-bridge.csv")
    candidate_review = build_candidate_review(candidates)
    guard_review = build_guard_review(guards)
    module_records = build_module_records(candidate_review)
    lane_summary = build_lane_summary(candidate_review, guard_review)

    write_csv(
        CONTROL_DIR / "mmd-004.candidate-review.csv",
        candidate_review,
        [
            "Review ID",
            "Bridge ID",
            "Graph ID",
            "Node ID",
            "Label",
            "Trigger References",
            "Candidate Class",
            "Sensitivity",
            "Lane",
            "Gate Decision",
            "Gate Status",
            "Reason",
            "Canonical TRG Status",
            "Boundary",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-004.guard-review.csv",
        guard_review,
        [
            "Review ID",
            "Bridge Edge ID",
            "Graph ID",
            "Source Node",
            "Target Node",
            "Guard Condition",
            "Trigger References",
            "Sensitivity",
            "Lane",
            "Gate Status",
            "Reason",
            "Boundary",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-004.module-record-candidates.csv",
        module_records,
        [
            "Module Candidate ID",
            "Visible Reference",
            "Working Name",
            "Lane",
            "Gate Status",
            "Canonical TRG ID",
            "Evidence Count",
            "Evidence",
            "Reason",
            "Next Action",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-004.lane-summary.csv",
        lane_summary,
        ["Lane", "Candidate Rows", "Guard Rows", "Gate Meaning"],
    )

    summary = {
        "review_id": "MMD-004",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "candidate_review_rows": len(candidate_review),
        "guard_review_rows": len(guard_review),
        "module_record_candidates": len(module_records),
        "lane_summary_rows": len(lane_summary),
        "candidate_lane_counts": dict(sorted(Counter(row["Lane"] for row in candidate_review).items())),
        "guard_lane_counts": dict(sorted(Counter(row["Lane"] for row in guard_review).items())),
        "eligible_module_candidates": [
            row["Visible Reference"] for row in module_records if row["Gate Status"] == "candidate"
        ],
        "held_references": [
            row["Visible Reference"] for row in module_records if row["Gate Status"] != "candidate"
        ],
        "boundary": "Review and canon gate only; no canonical TRG assignment.",
    }
    (CONTROL_DIR / "mmd-004.review-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
