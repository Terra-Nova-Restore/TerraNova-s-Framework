# ZIP Analysis Continuation 01

Status: CODEX_LOCAL_SAFE_ARTIFACT
Cycle: 1
Date: 2026-05-13
Source layer: GPT aggregate analysis, mirrored through Notion
Repository layer: GitHub-safe documentation only

## Scope

This folder records the first safe repository-side artifact set for the private
`XXL_DatenExport_500_000Zeilen.zip` corpus.

The raw corpus is intentionally not stored here. This cycle contains only
aggregate metrics, hashes, routing notes, and publication boundary material.

## Source Chain

1. GPT analyzed the private ZIP locally and produced aggregate-only findings.
2. Silvi copied the findings into Notion.
3. Notion persisted the page `ZIP_ANALYSIS_CONTINUATION_01 -- Hash-Anchored Korpus-Metrics`.
4. Codex converted the persisted page into repository-safe artifacts.

## Included Artifacts

- `manifest.json`: machine-readable cycle metadata and public-boundary flags.
- `hashes.sha256`: integrity hashes for the private corpus and export block.
- `metrics.csv`: aggregate hard metrics and term frequencies.
- `safe-index.md`: public-safe index of what this cycle contains and excludes.
- `redaction-policy.md`: cycle-specific publication and promotion policy.

## Hard Boundary

GitHub must not receive the raw 553,000-line text export. Notion, GitHub, and
Zenodo receive only curated, aggregate, or redacted derivatives until a later
review explicitly clears additional material.

## Naming Bridge

GPT's label `CEI-DATA-04` is treated as a corpus and sensitive-review concept.
In the Notion tree it maps to CEI-00 plus CEI-04 / CEI-04A / CEI-04B / CEI-04C.

`CEI-DATA-05` remains the workspace index and page census layer. It is not used
as the home for ZIP corpus material.
