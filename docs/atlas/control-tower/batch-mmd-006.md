# MMD-006 - CAP Module Registry Package

Date: 2026-05-17

Activation: `MMD-006 - CAP Module Registry Package GO`

Mode: repo-local registry package preparation, then explicitly authorized Notion apply

External mutation: applied after exact authorization

Notion AI credits used: 0

## Purpose

MMD-006 prepares the mutation-safe registry package for the five MMD-005 CAP module drafts.

## Result

- Registry rows: 5
- Field map rows: 27
- View package rows: 2
- Mutation package rows: 4
- Required apply command: `GO Notion MMD-006 anwenden`

## Boundary

The package does not assign canonical `TRG-*` IDs and does not expose raw private IDs.

## Applied Result

Authorization:

```text
GO Notion MMD-006 anwenden
```

Applied Notion changes:

- created five CAP module draft registry rows
- created registry view `CAP Module Drafts`
- created registry view `CAP Module Sync Needed`
- appended an MMD-006 checkpoint to the CAP page

Blocked during apply:

- deletion
- schema change
- canonical `TRG-*` assignment
- raw private inventory export
- expansion of `517`, `777` or `988-992`
