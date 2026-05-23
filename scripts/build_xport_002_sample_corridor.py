#!/usr/bin/env python3
"""Review XPORT-002 sample corridors against local raw files.

The script resolves selected XPORT-002 sample hashes inside explicit local
source roots, verifies file integrity, scans for public-safe trigger/tokenomics
signals, and emits only handles, counts, gates and review decisions. It never
prints raw prompts, messages, titles, local paths, conversation IDs or account
data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "atlas" / "control-tower"
BATCH = "XPORT-002-SAMPLE-CORRIDOR"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T16:17:52+02:00"


TERM_GROUPS: dict[str, tuple[str, ...]] = {
    "trigger_core": ("trigger", "trg", "/fff", "modul", "module", "canon", "kanon"),
    "cap_ii_tokenomics": (
        "cap-ii",
        "cap ii",
        "revoke",
        "license",
        "lizenz",
        "lizenzierung",
        "tokenomics",
        "token",
        "dao",
        "wallet",
        "staking",
        "ferr",
    ),
    "tnpx_patent_ip": (
        "tnpx",
        "patent",
        "ige",
        "intellectual property",
        "schutzrecht",
        "ip review",
        " ip ",
    ),
    "metarotik": ("metarotik", "metaerotik", "erotik", "intim", "flutung", "koerper", "körper"),
    "mermaid_graph": ("mermaid", "mmd", "flowchart", "diagram", "graph"),
    "control_tower": ("control tower", "equilibrium", "triquetra", "ora", "cic", "terranova", "ferrai"),
    "notion_workspace": ("notion", "workspace", "database", "page", "registry"),
    "source_governance": ("source", "evidence", "review", "public", "internal", "protected", "redaction"),
}


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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_from_json(value: Any) -> str:
    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                key_lower = key.lower()
                if key_lower in {"content", "text", "message", "title", "summary"} and isinstance(child, str):
                    parts.append(child)
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)
        elif isinstance(node, str) and len(node) > 20:
            parts.append(node)

    walk(value)
    return "\n".join(parts)


def read_scan_text(path: Path, data: bytes) -> str:
    if path.suffix.lower() == ".json":
        try:
            return text_from_json(json.loads(data.decode("utf-8-sig", errors="replace")))
        except json.JSONDecodeError:
            return ""
    if path.suffix.lower() in {".txt", ".md", ".csv", ".tex"}:
        return data.decode("utf-8-sig", errors="replace")
    return ""


def iter_candidate_files(source_roots: list[Path], target_sizes: set[int]) -> list[Path]:
    candidates: list[Path] = []
    for root in source_roots:
        if not root.exists():
            continue
        if root.is_file():
            if root.stat().st_size in target_sizes:
                candidates.append(root)
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            try:
                if path.stat().st_size in target_sizes:
                    candidates.append(path)
            except OSError:
                continue
    return sorted(candidates)


def resolve_sample_files(
    sample_rows: list[dict[str, str]], source_roots: list[Path]
) -> dict[str, list[tuple[Path, bytes]]]:
    size_to_samples: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in sample_rows:
        size_to_samples[int(row["Bytes"])].append(row)

    resolved: dict[str, list[tuple[Path, bytes]]] = {row["Sample Handle"]: [] for row in sample_rows}
    for path in iter_candidate_files(source_roots, set(size_to_samples)):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        digest = sha256_bytes(data)
        for row in size_to_samples.get(len(data), []):
            if digest == row["SHA-256"]:
                resolved[row["Sample Handle"]].append((path, data))
    return resolved


def count_term(text_lower: str, term: str) -> int:
    if term.strip() != term:
        return text_lower.count(term)
    pattern = re.compile(rf"(?<![a-z0-9_-]){re.escape(term)}(?![a-z0-9_-])", re.IGNORECASE)
    return len(pattern.findall(text_lower))


def public_signal_counts(text: str) -> dict[str, int]:
    text_lower = f" {text.lower()} "
    return {
        group: sum(count_term(text_lower, term.lower()) for term in terms)
        for group, terms in TERM_GROUPS.items()
    }


def trigger_rows_174_210() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(OUT / "trigger-map-001.seed.csv"):
        ref = row.get("trigger_ref", "")
        if ref.isdigit() and 174 <= int(ref) <= 210:
            rows.append(row)
    return sorted(rows, key=lambda row: int(row["trigger_ref"]))


def trigger_hits(text: str, triggers: list[dict[str, str]]) -> tuple[dict[str, int], dict[str, int]]:
    text_lower = f" {text.lower()} "
    number_hits: dict[str, int] = {}
    name_hits: dict[str, int] = {}
    for row in triggers:
        ref = row["trigger_ref"]
        name = row["working_name"]
        number_hits[ref] = len(re.findall(rf"(?<!\d){re.escape(ref)}(?!\d)", text_lower))
        name_hits[ref] = text_lower.count(name.lower())
    return number_hits, name_hits


def classify_decision(sample_row: dict[str, str], number_hit_sum: int, name_hit_sum: int) -> tuple[str, str]:
    focus = sample_row["Review Focus"]
    if name_hit_sum:
        return (
            "direct_trigger_name_evidence_candidate",
            "May support targeted per-trigger source review after manual excerpt validation.",
        )
    if number_hit_sum:
        return (
            "numeric_trigger_signal_only",
            "Use only as correlation signal; numeric hits need manual context review before any source claim.",
        )
    if focus == "tokenomics_trigger_shared":
        return (
            "axis_corridor_for_cap_ii_tokenomics",
            "Use as CAP-II/tokenomics/IP review corridor, not as direct 174-210 semantic evidence.",
        )
    if focus == "trigger_only":
        return (
            "axis_corridor_for_trigger_review",
            "Use as trigger review corridor, not as direct 174-210 semantic evidence unless excerpts validate it.",
        )
    return (
        "context_only",
        "Use as tokenomics or surrounding context only; no direct trigger-source claim.",
    )


def build_review(
    sample_rows: list[dict[str, str]], resolved: dict[str, list[tuple[Path, bytes]]]
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    triggers = trigger_rows_174_210()
    sample_review_rows: list[dict[str, object]] = []
    term_signal_rows: list[dict[str, object]] = []
    trigger_signal_rows: list[dict[str, object]] = []

    for row in sample_rows:
        sample = row["Sample Handle"]
        matches = resolved[sample]
        representative_data = matches[0][1] if matches else b""
        representative_path = matches[0][0] if matches else Path("")
        text = read_scan_text(representative_path, representative_data) if matches else ""
        text_chars = len(text)
        term_counts = public_signal_counts(text)
        number_counts, name_counts = trigger_hits(text, triggers)
        number_hits = {ref: count for ref, count in number_counts.items() if count}
        name_hits = {ref: count for ref, count in name_counts.items() if count}
        number_hit_sum = sum(number_hits.values())
        name_hit_sum = sum(name_hits.values())
        decision, allowed_use = classify_decision(row, number_hit_sum, name_hit_sum)

        sample_review_rows.append(
            {
                "Sample Handle": sample,
                "Review Focus": row["Review Focus"],
                "Priority": row["Priority"],
                "Representative File Handle": row["Representative File Handle"],
                "SHA-256": row["SHA-256"],
                "Expected Bytes": row["Bytes"],
                "Local Hash Matches": len(matches),
                "Integrity Status": "sha256_verified" if matches else "missing_local_raw",
                "Scan Text Chars": text_chars,
                "Trigger Number Hit Count": number_hit_sum,
                "Trigger Name Hit Count": name_hit_sum,
                "Matched Trigger Refs": ";".join(sorted(set(number_hits) | set(name_hits), key=int)),
                "Matched Trigger Name Refs": ";".join(sorted(name_hits, key=int)),
                "Term Signal Total": sum(term_counts.values()),
                "Review Decision": decision,
                "Allowed Use Now": allowed_use,
                "Blocked Use Now": (
                    "No raw excerpt publication, no public canon promotion, no canonical TRG assignment, "
                    "no tokenomics/IP claim and no external mutation."
                ),
                "Next Action": (
                    "Manual excerpt validation inside private/raw workspace before promoting any sample from "
                    "corridor evidence to source evidence."
                ),
            }
        )

        for group, count in sorted(term_counts.items()):
            term_signal_rows.append(
                {
                    "Sample Handle": sample,
                    "Review Focus": row["Review Focus"],
                    "Signal Group": group,
                    "Signal Count": count,
                    "Public Meaning": "count-only signal; not raw evidence",
                }
            )

        for trigger in triggers:
            ref = trigger["trigger_ref"]
            if number_counts[ref] or name_counts[ref]:
                trigger_signal_rows.append(
                    {
                        "Sample Handle": sample,
                        "Review Focus": row["Review Focus"],
                        "Trigger Ref": ref,
                        "Working Name": trigger["working_name"],
                        "Number Hit Count": number_counts[ref],
                        "Name Hit Count": name_counts[ref],
                        "Evidence Class": (
                            "name_and_number_signal"
                            if name_counts[ref] and number_counts[ref]
                            else "name_signal"
                            if name_counts[ref]
                            else "number_signal"
                        ),
                        "Public Meaning": "signal only until raw excerpt context is reviewed privately",
                    }
                )

    return sample_review_rows, term_signal_rows, trigger_signal_rows


def build_gate_rows(sample_review_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    direct_name_samples = [row["Sample Handle"] for row in sample_review_rows if row["Trigger Name Hit Count"]]
    numeric_samples = [row["Sample Handle"] for row in sample_review_rows if row["Trigger Number Hit Count"]]
    return [
        {
            "Gate ID": "XPORT2-CORR-G001",
            "Gate": "Local raw hash integrity",
            "Status": "passed" if all(row["Local Hash Matches"] for row in sample_review_rows) else "failed",
            "Evidence": "All selected sample handles resolve to local files with matching SHA-256."
            if all(row["Local Hash Matches"] for row in sample_review_rows)
            else "At least one sample handle did not resolve locally.",
            "Blocks Until Cleared": "Any XPORT-002 raw review claim.",
        },
        {
            "Gate ID": "XPORT2-CORR-G002",
            "Gate": "Raw excerpt publication",
            "Status": "blocked",
            "Evidence": "This pass emits counts only; no prompt, message, title, path or conversation ID is printed.",
            "Blocks Until Cleared": "Public quote, raw title, raw message or local path publication.",
        },
        {
            "Gate ID": "XPORT2-CORR-G003",
            "Gate": "Direct 174-210 trigger-name evidence",
            "Status": "candidate" if direct_name_samples else "not_found_in_sample_corridor",
            "Evidence": ";".join(direct_name_samples) if direct_name_samples else "No exact 174-210 working-name hit in selected samples.",
            "Blocks Until Cleared": "Claim that XPORT-002 directly defines any 174-210 trigger.",
        },
        {
            "Gate ID": "XPORT2-CORR-G004",
            "Gate": "Numeric trigger context",
            "Status": "requires_private_context_review" if numeric_samples else "not_found_in_sample_corridor",
            "Evidence": ";".join(numeric_samples) if numeric_samples else "No 174-210 numeric hit in selected samples.",
            "Blocks Until Cleared": "Use of numeric hits as per-trigger evidence.",
        },
        {
            "Gate ID": "XPORT2-CORR-G005",
            "Gate": "CAP-II/tokenomics/IP public wording",
            "Status": "pending",
            "Evidence": "P1 shared samples remain protected corridors for 205-210, tokenomics, business and IP review.",
            "Blocks Until Cleared": "Any CAP-II, Revoke, license, tokenomics or TNPX-01 public claim.",
        },
        {
            "Gate ID": "XPORT2-CORR-G006",
            "Gate": "SOURCE-174-210 promotion",
            "Status": "blocked",
            "Evidence": "A hash/sample corridor is not a canon contract or activation protocol.",
            "Blocks Until Cleared": "L3/L4 canon admission, canonical TRG assignment or activation semantics.",
        },
    ]


def build_summary(
    sample_rows: list[dict[str, str]],
    sample_review_rows: list[dict[str, object]],
    term_signal_rows: list[dict[str, object]],
    trigger_signal_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
) -> dict[str, object]:
    focus_counts = Counter(row["Review Focus"] for row in sample_rows)
    decision_counts = Counter(str(row["Review Decision"]) for row in sample_review_rows)
    gate_counts = Counter(str(row["Status"]) for row in gate_rows)
    signal_counts: Counter[str] = Counter()
    for row in term_signal_rows:
        signal_counts[str(row["Signal Group"])] += int(row["Signal Count"])

    return {
        "batch": BATCH,
        "status": "local_raw_sample_corridor_review",
        "created_at": CREATED_AT,
        "inputs": {
            "review_samples": "chatgpt-xport-002.review-samples.csv",
            "trigger_seed": "trigger-map-001.seed.csv",
            "local_source_roots": "provided at runtime; not published",
        },
        "sample_count": len(sample_rows),
        "local_hash_match_count": sum(int(row["Local Hash Matches"]) for row in sample_review_rows),
        "sample_focus_counts": dict(sorted(focus_counts.items())),
        "review_decision_counts": dict(sorted(decision_counts.items())),
        "term_signal_counts": dict(sorted(signal_counts.items())),
        "trigger_signal_row_count": len(trigger_signal_rows),
        "gate_status_counts": dict(sorted(gate_counts.items())),
        "boundaries": {
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
            "XPORT-002 is verified as a local raw hash corridor. It remains corridor evidence "
            "unless private excerpt review confirms direct trigger definitions."
        ),
    }


def build_batch_markdown(summary: dict[str, object], gate_rows: list[dict[str, object]]) -> str:
    focus_counts = summary["sample_focus_counts"]
    decision_counts = summary["review_decision_counts"]
    gate_counts = summary["gate_status_counts"]
    return f"""# {BATCH} - Raw sample corridor review

