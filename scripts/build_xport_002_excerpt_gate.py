#!/usr/bin/env python3
"""Build XPORT-002 private excerpt-context gate artifacts.

This pass reads local raw sample files to classify whether XPORT-002 sample
signals are direct definition-context candidates or only numeric/name
correlation. Outputs remain public-safe: no raw prompts, messages, titles,
local paths, conversation IDs or account data are emitted.
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
BATCH = "XPORT-002-EXCERPT-GATE-001"
TODAY = "2026-05-23"
CREATED_AT = "2026-05-23T16:30:00+02:00"


CONTEXT_RADIUS = 1800
SOURCE_ANCHORS = (
    "trigger",
    "definition",
    "definitionen",
    "definiert",
    "modul",
    "module",
    "triggerexport",
    "codex139",
    "silvimodus",
    "tnpx",
    "canon",
    "kanon",
)
CAPII_ANCHORS = (
    "cap-ii",
    "cap ii",
    "revoke",
    "license",
    "lizenz",
    "tokenomics",
    "token",
    "dao",
    "wallet",
    "tnpx",
    "patent",
    "ige",
)
STOPWORDS = {
    "und",
    "oder",
    "der",
    "die",
    "das",
    "ein",
    "eine",
    "einen",
    "einem",
    "als",
    "zur",
    "zum",
    "fuer",
    "für",
    "mit",
    "von",
    "den",
    "dem",
    "des",
    "bei",
    "im",
    "in",
    "ins",
    "ist",
    "sich",
    "nicht",
    "oder",
    "um",
    "zu",
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
                if key.lower() in {"content", "text", "message", "title", "summary"} and isinstance(child, str):
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


def trigger_rows_174_210() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(OUT / "trigger-map-001.seed.csv"):
        ref = row.get("trigger_ref", "")
        if ref.isdigit() and 174 <= int(ref) <= 210:
            rows.append(row)
    return sorted(rows, key=lambda row: int(row["trigger_ref"]))


def definition_terms(definition: str) -> set[str]:
    normalized = definition.lower().replace("oe", "ö").replace("ue", "ü").replace("ae", "ä")
    tokens = re.findall(r"[a-zäöüß0-9_-]{4,}", normalized)
    return {token for token in tokens if token not in STOPWORDS}


def name_patterns(name: str) -> list[str]:
    forms = {name.lower()}
    forms.add(name.lower().replace("Ue", "Ü").replace("ue", "ü").replace("Ae", "Ä").replace("ae", "ä"))
    forms.add(name.lower().replace("Ü", "Ue").replace("ü", "ue").replace("Ä", "Ae").replace("ä", "ae"))
    return sorted(forms)


def exact_name_positions(text_lower: str, name: str) -> list[int]:
    positions: list[int] = []
    for form in name_patterns(name):
        start = 0
        while True:
            index = text_lower.find(form, start)
            if index == -1:
                break
            positions.append(index)
            start = index + max(1, len(form))
    return sorted(set(positions))


def number_hit_count(text_lower: str, ref: str) -> int:
    return len(re.findall(rf"(?<!\d){re.escape(ref)}(?!\d)", text_lower))


def anchor_count(window_lower: str, anchors: tuple[str, ...]) -> int:
    return sum(1 for anchor in anchors if anchor in window_lower)


def max_context_score(text_lower: str, name: str, definition: str, ref: str) -> dict[str, object]:
    positions = exact_name_positions(text_lower, name)
    terms = definition_terms(definition)
    best = {
        "name_hits": len(positions),
        "number_hits": number_hit_count(text_lower, ref),
        "definition_term_overlap": 0,
        "definition_term_total": len(terms),
        "source_anchor_count": 0,
        "capii_anchor_count": 0,
        "strongest_window_chars": 0,
    }
    for position in positions:
        left = max(0, position - CONTEXT_RADIUS)
        right = min(len(text_lower), position + CONTEXT_RADIUS)
        window = text_lower[left:right]
        overlap = sum(1 for term in terms if term in window)
        source_count = anchor_count(window, SOURCE_ANCHORS)
        capii_count = anchor_count(window, CAPII_ANCHORS)
        score = (overlap * 3) + (source_count * 2) + capii_count
        best_score = (
            int(best["definition_term_overlap"]) * 3
            + int(best["source_anchor_count"]) * 2
            + int(best["capii_anchor_count"])
        )
        if score > best_score:
            best.update(
                {
                    "definition_term_overlap": overlap,
                    "source_anchor_count": source_count,
                    "capii_anchor_count": capii_count,
                    "strongest_window_chars": right - left,
                }
            )
    return best


def classify_gate(row: dict[str, str], score: dict[str, object]) -> tuple[str, str, str]:
    name_hits = int(score["name_hits"])
    number_hits = int(score["number_hits"])
    overlap = int(score["definition_term_overlap"])
    source_anchors = int(score["source_anchor_count"])
    capii_anchors = int(score["capii_anchor_count"])
    ref = int(row["trigger_ref"])

    if name_hits and overlap >= 3 and source_anchors >= 2:
        decision = "excerpt_context_supports_definition_candidate"
        confidence = "high_context_candidate"
        next_action = "Promote to private source-review shortlist; still no raw excerpt publication."
    elif name_hits and source_anchors:
        decision = "excerpt_context_supports_name_candidate"
        confidence = "medium_context_candidate"
        next_action = "Manual private excerpt reading before any direct source claim."
    elif name_hits:
        decision = "name_seen_context_weak"
        confidence = "low_context_candidate"
        next_action = "Treat as correlation unless a human validates the surrounding raw context."
    elif number_hits:
        decision = "numeric_context_only"
        confidence = "low_numeric_signal"
        next_action = "Do not use as source evidence without exact raw context validation."
    else:
        decision = "not_observed_in_sample"
        confidence = "no_sample_signal"
        next_action = "Use Codex139+ Notion source only; XPORT sample does not add evidence here."

    if 205 <= ref <= 210 and capii_anchors:
        next_action = f"{next_action} CAP-II/tokenomics/IP review remains mandatory."
    return decision, confidence, next_action


def build_gate_rows(
    sample_rows: list[dict[str, str]], resolved: dict[str, list[tuple[Path, bytes]]]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    triggers = trigger_rows_174_210()
    per_context_rows: list[dict[str, object]] = []
    per_trigger_best: dict[str, dict[str, object]] = {}

    for sample in sample_rows:
        sample_handle = sample["Sample Handle"]
        matches = resolved[sample_handle]
        if not matches:
            text_lower = ""
        else:
            text_lower = read_scan_text(matches[0][0], matches[0][1]).lower()
        for trigger in triggers:
            score = max_context_score(
                text_lower,
                trigger["working_name"],
                trigger["public_safe_definition"],
                trigger["trigger_ref"],
            )
            decision, confidence, next_action = classify_gate(trigger, score)
            if decision == "not_observed_in_sample":
                continue
            row = {
                "Sample Handle": sample_handle,
                "Review Focus": sample["Review Focus"],
                "Trigger Ref": trigger["trigger_ref"],
                "Working Name": trigger["working_name"],
                "Name Hits": score["name_hits"],
                "Number Hits": score["number_hits"],
                "Definition Term Overlap": score["definition_term_overlap"],
                "Definition Term Total": score["definition_term_total"],
                "Source Anchor Count": score["source_anchor_count"],
                "CAPII Anchor Count": score["capii_anchor_count"],
                "Strongest Window Chars": score["strongest_window_chars"],
                "Excerpt Gate Decision": decision,
                "Confidence": confidence,
                "Allowed Use Now": "Private source-review routing and count-only public-safe evidence classification.",
                "Blocked Use Now": "No raw excerpt, no title, no local path, no conversation ID, no public canon, no TRG assignment.",
                "Next Action": next_action,
            }
            per_context_rows.append(row)

            current = per_trigger_best.get(trigger["trigger_ref"])
            candidate_rank = decision_rank(decision)
            current_rank = decision_rank(str(current["Excerpt Gate Decision"])) if current else -1
            if current is None or candidate_rank > current_rank:
                per_trigger_best[trigger["trigger_ref"]] = row

    best_rows = [
        {
            "Trigger Ref": ref,
            "Working Name": row["Working Name"],
            "Best Sample Handle": row["Sample Handle"],
            "Best Review Focus": row["Review Focus"],
            "Best Decision": row["Excerpt Gate Decision"],
            "Best Confidence": row["Confidence"],
            "Name Hits": row["Name Hits"],
            "Number Hits": row["Number Hits"],
            "Definition Term Overlap": row["Definition Term Overlap"],
            "Source Anchor Count": row["Source Anchor Count"],
            "CAPII Anchor Count": row["CAPII Anchor Count"],
            "Allowed Use Now": row["Allowed Use Now"],
            "Blocked Use Now": row["Blocked Use Now"],
            "Next Action": row["Next Action"],
        }
        for ref, row in sorted(per_trigger_best.items(), key=lambda item: int(item[0]))
    ]
    return per_context_rows, best_rows


def decision_rank(decision: str) -> int:
    return {
        "not_observed_in_sample": 0,
        "numeric_context_only": 1,
        "name_seen_context_weak": 2,
        "excerpt_context_supports_name_candidate": 3,
        "excerpt_context_supports_definition_candidate": 4,
    }.get(decision, 0)


def build_review_gates(best_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    decision_counts = Counter(str(row["Best Decision"]) for row in best_rows)
    definition_count = decision_counts["excerpt_context_supports_definition_candidate"]
    name_count = decision_counts["excerpt_context_supports_name_candidate"]
    numeric_count = decision_counts["numeric_context_only"]
    return [
        {
            "Gate ID": "XPORT2-EXCERPT-G001",
            "Gate": "Private raw context read",
            "Status": "completed_count_only",
            "Evidence": "Local raw windows were read by script; only classification counts were emitted.",
            "Blocks Until Cleared": "Raw excerpt publication and human-readable quote use remain blocked.",
        },
        {
            "Gate ID": "XPORT2-EXCERPT-G002",
            "Gate": "Definition-context candidate promotion",
            "Status": "candidate" if definition_count else "not_met",
            "Evidence": f"{definition_count} triggers have name, definition-token and source-anchor support.",
            "Blocks Until Cleared": "Direct claim that XPORT-002 defines a trigger without private human confirmation.",
        },
        {
            "Gate ID": "XPORT2-EXCERPT-G003",
            "Gate": "Name-context candidate promotion",
            "Status": "candidate" if name_count else "not_met",
            "Evidence": f"{name_count} triggers have name and source-anchor support without full definition-token threshold.",
            "Blocks Until Cleared": "Public source-evidence claim for these rows.",
        },
        {
            "Gate ID": "XPORT2-EXCERPT-G004",
            "Gate": "Numeric-only context",
            "Status": "requires_manual_rejection_or_confirmation" if numeric_count else "not_applicable",
            "Evidence": f"{numeric_count} triggers remain numeric-only in selected samples.",
            "Blocks Until Cleared": "Any numeric-only trigger-source claim.",
        },
        {
            "Gate ID": "XPORT2-EXCERPT-G005",
            "Gate": "CAP-II/tokenomics/IP wording",
            "Status": "pending",
            "Evidence": "205-210 can be routed through XPORT context, but CAP-II/tokenomics/IP public wording is not cleared.",
            "Blocks Until Cleared": "CAP-II, Revoke, license, tokenomics, TNPX-01 or IP-facing public claim.",
        },
        {
            "Gate ID": "XPORT2-EXCERPT-G006",
            "Gate": "Public canon / TRG assignment",
            "Status": "blocked",
            "Evidence": "Excerpt context classification is not an L3/L4 contract.",
            "Blocks Until Cleared": "Canonical TRG assignment, activation semantics or public trigger canon promotion.",
        },
    ]


def build_summary(
    sample_rows: list[dict[str, str]],
    resolved: dict[str, list[tuple[Path, bytes]]],
    context_rows: list[dict[str, object]],
    best_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
) -> dict[str, object]:
    best_decisions = Counter(str(row["Best Decision"]) for row in best_rows)
    gate_status = Counter(str(row["Status"]) for row in gate_rows)
    sample_focus = Counter(row["Review Focus"] for row in sample_rows)
    return {
        "batch": BATCH,
        "status": "private_excerpt_context_gate_completed",
        "created_at": CREATED_AT,
        "inputs": {
            "review_samples": "chatgpt-xport-002.review-samples.csv",
            "sample_corridor": "xport-002.sample-corridor.review.csv",
            "trigger_seed": "trigger-map-001.seed.csv",
            "local_source_roots": "provided at runtime; not published",
        },
        "sample_count": len(sample_rows),
        "local_hash_match_count": sum(len(matches) for matches in resolved.values()),
        "sample_focus_counts": dict(sorted(sample_focus.items())),
        "context_row_count": len(context_rows),
        "best_trigger_row_count": len(best_rows),
        "best_decision_counts": dict(sorted(best_decisions.items())),
        "gate_status_counts": dict(sorted(gate_status.items())),
        "boundaries": {
            "raw_messages_printed": False,
            "raw_titles_printed": False,
            "raw_excerpts_printed": False,
            "local_paths_printed": False,
            "conversation_ids_printed": False,
            "account_data_printed": False,
            "notion_write_performed": False,
            "git_push_performed": False,
            "pr_opened": False,
            "commit_created": False,
        },
        "decision": (
            "Private excerpt-context gate can route direct candidates into SOURCE-174-210 review, "
            "but public canon, raw excerpts, TRG assignment and tokenomics/IP wording remain blocked."
        ),
    }


def build_batch_markdown(summary: dict[str, object]) -> str:
    decisions = summary["best_decision_counts"]
    gates = summary["gate_status_counts"]
    return f"""# {BATCH} - Private excerpt-context gate

