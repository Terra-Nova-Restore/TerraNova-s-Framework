#!/usr/bin/env python3
"""Build MMD-007 CAP module source review and canon admission gates."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"

MODULE_DRAFTS = "mmd-005.cap-module-drafts.csv"
MODULE_EVIDENCE = "mmd-005.module-evidence.csv"
MODULE_RELATIONS = "mmd-005.module-relation-map.csv"

REVIEWED_SOURCES = {
    "docs/triggers/gap_ledger.md": {
        "tier": "S1",
        "status": "reviewed_gap_ledger",
        "use": "range status and canon boundary",
        "boundary": "Does not provide full per-trigger semantics.",
    },
    "atlas/sources/trigger-complement-2026-03-30.md": {
        "tier": "S1",
        "status": "user_provided_trigger_complement",
        "use": "trigger truth model, clusters and known single triggers",
        "boundary": "Summary-level complement, not a full trigger definition.",
    },
    "atlas/atlas.manifest.v1.1.json": {
        "tier": "S2",
        "status": "generated_from_reviewed_sources",
        "use": "object summaries, cluster membership and architecture layer",
        "boundary": "Atlas context only; not complete historical trigger definition.",
    },
    "docs/atlas/control-tower/mmd-005.module-evidence.csv": {
        "tier": "S2",
        "status": "generated_evidence_matrix",
        "use": "visual candidates, guard relations and Atlas evidence rows",
        "boundary": "Evidence only; visual rows never equal canon by themselves.",
    },
    "docs/atlas/control-tower/mmd-004.candidate-review-and-canon-gate.md": {
        "tier": "S1",
        "status": "canon_gate",
        "use": "canon admission boundary and held references",
        "boundary": "Gate output, not trigger semantics.",
    },
}

ADMISSION_LEVELS = [
    {
        "Canon Level": "L0-ID-ANCHOR",
        "Meaning": "Trigger number exists as a named internal anchor.",
        "Minimum Evidence": "Reviewed gap/source ledger or trigger complement plus no sensitivity block.",
        "Allowed Claim": "Use the numeric trigger reference internally.",
        "Blocked Claim": "Any operational semantics beyond the source.",
    },
    {
        "Canon Level": "L1-NAME-CLUSTER",
        "Meaning": "Working name, cluster and architecture layer are source-supported.",
        "Minimum Evidence": "Trigger complement plus Atlas v1.1 object or cluster relation.",
        "Allowed Claim": "Name, cluster and layer can be used as canon candidate metadata.",
        "Blocked Claim": "Full module behavior or execution permission.",
    },
    {
        "Canon Level": "L2-ROUTING-MARKER",
        "Meaning": "The module can guide routing inside CAP.",
        "Minimum Evidence": "L1 evidence plus reviewed guard or Mermaid relation.",
        "Allowed Claim": "Use as internal routing marker with boundary text.",
        "Blocked Claim": "Treat route as automation or external mutation permission.",
    },
    {
        "Canon Level": "L3-MODULE-SEMANTICS",
        "Meaning": "Full CAP module semantics are source-supported.",
        "Minimum Evidence": "Direct primary source definition plus secondary corroboration plus boundary review.",
        "Allowed Claim": "Move from draft module to canon module candidate.",
        "Blocked Claim": "Public canon or execution rule without test and sensitivity review.",
    },
    {
        "Canon Level": "L4-EXECUTION-OR-PUBLIC",
        "Meaning": "The module can drive execution rules or public-facing canon.",
        "Minimum Evidence": "L3 plus tests, SENS review, Equilibrium check and publication boundary.",
        "Allowed Claim": "Execution/public claim after explicit GO.",
        "Blocked Claim": "Silent external mutation, restricted expansion or raw private source exposure.",
    },
]

REF_REVIEW = {
    "516": {
        "source_status": "documented subset through 516-523 plus Atlas v1.1 named anchor",
        "max_level": "L2-ROUTING-MARKER",
        "decision": "canon_candidate_l2_internal",
        "allowed": "ID, name Inspiration, Creative Flow cluster and internal inspiration-routing marker.",
        "blocked": "AutoFlow sibling semantics, execution behavior and public trigger definition.",
        "reason": "Name and cluster are supported; full module semantics are still a draft inference.",
        "next_action": "Find or curate direct source text for Inspiration behavior before L3.",
        "risk": "medium",
    },
    "520": {
        "source_status": "documented subset through 516-523 plus Atlas v1.1 and SESSION_ROOT visual guard",
        "max_level": "L2-ROUTING-MARKER",
        "decision": "canon_candidate_l2_internal",
        "allowed": "ID, name SessionStart, Core System cluster, session initialization routing and session_opened guard as internal marker.",
        "blocked": "External mutation permission, autonomous session control and full historical trigger definition.",
        "reason": "This is the strongest operational candidate, but the guard remains relation evidence only.",
        "next_action": "Curate primary SessionStart definition and add a bounded test case before L3.",
        "risk": "low",
    },
    "521": {
        "source_status": "documented subset plus protection-layer overlap",
        "max_level": "L1-NAME-CLUSTER",
        "decision": "canon_candidate_l1_protected",
        "allowed": "ID, name Preflight, Core System and Protection Layer membership.",
        "blocked": "Schattenarchiv-depth behavior, protection execution and preflight automation.",
        "reason": "Protection-layer overlap raises boundary risk; route semantics need a more explicit source.",
        "next_action": "Review protection/preflight source separately and keep 777 boundary closed.",
        "risk": "high",
    },
    "540": {
        "source_status": "documented point; gap ledger says routing marker only",
        "max_level": "L2-ROUTING-MARKER",
        "decision": "canon_candidate_l2_internal",
        "allowed": "ID, name Observable Momentum, Meta-Reflexion cluster and progress-visibility routing marker.",
        "blocked": "Proof of correctness, metric finality and public scientific claim.",
        "reason": "Gap ledger permits routing marker use only; Prism relation supports feedback path, not full semantics.",
        "next_action": "Tie to explicit Prism/CAP text before L3.",
        "risk": "medium",
    },
    "544": {
        "source_status": "documented point; gap ledger says routing marker only",
        "max_level": "L2-ROUTING-MARKER",
        "decision": "canon_candidate_l2_internal",
        "allowed": "ID, name Synchronization Node, Meta-Reflexion cluster and state-delta routing marker.",
        "blocked": "Full workspace sync claim, automatic synchronization and public canon.",
        "reason": "Guard delta_confirmed supports routing; sync requires explicit scope before stronger canon.",
        "next_action": "Add explicit sync-scope source and test before L3.",
        "risk": "medium",
    },
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


def count_by_ref(rows: list[dict[str, str]], ref_field: str = "Visible Reference") -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[row[ref_field]] += 1
    return counts


def evidence_types_for_ref(rows: list[dict[str, str]], ref: str) -> str:
    types = sorted({row["Evidence Type"] for row in rows if row["Visible Reference"] == ref})
    return " | ".join(types)


def relation_sources_for_ref(rows: list[dict[str, str]], ref: str) -> str:
    sources = sorted({row["Relation Source"] for row in rows if row["Visible Reference"] == ref})
    return " | ".join(sources)


def build_source_index() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path, data in REVIEWED_SOURCES.items():
        rows.append(
            {
                "Source ID": f"MMD7-S{len(rows) + 1:03d}",
                "Source Path": path,
                "Tier": data["tier"],
                "Source Status": data["status"],
                "Use In MMD-007": data["use"],
                "Boundary": data["boundary"],
            }
        )
    return rows


def build_review_rows(
    module_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    relation_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    evidence_counts = count_by_ref(evidence_rows)
    relation_counts = count_by_ref(relation_rows)
    rows: list[dict[str, str]] = []
    for module in module_rows:
        ref = module["Visible Reference"]
        review = REF_REVIEW[ref]
        rows.append(
            {
                "Review ID": f"MMD7-R{len(rows) + 1:03d}",
                "Draft Module ID": module["Draft Module ID"],
                "Visible Reference": ref,
                "Working Name": module["Working Name"],
                "Current Registry Status": "Candidate / Needs sync",
                "Source Status": review["source_status"],
                "Evidence Rows": str(evidence_counts.get(ref, 0)),
                "Evidence Types": evidence_types_for_ref(evidence_rows, ref),
                "Relation Rows": str(relation_counts.get(ref, 0)),
                "Relation Sources": relation_sources_for_ref(relation_rows, ref),
                "Max Canon Level Now": review["max_level"],
                "Canon Decision": review["decision"],
                "Allowed Into Canon Now": review["allowed"],
                "Blocked From Canon Now": review["blocked"],
                "Reason": review["reason"],
                "Risk": review["risk"],
                "Next Source Action": review["next_action"],
            }
        )
    return rows


def build_decision_queue(review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in review_rows:
        rows.append(
            {
                "Queue ID": f"MMD7-Q{len(rows) + 1:03d}",
                "Draft Module ID": row["Draft Module ID"],
                "Visible Reference": row["Visible Reference"],
                "Proposed Registry Move": "Keep Candidate; add Canon Level marker locally",
                "Notion Mutation": "No",
                "Required Before Notion Update": "MMD-007 Notion package or explicit GO after review",
                "Required Before L3": row["Next Source Action"],
                "Stop Rule": row["Blocked From Canon Now"],
            }
        )
    return rows


def build_markdown(review_rows: list[dict[str, str]]) -> str:
    lines = [
        "# MMD-007 - CAP Module Source Review",
        "",
        "Status: completed",
        "",
        "Date: 2026-05-17",
        "",
        "## Core Answer",
        "",
        "Canon admission is not decided by how plausible a module feels. It is decided by source tier, source agreement, boundary clarity and reversibility.",
        "",
        "MMD-007 uses a five-level canon ladder:",
        "",
        "| Level | Meaning | Admission Rule |",
        "| --- | --- | --- |",
    ]
    for level in ADMISSION_LEVELS:
        lines.append(f"| `{level['Canon Level']}` | {level['Meaning']} | {level['Minimum Evidence']} |")

    lines.extend(
        [
            "",
            "## Result",
            "",
            "| Ref | Working Name | Max Canon Level Now | Decision | Risk |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for row in review_rows:
        lines.append(
            f"| `{row['Visible Reference']}` | {row['Working Name']} | `{row['Max Canon Level Now']}` | "
            f"{row['Canon Decision']} | {row['Risk']} |"
        )

    lines.extend(
        [
            "",
            "## What Can Enter Canon Now",
            "",
            "Allowed now:",
            "",
            "- numeric trigger anchors for `516`, `520`, `521`, `540`, `544`",
            "- working names where supported by Atlas/gap/source complement",
            "- cluster and architecture-layer metadata",
            "- internal routing-marker use for `516`, `520`, `540`, `544`",
            "- protected name/cluster metadata for `521`",
            "",
            "Blocked now:",
            "",
            "- full historical trigger definitions",
            "- canonical `TRG-*` assignment",
            "- execution permission",
            "- public-facing trigger canon",
            "- AutoFlow `517`, Schattenarchiv `777`, and integrity suite `988-992` expansion",
            "",
            "## Per-Module Notes",
            "",
        ]
    )
    for row in review_rows:
        lines.extend(
            [
                f"### {row['Visible Reference']} - {row['Working Name']}",
                "",
                f"- Source status: {row['Source Status']}",
                f"- Allowed into canon now: {row['Allowed Into Canon Now']}",
                f"- Blocked from canon now: {row['Blocked From Canon Now']}",
                f"- Next source action: {row['Next Source Action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Practical Canon Test",
            "",
            "A module can move upward only when all five questions pass:",
            "",
            "1. Which exact source says this?",
            "2. Is the source curated, reviewed or raw?",
            "3. Does a second source agree, or does the source explicitly define the boundary?",
            "4. What exactly is allowed, and what remains blocked?",
            "5. Can the claim be reversed or downgraded without breaking the registry?",
            "",
            "If any answer is unclear, the row stays `Candidate` and `Needs sync`.",
            "",
            "## Repeat Command",
            "",
            "```powershell",
            "python scripts/build_cap_module_source_review.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def build_batch_markdown(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MMD-007 - CAP Module Source Review",
            "",
            "Date: 2026-05-17",
            "",
            "Activation: `MMD-007 - CAP Module Source Review`",
            "",
            "Mode: repo-local source review and canon admission rules",
            "",
            "External mutation: none",
            "",
            "Notion AI credits used: 0",
            "",
            "## Purpose",
            "",
            "MMD-007 decides what parts of the five CAP module drafts may enter canon now and what must remain draft-only.",
            "",
            "## Result",
            "",
            f"- Reviewed modules: {summary['reviewed_modules']}",
            f"- Source index rows: {summary['source_index_rows']}",
            f"- Canon levels: {summary['canon_level_rows']}",
            f"- Decision queue rows: {summary['decision_queue_rows']}",
            "",
            "## Boundary",
            "",
            "No live Notion mutation was performed. MMD-007 keeps all five live rows as Candidate / Needs sync until a later explicit package updates them.",
            "",
        ]
    )


def build_causal_log(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "log_id": "CAP-LOG-2026-05-17-MMD-007",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": "Codex",
        "mode": "STUDIO",
        "activation": "manual",
        "source_trace": [
            "docs/triggers/gap_ledger.md",
            "atlas/sources/trigger-complement-2026-03-30.md",
            "atlas/atlas.manifest.v1.1.json",
            "docs/atlas/control-tower/mmd-005.module-evidence.csv",
            "docs/atlas/control-tower/mmd-006.registry-updates.csv",
        ],
        "observation": "Five CAP module draft rows are live in Notion but still marked Candidate / Needs sync.",
        "trigger_band": "401+",
        "trigger_ids": ["516", "520", "521", "540", "544"],
        "probabilistic_hypothesis": "The draft modules can safely enter canon only at metadata/routing levels until direct primary definitions are curated.",
        "probability_note": "High confidence for L1/L2 internal admission; low confidence for full module semantics without more source review.",
        "deterministic_boundary": "No canonical TRG assignment, no execution permission, no Notion mutation, no expansion of held sensitive ranges.",
        "selected_action": "Created MMD-007 source review, canon ladder, per-module decisions and source-action queue.",
        "feedback_target": "trigger_map",
        "backpropagation_result": "CAP now distinguishes ID/name/cluster canon from routing markers and full trigger semantics.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> int:
    module_rows = read_csv(MODULE_DRAFTS)
    evidence_rows = read_csv(MODULE_EVIDENCE)
    relation_rows = read_csv(MODULE_RELATIONS)

    review_rows = build_review_rows(module_rows, evidence_rows, relation_rows)
    source_index_rows = build_source_index()
    decision_queue_rows = build_decision_queue(review_rows)

    write_csv(
        CONTROL_DIR / "mmd-007.source-index.csv",
        source_index_rows,
        ["Source ID", "Source Path", "Tier", "Source Status", "Use In MMD-007", "Boundary"],
    )
    write_csv(
        CONTROL_DIR / "mmd-007.canon-admission-levels.csv",
        ADMISSION_LEVELS,
        ["Canon Level", "Meaning", "Minimum Evidence", "Allowed Claim", "Blocked Claim"],
    )
    write_csv(
        CONTROL_DIR / "mmd-007.source-review.csv",
        review_rows,
        [
            "Review ID",
            "Draft Module ID",
            "Visible Reference",
            "Working Name",
            "Current Registry Status",
            "Source Status",
            "Evidence Rows",
            "Evidence Types",
            "Relation Rows",
            "Relation Sources",
            "Max Canon Level Now",
            "Canon Decision",
            "Allowed Into Canon Now",
            "Blocked From Canon Now",
            "Reason",
            "Risk",
            "Next Source Action",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-007.canon-decision-queue.csv",
        decision_queue_rows,
        [
            "Queue ID",
            "Draft Module ID",
            "Visible Reference",
            "Proposed Registry Move",
            "Notion Mutation",
            "Required Before Notion Update",
            "Required Before L3",
            "Stop Rule",
        ],
    )

    summary = {
        "review_id": "MMD-007",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "reviewed_modules": len(review_rows),
        "source_index_rows": len(source_index_rows),
        "canon_level_rows": len(ADMISSION_LEVELS),
        "decision_queue_rows": len(decision_queue_rows),
        "current_allowed_levels": {row["Visible Reference"]: row["Max Canon Level Now"] for row in review_rows},
        "boundary": "Source review only; no live Notion mutation and no canonical TRG assignment.",
    }

    (CONTROL_DIR / "mmd-007.review-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (CONTROL_DIR / "mmd-007.cap-module-source-review.md").write_text(
        build_markdown(review_rows),
        encoding="utf-8",
    )
    (CONTROL_DIR / "batch-mmd-007.md").write_text(
        build_batch_markdown(summary),
        encoding="utf-8",
    )
    (CONTROL_DIR / "causal-log.mmd-007-source-review-2026-05-17.json").write_text(
        json.dumps(build_causal_log(summary), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
