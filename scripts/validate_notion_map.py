#!/usr/bin/env python3
"""Validate TerraNova Notion -> GitHub import maps.

This validator is intentionally lightweight and dependency-free.
It checks structural integrity before any automated export writes files.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = {"version", "name", "created", "target_repository", "source_index", "policy", "targets"}
REQUIRED_TARGET_FIELDS = {
    "notion_title",
    "github_path",
    "cluster",
    "status",
    "content_type",
    "priority",
    "visibility",
}
ALLOWED_CONTENT_TYPES = {"markdown", "latex", "mermaid"}
ALLOWED_VISIBILITY = {"public_candidate", "redacted_candidate", "private_or_redacted_only"}
ALLOWED_STATUS = {"canonical_candidate", "restricted_candidate", "public_ready_candidate", "cleanup_required"}
PATH_RE = re.compile(r"^[A-Za-z0-9_./+@=,:()\-]+$")


def fail(message: str) -> None:
    print(f"[notion-map] ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    missing = REQUIRED_TOP_LEVEL - set(data)
    if missing:
        fail(f"missing top-level fields: {sorted(missing)}")

    targets = data.get("targets")
    if not isinstance(targets, list) or not targets:
        fail("targets must be a non-empty list")

    seen_paths: set[str] = set()
    seen_titles: set[str] = set()

    for idx, target in enumerate(targets, start=1):
        if not isinstance(target, dict):
            fail(f"target #{idx} is not an object")

        missing_fields = REQUIRED_TARGET_FIELDS - set(target)
        if missing_fields:
            fail(f"target #{idx} missing fields: {sorted(missing_fields)}")

        title = str(target["notion_title"]).strip()
        github_path = str(target["github_path"]).strip()
        content_type = target["content_type"]
        visibility = target["visibility"]
        status = target["status"]
        priority = target["priority"]

        if not title:
            fail(f"target #{idx} has empty notion_title")
        if title in seen_titles:
            fail(f"duplicate notion_title: {title}")
        seen_titles.add(title)

        if not github_path or github_path.startswith("/") or ".." in github_path:
            fail(f"invalid github_path for {title}: {github_path}")
        if not PATH_RE.match(github_path):
            fail(f"github_path contains suspicious characters for {title}: {github_path}")
        if github_path in seen_paths:
            fail(f"duplicate github_path: {github_path}")
        seen_paths.add(github_path)

        if content_type not in ALLOWED_CONTENT_TYPES:
            fail(f"invalid content_type for {title}: {content_type}")
        if visibility not in ALLOWED_VISIBILITY:
            fail(f"invalid visibility for {title}: {visibility}")
        if status not in ALLOWED_STATUS:
            fail(f"invalid status for {title}: {status}")
        if not isinstance(priority, int) or priority < 1 or priority > 5:
            fail(f"priority must be integer 1..5 for {title}: {priority}")

    print(f"[notion-map] OK: {path} ({len(targets)} targets)")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_notion_map.py <path-to-map.json>", file=sys.stderr)
        return 2
    validate(Path(argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
