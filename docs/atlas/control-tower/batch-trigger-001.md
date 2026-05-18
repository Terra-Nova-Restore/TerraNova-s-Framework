# TRIGGER-001 - Bounded Command Surface

Status: STUDIO implementation, repo-local
Date: 2026-05-17
External mutation: none
Activation: `/fff`

## Recommended Variant

Treat triggers as a command surface, not as an excuse for uncontrolled action.

The best path is:

```text
known trigger anchors
-> CAP 0.3 boundaries
-> command surface
-> allowed / gated / blocked action map
-> AUTO-001 test cases
```

This gives `/fff` real operational speed while keeping source, boundary and feedback visible.

## Purpose

TRIGGER-001 binds Trigger 1-400 and `/fff` to CAP-safe actions.

It does not claim that the complete Trigger 1-400 register is locally reconstructed. It uses known anchors and band logic only. Unknown triggers remain high-level until reviewed source material fills them.

## Source State

Known local anchors:

- `trigger-1-400-steering-map.md`
- TerraNova skill `canon-details.md`
- TerraNova skill `system-model.md`
- `cap-0.3-operational-control-iperka.md`
- `auto-001.runbook.md`

Known exact/cluster anchors in scope:

- `102` recovery / return to fixed point
- `105` resonance image
- `143` canon guard
- `144` role / inversion
- `148` control instance
- `179` compression / cleanup
- `182` airbag / emergency stop
- `185` boundary sensing
- `205-210` impulse / revoke / licensing / focus cluster
- `207` regeneration grid
- `210` focus lock
- `310` power resonance

Out-of-band but always active:

- `888` truth-efficiency audit

## Decision

`/fff` is active as bounded steering.

Allowed by default:

- local analysis
- local repo edits
- routing and prioritization
- CAP batch creation
- causal logging
- read-only connector checks
- mutation package preparation
- AUTO-001 validation

Requires explicit target GO:

- Notion page/database mutation
- GitHub commit/push/PR
- Google Drive export/create
- Slack send
- Linear issue mutation
- Zenodo draft/upload/publish
- Stripe or payment action

Blocked by default:

- deletion
- raw private inventory export
- schema mutation without package
- Notion Custom Agents / scheduled AI
- restricted wiki content exposure
- protected duplicate cleanup
- unmarked Block-3 / deep-state normalization
- claims of machine consciousness/personhood

## Implemented Files

| File | Purpose |
| --- | --- |
| `trigger-001.command-surface.md` | Human-readable command rules for `/fff` and Trigger 1-400. |
| `trigger-001.control-crosswalk.csv` | Trigger-to-CAP action crosswalk. |
| `trigger-001.blocked-actions.csv` | Explicit blocked or gated action list. |
| `trigger-001.test-cases.csv` | Test cases for AUTO-001 and manual review. |
| `causal-log.trigger-001-plan-2026-05-17.json` | Causal trace. |

## Control Answer

TRIGGER-001 makes `/fff` operationally useful:

```text
/fff
-> choose next action
-> state boundary
-> perform local/reversible work
-> package external mutation
-> require explicit target GO before writing outside repo
```

This is the working form of bounded autonomy inside CAP 0.3.

## Validation

AUTO-001 validates TRIGGER-001.

Result after implementation:

| Check | Value |
| --- | --- |
| `trigger-001.control-crosswalk.csv` rows | 14 |
| `trigger-001.blocked-actions.csv` rows | 12 |
| `trigger-001.test-cases.csv` rows | 12 |
| AUTO-001 status | `pass` |
| External mutation | 0 |
| Notion AI credits | 0 |
