#!/usr/bin/env python3
"""Quick sanity checks for Python scripts pasted from chat/notion contexts."""

from __future__ import annotations

import argparse
from pathlib import Path


def check_script(path: Path) -> int:
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    has_tabs = "\t" in text
    literal_n_count = text.count("\\n")
    has_argparse_symbol = "argparse." in text
    has_import_argparse = "import argparse" in text or "from argparse import" in text

    print(f"FILE: {path}")
    print(f"HAS_TAB {has_tabs}")
    print(f"HAS_LITERAL_N {literal_n_count > 20} (count={literal_n_count})")
    print(f"USES_ARGPARSE {has_argparse_symbol}")
    print(f"IMPORTS_ARGPARSE {has_import_argparse}")

    if has_argparse_symbol and not has_import_argparse:
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
    args = parser.parse_args()
    return check_script(Path(args.path))


if __name__ == "__main__":
    raise SystemExit(main())
