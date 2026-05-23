#!/usr/bin/env python3
"""Build SOURCE-174-210 review scaffolding from TRIGGER-MAP-001 and XPORT-002.

The package starts the per-trigger review corridor for Trigger 174-210 without
printing raw ChatGPT export content, local paths, conversation IDs or account
data. XPORT-002 samples are used as hashed review corridors, not as direct
semantic authority.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
BATCH = "SOURCE-174-210"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T13:31:24+02:00"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def split_items(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def trigger_number(row: dict[str, str]) -> int | None:
    value = row.get("trigger_ref", "")
    return int(value) if value.isdigit() else None


def handles(rows: list[dict[str, str]], focus: str) -> list[str]:
    return [row["Sample Handle"] for row in rows if row["Review Focus"] == focus]


def classify_trigger(number: int) -> tuple[str, str, str]:
    if 205 <= number <= 210:
        return (
            "cap_ii_tokenomics_ip_gate",
            "hold_at_l2_protected_biz_ip_review_pending_xport_tnpx_tokenomics",
            "review xport2 tokenomics-trigger P1 samples; compare with TNPX-01, CAP-II/Revoke and tokenomics before any public claim",
        )
    if number in {177, 182}:
        return (
            "sensitivity_language_gate",
            "hold_at_l2_source_backed_reference_pending_sensitivity_and_xport_review",
            "review xport2 trigger-only samples and rewrite public language before public canon admission",
        )
    return (
        "standard_trigger_source_gate",
        "hold_at_l2_source_backed_reference_pending_xport_raw_review",
        "review xport2 trigger-only samples; compare with Codex139+ and TNPX-01 before public canon admission",
    )


def build_per_trigger_rows(
    trigger_rows: list[dict[str, str]], sample_rows: list[dict[str, str]]
) -> list[dict[str, object]]:
    trigger_only = handles(sample_rows, "trigger_only")
    tokenomics_trigger = handles(sample_rows, "tokenomics_trigger_shared")

    rows: list[dict[str, object]] = []
    for index, row in enumerate(trigger_rows, start=1):
        number = int(row["trigger_ref"])
        review_lane, decision, next_action = classify_trigger(number)
        sample_handles = list(trigger_only)
        if 205 <= number <= 210:
            sample_handles = tokenomics_trigger + trigger_only

        gates = split_items(row["review_gates"])
        if "xport_002_sample_review" not in gates:
            gates.append("xport_002_sample_review")
        if 205 <= number <= 210 and "tnpx_01_cap_ii_review" not in gates:
            gates.append("tnpx_01_cap_ii_review")

        rows.append(
            {
                "Review ID": f"SOURCE174210-R{index:03d}",
                "Trigger Ref": row["trigger_ref"],
                "Working Name": row["working_name"],
                "Definition Status From Map": row["definition_status"],
                "Canon Level From Map": row["canon_level_now"],
                "Publication Lane From Map": row["publication_lane"],
                "Review Lane Now": review_lane,
                "Strongest Direct Source": "N-CODEX139-174210",
                "XPORT-002 Samples": ";".join(sample_handles),
                "XPORT-002 Role": "deduped hash review corridor; not raw semantic authority",
                "Decision Now": decision,
                "Allowed Claim Now": "Use trigger number, working name and short definition as source-backed L2 reference material.",
                "Blocked Claim Now": (
                    "No canonical TRG assignment, execution semantics, activation protocol, "
                    "medical claim, tokenomics claim or public canon promotion."
                ),
                "Review Gates": ";".join(gates),
                "Next Source Action": next_action,
                "Notes": "171-173 are reserved L0 ID anchors and are intentionally outside this SOURCE-174-210 scope.",
            }
        )
    return rows


def build_xport_correlation_rows(sample_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in sample_rows:
        focus = row["Review Focus"]
        if focus == "trigger_only":
            source_role = "general trigger cross-check corridor for 174-210"
            used_for = "174-210"
            status = "linked_for_review"
        elif focus == "tokenomics_trigger_shared":
            source_role = "CAP-II/tokenomics/IP corridor for 205-210"
            used_for = "205-210"
            status = "linked_for_protected_review"
        else:
            source_role = "tokenomics context only; no direct trigger-source claim"
            used_for = "context_only"
            status = "not_primary_for_trigger_review"

        rows.append(
            {
                "Sample Handle": row["Sample Handle"],
                "Priority": row["Priority"],
                "Review Focus": focus,
                "Representative File Handle": row["Representative File Handle"],
                "SHA-256": row["SHA-256"],
                "Axes": row["Axes"],
                "Publication Lane": row["Publication Lane"],
                "Review Gates": row["Review Gates"],
                "Used For": used_for,
                "SOURCE-174-210 Role": source_role,
                "SOURCE-174-210 Status": status,
            }
        )
    return rows


def build_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "Gate ID": "SOURCE174210-G001",
            "Gate": "Trigger-map seed coverage",
            "Scope": "174-210",
            "Status": "passed",
            "Evidence": "trigger-map-001.seed.csv contains 37 source-backed rows from N-CODEX139-174210",
            "Required Before": "Use names and short definitions as L2 reference entries",
        },
        {
            "Gate ID": "SOURCE174210-G002",
            "Gate": "XPORT-002 trigger-only sample review",
            "Scope": "174-210",
            "Status": "started_not_completed",
            "Evidence": "xport2-sample-010;xport2-sample-011;xport2-sample-012 linked as hash corridors",
            "Required Before": "Any public trigger canon or TRG assignment",
        },
        {
            "Gate ID": "SOURCE174210-G003",
            "Gate": "XPORT-002 tokenomics-trigger shared review",
            "Scope": "205-210",
            "Status": "pending",
            "Evidence": "xport2-sample-001 through xport2-sample-006 linked for protected CAP-II review",
            "Required Before": "Any CAP-II, Revoke, business, tokenomics or license claim",
        },
        {
            "Gate ID": "SOURCE174210-G004",
            "Gate": "TNPX-01 comparison",
            "Scope": "174-210",
            "Status": "pending",
            "Evidence": "TNPX-01 is referenced by TRIGGER-MAP-001 but not reviewed in this source pass",
            "Required Before": "Patent/IP-facing wording or public reference expansion",
        },
        {
            "Gate ID": "SOURCE174210-G005",
            "Gate": "Sensitivity language review",
            "Scope": "177;182;208",
            "Status": "pending",
            "Evidence": "TRIGGER-MAP-001 marks sensitivity review on these trigger rows",
            "Required Before": "Public-facing formulations for sensitive trigger labels",
        },
        {
            "Gate ID": "SOURCE174210-G006",
            "Gate": "Canonical TRG assignment",
            "Scope": "174-210",
            "Status": "blocked",
            "Evidence": "No reviewed L3/L4 contract, no activation protocol, no public canon decision",
            "Required Before": "Any TRG-* number or execution rule",
        },
        {
            "Gate ID": "SOURCE174210-G007",
            "Gate": "External mutation / publication",
            "Scope": "all",
            "Status": "blocked_by_directive",
            "Evidence": "Silvi directive: no push, no PR; DIRTY-SPLIT-001 remains separate",
            "Required Before": "Notion write, push, PR or publication",
        },
    ]


def build_summary(
    per_trigger_rows: list[dict[str, object]],
    sample_rows: list[dict[str, str]],
    gate_rows: list[dict[str, object]],
) -> dict[str, object]:
    review_lane_counts = Counter(str(row["Review Lane Now"]) for row in per_trigger_rows)
    sample_focus_counts = Counter(row["Review Focus"] for row in sample_rows)
    gate_status_counts = Counter(str(row["Status"]) for row in gate_rows)
    return {
        "batch": BATCH,
        "status": "started_local_review_scaffold",
        "created_at": CREATED_AT,
        "inputs": {
            "trigger_map_seed": "trigger-map-001.seed.csv",
            "xport_002_samples": "chatgpt-xport-002.review-samples.csv",
            "xport_002_summary": "chatgpt-xport-002.review-summary.json",
        },
        "scope": {
            "trigger_start": 174,
            "trigger_end": 210,
            "per_trigger_rows": len(per_trigger_rows),
            "reserved_slots_out_of_scope": ["171", "172", "173"],
        },
        "review_lane_counts": dict(sorted(review_lane_counts.items())),
        "xport_002": {
            "sample_count": len(sample_rows),
            "sample_focus_counts": dict(sorted(sample_focus_counts.items())),
            "trigger_only_samples": handles(sample_rows, "trigger_only"),
            "tokenomics_trigger_shared_samples": handles(sample_rows, "tokenomics_trigger_shared"),
        },
        "gate_status_counts": dict(sorted(gate_status_counts.items())),
        "boundaries": {
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
            "notion_write_performed": False,
            "git_push_performed": False,
            "pr_opened": False,
            "commit_created": False,
        },
        "next_source_action": (
            "review XPORT-002 sample corridors against raw local exports, then compare with "
            "TNPX-01 and CAP-II/tokenomics gates before any public trigger canon expansion"
        ),
    }


def build_batch_markdown(
    summary: dict[str, object],
    per_trigger_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
) -> str:
    lane_counts = summary["review_lane_counts"]
    gate_counts = summary["gate_status_counts"]
    return f"""# {BATCH} - Per-trigger source review corridor

