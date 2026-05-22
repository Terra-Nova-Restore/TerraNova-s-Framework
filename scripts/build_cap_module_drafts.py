#!/usr/bin/env python3
"""Build MMD-005 CAP module drafts from the MMD-004 canon gate."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"
ATLAS_MANIFEST = REPO_ROOT / "atlas" / "atlas.manifest.v1.1.json"
TRIGGER_COMPLEMENT = REPO_ROOT / "atlas" / "sources" / "trigger-complement-2026-03-30.md"

ELIGIBLE_REFS = ["516", "520", "521", "540", "544"]

MODULE_PROFILE = {
    "516": {
        "working_name": "Inspiration",
        "primary_runtime_role": "creative-flow intake",
        "cap_function": "Route a live inspiration signal into bounded CAP work without turning it into execution by itself.",
        "activation_surface": "Creative Flow / inspiration queue",
        "feedback_target": "trigger_map",
        "source_state": "visible Mermaid evidence plus Atlas v1.1 documented anchor",
        "boundary": "Draft module only; AutoFlow sibling 517 remains a caution lane and is not normalized.",
    },
    "520": {
        "working_name": "SessionStart",
        "primary_runtime_role": "session initialization",
        "cap_function": "Mark the start of a working session and bind it to a visible root state before deeper routing.",
        "activation_surface": "SESSION_ROOT / ferro:state=init",
        "feedback_target": "logbook",
        "source_state": "visible Mermaid evidence plus Atlas v1.1 documented anchor",
        "boundary": "Draft module only; session start does not authorize external mutation.",
    },
    "521": {
        "working_name": "Preflight",
        "primary_runtime_role": "pre-action gate",
        "cap_function": "Check source, mode, boundary and protection state before execution or sync movement.",
        "activation_surface": "preflight_ok guard",
        "feedback_target": "logbook",
        "source_state": "visible Mermaid evidence plus Atlas v1.1 documented anchor",
        "boundary": "Draft module only; protection-layer overlap does not open Schattenarchiv depth.",
    },
    "540": {
        "working_name": "Observable Momentum",
        "primary_runtime_role": "progress visibility",
        "cap_function": "Make movement measurable so CAP can distinguish real progress from narrative drift.",
        "activation_surface": "Meta-Reflexion / validation and momentum",
        "feedback_target": "prism_zenodo",
        "source_state": "visible Mermaid evidence plus Atlas v1.1 documented anchor",
        "boundary": "Draft module only; observable momentum is a control signal, not proof of correctness.",
    },
    "544": {
        "working_name": "Synchronization Node",
        "primary_runtime_role": "state reconciliation",
        "cap_function": "Confirm and route a state delta into sync, decision or feedback handling.",
        "activation_surface": "delta_confirmed guard",
        "feedback_target": "registry",
        "source_state": "visible Mermaid evidence plus Atlas v1.1 documented anchor",
        "boundary": "Draft module only; synchronization requires explicit scope and does not imply full workspace sync.",
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


def ref_list(value: str) -> list[str]:
    return [part for part in (value or "").split(";") if part]


def has_ref(row: dict[str, str], ref: str) -> bool:
    return ref in ref_list(row.get("Trigger References", ""))


def load_atlas() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    data = json.loads(ATLAS_MANIFEST.read_text(encoding="utf-8"))
    objects = {item["id"]: item for item in data.get("objects", [])}
    relations = data.get("relations", [])
    return objects, relations


def atlas_object(objects: dict[str, dict[str, Any]], object_id: str) -> dict[str, Any]:
    return objects.get(object_id, {})


def relation_rows_for_ref(
    ref: str,
    objects: dict[str, dict[str, Any]],
    atlas_relations: list[dict[str, Any]],
    guard_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    trigger_id = f"trigger_{ref}"
    rows: list[dict[str, str]] = []

    for relation in atlas_relations:
        source = relation.get("from", "")
        target = relation.get("to", "")
        if source != trigger_id and target != trigger_id:
            continue
        rows.append(
            {
                "Relation ID": f"MMD5-R{len(rows) + 1:03d}",
                "Visible Reference": ref,
                "Draft Module ID": f"CAP-MOD-DRAFT-{ref}",
                "Relation Source": "atlas.manifest.v1.1.json",
                "From": source,
                "From Title": atlas_object(objects, source).get("title", source),
                "To": target,
                "To Title": atlas_object(objects, target).get("title", target),
                "Relation Type": relation.get("type", ""),
                "Guard Condition": "",
                "Note": relation.get("note", ""),
                "Boundary": "Atlas relation only; not a canonical trigger definition.",
            }
        )

    for row in guard_rows:
        if not has_ref(row, ref):
            continue
        rows.append(
            {
                "Relation ID": f"MMD5-R{len(rows) + 1:03d}",
                "Visible Reference": ref,
                "Draft Module ID": f"CAP-MOD-DRAFT-{ref}",
                "Relation Source": "mmd-004.guard-review.csv",
                "From": row.get("Source Node", ""),
                "From Title": row.get("Source Node", ""),
                "To": row.get("Target Node", ""),
                "To Title": row.get("Target Node", ""),
                "Relation Type": row.get("Lane", ""),
                "Guard Condition": row.get("Guard Condition", ""),
                "Note": row.get("Reason", ""),
                "Boundary": row.get("Boundary", "Guard relation only; not execution permission."),
            }
        )

    return rows


def build_evidence_rows(
    candidate_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    objects: dict[str, dict[str, Any]],
    atlas_relations: list[dict[str, Any]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for ref in ELIGIBLE_REFS:
        draft_id = f"CAP-MOD-DRAFT-{ref}"
        trigger_obj = atlas_object(objects, f"trigger_{ref}")

        for row in candidate_rows:
            if not has_ref(row, ref):
                continue
            rows.append(
                {
                    "Evidence Row ID": f"MMD5-E{len(rows) + 1:03d}",
                    "Draft Module ID": draft_id,
                    "Visible Reference": ref,
                    "Evidence Type": "visual_candidate",
                    "Source File": "mmd-004.candidate-review.csv",
                    "Source Anchor": f"{row.get('Graph ID', '')}::{row.get('Node ID', '')}",
                    "Label Or Guard": row.get("Label", ""),
                    "Relation": row.get("Lane", ""),
                    "Status": row.get("Gate Status", ""),
                    "Boundary": row.get("Boundary", ""),
                }
            )

        for row in guard_rows:
            if not has_ref(row, ref):
                continue
            rows.append(
                {
                    "Evidence Row ID": f"MMD5-E{len(rows) + 1:03d}",
                    "Draft Module ID": draft_id,
                    "Visible Reference": ref,
                    "Evidence Type": "guard_relation",
                    "Source File": "mmd-004.guard-review.csv",
                    "Source Anchor": f"{row.get('Source Node', '')}->{row.get('Target Node', '')}",
                    "Label Or Guard": row.get("Guard Condition", ""),
                    "Relation": row.get("Lane", ""),
                    "Status": row.get("Gate Status", ""),
                    "Boundary": row.get("Boundary", ""),
                }
            )

        rows.append(
            {
                "Evidence Row ID": f"MMD5-E{len(rows) + 1:03d}",
                "Draft Module ID": draft_id,
                "Visible Reference": ref,
                "Evidence Type": "atlas_object",
                "Source File": "atlas.manifest.v1.1.json",
                "Source Anchor": f"trigger_{ref}",
                "Label Or Guard": trigger_obj.get("summary", ""),
                "Relation": ",".join(trigger_obj.get("tags", [])),
                "Status": trigger_obj.get("status", ""),
                "Boundary": "Atlas object context only; not a complete historical trigger definition.",
            }
        )

        for relation in atlas_relations:
            if relation.get("to") != f"trigger_{ref}" and relation.get("from") != f"trigger_{ref}":
                continue
            rows.append(
                {
                    "Evidence Row ID": f"MMD5-E{len(rows) + 1:03d}",
                    "Draft Module ID": draft_id,
                    "Visible Reference": ref,
                    "Evidence Type": "atlas_relation",
                    "Source File": "atlas.manifest.v1.1.json",
                    "Source Anchor": f"{relation.get('from', '')}->{relation.get('to', '')}",
                    "Label Or Guard": relation.get("type", ""),
                    "Relation": relation.get("note", ""),
                    "Status": "context",
                    "Boundary": "Atlas relation context only; not a canonical trigger definition.",
                }
            )

    return rows


def cluster_titles_for_ref(
    ref: str, objects: dict[str, dict[str, Any]], atlas_relations: list[dict[str, Any]]
) -> list[str]:
    trigger_id = f"trigger_{ref}"
    titles: list[str] = []
    for relation in atlas_relations:
        if relation.get("type") == "has_members" and relation.get("to") == trigger_id:
            source = relation.get("from", "")
            titles.append(atlas_object(objects, source).get("title", source))
    return titles


def layer_titles_for_ref(
    ref: str, objects: dict[str, dict[str, Any]], atlas_relations: list[dict[str, Any]]
) -> list[str]:
    trigger_id = f"trigger_{ref}"
    titles: list[str] = []
    for relation in atlas_relations:
        if relation.get("type") == "belongs_to_layer" and relation.get("from") == trigger_id:
            target = relation.get("to", "")
            titles.append(atlas_object(objects, target).get("title", target))
    return titles


def build_hash_material(
    ref: str,
    profile: dict[str, str],
    candidate_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    objects: dict[str, dict[str, Any]],
    atlas_relations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "material_version": "MMD-005:v1",
        "draft_module_id": f"CAP-MOD-DRAFT-{ref}",
        "visible_reference": ref,
        "working_name": profile["working_name"],
        "source_state": profile["source_state"],
        "canon_status": "draft_only_no_canonical_trg_assignment",
        "primary_runtime_role": profile["primary_runtime_role"],
        "cap_function": profile["cap_function"],
        "activation_surface": profile["activation_surface"],
        "feedback_target": profile["feedback_target"],
        "clusters": cluster_titles_for_ref(ref, objects, atlas_relations),
        "architecture_layers": layer_titles_for_ref(ref, objects, atlas_relations),
        "candidate_evidence": [
            {
                "review_id": row.get("Review ID", ""),
                "graph_id": row.get("Graph ID", ""),
                "node_id": row.get("Node ID", ""),
                "label": row.get("Label", ""),
            }
            for row in candidate_rows
            if has_ref(row, ref)
        ],
        "guard_evidence": [
            {
                "review_id": row.get("Review ID", ""),
                "source_node": row.get("Source Node", ""),
                "target_node": row.get("Target Node", ""),
                "guard_condition": row.get("Guard Condition", ""),
                "lane": row.get("Lane", ""),
            }
            for row in guard_rows
            if has_ref(row, ref)
        ],
        "atlas_trigger_summary": atlas_object(objects, f"trigger_{ref}").get("summary", ""),
        "boundary": profile["boundary"],
    }


def stable_hash(material: dict[str, Any]) -> str:
    rendered = json.dumps(material, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def build_modules(
    candidate_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    objects: dict[str, dict[str, Any]],
    atlas_relations: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, Any]]:
    module_rows: list[dict[str, str]] = []
    hash_rows: list[dict[str, str]] = []
    hash_material_by_ref: dict[str, Any] = {}

    for ref in ELIGIBLE_REFS:
        profile = MODULE_PROFILE[ref]
        candidate_count = sum(1 for row in candidate_rows if has_ref(row, ref))
        guard_count = sum(1 for row in guard_rows if has_ref(row, ref))
        clusters = cluster_titles_for_ref(ref, objects, atlas_relations)
        layers = layer_titles_for_ref(ref, objects, atlas_relations)
        material = build_hash_material(ref, profile, candidate_rows, guard_rows, objects, atlas_relations)
        digest = stable_hash(material)
        handle = f"CAP-DRAFT-{ref}-{digest[:12]}"
        hash_material_by_ref[ref] = {
            "hash_handle": handle,
            "sha256": digest,
            "material": material,
        }

        module_rows.append(
            {
                "Draft Module ID": f"CAP-MOD-DRAFT-{ref}",
                "Visible Reference": ref,
                "Working Name": profile["working_name"],
                "Draft Status": "active_draft",
                "Canon Status": "not assigned",
                "Source State": profile["source_state"],
                "Primary Runtime Role": profile["primary_runtime_role"],
                "CAP Function": profile["cap_function"],
                "Trigger Cluster": " | ".join(clusters),
                "Architecture Layer": " | ".join(layers),
                "Activation Surface": profile["activation_surface"],
                "Guard Summary": summarize_guards(ref, guard_rows),
                "Evidence Count": str(candidate_count),
                "Guard Count": str(guard_count),
                "Hash Handle": handle,
                "Boundary": profile["boundary"],
                "Next Action": "source-review before canonical TRG assignment",
            }
        )
        hash_rows.append(
            {
                "Hash Handle": handle,
                "Draft Module ID": f"CAP-MOD-DRAFT-{ref}",
                "Visible Reference": ref,
                "Hash Algorithm": "SHA-256",
                "Hash Material Version": "MMD-005:v1",
                "Draft Hash": digest,
                "Canon Claim": "none",
                "Hash Material File": "mmd-005.hash-material.json",
                "Boundary": "Draft hash fingerprints current material only; it is not a canonical trigger hash.",
            }
        )

    return module_rows, hash_rows, hash_material_by_ref


def summarize_guards(ref: str, guard_rows: list[dict[str, str]]) -> str:
    parts: list[str] = []
    for row in guard_rows:
        if not has_ref(row, ref):
            continue
        condition = row.get("Guard Condition", "") or "structural_relation"
        parts.append(f"{row.get('Source Node', '')}->{row.get('Target Node', '')}:{condition}")
    return " | ".join(parts)


def build_relation_map(
    guard_rows: list[dict[str, str]],
    objects: dict[str, dict[str, Any]],
    atlas_relations: list[dict[str, Any]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for ref in ELIGIBLE_REFS:
        for relation in relation_rows_for_ref(ref, objects, atlas_relations, guard_rows):
            relation["Relation ID"] = f"MMD5-R{len(rows) + 1:03d}"
            rows.append(relation)
    return rows


def build_markdown(
    module_rows: list[dict[str, str]],
    hash_rows: list[dict[str, str]],
    relation_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# MMD-005 - CAP Module Drafts",
        "",
        "Status: completed",
        "",
        "Date: 2026-05-17",
        "",
        "## Decision",
        "",
        "MMD-005 turns the five MMD-004 eligible visual trigger references into local CAP module drafts.",
        "",
        "No canonical `TRG-*` IDs were created. The hashes are draft material fingerprints, not trigger canon.",
        "",
        "## Draft Modules",
        "",
        "| Draft Module | Reference | Working Name | Runtime Role | Hash Handle |",
        "| --- | ---: | --- | --- | --- |",
    ]
    hash_by_module = {row["Draft Module ID"]: row["Hash Handle"] for row in hash_rows}
    for row in module_rows:
        lines.append(
            f"| `{row['Draft Module ID']}` | `{row['Visible Reference']}` | {row['Working Name']} | "
            f"{row['Primary Runtime Role']} | `{hash_by_module[row['Draft Module ID']]}` |"
        )

    lines.extend(
        [
            "",
            "## Module Notes",
            "",
        ]
    )
    for row in module_rows:
        lines.extend(
            [
                f"### {row['Draft Module ID']} - {row['Working Name']}",
                "",
                f"- Visible reference: `{row['Visible Reference']}`",
                f"- CAP function: {row['CAP Function']}",
                f"- Activation surface: {row['Activation Surface']}",
                f"- Trigger cluster: {row['Trigger Cluster'] or 'not mapped'}",
                f"- Architecture layer: {row['Architecture Layer'] or 'not mapped'}",
                f"- Guard summary: {row['Guard Summary'] or 'visual evidence only'}",
                f"- Boundary: {row['Boundary']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Hash Rule",
            "",
            "Each draft hash is built from stable local material:",
            "",
            "- visible reference",
            "- working name",
            "- source state",
            "- runtime role",
            "- CAP function",
            "- activation surface",
            "- guard evidence",
            "- Atlas cluster/layer context",
            "- boundary text",
            "",
            "The hash changes if the draft material changes. It does not prove that the historical trigger definition is complete.",
            "",
            "## Relation Result",
            "",
            f"MMD-005 records {len(relation_rows)} module relation rows across Atlas context and MMD-004 guard evidence.",
            "",
            "## Boundary",
            "",
            "MMD-005 does not:",
            "",
            "- mutate Notion",
            "- use Notion AI",
            "- assign canonical `TRG-*` IDs",
            "- expand `517`, `777` or `988-992`",
            "- treat visual evidence as complete trigger history",
            "",
            "## Repeat Command",
            "",
            "```powershell",
            "python scripts/build_cap_module_drafts.py",
            "```",
            "",
            "## Next",
            "",
            "Best next action: `MMD-006 - CAP Module Registry Package`.",
            "",
            "That package should prepare a mutation-safe registry import/update package for these five draft modules, still without Notion mutation unless explicitly authorized.",
            "",
        ]
    )
    return "\n".join(lines)


def build_batch_markdown(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MMD-005 - CAP Module Drafts",
            "",
            "Date: 2026-05-17",
            "",
            "Activation: `MMD-005 - CAP Module Drafts go`",
            "",
            "Mode: repo-local module drafting",
            "",
            "External mutation: none",
            "",
            "Notion AI credits used: 0",
            "",
            "## Purpose",
            "",
            "MMD-005 drafts local CAP module records for the five safe candidates promoted by MMD-004.",
            "",
            "## Inputs",
            "",
            "| File | Role |",
            "| --- | --- |",
            "| `mmd-004.module-record-candidates.csv` | Canon-gated candidate list. |",
            "| `mmd-004.candidate-review.csv` | Visual evidence rows. |",
            "| `mmd-004.guard-review.csv` | Guard relation rows. |",
            "| `atlas.manifest.v1.1.json` | Local Atlas trigger and cluster context. |",
            "| `trigger-complement-2026-03-30.md` | Repo-local source note for Atlas v1.1 trigger-depth. |",
            "",
            "## Outputs",
            "",
            "| File | Purpose |",
            "| --- | --- |",
            "| `mmd-005.cap-module-drafts.csv` | Five local CAP draft module records. |",
            "| `mmd-005.module-evidence.csv` | Evidence rows for visual candidates, guards and Atlas context. |",
            "| `mmd-005.module-relation-map.csv` | Draft module relation map. |",
            "| `mmd-005.hash-ledger.csv` | Draft hash handles and SHA-256 digests. |",
            "| `mmd-005.hash-material.json` | Hash material used for deterministic fingerprints. |",
            "| `mmd-005.review-summary.json` | Machine-readable summary. |",
            "| `mmd-005.cap-module-drafts.md` | Human-readable module draft summary. |",
            "| `scripts/build_cap_module_drafts.py` | Repeatable draft builder. |",
            "",
            "## Result",
            "",
            f"- Draft modules: {summary['draft_modules']}",
            f"- Evidence rows: {summary['module_evidence_rows']}",
            f"- Relation rows: {summary['module_relation_rows']}",
            f"- Hash rows: {summary['hash_rows']}",
            f"- Eligible references: `{', '.join(summary['eligible_references'])}`",
            "",
            "## Boundary",
            "",
            "The draft hashes fingerprint current module material only. They are not canonical trigger hashes and do not replace source review.",
            "",
            "## Next",
            "",
            "Best next action: `MMD-006 - CAP Module Registry Package`.",
            "",
        ]
    )


def build_causal_log(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "log_id": "CAP-LOG-2026-05-17-MMD-005",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": "Codex",
        "mode": "STUDIO",
        "activation": "manual",
        "source_trace": [
            "docs/atlas/control-tower/mmd-004.module-record-candidates.csv",
            "docs/atlas/control-tower/mmd-004.candidate-review.csv",
            "docs/atlas/control-tower/mmd-004.guard-review.csv",
            "atlas/atlas.manifest.v1.1.json",
            "atlas/sources/trigger-complement-2026-03-30.md",
        ],
        "observation": "MMD-004 promoted five safe visual trigger references for local CAP module draft work.",
        "trigger_band": "401+",
        "trigger_ids": summary["eligible_references"],
        "probabilistic_hypothesis": "The five safe references can act as a minimal CAP module surface for session start, preflight, inspiration, momentum and synchronization.",
        "probability_note": "High confidence for local draft use; incomplete confidence for historical trigger canon until source review expands definitions.",
        "deterministic_boundary": "No external mutation, no Notion AI credit use, no canonical TRG assignment, no expansion of held sensitive or AutoFlow material.",
        "selected_action": "Created local CAP module drafts, evidence rows, relation map and draft hash ledger for references 516, 520, 521, 540 and 544.",
        "feedback_target": "github_atlas",
        "backpropagation_result": "CAP now has five local draft module records that can feed a later registry package or source-review pass.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main() -> int:
    module_candidates = read_csv("mmd-004.module-record-candidates.csv")
    candidate_rows = read_csv("mmd-004.candidate-review.csv")
    guard_rows = read_csv("mmd-004.guard-review.csv")
    objects, atlas_relations = load_atlas()

    eligible_from_gate = [
        row["Visible Reference"]
        for row in module_candidates
        if row.get("Gate Status") == "candidate" and row.get("Visible Reference") in ELIGIBLE_REFS
    ]
    if eligible_from_gate != ELIGIBLE_REFS:
        raise RuntimeError(f"MMD-004 gate mismatch: expected {ELIGIBLE_REFS}, got {eligible_from_gate}")

    module_rows, hash_rows, hash_material = build_modules(candidate_rows, guard_rows, objects, atlas_relations)
    evidence_rows = build_evidence_rows(candidate_rows, guard_rows, objects, atlas_relations)
    relation_rows = build_relation_map(guard_rows, objects, atlas_relations)

    write_csv(
        CONTROL_DIR / "mmd-005.cap-module-drafts.csv",
        module_rows,
        [
            "Draft Module ID",
            "Visible Reference",
            "Working Name",
            "Draft Status",
            "Canon Status",
            "Source State",
            "Primary Runtime Role",
            "CAP Function",
            "Trigger Cluster",
            "Architecture Layer",
            "Activation Surface",
            "Guard Summary",
            "Evidence Count",
            "Guard Count",
            "Hash Handle",
            "Boundary",
            "Next Action",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-005.module-evidence.csv",
        evidence_rows,
        [
            "Evidence Row ID",
            "Draft Module ID",
            "Visible Reference",
            "Evidence Type",
            "Source File",
            "Source Anchor",
            "Label Or Guard",
            "Relation",
            "Status",
            "Boundary",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-005.module-relation-map.csv",
        relation_rows,
        [
            "Relation ID",
            "Visible Reference",
            "Draft Module ID",
            "Relation Source",
            "From",
            "From Title",
            "To",
            "To Title",
            "Relation Type",
            "Guard Condition",
            "Note",
            "Boundary",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-005.hash-ledger.csv",
        hash_rows,
        [
            "Hash Handle",
            "Draft Module ID",
            "Visible Reference",
            "Hash Algorithm",
            "Hash Material Version",
            "Draft Hash",
            "Canon Claim",
            "Hash Material File",
            "Boundary",
        ],
    )

    hash_package = {
        "package_id": "MMD-005-HASH-MATERIAL",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "hash_rule": "SHA-256 over sorted compact JSON material; draft fingerprint only.",
        "source_files": [
            "mmd-004.module-record-candidates.csv",
            "mmd-004.candidate-review.csv",
            "mmd-004.guard-review.csv",
            str(ATLAS_MANIFEST.relative_to(REPO_ROOT)),
            str(TRIGGER_COMPLEMENT.relative_to(REPO_ROOT)),
        ],
        "modules": hash_material,
    }
    (CONTROL_DIR / "mmd-005.hash-material.json").write_text(
        json.dumps(hash_package, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    summary = {
        "review_id": "MMD-005",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "draft_modules": len(module_rows),
        "module_evidence_rows": len(evidence_rows),
        "module_relation_rows": len(relation_rows),
        "hash_rows": len(hash_rows),
        "eligible_references": ELIGIBLE_REFS,
        "hash_handles": {row["Visible Reference"]: row["Hash Handle"] for row in hash_rows},
        "boundary": "CAP module drafts only; no canonical TRG assignment.",
    }
    (CONTROL_DIR / "mmd-005.review-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (CONTROL_DIR / "mmd-005.cap-module-drafts.md").write_text(
        build_markdown(module_rows, hash_rows, relation_rows),
        encoding="utf-8",
    )
    (CONTROL_DIR / "batch-mmd-005.md").write_text(
        build_batch_markdown(summary),
        encoding="utf-8",
    )
    (CONTROL_DIR / "causal-log.mmd-005-module-drafts-2026-05-17.json").write_text(
        json.dumps(build_causal_log(summary), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
