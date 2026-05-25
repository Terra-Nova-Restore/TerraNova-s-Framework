# Prism Import Manifest

Status: BIZ / Governance
Source: Issue #17 Prism scale checkpoint and current repository boundary policy.
Trace: Issue #17; `raw/exports/prism/source-pack/README.md`; `docs/atlas/README.md`; `raw/exports/REVIEW_GATE.md`.
Boundary: Public-safe import manifest only. It does not publish ignored Prism source-pack contents.
Mode: BIZ
GitHub sync state: tracked in this repository; validate with `scripts/validate_docs.py`.
Notion source awareness: Notion and local Prism exports may contain richer source material; GitHub admits only reviewed derivatives.

## Purpose

This manifest gives large Prism/CIC imports a controlled entry lane before they
touch public documentation. It is the first repository-side answer to the
150k-line scale checkpoint.

## Import Lanes

| Lane | Target | Visibility | Rule |
| --- | --- | --- | --- |
| Atlas docs | `docs/atlas/` | Public after review | Generated or curated summaries only |
| Trigger docs | `docs/triggers/` | Public after review | Gap ledger and redacted trigger-facing summaries only |
| Governance docs | `docs/governance/` | Public after review | Policies, status registries and decision mirrors |
| Release packages | `releases/` | Public after gate | Only explicit release candidates and manifests |
| Source packs | `raw/exports/prism/source-pack/*/` | Ignored/local | Provenance input; do not commit raw source-pack directories |
| Incoming derivatives | `raw/exports/incoming/` | Bounded public review lane | Only reviewed derivatives with checksum and retention rules |

## Current Public Import State

| Surface | Status | Notes |
| --- | --- | --- |
| `raw/exports/prism/source-pack/README.md` | Tracked policy pointer | Allows directory-level provenance without committing ignored packs |
| `docs/atlas/public_overview.md` | Generated public slice | Regenerated through `scripts/render_prism_atlas.py` |
| `docs/atlas/semantic_spine_registry.md` | Public semantic bridge | Connects semantic architecture docs to atlas/source routing |
| `docs/triggers/gap_ledger.md` | Public gap ledger | Redacted trigger-facing review surface |
| `raw/exports/incoming/README.md` | Bounded derivative policy | Created to avoid treating incoming batches as generic raw dumps |

## Required Metadata For Future Imports

Every future Prism/CIC import batch needs:

- source date or export date;
- source class (`source-pack`, `generated-doc`, `manual-review`, `incoming-derivative`);
- intended target lane;
- visibility classification (`public-ok`, `redact-candidate`, `internal`, `private`, `patent-sensitive`);
- line count or file count;
- checksum when file identity matters;
- reviewer/agent note;
- reason why the import belongs in GitHub rather than Notion/local archive only.

## Blockers

Do not import:

- raw ignored source-pack directories;
- private trigger canon or deep internal VORTEX/block-system material;
- wallet, token, credential, API or private-key material;
- TNPX-01 protected source packages;
- Track C or `GODFATHER_LOCK` material without a dedicated intake gate.

## Validation

Before merge:

```text
python scripts/render_prism_atlas.py
python scripts/validate_docs.py
git diff --check
targeted secret/PII scan for changed import files
```

## Next Import Gate

The next real import should create a batch-specific manifest under
`docs/atlas/control-tower/` or `releases/`, not expand this policy file into a
raw source listing.
