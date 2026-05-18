# DASH-ZEN-002 - Zenodo Source and Sensitivity Pass

Status: applied to Notion registry on 2026-05-18
Date: 2026-05-18
Parent gate: `DASH-ZEN-001`
Mutation policy: live Notion metadata update applied after explicit approval `DASH-ZEN-002 GO`

## Purpose

`DASH-ZEN-002` closes the first source and sensitivity pass over the new
Zenodo dashboard structure that was indexed by `DASH-ZEN-001`.

The pass does not republish Zenodo, does not change DOI/version metadata, does
not create new public canon, and does not copy manuscript, patent, token or
private passages into GitHub.

## Sources Checked

Primary live Notion sources:

- `Zenodo` root page.
- `Monographie - Teil I`.
- `Monographie - Teil II`.
- `Monographie - Teil III`.
- `Zenodo-Z1 - Routing-State Anchor (DEFERRED)`.
- `Zenodo-Z2 - Routing-State Anchor (UPDATED / CLOSED)`.
- `Zenodo-Z3 - Routing-State Anchor (Metadata Refresh, RC01-v12)`.
- CAP registry data source schema.

Supporting repo-local and public sources:

- `docs/references/zenodo.md`
- `docs/atlas/control-tower/batch-dash-zen-001.md`
- `docs/atlas/control-tower/prism-002.zenodo-live-delta-2026-05-17.json`
- public Zenodo record `10.5281/zenodo.20073579`

## Decision

The Zenodo root and `Monographie - Teil I` are now source-reviewed internal
routing references.

The heavier monographie pages remain sensitive source clusters:

- `Monographie - Teil II` stays at `L1-NAME-CLUSTER` with sensitivity hold.
- `Monographie - Teil III` stays at `L1-NAME-CLUSTER` with sensitivity hold.

The newly reachable Z1/Z2/Z3 routing anchors are acknowledged as relevant
historical control-state sources, but no new registry rows are created in
`DASH-ZEN-002`. They are queued for `DASH-ZEN-003` because they need their own
anchor-row package.

## Allowed Claims

- The Zenodo root page is an internal Notion dashboard mirror for the RC01-v12
  record and child monographie routing.
- `Monographie - Teil I` is a source-reviewed internal reference entry point
  for the monographie material.
- `Monographie - Teil II` contains heavier appendix, source-index and
  implementation-adjacent material and must stay sensitivity-bound.
- `Monographie - Teil III` contains return-path, Track-C, appendix and
  faksimile-adjacent material and must stay sensitivity-bound.
- Z1/Z2/Z3 are reachable routing-state anchors and should be indexed in the
  next dashboard package.

## Blocked Claims

- The Notion monographie pages are final public canon.
- `Monographie - Teil II` or `Monographie - Teil III` may be elevated without
  splitting sensitive material from publishable claims.
- The Notion Zenodo dashboard authorizes a Zenodo republish, DOI mutation,
  concept DOI mutation, upload, new version or publish event.
- Z1/Z2/Z3 are registry-complete in `DASH-ZEN-002`.
- Notion Custom Agents or credit-consuming Notion AI automation are required.

## Causal Chain

```plain text
Notion integration reachability improved
-> Zenodo root and child pages searched
-> Z1/Z2/Z3 routing anchors detected
-> existing DASH-ZEN-001 registry rows reviewed first
-> root and Teil I raised to L2 internal reference state
-> Teil II and Teil III held at L1 sensitivity boundary
-> Z1/Z2/Z3 queued for a separate anchor package
-> CAP 0.1.0 checkpoint and GitHub trace updated
```

## Notion State

Live registry mutation completed after explicit approval.

Updated registry rows:

- `DASH-ZEN-001 - Zenodo Root`
- `DASH-ZEN-001 - Monographie Teil I`
- `DASH-ZEN-001 - Monographie Teil II`
- `DASH-ZEN-001 - Monographie Teil III`

CAP 0.1.0 also records the `DASH-ZEN-002` checkpoint.

## Done Criteria

`DASH-ZEN-002` is complete when:

- existing Zenodo dashboard registry rows carry reviewed source/sensitivity
  decisions.
- Z1/Z2/Z3 are acknowledged as reachable context without being silently
  admitted as new registry rows.
- GitHub trace has no raw private Notion IDs.
- local CAP control checks pass, including live Zenodo read.
- PR #48 branch is pushed with the new trace.

Status: complete.
