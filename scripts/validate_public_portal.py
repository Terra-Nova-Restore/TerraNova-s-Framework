#!/usr/bin/env python3
"""Validate public portal surfaces used by public-facing entry-pack PRs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_INDEX = Path("site/index.html")
ENTRY_PACK_LINK = Path("site/entry-pack-link.txt")
REQUIRED_PUBLIC_DOCS = [
    Path("docs/public/entry_pack_architecture_v0_1.md"),
    Path("docs/public/entry_pack_architecture_offer_v0_1.md"),
    Path("docs/public/entry_pack_architecture_boundary_v0_1.md"),
]
REQUIRED_SITE_STRINGS = [
    "Start with the Entry Pack",
    "Architecture Entry Pack v0.1",
    "Open offer draft",
    "Open boundary sheet",
]
REQUIRED_SITE_LINKS = [
    "https://github.com/Terra-Nova-Restore/TerraNova-s-Framework/blob/main/docs/public/entry_pack_architecture_v0_1.md",
    "https://github.com/Terra-Nova-Restore/TerraNova-s-Framework/blob/main/docs/public/entry_pack_architecture_offer_v0_1.md",
    "https://github.com/Terra-Nova-Restore/TerraNova-s-Framework/blob/main/docs/public/entry_pack_architecture_boundary_v0_1.md",
]
PLACEHOLDER_RE = re.compile(r"placeholder", re.IGNORECASE)
HTTPS_URL_RE = re.compile(r"^https://\S+$")


def fail(message: str) -> None:
    print(f"[validate-public-portal] ERROR: {message}", file=sys.stderr)


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []

    for rel_path in REQUIRED_PUBLIC_DOCS:
        if not (root / rel_path).is_file():
            errors.append(f"missing required public document: {rel_path.as_posix()}")

    site_index = root / SITE_INDEX
    if not site_index.is_file():
        errors.append(f"missing portal index: {SITE_INDEX.as_posix()}")
        return errors

    text = site_index.read_text(encoding="utf-8")
    for value in REQUIRED_SITE_STRINGS:
        if value not in text:
            errors.append(f"site/index.html missing required text: {value}")
    for value in REQUIRED_SITE_LINKS:
        if value not in text:
            errors.append(f"site/index.html missing required link: {value}")

    entry_pack_link = root / ENTRY_PACK_LINK
    if entry_pack_link.exists():
        link_text = entry_pack_link.read_text(encoding="utf-8").strip()
        if not link_text:
            errors.append(f"{ENTRY_PACK_LINK.as_posix()} is empty")
        elif PLACEHOLDER_RE.search(link_text):
            errors.append(f"{ENTRY_PACK_LINK.as_posix()} still contains placeholder text")
        elif not HTTPS_URL_RE.fullmatch(link_text):
            errors.append(
                f"{ENTRY_PACK_LINK.as_posix()} must contain exactly one https URL when present"
            )

    return errors


def main() -> int:
    errors = validate_repo(REPO_ROOT)
    if errors:
        for error in errors:
            fail(error)
        return 1
    print("[validate-public-portal] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
