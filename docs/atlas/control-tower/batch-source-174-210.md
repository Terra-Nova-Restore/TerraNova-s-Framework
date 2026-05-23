# SOURCE-174-210 - Per-trigger source review corridor

Status: started local review scaffold
Created: 2026-05-23
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

`SOURCE-174-210` starts the per-trigger source review after `TRIGGER-MAP-001`.
It does not replace the Notion master, does not publish raw ChatGPT export
content, and does not assign canonical `TRG-*` IDs.

The pass links the 37 source-backed `174-210` rows from
`trigger-map-001.seed.csv` to the deduped `CHATGPT-XPORT-002` review corridor.
XPORT-002 is used as a hashed review target, not as direct semantic authority.

## Scope

| Item | Value |
| --- | --- |
| Trigger range | `174-210` |
| Per-trigger rows | `37` |
| Trigger-only XPORT samples | `3` |
| Tokenomics-trigger XPORT samples | `6` |
| Reserved slots | `171-173` remain reserved L0 ID anchors and are outside this pass |

## Review Lanes

| Lane | Count |
| --- | ---: |
| `standard_trigger_source_gate` | `29` |
| `sensitivity_language_gate` | `2` |
| `cap_ii_tokenomics_ip_gate` | `6` |

## Gate State

| Status | Count |
| --- | ---: |
| `passed` | `1` |
| `started_not_completed` | `1` |
| `pending` | `3` |
| `blocked` | `1` |
| `blocked_by_directive` | `1` |

## Current Decision

All 37 triggers stay at `L2-SOURCE-BACKED-REFERENCE`. Names and short
definitions may be used as source-backed reference material. Public canon,
activation protocols, execution semantics, medical claims, tokenomics claims
and canonical `TRG-*` assignment remain blocked.

`205-210` are stricter than the rest of the range because TRIGGER-MAP-001 links
them to CAP-II/Revoke, tokenomics, business and IP review. They are therefore
held behind XPORT-002 P1 tokenomics-trigger samples plus TNPX-01 comparison.

## Artifacts

| File | Role |
| --- | --- |
| `source-174-210.per-trigger-review.csv` | Per-trigger review rows for `174-210`. |
| `source-174-210.xport-002-correlation.csv` | XPORT-002 sample handles and roles for this pass. |
| `source-174-210.review-gates.csv` | Gates before public canon, TRG assignment, tokenomics/IP wording or mutation. |
| `source-174-210.review-summary.json` | Machine-readable summary and boundary flags. |
| `causal-log.source-174-210-2026-05-23.json` | Causal log for the started review corridor. |

## Boundary

- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No Notion write.
- No commit, push or PR in this pass.
- `DIRTY-SPLIT-001` remains separate; unrelated dirty files are not touched.
