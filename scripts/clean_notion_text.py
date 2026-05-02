#!/usr/bin/env python3
"""Basic cleaner for Notion-exported text → Markdown/LaTeX friendly.

- normalizes broken glyphs
- fixes common bullet/arrow artifacts
- trims excessive whitespace
"""

from __future__ import annotations

import sys
from pathlib import Path

REPLACEMENTS = {
    "": "-",
    "": "",
    "→": "->",
    " ": " ",  # non-breaking space
}


def clean(text: str) -> str:
    out = text
    for k, v in REPLACEMENTS.items():
        out = out.replace(k, v)

    # normalize line endings and trim trailing spaces
    lines = [ln.rstrip() for ln in out.replace("\r\n", "\n").split("\n")]

    # collapse >2 empty lines
    cleaned = []
    empty_run = 0
    for ln in lines:
        if ln.strip() == "":
            empty_run += 1
            if empty_run <= 2:
                cleaned.append("")
        else:
            empty_run = 0
            cleaned.append(ln)

    return "\n".join(cleaned).strip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: clean_notion_text.py <input> <output>", file=sys.stderr)
        return 2
    inp = Path(argv[1]).read_text(encoding="utf-8")
    out = clean(inp)
    Path(argv[2]).write_text(out, encoding="utf-8")
    print(f"[clean] wrote {argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