Status: local raw review completed as public-safe count artifacts
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This pass checks whether the `CHATGPT-XPORT-002` review samples still resolve
to local raw files and what kind of public-safe signal they carry for
`SOURCE-174-210`.

It does not publish raw prompts, messages, titles, local paths, conversation IDs
or account data. It also does not promote any trigger to public canon.

## Scope

| Item | Value |
| --- | ---: |
| XPORT-002 samples | `{summary["sample_count"]}` |
| Local hash matches | `{summary["local_hash_match_count"]}` |
| Trigger signal rows | `{summary["trigger_signal_row_count"]}` |
| Tokenomics-trigger shared samples | `{focus_counts.get("tokenomics_trigger_shared", 0)}` |
| Trigger-only samples | `{focus_counts.get("trigger_only", 0)}` |
| Tokenomics-only samples | `{focus_counts.get("tokenomics_only", 0)}` |

## Review Decisions

| Decision | Count |
| --- | ---: |
| `axis_corridor_for_cap_ii_tokenomics` | `{decision_counts.get("axis_corridor_for_cap_ii_tokenomics", 0)}` |
| `axis_corridor_for_trigger_review` | `{decision_counts.get("axis_corridor_for_trigger_review", 0)}` |
| `context_only` | `{decision_counts.get("context_only", 0)}` |
| `numeric_trigger_signal_only` | `{decision_counts.get("numeric_trigger_signal_only", 0)}` |
| `direct_trigger_name_evidence_candidate` | `{decision_counts.get("direct_trigger_name_evidence_candidate", 0)}` |