Status: started local review scaffold
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

`SOURCE-174-210` starts the per-trigger source review after `TRIGGER-MAP-001`.
It does not replace the Notion master, does not publish raw ChatGPT export
content, and does not assign canonical `TRG-*` IDs.

The pass links the 37 source-backed `174-210` rows from
`trigger-map-001.seed.csv` to the deduped `CHATGPT-XPORT-002` review corridor.
XPORT-002 is used as a hashed review target, not as direct semantic authority.

## Scope

| Item | Value |
| --- | --- |
| Trigger range | `174-210` |
| Per-trigger rows | `{summary["scope"]["per_trigger_rows"]}` |
| Trigger-only XPORT samples | `{len(summary["xport_002"]["trigger_only_samples"])}` |
| Tokenomics-trigger XPORT samples | `{len(summary["xport_002"]["tokenomics_trigger_shared_samples"])}` |
| Reserved slots | `171-173` remain reserved L0 ID anchors and are outside this pass |

## Review Lanes

| Lane | Count |
| --- | ---: |
| `standard_trigger_source_gate` | `{lane_counts.get("standard_trigger_source_gate", 0)}` |
| `sensitivity_language_gate` | `{lane_counts.get("sensitivity_language_gate", 0)}` |
| `cap_ii_tokenomics_ip_gate` | `{lane_counts.get("cap_ii_tokenomics_ip_gate", 0)}` |

