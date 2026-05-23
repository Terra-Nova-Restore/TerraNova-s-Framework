# XPORT-002-SAMPLE-CORRIDOR - Raw sample corridor review

Status: local raw review completed as public-safe count artifacts
Created: 2026-05-23
Activation: `/fff`
External mutation: none
Commit status: uncommitted by design

## Purpose

This pass checks whether the `CHATGPT-XPORT-002` review samples still resolve
to local raw files and what kind of public-safe signal they carry for
`SOURCE-174-210`.

It does not publish raw prompts, messages, titles, local paths, conversation IDs
or account data. It also does not promote any trigger to public canon.

## Scope

| Item | Value |
| --- | ---: |
| XPORT-002 samples | `12` |
| Local hash matches | `14` |
| Trigger signal rows | `143` |
| Tokenomics-trigger shared samples | `6` |
| Trigger-only samples | `3` |
| Tokenomics-only samples | `3` |

## Review Decisions

| Decision | Count |
| --- | ---: |
| `axis_corridor_for_cap_ii_tokenomics` | `0` |
| `axis_corridor_for_trigger_review` | `1` |
| `context_only` | `0` |
| `numeric_trigger_signal_only` | `5` |
| `direct_trigger_name_evidence_candidate` | `6` |

## Gate State

| Status | Count |
| --- | ---: |
| `passed` | `1` |
| `blocked` | `2` |
| `pending` | `1` |
| `candidate` | `1` |
| `not_found_in_sample_corridor` | `0` |
| `requires_private_context_review` | `1` |

## Decision

`XPORT-002` is verified as a local raw hash corridor. It is useful for review
routing, especially for `205-210` CAP-II/tokenomics/IP gates and general
trigger correlation. It is not yet direct source authority for public trigger
canon unless private excerpt review validates the exact context.

## Artifacts

| File | Role |
| --- | --- |
| `xport-002.sample-corridor.review.csv` | Per-sample integrity, signal and allowed-use decision. |
| `xport-002.sample-corridor.term-signals.csv` | Count-only signal groups per sample. |
| `xport-002.sample-corridor.trigger-signals.csv` | Count-only `174-210` number/name signals. |
| `xport-002.sample-corridor.gates.csv` | Gates before source promotion, public wording or mutation. |
| `xport-002.sample-corridor.review-summary.json` | Machine-readable summary and boundary flags. |
| `causal-log.xport-002-sample-corridor-2026-05-23.json` | Causal trace for this raw corridor review. |

## Boundary

- No raw messages printed.
- No raw titles printed.
- No local paths printed.
- No conversation IDs printed.
- No account data printed.
- No Notion write.
- No commit, push or PR in this pass.
- `DIRTY-SPLIT-001` remains separate.
