#!/usr/bin/env python3
"""Quick sanity checks for Python scripts pasted from chat/notion contexts."""

from __future__ import annotations

import argparse
from pathlib import Path


ARGPARSE_IMPORT_LINE = "import argparse\n"


def _ensure_trailing_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def _autofix_argparse_import(path: Path, text: str) -> bool:
    """Insert `import argparse` near the top of the file if missing."""
    lines = text.splitlines(keepends=True)

    insert_at = 0
    if lines and lines[0].startswith("#!"):
        insert_at = 1

    # Keep module docstring at file top when present.
    if insert_at < len(lines) and lines[insert_at].lstrip().startswith(('"""', "'''")):
        quote = '"""' if '"""' in lines[insert_at] else "'''"
        insert_at += 1
        while insert_at < len(lines):
            if quote in lines[insert_at]:
                insert_at += 1
                break
            insert_at += 1

    # Skip future imports to avoid violating Python rules.
    while insert_at < len(lines) and lines[insert_at].strip().startswith("from __future__ import"):
        insert_at += 1

    lines.insert(insert_at, ARGPARSE_IMPORT_LINE)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def check_script(path: Path, fix_missing_argparse: bool = False) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    has_tabs = "\t" in text
    literal_n_count = text.count("\\n")
    has_argparse_symbol = "argparse." in text or "ArgumentParser(" in text
    has_import_argparse = "import argparse" in text or "from argparse import" in text

    print(f"FILE: {path}")
    print(f"HAS_TAB {has_tabs}")
    print(f"HAS_LITERAL_N {literal_n_count > 20} (count={literal_n_count})")
    print(f"USES_ARGPARSE {has_argparse_symbol}")
    print(f"IMPORTS_ARGPARSE {has_import_argparse}")

    if has_argparse_symbol and not has_import_argparse:
        if fix_missing_argparse:
            changed = _autofix_argparse_import(path, _ensure_trailing_newline(text))
            if changed:
                print("AUTO_FIXED inserted `import argparse`")
                return 0
        print("LIKELY_ERROR missing `import argparse`")
        return 1

    if literal_n_count > 20 and not has_tabs:
        print("LIKELY_ERROR file may be copy/paste-rendered with escaped newlines")
        return 1

    print("OK sanity checks passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run quick script sanity checks.")
    parser.add_argument("path", help="Path to a .py file")
    parser.add_argument(
        "--fix-missing-argparse",
        action="store_true",
        help="Automatically insert `import argparse` when argparse is used but missing.",
    )
    args = parser.parse_args()
    return check_script(Path(args.path), fix_missing_argparse=args.fix_missing_argparse)


if __name__ == "__main__":
    raise SystemExit(main())
