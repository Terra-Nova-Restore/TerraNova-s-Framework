#!/usr/bin/env python3
"""Phase 1: Notion full mirror exporter

Scope:
- Reads ONLY the database referenced by env var name NOTION_DATABASE_ID_CHANGES
- Exports per-page raw JSON + rendered Markdown to mirror/notion/pages/
- Writes manifest to mirror/notion/manifest.phase1.json

Hard boundaries:
- Does NOT touch GitHub Actions or .github/workflows
- Does NOT print NOTION_TOKEN or the database id value
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

DB_ENV_NAME = "NOTION_DATABASE_ID_CHANGES"
OUT_PAGES_DIR = Path("mirror/notion/pages")
OUT_MANIFEST_PATH = Path("mirror/notion/manifest.phase1.json")
LOG_DIR = Path("logs/phase1")

MAX_PAGES_DEFAULT = 500


# ----------------------------
# Utilities
# ----------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def slugify(title: str, max_len: int = 60) -> str:
    s = (title or "").strip().lower()
    # best-effort ASCII slug
    s = s.encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "untitled"
    return s[:max_len].rstrip("-")


def page_id_no_dashes(page_id: str) -> str:
    return page_id.replace("-", "")


def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Notion API client with retries
# ----------------------------

@dataclass
class RetryConfig:
    max_attempts: int = 8
    base_backoff_s: float = 0.8
    max_backoff_s: float = 30.0


class NotionClient:
    def __init__(self, token: str, retry: RetryConfig | None = None):
        if not token:
            raise ValueError("NOTION_TOKEN env var is required")
        self.s = requests.Session()
        self.s.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            }
        )
        self.retry = retry or RetryConfig()

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def request(self, method: str, url: str, *, params: dict | None = None, json_body: dict | None = None) -> dict:
        """HTTP request wrapper.

        Requirements implemented:
        - 429: honor Retry-After when present
        - 5xx: exponential backoff
        - bounded retries
        """

        attempt = 0
        last_exc: Exception | None = None

        while attempt < self.retry.max_attempts:
            attempt += 1
            try:
                r = self.s.request(method, url, params=params, json=json_body, timeout=30)

                # 429 rate limit
                if r.status_code == 429:
                    retry_after = r.headers.get("Retry-After")
                    if retry_after is not None:
                        try:
                            wait_s = float(retry_after)
                        except ValueError:
                            wait_s = None
                    else:
                        wait_s = None

                    if wait_s is None:
                        wait_s = min(self.retry.max_backoff_s, self.retry.base_backoff_s * (2 ** (attempt - 1)))

                    self._sleep(wait_s)
                    continue

                # 5xx backoff
                if 500 <= r.status_code <= 599:
                    wait_s = min(self.retry.max_backoff_s, self.retry.base_backoff_s * (2 ** (attempt - 1)))
                    self._sleep(wait_s)
                    continue

                r.raise_for_status()
                return r.json()

            except requests.RequestException as e:
                last_exc = e
                wait_s = min(self.retry.max_backoff_s, self.retry.base_backoff_s * (2 ** (attempt - 1)))
                self._sleep(wait_s)

        raise RuntimeError(f"Notion API request failed after {self.retry.max_attempts} attempts: {method} {url}") from last_exc

    # ----------------------------
    # Pagination helpers
    # ----------------------------

    def query_database_all_pages(self, database_id: str, page_size: int = 100) -> List[dict]:
        results: List[dict] = []
        cursor: Optional[str] = None

        while True:
            body: Dict[str, Any] = {"page_size": page_size}
            if cursor:
                body["start_cursor"] = cursor

            data = self.request("POST", f"{NOTION_API}/databases/{database_id}/query", json_body=body)
            results.extend(data.get("results", []))

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

        return results

    def get_block_children_all(self, block_id: str, page_size: int = 100) -> List[dict]:
        results: List[dict] = []
        cursor: Optional[str] = None

        while True:
            params: Dict[str, Any] = {"page_size": page_size}
            if cursor:
                params["start_cursor"] = cursor

            data = self.request("GET", f"{NOTION_API}/blocks/{block_id}/children", params=params)
            results.extend(data.get("results", []))

            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")

        return results

    def get_page(self, page_id: str) -> dict:
        return self.request("GET", f"{NOTION_API}/pages/{page_id}")


# ----------------------------
# Renderer
# ----------------------------

def rich_text_to_md(rich_text: List[dict]) -> str:
    parts: List[str] = []
    for rt in rich_text or []:
        plain = rt.get("plain_text", "")

        # visible inline mentions (best-effort)
        if rt.get("type") == "mention":
            mention = rt.get("mention", {})
            mtype = mention.get("type")
            if mtype == "page":
                pid = (mention.get("page") or {}).get("id")
                if pid:
                    plain = f"[page:{pid}]"
            elif mtype == "user":
                uid = (mention.get("user") or {}).get("id")
                if uid:
                    plain = f"@user:{uid}"
            elif mtype == "date":
                date = mention.get("date") or {}
                start = date.get("start")
                end = date.get("end")
                plain = f"{start}{(' → ' + end) if end else ''}"
            else:
                plain = f"[mention:{mtype}] {plain}".strip()

        ann = (rt.get("annotations") or {})
        if ann.get("code"):
            plain = f"`{plain}`"
        if ann.get("bold"):
            plain = f"**{plain}**"
        if ann.get("italic"):
            plain = f"*{plain}*"
        if ann.get("strikethrough"):
            plain = f"~~{plain}~~"
        if ann.get("underline"):
            plain = f"<span underline=\"true\">{plain}</span>"

        href = rt.get("href")
        if href:
            plain = f"[{plain}]({href})"

        parts.append(plain)
    return "".join(parts)


def page_title_from_properties(page: dict) -> str:
    props = page.get("properties") or {}
    for _, v in props.items():
        if (v or {}).get("type") == "title":
            return rich_text_to_md((v.get("title") or [])) or "Untitled"
    return "Untitled"


def render_block(block: dict, children_md: List[str]) -> List[str]:
    t = block.get("type")
    out: List[str] = []

    def text_of(key: str) -> str:
        obj = block.get(key) or {}
        return rich_text_to_md(obj.get("rich_text") or [])

    # paragraph
    if t == "paragraph":
        out.append(text_of("paragraph"))

    # headings 1-3
    elif t == "heading_1":
        out.append(f"# {text_of('heading_1')}")
    elif t == "heading_2":
        out.append(f"## {text_of('heading_2')}")
    elif t == "heading_3":
        out.append(f"### {text_of('heading_3')}")

    # bulleted / numbered list items
    elif t == "bulleted_list_item":
        line = f"- {text_of('bulleted_list_item')}"
        out.append(line)
        out.extend([indent_md(x) for x in children_md])
    elif t == "numbered_list_item":
        line = f"1. {text_of('numbered_list_item')}"
        out.append(line)
        out.extend([indent_md(x) for x in children_md])

    # to_do
    elif t == "to_do":
        obj = block.get("to_do") or {}
        checked = obj.get("checked")
        box = "x" if checked else " "
        out.append(f"- [{box}] {rich_text_to_md(obj.get('rich_text') or [])}")
        out.extend([indent_md(x) for x in children_md])

    # toggle with children
    elif t == "toggle":
        out.append(f"<details>\n<summary>{text_of('toggle')}</summary>")
        out.extend([indent_md(x) for x in children_md])
        out.append("</details>")

    # code blocks with language fences
    elif t == "code":
        obj = block.get("code") or {}
        lang = obj.get("language") or ""
        code = rich_text_to_md(obj.get("rich_text") or [])
        out.append(f"```{lang}\n{code}\n```")

    # quote
    elif t == "quote":
        out.append(f"> {text_of('quote')}")
        out.extend([indent_md(x) for x in children_md])

    # callout
    elif t == "callout":
        obj = block.get("callout") or {}
        icon = obj.get("icon") or {}
        icon_txt = ""
        if icon.get("type") == "emoji":
            icon_txt = icon.get("emoji")
        out.append(f"<callout icon=\"{icon_txt}\">\n\t{rich_text_to_md(obj.get('rich_text') or [])}")
        out.extend(["\t" + x if x else "\t" for x in children_md])
        out.append("</callout>")

    # child page / child database markers
    elif t == "child_page":
        name = (block.get("child_page") or {}).get("title") or ""
        out.append(f"[child_page] {name}")
    elif t == "child_database":
        name = (block.get("child_database") or {}).get("title") or ""
        out.append(f"[child_database] {name}")

    # embeds/bookmarks/files/images as visible URL markers
    elif t in ("embed", "bookmark", "file", "image", "video", "pdf"):
        obj = block.get(t) or {}
        url = obj.get("url")
        if not url:
            # try common file shapes
            f = obj.get("file") or obj.get("external") or {}
            url = f.get("url")
        out.append(f"[{t}] {url or '[no url]'}")

    else:
        # unknown or unrendered block types must not crash
        out.append(f"[unsupported block: {t}]")

    # If block has children but wasn't handled above (e.g. callout already)
    if children_md and t not in ("bulleted_list_item", "numbered_list_item", "to_do", "toggle", "quote", "callout"):
        out.extend(children_md)

    return out


def indent_md(line: str) -> str:
    if line == "":
        return "\t"
    return "\t" + line


def fetch_block_tree(client: NotionClient, block_id: str) -> List[dict]:
    """Recursively fetch blocks.

    Any block with has_children=true will have children fetched.
    """
    blocks = client.get_block_children_all(block_id)
    for b in blocks:
        if b.get("has_children"):
            try:
                b["children"] = fetch_block_tree(client, b["id"])
            except Exception as e:
                b["children_error"] = str(e)
                b["children"] = []
    return blocks


def render_blocks_md(blocks: List[dict]) -> str:
    lines: List[str] = []

    def walk(bs: List[dict]):
        for b in bs:
            children = b.get("children") or []
            children_md = []
            if children:
                # render child blocks, but keep as list of lines
                child_txt = render_blocks_md(children)
                children_md = child_txt.split("\n") if child_txt else []

            rendered = render_block(b, children_md)
            lines.extend(rendered)

    walk(blocks)
    return "\n".join(lines).rstrip() + "\n"


# ----------------------------
# Export
# ----------------------------

def export_database_phase1(client: NotionClient, database_id: str, max_pages: int = MAX_PAGES_DEFAULT) -> dict:
    safe_mkdir(OUT_PAGES_DIR)
    safe_mkdir(OUT_MANIFEST_PATH.parent)
    safe_mkdir(LOG_DIR)

    pages = client.query_database_all_pages(database_id)
    total_pages = len(pages)

    exported_files: List[str] = []
    failed_pages: List[dict] = []

    export_count = 0

    for idx, page in enumerate(pages):
        if export_count >= max_pages:
            break

        page_id = page.get("id")
        if not page_id:
            continue

        try:
            page_full = client.get_page(page_id)
            title = page_title_from_properties(page_full)
            slug = slugify(title)

            blocks_tree = fetch_block_tree(client, page_id)

            # JSON export must include page meta + properties + blocks
            payload = {
                "page": {
                    "id": page_full.get("id"),
                    "url": page_full.get("url"),
                    "parent": page_full.get("parent"),
                    "archived": page_full.get("archived"),
                    "created_time": page_full.get("created_time"),
                    "last_edited_time": page_full.get("last_edited_time"),
                    "properties": page_full.get("properties"),
                    "title": title,
                },
                "blocks": blocks_tree,
            }

            pid = page_id_no_dashes(page_id)
            json_path = OUT_PAGES_DIR / f"{slug}__{pid}.json"
            md_path = OUT_PAGES_DIR / f"{slug}__{pid}.md"

            json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            md_path.write_text(render_blocks_md(blocks_tree), encoding="utf-8")

            exported_files.append(str(json_path))
            exported_files.append(str(md_path))
            export_count += 1

        except Exception as e:
            failed_pages.append({"page_id": page_id, "reason": str(e)})
            # continue

    total_size = 0
    for f in exported_files:
        try:
            total_size += Path(f).stat().st_size
        except FileNotFoundError:
            pass

    remaining_pages = max(0, total_pages - export_count)

    manifest = {
        "exported_page_count": export_count,
        "total_mirror_size_bytes": total_size,
        "generated_at": utc_now_iso(),
        "source_database_env_name": DB_ENV_NAME,
        "files_written": exported_files,
        "failed_pages": failed_pages,
        "max_pages": max_pages,
        "remaining_pages": remaining_pages,
    }

    OUT_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    return manifest


def main() -> int:
    # Print only env name, never secrets.
    print(f"Database ID source env: {DB_ENV_NAME}")

    token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get(DB_ENV_NAME)
    if not database_id:
        raise ValueError(f"Missing required env var: {DB_ENV_NAME}")

    max_pages = int(os.environ.get("PHASE1_MAX_PAGES", str(MAX_PAGES_DEFAULT)))

    client = NotionClient(token)

    manifest = export_database_phase1(client, database_id, max_pages=max_pages)

    # After run, report summary without leaking secrets
    print(f"Exported pages: {manifest['exported_page_count']}")
    print(f"Total mirror size (bytes): {manifest['total_mirror_size_bytes']}")
    print(f"Manifest path: {OUT_MANIFEST_PATH}")

    # sample of one .md file
    md_files = [p for p in manifest.get('files_written', []) if p.endswith('.md')]
    if md_files:
        sample_path = Path(md_files[0])
        try:
            sample = sample_path.read_text(encoding='utf-8')
            sample_lines = sample.splitlines()[:40]
            print("--- SAMPLE MD (first 40 lines) ---")
            print("\n".join(sample_lines))
            print("--- END SAMPLE ---")
        except Exception:
            pass

    # exact retry/429 handling code location
    print("Retry/429 handling location: NotionClient.request (scripts/notion_full_mirror.py)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
