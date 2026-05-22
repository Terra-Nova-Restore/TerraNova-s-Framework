# WORKSPACE-CORR-001 - Relation-Preserving Workspace Correlation

Status: STUDIO / repo-local correlation pass
Source: Local `Home_Ansicht_22.05.2026.txt`, GH-XW-001 crosswalk package, CAP Control Tower, Trigger Truth model, Silvan publication boundary correction
Trace: WORKSPACE-CORR-001
Boundary: Aggregate and schema layer only. No raw Notion URLs, raw page IDs, raw page titles, third-party identities, account data, secrets or unreviewed IP specifics are published by this batch.
Mode: STUDIO
GitHub sync state: Prepared locally; no commit, push or PR performed by this batch.
Notion source awareness: Notion remains the living source of record. This batch does not mutate Notion.

## Decision

`WORKSPACE-CORR-001` establishes the next operating order:

```text
Notion workspace corpus
-> ChatGPT export correlation
-> tokenomics and trigger module work
-> Metarotik and deep phenomenology publication tracks
```

This order is now the default because trigger, tokenomics and Metarotik cannot
be interpreted safely or accurately without the workspace correlation layer.

## Publication Principle

The public boundary is corrected:

```text
Silvan-related material is not private by default.
It is public after professional framing, source preservation and relation-safe redaction.
```

Allowed to preserve and later publish in accountable form:

- deep conversations
- Silvan-related development history
- metaphysical and phenomenological material
- Trigger, tokenomics, Mermaid and Metarotik relations
- ORA, Triquetra, TerraNovaCIC and Equilibrium development logic

Still excluded or abstracted:

- private third parties
- account data
- raw identities that do not need public exposure
- intimate real names
- security material
- unreviewed IP specifics

## Relation Preservation Rule

Redaction must not destroy correlation.

If a page is too sensitive for direct release, the public artifact must preserve
at least its relation axes:

```text
page exists
-> domain axis
-> trigger / tokenomics / Mermaid / patent / Metarotik relation
-> source status
-> publication lane
-> next review gate
```

This prevents "safety" from becoming accidental erasure of the real system
structure.

## Aggregate Result

The local Home export hash matched the GH-XW-001 source hash:

```text
7c8ee97c6bdd3299a0f380230e681e1036a86c78a266329b291b2a2c221b3163
```

The correlation pass found:

| Metric | Value |
| --- | ---: |
| URLs seen | 877 |
| Unique page refs | 841 |
| Database/view URLs with `v=` | 93 |
| Block anchor URLs | 23 |
| Correlation axes | 10 |
| Publication lanes | 10 |

## High-Value Counts

| Axis | Page count |
| --- | ---: |
| Control Tower / CAP / Equilibrium / CIC | 174 |
| Tokenomics / DAO / wallet / license | 89 |
| ChatGPT / Codex / export dialogue | 68 |
| Patent / IGE / TNPX / IP | 64 |
| Trigger | 43 |
| GitHub / sync / delta | 39 |
| Metarotik / intimacy / phenomenology | 18 |
| Mermaid / MMD / graph | 16 |
| Prism / Zenodo / LaTeX / DOI | 12 |

## Implemented Files

| File | Role |
| --- | --- |
| `workspace-corr-001.relation-preservation-rules.md` | Human-readable publication and redaction rulebook. |
| `workspace-corr-001.axis-counts.csv` | Aggregate count per correlation axis. |
| `workspace-corr-001.axis-cooccurrence.csv` | Aggregate co-occurrence matrix for relation preservation. |
| `workspace-corr-001.publication-lane-counts.csv` | Aggregate count per publication/review lane. |
| `workspace-corr-001.review-summary.json` | Machine-readable summary of the pass. |
| `causal-log.workspace-corr-001-2026-05-22.json` | Causal trace for the batch. |
| `scripts/build_workspace_correlation_package.py` | Reproducible local analysis script. |

## Next

Best next action: `CHATGPT-XPORT-001`.

Reason: the Notion workspace now has a first relation map. The next correlation
layer must be the ChatGPT export corpus before trigger, tokenomics or Metarotik
work is expanded.
