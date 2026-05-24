#!/usr/bin/env python3
"""Build TRIGGER-DEF-001-SCAFFOLD.

This scaffold prepares the public trigger rulebook without finalizing public
canon. It consumes already reviewed Control Tower summaries and emits public-
safe terms, admission levels, publication lanes and gates. It does not read raw
exports, does not publish raw excerpts and does not assign TRG contracts.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
BATCH = "TRIGGER-DEF-001-SCAFFOLD"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T19:07:42+02:00"


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


def build_term_rows() -> list[dict[str, object]]:
    return [
        {
            "Term": "Trigger",
            "Draft Definition": "A named cognitive, operational or system steering unit that can be referenced, reviewed and governed.",
            "Source Basis": "Trigger Truth complement; TRIGGER-MAP-001; SOURCE-174-210",
            "Public Boundary": "A Trigger is not automatically an executable command, medical claim or public canon object.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Trigger-ID",
            "Draft Definition": "The visible numeric or symbolic identifier used to address a trigger family or slot.",
            "Source Basis": "Trigger Truth complement key rule",
            "Public Boundary": "Trigger-ID alone is not a unique trigger entry.",
            "Scaffold Status": "canonical_rule_needed",
        },
        {
            "Term": "Unique Trigger Entry Key",
            "Draft Definition": "Trigger-ID plus layer/instance plus mode/promille plus context.",
            "Source Basis": "trigger-complement-2026-03-30.md; trigger-map-001.source-index.csv",
            "Public Boundary": "Do not collapse multiple instances into one flat number row.",
            "Scaffold Status": "must_be_public_rule",
        },
        {
            "Term": "Trigger Instance",
            "Draft Definition": "A concrete occurrence of a trigger within a layer, mode, person, context or implementation surface.",
            "Source Basis": "Trigger Truth model",
            "Public Boundary": "Instance detail can be protected if it reveals private identity, account or security context.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Trigger Cluster",
            "Draft Definition": "A semantic grouping of triggers sharing a functional, thematic or control purpose.",
            "Source Basis": "Atlas v1.1 trigger clusters; TRIGGER-MAP-001",
            "Public Boundary": "Cluster membership is routing evidence, not proof of L3/L4 canon.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Trigger Band",
            "Draft Definition": "A numeric or symbolic range used to group source-review and publication work.",
            "Source Basis": "SOURCE-174-210; TNPX-CAPII-TOKENOMICS-GATE-001",
            "Public Boundary": "Band-level rules must not invent per-trigger semantics.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Trigger Layer",
            "Draft Definition": "The source, control, execution or publication layer where a trigger is observed or used.",
            "Source Basis": "Trigger Truth model; CAP control tower",
            "Public Boundary": "Layer movement requires gates; L2 reference does not imply L3 execution.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Experienced",
            "Draft Definition": "A trigger was observed in lived, operational or session context but is not necessarily defined.",
            "Source Basis": "Workspace correlation doctrine",
            "Public Boundary": "Experience-derived material may be public after professional framing; third-party/private specifics remain protected.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Defined",
            "Draft Definition": "A trigger has a source-backed name and definition candidate.",
            "Source Basis": "TRIGGER-MAP-001; SOURCE-174-210",
            "Public Boundary": "Defined does not equal stable public canon.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Emergent",
            "Draft Definition": "A trigger pattern exists as correlation or candidate relation but lacks enough source-review depth.",
            "Source Basis": "XPORT-002 sample corridor; workspace correlation",
            "Public Boundary": "Emergent rows stay out of public canon.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Active",
            "Draft Definition": "A trigger is used in bounded command or routing practice.",
            "Source Basis": "/fff command surface; CAP control tower",
            "Public Boundary": "Active command surfaces need mutation and incident gates.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Stable",
            "Draft Definition": "A trigger has enough source, gate and publication review to be treated as durable within its level.",
            "Source Basis": "CAP canon admission logic",
            "Public Boundary": "Stable level must be named: L1, L2, L3 or L4.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Public",
            "Draft Definition": "Material that may be published after source, framing and redaction gates pass.",
            "Source Basis": "WORKSPACE-CORR-001; Track B promotion queue",
            "Public Boundary": "Public must preserve correlation without exposing third parties, accounts, raw identities, security or protected IP.",
            "Scaffold Status": "must_be_public_rule",
        },
        {
            "Term": "Internal",
            "Draft Definition": "Material usable inside the workspace or repo trace but not released as public canon.",
            "Source Basis": "CAP control tower; Notion SoR policy",
            "Public Boundary": "Internal can be summarized by handle but not fully exported by default.",
            "Scaffold Status": "draft_required",
        },
        {
            "Term": "Metarotik",
            "Draft Definition": "A recognized later trigger/phenomenology cluster that must be preserved as relation but not expanded in this scaffold.",
            "Source Basis": "Workspace correlation; trigger complement seed",
            "Public Boundary": "Deferred until after trigger/tokenomics basis is stable.",
            "Scaffold Status": "deferred_cluster",
        },
        {
            "Term": "Protected",
            "Draft Definition": "Material whose relation can be preserved but whose detail is blocked by IP, legal, business, security, account, third-party or sensitivity gates.",
            "Source Basis": "TNPX-CAPII-TOKENOMICS-GATE-001; SENS lanes",
            "Public Boundary": "Protected means handle-level relation only unless explicit review and Silvan publication GO clears more.",
            "Scaffold Status": "must_be_public_rule",
        },
        {
            "Term": "Silvan-Specific Material",
            "Draft Definition": "Source material anchored in Silvan's authorship, lived system work or workspace history.",
            "Source Basis": "WORKSPACE-CORR-001",
            "Public Boundary": "Not private by default; public after professional framing, with third-party/account/raw-identity/security/IP exceptions.",
            "Scaffold Status": "must_be_public_rule",
        },
    ]


def build_admission_rows() -> list[dict[str, object]]:
    return [
        {
            "Canon Level": "L0-ID-ANCHOR",
            "Meaning": "Reserved or named slot with no source-definition claim.",
            "Minimum Evidence": "Explicit reservation or source index.",
            "Allowed Use": "Keep number or symbolic slot available.",
            "Blocked Use": "Definition, canon claim, activation or TRG assignment.",
            "Example From Current Sprint": "171;172;173",
        },
        {
            "Canon Level": "L1-NAME-CLUSTER",
            "Meaning": "Name or cluster-level routing marker.",
            "Minimum Evidence": "Name, cluster or visual/source relation.",
            "Allowed Use": "Route review and preserve relation.",
            "Blocked Use": "Definition authority, implementation contract or public canon.",
            "Example From Current Sprint": "legacy MMD/CAP candidates",
        },
        {
            "Canon Level": "L2-SOURCE-BACKED-REFERENCE",
            "Meaning": "Source-backed reference with name and/or definition candidate.",
            "Minimum Evidence": "Reviewed source handle and boundary gates.",
            "Allowed Use": "Use as source-backed reference material.",
            "Blocked Use": "TRG assignment, activation semantics, public canon promotion.",
            "Example From Current Sprint": "174-210",
        },
        {
            "Canon Level": "L3-CANON-CANDIDATE",
            "Meaning": "Draft public or internal canon candidate with explicit gates and wording.",
            "Minimum Evidence": "L2 source plus private confirmation, sensitivity review and protected/public split.",
            "Allowed Use": "Draft candidate wording for review.",
            "Blocked Use": "Final public canon or executable contract.",
            "Example From Current Sprint": "future 176/182/202 after human confirmation",
        },
        {
            "Canon Level": "L4-PUBLIC-CANON",
            "Meaning": "Public stable rule or module contract.",
            "Minimum Evidence": "Approved source, publication, redaction, legal/IP and implementation gates.",
            "Allowed Use": "Public rulebook or canonical module reference.",
            "Blocked Use": "Anything beyond the approved scope.",
            "Example From Current Sprint": "not reached",
        },
    ]


def build_publication_rows() -> list[dict[str, object]]:
    return [
        {
            "Lane": "public_after_trigger_review",
            "Scope": "Trigger material that can become public after source and canon gates.",
            "Allowed Now": "Handle relation and L2 reference wording.",
            "Blocked Now": "Public canon until TRIGGER-DEF and promotion gates clear.",
            "Current Sprint Anchor": "176;202 candidates",
        },
        {
            "Lane": "internal_sensitivity_review",
            "Scope": "Material needing wording or sensitivity review before public use.",
            "Allowed Now": "Internal queue and redacted relation.",
            "Blocked Now": "Public wording until sensitivity gate clears.",
            "Current Sprint Anchor": "182",
        },
        {
            "Lane": "protected_biz_ip_review",
            "Scope": "Trigger rows entangled with IP, CAP-II, Revoke, license, tokenomics or business review.",
            "Allowed Now": "Handle-level protected L2 reference.",
            "Blocked Now": "Patent, contract, tokenomics, financial or protected technical claims.",
            "Current Sprint Anchor": "205-210",
        },
        {
            "Lane": "private_context_input",
            "Scope": "Private raw or excerpt context used only for classification and routing.",
            "Allowed Now": "Count-only evidence and sample handles.",
            "Blocked Now": "Raw excerpt, title, local path, conversation ID or direct source claim.",
            "Current Sprint Anchor": "XPORT-002 excerpt gate",
        },
        {
            "Lane": "metarotik_deferred",
            "Scope": "Metarotik/phenomenology relations preserved for later lane.",
            "Allowed Now": "Relation marker only.",
            "Blocked Now": "Public explanation or canon expansion in TRIGGER-DEF-001 scaffold.",
            "Current Sprint Anchor": "future METAROTIK-PHEN-001",
        },
        {
            "Lane": "external_mutation_blocked",
            "Scope": "Notion, GitHub push/PR, token/contract and publication actions.",
            "Allowed Now": "Local artifacts and review packages only.",
            "Blocked Now": "External mutation without explicit Silvan GO per lane.",
            "Current Sprint Anchor": "/fff local-only",
        },
    ]


def build_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "Gate ID": "TRIGGER-DEF-G001",
            "Gate": "Unique key rule",
            "Status": "must_include",
            "Evidence": "Trigger-ID + layer/instance + mode/promille + context.",
            "Blocks Until Cleared": "Any public rulebook that treats Trigger-ID alone as unique.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G002",
            "Gate": "Track A protected/public split",
            "Status": "available_as_scaffold_input",
            "Evidence": "TNPX-CAPII-TOKENOMICS-GATE-001 committed locally.",
            "Blocks Until Cleared": "Final public protected/IP/tokenomics wording.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G003",
            "Gate": "Track B promotion queue",
            "Status": "available_as_scaffold_input",
            "Evidence": "SOURCE-174-210-PROMOTION-QUEUE-001 committed locally.",
            "Blocks Until Cleared": "L3 wording for 176, 182 and 202.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G004",
            "Gate": "Raw source boundary",
            "Status": "blocked",
            "Evidence": "XPORT and source corridors emit count-only/hash/source-handle outputs.",
            "Blocks Until Cleared": "Any raw excerpt, raw title, local path or conversation ID publication.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G005",
            "Gate": "Public canon and TRG assignment",
            "Status": "blocked",
            "Evidence": "Current lanes explicitly stop at scaffold/private queue.",
            "Blocks Until Cleared": "TRIGGER-174-210-CANON-DRAFT-001 and explicit Silvan GO.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G006",
            "Gate": "Silvan framing",
            "Status": "must_include",
            "Evidence": "WORKSPACE-CORR-001 relation-preservation rule.",
            "Blocks Until Cleared": "Any rulebook that hides Silvan-specific authorship instead of professionally framing it.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G007",
            "Gate": "Third-party/account/security/IP redaction",
            "Status": "must_include",
            "Evidence": "WORKSPACE-CORR-001 and Track A protected gates.",
            "Blocks Until Cleared": "Any public text exposing third parties, accounts, raw identities, security details or protected IP.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G008",
            "Gate": "Metarotik deferral",
            "Status": "deferred",
            "Evidence": "Metarotik is a recognized cluster but intentionally later than tokenomics/trigger scaffolding.",
            "Blocks Until Cleared": "Any public metarotik explanation inside this scaffold.",
        },
        {
            "Gate ID": "TRIGGER-DEF-G009",
            "Gate": "External mutation",
            "Status": "blocked",
            "Evidence": "/fff local-only execution.",
            "Blocks Until Cleared": "Notion write, GitHub push, PR or publication.",
        },
    ]


def build_dependency_rows(track_a: dict[str, object], track_b: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            "Dependency": "Trigger Truth complement",
            "Current Status": "source_handle_available",
            "Provides": "Unique key rule and trigger-truth model.",
            "Needed For TRIGGER-DEF": "Core definition section.",
            "Blocks": "Rulebook if key rule is absent.",
        },
        {
            "Dependency": "WORKSPACE-CORR-001",
            "Current Status": "committed",
            "Provides": "Correlation-preservation and Silvan framing rule.",
            "Needed For TRIGGER-DEF": "Publication/redaction doctrine.",
            "Blocks": "Rulebook if correlation is destroyed by over-redaction.",
        },
        {
            "Dependency": "TRIGGER-MAP-001",
            "Current Status": "committed",
            "Provides": "Source-backed trigger map and 171-173 reserved slots.",
            "Needed For TRIGGER-DEF": "Admission examples and L0/L2 boundaries.",
            "Blocks": "Any claim that all 174-210 rows are L3/L4.",
        },
        {
            "Dependency": "TNPX-CAPII-TOKENOMICS-GATE-001",
            "Current Status": str(track_a.get("status", "unknown")),
            "Provides": "Protected/public split for 205-210.",
            "Needed For TRIGGER-DEF": "Protected/IP/business/tokenomics clause.",
            "Blocks": "Public wording for 205-210 and protected claims.",
        },
        {
            "Dependency": "SOURCE-174-210-PROMOTION-QUEUE-001",
            "Current Status": str(track_b.get("status", "unknown")),
            "Provides": "Private promotion queue for 176/182/202 and holds for 196/201.",
            "Needed For TRIGGER-DEF": "Promotion/admission flow and negative-control rule.",
            "Blocks": "L3 candidate wording and public canon draft.",
        },
        {
            "Dependency": "XPORT-002 excerpt gate",
            "Current Status": "count_only_completed",
            "Provides": "Private routing evidence, no raw publication.",
            "Needed For TRIGGER-DEF": "Evidence-source boundary clause.",
            "Blocks": "Direct XPORT public source claims.",
        },
        {
            "Dependency": "Future METAROTIK-PHEN-001",
            "Current Status": "deferred",
            "Provides": "Later phenomenology cluster treatment.",
            "Needed For TRIGGER-DEF": "Only relation marker now.",
            "Blocks": "Metarotik public explanation in this scaffold.",
        },
    ]


def build_summary(
    term_rows: list[dict[str, object]],
    admission_rows: list[dict[str, object]],
    publication_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    dependency_rows: list[dict[str, object]],
    track_a: dict[str, object],
    track_b: dict[str, object],
) -> dict[str, object]:
    return {
        "batch": BATCH,
        "status": "scaffold_only_not_public_canon",
        "created_at": CREATED_AT,
        "inputs": {
            "trigger_truth_seed": "trigger-complement-2026-03-30.md",
            "trigger_map": "trigger-map-001.seed.csv",
            "track_a_gate": "tnpx-capii-tokenomics-gate-001.review-summary.json",
            "track_b_queue": "source-174-210.promotion-summary.json",
            "workspace_corr": "workspace-corr-001.relation-preservation-rules.md",
        },
        "term_rows": len(term_rows),
        "admission_rows": len(admission_rows),
        "publication_rows": len(publication_rows),
        "gate_rows": len(gate_rows),
        "dependency_rows": len(dependency_rows),
        "gate_status_counts": dict(Counter(row["Status"] for row in gate_rows)),
        "track_a_status": track_a.get("status"),
        "track_b_status": track_b.get("status"),
        "candidate_trigger_refs": track_b.get("candidate_trigger_refs", []),
        "protected_trigger_refs": track_a.get("protected_trigger_refs", []),
        "decision": (
            "TRIGGER-DEF-001 may be scaffolded from Track A and Track B, but final public "
            "rulebook, public canon and TRG assignment remain blocked."
        ),
        "next_lane": "TRIGGER-DEF-001-DRAFT after human review of scaffold scope, then TRIGGER-174-210-CANON-DRAFT-001.",
        "boundaries": {
            "raw_excerpts_printed": False,
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
            "public_canon_promoted": False,
            "trg_assigned": False,
            "patent_claims_printed": False,
            "tokenomics_claims_printed": False,
            "metarotik_expanded": False,
            "notion_write_performed": False,
            "git_push_performed": False,
            "pr_opened": False,
            "commit_created": False,
        },
    }


def build_batch_markdown(summary: dict[str, object]) -> str:
    gate_counts = "\n".join(
        f"| `{status}` | `{count}` |"
        for status, count in summary["gate_status_counts"].items()
    )
    candidates = ";".join(str(ref) for ref in summary["candidate_trigger_refs"])
    protected = ";".join(str(ref) for ref in summary["protected_trigger_refs"])
    return f"""# {BATCH} - Trigger Definition Canon scaffold

