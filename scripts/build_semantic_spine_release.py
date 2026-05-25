#!/usr/bin/env python3
"""Build the TerraNova semantic spine release package.

The script intentionally has no third-party Python dependencies. It renders the
public Markdown release candidate into a standalone HTML artifact, attempts a
local headless Edge/Chrome PDF render when available, and writes review-only
metadata/draft files for GitHub and Zenodo.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = REPO_ROOT / "docs/public/semantic_architecture_public_release_v0_1.md"
PACKAGE_DIR = REPO_ROOT / "releases/zenodo/semantic-spine-v0.1-2026-05-25"
VERSION = "semantic-spine-v0.1"
TITLE = "TerraNova / FerrAI Semantic Architecture Public Release v0.1"
AUTHOR = "Lenhard, Silvan"
ORCID = "0009-0007-8033-3508"
REPOSITORY = "https://github.com/Terra-Nova-Restore/TerraNova-s-Framework"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower())
    return text.strip("-") or "section"


def inline_markdown(text: str) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f"\u0000{len(placeholders) - 1}\u0000"

    def code_repl(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", code_repl, text)
    escaped = html.escape(text)

    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    def link_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(match.group(2), quote=True)
        return f'<a href="{href}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)

    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{index}\u0000", value)
    return escaped


def render_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""

    header, *body = rows
    html_lines = ["<table>", "<thead>", "<tr>"]
    html_lines.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    html_lines.extend(["</tr>", "</thead>", "<tbody>"])
    for row in body:
        html_lines.append("<tr>")
        html_lines.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        html_lines.append("</tr>")
    html_lines.extend(["</tbody>", "</table>"])
    return "\n".join(html_lines)


def markdown_to_html(markdown_text: str) -> str:
    output: list[str] = []
    lines = markdown_text.splitlines()
    i = 0
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            language = stripped[3:].strip() or "text"
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            output.append(
                f'<pre class="code-block language-{html.escape(language)}"><code>{html.escape(chr(10).join(code_lines))}</code></pre>'
            )
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            flush_paragraph()
            table_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            output.append(render_table(table_lines))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            anchor = slugify(text)
            output.append(f'<h{level} id="{anchor}">{inline_markdown(text)}</h{level}>')
            i += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            output.append("<ul>")
            output.extend(f"<li>{inline_markdown(item)}</li>" for item in items)
            output.append("</ul>")
            continue

        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    return "\n".join(output)


def build_html(markdown_text: str) -> str:
    body = markdown_to_html(markdown_text)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(TITLE)}</title>
  <style>
    :root {{
      --ink: #18201b;
      --muted: #5d675f;
      --paper: #fffdf6;
      --line: #d8cbb1;
      --accent: #8f4e24;
      --accent-dark: #4d2f1e;
      --wash: #f3ead8;
      --code: #1e2420;
    }}
    @page {{ size: A4; margin: 18mm 16mm; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at top left, #f6ead3 0, #fffdf6 34%, #f9f4e8 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.58;
    }}
    main {{
      max-width: 920px;
      margin: 0 auto;
      padding: 52px 38px 72px;
      background: rgba(255, 253, 246, 0.92);
    }}
    .kicker {{
      color: var(--accent);
      font-family: "Trebuchet MS", Verdana, sans-serif;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }}
    h1, h2, h3, h4 {{
      color: var(--accent-dark);
      line-height: 1.15;
      page-break-after: avoid;
    }}
    h1 {{
      max-width: 760px;
      margin: 12px 0 20px;
      font-size: 2.55rem;
    }}
    h2 {{
      margin-top: 2.2rem;
      border-top: 1px solid var(--line);
      padding-top: 1rem;
      font-size: 1.55rem;
    }}
    h3 {{ margin-top: 1.6rem; }}
    p {{ margin: 0.85rem 0; }}
    a {{ color: #7f3f1f; text-decoration-thickness: 0.08em; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0 1.35rem;
      font-size: 0.92rem;
      page-break-inside: avoid;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 0.55rem 0.65rem;
      vertical-align: top;
    }}
    th {{
      background: var(--wash);
      text-align: left;
      font-family: "Trebuchet MS", Verdana, sans-serif;
      font-size: 0.78rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    code {{
      background: #efe5d0;
      border-radius: 4px;
      padding: 0.08rem 0.22rem;
      font-family: Consolas, "Courier New", monospace;
      font-size: 0.9em;
    }}
    pre {{
      background: var(--code);
      color: #f8f1df;
      border-radius: 12px;
      margin: 1.1rem 0;
      padding: 1rem;
      overflow-x: auto;
      white-space: pre-wrap;
      page-break-inside: avoid;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      color: inherit;
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 0.5rem 1.2rem;
      margin: 1.25rem 0 2rem;
      padding: 1rem;
      border: 1px solid var(--line);
      background: rgba(243, 234, 216, 0.58);
      font-family: "Trebuchet MS", Verdana, sans-serif;
      font-size: 0.88rem;
    }}
    .meta strong {{ color: var(--accent-dark); }}
    @media print {{
      body {{ background: #fffdf6; }}
      main {{ padding: 0; }}
    }}
  </style>
</head>
<body>
<main>
  <div class="kicker">TerraNova / FerrAI public release candidate</div>
  <section class="meta">
    <div><strong>Version:</strong> v0.1</div>
    <div><strong>Prepared:</strong> 2026-05-25</div>
    <div><strong>Author:</strong> Silvan Lenhard</div>
    <div><strong>Repository:</strong> Terra-Nova-Restore/TerraNova-s-Framework</div>
  </section>
{body}
</main>
</body>
</html>
"""


