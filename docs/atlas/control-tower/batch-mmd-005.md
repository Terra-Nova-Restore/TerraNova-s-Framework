# MMD-005 - CAP Module Drafts

Date: 2026-05-17

Activation: `MMD-005 - CAP Module Drafts go`

Mode: repo-local module drafting

External mutation: none

Notion AI credits used: 0

## Purpose

MMD-005 drafts local CAP module records for the five safe candidates promoted by MMD-004.

## Inputs

| File | Role |
| --- | --- |
| `mmd-004.module-record-candidates.csv` | Canon-gated candidate list. |
| `mmd-004.candidate-review.csv` | Visual evidence rows. |
| `mmd-004.guard-review.csv` | Guard relation rows. |
| `atlas.manifest.v1.1.json` | Local Atlas trigger and cluster context. |
| `trigger-complement-2026-03-30.md` | Repo-local source note for Atlas v1.1 trigger-depth. |

## Outputs

| File | Purpose |
| --- | --- |
| `mmd-005.cap-module-drafts.csv` | Five local CAP draft module records. |
| `mmd-005.module-evidence.csv` | Evidence rows for visual candidates, guards and Atlas context. |
| `mmd-005.module-relation-map.csv` | Draft module relation map. |
| `mmd-005.hash-ledger.csv` | Draft hash handles and SHA-256 digests. |
| `mmd-005.hash-material.json` | Hash material used for deterministic fingerprints. |
| `mmd-005.review-summary.json` | Machine-readable summary. |
| `mmd-005.cap-module-drafts.md` | Human-readable module draft summary. |
| `scripts/build_cap_module_drafts.py` | Repeatable draft builder. |

## Result

- Draft modules: 5
- Evidence rows: 33
- Relation rows: 21
- Hash rows: 5
- Eligible references: `516, 520, 521, 540, 544`

## Boundary

The draft hashes fingerprint current module material only. They are not canonical trigger hashes and do not replace source review.

## Next

Best next action: `MMD-006 - CAP Module Registry Package`.
