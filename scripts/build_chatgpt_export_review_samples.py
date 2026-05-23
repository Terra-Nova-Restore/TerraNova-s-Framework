#!/usr/bin/env python3
"""Build CHATGPT-XPORT-002 dedupe and review-sample artifacts.

The follow-up package preserves correlation while collapsing obvious duplicate
source families and file hashes from CHATGPT-XPORT-001. Outputs remain
public-safe: no raw prompts, messages, titles, local paths or conversation IDs.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SAMPLE_LIMITS = {
    "tokenomics_trigger_shared": 6,
    "tokenomics_only": 3,
    "trigger_only": 3,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def split_items(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def axis_count(value: str) -> int:
    return len(split_items(value))


def int_field(row: dict[str, str], field: str) -> int:
    return int(row[field])


def classify_focus(axes: list[str]) -> str | None:
    has_tokenomics = "tokenomics" in axes
    has_trigger = "trigger" in axes
    if has_tokenomics and has_trigger:
        return "tokenomics_trigger_shared"
    if has_tokenomics:
        return "tokenomics_only"
    if has_trigger:
        return "trigger_only"
    return None


def representative_row(group: list[dict[str, str]]) -> dict[str, str]:
    return sorted(
        group,
        key=lambda row: (
            axis_count(row["Axes"]),
            int_field(row, "Message Markers"),
            int_field(row, "Bytes"),
            row["File Handle"],
        ),
        reverse=True,
    )[0]


def build_source_dedupe_rows(source_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        groups[row["Source Hash"]].append(row)

    dedupe_rows: list[dict[str, object]] = []
    sorted_groups = sorted(groups.values(), key=lambda group: group[0]["Source Handle"])
    for index, group in enumerate(sorted_groups, start=1):
        group = sorted(group, key=lambda row: row["Source Handle"])
        canonical = group[0]
        aliases = [row["Source Handle"] for row in group[1:]]
        dedupe_rows.append(
            {
                "Dedupe Family": f"xport2-family-{index:03d}",
                "Canonical Source Handle": canonical["Source Handle"],
                "Canonical Source Label": canonical["Source Label"],
                "Alias Source Handles": ";".join(aliases),
                "Source Labels": ";".join(row["Source Label"] for row in group),
                "Source Hash": canonical["Source Hash"],
                "Source Copies": len(group),
                "Nominal File Count": sum(int_field(row, "File Count") for row in group),
                "Canonical File Count": int_field(canonical, "File Count"),
                "Nominal Bytes": sum(int_field(row, "Bytes") for row in group),
                "Canonical Bytes": int_field(canonical, "Bytes"),
                "Conversation JSON": sum(int_field(row, "Conversation JSON") for row in group),
                "Text Files": sum(int_field(row, "Text Files") for row in group),
                "Binary Files": sum(int_field(row, "Binary Files") for row in group),
                "Path Published": canonical["Path Published"],
                "Dedupe Status": "alias-collapsed" if aliases else "canonical-only",
            }
        )
    return dedupe_rows


def build_hash_groups(
    file_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in file_rows:
        groups[row["SHA-256"]].append(row)

    hash_rows: list[dict[str, object]] = []
    unique_candidates: list[dict[str, object]] = []
    duplicate_file_rows = 0
    sorted_groups = sorted(groups.items(), key=lambda item: representative_row(item[1])["File Handle"])
    for index, (digest, group) in enumerate(sorted_groups, start=1):
        group = sorted(group, key=lambda row: row["File Handle"])
        rep = representative_row(group)
        axes = split_items(rep["Axes"])
        gates = split_items(rep["Review Gates"])
        file_count = len(group)
        if file_count > 1:
            duplicate_file_rows += file_count - 1

        hash_rows.append(
            {
                "Hash Group": f"xport2-hashgrp-{index:03d}",
                "Representative File Handle": rep["File Handle"],
                "Source Handles": ";".join(sorted({row["Source Handle"] for row in group})),
                "SHA-256": digest,
                "File Copies": file_count,
                "Bytes": int_field(rep, "Bytes"),
                "Message Markers": int_field(rep, "Message Markers"),
                "Axis Count": len(axes),
                "Axes": ";".join(axes),
                "Publication Lane": rep["Publication Lane"],
                "Review Gates": ";".join(gates),
                "File Handles": ";".join(row["File Handle"] for row in group),
            }
        )

        unique_candidates.append(
            {
                "hash_group": f"xport2-hashgrp-{index:03d}",
                "representative_file_handle": rep["File Handle"],
                "source_handles": ";".join(sorted({row["Source Handle"] for row in group})),
                "sha256": digest,
                "file_copies": file_count,
                "bytes": int_field(rep, "Bytes"),
                "message_markers": int_field(rep, "Message Markers"),
                "axis_count": len(axes),
                "axes": axes,
                "publication_lane": rep["Publication Lane"],
                "review_gates": gates,
            }
        )

    stats = {
        "unique_file_hash_count": len(unique_candidates),
        "duplicate_hash_group_count": sum(1 for row in hash_rows if int(row["File Copies"]) > 1),
        "duplicate_file_rows": duplicate_file_rows,
    }
    return hash_rows, unique_candidates, stats


def sample_sort_key(candidate: dict[str, object]) -> tuple[int, int, int, int, str]:
    return (
        int(candidate["axis_count"]),
        int(candidate["message_markers"]),
        int(candidate["bytes"]),
        int(candidate["file_copies"]),
        str(candidate["representative_file_handle"]),
    )


def build_review_samples(unique_candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    buckets: dict[str, list[dict[str, object]]] = {
        "tokenomics_trigger_shared": [],
        "tokenomics_only": [],
        "trigger_only": [],
    }
    for candidate in unique_candidates:
        focus = classify_focus(candidate["axes"])
        if focus is not None:
            buckets[focus].append(candidate)

    for focus in buckets:
        buckets[focus] = sorted(buckets[focus], key=sample_sort_key, reverse=True)

    sample_rows: list[dict[str, object]] = []
    sample_index = 1
    for focus in ("tokenomics_trigger_shared", "tokenomics_only", "trigger_only"):
        limit = SAMPLE_LIMITS[focus]
        priority = "P1" if focus == "tokenomics_trigger_shared" else "P2"
        label = focus.replace("_", " ")
        for rank, candidate in enumerate(buckets[focus][:limit], start=1):
            sample_rows.append(
                {
                    "Sample Handle": f"xport2-sample-{sample_index:03d}",
                    "Priority": priority,
                    "Review Focus": focus,
                    "Focus Rank": rank,
                    "Hash Group": candidate["hash_group"],
                    "Representative File Handle": candidate["representative_file_handle"],
                    "Source Handles": candidate["source_handles"],
                    "SHA-256": candidate["sha256"],
                    "File Copies": int(candidate["file_copies"]),
                    "Bytes": int(candidate["bytes"]),
                    "Message Markers": int(candidate["message_markers"]),
                    "Axis Count": int(candidate["axis_count"]),
                    "Axes": ";".join(candidate["axes"]),
                    "Publication Lane": candidate["publication_lane"],
                    "Review Gates": ";".join(candidate["review_gates"]),
                    "Selection Reason": (
                        f"{label} anchor with {candidate['axis_count']} axes, "
                        f"{candidate['message_markers']} message markers and "
                        f"{candidate['file_copies']} deduped file copy/copies."
                    ),
                }
            )
            sample_index += 1
    return sample_rows


def build_summary(
    source_rows: list[dict[str, str]],
    dedupe_rows: list[dict[str, object]],
    file_rows: list[dict[str, str]],
    hash_rows: list[dict[str, object]],
    hash_stats: dict[str, int],
    sample_rows: list[dict[str, object]],
) -> dict[str, object]:
    sample_focus_counts: dict[str, int] = defaultdict(int)
    for row in sample_rows:
        sample_focus_counts[str(row["Review Focus"])] += 1

    alias_groups = [
        {
            "dedupe_family": row["Dedupe Family"],
            "canonical_source_handle": row["Canonical Source Handle"],
            "alias_source_handles": row["Alias Source Handles"],
            "source_labels": row["Source Labels"],
            "source_hash": row["Source Hash"],
        }
        for row in dedupe_rows
        if row["Alias Source Handles"]
    ]

    return {
        "batch": "CHATGPT-XPORT-002",
        "inputs": {
            "source_batch": "CHATGPT-XPORT-001",
            "raw_source_count": len(source_rows),
            "raw_file_count": len(file_rows),
        },
        "dedupe": {
            "canonical_source_family_count": len(dedupe_rows),
            "collapsed_alias_source_count": len(source_rows) - len(dedupe_rows),
            "duplicate_hash_group_count": hash_stats["duplicate_hash_group_count"],
            "duplicate_file_rows": hash_stats["duplicate_file_rows"],
            "unique_file_hash_count": hash_stats["unique_file_hash_count"],
        },
        "review_corridor": {
            "sample_count": len(sample_rows),
            "sample_focus_counts": dict(sorted(sample_focus_counts.items())),
        },
        "alias_groups": alias_groups,
        "selected_samples": [
            {
                "sample_handle": row["Sample Handle"],
                "review_focus": row["Review Focus"],
                "representative_file_handle": row["Representative File Handle"],
                "sha256": row["SHA-256"],
                "axis_count": row["Axis Count"],
                "message_markers": row["Message Markers"],
                "file_copies": row["File Copies"],
            }
            for row in sample_rows
        ],
        "boundaries": {
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
        },
    }


def render_batch_markdown(summary: dict[str, object], sample_rows: list[dict[str, object]]) -> str:
    dedupe = summary["dedupe"]
    corridor = summary["review_corridor"]
    alias_groups = summary["alias_groups"]
    sample_focus_counts = corridor["sample_focus_counts"]

    alias_lines = []
    if alias_groups:
        alias_lines.append("| Canonical | Aliases | Hash |")
        alias_lines.append("| --- | --- | --- |")
        for group in alias_groups:
            alias_lines.append(
                f"| `{group['canonical_source_handle']}` | "
                f"`{group['alias_source_handles']}` | "
                f"`{group['source_hash']}` |"
            )
    else:
        alias_lines.append("No alias source families were collapsed.")

    sample_lines = ["| Sample | Focus | File | Axes | Markers | Copies |", "| --- | --- | --- | ---: | ---: | ---: |"]
    for row in sample_rows:
        sample_lines.append(
            f"| `{row['Sample Handle']}` | `{row['Review Focus']}` | "
            f"`{row['Representative File Handle']}` | {row['Axis Count']} | "
            f"{row['Message Markers']} | {row['File Copies']} |"
        )

    focus_lines = []
    for focus, count in sample_focus_counts.items():
        focus_lines.append(f"- `{focus}`: {count}")

    return "\n".join(
        [
            "# CHATGPT-XPORT-002 - Dedupe and Review Samples",
            "",
            "Status: STUDIO / repo-local correlation hardening",
            "Source: CHATGPT-XPORT-001 public-safe ledgers",
            "Trace: CHATGPT-XPORT-002",
            "Boundary: Dedupe families, duplicate hash groups and review samples only. "
            "No raw prompts, messages, titles, local paths, conversation IDs, account data or third-party identities are published.",
            "Mode: STUDIO",
            "GitHub sync state: Prepared locally by script; no push or PR performed by this batch.",
            "Notion source awareness: Notion remains the primary workspace corpus; ChatGPT exports stay a second correlation layer.",
            "",
            "## Decision",
            "",
            "CHATGPT-XPORT-002 keeps correlation and removes only obvious duplicate surfaces.",
            "",
            "Equivalent TXT/Markdown mirrors remain visible as aliases instead of being deleted from the evidence corridor.",
            "Repeated file hashes are grouped before trigger/tokenomics review, so the next pass does not re-read the same content twice.",
            "",
            "## Dedupe Result",
            "",
            f"- Raw source families: `{summary['inputs']['raw_source_count']}`",
            f"- Canonical source families after hash collapse: `{dedupe['canonical_source_family_count']}`",
            f"- Collapsed alias source copies: `{dedupe['collapsed_alias_source_count']}`",
            f"- Unique file hashes: `{dedupe['unique_file_hash_count']}`",
            f"- Duplicate hash groups: `{dedupe['duplicate_hash_group_count']}`",
            f"- Duplicate file rows removed from repeat-review: `{dedupe['duplicate_file_rows']}`",
            "",
            "## Alias Families",
            "",
            *alias_lines,
            "",
            "## Review Corridor",
            "",
            *focus_lines,
            "",
            *sample_lines,
            "",
            "## Next",
            "",
            "Best next action: `TRIGGER-MAP-001`.",
            "",
            "Goal: use the selected sample corridor to start trigger/module and tokenomics source mapping without breaking the correlation chain.",
        ]
    )


def build_causal_log(output_names: list[str]) -> dict[str, object]:
    return {
        "trace": "CHATGPT-XPORT-002",
        "date": "2026-05-23",
        "status": "completed",
        "mode": "STUDIO",
        "source": [
            "CHATGPT-XPORT-001",
            "local ChatGPT/Codex export ledgers",
            "Control Tower relation-preservation rule",
        ],
        "decision": [
            "Collapsed only hash-identical source families.",
            "Grouped duplicate file hashes before review sampling.",
            "Selected tokenomics/trigger review samples from deduped hash groups.",
        ],
        "boundary": {
            "raw_prompts": "excluded",
            "raw_messages": "excluded",
            "titles": "excluded",
            "local_paths": "excluded",
            "conversation_ids": "excluded",
            "account_data": "excluded",
        },
        "outputs": output_names,
        "next": "TRIGGER-MAP-001",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/atlas/control-tower"),
        help="Directory containing CHATGPT-XPORT-001 inputs and XPORT-002 outputs.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    source_path = output_dir / "chatgpt-xport-001.source-families.csv"
    file_path = output_dir / "chatgpt-xport-001.file-ledger.csv"
    source_rows = read_csv(source_path)
    file_rows = read_csv(file_path)

    dedupe_rows = build_source_dedupe_rows(source_rows)
    hash_rows, unique_candidates, hash_stats = build_hash_groups(file_rows)
    sample_rows = build_review_samples(unique_candidates)
    summary = build_summary(source_rows, dedupe_rows, file_rows, hash_rows, hash_stats, sample_rows)

    source_dedupe_name = "chatgpt-xport-002.source-dedupe.csv"
    hash_groups_name = "chatgpt-xport-002.hash-groups.csv"
    review_samples_name = "chatgpt-xport-002.review-samples.csv"
    review_summary_name = "chatgpt-xport-002.review-summary.json"
    batch_name = "batch-chatgpt-xport-002.md"
    causal_log_name = "causal-log.chatgpt-xport-002-2026-05-23.json"

    write_csv(output_dir / source_dedupe_name, list(dedupe_rows[0].keys()), dedupe_rows)
    write_csv(output_dir / hash_groups_name, list(hash_rows[0].keys()), hash_rows)
    write_csv(output_dir / review_samples_name, list(sample_rows[0].keys()), sample_rows)
    write_text(output_dir / review_summary_name, json.dumps(summary, indent=2))
    write_text(output_dir / batch_name, render_batch_markdown(summary, sample_rows))

    output_names = [
        batch_name,
        source_dedupe_name,
        hash_groups_name,
        review_samples_name,
        review_summary_name,
    ]
    causal_log = build_causal_log(output_names)
    write_text(output_dir / causal_log_name, json.dumps(causal_log, indent=2))

    print(json.dumps(summary["dedupe"], indent=2))
    print(json.dumps(summary["review_corridor"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
