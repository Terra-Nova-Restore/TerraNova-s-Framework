#!/usr/bin/env python3
"""Build public-safe intake metrics for ChatGPT/Codex export sources.

The intake reads local export candidates and emits only file hashes, aggregate
counts, correlation axes and publication lanes. It does not print raw prompts,
messages, titles, local paths, account data or conversation IDs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


TEXT_EXTENSIONS = {".md", ".txt", ".tex", ".csv"}
BINARY_EXTENSIONS = {".docx", ".pdf", ".zip", ".har", ".gz", ".tar", ".exe"}

AXIS_RULES: dict[str, tuple[str, ...]] = {
    "chatgpt_export": ("chatgpt", "gpt", "codex", "openai", "prompt", "conversation"),
    "notion_workspace": ("notion", "workspace", "page", "database"),
    "control_tower": (
        "cap",
        "control tower",
        "equilibrium",
        "ora",
        "triquetra",
        "cic",
        "terranova",
        "ferrai",
    ),
    "trigger": ("trigger", "/fff", "sessionstart", "preflight", "scl"),
    "tokenomics": ("token", "dao", "wallet", "staking", "ferr", "license", "lizenz"),
    "mermaid": ("mermaid", "mmd", "graph", "flowchart", "diagram"),
    "patent_ip": ("patent", "tnpx", "ige", "schutz", "ip ", "intellectual property"),
    "metarotik": ("metarotik", "metaerotik", "erotik", "intim", "flutung", "körper", "koerper"),
    "prism_zenodo": ("prism", "zenodo", "latex", "doi", "monographie", "rc01"),
    "github_sync": ("github", "sync", "delta", "repository", "pull request", "pr-"),
}

AXIS_ORDER = [
    "chatgpt_export",
    "notion_workspace",
    "control_tower",
    "trigger",
    "tokenomics",
    "mermaid",
    "patent_ip",
    "metarotik",
    "prism_zenodo",
    "github_sync",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json" and any(part.lower() == "conversations" for part in path.parts):
        return "conversation_json"
    if suffix == ".json":
        return "json"
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if suffix in BINARY_EXTENSIONS:
        return "binary"
    return "other"


def iter_source_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.is_dir():
        return []

    files: list[Path] = []
    for candidate in sorted(path.rglob("*")):
        if not candidate.is_file():
            continue
        suffix = candidate.suffix.lower()
        if suffix == ".json" and any(part.lower() == "conversations" for part in candidate.parts):
            files.append(candidate)
        elif candidate.name.lower() in {"conversations.json", "chat.html"}:
            files.append(candidate)
    return files


def text_from_json(value: Any) -> str:
    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                if key.lower() in {"content", "text", "message", "title", "summary"}:
                    if isinstance(child, str):
                        parts.append(child)
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)
        elif isinstance(node, str):
            if len(node) > 20:
                parts.append(node)

    walk(value)
    return "\n".join(parts)


def read_public_scan_text(path: Path, data: bytes) -> tuple[str, int, int]:
    kind = file_type(path)
    if kind in {"conversation_json", "json"}:
        try:
            parsed = json.loads(data.decode("utf-8-sig", errors="replace"))
        except json.JSONDecodeError:
            return "", 0, 0
        text = text_from_json(parsed)
        message_count = text.lower().count("assistant") + text.lower().count("user")
        return text, message_count, len(text)
    if kind == "text":
        text = data.decode("utf-8-sig", errors="replace")
        return text, 0, len(text)
    return "", 0, 0


def classify_axes(text: str, path: Path) -> set[str]:
    scan = f"{path.suffix.lower()} {text[:250000]}".lower()
    axes = {"chatgpt_export"}
    for axis, needles in AXIS_RULES.items():
        if axis == "chatgpt_export":
            continue
        if any(needle in scan for needle in needles):
            axes.add(axis)
    return axes


def lane_for_axes(axes: set[str]) -> str:
    if "patent_ip" in axes:
        return "public_after_ip_review"
    if "tokenomics" in axes:
        return "public_after_biz_review"
    if "metarotik" in axes:
        return "public_after_phenomenology_review"
    if "trigger" in axes:
        return "trigger_correlation_candidate"
    if "mermaid" in axes:
        return "diagram_correlation_candidate"
    if "prism_zenodo" in axes:
        return "evidence_apparatus_candidate"
    if "github_sync" in axes:
        return "sync_trace_candidate"
    if "control_tower" in axes:
        return "control_tower_candidate"
    if "notion_workspace" in axes:
        return "notion_correlation_candidate"
    return "chat_export_index_candidate"


def gates_for_axes(axes: set[str]) -> list[str]:
    gates: list[str] = []
    if "patent_ip" in axes:
        gates.append("ip_review")
    if "tokenomics" in axes:
        gates.append("biz_tokenomics_review")
    if "metarotik" in axes:
        gates.append("phenomenology_metarotik_review")
    if "trigger" in axes:
        gates.append("trigger_source_review")
    if "mermaid" in axes:
        gates.append("mermaid_graph_review")
    if "prism_zenodo" in axes:
        gates.append("evidence_apparatus_review")
    if "github_sync" in axes:
        gates.append("sync_trace_review")
    if "notion_workspace" in axes:
        gates.append("notion_correlation_review")
    if "control_tower" in axes:
        gates.append("control_tower_review")
    return gates or ["chat_export_index_review"]


def parse_source(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise ValueError("source must use label=path form")
    label, path_text = raw.split("=", 1)
    label = re.sub(r"[^a-zA-Z0-9_.-]+", "_", label.strip()).strip("_")
    if not label:
        raise ValueError("source label is empty")
    return label, Path(path_text)


def analyze(sources: list[tuple[str, Path]]) -> dict[str, object]:
    file_rows: list[dict[str, object]] = []
    source_counter: dict[str, Counter[str]] = {}
    source_bytes: Counter[str] = Counter()
    source_hash_material: dict[str, list[str]] = {}
    axis_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()
    gate_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    total_bytes = 0
    total_scan_chars = 0
    total_message_markers = 0

    for source_index, (source_label, source_path) in enumerate(sources, start=1):
        source_handle = f"xport-src-{source_index:03d}"
        source_counter[source_handle] = Counter()
        source_hash_material[source_handle] = []
        files = iter_source_files(source_path)
        for file_index, path in enumerate(files, start=1):
            data = path.read_bytes()
            digest = sha256_bytes(data)
            kind = file_type(path)
            scan_text, message_markers, scan_chars = read_public_scan_text(path, data)
            axes = classify_axes(scan_text, path)
            lane = lane_for_axes(axes)
            gates = gates_for_axes(axes)
            file_handle = f"{source_handle}-file-{file_index:04d}"

            file_rows.append(
                {
                    "Source Handle": source_handle,
                    "Source Label": source_label,
                    "File Handle": file_handle,
                    "File Type": kind,
                    "Bytes": len(data),
                    "SHA-256": digest,
                    "Scan Chars": scan_chars,
                    "Message Markers": message_markers,
                    "Axes": ";".join(sorted(axes)),
                    "Publication Lane": lane,
                    "Review Gates": ";".join(gates),
                }
            )
            source_counter[source_handle][kind] += 1
            source_bytes[source_handle] += len(data)
            source_hash_material[source_handle].append(digest)
            type_counts[kind] += 1
            lane_counts[lane] += 1
            for gate in gates:
                gate_counts[gate] += 1
            for axis in axes:
                axis_counts[axis] += 1
            total_bytes += len(data)
            total_scan_chars += scan_chars
            total_message_markers += message_markers

    source_rows = []
    for source_index, (source_label, _source_path) in enumerate(sources, start=1):
        source_handle = f"xport-src-{source_index:03d}"
        material = "".join(sorted(source_hash_material[source_handle])).encode("ascii")
        source_rows.append(
            {
                "Source Handle": source_handle,
                "Source Label": source_label,
                "File Count": sum(source_counter[source_handle].values()),
                "Bytes": source_bytes[source_handle],
                "Conversation JSON": source_counter[source_handle].get("conversation_json", 0),
                "Text Files": source_counter[source_handle].get("text", 0),
                "Binary Files": source_counter[source_handle].get("binary", 0),
                "Source Hash": sha256_bytes(material) if material else "",
                "Path Published": "no",
            }
        )

    return {
        "batch": "CHATGPT-XPORT-001",
        "metrics": {
            "source_count": len(sources),
            "file_count": len(file_rows),
            "total_bytes": total_bytes,
            "total_scan_chars": total_scan_chars,
            "message_markers": total_message_markers,
            "axis_count": len(axis_counts),
            "publication_lane_count": len(lane_counts),
            "review_gate_count": len(gate_counts),
        },
        "source_rows": source_rows,
        "file_rows": file_rows,
        "axis_counts": dict(sorted(axis_counts.items())),
        "file_type_counts": dict(sorted(type_counts.items())),
        "publication_lanes": dict(sorted(lane_counts.items())),
        "review_gates": dict(sorted(gate_counts.items())),
        "redaction": {
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
        },
    }


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_count_csv(path: Path, key_name: str, rows: dict[str, int]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([key_name, "Count"])
        for key, count in sorted(rows.items()):
            writer.writerow([key, count])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, help="Source in label=path form.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    args = parser.parse_args(argv[1:])

    try:
        sources = [parse_source(raw) for raw in args.source]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    missing = [f"{label}={path}" for label, path in sources if not path.exists()]
    if missing:
        print("missing source(s):", file=sys.stderr)
        for item in missing:
            print(item, file=sys.stderr)
        return 2

    result = analyze(sources)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        output_dir / "chatgpt-xport-001.source-families.csv",
        result["source_rows"],
        [
            "Source Handle",
            "Source Label",
            "File Count",
            "Bytes",
            "Conversation JSON",
            "Text Files",
            "Binary Files",
            "Source Hash",
            "Path Published",
        ],
    )
    write_csv(
        output_dir / "chatgpt-xport-001.file-ledger.csv",
        result["file_rows"],
        [
            "Source Handle",
            "Source Label",
            "File Handle",
            "File Type",
            "Bytes",
            "SHA-256",
            "Scan Chars",
            "Message Markers",
            "Axes",
            "Publication Lane",
            "Review Gates",
        ],
    )
    write_count_csv(output_dir / "chatgpt-xport-001.axis-counts.csv", "Axis", result["axis_counts"])
    write_count_csv(
        output_dir / "chatgpt-xport-001.file-type-counts.csv",
        "File Type",
        result["file_type_counts"],
    )
    write_count_csv(
        output_dir / "chatgpt-xport-001.publication-lane-counts.csv",
        "Publication Lane",
        result["publication_lanes"],
    )
    write_count_csv(
        output_dir / "chatgpt-xport-001.review-gate-counts.csv",
        "Review Gate",
        result["review_gates"],
    )
    summary = {key: value for key, value in result.items() if key not in {"file_rows"}}
    (output_dir / "chatgpt-xport-001.review-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
