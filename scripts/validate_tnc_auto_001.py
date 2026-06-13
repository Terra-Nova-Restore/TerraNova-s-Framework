#!/usr/bin/env python3
"""Validate the TNC-AUTO-001 dry-run controller and reports."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ".codex/tnc-auto-001.yaml",
    ".codex/lane_registry.yaml",
    ".codex/safety_policy.yaml",
    "scripts/tnc_auto_001.py",
    "docs/governance/tnc_auto_001_dry_run_policy.md",
]
REQUIRED_OUTPUTS = [
    "source_manifest.json",
    "claim_ledger.csv",
    "model_vote_matrix.csv",
    "contradiction_ledger.md",
    "boundary_report.md",
    "risk_report.md",
    "proposed_changes.md",
    "next_gate.md",
    "dry_run_report.json",
]
OUTPUT_DIR = Path("raw/exports/local-private/tnc-auto-001-dry-run")
LOCAL_LEXICON_PATH = Path("raw/exports/local-private/tnc-auto-001/lane_lexicon.local.json")
BLOCKED_NETWORK_MODULES = {"requests", "urllib", "http.client"}


def error(message: str) -> None:
    print(f"[validate-tnc-auto-001] ERROR: {message}", file=sys.stderr)


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate_no_network_imports() -> list[str]:
    path = REPO_ROOT / "scripts" / "tnc_auto_001.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if is_blocked_network_module(alias.name):
                    found.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if is_blocked_network_module(node.module):
                found.append(node.module)
    return found


def is_blocked_network_module(module: str) -> bool:
    return any(module == blocked or module.startswith(f"{blocked}.") for blocked in BLOCKED_NETWORK_MODULES)


def git_ls_files(paths: list[str]) -> list[str]:
    args = ["git", "ls-files"]
    if paths:
        args.extend(["--", *paths])
    result = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line]


def validate_tracked_public_deny_terms() -> list[str]:
    path = REPO_ROOT / LOCAL_LEXICON_PATH
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ["local lexicon root must be an object"]

    terms = payload.get("tracked_public_deny_terms", [])
    scan_paths = payload.get("tracked_public_deny_paths", [])
    if not isinstance(terms, list) or not all(isinstance(item, str) for item in terms):
        return ["local lexicon tracked_public_deny_terms must be a string list"]
    if not isinstance(scan_paths, list) or not all(isinstance(item, str) for item in scan_paths):
        return ["local lexicon tracked_public_deny_paths must be a string list"]

    findings: list[str] = []
    for rel in git_ls_files(scan_paths):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8", errors="replace")
        if any(term and term in text for term in terms):
            findings.append(f"tracked public deny term found in scoped file: {rel}")
    return findings


def ensure_dry_run_outputs() -> list[str]:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/tnc_auto_001.py",
            "--output-dir",
            OUTPUT_DIR.as_posix(),
            "--lexicon",
            LOCAL_LEXICON_PATH.as_posix(),
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        return [f"dry-run controller failed while preparing validation outputs: {details}"]
    return []


def main(argv: list[str]) -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    safety_text = (REPO_ROOT / ".codex" / "safety_policy.yaml").read_text(encoding="utf-8")
    for required in [
        "default_external_mutation: deny",
        "default_git_remote_mutation: deny",
        "default_notion_mutation: deny",
        "external_mutation_count_zero",
    ]:
        if required not in safety_text:
            errors.append(f"safety policy missing: {required}")

    output_rel = OUTPUT_DIR.as_posix()
    if not git_check_ignore(output_rel):
        errors.append(f"output directory is not gitignored: {output_rel}")

    errors.extend(ensure_dry_run_outputs())

    for rel in REQUIRED_OUTPUTS:
        output = REPO_ROOT / OUTPUT_DIR / rel
        if not output.exists():
            errors.append(f"missing dry-run output: {OUTPUT_DIR / rel}")

    report_path = REPO_ROOT / OUTPUT_DIR / "dry_run_report.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("external_mutation_count") != 0:
            errors.append("external_mutation_count is not zero")
        if report.get("commit_safe") is not False:
            errors.append("first dry-run must report commit_safe=false")

    network_imports = validate_no_network_imports()
    if network_imports:
        errors.append(f"network imports are not allowed: {', '.join(network_imports)}")

    deny_findings = validate_tracked_public_deny_terms()
    errors.extend(deny_findings)

    if errors:
        for item in errors:
            error(item)
        return 1

    print("[validate-tnc-auto-001] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
