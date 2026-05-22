# GH-XW-001 Public Boundary Review

Status: STUDIO / boundary review complete
Source: `docs/governance/public_boundary.md`, `docs/atlas/control-tower/sens-001.findings.md`, Equilibrium rulebook, GPT H.4 synthesis
Trace: GH-XW-001
Boundary: Public-safe decision record only. No raw Notion source inventory is included.
Mode: STUDIO
GitHub sync state: Prepared as repository-side boundary note.
Notion source awareness: Notion remains the live system of record for page contents, titles, relations and review status.

## Decision

The 2026-05-22 Home view export is admitted to GitHub only as an aggregate
source and method trace.

The raw export itself remains local/private.

## Allowed in GitHub

- aggregate metrics
- hash of the raw export
- public-safe H.4 governance candidate
- schema and field semantics
- negative rules for sync and publication
- reproducible local analysis script
- release gate for future LaTeX or Zenodo work

## Blocked from Public GitHub

- raw URL list
- raw Notion page IDs
- full page title inventory
- raw XLSX/CSV crosswalk tables
- HOLD/private/protected/adult/legal_ip rows
- screenshots exposing private workspace state
- private chat, personal or sensitive content summaries

## Equilibrium Check

| Rule | Result |
| --- | --- |
| Status carried | The package is marked as STUDIO candidate, not final publication. |
| Trace visible | Hash, source label and GH-XW-001 trace are included. |
| Boundary visible | Raw inventory and private rows are explicitly blocked. |
| Mode separated | Notion, GitHub, Zenodo, PDF and Public Surface remain distinct. |
| No silent mutation | No Notion, GitHub remote or Zenodo mutation is performed by this package. |

## Publication Meaning

Publishing this package to GitHub would publish the control method, not the
workspace contents.

It does not approve:

- an automated Notion sync
- a Zenodo update
- a monograph renumbering
- a public page inventory
- a release of protected or private materials
