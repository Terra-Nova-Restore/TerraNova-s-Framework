# EQUILIBRIUM Weight Policy v0.1

Status: policy mirror, not canonical rule text.
Date: 2026-05-24

## Purpose

This document mirrors the operational weighting policy for the EQUILIBRIUM
State DB. It is intentionally limited to policy, mapping, trace, and guardrails.
The canonical rule text remains in Notion.

## Sources Of Record

- Rulebook text source: https://www.notion.so/a045fc7b60f24b3f9a6c579aff276b16
- State/activation matrix: https://www.notion.so/2fbf2819a2884ab398146ec4d70ad9cb
- Bridge contract: https://www.notion.so/7c3b2740d90e477597452cab9a8c4209
- Weight rationale: https://www.notion.so/1004f51942194da694bffd6b91431363
- Matrix freeze checkpoint: https://www.notion.so/6c074d1a17374ed1a0edc64a0b6fd9b8

## Boundaries

- Do not migrate rule text into this repository.
- Do not treat formula outputs as verification.
- Do not promote any sync target to `both_allowlisted` without explicit operator approval.
- Keep `GS`, `CIC`, and `INDEX` budget-excluded orientation nodes.
- GitHub mirrors policy and trace only; Notion remains the source of record.

## Weighting Model

Selected approach: Option B.

`400` is the default normal-operation weight. Values above or below `400`
are prioritization signals, not proof of truth or final importance.

## Rank To Weight Mapping

| Rank | Weight |
| ---: | ---: |
| 19 | 480 |
| 18 | 460 |
| 17 | 440 |
| 16 | 420 |
| 15 | 400 |
| 14 | 400 |
| 13 | 400 |
| 12 | 400 |
| 11 | 400 |
| 10 | 380 |
| 9 | 360 |
| 8 | 340 |
| 7 | 320 |
| 6 | 300 |
| 5 | 280 |
| 4 | 260 |
| 3 | 240 |
| 2 | 220 |
| 1 | 200 |

## Applied Weights

| Rule ID | Weight |
| --- | ---: |
| R4 | 480 |
| R11 | 460 |
| R19 | 440 |
| R2 | 420 |
| R6 | 400 |
| R7 | 400 |
| R8 | 400 |
| R10 | 400 |
| R15 | 400 |
| R17 | 380 |
| R12 | 360 |
| R1 | 340 |
| R3 | 320 |
| R9 | 300 |
| R15.1 | 300 |
| R16 | 280 |
| R13 | 240 |
| R14 | 220 |
| R5 | 220 |

## Core Set

The current must-carry core set is:

`R2`, `R4`, `R6`, `R7`, `R8`, `R10`, `R11`, `R15`, `R17`, `R19`.

## Dependency Pass Notes

`DEP-LINKED-RULE-PASS-001` was applied on 2026-05-24 in Notion only.
`WEIGHT-PASS-001` was applied on 2026-05-24 in Notion only: `R5` moved to
`220`, `R15.1` moved to `300`, and `R13` stayed at `240`.

- `R9` is intentionally left without broad linked-rule dependencies because it
  is a high-risk global mode gate.
- `R13` remains `github_allowlist_candidate` and is linked narrowly to `R18.6`,
  `R4`, and `R19`.
- `R18` now acts as parent structure for `R18.1` through `R18.8`.
- No rule text was migrated into the State DB or this repository.

## Drift And Review

The post-apply DB search for `draft:` and `bitte review` returned no active
State DB hits after the dependency pass. This is a surface check only, not a
verification claim.
