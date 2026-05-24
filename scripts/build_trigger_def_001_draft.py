#!/usr/bin/env python3
"""Build TRIGGER-DEF-001-DRAFT.

This converts the scaffold into a public-capable draft rulebook. The output is
not final public canon and does not assign TRG contracts. It preserves the
protected/public split and keeps raw-source, IP, tokenomics and Metarotik
boundaries explicit.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
BATCH = "TRIGGER-DEF-001-DRAFT"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T19:29:44+02:00"


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


def read_json(path: str) -> dict[str, object]:
    return json.loads((OUT / path).read_text(encoding="utf-8"))


def bullet_lines(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)


def table_from_rows(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row.get(column, "").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep] + body)


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "Decision ID": "TRIGGER-DEF-D001",
            "Decision": "Draft is public-capable but not final public canon.",
            "Status": "draft_only",
            "Reason": "Track A and Track B are stable enough for rulebook wording, not for final canon release.",
        },
        {
            "Decision ID": "TRIGGER-DEF-D002",
            "Decision": "Trigger-ID alone is never the unique trigger entry key.",
            "Status": "must_include",
            "Reason": "Trigger Truth requires Trigger-ID plus layer/instance plus mode/promille plus context.",
        },
        {
            "Decision ID": "TRIGGER-DEF-D003",
            "Decision": "Silvan-specific source material is professionally framed, not hidden by default.",
            "Status": "must_include",
            "Reason": "Workspace correlation rules preserve authorship and relation while redacting sensitive details.",
        },
        {
            "Decision ID": "TRIGGER-DEF-D004",
            "Decision": "Protected lanes preserve relation but suppress protected details.",
            "Status": "must_include",
            "Reason": "TNPX/IP, CAP-II, tokenomics, accounts, security and third-party content cannot be exposed by rulebook wording.",
        },
        {
            "Decision ID": "TRIGGER-DEF-D005",
            "Decision": "Metarotik remains deferred.",
            "Status": "deferred",
            "Reason": "The cluster is recognized but comes after trigger/tokenomics foundations.",
        },
    ]


def build_open_issue_rows() -> list[dict[str, object]]:
    return [
        {
            "Open Item": "Human wording review",
            "Blocks": "TRIGGER-DEF-001 finalization",
            "Current Owner": "Silvan",
            "Required Action": "Approve or edit public wording before final canon draft.",
        },
        {
            "Open Item": "Private excerpt confirmation for 176/182/202",
            "Blocks": "L3 candidate wording and later canon draft.",
            "Current Owner": "Silvan/Codex local review",
            "Required Action": "Confirm raw context privately without publishing excerpts.",
        },
        {
            "Open Item": "Sensitivity wording for 182",
            "Blocks": "Public wording for Trigger 182.",
            "Current Owner": "Silvan",
            "Required Action": "Approve neutral public wording or keep internal.",
        },
        {
            "Open Item": "Protected claim review for 205-210",
            "Blocks": "Any TNPX/IP, CAP-II, Revoke, license or tokenomics public claim.",
            "Current Owner": "Silvan/human IP and business review",
            "Required Action": "Review protected material before any detail leaves handle level.",
        },
        {
            "Open Item": "TRIGGER-174-210-CANON-DRAFT-001",
            "Blocks": "Final public trigger subset.",
            "Current Owner": "Future lane",
            "Required Action": "Only start after TRIGGER-DEF-001-DRAFT is reviewed.",
        },
    ]


def build_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G001",
            "Gate": "Draft status",
            "Status": "completed_draft",
            "Evidence": "trigger-def-001.draft.md created with explicit draft boundaries.",
            "Blocks Until Cleared": "Final public rulebook claim.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G002",
            "Gate": "Unique-key rule",
            "Status": "included",
            "Evidence": "Draft states Trigger-ID alone is not unique.",
            "Blocks Until Cleared": "Any flat ID-only registry model.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G003",
            "Gate": "Protected/public split",
            "Status": "included",
            "Evidence": "Draft carries Track A protected lanes and Track B queue boundaries.",
            "Blocks Until Cleared": "Protected claim release and final canon wording.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G004",
            "Gate": "Silvan framing",
            "Status": "included",
            "Evidence": "Draft frames Silvan-specific material as authored source material, not default-private material.",
            "Blocks Until Cleared": "Any over-redacted version that destroys correlation.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G005",
            "Gate": "Raw source boundary",
            "Status": "blocked",
            "Evidence": "Draft forbids raw excerpts, titles, local paths and conversation IDs.",
            "Blocks Until Cleared": "Any publication of raw source material.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G006",
            "Gate": "Public canon / TRG assignment",
            "Status": "blocked",
            "Evidence": "Draft does not assign TRG or promote final canon.",
            "Blocks Until Cleared": "TRIGGER-174-210-CANON-DRAFT-001 plus explicit Silvan GO.",
        },
        {
            "Gate ID": "TRIGGER-DEF-DRAFT-G007",
            "Gate": "External mutation",
            "Status": "blocked",
            "Evidence": "/fff local-only execution.",
            "Blocks Until Cleared": "Notion write, GitHub push, PR or publication.",
        },
    ]


def build_draft_markdown(
    terms: list[dict[str, str]],
    admissions: list[dict[str, str]],
    lanes: list[dict[str, str]],
    dependencies: list[dict[str, str]],
) -> str:
    term_table = table_from_rows(
        terms,
        ["Term", "Draft Definition", "Public Boundary"],
    )
    admission_table = table_from_rows(
        admissions,
        ["Canon Level", "Meaning", "Minimum Evidence", "Allowed Use", "Blocked Use"],
    )
    lane_table = table_from_rows(
        lanes,
        ["Lane", "Scope", "Allowed Now", "Blocked Now"],
    )
    dependency_table = table_from_rows(
        dependencies,
        ["Dependency", "Current Status", "Provides", "Blocks"],
    )

    non_goals = bullet_lines(
        [
            "This draft is not final public canon.",
            "This draft does not assign canonical TRG identifiers.",
            "This draft does not publish raw ChatGPT exports, raw excerpts, page titles, local paths, conversation IDs or account data.",
            "This draft does not make medical, financial, legal, patent, tokenomics or contract claims.",
            "This draft does not expand Metarotik beyond a deferred relation marker.",
            "This draft does not authorize Notion writes, GitHub pushes, PRs, token actions or publication.",
        ]
    )
    exceptions = bullet_lines(
        [
            "Third-party identities and raw third-party context.",
            "Accounts, addresses, credentials, credential material, security details and operational secrets.",
            "Raw identities, intimate real names and unreviewed private biographical details.",
            "Patent claims, filing strategy, protected technical detail and unreviewed IP specifics.",
            "Tokenomics promises, financial wording, sales wording and contract mechanics.",
            "Raw transcripts, raw excerpts, local file paths, page URLs and conversation identifiers.",
        ]
    )
    current_examples = bullet_lines(
        [
            "`171-173` are L0 reserved ID anchors, not source gaps.",
            "`176`, `182` and `202` are private promotion-queue candidates, not public canon.",
            "`182` has a sensitivity-language gate before public wording.",
            "`196` and `201` are numeric-only negative controls and must not be promoted from XPORT evidence.",
            "`205-210` remain protected L2 references behind TNPX/IP, CAP-II/license/Revoke and FERR/tokenomics gates.",
        ]
    )

    return f"""# TRIGGER-DEF-001 - Trigger Definition Canon (Draft)

