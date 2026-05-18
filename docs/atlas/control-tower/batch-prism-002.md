# PRISM-002 - Next-Release Backpropagation

Status: STUDIO plan, repo-local
Date: 2026-05-17
Predecessor: `PRISM-001 Backpropagation Queue`
External mutation: none

## Recommended Variant

Treat PRISM-002 as release-readiness control, not as publication action.

The best path is:

```text
RC01-v12 citable snapshot
-> PRISM-001 feedback queue
-> existing RC01-v13 preflight
-> PRISM-002 readiness gates
-> distinct public-safe artifact later
-> explicit Zenodo draft GO later
```

This preserves the published DOI while allowing the living CAP system to feed the next release intelligently.

## Current Answer

Yes, the system can work as designed if each layer keeps its role:

- Notion is the live control surface.
- GitHub is the audit and execution trace.
- Zenodo is the published snapshot, not the live truth.
- CAP is the operating control layer.
- `/fff` steers bounded internal action, not uncontrolled external mutation.

The current hard publication blocker is not conceptual. It is artifact readiness: no distinct public-safe RC01-v13 PDF exists yet.

## Input State

| Signal | Value |
| --- | --- |
| Current citable release | `RC01-v12` |
| Current live title | `FerrAI-Terra'Nova CIC Framework - System Architecture, State Logic and Governance Boundaries` |
| Current DOI | `10.5281/zenodo.20073579` |
| Concept DOI | `10.5281/zenodo.19774446` |
| Publication date | `2026-05-17` after metadata refresh |
| Record created | `2026-05-07T19:39:34+02:00` |
| Metadata updated | `2026-05-17T07:20:40.751823+02:00` |
| PDF pages | 661 |
| PDF SHA-256 | `1e9ce2f810b0af8c245887bb3a01ebcb01ca8f90c971bd5cf39da47a6b8dda40` |
| Existing RC01-v13 preflight | `releases/zenodo/rc01-v13-preflight-2026-05-13/` |
| RC01-v13 artifact state | missing distinct public-safe PDF |
| Known bad candidate | `main (45).pdf` byte-identical to RC01-v12 |
| Zenodo mutation authorization | none |

## Decision

PRISM-002 translates the seven PRISM-001 feedback items into release and companion-material gates.

It does not:

- create a Zenodo draft
- upload a file
- reserve a DOI
- publish a new version
- expose raw private Notion inventory
- expose restricted wiki material
- expose sensitive IP detail

## PRISM-002 Work Products

| File | Purpose |
| --- | --- |
| `prism-002.next-release-checklist.csv` | Concrete checklist for RC01-v13 / companion readiness. |
| `prism-002.companion-material-map.md` | Where CAP material belongs: main release, companion note, appendix, internal-only, or blocked. |
| `prism-002.release-readiness-gate.csv` | Hard release gates before any Zenodo draft cycle. |
| `causal-log.prism-002-plan-2026-05-17.json` | Causal trace for PRISM-002. |

## Release Logic

PRISM-002 separates three truths:

| Truth layer | Meaning | Owner |
| --- | --- | --- |
| Published truth | RC01-v12 is the current citation target. | Zenodo |
| Living operational truth | CAP 0.1-0.3 controls the workspace now. | Notion + GitHub |
| Future release truth | RC01-v13 may include selected, sanitized CAP deltas. | GitHub preflight, then Zenodo draft after GO |

The key control rule:

```text
CAP may update the next-release queue.
CAP must not silently rewrite the publication record.
```

## Gate Summary

PRISM-002 promotes these items:

- citation/title-page alignment
- CAP term hardening
- R16 governance delta
- registry and causal-log appendix candidate
- SENS-001 public-boundary gate
- diagram/visual apparatus promotion queue
- no-credit operating policy

PRISM-002 blocks:

- any RC01-v13 upload based on byte-identical PDF
- any raw Notion inventory export
- any private, restricted, token, wallet, credential, chat, or patent-sensitive detail expansion
- any Zenodo write without explicit later GO

## Next Action

The next efficient step is `AUTO-001`.

Recommended order:

1. `AUTO-001` for repeatable test runs and validation scripts.
2. `DASH-001` if the goal is better Notion steering visibility.

For publication work, the next blocked requirement is:

```text
Create a distinct public-safe RC01-v13 PDF artifact.
```

Until that exists, PRISM remains in readiness and companion-material mode.