Status: completed as public-safe classification artifacts
Created: {TODAY}
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This pass performs the agreed private excerpt-context review for the
`XPORT-002` sample corridor. It reads local raw windows to classify whether
sample hits are definition-context candidates, name-context candidates or only
numeric correlation.

It does not publish raw prompts, raw messages, raw excerpts, titles, local
paths, conversation IDs or account data.

## Result

| Item | Value |
| --- | ---: |
| XPORT-002 samples | `{summary["sample_count"]}` |
| Local hash matches | `{summary["local_hash_match_count"]}` |
| Context rows | `{summary["context_row_count"]}` |
| Best trigger rows | `{summary["best_trigger_row_count"]}` |

## Best Trigger Decisions

| Decision | Count |
| --- | ---: |
| `excerpt_context_supports_definition_candidate` | `{decisions.get("excerpt_context_supports_definition_candidate", 0)}` |
| `excerpt_context_supports_name_candidate` | `{decisions.get("excerpt_context_supports_name_candidate", 0)}` |
| `name_seen_context_weak` | `{decisions.get("name_seen_context_weak", 0)}` |
| `numeric_context_only` | `{decisions.get("numeric_context_only", 0)}` |

## Gate State

| Status | Count |
| --- | ---: |
| `completed_count_only` | `{gates.get("completed_count_only", 0)}` |
| `candidate` | `{gates.get("candidate", 0)}` |
| `requires_manual_rejection_or_confirmation` | `{gates.get("requires_manual_rejection_or_confirmation", 0)}` |
| `pending` | `{gates.get("pending", 0)}` |
| `blocked` | `{gates.get("blocked", 0)}` |

