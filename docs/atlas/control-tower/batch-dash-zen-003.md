# DASH-ZEN-003 - Zenodo Routing Anchor Registry Package

Status: applied to Notion registry on 2026-05-18
Date: 2026-05-18
Parent gate: `DASH-ZEN-002`
Mutation policy: live Notion registry row creation applied after explicit
activation `DASH-ZEN-003`

## Purpose

`DASH-ZEN-003` turns the now reachable Zenodo routing-state anchors into
explicit CAP registry rows.

The package covers:

- `Zenodo-Z1 - Routing-State Anchor (DEFERRED)`.
- `Zenodo-Z2 - Routing-State Anchor (UPDATED / CLOSED)`.
- `Zenodo-Z3 - Routing-State Anchor (Metadata Refresh, RC01-v12)`.

These rows document historical control-state and routing boundaries. They do
not execute, merge, publish, upload, reserve DOI, create a Zenodo draft, or
open a new cycle.

## Source Interpretation

`Z1` is a deferred/backlog routing anchor. It records that a GitHub-only draft
preflight lane existed, that it was not executed, and that Zenodo/DOI remained
untouched.

`Z2` is a closed metadata-only execution anchor. It records the RC01-v12
metadata correction lane and the hard locks that kept file, version, DOI and
publish state unchanged.

`Z3` is a closed metadata-refresh anchor. It records the later metadata refresh
lane and its hard-lock verification. Because the live Zenodo root/API received
later metadata activity on 2026-05-17, `Z3` is a historical lane anchor, not the
sole latest-state authority.

## Registry Decision

All three Z-anchors are admitted as `L2-ROUTING-MARKER` rows with
`Source Review Passed`.

They are not L3/L4 module semantics and not executable Zenodo instructions.

## Allowed Claims

- Z1/Z2/Z3 are internal routing-state anchors for Zenodo-related work.
- Z1 is deferred and must stay parked until a separate explicit opening.
- Z2 is closed and can be used as metadata-only hard-lock precedent.
- Z3 is closed and can be used as metadata-refresh hard-lock precedent.
- Live Zenodo truth still routes through the public Zenodo API and the current
  Zenodo root dashboard row.

## Blocked Claims

- Z1 authorizes PR #40 merge, workflow execution or RC01-v13 publication.
- Z2 authorizes further Zenodo writes.
- Z3 is the sole latest live-state authority after the 2026-05-17 refresh.
- Any Z-anchor authorizes file upload, DOI mutation, concept DOI mutation, new
  version, publish event, secret exposure or token handling.
- Any Z-anchor imports raw private Notion content into public GitHub artifacts.
- Any Z-anchor consumes Notion AI credits or requires a Notion Custom Agent.

## Causal Chain

```plain text
DASH-ZEN-002 detects reachable Z-anchors
-> no duplicate registry row found
-> Z1/Z2/Z3 fetched through Notion connector
-> each anchor classified by routing state and hard locks
-> three L2 routing marker registry rows created
-> CAP 0.1.0 checkpoint appended
-> GitHub trace updated and validated
```

## Notion State

Created registry rows:

- `DASH-ZEN-003 - Zenodo Z1 Routing Anchor`
- `DASH-ZEN-003 - Zenodo Z2 Routing Anchor`
- `DASH-ZEN-003 - Zenodo Z3 Routing Anchor`

CAP 0.1.0 records the `DASH-ZEN-003` checkpoint.

## Done Criteria

`DASH-ZEN-003` is complete when:

- all three Z-anchors have explicit CAP registry rows.
- Z1 remains parked.
- Z2 and Z3 remain closed historical anchors.
- no Zenodo mutation or GitHub PR action is executed.
- no raw private Notion IDs are present in GitHub artifacts.
- local CAP control checks pass, including live Zenodo read.

Status: complete.