Status: draft, not final public canon
Created: {TODAY}
Activation: `/fff`
Source mode: repo-local scaffold from reviewed Control Tower artifacts
External mutation: none

## 1. Purpose

`TRIGGER-DEF-001` defines the public-facing rule language for TerraNova trigger
work. It exists to prevent three failure modes:

1. Reducing a trigger to a flat number.
2. Publishing protected or private material as if it were public canon.
3. Promoting source-backed references into executable or canonical modules too early.

This draft is public-capable in structure, but it is not a publication release.
It still requires human review before public use.

## 2. Non-Goals

{non_goals}

## 3. Core Rule

`Trigger-ID` is not the unique trigger entry key.

The unique trigger entry key is:

```text
Trigger-ID + Layer/Instanz + Modus/Promille + Kontext
```

This means a single visible ID can have more than one legitimate entry if the
layer, instance, mode, promille or context differs. Public documentation must
not collapse those entries into one flat number row.

## 4. Definitions

{term_table}

## 5. Canon Admission Levels

{admission_table}

## 6. Publication Lanes

{lane_table}

## 7. Silvan Framing Rule

Silvan-specific material is not private by default.

If the material is authored by Silvan, grounded in Silvan's system work, or
necessary to understand TerraNova/FerrAI structure, the default action is to
frame it professionally and preserve its correlation. The goal is not to hide
the author, erase lived development history or destroy the relation graph.

