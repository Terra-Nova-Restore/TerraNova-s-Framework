#!/usr/bin/env python3
"""Aggregate-safe metrics for a local Notion Home export.

The script reads a local text export and prints aggregate metrics only. It does
not print raw URLs, page IDs or titles, so its output is suitable for the
GH-XW-001 public-safe package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path


URL_RE = re.compile(r"(?:https?://)?(?:www\.)?notion\.so/[^\s)\]>\"']+", re.IGNORECASE)
UUID32_RE = re.compile(r"([0-9a-f]{32})$", re.IGNORECASE)
DASHED_UUID_RE = re.compile(
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)


def normalize_url(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"https://{raw}"


def page_id_from_path(path: str) -> tuple[str | None, str]:
    last = path.rstrip("/").split("/")[-1]
    match = UUID32_RE.search(last) or DASHED_UUID_RE.search(last)
    if not match:
        return None, urllib.parse.unquote(last).strip() or "(no-slug)"

    page_id = match.group(1).replace("-", "").lower()
    slug = urllib.parse.unquote(last[: match.start(1)].rstrip("-")).strip() or "(no-slug)"
    return page_id, slug


def analyze(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    nonempty_lines = [line for line in lines if line.strip()]
    urls = [normalize_url(match) for match in URL_RE.findall(text)]

    page_occurrences: dict[str, int] = {}
    page_raw_urls: dict[str, set[str]] = {}
    page_clean_urls: dict[str, set[str]] = {}
    title_to_ids: dict[str, set[str]] = {}
    view_count = 0
    anchor_count = 0

    for url in urls:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        if "v" in query:
            view_count += 1
        if parsed.fragment:
            anchor_count += 1

        page_id, slug = page_id_from_path(parsed.path)
        if page_id is None:
            continue

        page_occurrences[page_id] = page_occurrences.get(page_id, 0) + 1
        page_raw_urls.setdefault(page_id, set()).add(url)
        clean_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
        page_clean_urls.setdefault(page_id, set()).add(clean_url)
        title_to_ids.setdefault(slug, set()).add(page_id)

    return {
        "source_file_label": path.name,
        "source_file_sha256": hashlib.sha256(data).hexdigest(),
        "source_file_bytes": len(data),
        "metrics": {
            "total_lines": len(lines),
            "nonempty_lines": len(nonempty_lines),
            "notion_urls_found": len(urls),
            "unique_raw_urls": len(set(urls)),
            "unique_page_ids": len(page_occurrences),
            "database_view_urls_with_v": view_count,
            "block_anchor_urls": anchor_count,
            "page_ids_with_multiple_occurrences": sum(
                1 for count in page_occurrences.values() if count > 1
            ),
            "page_ids_with_multiple_distinct_raw_urls": sum(
                1 for raw_urls in page_raw_urls.values() if len(raw_urls) > 1
            ),
            "page_ids_with_multiple_distinct_clean_urls": sum(
                1 for clean_urls in page_clean_urls.values() if len(clean_urls) > 1
            ),
            "title_groups_with_multiple_page_ids": sum(
                1 for page_ids in title_to_ids.values() if len(page_ids) > 1
            ),
        },
        "redaction": {
            "raw_urls_printed": False,
            "raw_page_ids_printed": False,
            "raw_titles_printed": False,
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Local Notion Home export text file.")
    parser.add_argument(
        "--expect-sha256",
        help="Optional expected SHA-256. Exits non-zero if the file does not match.",
    )
    args = parser.parse_args(argv[1:])

    path = Path(args.path)
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2

    result = analyze(path)
    if args.expect_sha256 and result["source_file_sha256"] != args.expect_sha256:
        print(
            "sha256 mismatch: "
            f"expected {args.expect_sha256}, got {result['source_file_sha256']}",
            file=sys.stderr,
        )
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
