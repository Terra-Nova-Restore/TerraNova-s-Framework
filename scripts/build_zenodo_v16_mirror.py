#!/usr/bin/env python3
"""Build a searchable, provenance-preserving GitHub mirror of Zenodo v16.

The PDF remains the canonical binary publication artifact. Text files produced here
are search derivatives only and preserve PDF page boundaries with explicit markers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "v16"
PAGES = 713
FILE_SIZE = 2_884_898
MD5 = "5fcb85593c0297512927491d933c2290"
SHA256 = "c43cc558b8dfc715f8febeff6231e6be064ab9be50e65857cf2e42a305d96cfd"
VERSION_DOI = "10.5281/zenodo.20732376"
CONCEPT_DOI = "10.5281/zenodo.19774446"
ZENODO_RECORD = "https://zenodo.org/records/20732376"
SOURCE_FILE_KEY = "main_v16_cq_ct_candidate (1).pdf"
MIRROR_FILE_NAME = "FerrAI_TerraNovaCIC_v16_713.pdf"
CHUNK_SIZE = 25


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_pdf(pdf: Path) -> None:
    if not pdf.is_file():
        raise SystemExit(f"Missing PDF: {pdf}")
    size = pdf.stat().st_size
    md5 = digest(pdf, "md5")
    sha256 = digest(pdf, "sha256")
    failures: list[str] = []
    if size != FILE_SIZE:
        failures.append(f"size {size} != {FILE_SIZE}")
    if md5 != MD5:
        failures.append(f"md5 {md5} != {MD5}")
    if sha256 != SHA256:
        failures.append(f"sha256 {sha256} != {SHA256}")

    info = subprocess.run(
        ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
    ).stdout
    match = re.search(r"^Pages:\s+(\d+)\s*$", info, flags=re.MULTILINE)
    page_count = int(match.group(1)) if match else None
    if page_count != PAGES:
        failures.append(f"pages {page_count} != {PAGES}")
    if failures:
        raise SystemExit("PDF verification failed: " + "; ".join(failures))


def extract_pages(pdf: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True,
        capture_output=True,
    )
    text = result.stdout.decode("utf-8", errors="replace")
    pages = text.split("\f")
    if pages and pages[-1] == "":
        pages.pop()
    if len(pages) != PAGES:
        raise SystemExit(f"Text extraction produced {len(pages)} pages, expected {PAGES}")
    return pages


def clean_output(root: Path) -> None:
    for relative in ("text", "index"):
        target = root / relative
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)


def write_text_chunks(root: Path, pages: list[str]) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    text_dir = root / "text"
    for start in range(1, PAGES + 1, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE - 1, PAGES)
        filename = f"pages-{start:03d}-{end:03d}.md"
        path = text_dir / filename
        lines = [
            f"# Zenodo {VERSION} searchable derivative - PDF pages {start}-{end}",
            "",
            "> Search derivative generated from the byte-verified Zenodo v16 PDF. "
            "The PDF is authoritative; extraction artifacts are non-canonical.",
            "",
        ]
        for page_number in range(start, end + 1):
            page_text = pages[page_number - 1].rstrip()
            lines.extend(
                [
                    f"<!-- PDF_PAGE: {page_number} -->",
                    f"## PDF page {page_number}",
                    "",
                    "```text",
                    page_text,
                    "```",
                    "",
                ]
            )
        path.write_text("\n".join(lines), encoding="utf-8")
        chunks.append(
            {
                "file": f"text/{filename}",
                "start_pdf_page": start,
                "end_pdf_page": end,
                "page_count": end - start + 1,
                "sha256": digest(path, "sha256"),
                "bytes": path.stat().st_size,
            }
        )
    return chunks


def write_indexes(root: Path, chunks: list[dict[str, object]], pages: list[str]) -> None:
    index_dir = root / "index"

    with (index_dir / "page-map.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["pdf_page", "text_file", "anchor"])
        for chunk in chunks:
            for page in range(int(chunk["start_pdf_page"]), int(chunk["end_pdf_page"]) + 1):
                writer.writerow([page, chunk["file"], f"pdf-page-{page}"])

    (index_dir / "chunk-map.json").write_text(
        json.dumps({"chunk_size": CHUNK_SIZE, "chunks": chunks}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    toc_pages = 18
    toc_lines = [
        f"# Raw frontmatter and table-of-contents extraction - PDF pages 1-{toc_pages}",
        "",
        "> Raw layout-preserving extraction for navigation. PDF page numbers are explicit.",
        "",
    ]
    for page_number in range(1, toc_pages + 1):
        toc_lines.extend(
            [
                f"<!-- PDF_PAGE: {page_number} -->",
                f"## PDF page {page_number}",
                "",
                "```text",
                pages[page_number - 1].rstrip(),
                "```",
                "",
            ]
        )
    (index_dir / "table-of-contents-extract.md").write_text(
        "\n".join(toc_lines), encoding="utf-8"
    )


def write_manifest(root: Path, chunks: list[dict[str, object]]) -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "schema": "terranova.zenodo-github-mirror.v1",
        "status": "frozen-binary-mirror-with-search-derivative",
        "generated_at_utc": generated_at,
        "work": {
            "title": "FerrAI / Terra'Nova'CIC - Werkmonographie und Evidenzapparat",
            "creator": "Silvan Lenhard",
            "version": VERSION,
            "publication_date": "2026-06-17",
            "pages": PAGES,
            "license": "CC-BY-4.0",
            "language": "deu",
            "version_doi": VERSION_DOI,
            "concept_doi": CONCEPT_DOI,
            "zenodo_record": ZENODO_RECORD,
        },
        "source_artifact": {
            "zenodo_file_key": SOURCE_FILE_KEY,
            "repository_path": f"artifact/{MIRROR_FILE_NAME}",
            "bytes": FILE_SIZE,
            "md5": MD5,
            "sha256": SHA256,
            "verification": "byte-verified against the stored Zenodo v16 API payload",
        },
        "derivative": {
            "format": "layout-preserving UTF-8 Markdown chunks",
            "authority": "non-canonical search derivative; PDF remains authoritative",
            "chunk_size_pages": CHUNK_SIZE,
            "chunk_count": len(chunks),
            "page_markers": "<!-- PDF_PAGE: N -->",
            "chunks": chunks,
        },
    }
    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (root / "SHA256SUMS").write_text(
        f"{SHA256}  artifact/{MIRROR_FILE_NAME}\n", encoding="utf-8"
    )


def write_readme(root: Path, chunks: list[dict[str, object]]) -> None:
    lines = [
        "# Zenodo v16 GitHub mirror",
        "",
        "This directory mirrors the published Zenodo v16 work and adds a searchable text derivative.",
        "",
        "## Authority model",
        "",
        "- **Zenodo v16 / DOI**: canonical published freeze and citation authority.",
        "- **`artifact/` PDF**: byte-identical GitHub mirror of the Zenodo v16 file.",
        "- **`text/` Markdown**: non-canonical searchable derivative, split by PDF page range.",
        "- **`index/`**: deterministic page-to-file navigation and raw frontmatter/TOC extraction.",
        "- **Notion**: current semantic and operational state, which may be newer than v16.",
        "",
        "## Verified artifact",
        "",
        f"- Version: `{VERSION}`",
        f"- Publication date: `2026-06-17`",
        f"- Extent: `{PAGES} PDF pages`",
        f"- Version DOI: `{VERSION_DOI}`",
        f"- Concept DOI: `{CONCEPT_DOI}`",
        f"- Size: `{FILE_SIZE} bytes`",
        f"- MD5: `{MD5}`",
        f"- SHA-256: `{SHA256}`",
        f"- Mirror path: `artifact/{MIRROR_FILE_NAME}`",
        "",
        "## Search derivative",
        "",
        f"The text layer contains `{len(chunks)}` Markdown chunks of at most `{CHUNK_SIZE}` PDF pages each.",
        "Every extracted page starts with an explicit `PDF_PAGE` marker. Layout extraction can contain",
        "line-break, glyph, or hyphenation artifacts and must not silently override the PDF.",
        "",
        "## Navigation",
        "",
        "- `index/page-map.csv` maps each PDF page to a text file and anchor.",
        "- `index/chunk-map.json` records chunk ranges, sizes, and hashes.",
        "- `index/table-of-contents-extract.md` contains the raw extracted frontmatter and TOC pages.",
        "- `MANIFEST.json` records provenance, hashes, authority boundaries, and derivative metadata.",
        "",
        "## Update rule",
        "",
        "Do not replace this directory with an unversioned later build. A new Zenodo version receives a new",
        "sibling directory and its own verified manifest. GitHub mirrors Zenodo; it does not redefine the DOI freeze.",
        "",
    ]
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def patch_zenodo_reference(repo_root: Path) -> None:
    path = repo_root / "docs" / "references" / "zenodo.md"
    if not path.exists():
        raise SystemExit(f"Missing repository reference file: {path}")
    text = path.read_text(encoding="utf-8")
    old = (
        "The canonical source available to this repository preparation did not supply a\n"
        "current file size or checksum. Those fields remain unresolved and are not inferred."
    )
    new = (
        "Verified file size:\n"
        f"`{FILE_SIZE} bytes`\n\n"
        "Verified checksums:\n"
        f"- `md5:{MD5}`\n"
        f"- `sha256:{SHA256}`\n\n"
        "Repository mirror:\n"
        f"`publications/zenodo/v16/artifact/{MIRROR_FILE_NAME}`\n\n"
        "The binary mirror is byte-identical to the published v16 artifact according to the stored\n"
        "Zenodo API payload and local verification. The adjacent text layer is a non-canonical\n"
        "search derivative and must not override the PDF or DOI record."
    )
    if old in text:
        text = text.replace(old, new, 1)
    elif MD5 in text and "publications/zenodo/v16" in text:
        return
    else:
        raise SystemExit("Expected unresolved checksum block not found in docs/references/zenodo.md")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path.cwd(), type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    mirror_root = repo_root / "publications" / "zenodo" / VERSION
    artifact_dir = mirror_root / "artifact"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    target_pdf = artifact_dir / MIRROR_FILE_NAME

    if args.pdf.resolve() != target_pdf.resolve():
        shutil.copyfile(args.pdf, target_pdf)

    verify_pdf(target_pdf)
    clean_output(mirror_root)
    pages = extract_pages(target_pdf)
    chunks = write_text_chunks(mirror_root, pages)
    write_indexes(mirror_root, chunks, pages)
    write_manifest(mirror_root, chunks)
    write_readme(mirror_root, chunks)
    patch_zenodo_reference(repo_root)

    print(
        json.dumps(
            {
                "status": "ok",
                "version": VERSION,
                "pages": PAGES,
                "chunks": len(chunks),
                "pdf": str(target_pdf.relative_to(repo_root)),
                "sha256": SHA256,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