Public handling changes only where a protected category applies.

## 8. Protected Exceptions

{exceptions}

Protected does not mean deleted. Protected means the relation may be preserved
at handle level while protected details stay blocked until explicit review and
Silvan publication approval.

## 9. Current Sprint Examples

{current_examples}

## 10. Source Precedence

{dependency_table}

Notion remains the living workspace source of record where applicable. GitHub
Control Tower artifacts provide the versioned review trace, boundary logic and
local reproducibility layer.

## 11. Draft Gates

Before this draft can become a final public rulebook, the following must happen:

- Human review of the wording and public/protected split.
- Private excerpt confirmation for any promotion candidate that relies on XPORT context.
- Sensitivity wording review for `182`.
- Protected claim review for `205-210`.
- Explicit Silvan GO for publication or downstream canon draft.

## 12. Current Decision

This draft is ready for review as `TRIGGER-DEF-001-DRAFT`.

It is not final public canon. It does not clear `TRIGGER-174-210-CANON-DRAFT-001`.
"""


def build_batch_markdown(summary: dict[str, object]) -> str:
    gate_counts = "\n".join(
        f"| `{status}` | `{count}` |"
        for status, count in summary["gate_status_counts"].items()
    )
    return f"""# TRIGGER-DEF-001-DRAFT - public-capable trigger rulebook draft

Status: local draft, not final public canon
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This batch converts `TRIGGER-DEF-001-SCAFFOLD` into a readable rulebook draft.
It keeps all final-public, TRG, raw-source, protected-IP, tokenomics and
Metarotik gates closed.

## Result

| Item | Value |
| --- | ---: |
| Draft document rows/sections | `{summary["draft_sections"]}` |
| Decision rows | `{summary["decision_rows"]}` |
| Open review items | `{summary["open_review_items"]}` |
| Gate rows | `{summary["gate_rows"]}` |

## Gate State

| Status | Count |
| --- | ---: |
{gate_counts}

## Current Decision

`TRIGGER-DEF-001-DRAFT` is ready for human review. It is not public canon, does
not assign TRG IDs and does not authorize publication or external mutation.

## Artifacts

| File | Role |
| --- | --- |
| `trigger-def-001.draft.md` | Human-readable trigger definition rulebook draft. |
| `trigger-def-001.draft-decisions.csv` | Key decisions carried into the draft. |
| `trigger-def-001.draft-open-items.csv` | Human-review items before finalization. |
| `trigger-def-001.draft-gates.csv` | Gates before final public rulebook or canon work. |
| `trigger-def-001.draft-summary.json` | Machine-readable draft summary and boundary flags. |
| `causal-log.trigger-def-001-draft-2026-05-23.json` | Causal trace for this draft batch. |

## Boundary

