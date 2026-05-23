# SOURCE-174-210-ROUTING-001 - XPORT excerpt routing for SOURCE-174-210

Status: completed as local public-safe routing layer
Created: 2026-05-23
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This batch consumes `XPORT-002-EXCERPT-GATE-001` and routes its count-only
classification into `SOURCE-174-210`. It does not read raw exports, does not
publish excerpts and does not promote any trigger to public canon.

## Result

| Item | Value |
| --- | ---: |
| Trigger rows | `37` |
| Definition-context shortlist | `3` |
| Numeric-only hold | `2` |
| CAP-II protected rows | `6` |
| Sensitivity rows | `3` |

## Routing Decisions

| Decision | Count |
| --- | ---: |
| `shortlist_for_private_source_confirmation` | `3` |
| `route_to_private_context_review` | `32` |
| `do_not_promote_from_xport` | `2` |

## Gate State

| Status | Count |
| --- | ---: |
| `completed` | `1` |
| `candidate` | `1` |
| `private_review_required` | `1` |
| `hold` | `1` |
| `pending` | `2` |
| `blocked` | `1` |

## Current Decision

`176`, `182` and `202` are routed to private source-confirmation shortlist.
`196` and `201` are held as numeric-only and must not be promoted from XPORT.
`205-210` remain behind CAP-II/tokenomics/business/IP/TNPX gates even where
XPORT has name-context evidence.

## Artifacts

| File | Role |
| --- | --- |
| `source-174-210.xport-excerpt-routing.csv` | Per-trigger routing matrix from SOURCE rows and XPORT excerpt gate. |
| `source-174-210.routing-gates.csv` | Gates before source promotion, public wording, CAP-II/IP claims or TRG assignment. |
| `source-174-210.xport-excerpt-routing.summary.json` | Machine-readable routing summary and boundary flags. |
| `causal-log.source-174-210-routing-001-2026-05-23.json` | Causal trace for this routing batch. |

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
