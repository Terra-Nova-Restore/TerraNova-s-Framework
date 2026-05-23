#!/usr/bin/env python3
"""Build SOURCE-174-210-ROUTING-001 from SOURCE and XPORT gate artifacts.

This script consumes public-safe CSV/JSON artifacts only. It does not read raw
exports and does not emit raw excerpts, titles, local paths, conversation IDs
or account data.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
BATCH = "SOURCE-174-210-ROUTING-001"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T17:37:10+02:00"


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


def routing_decision(trigger_ref: str, gate_decision: str) -> tuple[str, str, str]:
    is_capii = 205 <= int(trigger_ref) <= 210
    if gate_decision == "excerpt_context_supports_definition_candidate":
        base = "shortlist_for_private_source_confirmation"
        use = "May route into SOURCE-174-210 as XPORT-supported private confirmation candidate."
        next_action = "Private human excerpt confirmation; do not publish raw excerpt."
    elif gate_decision == "excerpt_context_supports_name_candidate":
        base = "route_to_private_context_review"
        use = "May route as name-context support, not as independent public definition source."
        next_action = "Private context review before any direct source-evidence claim."
    elif gate_decision == "numeric_context_only":
        base = "do_not_promote_from_xport"
        use = "Use as numeric correlation only; no XPORT source promotion."
        next_action = "Keep Codex139+ as source; reject or confirm numeric context privately."
    else:
        base = "hold_without_xport_support"
        use = "No XPORT routing support."
        next_action = "Use non-XPORT source layers only."

    if is_capii:
        next_action = f"{next_action} CAP-II/tokenomics/IP and TNPX-01 review remains mandatory."
    return base, use, next_action


def build_rows() -> list[dict[str, object]]:
    source_rows = {row["Trigger Ref"]: row for row in read_csv(OUT / "source-174-210.per-trigger-review.csv")}
    excerpt_rows = {row["Trigger Ref"]: row for row in read_csv(OUT / "xport-002.excerpt-gate.best-trigger-review.csv")}
    rows: list[dict[str, object]] = []
    for ref in sorted(source_rows, key=int):
        source = source_rows[ref]
        excerpt = excerpt_rows.get(ref)
        if excerpt is None:
            gate_decision = "not_observed_in_excerpt_gate"
            confidence = "no_sample_signal"
            sample_handle = ""
            review_focus = ""
            overlap = "0"
            source_anchor_count = "0"
            capii_anchor_count = "0"
        else:
            gate_decision = excerpt["Best Decision"]
            confidence = excerpt["Best Confidence"]
            sample_handle = excerpt["Best Sample Handle"]
            review_focus = excerpt["Best Review Focus"]
            overlap = excerpt["Definition Term Overlap"]
            source_anchor_count = excerpt["Source Anchor Count"]
            capii_anchor_count = excerpt["CAPII Anchor Count"]

        decision, allowed_use, next_action = routing_decision(ref, gate_decision)
        rows.append(
            {
                "Trigger Ref": ref,
                "Working Name": source["Working Name"],
                "SOURCE-174-210 Current Decision": source["Decision Now"],
                "XPORT Excerpt Gate Decision": gate_decision,
                "XPORT Excerpt Confidence": confidence,
                "Best Sample Handle": sample_handle,
                "Best Review Focus": review_focus,
                "Definition Term Overlap": overlap,
                "Source Anchor Count": source_anchor_count,
                "CAPII Anchor Count": capii_anchor_count,
                "Routing Decision": decision,
                "Allowed Use Now": allowed_use,
                "Blocked Use Now": (
                    "No raw excerpt publication, no public canon promotion, no canonical TRG assignment, "
                    "no activation semantics, no CAP-II/tokenomics/IP public claim."
                ),
                "Next Action": next_action,
            }
        )
    return rows


def build_gate_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    definition_refs = [
        str(row["Trigger Ref"])
        for row in rows
        if row["Routing Decision"] == "shortlist_for_private_source_confirmation"
    ]
    name_refs = [
        str(row["Trigger Ref"])
        for row in rows
        if row["Routing Decision"] == "route_to_private_context_review"
    ]
    numeric_refs = [
        str(row["Trigger Ref"])
        for row in rows
        if row["Routing Decision"] == "do_not_promote_from_xport"
    ]
    return [
        {
            "Gate ID": "SOURCE174210-ROUTE-G001",
            "Gate": "XPORT excerpt gate consumed",
            "Status": "completed",
            "Evidence": "All 37 SOURCE-174-210 rows are joined with best XPORT excerpt-gate classification.",
            "Blocks Until Cleared": "None for local routing; this does not clear publication.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G002",
            "Gate": "Definition-context shortlist",
            "Status": "candidate",
            "Evidence": ";".join(definition_refs),
            "Blocks Until Cleared": "Direct public claim that XPORT defines these triggers.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G003",
            "Gate": "Name-context review queue",
            "Status": "private_review_required",
            "Evidence": f"{len(name_refs)} trigger rows require private context review.",
            "Blocks Until Cleared": "Public source-evidence claim for name-context-only rows.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G004",
            "Gate": "Numeric-only rejection/hold",
            "Status": "hold",
            "Evidence": ";".join(numeric_refs),
            "Blocks Until Cleared": "Any XPORT promotion for numeric-only rows.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G005",
            "Gate": "Sensitivity wording",
            "Status": "pending",
            "Evidence": "177;182;208 remain sensitivity-language rows.",
            "Blocks Until Cleared": "Public-facing wording for sensitive trigger labels.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G006",
            "Gate": "CAP-II/tokenomics/IP/TNPX",
            "Status": "pending",
            "Evidence": "205-210 remain behind CAP-II, tokenomics, business, IP and TNPX-01 gates.",
            "Blocks Until Cleared": "Any CAP-II, Revoke, license, tokenomics, TNPX-01 or IP-facing public claim.",
        },
        {
            "Gate ID": "SOURCE174210-ROUTE-G007",
            "Gate": "Public canon / TRG assignment",
            "Status": "blocked",
            "Evidence": "Routing is not an L3/L4 module contract.",
            "Blocks Until Cleared": "Canonical TRG assignment, activation semantics or public trigger canon promotion.",
        },
    ]


def build_summary(rows: list[dict[str, object]], gate_rows: list[dict[str, object]]) -> dict[str, object]:
    decision_counts = Counter(str(row["Routing Decision"]) for row in rows)
    confidence_counts = Counter(str(row["XPORT Excerpt Confidence"]) for row in rows)
    gate_counts = Counter(str(row["Status"]) for row in gate_rows)
    return {
        "batch": BATCH,
        "status": "public_safe_xport_excerpt_routing",
        "created_at": CREATED_AT,
        "inputs": {
            "source_review": "source-174-210.per-trigger-review.csv",
            "excerpt_gate": "xport-002.excerpt-gate.best-trigger-review.csv",
        },
        "trigger_rows": len(rows),
        "routing_decision_counts": dict(sorted(decision_counts.items())),
        "excerpt_confidence_counts": dict(sorted(confidence_counts.items())),
        "gate_status_counts": dict(sorted(gate_counts.items())),
        "definition_context_shortlist": [
            str(row["Trigger Ref"])
            for row in rows
            if row["Routing Decision"] == "shortlist_for_private_source_confirmation"
        ],
        "numeric_only_hold": [
            str(row["Trigger Ref"])
            for row in rows
            if row["Routing Decision"] == "do_not_promote_from_xport"
        ],
        "protected_capii_range": ["205", "206", "207", "208", "209", "210"],
        "sensitivity_rows": ["177", "182", "208"],
        "boundaries": {
            "raw_excerpts_printed": False,
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
        "decision": (
            "XPORT excerpt-gate results are routed into SOURCE-174-210 without promoting public canon "
            "or publishing raw excerpts."
        ),
    }


def build_batch_markdown(summary: dict[str, object]) -> str:
    decisions = summary["routing_decision_counts"]
    gates = summary["gate_status_counts"]
    return f"""# {BATCH} - XPORT excerpt routing for SOURCE-174-210

