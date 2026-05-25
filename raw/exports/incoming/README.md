# Incoming Raw-Export Derivative Lane

Status: bounded public review lane

This directory contains tracked manuscript and appendix intake derivatives used
for RC01/500-page reconstruction and review. The files are not treated as the
private XXL raw ChatGPT dump, but they are larger than aggregate indexes and
therefore require explicit retention rules.

## Current Inventory Shape

```text
batch_01..06   small text intake fragments with checksum sidecars
batch_07       Appendix II, I-Q derivative, with checksum sidecar
batch_08       Ausbau/intake corridor R-V derivative, with checksum sidecar
batch_09       Erweiterungsbloecke W-AF derivative, with checksum sidecar
batch_10       Erweiterungsbloecke AG-end/release notes derivative, with checksum sidecar
```

The larger `.md` files are public-review derivatives, not raw private transcript
exports. They still require sensitivity discipline because they mention
categories such as tokenization, wallet, patent/IP, Track C and trigger/session
architecture.

## Retention Rule

Files may remain here only while they support at least one active public-safe
purpose:

- reconstructing a cited release package;
- proving checksum-backed provenance;
- reviewing appendix/manuscript migration;
- preparing a curated public doc outside `raw/exports/`.

If a file no longer serves one of these purposes, replace it with a public-safe
manifest/checksum pointer and move the source material to private/local storage.

## Promotion Rule

Do not promote files from this lane by copying them wholesale into public docs.
Promotion means extracting reviewed, redacted, source-aware content into a
curated target such as `docs/`, `data_exports/`, or `releases/`.

Minimum promotion record:

- source filename and checksum;
- classification result;
- redaction/sensitivity scan result;
- target artifact path;
- date and reviewer/agent note.

## Block Rule

Immediately stop public-lane use if review finds:

- credential-like values or real secrets;
- wallet/private-key material;
- direct PII, banking, account or payment data;
- raw internal Notion IDs or workspace object lists;
- protected TNPX-01 source material;
- uncleared Track C, `GODFATHER_LOCK`, intimate or private-session content.

Keep a checksum/audit pointer if provenance matters; keep the source itself
outside the public repository.