def find_browser() -> Path | None:
    env_browser = os.environ.get("SEMANTIC_SPINE_BROWSER")
    candidates = [
        env_browser,
        shutil.which("msedge"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    return None


def render_pdf(html_path: Path, pdf_path: Path) -> bool:
    browser = find_browser()
    if browser is None:
        return False
    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, timeout=120)
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    return pdf_path.exists() and pdf_path.stat().st_size > 0


def metadata_payload(github_commit: str | None = None) -> dict[str, object]:
    description = (
        "Public-safe release candidate defining the TerraNova / FerrAI semantic "
        "architecture spine: Semantic Trigger Architecture, Semantic Core Layer "
        "(SCL), Iterative Interaction Collapse, Lenhard Decoding Module, Lenhard "
        "Model, and Mermaid Cluster. This package is a review candidate and does "
        "not claim an external Zenodo upload until an explicit upload action is "
        "performed."
    )
    metadata: dict[str, object] = {
        "review_package": {
            "id": "semantic-spine-v0.1-2026-05-25",
            "status": "REVIEW_ONLY_NO_MUTATION",
            "created_date": "2026-05-25",
            "zenodo_mutation_authorized": False,
            "github_release_authorized": False,
            "tag_authorized": False,
        },
        "proposed_api_payload_candidate": {
            "metadata": {
                "title": TITLE,
                "upload_type": "publication",
                "publication_type": "workingpaper",
                "description": f"<p>{html.escape(description)}</p>",
                "creators": [
                    {
                        "name": AUTHOR,
                        "affiliation": "Terra'Nova'Restore",
                        "orcid": ORCID,
                    }
                ],
                "access_right": "open",
                "license": "cc-by-4.0",
                "version": "v0.1",
                "language": "eng",
                "publication_date": "2026-05-25",
                "keywords": [
                    "TerraNova",
                    "FerrAI",
                    "Semantic Core Layer",
                    "Semantic Trigger Architecture",
                    "Iterative Interaction Collapse",
                    "Lenhard Decoding Module",
                    "Lenhard Model",
                    "Mermaid",
                    "human-AI collaboration",
                    "system architecture",
                ],
                "related_identifiers": [
                    {
                        "identifier": REPOSITORY,
                        "relation": "isSupplementTo",
                        "scheme": "url",
                        "resource_type": "software",
                    }
                ],
                "custom": {"code:codeRepository": REPOSITORY},
                "notes": "Review package only. No Zenodo draft, DOI reservation, upload, publish action, GitHub tag, or GitHub release is authorized by this file.",
            }
        },
    }
    if github_commit:
        metadata["github_commit"] = github_commit
    return metadata


def release_notes() -> str:
    return f"""# GitHub Release Draft: {VERSION}

Status: draft text only
Source: `docs/public/semantic_architecture_public_release_v0_1.md`
Trace: generated 2026-05-25 by `scripts/build_semantic_spine_release.py`
Boundary: no GitHub tag or release is created by this file
Mode: SYNC / release preparation
GitHub sync state: ready for explicit release GO
Notion source awareness: GitHub-visible public-safe synthesis only

## Title

{TITLE}

## Suggested Tag

```text
semantic-spine-v0.1
```

## Release Notes

This release candidate publishes the TerraNova / FerrAI semantic architecture
spine as a citable public artifact.

Included:

- Semantic Trigger Architecture
- Semantic Core Layer (SCL)
- Iterative Interaction Collapse
- Lenhard Decoding Module (LDM)
- Lenhard Model
- Mermaid Cluster
- Atlas/source registry bridge
- Zenodo-ready review package

## Assets

- `semantic_architecture_public_release_v0_1.html`
- `semantic_architecture_public_release_v0_1.pdf`
- `zenodo_metadata.semantic-spine-v0.1.review.json`

## Boundary

This draft does not create a tag, publish a GitHub release or upload to Zenodo.
Those actions require an explicit release command.
"""


def upload_gate() -> str:
    return f"""# Zenodo Upload Gate: {VERSION}

Status: explicit-GO gate
Source: semantic spine release package
Trace: generated 2026-05-25 by `scripts/build_semantic_spine_release.py`
Boundary: no external Zenodo action is authorized by this gate alone
Mode: SYNC / publication gate
GitHub sync state: package prepared in repository
Notion source awareness: public-safe GitHub synthesis; no raw Notion material in upload package

## Upload Preconditions

| Gate | State |
| --- | --- |
| Public release Markdown exists | ready |
| HTML artifact exists | ready |
| PDF artifact exists | generated when local browser renderer is available |
| Zenodo metadata JSON exists | ready for review |
| Raw Notion URLs / page IDs | blocked |
| Raw exports | blocked |
| Protected TNPX-01 draft details | blocked |
| External upload | requires explicit GO |

## Exact GO Wording

Use this only when the external upload should actually happen:

```text
GO Zenodo semantic-spine-v0.1 upload
```

## Upload Payload

- `docs/public/semantic_architecture_public_release_v0_1.md`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/semantic_architecture_public_release_v0_1.html`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/semantic_architecture_public_release_v0_1.pdf`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/zenodo_metadata.semantic-spine-v0.1.review.json`
"""


def update_manifest(package_dir: Path, files: Iterable[Path], pdf_rendered: bool) -> None:
    manifest_path = package_dir / "manifest.json"
    manifest = {
        "version": VERSION,
        "prepared_at": str(date(2026, 5, 25)),
        "status": "release-ready-review-package",
        "external_upload_state": "not_uploaded",
        "title": TITLE,
        "primary_artifact": "docs/public/semantic_architecture_public_release_v0_1.md",
        "boundary": {
            "raw_notion_urls": False,
            "raw_exports": False,
            "tnpx_01_protected_draft_details": False,
            "external_zenodo_mutation": False,
            "github_release_mutation": False,
        },
        "rendering": {
            "html": True,
            "pdf": pdf_rendered,
            "renderer": "python-stdlib-html + headless-browser-pdf",
        },
        "files": [],
        "next_external_step": "Explicit GitHub release/tag GO or Zenodo metadata review and upload/update GO.",
    }
    file_entries = []
    for path in files:
        if path.exists():
            file_entries.append(
                {
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    manifest["files"] = file_entries
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build(args: argparse.Namespace) -> int:
    if not SOURCE_MD.exists():
        raise FileNotFoundError(SOURCE_MD)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    markdown_text = SOURCE_MD.read_text(encoding="utf-8")
    html_path = PACKAGE_DIR / "semantic_architecture_public_release_v0_1.html"
    pdf_path = PACKAGE_DIR / "semantic_architecture_public_release_v0_1.pdf"
    metadata_path = PACKAGE_DIR / "zenodo_metadata.semantic-spine-v0.1.review.json"
    github_release_path = PACKAGE_DIR / "github_release_draft.semantic-spine-v0.1.md"
    upload_gate_path = PACKAGE_DIR / "zenodo_upload_gate.semantic-spine-v0.1.md"

    html_path.write_text(build_html(markdown_text), encoding="utf-8")
    pdf_rendered = False
    if not args.no_pdf:
        pdf_rendered = render_pdf(html_path, pdf_path)

    metadata_path.write_text(
        json.dumps(metadata_payload(args.github_commit), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    github_release_path.write_text(release_notes(), encoding="utf-8")
    upload_gate_path.write_text(upload_gate(), encoding="utf-8")

    package_files = [
        SOURCE_MD,
        REPO_ROOT / "docs/atlas/semantic_spine_registry.md",
        REPO_ROOT / "docs/architecture/public_semantic_architecture_spine.md",
        REPO_ROOT / "docs/architecture/semantic_trigger_architecture.md",
        REPO_ROOT / "docs/architecture/semantic_core_layer.md",
        REPO_ROOT / "docs/architecture/iterative_interaction_collapse.md",
        REPO_ROOT / "docs/architecture/lenhard_decoding_module.md",
        REPO_ROOT / "docs/architecture/lenhard_model.md",
        REPO_ROOT / "docs/atlas/mermaid_cluster.md",
        html_path,
        pdf_path,
        metadata_path,
        github_release_path,
        upload_gate_path,
        PACKAGE_DIR / "README.md",
    ]
    update_manifest(PACKAGE_DIR, package_files, pdf_rendered)

    print(json.dumps({"html": str(html_path), "pdf_rendered": pdf_rendered, "package": str(PACKAGE_DIR)}, indent=2))
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the semantic spine release package.")
    parser.add_argument("--no-pdf", action="store_true", help="Skip headless-browser PDF rendering.")
    parser.add_argument("--github-commit", help="Optional GitHub commit SHA to record in metadata.")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    return build(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