## Decision

The gate can route direct candidates into `SOURCE-174-210`, but it does not
clear public canon, raw excerpt publication, canonical `TRG-*` assignment,
activation semantics or CAP-II/tokenomics/IP wording.

## Artifacts

| File | Role |
| --- | --- |
| `xport-002.excerpt-gate.context-review.csv` | Per sample/trigger context classification, count-only. |
| `xport-002.excerpt-gate.best-trigger-review.csv` | Best public-safe XPORT evidence class per trigger. |
| `xport-002.excerpt-gate.gates.csv` | Gates before source promotion, public wording or canon assignment. |
| `xport-002.excerpt-gate.review-summary.json` | Machine-readable gate summary and boundary flags. |
| `causal-log.xport-002-excerpt-gate-001-2026-05-23.json` | Causal trace for this private excerpt gate. |

## Boundary

- No raw excerpts printed.
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
        "log_id": "CAP-LOG-2026-05-23-XPORT-002-EXCERPT-GATE-001",
        "created_at": CREATED_AT,
        "operator": "Codex / FerrAI",
        "mode": "STUDIO",
        "activation": "/fff",
        "source_trace": [
            "chatgpt-xport-002.review-samples.csv",
            "xport-002.sample-corridor.review.csv",
            "trigger-map-001.seed.csv",
            "local raw export roots provided at runtime; paths withheld",
        ],
        "observation": "Private raw context can classify trigger signals without publishing raw excerpts.",
        "trigger_band": "201-300",
        "trigger_ids": ["174-210", "205-210", "/fff"],
        "probabilistic_hypothesis": "XPORT-002 can strengthen SOURCE-174-210 routing, but remains below public canon until human source promotion.",
        "probability_note": "High confidence for count-only context classes; public wording remains blocked by no-raw-excerpt and CAP-II/IP gates.",
        "deterministic_boundary": "No raw excerpts, no paths, no conversation IDs, no external mutation, no commit, no push and no PR.",
        "selected_action": "Create private excerpt-context gate artifacts with public-safe classification only.",
        "feedback_target": "trigger_map",
        "backpropagation_result": "Direct XPORT candidates can be routed into SOURCE-174-210; public canon and CAP-II/tokenomics/IP claims remain blocked.",
        "verification_state": "repo_checked",
        "external_mutation": False,
        "mutation_authorization": "",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", action="append", required=True, help="Local source root to scan.")
    args = parser.parse_args(argv[1:])

    source_roots = [Path(raw) for raw in args.source_root]
    if any(not path.exists() for path in source_roots):
        print("missing source root(s); paths withheld in artifacts", file=sys.stderr)
        return 2

    sample_rows = read_csv(OUT / "chatgpt-xport-002.review-samples.csv")
    resolved = resolve_sample_files(sample_rows, source_roots)
    context_rows, best_rows = build_gate_rows(sample_rows, resolved)
    gate_rows = build_review_gates(best_rows)
    summary = build_summary(sample_rows, resolved, context_rows, best_rows, gate_rows)

    write_csv(
        OUT / "xport-002.excerpt-gate.context-review.csv",
        [
            "Sample Handle",
            "Review Focus",
            "Trigger Ref",
            "Working Name",
            "Name Hits",
            "Number Hits",
            "Definition Term Overlap",
            "Definition Term Total",
            "Source Anchor Count",
            "CAPII Anchor Count",
            "Strongest Window Chars",
            "Excerpt Gate Decision",
            "Confidence",
            "Allowed Use Now",
            "Blocked Use Now",
            "Next Action",
        ],
        context_rows,
    )
    write_csv(
        OUT / "xport-002.excerpt-gate.best-trigger-review.csv",
        [
            "Trigger Ref",
            "Working Name",
            "Best Sample Handle",
            "Best Review Focus",
            "Best Decision",
            "Best Confidence",
            "Name Hits",
            "Number Hits",
            "Definition Term Overlap",
            "Source Anchor Count",
            "CAPII Anchor Count",
            "Allowed Use Now",
            "Blocked Use Now",
            "Next Action",
        ],
        best_rows,
    )
    write_csv(
        OUT / "xport-002.excerpt-gate.gates.csv",
        ["Gate ID", "Gate", "Status", "Evidence", "Blocks Until Cleared"],
        gate_rows,
    )
    write_json(OUT / "xport-002.excerpt-gate.review-summary.json", summary)
    write_json(OUT / "causal-log.xport-002-excerpt-gate-001-2026-05-23.json", build_causal_log())
    write_text(OUT / "batch-xport-002-excerpt-gate-001.md", build_batch_markdown(summary))
    print(
        json.dumps(
            {
                "context_row_count": summary["context_row_count"],
                "best_decision_counts": summary["best_decision_counts"],
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
