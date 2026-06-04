#!/usr/bin/env python3
"""Local dry-run controller for TerraNovaCIC self-extension.

The controller is intentionally dependency-free and side-effect limited. It
reads local-private source material, classifies it into lanes and emits reports
under an ignored local-private output directory. It does not call external
services or perform Git remote actions.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = Path("raw/exports/local-private")
DEFAULT_OUTPUT_DIR = Path("raw/exports/local-private/tnc-auto-001-dry-run")

LANE_PATTERNS: dict[str, list[str]] = {
    "github_governance": [
        r"\bgithub\b",
        r"\bPR\b",
        r"#77",
        r"\bbranch\b",
        r"\bcommit\b",
        r"\bpush\b",
        r"\bworkflow\b",
        r"\bCI\b",
    ],
    "notion_substrate": [
        r"\bnotion\b",
        r"\bworkspace\b",
        r"\bReflexions-Log\b",
        r"\bpage\b",
        r"\bdatabase\b",
        r"\bsource of record\b",
    ],
    "zenodo_publication": [
        r"\bzenodo\b",
        r"\bDOI\b",
        r"\brelease\b",
        r"\bpublication\b",
        r"\bpublikation\b",
    ],
    "gumroad_portal": [
        r"\bgumroad\b",
        r"\bportal\b",
        r"\bproduct\b",
        r"\bCTA\b",
        r"\bStripe\b",
        r"\bNetlify\b",
    ],
    "codex_internal": [
        r"\bcodex\b",
        r"\bTNC-AUTO-001\b",
        r"\bcontroller\b",
        r"\bVORTEX\b",
        r"\bSCL\b",
        r"\btrigger\b",
        r"\b777\b",
        r"\b601\b",
    ],
    "protected_ip_token": [
        r"\bTNPX\b",
        r"\bpatent\b",
        r"\bCAP-II\b",
        r"\bFERR\b",
        r"\btoken\b",
        r"\bPolygon\b",
        r"\bIPFS\b",
        r"\blicen[cs]e\b",
        r"\blizenz\b",
    ],
    "private_sensitive": [
        r"\bprivate\b",
        r"\bprivat\b",
        r"\bsurvival\b",
        r"\bMetarotik\b",
        r"\bSchattenarchiv\b",
        r"\bpersonal\b",
        r"\bintimate\b",
    ],
}

PUBLIC_BLOCKERS: dict[str, list[str]] = {
    "raw_private_export": [r"raw export", r"raw/exports/local-private", r"Gemini_unterhaltung"],
    "protected_ip": [r"\bTNPX\b", r"\bCAP-II\b", r"\bFERR\b", r"\btoken\b"],
    "private_sensitive": [r"\bprivate\b", r"\bprivat\b", r"\bsurvival\b", r"\bMetarotik\b"],
    "external_mutation": [r"\bpush\b", r"\bopen PR\b", r"\bStripe\b", r"\bNetlify\b", r"\bZenodo\b"],
}


@dataclass(frozen=True)
class SourceRecord:
    path: Path
    rel_path: str
    bytes: int
    lines: int
    sha256: str
    ignored_by_git: bool


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_check_ignored(root: Path, rel_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", rel_path],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def git_status(root: Path) -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return f"git status failed: {result.stderr.strip()}"
    return result.stdout.strip()


def iter_sources(source_dir: Path) -> list[Path]:
    if not source_dir.exists():
        return []
    return sorted(
        path
        for path in source_dir.glob("*.md")
        if path.name.startswith(("gemini-", "terra-nova", "tncic-"))
    )


def build_source_record(root: Path, path: Path) -> SourceRecord:
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    rel_path = path.relative_to(root).as_posix()
    return SourceRecord(
        path=path,
        rel_path=rel_path,
        bytes=len(data),
        lines=len(text.splitlines()),
        sha256=sha256_bytes(data),
        ignored_by_git=git_check_ignored(root, rel_path),
    )


def count_patterns(text: str, patterns: Iterable[str]) -> int:
    return sum(len(re.findall(pattern, text, flags=re.IGNORECASE)) for pattern in patterns)


def classify_text(text: str) -> dict[str, int]:
    counts = {lane: count_patterns(text, patterns) for lane, patterns in LANE_PATTERNS.items()}
    if not any(counts.values()):
        counts["residue_unknown"] = 1
    return counts


def boundary_counts(text: str) -> dict[str, int]:
    return {risk: count_patterns(text, patterns) for risk, patterns in PUBLIC_BLOCKERS.items()}


def highest_lane(counts: dict[str, int]) -> str:
    non_zero = {lane: value for lane, value in counts.items() if value > 0}
    if not non_zero:
        return "residue_unknown"
    return max(non_zero.items(), key=lambda item: item[1])[0]


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_source_manifest(output_dir: Path, records: list[SourceRecord]) -> None:
    write_json(
        output_dir / "source_manifest.json",
        [
            {
                "path": record.rel_path,
                "bytes": record.bytes,
                "lines": record.lines,
                "sha256": record.sha256,
                "ignored_by_git": record.ignored_by_git,
            }
            for record in records
        ],
    )


def write_claim_ledger(output_dir: Path, root: Path, records: list[SourceRecord]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in records:
        text = record.path.read_text(encoding="utf-8", errors="replace")
        lane_counts = classify_text(text)
        risk_counts = boundary_counts(text)
        rows.append(
            {
                "source": record.rel_path,
                "primary_lane": highest_lane(lane_counts),
                "lane_counts": json.dumps(lane_counts, sort_keys=True),
                "risk_counts": json.dumps(risk_counts, sort_keys=True),
                "public_safe": "false" if any(risk_counts.values()) else "true",
                "action": "report_only",
            }
        )

    with (output_dir / "claim_ledger.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source", "primary_lane", "lane_counts", "risk_counts", "public_safe", "action"],
        )
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_model_vote_matrix(output_dir: Path) -> None:
    rows = [
        {
            "instance": "Codex",
            "role": "local executor",
            "vote": "build local-only dry-run controller",
            "authority": "local facts, git, tests, diffs",
        },
        {
            "instance": "GPT",
            "role": "governance reviewer",
            "vote": "concordance closure before implementation",
            "authority": "scope, boundary, risk",
        },
        {
            "instance": "Gemini",
            "role": "long-context verifier",
            "vote": "local anchor and validation loop",
            "authority": "breadth and contradiction review",
        },
        {
            "instance": "Notion Grok",
            "role": "workspace distiller",
            "vote": "Notion substrate and self-extension spec",
            "authority": "Notion context, requires verification",
        },
    ]
    with (output_dir / "model_vote_matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["instance", "role", "vote", "authority"])
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_reports(output_dir: Path, rows: list[dict[str, object]], status: str) -> dict[str, object]:
    risk_sources = [row for row in rows if row["public_safe"] == "false"]
    commit_safe = False
    report = {
        "run_id": "TNC-AUTO-001-2026-06-04",
        "mode": "LOCAL_ONLY/DRY_RUN_CONTROLLER",
        "external_mutation_count": 0,
        "sources": len(rows),
        "risk_sources": len(risk_sources),
        "commit_safe": commit_safe,
        "git_status": status,
    }

    (output_dir / "contradiction_ledger.md").write_text(
        "# Contradiction Ledger\n\n"
        "Status: dry-run only.\n\n"
        "- Grok and Gemini are more permissive about automation expansion.\n"
        "- GPT and Codex require a local-only controller before implementation.\n"
        "- Resolution: local-only dry-run MVP; no external mutation.\n",
        encoding="utf-8",
    )
    (output_dir / "boundary_report.md").write_text(
        "# Boundary Report\n\n"
        "External mutation count: 0\n\n"
        "Public-safe default: deny until source-backed and boundary-cleared.\n\n"
        "Risk-bearing source count: "
        f"{len(risk_sources)}\n\n"
        "Blocked lanes: raw private exports, protected IP/token/business, private "
        "survival or Metarotik material, payment and production surfaces.\n",
        encoding="utf-8",
    )
    (output_dir / "risk_report.md").write_text(
        "# Risk Report\n\n"
        "| Risk | Control |\n"
        "| --- | --- |\n"
        "| Raw private material leaks into public docs | Keep outputs local-private; boundary report required |\n"
        "| Notion claims treated as Git truth | Verify through source-of-record before any tracked diff |\n"
        "| External mutation without explicit GO | Default deny; human gate required |\n"
        "| Existing dirty branch contamination | Use clean worktree; report git status |\n"
        "| Premature commit | commit_safe remains false for first dry-run |\n",
        encoding="utf-8",
    )
    (output_dir / "proposed_changes.md").write_text(
        "# Proposed Changes\n\n"
        "Dry-run proposal only:\n\n"
        "1. Keep TNC-AUTO-001 local-only until ledgers are reviewed.\n"
        "2. Add tracked controller files only after dry-run validation.\n"
        "3. Defer PR creation to AUTO-PR-001 after explicit gate.\n"
        "4. Do not alter #77, CAP, Control Tower, Notion, Zenodo, token/IP or portal lanes in this MVP.\n",
        encoding="utf-8",
    )
    (output_dir / "next_gate.md").write_text(
        "# Next Gate\n\n"
        "Recommended next command after review:\n\n"
        "```text\n"
        "REVIEW_TNC_AUTO_001_DRY_RUN\n"
        "```\n\n"
        "Commit is not recommended until a human reviews the dry-run outputs and "
        "explicitly approves a tracked implementation commit.\n",
        encoding="utf-8",
    )
    write_json(output_dir / "dry_run_report.json", report)
    return report


def run_controller(root: Path, source_dir: Path, output_dir: Path) -> dict[str, object]:
    abs_source_dir = (root / source_dir).resolve()
    abs_output_dir = (root / output_dir).resolve()
    abs_output_dir.mkdir(parents=True, exist_ok=True)

    records = [build_source_record(root, path) for path in iter_sources(abs_source_dir)]
    write_source_manifest(abs_output_dir, records)
    rows = write_claim_ledger(abs_output_dir, root, records)
    write_model_vote_matrix(abs_output_dir)
    status = git_status(root)
    report = write_markdown_reports(abs_output_dir, rows, status)
    return {"output_dir": abs_output_dir.as_posix(), **report}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the TNC-AUTO-001 local dry-run controller.")
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR.as_posix())
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR.as_posix())
    parser.add_argument("--json", action="store_true", help="Print the final report as JSON.")
    args = parser.parse_args(argv[1:])

    result = run_controller(REPO_ROOT, Path(args.source_dir), Path(args.output_dir))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"[tnc-auto-001] output_dir={result['output_dir']}")
        print(f"[tnc-auto-001] commit_safe={result['commit_safe']}")
        print("[tnc-auto-001] external_mutation_count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