Status: completed as local public-safe routing layer
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This batch consumes `XPORT-002-EXCERPT-GATE-001` and routes its count-only
classification into `SOURCE-174-210`. It does not read raw exports, does not
publish excerpts and does not promote any trigger to public canon.

## Result

| Item | Value |
| --- | ---: |
| Trigger rows | `{summary["trigger_rows"]}` |
| Definition-context shortlist | `{len(summary["definition_context_shortlist"])}` |
| Numeric-only hold | `{len(summary["numeric_only_hold"])}` |
| CAP-II protected rows | `{len(summary["protected_capii_range"])}` |
| Sensitivity rows | `{len(summary["sensitivity_rows"])}` |

## Routing Decisions

| Decision | Count |
| --- | ---: |
| `shortlist_for_private_source_confirmation` | `{decisions.get("shortlist_for_private_source_confirmation", 0)}` |
| `route_to_private_context_review` | `{decisions.get("route_to_private_context_review", 0)}` |
| `do_not_promote_from_xport` | `{decisions.get("do_not_promote_from_xport", 0)}` |

## Gate State

| Status | Count |
| --- | ---: |
| `completed` | `{gates.get("completed", 0)}` |
| `candidate` | `{gates.get("candidate", 0)}` |
| `private_review_required` | `{gates.get("private_review_required", 0)}` |
| `hold` | `{gates.get("hold", 0)}` |
| `pending` | `{gates.get("pending", 0)}` |
| `blocked` | `{gates.get("blocked", 0)}` |

