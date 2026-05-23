# TRIGGER-MAP-001 - Trigger Source Map Pass

Status: local complete
Date: 2026-05-23
Mode: STUDIO / `/fff` bounded local execution
External mutation: none

## Purpose

`TRIGGER-MAP-001` converts the current workspace evidence into a source-backed
trigger map without inventing missing rules. It follows the post
`CHATGPT-XPORT-002` sequence: Notion and local source anchors first, ChatGPT
exports as review corridor, tokenomics/trigger work next, Metarotik later.

## Source Principle

No new trigger rule is created in this pass. Existing Notion, local GitHub and
raw source-pack evidence is indexed first. If a number or range is visible but
not source-backed, it remains a review lane.

The controlling Trigger Truth rule is:

```text
Trigger-ID != unique trigger entry
unique key = Trigger-ID + Layer/Instanz + Modus/Promille + Kontext
```

`trigger-map-001.seed.csv` therefore uses `trigger_ref` as a source anchor, not
as a deployment instance key.

## Main Findings

- `174-210` is no longer just a visual range: the Notion Codex139+ export gives
  all 37 names and short definitions.
- `174-210` is still not public trigger canon. It is admitted here as
  `L2-SOURCE-BACKED-REFERENCE`, with execution, activation protocol and public
  `TRG-*` assignment blocked.
- `171-173` are reserved slots per Silvi decision from 2026-05-23. They are
  `reserved_slot` / `L0-ID-ANCHOR`, not source gaps.
- `205-210` is source-backed but routed through CAP-II/Revoke, tokenomics,
  business and IP review before any publication use.
- `988-992` stays protected because active Notion labels and the local Deep
  Reference labels differ.
- `/fff` is active as bounded local steering, but incident/data-loss paths still
  require `/preflight -> /snapshot -> /audit -> /coherence` first.

## Outputs

| File | Role |
| --- | --- |
| `trigger-map-001.source-index.csv` | Source handles, tiers and public-safe evidence scopes. |
| `trigger-map-001.seed.csv` | Source-backed trigger seed rows, including `174-210`. |
| `trigger-map-001.range-status.csv` | Range-level correction map from old gap ledger to current evidence. |
| `trigger-map-001.contradictions.csv` | Drift and conflict ledger with current resolutions. |
| `trigger-map-001.source-search.csv` | Positive and negative search trace for `171-173` and `174-210`. |
| `trigger-map-001.review-summary.json` | Machine-readable counts and next action. |
| `causal-log.trigger-map-001-2026-05-23.json` | Causal coherence log for this pass. |

## Counts

| Metric | Value |
| --- | --- |
| Source handles | 16 |
| Seed rows | 71 |
| Codex139+ 174-210 rows | 37 |
| Range-status rows | 12 |
| Contradictions | 6 |
| Source-search rows | 5 |

## Seed Status Counts

| Status | Count |
| --- | --- |
| `active_command_surface` | 1 |
| `defined_reference_export` | 37 |
| `documented_anchor` | 5 |
| `documented_point` | 2 |
| `documented_range_reference` | 7 |
| `documented_sensitive` | 3 |
| `documented_sensitive_conflict` | 3 |
| `documented_subset` | 3 |
| `documented_subset_caution` | 1 |
| `identified_cluster` | 1 |
| `known_anchor` | 3 |
| `reserved_slot` | 3 |
| `source_review_complete` | 2 |

## Publication Lane Counts

| Lane | Count |
| --- | --- |
| `hold_until_filled` | 3 |
| `internal` | 11 |
| `internal_caution` | 1 |
| `internal_public_rule_ok` | 3 |
| `internal_sensitivity_review` | 2 |
| `protected_biz_ip_review` | 6 |
| `protected_internal` | 1 |
| `protected_internal_only` | 6 |
| `protected_later` | 2 |
| `public_after_source_extraction` | 7 |
| `public_after_trigger_review` | 29 |

## Next Action

`SOURCE-174-210` if the next goal is public-safe trigger definition review.
Keep `171-173` as reserved slots and fill them later from XPORT-002, TNPX-01 or
a future session.
