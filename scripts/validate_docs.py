#!/usr/bin/env python3
"""Validate BIZ-grade TerraNova/FerrAI documentation markers.

The check is intentionally small and dependency-free. It enforces the Codex
boot contract without turning GitHub into a second Notion rulebook.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [
    "BIZ.md",
    "docs/architecture/ferrAI_operating_kernel_v0.1.md",
    "docs/codex",
    "docs/governance",
]
REQUIRED_TERMS = {
    "Status": re.compile(r"(?im)^\s*(?:[-*]\s*)?Status\s*:"),
    "Source": re.compile(r"(?im)^\s*(?:[-*]\s*)?Source\s*:"),
    "Trace": re.compile(r"(?im)^\s*(?:[-*]\s*)?Trace\s*:"),
    "Boundary": re.compile(r"(?im)^\s*(?:[-*]\s*)?Boundary\s*:"),
    "Mode": re.compile(r"(?im)^\s*(?:[-*]\s*)?Mode\s*:"),
    "GitHub sync state": re.compile(r"(?im)^\s*(?:[-*]\s*)?GitHub sync state\s*:"),
    "Notion source awareness": re.compile(r"(?im)^\s*(?:[-*]\s*)?Notion source awareness\s*:"),
}
BIZ_MARKER = re.compile(r"(?im)^\s*Status\s*:\s*.*\bBIZ\b|`/biz`|# .*BIZ")


def fail(message: str) -> None:
    print(f"[validate-docs] ERROR: {message}", file=sys.stderr)


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        else:
            fail(f"target does not exist or is not markdown: {path}")
            raise SystemExit(2)
    return files


def is_biz_relevant(path: Path, text: str) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel.startswith("docs/codex/"):
        return True
    if rel == "docs/architecture/ferrAI_operating_kernel_v0.1.md":
        return True
    if rel.startswith("docs/governance/"):
        return True
    return bool(BIZ_MARKER.search(text))


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not is_biz_relevant(path, text):
        return []

    missing = [term for term, pattern in REQUIRED_TERMS.items() if not pattern.search(text)]
    if missing:
        rel = path.relative_to(REPO_ROOT).as_posix()
        return [f"{rel}: missing required marker(s): {', '.join(missing)}"]
    return []


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate TerraNova/FerrAI BIZ documentation markers.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Markdown files or directories to validate. Defaults to BIZ/Codex/kernel governance targets.",
    )
    args = parser.parse_args(argv[1:])

    raw_paths = args.paths or DEFAULT_TARGETS
    paths = [(REPO_ROOT / raw_path).resolve() for raw_path in raw_paths]

    errors: list[str] = []
    for path in iter_markdown(paths):
        errors.extend(validate_file(path))

    if errors:
        for error in errors:
            fail(error)
        return 1

    print("[validate-docs] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
