# CANON-002 - Canon Admission Rulebook

Date: 2026-05-17

Activation: `GO CAP 0.4 IPERKA`

Mode: repo-local canon governance boot

External mutation: none

Notion AI credits used: 0

## Purpose

CANON-002 defines how CAP decides what may enter canon, at which level, from which source tier and with which blocked claims.

## Inputs

- `mmd-007.cap-module-source-review.md`
- `mmd-007.source-review.csv`
- `mmd-007.canon-decision-queue.csv`
- `cap-0.3-operational-control-iperka.md`
- `sens-001.boundary-map.csv`
- `trigger-001.command-surface.md`

## Outputs

- `cap-0.4-canon-admission-iperka.md`
- `canon-admission-rulebook.md`
- `canon-source-tier-map.csv`
- `canon-elevation-queue.csv`
- `causal-log.cap-0.4-iperka-2026-05-17.json`

## Result

CAP 0.4 is now the local admission layer between useful material and canon status.

Immediate decisions:

- `516`, `520`, `540` and `544` stay L2 internal routing markers.
- `521` stays L1 protected name/cluster.
- no canonical `TRG-*` assignment is created.
- no execution rule or public canon claim is created.
- live Notion registry updates require a later explicit apply package and GO.

## Boundary

This batch does not mutate Notion, GitHub remote, Zenodo, Google Drive, Slack, Linear or Stripe. It only creates repo-local governance artifacts and AUTO-001 check coverage.
