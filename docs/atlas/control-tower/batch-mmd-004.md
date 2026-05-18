# MMD-004 - Candidate Review and Canon Gate

Date: 2026-05-17

Activation: `MMD-004 go`

Mode: repo-local review and canon gate

External mutation: none

Notion AI credits used: 0

## Purpose

MMD-004 reviews the 53 visual trigger candidates from MMD-003 and separates
them into usable CAP lanes without creating canonical `TRG-*` entries.

## Inputs

| File | Role |
| --- | --- |
| `mmd-003.visual-trigger-candidates.csv` | Visual node candidates. |
| `mmd-003.guard-bridge.csv` | Guard/edge trigger bridge rows. |
| `canon-details.md` | Local canon reference for known safe anchors and caution zones. |

## Outputs

| File | Purpose |
| --- | --- |
| `mmd-004.candidate-review.csv` | Review decision for each visual candidate. |
| `mmd-004.guard-review.csv` | Review decision for each guard bridge row. |
| `mmd-004.module-record-candidates.csv` | Unique visible trigger references and gate status. |
| `mmd-004.lane-summary.csv` | Lane counts and gate meanings. |
| `mmd-004.review-summary.json` | Machine-readable summary. |
| `mmd-004.candidate-review-and-canon-gate.md` | Human-readable summary. |
| `scripts/review_visual_trigger_candidates.py` | Repeatable review builder. |

## Result

| Metric | Count |
| --- | ---: |
| Candidate review rows | 53 |
| Guard review rows | 140 |
| Unique module record candidates | 14 |
| Review lanes | 8 |

Eligible CAP module candidates:

```text
516, 520, 521, 540, 544
```

Held/deferred references:

```text
174-210, 517, 600, 777, 988, 989, 990, 991, 992
```

## Boundary

MMD-004 does not:

- mutate Notion
- use Notion AI
- assign canonical `TRG-*` entries
- treat visual labels as complete trigger history
- normalize AutoFlow or Schattenarchiv-depth work
- expand token/integrity material without SENS-001

## Next

Best next action:

```text
MMD-005 - CAP Module Drafts
```

MMD-005 should draft local CAP module records for the five eligible candidates
only: `516`, `520`, `521`, `540`, `544`.