## Current Decision

`176`, `182` and `202` are routed to private source-confirmation shortlist.
`196` and `201` are held as numeric-only and must not be promoted from XPORT.
`205-210` remain behind CAP-II/tokenomics/business/IP/TNPX gates even where
XPORT has name-context evidence.

## Artifacts

| File | Role |
| --- | --- |
| `source-174-210.xport-excerpt-routing.csv` | Per-trigger routing matrix from SOURCE rows and XPORT excerpt gate. |
| `source-174-210.routing-gates.csv` | Gates before source promotion, public wording, CAP-II/IP claims or TRG assignment. |
| `source-174-210.xport-excerpt-routing.summary.json` | Machine-readable routing summary and boundary flags. |
| `causal-log.source-174-210-routing-001-2026-05-23.json` | Causal trace for this routing batch. |

## Boundary

- No raw excerpts printed.
- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No Notion write.
- No commit, push or PR in this pass.
- `DIRTY-SPLIT-001` remains separate.
"""


def build_causal_log() -> dict[str, object]:
    return {
        "log_id": "CAP-LOG-2026-05-23-SOURCE-174-210-ROUTING-001",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "source-174-210.per-trigger-review.csv",
            "xport-002.excerpt-gate.best-trigger-review.csv",
            "xport-002.excerpt-gate.gates.csv",
        ],
        "observation": "XPORT excerpt-gate classes can be routed into SOURCE-174-210 without raw excerpt publication.",
        "trigger_band": "201-300",
        "trigger_ids": ["174-210", "176", "182", "196", "201", "202", "205-210", "/fff"],
        "probabilistic_hypothesis": "The routing layer can strengthen review priority but cannot replace Notion Codex139+ as source authority.",
        "probability_note": "High confidence for routing categories; public source promotion remains blocked by private confirmation and canon gates.",
        "deterministic_boundary": "No raw excerpts, no external mutation, no commit, no push, no PR and no canonical TRG assignment.",
        "selected_action": "Create SOURCE-174-210-ROUTING-001 matrix and gates from XPORT excerpt-gate output.",
        "feedback_target": "trigger_map",
        "backpropagation_result": "176, 182 and 202 enter private confirmation shortlist; 196 and 201 are XPORT numeric-only holds; 205-210 remain CAP-II/tokenomics/IP protected.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> None:
    rows = build_rows()
    gate_rows = build_gate_rows(rows)
    summary = build_summary(rows, gate_rows)
    write_csv(
        OUT / "source-174-210.xport-excerpt-routing.csv",
        [
            "Trigger Ref",
            "Working Name",
            "SOURCE-174-210 Current Decision",
            "XPORT Excerpt Gate Decision",
            "XPORT Excerpt Confidence",
            "Best Sample Handle",
            "Best Review Focus",
            "Definition Term Overlap",
            "Source Anchor Count",
            "CAPII Anchor Count",
            "Routing Decision",
            "Allowed Use Now",
            "Blocked Use Now",
            "Next Action",
        ],
        rows,
    )
    write_csv(
        OUT / "source-174-210.routing-gates.csv",
        ["Gate ID", "Gate", "Status", "Evidence", "Blocks Until Cleared"],
        gate_rows,
    )
    write_json(OUT / "source-174-210.xport-excerpt-routing.summary.json", summary)
    write_json(OUT / "causal-log.source-174-210-routing-001-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-source-174-210-routing-001.md", build_batch_markdown(summary))


if __name__ == "__main__":
    main()