## Gate State

| Status | Count |
| --- | ---: |
| `passed` | `{gate_counts.get("passed", 0)}` |
| `blocked` | `{gate_counts.get("blocked", 0)}` |
| `pending` | `{gate_counts.get("pending", 0)}` |
| `candidate` | `{gate_counts.get("candidate", 0)}` |
| `not_found_in_sample_corridor` | `{gate_counts.get("not_found_in_sample_corridor", 0)}` |
| `requires_private_context_review` | `{gate_counts.get("requires_private_context_review", 0)}` |

## Decision

`XPORT-002` is verified as a local raw hash corridor. It is useful for review
routing, especially for `205-210` CAP-II/tokenomics/IP gates and general
trigger correlation. It is not yet direct source authority for public trigger
canon unless private excerpt review validates the exact context.

## Artifacts

| File | Role |
| --- | --- |
| `xport-002.sample-corridor.review.csv` | Per-sample integrity, signal and allowed-use decision. |
| `xport-002.sample-corridor.term-signals.csv` | Count-only signal groups per sample. |
| `xport-002.sample-corridor.trigger-signals.csv` | Count-only `174-210` number/name signals. |
| `xport-002.sample-corridor.gates.csv` | Gates before source promotion, public wording or mutation. |
| `xport-002.sample-corridor.review-summary.json` | Machine-readable summary and boundary flags. |
| `causal-log.xport-002-sample-corridor-2026-05-23.json` | Causal trace for this raw corridor review. |