Status: scaffold only, not public canon
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This batch prepares `TRIGGER-DEF-001` as a public-capable trigger rulebook
scaffold. It does not finalize the rulebook, does not promote public canon and
does not assign canonical `TRG-*` contracts.

The scaffold carries forward:

- Track A protected/public split for `{protected}`.
- Track B private promotion queue for `{candidates}`.
- The Trigger Truth key rule: `Trigger-ID + Layer/Instanz + Modus/Promille + Kontext`.
- The workspace rule that Silvan-related material is not private by default, but must be professionally framed.

## Result

| Item | Value |
| --- | ---: |
| Term rows | `{summary["term_rows"]}` |
| Admission rows | `{summary["admission_rows"]}` |
| Publication rows | `{summary["publication_rows"]}` |
| Gate rows | `{summary["gate_rows"]}` |
| Dependency rows | `{summary["dependency_rows"]}` |

## Gate State

| Status | Count |
| --- | ---: |
{gate_counts}

## Current Decision

`TRIGGER-DEF-001` can now be drafted from stable scaffold components, but it is
not itself public canon yet. Final public text remains blocked until human
review confirms scope, wording, protected/public split and promotion boundaries.

## Artifacts

| File | Role |
| --- | --- |
| `trigger-def-001.term-scaffold.csv` | Draft term definitions for the trigger rulebook. |
| `trigger-def-001.admission-levels.csv` | L0-L4 canon admission scaffold. |
| `trigger-def-001.publication-lanes.csv` | Public/internal/protected/metarotik/deferred lane scaffold. |
| `trigger-def-001.rule-gates.csv` | Gates before public rulebook, public canon or TRG assignment. |
| `trigger-def-001.dependency-map.csv` | Dependencies from Track A, Track B and source-truth work. |
| `trigger-def-001.review-summary.json` | Machine-readable scaffold summary and boundary flags. |
| `causal-log.trigger-def-001-scaffold-2026-05-23.json` | Causal trace for this scaffold batch. |

