# XPORT-002-EXCERPT-GATE-001 - Private excerpt-context gate

Status: completed as public-safe classification artifacts
Created: 2026-05-23
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This pass performs the agreed private excerpt-context review for the
`XPORT-002` sample corridor. It reads local raw windows to classify whether
sample hits are definition-context candidates, name-context candidates or only
numeric correlation.

It does not publish raw prompts, raw messages, raw excerpts, titles, local
paths, conversation IDs or account data.

## Result

| Item | Value |
| --- | ---: |
| XPORT-002 samples | `12` |
| Local hash matches | `14` |
| Context rows | `143` |
| Best trigger rows | `37` |

## Best Trigger Decisions

| Decision | Count |
| --- | ---: |
| `excerpt_context_supports_definition_candidate` | `3` |
| `excerpt_context_supports_name_candidate` | `32` |
| `name_seen_context_weak` | `0` |
| `numeric_context_only` | `2` |

## Gate State

| Status | Count |
| --- | ---: |
| `completed_count_only` | `1` |
| `candidate` | `2` |
| `requires_manual_rejection_or_confirmation` | `1` |
| `pending` | `1` |
| `blocked` | `1` |

## Decision

The gate can route direct candidates into `SOURCE-174-210`, but it does not
clear public canon, raw excerpt publication, canonical `TRG-*` assignment,
activation semantics or CAP-II/tokenomics/IP wording.

## Artifacts

| File | Role |
| --- | --- |
| `xport-002.excerpt-gate.context-review.csv` | Per sample/trigger context classification, count-only. |
| `xport-002.excerpt-gate.best-trigger-review.csv` | Best public-safe XPORT evidence class per trigger. |
| `xport-002.excerpt-gate.gates.csv` | Gates before source promotion, public wording or canon assignment. |
| `xport-002.excerpt-gate.review-summary.json` | Machine-readable gate summary and boundary flags. |
| `causal-log.xport-002-excerpt-gate-001-2026-05-23.json` | Causal trace for this private excerpt gate. |

## Boundary

- No raw excerpts printed.
- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No Notion write.
- No commit, push or PR in this pass.
- `DIRTY-SPLIT-001` remains separate.