## Boundary

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
        "log_id": "CAP-LOG-2026-05-23-XPORT-002-SAMPLE-CORRIDOR",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "chatgpt-xport-002.review-samples.csv",
            "trigger-map-001.seed.csv",
            "local raw export roots provided at runtime; paths withheld",
        ],
        "observation": "XPORT-002 sample handles can be checked against local raw files by SHA-256 without publishing raw content.",
        "trigger_band": "201-300",
        "trigger_ids": ["174-210", "205-210", "/fff"],
        "probabilistic_hypothesis": "XPORT-002 is currently strongest as a review corridor, not direct public trigger canon evidence.",
        "probability_note": "High confidence for hash integrity; lower confidence for direct trigger definition evidence until private excerpt context is reviewed.",
        "deterministic_boundary": "No raw content, no local paths, no conversation IDs, no external mutation, no commit, no push and no PR.",
        "selected_action": "Create public-safe XPORT-002 sample corridor review artifacts with count-only signal rows.",
        "feedback_target": "trigger_map",
        "backpropagation_result": "SOURCE-174-210 can use XPORT-002 for review routing; direct evidence promotion remains blocked by private excerpt review.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", action="append", required=True, help="Local source root to scan.")
    args = parser.parse_args(argv[1:])

    source_roots = [Path(raw) for raw in args.source_root]
    missing = [str(path) for path in source_roots if not path.exists()]
    if missing:
        print("missing source root(s); paths withheld in artifacts", file=sys.stderr)
        return 2

    sample_rows = read_csv(OUT / "chatgpt-xport-002.review-samples.csv")
    resolved = resolve_sample_files(sample_rows, source_roots)
    sample_review_rows, term_signal_rows, trigger_signal_rows = build_review(sample_rows, resolved)
    gate_rows = build_gate_rows(sample_review_rows)
    summary = build_summary(sample_rows, sample_review_rows, term_signal_rows, trigger_signal_rows, gate_rows)

    write_csv(
        OUT / "xport-002.sample-corridor.review.csv",
        [
            "Sample Handle",
            "Review Focus",
            "Priority",
            "Representative File Handle",
            "SHA-256",
            "Expected Bytes",
            "Local Hash Matches",
            "Integrity Status",
            "Scan Text Chars",
            "Trigger Number Hit Count",
            "Trigger Name Hit Count",
            "Matched Trigger Refs",
            "Matched Trigger Name Refs",
            "Term Signal Total",
            "Review Decision",
            "Allowed Use Now",
            "Blocked Use Now",
            "Next Action",
        ],
        sample_review_rows,
    )
    write_csv(
        OUT / "xport-002.sample-corridor.term-signals.csv",
        ["Sample Handle", "Review Focus", "Signal Group", "Signal Count", "Public Meaning"],
        term_signal_rows,
    )
    write_csv(
        OUT / "xport-002.sample-corridor.trigger-signals.csv",
        [
            "Sample Handle",
            "Review Focus",
            "Trigger Ref",
            "Working Name",
            "Number Hit Count",
            "Name Hit Count",
            "Evidence Class",
            "Public Meaning",
        ],
        trigger_signal_rows,
    )
    write_csv(
        OUT / "xport-002.sample-corridor.gates.csv",
        ["Gate ID", "Gate", "Status", "Evidence", "Blocks Until Cleared"],
        gate_rows,
    )
    write_json(OUT / "xport-002.sample-corridor.review-summary.json", summary)
    write_json(OUT / "causal-log.xport-002-sample-corridor-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-xport-002-sample-corridor.md", build_batch_markdown(summary, gate_rows))
    print(json.dumps({k: summary[k] for k in ("sample_count", "local_hash_match_count", "review_decision_counts")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
