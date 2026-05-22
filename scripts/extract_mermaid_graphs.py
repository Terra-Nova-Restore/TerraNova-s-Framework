#!/usr/bin/env python3
"""Extract Mermaid graph structure for MMD-002.

The extractor is intentionally conservative. It treats the Notion Mermaid CSV
as status truth and the exported code depot as provenance. It does not contact
Notion or any other external system.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "raw" / "exports" / "prism" / "source-pack" / "2026-05-02"
CONTROL_DIR = REPO_ROOT / "docs" / "atlas" / "control-tower"

REGISTRY_CSV = SOURCE_DIR / "📊 Mermaid Diagrams – Code Library 8ce614de6f674ce3bc46a165c573d7f9_all (2).csv"
DEPOT_MD = SOURCE_DIR / "Mermaid Code Library – Complete Collection 999ce78e7102420cbf7a2a4385c28603 (2).md"
MANIFEST_MD = SOURCE_DIR / "🌿 Mermaid als lebendiger Trigger-Organismus – Konz 2e8c384b79d841979068f3595ecbde00 (2).md"
SYNC_SEQUENCE_MD = REPO_ROOT / "docs" / "ai" / "full_sync_terra_nova_mcp_sequence.md"
MMD001_MD = CONTROL_DIR / "mmd-001.mermaid-universe-readpass.md"


NODE_RE = re.compile(
    r"(?P<id>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(?P<bracket>\[\[.*?\]\]|\[.*?\]|\(\(.*?\)\)|\([^)]*?\)|\{.*?\})"
)
EDGE_RE = re.compile(
    r"^\s*(?:(?P<src>[A-Za-z_][A-Za-z0-9_]*)(?:\s*(?:\[\[.*?\]\]|\[.*?\]|\(\(.*?\)\)|\([^)]*?\)|\{.*?\}))?\s*)?"
    r"(?P<op>-->|-\.->|==>|---)"
    r"\s*(?:\|(?P<guard>[^|]*)\|\s*)?"
    r"(?P<tgt>[A-Za-z_][A-Za-z0-9_]*)"
)
PARTICIPANT_RE = re.compile(r"^\s*(?:actor|participant)\s+(?P<id>[A-Za-z_][A-Za-z0-9_]*)\s+as\s+(?P<label>.+)$")
SEQUENCE_EDGE_RE = re.compile(
    r"^\s*(?P<src>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<op>-+>>|-->>|->>|->|-->)\s*(?P<tgt>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<label>.+)$"
)
TRIGGER_LABEL_RE = re.compile(r"\bTrigger\s*([1-9][0-9]{2,3})(?:\s*[-–]\s*([1-9][0-9]{2,3}))?", re.IGNORECASE)
TRIGGER_NODE_RE = re.compile(r"\bT-?([1-9][0-9]{2,3})(?:[_-]([1-9][0-9]{2,3}))?", re.IGNORECASE)


@dataclass
class SourceSpec:
    title: str
    role: str
    zoom: str
    status: str
    registry_type: str
    source_file: Path
    source_kind: str
    code: str


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "graph"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def strip_label(bracket: str) -> str:
    value = bracket.strip()
    pairs = [("[[", "]]"), ("[", "]"), ("((", "))"), ("(", ")"), ("{", "}")]
    for start, end in pairs:
        if value.startswith(start) and value.endswith(end):
            value = value[len(start) : -len(end)]
            break
    value = value.strip().strip('"').strip("'")
    return re.sub(r"<br\s*/?>", " | ", value, flags=re.IGNORECASE)


def clean_section_title(raw: str) -> str:
    value = raw.strip().lstrip("#").strip()
    value = re.sub(r"^[0-9]+[^\w]+", "", value)
    value = re.sub(r"^[^\w]+", "", value)
    return value.strip()


def read_active_registry() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with REGISTRY_CSV.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row.get("Status") == "ACTIVE" and row.get("Role") != "DEPOT" and row.get("Diagram Name"):
                rows.append(row)
    return rows


def split_depot_sections() -> dict[str, str]:
    text = DEPOT_MD.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = clean_section_title(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end]
    return sections


def extract_first_mermaid_block(section: str) -> str:
    fenced = re.search(r"```mermaid\s*(?P<code>.*?)```", section, flags=re.DOTALL)
    if fenced:
        return fenced.group("code").strip()

    lines = section.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("[graph ") or line.startswith("[flowchart "):
            collected: list[str] = [line[1:]]
            for follow in lines[index + 1 :]:
                if re.search(r"\]\([^)]*\)\s*$", follow):
                    collected.append(re.sub(r"\]\([^)]*\)\s*$", "", follow))
                    return "\n".join(collected).strip()
                collected.append(follow)
            return "\n".join(collected).strip()
    return ""


def extract_named_block(path: Path, title: str) -> str:
    text = path.read_text(encoding="utf-8")
    fenced_blocks = re.findall(r"```mermaid\s*(.*?)```", text, flags=re.DOTALL)
    if not fenced_blocks:
        return ""
    if title == "MMD-001 CAP Visual Control Model":
        for block in fenced_blocks:
            if "Mermaid Universe" in block and "CAP Control Tower" in block:
                return block.strip()
    return fenced_blocks[0].strip()


def load_sources() -> list[SourceSpec]:
    sections = split_depot_sections()
    sources: list[SourceSpec] = []

    for row in read_active_registry():
        title = row["Diagram Name"]
        section = sections.get(title, "")
        code = extract_first_mermaid_block(section)
        sources.append(
            SourceSpec(
                title=title,
                role=row.get("Role", ""),
                zoom=row.get("Zoom-of", ""),
                status=row.get("Status", ""),
                registry_type=row.get("Type", ""),
                source_file=DEPOT_MD,
                source_kind="active_registry_depot",
                code=code,
            )
        )

    sources.extend(
        [
            SourceSpec(
                title="SESSION_ROOT Living Trigger Organism",
                role="MANIFEST",
                zoom="TRIGGER-ORGANISM",
                status="ACTIVE",
                registry_type="graph TD",
                source_file=MANIFEST_MD,
                source_kind="manifest",
                code=extract_named_block(MANIFEST_MD, "SESSION_ROOT Living Trigger Organism"),
            ),
            SourceSpec(
                title="Full Sync Terra Nova MCP Sequence",
                role="INTEGRATION",
                zoom="SYNC",
                status="ACTIVE",
                registry_type="sequenceDiagram",
                source_file=SYNC_SEQUENCE_MD,
                source_kind="repo_sequence",
                code=extract_named_block(SYNC_SEQUENCE_MD, "Full Sync Terra Nova MCP Sequence"),
            ),
            SourceSpec(
                title="MMD-001 CAP Visual Control Model",
                role="CAP",
                zoom="CONTROL",
                status="ACTIVE",
                registry_type="flowchart LR",
                source_file=MMD001_MD,
                source_kind="cap_derived",
                code=extract_named_block(MMD001_MD, "MMD-001 CAP Visual Control Model"),
            ),
        ]
    )
    return sources


def diagram_type(code: str) -> tuple[str, str]:
    for raw in code.splitlines():
        line = raw.strip()
        if line.startswith("graph ") or line.startswith("flowchart "):
            parts = line.split()
            return parts[0], parts[1] if len(parts) > 1 else ""
        if line.startswith("sequenceDiagram"):
            return "sequenceDiagram", ""
        if line.startswith("stateDiagram"):
            return "stateDiagram", ""
    return "", ""


def classify_guard(guard: str, operator: str, diagram_kind: str) -> str:
    if diagram_kind == "sequenceDiagram":
        return "sequence_message"
    if guard:
        return "explicit_guard"
    if operator == "---":
        return "structural_link"
    return "unlabeled_transition"


def extract_trigger_refs(value: str) -> str:
    refs: set[str] = set()
    for match in TRIGGER_LABEL_RE.finditer(value or ""):
        refs.add(match.group(1))
        if match.group(2):
            refs.add(match.group(2))
    for match in TRIGGER_NODE_RE.finditer(value or ""):
        refs.add(match.group(1))
        if match.group(2):
            refs.add(match.group(2))
    refs = sorted(refs, key=lambda item: int(item))
    return ";".join(refs)


def detect_signal(value: str, terms: Iterable[str]) -> str:
    lowered = (value or "").lower()
    return "yes" if any(term.lower() in lowered for term in terms) else "no"


def parse_graph(spec: SourceSpec) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    graph_id = slug(spec.title)
    kind, direction = diagram_type(spec.code)
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []
    guards: list[dict[str, str]] = []
    gaps: list[dict[str, str]] = []

    if not spec.code:
        gaps.append(
            {
                "Graph ID": graph_id,
                "Gap Type": "missing_code",
                "Detail": "No Mermaid code block found in configured source.",
                "Severity": "High",
                "Next Action": "Review source page/export and decide whether to preserve as metadata-only graph.",
            }
        )
        return [], [], [], gaps

    current_source = ""
    for line_no, raw in enumerate(spec.code.splitlines(), start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("%%") or stripped.startswith("style ") or stripped.startswith("class ") or stripped.startswith("classDef "):
            continue
        if stripped.startswith("subgraph ") or stripped == "end" or stripped.startswith("note ") or stripped.startswith("alt ") or stripped.startswith("else ") or stripped.startswith("loop ") or stripped.startswith("rect "):
            continue
        if stripped.startswith("graph ") or stripped.startswith("flowchart ") or stripped.startswith("sequenceDiagram") or stripped == "autonumber":
            continue

        participant = PARTICIPANT_RE.match(stripped)
        if participant:
            node_id = participant.group("id")
            nodes.setdefault(
                node_id,
                {
                    "Graph ID": graph_id,
                    "Node ID": node_id,
                    "Label": participant.group("label").strip(),
                    "Node Type": "participant",
                    "Source Line": str(line_no),
                    "In Degree": "0",
                    "Out Degree": "0",
                    "Trigger Signal": "no",
                    "VORTEX Signal": "no",
                    "Sensitivity Signal": "no",
                },
            )
            current_source = node_id
            continue

        sequence_edge = SEQUENCE_EDGE_RE.match(stripped)
        if sequence_edge:
            src = sequence_edge.group("src")
            tgt = sequence_edge.group("tgt")
            label = sequence_edge.group("label").strip()
            for node_id in (src, tgt):
                nodes.setdefault(
                    node_id,
                    {
                        "Graph ID": graph_id,
                        "Node ID": node_id,
                        "Label": node_id,
                        "Node Type": "participant",
                        "Source Line": str(line_no),
                        "In Degree": "0",
                        "Out Degree": "0",
                        "Trigger Signal": "no",
                        "VORTEX Signal": "no",
                        "Sensitivity Signal": "no",
                    },
                )
            edge_id = f"{graph_id}-E{len(edges) + 1:03d}"
            edges.append(
                {
                    "Graph ID": graph_id,
                    "Edge ID": edge_id,
                    "Source Node": src,
                    "Target Node": tgt,
                    "Guard Condition": label,
                    "Operator": sequence_edge.group("op"),
                    "Source Line": str(line_no),
                    "Edge Role": "sequence_message",
                }
            )
            guards.append(
                {
                    "Graph ID": graph_id,
                    "Edge ID": edge_id,
                    "Guard Condition": label,
                    "Guard Type": "sequence_message",
                    "Trigger References": extract_trigger_refs(label),
                    "VORTEX Signal": detect_signal(label, ["vortex", "sync", "reconcile"]),
                    "Boundary": "Message extracted from sequence diagram; not an action authorization.",
                }
            )
            continue

        for node_match in NODE_RE.finditer(stripped):
            node_id = node_match.group("id")
            label = strip_label(node_match.group("bracket"))
            nodes.setdefault(
                node_id,
                {
                    "Graph ID": graph_id,
                    "Node ID": node_id,
                    "Label": label,
                    "Node Type": "node",
                    "Source Line": str(line_no),
                    "In Degree": "0",
                    "Out Degree": "0",
                    "Trigger Signal": detect_signal(label, ["trigger", "T-", "SESSION", "PREFLIGHT", "SYNC"]),
                    "VORTEX Signal": detect_signal(label, ["vortex"]),
                    "Sensitivity Signal": detect_signal(label, ["metarotik", "privat", "token", "dao", "patent", "schattenarchiv"]),
                },
            )
            if stripped.startswith(node_id):
                current_source = node_id

        edge_match = EDGE_RE.match(stripped)
        if edge_match:
            src = edge_match.group("src") or current_source
            tgt = edge_match.group("tgt")
            guard = (edge_match.group("guard") or "").strip().strip('"')
            op = edge_match.group("op")
            if not src:
                gaps.append(
                    {
                        "Graph ID": graph_id,
                        "Gap Type": "edge_without_source",
                        "Detail": f"Line {line_no}: {stripped}",
                        "Severity": "Medium",
                        "Next Action": "Manual review if this edge matters for trigger routing.",
                    }
                )
                continue
            for node_id in (src, tgt):
                nodes.setdefault(
                    node_id,
                    {
                        "Graph ID": graph_id,
                        "Node ID": node_id,
                        "Label": node_id,
                        "Node Type": "implicit",
                        "Source Line": str(line_no),
                        "In Degree": "0",
                        "Out Degree": "0",
                        "Trigger Signal": detect_signal(node_id, ["trigger", "T"]),
                        "VORTEX Signal": detect_signal(node_id, ["vortex"]),
                        "Sensitivity Signal": detect_signal(node_id, ["metarotik", "token", "dao", "patent", "schattenarchiv"]),
                    },
                )
            edge_id = f"{graph_id}-E{len(edges) + 1:03d}"
            role = classify_guard(guard, op, kind)
            edges.append(
                {
                    "Graph ID": graph_id,
                    "Edge ID": edge_id,
                    "Source Node": src,
                    "Target Node": tgt,
                    "Guard Condition": guard,
                    "Operator": op,
                    "Source Line": str(line_no),
                    "Edge Role": role,
                }
            )
            guard_text = " ".join(
                [
                    src,
                    tgt,
                    guard,
                    nodes.get(src, {}).get("Label", ""),
                    nodes.get(tgt, {}).get("Label", ""),
                ]
            )
            guards.append(
                {
                    "Graph ID": graph_id,
                    "Edge ID": edge_id,
                    "Guard Condition": guard,
                    "Guard Type": role,
                    "Trigger References": extract_trigger_refs(guard_text),
                    "VORTEX Signal": detect_signal(" ".join([src, tgt, guard_text]), ["vortex", "sync", "reconcile", "delta"]),
                    "Boundary": "Extracted relation only; not an execution permission.",
                }
            )

    indegree: Counter[str] = Counter()
    outdegree: Counter[str] = Counter()
    for edge in edges:
        outdegree[edge["Source Node"]] += 1
        indegree[edge["Target Node"]] += 1
    for node_id, node in nodes.items():
        node["In Degree"] = str(indegree[node_id])
        node["Out Degree"] = str(outdegree[node_id])

    if not edges:
        gaps.append(
            {
                "Graph ID": graph_id,
                "Gap Type": "no_edges_extracted",
                "Detail": "Mermaid code exists but no edges were parsed.",
                "Severity": "Medium",
                "Next Action": "Review parser coverage for this graph syntax.",
            }
        )
    return list(nodes.values()), edges, guards, gaps


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def main() -> int:
    sources = load_sources()
    graph_rows: list[dict[str, str]] = []
    node_rows: list[dict[str, str]] = []
    edge_rows: list[dict[str, str]] = []
    guard_rows: list[dict[str, str]] = []
    gap_rows: list[dict[str, str]] = []

    for spec in sources:
        graph_id = slug(spec.title)
        kind, direction = diagram_type(spec.code)
        nodes, edges, guards, gaps = parse_graph(spec)
        parsed_type = f"{kind} {direction}".strip()
        registry_type = spec.registry_type.strip()
        if spec.code and registry_type and parsed_type and registry_type != parsed_type:
            gaps.append(
                {
                    "Graph ID": graph_id,
                    "Gap Type": "registry_code_type_mismatch",
                    "Detail": f"Registry type '{registry_type}' differs from extracted code declaration '{parsed_type}'.",
                    "Severity": "Low",
                    "Next Action": "Prefer graph content for extraction, but review active Notion page if render behavior matters.",
                }
            )
        node_rows.extend(nodes)
        edge_rows.extend(edges)
        guard_rows.extend(guards)
        gap_rows.extend(gaps)
        graph_rows.append(
            {
                "Graph ID": graph_id,
                "Title": spec.title,
                "Role": spec.role,
                "Zoom": spec.zoom,
                "Status": spec.status,
                "Type": kind or spec.registry_type,
                "Direction": direction,
                "Source Kind": spec.source_kind,
                "Source File": str(spec.source_file.relative_to(REPO_ROOT)),
                "Source Hash": sha256_text(spec.code) if spec.code else "",
                "Code Lines": str(len(spec.code.splitlines())) if spec.code else "0",
                "Nodes": str(len(nodes)),
                "Edges": str(len(edges)),
                "Guards": str(len([row for row in guards if row.get("Guard Condition")])),
                "Extraction Status": "parsed" if spec.code and edges else "needs_review",
            }
        )

    write_csv(
        CONTROL_DIR / "mmd-002.graphs.csv",
        graph_rows,
        [
            "Graph ID",
            "Title",
            "Role",
            "Zoom",
            "Status",
            "Type",
            "Direction",
            "Source Kind",
            "Source File",
            "Source Hash",
            "Code Lines",
            "Nodes",
            "Edges",
            "Guards",
            "Extraction Status",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-002.nodes.csv",
        node_rows,
        [
            "Graph ID",
            "Node ID",
            "Label",
            "Node Type",
            "Source Line",
            "In Degree",
            "Out Degree",
            "Trigger Signal",
            "VORTEX Signal",
            "Sensitivity Signal",
        ],
    )
    write_csv(
        CONTROL_DIR / "mmd-002.edges.csv",
        edge_rows,
        ["Graph ID", "Edge ID", "Source Node", "Target Node", "Guard Condition", "Operator", "Source Line", "Edge Role"],
    )
    write_csv(
        CONTROL_DIR / "mmd-002.guard-conditions.csv",
        guard_rows,
        ["Graph ID", "Edge ID", "Guard Condition", "Guard Type", "Trigger References", "VORTEX Signal", "Boundary"],
    )
    write_csv(
        CONTROL_DIR / "mmd-002.extraction-gaps.csv",
        gap_rows,
        ["Graph ID", "Gap Type", "Detail", "Severity", "Next Action"],
    )

    report = {
        "extract_id": "MMD-002",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "external_mutation": False,
        "notion_ai_credits_used": 0,
        "source_count": len(sources),
        "graph_count": len(graph_rows),
        "node_count": len(node_rows),
        "edge_count": len(edge_rows),
        "guard_count": len(guard_rows),
        "gap_count": len(gap_rows),
        "graphs": {row["Graph ID"]: {"nodes": row["Nodes"], "edges": row["Edges"], "status": row["Extraction Status"]} for row in graph_rows},
    }
    (CONTROL_DIR / "mmd-002.extraction-summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if gap_rows == [] else 0


if __name__ == "__main__":
    raise SystemExit(main())