## Boundary

- No raw excerpts printed.
- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No public canon promoted.
- No TRG assignment.
- No patent or tokenomics claims printed.
- No Metarotik expansion.
- No Notion write.
- No commit, push or PR in this pass.
"""


def build_causal_log() -> dict[str, object]:
    return {
        "log_id": "CAP-LOG-2026-05-23-TRIGGER-DEF-001-SCAFFOLD",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "trigger-complement-2026-03-30.md",
            "trigger-map-001.seed.csv",
            "tnpx-capii-tokenomics-gate-001.review-summary.json",
            "source-174-210.promotion-summary.json",
            "workspace-corr-001.relation-preservation-rules.md",
        ],
        "observation": "Track A and Track B now provide enough structure to scaffold TRIGGER-DEF-001 without final public canon.",
        "trigger_band": "all trigger definition lanes",
        "trigger_ids": ["171-173", "174-210", "176", "182", "202", "205-210", "/fff"],
        "probabilistic_hypothesis": "A scaffold can preserve the public/protected split before drafting final rulebook wording.",
        "probability_note": "High confidence for scaffold structure; final wording remains blocked by human review and canon gates.",
        "deterministic_boundary": "No public canon, no TRG assignment, no raw excerpts, no external mutation, no push and no PR.",
        "selected_action": "Create TRIGGER-DEF-001-SCAFFOLD from Track A, Track B and Trigger Truth source rules.",
        "feedback_target": "trigger_definition_public_rulebook",
        "backpropagation_result": "TRIGGER-DEF-001 has a local scaffold with terms, L0-L4 admission, publication lanes, gates and dependencies.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> None:
    track_a = read_json("tnpx-capii-tokenomics-gate-001.review-summary.json")
    track_b = read_json("source-174-210.promotion-summary.json")
    term_rows = build_term_rows()
    admission_rows = build_admission_rows()
    publication_rows = build_publication_rows()
    gate_rows = build_gate_rows()
    dependency_rows = build_dependency_rows(track_a, track_b)
    summary = build_summary(
        term_rows,
        admission_rows,
        publication_rows,
        gate_rows,
        dependency_rows,
        track_a,
        track_b,
    )

    write_csv(
        OUT / "trigger-def-001.term-scaffold.csv",
        ["Term", "Draft Definition", "Source Basis", "Public Boundary", "Scaffold Status"],
        term_rows,
    )
    write_csv(
        OUT / "trigger-def-001.admission-levels.csv",
        ["Canon Level", "Meaning", "Minimum Evidence", "Allowed Use", "Blocked Use", "Example From Current Sprint"],
        admission_rows,
    )
    write_csv(
        OUT / "trigger-def-001.publication-lanes.csv",
        ["Lane", "Scope", "Allowed Now", "Blocked Now", "Current Sprint Anchor"],
        publication_rows,
    )
    write_csv(
        OUT / "trigger-def-001.rule-gates.csv",
        ["Gate ID", "Gate", "Status", "Evidence", "Blocks Until Cleared"],
        gate_rows,
    )
    write_csv(
        OUT / "trigger-def-001.dependency-map.csv",
        ["Dependency", "Current Status", "Provides", "Needed For TRIGGER-DEF", "Blocks"],
        dependency_rows,
    )
    write_json(OUT / "trigger-def-001.review-summary.json", summary)
    write_json(OUT / "causal-log.trigger-def-001-scaffold-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-trigger-def-001-scaffold.md", build_batch_markdown(summary))

    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