- No raw excerpts printed.
- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No patent or tokenomics claims printed.
- No Metarotik expansion.
- No public canon promoted.
- No TRG assignment.
- No Notion write.
- No commit, push or PR in this pass.
"""


def build_summary(
    decision_rows: list[dict[str, object]],
    open_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "batch": BATCH,
        "status": "draft_ready_for_human_review_not_public_canon",
        "created_at": CREATED_AT,
        "inputs": {
            "scaffold_summary": "trigger-def-001.review-summary.json",
            "term_scaffold": "trigger-def-001.term-scaffold.csv",
            "admission_levels": "trigger-def-001.admission-levels.csv",
            "publication_lanes": "trigger-def-001.publication-lanes.csv",
            "dependency_map": "trigger-def-001.dependency-map.csv",
            "rule_gates": "trigger-def-001.rule-gates.csv",
        },
        "draft_sections": 12,
        "decision_rows": len(decision_rows),
        "open_review_items": len(open_rows),
        "gate_rows": len(gate_rows),
        "gate_status_counts": dict(Counter(row["Status"] for row in gate_rows)),
        "decision": (
            "TRIGGER-DEF-001-DRAFT is ready for human review, but remains blocked from final "
            "public canon, TRG assignment and publication."
        ),
        "next_lane": "TRIGGER-DEF-001-DRAFT-REVIEW or TRIGGER-DEF-001-DRAFT-COMMIT, then TRIGGER-174-210-CANON-DRAFT-001 only after explicit GO.",
        "boundaries": {
            "raw_excerpts_printed": False,
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
            "patent_claims_printed": False,
            "tokenomics_claims_printed": False,
            "metarotik_expanded": False,
            "public_canon_promoted": False,
            "trg_assigned": False,
            "notion_write_performed": False,
            "git_push_performed": False,
            "pr_opened": False,
            "commit_created": False,
        },
    }


def build_causal_log() -> dict[str, object]:
    return {
        "log_id": "CAP-LOG-2026-05-23-TRIGGER-DEF-001-DRAFT",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "trigger-def-001.term-scaffold.csv",
            "trigger-def-001.admission-levels.csv",
            "trigger-def-001.publication-lanes.csv",
            "trigger-def-001.dependency-map.csv",
            "trigger-def-001.rule-gates.csv",
        ],
        "observation": "The trigger definition scaffold can be rendered as a human-readable rulebook draft without changing canon status.",
        "trigger_band": "trigger-definition-canon",
        "trigger_ids": ["171-173", "176", "182", "196", "201", "202", "205-210", "/fff"],
        "probabilistic_hypothesis": "A public-capable draft improves review quality while preserving final-public gates.",
        "probability_note": "High confidence for structure; final wording and publication remain human decision points.",
        "deterministic_boundary": "No public canon, no TRG assignment, no raw source publication, no external mutation, no push and no PR.",
        "selected_action": "Create TRIGGER-DEF-001-DRAFT from committed scaffold artifacts.",
        "feedback_target": "trigger_definition_public_rulebook",
        "backpropagation_result": "The rulebook now has a readable draft with key rule, definitions, L0-L4 levels, lanes, exceptions and review gates.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> None:
    terms = read_csv(OUT / "trigger-def-001.term-scaffold.csv")
    admissions = read_csv(OUT / "trigger-def-001.admission-levels.csv")
    lanes = read_csv(OUT / "trigger-def-001.publication-lanes.csv")
    dependencies = read_csv(OUT / "trigger-def-001.dependency-map.csv")
    decision_rows = build_decision_rows()
    open_rows = build_open_issue_rows()
    gate_rows = build_gate_rows()
    summary = build_summary(decision_rows, open_rows, gate_rows)

    write_text(OUT / "trigger-def-001.draft.md", build_draft_markdown(terms, admissions, lanes, dependencies))
    write_csv(
        OUT / "trigger-def-001.draft-decisions.csv",
        ["Decision ID", "Decision", "Status", "Reason"],
        decision_rows,
    )
    write_csv(
        OUT / "trigger-def-001.draft-open-items.csv",
        ["Open Item", "Blocks", "Current Owner", "Required Action"],
        open_rows,
    )
    write_csv(
        OUT / "trigger-def-001.draft-gates.csv",
        ["Gate ID", "Gate", "Status", "Evidence", "Blocks Until Cleared"],
        gate_rows,
    )
    write_json(OUT / "trigger-def-001.draft-summary.json", summary)
    write_json(OUT / "causal-log.trigger-def-001-draft-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-trigger-def-001-draft.md", build_batch_markdown(summary))

    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
