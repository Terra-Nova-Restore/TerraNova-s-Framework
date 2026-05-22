#!/usr/bin/env python3
"""Build the MMD-003 visual trigger bridge from MMD-002 graph tables.

This script keeps the distinction between visible trigger evidence and canon.
It creates trigger module candidates, not authoritative TRG-* definitions.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"

NODE_REFS = re.compile(r"\bT-?([1-9][0-9]{2,3})(?:[_-]([1-9][0-9]{2,3}))?", re.IGNORECASE)
TRIGGER_LABEL_RE = re.compile(r"\bTrigger(?:liste)?\s*[_ ]?([1-9][0-9]{2,3})(?:\s*[-–_]\s*([1-9][0-9]{2,3}))?", re.IGNORECASE)
BARE_SUITE_RE = re.compile(r"\b(98[8-9]|99[0-2]|516|517|520|521|540|544|600|700|777|888|999|1001)\b")

SENSITIVE_TERMS = [
    "schattenarchiv",
    "metarotik",
    "privat",
    "token",
    "dao",
    "patent",
    "wallet",
    "ipfs",
    "cid",
    "polygon",
    "sigma",
]

TRIGGER_SURFACE_TERMS = [
    "trigger",
    "codex139",
    "codex_139",
    "sessionstart",
    "session_start",
    "preflight",
    "autoflow",
    "audit",
    "delta-sync",
    "delta sync",
    "sync",
    "synchronisationsknoten",
]

GUARD_TERMS = [
    "session",
    "preflight",
    "audit",
    "autoflow",
    "delta",
    "sync",
    "reconcile",
    "pull",
    "push",
    "auth",
    "trigger",
    "commit",
    "cursor",
    "savepoint",
]

KNOWN_MODULES = {
    "174-210": "Silvi/Codex139 range candidate",
    "516": "Inspiration trigger candidate",
    "517": "AutoFlow trigger candidate",
    "520": "SessionStart trigger candidate",
    "521": "Preflight trigger candidate",
    "540": "Observable momentum trigger candidate",
    "544": "Synchronization node trigger candidate",
    "600": "Trigger list / field candidate",
    "700": "Security ritual candidate",
    "777": "Schattenarchiv trigger candidate",
    "888": "Truth-efficiency audit overlay candidate",
    "988": "Snapshot lockpoint integrity candidate",
    "989": "Token sync beacon integrity candidate",
    "990": "Trigger audit engine integrity candidate",
    "991": "ZIP integrity pulse candidate",
    "992": "TriggerMap echo sync candidate",
    "999": "Workspace coherence candidate",
    "1001": "Pegasus output-log candidate",
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (CONTROL_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def lower(value: str) -> str:
    return (value or "").lower()


def extract_refs(*values: str) -> list[str]:
    refs: set[str] = set()
    joined = " ".join(value or "" for value in values)
    for match in TRIGGER_LABEL_RE.finditer(joined):
        if match.group(2):
            refs.add(f"{match.group(1)}-{match.group(2)}")
        else:
            refs.add(match.group(1))
    for match in NODE_REFS.finditer(joined):
        if match.group(2):
            refs.add(f"{match.group(1)}-{match.group(2)}")
        else:
            refs.add(match.group(1))
    for match in BARE_SUITE_RE.finditer(joined):
        refs.add(match.group(1))

    def key(ref: str) -> tuple[int, int]:
        if "-" in ref:
            start, end = ref.split("-", 1)
            return int(start), int(end)
        return int(ref), int(ref)

    return sorted(refs, key=key)


def normalize_refs(refs: Iterable[str]) -> list[str]:
    normalized = {ref for ref in refs if ref}
    if "174" in normalized and "210" in normalized:
        normalized.discard("174")
        normalized.discard("210")
        normalized.add("174-210")

    def key(ref: str) -> tuple[int, int]:
        if "-" in ref:
            start, end = ref.split("-", 1)
            return int(start), int(end)
        return int(ref), int(ref)

    return sorted(normalized, key=key)


def has_any(value: str, terms: Iterable[str]) -> bool:
    text = lower(value)
    return any(term in text for term in terms)


def sensitivity_for(*values: str) -> str:
    text = lower(" ".join(values))
    if "schattenarchiv" in text or "metarotik" in text or "privat" in text or "sigma" in text:
        return "Restricted"
    if any(term in text for term in ["token", "dao", "patent", "wallet", "ipfs", "cid", "polygon"]):
        return "Sensitive"
    return "Internal"


def candidate_class(refs: list[str], label: str, node_id: str) -> str:
    text = lower(f"{label} {node_id}")
    if refs:
        return "numeric_range" if any("-" in ref for ref in refs) else "numeric_anchor"
    if "trigger" in text:
        return "trigger_surface"
    if "codex" in text:
        return "codex_surface"
    if "sync" in text or "delta" in text:
        return "sync_surface"
    if "audit" in text:
        return "audit_surface"
    if "session" in text or "preflight" in text:
        return "session_surface"
    return "visual_module"


def source_state_for(refs: list[str], klass: str) -> str:
    if refs:
        return "visible_numeric_evidence"
    if klass.endswith("_surface"):
        return "visible_surface_evidence"
    return "visual_context_evidence"


def proposed_module(refs: list[str], label: str) -> str:
    if refs:
        modules = [KNOWN_MODULES.get(ref, f"Trigger {ref} candidate") for ref in refs]
        return "; ".join(modules)
    text = lower(label)
    if "trigger-architektur" in text:
        return "Trigger architecture surface"
    if "trigger-list" in text or "triggerlisten" in text:
        return "Trigger list surface"
    if "sync" in text or "delta" in text:
        return "Sync / reconciliation surface"
    if "audit" in text:
        return "Audit surface"
    if "codex" in text:
        return "Codex bridge surface"
    return "Visual module candidate"


def canonical_status(refs: list[str]) -> str:
    if not refs:
        return "not a canonical TRG assignment"
    return "visible number only; canon not asserted"


def node_evidence(node: dict[str, str], graph: dict[str, str]) -> str:
    return f"{graph.get('Title', node['Graph ID'])} :: {node.get('Node ID')} :: {node.get('Label')}"


def build_candidates(nodes: list[dict[str, str]], graphs: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for node in nodes:
        label = node.get("Label", "")
        node_id = node.get("Node ID", "")
        refs = extract_refs(node_id, label)
        visible = bool(refs) or has_any(f"{node_id} {label}", TRIGGER_SURFACE_TERMS)
        if not visible:
            continue
        key = (node["Graph ID"], node_id)
        if key in seen:
            continue
        seen.add(key)
        graph = graphs.get(node["Graph ID"], {})
        klass = candidate_class(refs, label, node_id)
        sensitivity = sensitivity_for(label, node_id, graph.get("Title", ""))
        rows.append(
            {
                "Bridge ID": f"VTB-{len(rows) + 1:03d}",
                "Graph ID": node["Graph ID"],
                "Graph Role": graph.get("Role", ""),
                "Graph Zoom": graph.get("Zoom", ""),
                "Node ID": node_id,
                "Label": label,
                "Trigger References": ";".join(refs),
                "Candidate Class": klass,
                "Source State": source_state_for(refs, klass),
                "Sensitivity": sensitivity,
                "In Degree": node.get("In Degree", ""),
                "Out Degree": node.get("Out Degree", ""),
                "VORTEX Signal": node.get("VORTEX Signal", "no"),
                "Evidence": node_evidence(node, graph),
                "Proposed CAP Module": proposed_module(refs, label),
                "Canonical TRG Status": canonical_status(refs),
                "Boundary": "Candidate only; do not assign canonical TRG semantics without source review.",
                "Next Action": "Use in MMD-004 review queue" if sensitivity != "Restricted" else "Gate through sensitivity review before expansion",
            }
        )
    return rows


def build_guard_bridge(guards: list[dict[str, str]], edges: dict[str, dict[str, str]], graphs: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for guard in guards:
        refs = normalize_refs(ref for ref in (guard.get("Trigger References") or "").split(";") if ref)
        condition = guard.get("Guard Condition", "")
        text = " ".join([condition, guard.get("Graph ID", ""), guard.get("Guard Type", "")])
        if not refs and not has_any(text, GUARD_TERMS):
            continue
        edge = edges.get(guard.get("Edge ID", ""), {})
        graph = graphs.get(guard.get("Graph ID", ""), {})
        src = edge.get("Source Node", "")
        tgt = edge.get("Target Node", "")
        sensitivity = sensitivity_for(condition, src, tgt, graph.get("Title", ""))
        rows.append(
            {
                "Bridge Edge ID": f"VTG-{len(rows) + 1:03d}",
                "Graph ID": guard.get("Graph ID", ""),
                "Graph Role": graph.get("Role", ""),
                "Source Node": src,
                "Target Node": tgt,
                "Guard Condition": condition,
                "Guard Type": guard.get("Guard Type", ""),
                "Trigger References": ";".join(refs),
                "VORTEX Signal": guard.get("VORTEX Signal", ""),
                "Sensitivity": sensitivity,
                "Bridge Meaning": "activation guard" if condition else "structural trigger relation",
                "Boundary": "Relation only; not execution permission.",
            }
        )
    return rows


def build_review_rows(candidates: list[dict[str, str]], guards: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for candidate in candidates:
        if candidate["Sensitivity"] in {"Sensitive", "Restricted"}:
            rows.append(
                {
                    "Review ID": f"VTR-{len(rows) + 1:03d}",
                    "Source Type": "candidate",
                    "Source ID": candidate["Bridge ID"],
                    "Graph ID": candidate["Graph ID"],
                    "Reason": candidate["Sensitivity"],
                    "Evidence": candidate["Evidence"],
                    "Required Gate": "SENS-001 boundary",
                    "Decision": "hold for explicit review",
                }
            )
    for guard in guards:
        if guard["Sensitivity"] in {"Sensitive", "Restricted"}:
            rows.append(
                {
                    "Review ID": f"VTR-{len(rows) + 1:03d}",
                    "Source Type": "guard",
                    "Source ID": guard["Bridge Edge ID"],
                    "Graph ID": guard["Graph ID"],
                    "Reason": guard["Sensitivity"],
                    "Evidence": f"{guard['Source Node']} -> {guard['Target Node']} | {guard['Guard Condition']}",
                    "Required Gate": "SENS-001 boundary",
                    "Decision": "hold for explicit review",
                }
            )
    return rows


def build_summary(candidates: list[dict[str, str]], guards: list[dict[str, str]], reviews: list[dict[str, str]]) -> dict[str, object]:
    class_counts = Counter(row["Candidate Class"] for row in candidates)
    sensitivity_counts = Counter(row["Sensitivity"] for row in candidates)
    graph_counts = Counter(row["Graph ID"] for row in candidates)
    refs: set[str] = set()
    for row in candidates:
        refs.update(ref for ref in row["Trigger References"].split(";") if ref)
    for row in guards:
        refs.update(ref for ref in row["Trigger References"].split(";") if ref)
    refs = set(normalize_refs(refs))
    return {
        "bridge_id": "MMD-003",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "candidate_count": len(candidates),
        "guard_bridge_count": len(guards),
        "review_count": len(reviews),
        "unique_trigger_reference_count": len(refs),
        "unique_trigger_references": sorted(refs, key=lambda ref: int(ref.split("-", 1)[0])),
        "candidate_class_counts": dict(sorted(class_counts.items())),
        "candidate_sensitivity_counts": dict(sorted(sensitivity_counts.items())),
        "top_graphs": dict(graph_counts.most_common(10)),
        "boundary": "Candidate bridge only; no canonical TRG assignment.",
    }


def main() -> int:
    graphs = {row["Graph ID"]: row for row in read_csv("mmd-002.graphs.csv")}
    nodes = read_csv("mmd-002.nodes.csv")
    edges = {row["Edge ID"]: row for row in read_csv("mmd-002.edges.csv")}
    guards = read_csv("mmd-002.guard-conditions.csv")

    candidates = build_candidates(nodes, graphs)
    guard_bridge = build_guard_bridge(guards, edges, graphs)
    review_rows = build_review_rows(candidates, guard_bridge)
    summary = build_summary(candidates, guard_bridge, review_rows)

    write_csv(
        CONTROL_DIR / "mmd-003.visual-trigger-candidates.csv",
        candidates,
        [
            "Bridge ID",
            "Graph ID",
            "Graph Role",
            "Graph Zoom",
            "Node ID",
            "Label",
            "Trigger References",
            "Candidate Class",
            "Source State",
            "Sensitivity",
            "In Degree",
            "Out Degree",
            "VORTEX Signal",
            "Evidence",
            "Proposed CAP Module",
            "Canonical TRG Status",
            "Boundary",
            "Next Action",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-003.guard-bridge.csv",
        guard_bridge,
        [
            "Bridge Edge ID",
            "Graph ID",
            "Graph Role",
            "Source Node",
            "Target Node",
            "Guard Condition",
            "Guard Type",
            "Trigger References",
            "VORTEX Signal",
            "Sensitivity",
            "Bridge Meaning",
            "Boundary",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-003.sensitivity-review.csv",
        review_rows,
        ["Review ID", "Source Type", "Source ID", "Graph ID", "Reason", "Evidence", "Required Gate", "Decision"],
    )
    (CONTROL_DIR / "mmd-003.bridge-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
