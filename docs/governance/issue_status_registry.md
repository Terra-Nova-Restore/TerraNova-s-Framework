# Governance Issue Status Registry

Status: BIZ / Governance
Source: GitHub issue and PR state after PR #60 and PR #66 merge.
Trace: Issues #15, #23, #25; PR #60, PR #66; Zenodo record `10.5281/zenodo.20073579`.
Boundary: Public-safe issue-status mirror only. It does not close issues by itself and does not mutate Notion or Zenodo.
Mode: BIZ
GitHub sync state: tracked in this repository; validate with `scripts/validate_docs.py`.
Notion source awareness: Notion remains the living source for canon and workspace memory.

## Purpose

This registry records which open governance questions are now resolved by
repository artifacts and which remain active work. It prevents stale issue text
from outranking newer reviewed repository state.

## Current Status

| Issue | Status | Repository evidence | Next action |
| --- | --- | --- | --- |
| #23 TNV-SYNC hardening | Closed/completed | PR #60, merge commit `d8c9337`; `tests/test_notion_to_github.py`; `.github/workflows/notion-map-validate.yml` | None for the issue; continue normal sync validation |
| #25 GitHub container hardening | Closed/completed | `docs/governance/public_boundary.md`; `docs/governance/repo_roles.md`; `raw/exports/REVIEW_GATE.md`; `raw/exports/incoming/README.md`; PR #66, merge commit `49e4024` | Keep as historical closure anchor |
| #15 Citation/stub reality check | Open | `CITATION.cff`; `docs/references/zenodo.md`; `docs/architecture/core_grid_spec.md`; `docs/science/dissertation/appendix/A02_formula_collection.tex`; `docs/architecture/cic_convergence_9_layers.md` | Keep open until A.2 formulas and CIC convergence receive controlled real exports |
| #13 Source-tier and Prism naming | Open | `docs/governance/source_tier_and_naming_policy.md`; `docs/ai/cic_atlas_usage.md`; `docs/ai/prism_atlas_usage.md` | Keep open until public naming review and external product-name decision are complete |
| #17 Prism scale governance | Open | `docs/governance/prism_import_manifest.md`; `raw/exports/prism/source-pack/README.md`; `docs/atlas/README.md`; boundary docs from PR #66 | Keep open until a real import batch is classified against the manifest |
| #10/#11 Track C intake/review | Open | `docs/governance/track_c_intake_checklist.md`; `docs/governance/public_boundary.md`; `raw/exports/incoming/README.md`; Track C references in issue bodies | Keep open until a real Track C batch is classified against the checklist |

## Issue #15 Reality Check

The citation layer is real but should stay soberly framed.

Current verified state:

- `CITATION.cff` exists and points to DOI `10.5281/zenodo.20073579`.
- The ORCID value in `CITATION.cff` matches the live Zenodo creator metadata observed on 2026-05-25.
- `docs/references/zenodo.md` is the public repository citation anchor.
- The live Zenodo API reports record `20073579`, concept record `19774446`, version `RC01-v12`, revision `12`, publication date `2026-05-17`, and metadata update `2026-05-21T19:29:35.963451+02:00`.

Current open work:

- `docs/science/dissertation/appendix/A02_formula_collection.tex` is still an initial controlled export stub.
- `docs/architecture/cic_convergence_9_layers.md` is still an initial controlled export stub.
- `docs/architecture/core_grid_spec.md` is no longer a stub; it is a real Notion-master import with open decisions.

## Issue #25 Closure Check

Issue #25 is closed as completed. The repository now contains the requested
container-hardening surfaces:

- public boundary policy;
- raw-export review gate;
- repository role vocabulary;
- conservative sync hardening through PR #60;
- incoming derivative lane policy through PR #66.

The remaining credential-rotation proof remains an account-level operational
check, not repository text evidence.

## Issue #17 Import Gate

The Prism scale checkpoint now has a public import manifest:

- `docs/governance/prism_import_manifest.md`

This is not a bulk-import approval. It is the gate a future import batch must
pass before entering public docs.

## Issues #10/#11 Track C Gate

Track C now has a public intake checklist:

- `docs/governance/track_c_intake_checklist.md`

This is not a publication approval. It prevents Track C material from being
merged into Track A, deleted by accident, or treated as factual evidence before
classification.

## Precedence Rule

When old issue text conflicts with newer reviewed files:

```text
merged PR evidence > current repository file > issue body > chat memory
```

Notion remains the living system-of-record for canon and workspace memory, but
GitHub remains the audit trail for public repository hardening.
