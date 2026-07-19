# OAL-001 Slice 2 Combined Execution Contract

Status: `LOCKED`
Mode: `historical_offline_replay`
Execution: `combined`
Parent: GitHub Issue #97
Work item: GitHub Issue #99
Source of record: Notion design page `IPERKA — Autodidaktisches Observatory / Codex Runtime (OAL-1.0)`
Boundary: public-safe historical projections and local-private evidence only; no connector or ledger mutation

## Locked contract

```yaml
execution_mode: combined

internal_gates:
  mode: autonomous_within_authorized_scope
  findings_within_scope: remediate_or_reject_then_controlled_close

stop_only_on:
  - material_finding_outside_authorized_remediation_scope
  - scope_drift
  - permission_gap
  - irreversible_human_decision

on_reject:
  candidate_action: terminate
  rollback: required
  evidence: required
  process_event: required
  final_report: required
  promotion_authorized: false

process_events:
  types: [interruption, restart]
  required_fields: [type, reason, stage, timestamp]

process_observations:
  interruption_count: derived_exactly_from_events
  restart_count: derived_exactly_from_events

efficiency_score:
  enabled: false
  reason: no_isolated_measurement_basis

final_human_gate:
  mode: at_most_once
  trigger: proposed_action_requires_human_authority
```

## Reject semantics

`REJECT` terminates the candidate action. It does not resume or promote the
rejected action. Only rollback, evidence binding, the required process event and
the final report continue to controlled completion. A rejected candidate always
records `promotion_authorized: false`.

## Historical admission boundary

The committed fixture contains redacted projections of records read directly
from the Observatory Learning Ledger on 2026-07-19. Raw records, workspace
locators, object identifiers and private source text are not committed. The
admission claim is limited: connector access verified the projection at
admission time; CI can verify only the committed projection bytes and their
digest.

The three scenarios are:

1. a complete Preflight/Hubble/Postflight triad;
2. a Hubble/Postflight cycle where Preflight was not visible;
3. a Hubble-only cycle where same-cycle ALMA records were not visible.

Missing visibility remains a visibility state. It is never converted into a
fabricated connector or system failure.

## 888 calibration

- Observed: approximately 350 percent of a weekly quota was consumed during
  Slice 1.
- Strongly inferred, not isolated: fragmented mini-gates materially contributed
  to the consumption.
- Slice 2 records exact interruption and restart events, with reason, stage and
  timestamp.
- No numeric efficiency score is emitted because no isolated measurement basis
  exists.

## Non-actions

The runtime performs no connector access, Notion write, Learning Ledger write,
remote Git mutation, workflow execution, merge, publication, payment mutation,
production activation or Zenodo mutation. A draft pull request may present the
implementation for review, but it does not authorize merge or promotion.
