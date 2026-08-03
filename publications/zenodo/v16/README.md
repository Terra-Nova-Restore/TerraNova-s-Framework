# Zenodo v16 GitHub mirror

This directory mirrors the published Zenodo v16 work and adds a searchable text derivative.

## Authority model

- **Zenodo v16 / DOI**: canonical published freeze and citation authority.
- **`artifact/` PDF**: byte-identical GitHub mirror of the Zenodo v16 file.
- **`text/` Markdown**: non-canonical searchable derivative, split by PDF page range.
- **`index/`**: deterministic page-to-file navigation and raw frontmatter/TOC extraction.
- **Notion**: current semantic and operational state, which may be newer than v16.

## Verified artifact

- Version: `v16`
- Publication date: `2026-06-17`
- Extent: `713 PDF pages`
- Version DOI: `10.5281/zenodo.20732376`
- Concept DOI: `10.5281/zenodo.19774446`
- Size: `2884898 bytes`
- MD5: `5fcb85593c0297512927491d933c2290`
- SHA-256: `c43cc558b8dfc715f8febeff6231e6be064ab9be50e65857cf2e42a305d96cfd`
- Mirror path: `artifact/FerrAI_TerraNovaCIC_v16_713.pdf`

## Search derivative

The text layer contains `29` Markdown chunks of at most `25` PDF pages each.
Every extracted page starts with an explicit `PDF_PAGE` marker. Layout extraction can contain
line-break, glyph, or hyphenation artifacts and must not silently override the PDF.

## Navigation

- `index/page-map.csv` maps each PDF page to a text file and anchor.
- `index/chunk-map.json` records chunk ranges, sizes, and hashes.
- `index/table-of-contents-extract.md` contains the raw extracted frontmatter and TOC pages.
- `MANIFEST.json` records provenance, hashes, authority boundaries, and derivative metadata.

## Update rule

Do not replace this directory with an unversioned later build. A new Zenodo version receives a new
sibling directory and its own verified manifest. GitHub mirrors Zenodo; it does not redefine the DOI freeze.
