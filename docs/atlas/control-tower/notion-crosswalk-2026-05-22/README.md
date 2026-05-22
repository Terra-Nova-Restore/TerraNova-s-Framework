# GH-XW-001 - Notion Crosswalk Public-Safe Package

Status: STUDIO / public-safe GitHub candidate
Source: Local `Home_Ansicht_22.05.2026.txt` raw export, GPT H.4 synthesis, Notion Zenodo page, Equilibrium rulebook, Zenodo RC01-v12 release mirror
Trace: GH-XW-001, `Home_Ansicht_22.05.2026.txt` SHA-256 `7c8ee97c6bdd3299a0f380230e681e1036a86c78a266329b291b2a2c221b3163`
Boundary: Aggregate-only package. No raw Notion URL list, no raw page inventory, no private page content, no Zenodo mutation.
Mode: STUDIO
GitHub sync state: Prepared as a reviewed repository-side candidate package.
Notion source awareness: Notion remains the living workspace source of record; this package is an audit and next-build bridge only.

## Purpose

`GH-XW-001` turns the 2026-05-22 Notion Home view export into a public-safe
GitHub package without publishing the raw workspace inventory.

The package supports a future monograph build where the crosswalk module may be
inserted into the evidence apparatus after the current `H.3` section. In the
published RC01-v12 PDF, the existing `H.4-H.9` headings are already occupied, so
this package treats the crosswalk as a next-build candidate and not as a silent
rewrite of the published Zenodo snapshot.

## Public-Safe Contents

| File | Role |
| --- | --- |
| `h4-crosswalk-governance-candidate.md` | Redacted H.4 candidate text for the evidence apparatus. |
| `metrics-summary.json` | Aggregate metrics from the local raw export. |
| `schema.md` | Public-safe register schema and field rules. |
| `public-boundary-review.md` | Publication boundary and blocked content decision. |
| `release-gate.md` | Gate before any LaTeX, Notion or Zenodo follow-up. |

## Explicitly Excluded

- the raw `Home_Ansicht_22.05.2026.txt` export
- full CSV/XLSX crosswalk files with raw Notion URLs or page IDs
- HOLD/private/protected/adult/legal_ip review rows
- screenshots that expose workspace internals
- any Zenodo draft, upload, publish or DOI action

## Current Admission

The crosswalk is admitted as `STUDIO / CANON-CANDIDATE`, not as `BIZ / public
release`.

Allowed use:

- aggregate citation and source audit
- next-build planning for the evidence apparatus
- local reproducibility checks
- public-safe explanation of why raw Notion visibility is not publication

Blocked use:

- public raw page inventory
- automated Notion full sync
- direct Zenodo release event
- final monograph renumbering without a new LaTeX build and review pass
