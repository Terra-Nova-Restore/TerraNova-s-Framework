# DASH-ZEN-001 - Zenodo Dashboard Registry Sync

Status: applied to Notion registry on 2026-05-18
Date: 2026-05-18
Parent gate: `CAP 0.4 - Canon Admission`
Mutation policy: live Notion metadata update applied after explicit approval `genauso mache mers`

## Purpose

`DASH-ZEN-001` closes the dashboard drift introduced by the new Notion
`Zenodo` page and its three monographie underpages.

The control tower had repo-local Zenodo evidence and older registry rows for
`Zenodo RC01-v12 reference`, `Zenodo RC01-v12 release mirror` and
`PRISM-001 Backpropagation Queue`, but the new live Notion structure was not
yet represented in the CAP registry.

## Sources Checked

Primary live Notion sources:

- `Zenodo` root page.
- `Monographie - Teil I`.
- `Monographie - Teil II`.
- `Monographie - Teil III`.
- CAP registry data source schema.

Supporting repo-local sources:

- `docs/references/zenodo.md`
- `docs/atlas/control-tower/prism-002.zenodo-live-delta-2026-05-17.json`
- `docs/atlas/control-tower/batch-pr-048-gate.md`

## Decision

The new Zenodo Notion structure is admitted as a dashboard/control surface, not
as a public-canon elevation.

Applied registry rows:

- `DASH-ZEN-001 - Zenodo Root`
- `DASH-ZEN-001 - Monographie Teil I`
- `DASH-ZEN-001 - Monographie Teil II`
- `DASH-ZEN-001 - Monographie Teil III`

## Boundaries

Allowed now:

- Registry visibility for the new live Zenodo hub.
- Root page as `L2-ROUTING-MARKER`.
- Monographie pages as `L1-NAME-CLUSTER` until deeper source/sensitivity pass.
- Prism / Zenodo feedback target on all four rows.
- Internal dashboard routing and follow-up queueing.

Still blocked:

- deletion or movement of Notion pages.
- raw private Notion IDs in public GitHub artifacts.
- treating Notion monographie pages as final public canon.
- republishing Zenodo or changing DOI/version metadata.
- importing sensitive manuscript, patent, token or private passages into public
  control artifacts.
- Notion Custom Agent use or credit-consuming AI automation.

## Notion State

Live registry mutation completed after explicit approval.

The CAP registry now has four new dashboard rows that connect the new Notion
`Zenodo` root and its three child pages back to the Prism / Zenodo feedback
loop.

The CAP 0.1.0 control page also records the DASH-ZEN-001 checkpoint.

## Done Criteria

`DASH-ZEN-001` is complete when:

- new Zenodo root and child pages are represented in the CAP registry.
- L2/L1 boundary is explicit.
- sensitivity hold is applied to the heavier monographie pages.
- GitHub trace is present without raw private Notion IDs.
- AUTO-001 validates the new trace files.

Status: complete.