## Gate State

| Status | Count |
| --- | ---: |
| `passed` | `{gate_counts.get("passed", 0)}` |
| `started_not_completed` | `{gate_counts.get("started_not_completed", 0)}` |
| `pending` | `{gate_counts.get("pending", 0)}` |
| `blocked` | `{gate_counts.get("blocked", 0)}` |
| `blocked_by_directive` | `{gate_counts.get("blocked_by_directive", 0)}` |

## Current Decision

All 37 triggers stay at `L2-SOURCE-BACKED-REFERENCE`. Names and short
definitions may be used as source-backed reference material. Public canon,
activation protocols, execution semantics, medical claims, tokenomics claims
and canonical `TRG-*` assignment remain blocked.

`205-210` are stricter than the rest of the range because TRIGGER-MAP-001 links
them to CAP-II/Revoke, tokenomics, business and IP review. They are therefore
held behind XPORT-002 P1 tokenomics-trigger samples plus TNPX-01 comparison.

## Artifacts

| File | Role |
| --- | --- |
| `source-174-210.per-trigger-review.csv` | Per-trigger review rows for `174-210`. |
| `source-174-210.xport-002-correlation.csv` | XPORT-002 sample handles and roles for this pass. |
| `source-174-210.review-gates.csv` | Gates before public canon, TRG assignment, tokenomics/IP wording or mutation. |
| `source-174-210.review-summary.json` | Machine-readable summary and boundary flags. |
| `causal-log.source-174-210-2026-05-23.json` | Causal log for the started review corridor. |

