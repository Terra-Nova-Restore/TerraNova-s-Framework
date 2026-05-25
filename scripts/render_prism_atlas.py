#!/usr/bin/env python3
"""Render a reviewed TerraNova CIC atlas from historical Prism/Notion exports."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT / "raw" / "exports" / "prism" / "source-pack"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "atlas"

SUPPORTED_SUFFIXES = {".md", ".csv"}
DATE_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CATEGORY_RULES = [
    ("all-in-one bundle", ("allinone",)),
    ("landing atlas", ("system atlas", "cic framework overview")),
    ("master overview", ("master overview", "terra nova workspace")),
    ("diagram registry", ("mermaid code library", "mermaid diagrams")),
    ("mermaid manifesto", ("mermaid-diagramme", "lebendiger trigger", "living trigger")),
    ("framework reference", ("frameworks", "eigenkonzepte")),
    ("sync architecture", ("notion", "chatgpt", "system-architektur", "fullsync")),
    ("routing", ("meta-conductor", "agent routing")),
    ("product/service", ("produkte", "services")),
    ("technical documentation", ("technische dokumentation", "digital ecosystem")),
    ("token/blockchain", ("blockchain", "token", "dao")),
    ("outreach", ("outreach", "session log", "apertus")),
    ("research review", ("deep research", "repository", "commit")),
    ("chat provenance", ("chatverlauf", "quelle")),
    ("trigger register", ("trigger-system", "triggermap", "trigger", "codex & trigger")),
]

SENSITIVITY_RULES = {
    "private": ("privat", "private", "persoenlich", "persönlich", "intim", "metarotik", "schattenarchiv"),
    "token/wallet": ("wallet", "token", "dao", "smart contract", "solidity", "polygon", "treasury"),
    "patent/ip": ("patent", "ip", "prior art", "ige", "tnpx"),
    "trigger-depth": ("trigger 777", "trigger-system", "trigger audit", "trigger 988", "trigger 992"),
    "raw-chat": ("chatverlauf", "raw chat", "quelle", "session-history"),
    "external/public": ("public", "outreach", "investor", "landing", "pitch", "mermaid.ai"),
}


@dataclass
class SourceArtifact:
    path: Path
    rel_path: str
    title: str
    suffix: str
    size: int
    sha256: str
    category: str
    sensitivity: list[str]
    headings: list[str] = field(default_factory=list)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def clean_filename_title(path: Path) -> str:
    stem = re.sub(r"\s+\(\d+\)$", "", path.stem)
    stem = re.sub(r"\s+[0-9a-f]{24,}$", "", stem, flags=re.IGNORECASE)
    return normalize(stem.replace("_", " "))


def markdown_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return normalize(match.group(1))
    return clean_filename_title(path)


def markdown_headings(text: str, limit: int = 8) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+)$", line.strip())
        if match:
            headings.append(normalize(match.group(1)))
        if len(headings) >= limit:
            break
    return headings


def csv_title(path: Path) -> str:
    return clean_filename_title(path)


def categorize(title: str, path: Path, text: str) -> str:
    haystack = f"{title} {path.name}".lower()
    for category, needles in CATEGORY_RULES:
        if any(needle in haystack for needle in needles):
            return category
    return "source note"


def sensitivity_flags(title: str, path: Path, text: str) -> list[str]:
    haystack = f"{title} {path.name} {text}".lower()
    flags = [label for label, needles in SENSITIVITY_RULES.items() if any(needle in haystack for needle in needles)]
    return sorted(flags)


def collect_sources(source_dir: Path) -> list[SourceArtifact]:
    if not source_dir.exists():
        raise SystemExit(f"Source directory not found: {source_dir}")

    artifacts: list[SourceArtifact] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = read_text(path)
        title = markdown_title(text, path) if path.suffix.lower() == ".md" else csv_title(path)
        artifacts.append(
            SourceArtifact(
                path=path,
                rel_path=path.relative_to(source_dir).as_posix(),
                title=title,
                suffix=path.suffix.lower().lstrip("."),
                size=path.stat().st_size,
                sha256=sha256_file(path),
                category=categorize(title, path, text),
                sensitivity=sensitivity_flags(title, path, text),
                headings=markdown_headings(text) if path.suffix.lower() == ".md" else [],
            )
        )
    return artifacts


def has_dated_child_dirs(source_dir: Path) -> bool:
    return any(path.is_dir() and DATE_DIR_PATTERN.match(path.name) for path in source_dir.iterdir())


def resolve_source_dir(source_dir: Path) -> Path:
    source_dir = source_dir.resolve()
    if not source_dir.exists():
        raise SystemExit(f"Source directory not found: {source_dir}")

    dated_dirs = [
        path
        for path in source_dir.iterdir()
        if path.is_dir() and DATE_DIR_PATTERN.match(path.name)
    ]
    if source_dir == DEFAULT_SOURCE_DIR.resolve() and dated_dirs:
        return sorted(dated_dirs, key=lambda path: path.name)[-1]
    if dated_dirs and not any(path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES for path in source_dir.iterdir()):
        return sorted(dated_dirs, key=lambda path: path.name)[-1]
    return source_dir


def source_stamp(source_dir: Path) -> str:
    if DATE_DIR_PATTERN.match(source_dir.name):
        return source_dir.name
    return datetime.now().astimezone().isoformat(timespec="seconds")


def manifest_source_dir(source_dir_value: str) -> Path:
    source_dir = Path(source_dir_value)
    if not source_dir.is_absolute():
        source_dir = ROOT / source_dir
    return source_dir


def load_manifest_snapshot(
    manifest_path: Path,
) -> tuple[list[SourceArtifact], list[dict[str, str]], Path, str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_dir = manifest_source_dir(str(data.get("source_dir", DEFAULT_SOURCE_DIR)))
    generated_at = str(data.get("generated_at", source_stamp(source_dir)))

    artifacts: list[SourceArtifact] = []
    for entry in data.get("source_files", []):
        rel_path = str(entry["source"])
        artifacts.append(
            SourceArtifact(
                path=ROOT / rel_path,
                rel_path=rel_path,
                title=str(entry["title"]),
                suffix=str(entry["type"]),
                size=int(entry["size_bytes"]),
                sha256=str(entry["sha256"]),
                category=str(entry["category"]),
                sensitivity=[str(flag) for flag in entry.get("sensitivity", [])],
                headings=[str(heading) for heading in entry.get("headings", [])],
            )
        )

    diagram_rows = [
        {str(key): str(value) for key, value in row.items()}
        for row in data.get("diagrams", [])
    ]
    return artifacts, deduplicate_diagrams(diagram_rows), source_dir, generated_at


def should_use_manifest_snapshot(source_dir: Path, artifacts: list[SourceArtifact]) -> bool:
    if not artifacts:
        return True
    if has_dated_child_dirs(source_dir):
        return False
    return len(artifacts) == 1 and artifacts[0].rel_path.casefold() == "readme.md"


def should_fallback_to_manifest_snapshot(requested_source_dir: Path) -> bool:
    return requested_source_dir.resolve() == DEFAULT_SOURCE_DIR.resolve()


def resolve_render_inputs(
    source_dir: Path,
    output_dir: Path,
) -> tuple[list[SourceArtifact], list[dict[str, str]], Path, str]:
    manifest_path = output_dir / "source_manifest.json"
    try:
        resolved_source_dir = resolve_source_dir(source_dir)
        artifacts = collect_sources(resolved_source_dir)
    except SystemExit:
        if manifest_path.exists() and should_fallback_to_manifest_snapshot(source_dir):
            return load_manifest_snapshot(manifest_path)
        raise

    # CI does not receive private dated source-pack exports. Re-render from the
    # committed manifest when only the archival README is present.
    if manifest_path.exists() and should_use_manifest_snapshot(resolved_source_dir, artifacts):
        return load_manifest_snapshot(manifest_path)

    if not artifacts:
        raise SystemExit(f"No supported source files found in: {resolved_source_dir}")
    return artifacts, deduplicate_diagrams(parse_diagram_registry(artifacts)), resolved_source_dir, source_stamp(resolved_source_dir)


def parse_diagram_registry(artifacts: list[SourceArtifact]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for artifact in artifacts:
        if artifact.suffix != "csv":
            continue
        text = read_text(artifact.path)
        try:
            reader = csv.DictReader(text.splitlines())
        except csv.Error:
            continue
        if not reader.fieldnames or "Diagram Name" not in reader.fieldnames:
            continue
        for index, row in enumerate(reader, start=1):
            name = normalize(row.get("Diagram Name", ""))
            if not name:
                continue
            rows.append(
                {
                    "name": name,
                    "category": normalize(row.get("Category", "")),
                    "complexity": normalize(row.get("Complexity", "")),
                    "status": normalize(row.get("Status", "")) or "UNKNOWN",
                    "role": normalize(row.get("Role", "")),
                    "type": normalize(row.get("Type", "")),
                    "zoom": normalize(row.get("Zoom-of", "")),
                    "lines": normalize(row.get("Lines of Code", "")),
                    "source_url": normalize(row.get("Source Page URL", "")),
                    "source_artifact": artifact.rel_path,
                    "row": str(index),
                }
            )
    return rows


def deduplicate_diagrams(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str, str]] = set()
    unique: list[dict[str, str]] = []
    for row in rows:
        key = (
            row["name"].casefold(),
            row["status"].casefold(),
            row["role"].casefold(),
            row["type"].casefold(),
            row["source_url"].casefold(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(cell.replace("\n", " ").replace("|", "\\|") for cell in row) + " |")
    return output


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def find_artifact(artifacts: list[SourceArtifact], category: str) -> SourceArtifact | None:
    matches = [artifact for artifact in artifacts if artifact.category == category]
    if not matches:
        return None
    return max(matches, key=lambda artifact: artifact.size)


def find_artifact_by_title(artifacts: list[SourceArtifact], title_part: str) -> SourceArtifact | None:
    title_part = title_part.casefold()
    matches = [artifact for artifact in artifacts if title_part in artifact.title.casefold()]
    if not matches:
        return None
    return max(matches, key=lambda artifact: artifact.size)


def source_cell(artifact: SourceArtifact | None) -> str:
    if not artifact:
        return "-"
    return f"`{artifact.rel_path}`"


def repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def render_index(
    artifacts: list[SourceArtifact],
    diagram_rows: list[dict[str, str]],
    source_dir: Path,
    generated_at: str,
) -> str:
    hash_groups = defaultdict(list)
    for artifact in artifacts:
        hash_groups[artifact.sha256].append(artifact)
    duplicates = [items for items in hash_groups.values() if len(items) > 1]
    active_count = sum(1 for row in diagram_rows if row["status"].upper() == "ACTIVE")
    legacy_count = sum(1 for row in diagram_rows if row["status"].upper() == "LEGACY")
    unknown_count = sum(1 for row in diagram_rows if row["status"].upper() == "UNKNOWN")

    payload = find_artifact(artifacts, "all-in-one bundle")
    landing = find_artifact(artifacts, "landing atlas")
    trigger_ref = find_artifact(artifacts, "trigger register")
    diagram_registry = find_artifact_by_title(artifacts, "Mermaid Code Library - Complete Collection") or find_artifact(
        artifacts,
        "diagram registry",
    )
    manifesto = find_artifact(artifacts, "mermaid manifesto")
    chat_source = find_artifact(artifacts, "chat provenance")

    lines = [
        "# TerraNova CIC Atlas",
        "",
        "Status: generated local atlas start page",
        "",
        f"Generated: {generated_at}",
        f"Source directory: `{repo_path(source_dir)}`",
        "",
        "## Purpose",
        "",
        "This page is the reviewed navigation layer for the CIC source pack.",
        "Raw exports stay in `raw/exports/prism/source-pack/` for provenance; curated working surfaces live here in `docs/atlas/`.",
        "",
        "## Naming boundary",
        "",
        "- **CIC** is the TerraNova framework, consistency and atlas layer.",
        "- **OpenAI Prism** is an external/editor source context only where explicitly meant.",
        "- Historical paths containing `prism` are not automatically renamed when they serve as raw provenance.",
        "",
        "## Snapshot",
        "",
    ]
    lines.extend(
        md_table(
            ["Metric", "Value"],
            [
                ["Source files", str(len(artifacts))],
                ["Unique payloads", str(len(hash_groups))],
                ["Duplicate payload groups", str(len(duplicates))],
                ["Diagram registry rows", str(len(diagram_rows))],
                ["Active diagrams", str(active_count)],
                ["Legacy diagrams", str(legacy_count)],
                ["Unknown diagram rows", str(unknown_count)],
                ["Total source size", human_size(sum(artifact.size for artifact in artifacts))],
            ],
        )
    )

    lines.extend(["", "## Use First", ""])
    lines.extend(
        md_table(
            ["Need", "Use", "Source"],
            [
                ["Orient TerraNova/CIC work", "Start with the landing atlas, then drill into diagrams.", source_cell(landing)],
                ["Archive the full graph payload", "Use the All-in-One bundle as the unchanged source payload.", source_cell(payload)],
                ["Route trigger work", "Use the trigger reference only as an index and gap tracker.", source_cell(trigger_ref)],
                ["Pick Mermaid diagrams", "Use `docs/atlas/diagrams.md`; prefer ACTIVE rows over LEGACY/UNKNOWN.", "`docs/atlas/diagrams.md`"],
                ["Prepare public material", "Start from the Mermaid manifesto and public outreach material, then review redactions.", source_cell(manifesto)],
                ["Check provenance", "Use chat source only as context, not canonical truth.", source_cell(chat_source)],
            ],
        )
    )

    lines.extend(["", "## Working Read", ""])
    lines.extend(
        [
            "- `ACTIVE` diagram rows are the current working set.",
            "- `LEGACY` rows are kept for history and replacement tracing.",
            "- `UNKNOWN` rows come from the short CSV export and are not status truth.",
            "- Source files with sensitivity flags are usable internally but need review before publication.",
            "- Trigger ranges that are not documented remain open gaps, not inferred system content.",
        ]
    )

    lines.extend(["", "## Source Roles", ""])
    role_rows = [
        ["Payload bundle", "`TerraNova_AllInOne`", "Archiveable full export for graph, Mermaid and README material.", source_cell(payload)],
        ["Landing atlas", "`TerraNova System Atlas - CIC Framework Overview`", "Human-readable start page and onboarding map.", source_cell(landing)],
        ["Trigger register", "`Trigger-System - Deep Reference (1-992)`", "Internal trigger index, gap tracking and routing reference.", source_cell(trigger_ref)],
        ["Diagram registry", "`Mermaid Code Library` plus CSV registry", "Renderable graph source and active/legacy metadata.", source_cell(diagram_registry)],
    ]
    lines.extend(md_table(["Role", "Anchor", "Use", "Source"], role_rows))

    lines.extend(["", "## Public/Internal Split", ""])
    lines.extend(
        md_table(
            ["Bucket", "Use", "Review rule"],
            [
                ["Public candidate", "Mermaid manifesto, high-level atlas, selected ACTIVE diagrams.", "Redact private, wallet/token and patent-sensitive material first."],
                ["Internal operating map", "All source categories, source manifest and trigger reference.", "Allowed for Codex/CIC work under reviewed-source discipline."],
                ["Archive only", "Raw chat provenance and All-in-One payload.", "Do not promote as canonical truth without extracted review notes."],
                ["Decision required", "Token/blockchain, patent/IP and deep trigger material.", "Needs explicit human review before external use."],
            ],
        )
    )

    lines.extend(["", "## Full Inventory", ""])
    lines.extend(
        [
            "- Machine-readable source list: `source_inventory.csv`.",
            "- Full generated manifest: `source_manifest.json`.",
            "- Diagram selection and replacement view: `diagrams.md`.",
        ]
    )

    lines.extend(["", "## Operating Rule", ""])
    lines.extend(
        [
            "- Raw source exports stay archival and unchanged.",
            "- Curated docs derived from this atlas need source status and review status.",
            "- Trigger gaps stay gaps until a reviewed source documents them.",
            "- Public material must avoid private trigger canon, wallet/token operations, patent-sensitive mappings and raw personal logs.",
        ]
    )

    return "\n".join(lines) + "\n"


def render_diagrams(diagram_rows: list[dict[str, str]], generated_at: str) -> str:
    rows = deduplicate_diagrams(diagram_rows)
    by_status = defaultdict(list)
    for row in rows:
        by_status[row["status"].upper()].append(row)

    active_by_name = {row["name"]: row for row in by_status.get("ACTIVE", [])}

    def recommended_use(row: dict[str, str]) -> str:
        name = row["name"].casefold()
        role = row["role"].upper()
        zoom = row["zoom"].upper()
        if "master overview" in name:
            return "Primary workspace map"
        if "digital ecosystem" in name:
            return "Target structure map"
        if "notion" in name and "chatgpt" in name:
            return "Integration architecture"
        if "meta-conductor" in name:
            return "Agent routing map"
        if "tokenaccess" in name:
            return "Trigger appendix"
        if "code library" in name:
            return "Diagram depot"
        if role == "ZOOM":
            return f"Zoom view for {zoom}" if zoom else "Zoom view"
        return "Reviewed diagram source"

    def diagram_table(items: list[dict[str, str]]) -> list[str]:
        sorted_items = sorted(items, key=lambda row: (row["name"].casefold(), row["status"].casefold()))
        return md_table(
            ["Name", "Status", "Use", "Role", "Type", "Zoom", "Lines", "Source artifact"],
            [
                [
                    row["name"],
                    row["status"],
                    recommended_use(row),
                    row["role"] or "-",
                    row["type"] or "-",
                    row["zoom"] or "-",
                    row["lines"] or "-",
                    row["source_artifact"],
                ]
                for row in sorted_items
            ],
        )

    duplicate_names = [
        (name, count)
        for name, count in Counter(row["name"] for row in rows).items()
        if count > 1
    ]

    lines = [
        "# TerraNova Mermaid Diagram Registry",
        "",
        "Status: generated local atlas diagram selection",
        "",
        f"Generated: {generated_at}",
        "",
        "## Decision",
        "",
        "Use `ACTIVE` diagrams for current docs and public-facing drafts.",
        "`LEGACY` rows remain useful for replacement tracing. `UNKNOWN` rows come",
        "from the short CSV export and should not override the `_all` CSV status.",
        "",
        "## Summary",
        "",
    ]
    lines.extend(
        md_table(
            ["Status", "Rows"],
            [[status, str(len(items))] for status, items in sorted(by_status.items())],
        )
    )

    for status in ("ACTIVE", "LEGACY", "ORPHAN", "UNKNOWN"):
        items = by_status.get(status, [])
        lines.extend(["", f"## {status.title()} Diagrams", ""])
        if items:
            lines.extend(diagram_table(items))
        else:
            lines.append("None detected.")

    lines.extend(["", "## Repeated Diagram Names", ""])
    if duplicate_names:
        lines.extend(md_table(["Name", "Occurrences"], [[name, str(count)] for name, count in sorted(duplicate_names)]))
    else:
        lines.append("No repeated diagram names detected after registry de-duplication.")

    legacy_with_replacement = [
        [row["name"], row["type"] or "-", active_by_name[row["name"]]["type"] or "-", active_by_name[row["name"]]["source_artifact"]]
        for row in by_status.get("LEGACY", [])
        if row["name"] in active_by_name
    ]
    lines.extend(["", "## Legacy Replacement Map", ""])
    if legacy_with_replacement:
        lines.extend(md_table(["Legacy name", "Legacy type", "Active type", "Use active source"], legacy_with_replacement))
    else:
        lines.append("No legacy rows with active replacements detected.")

    return "\n".join(lines) + "\n"


def render_public_overview(
    artifacts: list[SourceArtifact],
    diagram_rows: list[dict[str, str]],
    generated_at: str,
) -> str:
    active_diagrams = [row for row in diagram_rows if row["status"].upper() == "ACTIVE"]
    landing = find_artifact(artifacts, "landing atlas")
    manifesto = find_artifact(artifacts, "mermaid manifesto")

    lines = [
        "# TerraNova Public Overview",
        "",
        "Status: public-candidate draft generated from reviewed local atlas metadata",
        "",
        f"Generated: {generated_at}",
        "",
        "## Positioning",
        "",
        "TerraNova is a source-aware coordination framework for complex knowledge work.",
        "The public-facing slice now has four stable ideas: a navigable system atlas,",
        "Mermaid diagrams as living system maps, CIC as the consistency and coordination",
        "model behind the workspace, and the public semantic architecture spine.",
        "",
        "## Public Story",
        "",
        "- The atlas gives humans and agents the same orientation map.",
        "- Mermaid diagrams act as executable-looking system maps: nodes mark active concepts, edges mark relationships and routing paths.",
        "- Semantic Trigger Architecture treats triggers as semantic displacement spaces, not flat activators.",
        "- SCL treats language, commands, trigger names and symbolic references as operating surfaces.",
        "- CIC keeps large workspaces coherent by separating source, claim, route, review and publication layers.",
        "- Prism is treated as the internal authoring/editor layer until naming review is complete.",
        "",
        "## Public-Safe Building Blocks",
        "",
    ]
    lines.extend(
        md_table(
            ["Block", "Use"],
            [
                ["Atlas", "High-level workspace navigation and onboarding."],
                ["Mermaid", "Visual language for system structure, routing and public explanation."],
                ["Semantic Spine", "Public bridge for SCL, triggers, interaction collapse, LDM and Lenhard Model."],
                ["CIC", "Consistency and coordination model for human-AI collaboration."],
                ["Prism", "Internal authoring/editor context; avoid market-facing name hardening before review."],
            ],
        )
    )

    lines.extend(["", "## Semantic Spine Entry Points", ""])
    lines.extend(
        md_table(
            ["Artifact", "Use"],
            [
                ["`docs/architecture/public_semantic_architecture_spine.md`", "Public entry point for the semantic architecture spine."],
                ["`docs/atlas/semantic_spine_registry.md`", "Registry bridge between architecture docs, atlas, source routing and release artifact."],
                ["`docs/public/semantic_architecture_public_release_v0_1.md`", "Citable public release candidate."],
                ["`docs/atlas/mermaid_cluster.md`", "Visual trigger graph bridge from Mermaid to trigger/SCL architecture."],
            ],
        )
    )

    lines.extend(["", "## Diagram Candidates", ""])
    lines.extend(
        md_table(
            ["Diagram", "Public use", "Source status"],
            [
                [row["name"], "Use only after content review and redaction.", row["status"]]
                for row in sorted(active_diagrams, key=lambda row: row["name"].casefold())
            ],
        )
    )

    lines.extend(["", "## Do Not Publish Without Review", ""])
    lines.extend(
        [
            "- Private trigger canon or deep trigger mechanics.",
            "- Schattenarchiv-depth material, personal logs or raw chat provenance.",
            "- Wallet, token, treasury or operational blockchain details.",
            "- Patent-sensitive mappings, unpublished claims or restricted IP context.",
            "- Any source file flagged as `private`, `token/wallet`, `patent/ip`, `trigger-depth` or `raw-chat` unless it has been explicitly redacted.",
        ]
    )

    lines.extend(["", "## Source Basis", ""])
    lines.extend(
        md_table(
            ["Role", "Internal source"],
            [
                ["Landing atlas", "Reviewed local atlas export, redacted source handle."],
                ["Mermaid manifesto", "Reviewed local Mermaid manifesto export, redacted source handle."],
                ["Diagram selection", "`docs/atlas/diagrams.md`"],
                ["Source manifest", "`docs/atlas/source_manifest.json`"],
                ["Semantic spine registry", "`docs/atlas/semantic_spine_registry.md`"],
            ],
        )
    )

    lines.extend(["", "## Next Public Artifact", ""])
    lines.append("Prepare a release/Zenodo metadata package from `docs/public/semantic_architecture_public_release_v0_1.md` after final metadata review.")

    return "\n".join(lines) + "\n"


def render_operator_map(artifacts: list[SourceArtifact], generated_at: str) -> str:
    payload = find_artifact(artifacts, "all-in-one bundle")
    landing = find_artifact(artifacts, "landing atlas")
    trigger_ref = find_artifact(artifacts, "trigger register")
    diagram_registry = find_artifact_by_title(artifacts, "Mermaid Code Library - Complete Collection") or find_artifact(
        artifacts,
        "diagram registry",
    )
    manifesto = find_artifact(artifacts, "mermaid manifesto")
    chat_source = find_artifact(artifacts, "chat provenance")
    research = find_artifact(artifacts, "research review")

    lines = [
        "# TerraNova Operator Map",
        "",
        "Status: internal routing map generated from the Prism source pack",
        "",
        f"Generated: {generated_at}",
        "",
        "## Purpose",
        "",
        "This file tells Codex, Prism and future agents which source to consult first",
        "for common TerraNova tasks. It is internal operating material, not a public",
        "landing page.",
        "",
        "## Routing Table",
        "",
    ]
    lines.extend(
        md_table(
            ["Intent", "First source", "Action", "Guard"],
            [
                ["Orient a new session", source_cell(landing), "Read atlas summary, then choose diagram or source lane.", "Keep raw exports as context, not truth."],
                ["Build or update diagrams", source_cell(diagram_registry), "Use ACTIVE rows from `docs/atlas/diagrams.md`.", "Do not revive LEGACY rows unless explicitly needed."],
                ["Prepare public copy", source_cell(manifesto), "Draft from public overview and selected diagrams.", "Redact sensitivity flags first."],
                ["Work on triggers", source_cell(trigger_ref), "Check `docs/triggers/gap_ledger.md` before adding or naming ranges.", "Open gaps stay open until sourced."],
                ["Investigate provenance", source_cell(chat_source), "Use as background only; extract reviewed claims separately.", "Raw chat cannot become canonical truth."],
                ["Archive source payload", source_cell(payload), "Preserve unchanged and derive curated docs from it.", "Do not edit raw source-pack files."],
                ["Review repository/IP context", source_cell(research), "Use as a review input for repo-facing claims.", "Verify against GitHub before treating as current state."],
            ],
        )
    )

    lines.extend(["", "## Agent Procedure", ""])
    lines.extend(
        [
            "1. Identify the user's intent and pick one routing row.",
            "2. Read the first source and any generated atlas file named in the row.",
            "3. Produce a reviewed extract or local diff.",
            "4. Keep external writes gated behind explicit user confirmation.",
            "5. Update generated atlas docs by re-running `scripts/render_prism_atlas.py`, not by hand-editing generated files.",
        ]
    )

    lines.extend(["", "## Output Targets", ""])
    lines.extend(
        md_table(
            ["Need", "Target"],
            [
                ["Human-facing atlas", "`docs/atlas/index.md`"],
                ["Public-facing slice", "`docs/atlas/public_overview.md`"],
                ["Internal routing", "`docs/atlas/operator_map.md`"],
                ["Diagram selection", "`docs/atlas/diagrams.md`"],
                ["Trigger gaps", "`docs/triggers/gap_ledger.md`"],
                ["Machine inventory", "`docs/atlas/source_inventory.csv` and `source_manifest.json`"],
            ],
        )
    )

    lines.extend(["", "## Mutation Boundary", ""])
    lines.extend(
        [
            "- Local docs and generated files can be updated as part of repository work.",
            "- Git commits, pushes, PR actions and connector writes need explicit user confirmation.",
            "- Notion remains source-of-record where explicitly defined; GitHub remains the reviewed engineering mirror.",
        ]
    )

    return "\n".join(lines) + "\n"


def render_trigger_gap_ledger(artifacts: list[SourceArtifact], generated_at: str) -> str:
    trigger_ref = find_artifact(artifacts, "trigger register")

    lines = [
        "# TerraNova Trigger Gap Ledger",
        "",
        "Status: generated internal gap ledger",
        "",
        f"Generated: {generated_at}",
        "",
        "## Source",
        "",
        f"Primary trigger source: {source_cell(trigger_ref)}",
        "",
        "## Rule",
        "",
        "Undocumented trigger ranges stay open. Do not infer missing triggers from",
        "nearby ranges, chat memory or naming patterns.",
        "",
        "## Range Ledger",
        "",
    ]
    lines.extend(
        md_table(
            ["Range", "Status", "Current read", "Next action"],
            [
                ["1-170", "documented", "Codex base trigger set is present in the source pack.", "Use as indexed reference."],
                ["171-505", "open / partial", "Source explicitly marks this as a known documentation gap with 335 undocumented triggers.", "Do not fill without reviewed source."],
                ["506-515", "open", "No stable assignment detected in the current source snapshot.", "Leave unassigned until a source appears."],
                ["516-523", "documented subset", "Core system triggers are visible in the source pack.", "Use internally; review before public mention."],
                ["540 / 544", "documented points", "Meta-reflection and decision triggers are visible.", "Use as routing markers only."],
                ["777", "sensitive", "Schattenarchiv variants are referenced.", "Keep internal; requires explicit review before any external use."],
                ["988-992", "documented sensitive", "MAXSync/security range is visible.", "Use for internal sync/security routing only."],
                ["Slash commands", "documented group", "Source reports roughly 20 workspace commands.", "Extract only when needed."],
                ["Codex Agentium", "documented group", "Source reports 7 multi-agent commands.", "Keep internal until reviewed."],
            ],
        )
    )

    lines.extend(["", "## Open Decisions", ""])
    lines.extend(
        [
            "- Whether 171-505 should be reconstructed from future Notion/Prism source or left intentionally sparse.",
            "- Whether 988-992 belongs in a public appendix or internal sync/security appendix only.",
            "- Whether trigger names in sensitive ranges need redaction labels before repository publication.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_inventory_csv(artifacts: list[SourceArtifact], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["title", "category", "type", "size_bytes", "sha256", "sensitivity", "source"])
        for artifact in sorted(artifacts, key=lambda item: item.rel_path.casefold()):
            writer.writerow(
                [
                    artifact.title,
                    artifact.category,
                    artifact.suffix,
                    artifact.size,
                    artifact.sha256,
                    ";".join(artifact.sensitivity),
                    artifact.rel_path,
                ]
            )


def write_manifest(
    artifacts: list[SourceArtifact],
    diagram_rows: list[dict[str, str]],
    source_dir: Path,
    output_path: Path,
    generated_at: str,
) -> None:
    data = {
        "generated_at": generated_at,
        "source_dir": repo_path(source_dir),
        "source_files": [
            {
                "title": artifact.title,
                "category": artifact.category,
                "type": artifact.suffix,
                "size_bytes": artifact.size,
                "sha256": artifact.sha256,
                "sensitivity": artifact.sensitivity,
                "source": artifact.rel_path,
                "headings": artifact.headings,
            }
            for artifact in artifacts
        ],
        "diagrams": diagram_rows,
    }
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render(source_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    trigger_dir = output_dir.parent / "triggers"
    trigger_dir.mkdir(parents=True, exist_ok=True)
    artifacts, diagrams, source_dir, generated_at = resolve_render_inputs(source_dir, output_dir)

    (output_dir / "index.md").write_text(
        render_index(artifacts, diagrams, source_dir, generated_at),
        encoding="utf-8",
    )
    (output_dir / "diagrams.md").write_text(
        render_diagrams(diagrams, generated_at),
        encoding="utf-8",
    )
    (output_dir / "public_overview.md").write_text(
        render_public_overview(artifacts, diagrams, generated_at),
        encoding="utf-8",
    )
    (output_dir / "operator_map.md").write_text(
        render_operator_map(artifacts, generated_at),
        encoding="utf-8",
    )
    (trigger_dir / "gap_ledger.md").write_text(
        render_trigger_gap_ledger(artifacts, generated_at),
        encoding="utf-8",
    )
    write_inventory_csv(artifacts, output_dir / "source_inventory.csv")
    write_manifest(artifacts, diagrams, source_dir, output_dir / "source_manifest.json", generated_at)

    print(f"Rendered {len(artifacts)} source files into {output_dir}")
    print(f"Diagram rows: {len(diagrams)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render TerraNova CIC atlas docs from historical Prism source exports.")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Directory containing historical Prism/Notion Markdown and CSV source exports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated atlas docs.",
    )
    args = parser.parse_args()
    render(args.source_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