## Boundary

- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No Notion write.
- No commit, push or PR in this pass.
- `DIRTY-SPLIT-001` remains separate; unrelated dirty files are not touched.
"""


def build_causal_log() -> dict[str, object]:
    return {
        "log_id": "CAP-LOG-2026-05-23-SOURCE-174-210",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "trigger-map-001.seed.csv",
            "chatgpt-xport-002.review-samples.csv",
            "chatgpt-xport-002.review-summary.json",
            "N-CODEX139-174210",
            "L-XPORT-002",
        ],
        "observation": (
            "TRIGGER-MAP-001 contains 37 source-backed rows for 174-210; "
            "XPORT-002 contains hashed tokenomics/trigger review samples."
        ),
        "trigger_band": "201-300",
        "trigger_ids": ["174-210", "205-210", "171-173", "/fff"],
        "probabilistic_hypothesis": (
            "The next stable move is a per-trigger review corridor, not immediate "
            "public canon admission."
        ),
        "probability_note": (
            "High confidence for names and short definitions from N-CODEX139-174210; "
            "lower confidence for public wording, tokenomics/IP relation and execution semantics."
        ),
        "deterministic_boundary": (
            "No raw export content, no external mutation, no commit, no push, no PR, "
            "and no canonical TRG assignment."
        ),
        "selected_action": (
            "Create SOURCE-174-210 local review scaffold linking trigger-map rows to XPORT-002 samples."
        ),
        "feedback_target": "trigger_map",
        "backpropagation_result": (
            "174-210 now has a per-trigger review queue against XPORT-002; "
            "205-210 are held behind tokenomics/CAP-II/IP gates; 171-173 remain reserved L0 anchors."
        ),
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> None:
    seed_rows = read_csv(OUT / "trigger-map-001.seed.csv")
    sample_rows = read_csv(OUT / "chatgpt-xport-002.review-samples.csv")

    trigger_rows = [
        row for row in seed_rows if (number := trigger_number(row)) is not None and 174 <= number <= 210
    ]
    trigger_rows = sorted(trigger_rows, key=lambda row: int(row["trigger_ref"]))
    if len(trigger_rows) != 37:
        raise RuntimeError(f"Expected 37 trigger rows for 174-210, found {len(trigger_rows)}")

    per_trigger_rows = build_per_trigger_rows(trigger_rows, sample_rows)
    xport_rows = build_xport_correlation_rows(sample_rows)
    gate_rows = build_gate_rows()
    summary = build_summary(per_trigger_rows, sample_rows, gate_rows)

    write_csv(
        OUT / "source-174-210.per-trigger-review.csv",
        [
            "Review ID",
            "Trigger Ref",
            "Working Name",
            "Definition Status From Map",
            "Canon Level From Map",
            "Publication Lane From Map",
            "Review Lane Now",
            "Strongest Direct Source",
            "XPORT-002 Samples",
            "XPORT-002 Role",
            "Decision Now",
            "Allowed Claim Now",
            "Blocked Claim Now",
            "Review Gates",
            "Next Source Action",
            "Notes",
        ],
        per_trigger_rows,
    )
    write_csv(
        OUT / "source-174-210.xport-002-correlation.csv",
        [
            "Sample Handle",
            "Priority",
            "Review Focus",
            "Representative File Handle",
            "SHA-256",
            "Axes",
            "Publication Lane",
            "Review Gates",
            "Used For",
            "SOURCE-174-210 Role",
            "SOURCE-174-210 Status",
        ],
        xport_rows,
    )
    write_csv(
        OUT / "source-174-210.review-gates.csv",
        ["Gate ID", "Gate", "Scope", "Status", "Evidence", "Required Before"],
        gate_rows,
    )
    write_json(OUT / "source-174-210.review-summary.json", summary)
    write_json(OUT / "causal-log.source-174-210-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-source-174-210.md", build_batch_markdown(summary, per_trigger_rows, gate_rows))


if __name__ == "__main__":
    main()
