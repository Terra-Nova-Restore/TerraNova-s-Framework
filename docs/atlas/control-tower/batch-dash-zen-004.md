# DASH-ZEN-004 - Zenodo Release-State Matrix

Status: applied to Notion registry on 2026-05-18
Date: 2026-05-18
Parent gate: `DASH-ZEN-003`
Mutation policy: live Notion registry row creation applied after explicit
activation `DASH-ZEN-004`

## Purpose

`DASH-ZEN-004` reconciles the live Zenodo record, the Notion Zenodo dashboard
root, and the Z1/Z2/Z3 routing anchors into one release-state matrix.

This package creates a control artifact. It does not edit Zenodo, does not
advance any PR, does not run any workflow, and does not change DOI, files,
version labels, or publication state.

## Current Authority Order

1. **Zenodo API / public record** is the current external citation and release
   authority.
2. **Notion Zenodo root** is the internal dashboard mirror and routing surface.
3. **Z1/Z2/Z3 anchors** are historical routing-state anchors and hard-lock
   precedents.
4. **GitHub Atlas** is the auditable interpretation and control trace for this
   matrix.

## Live Zenodo State

Live read on 2026-05-18 through `AUTO-001 --live-zenodo`:

- Record: `20073579`
- DOI: `10.5281/zenodo.20073579`
- Concept DOI: `10.5281/zenodo.19774446`
- Version: `RC01-v12`
- Publication date: `2026-05-17`
- Modified: `2026-05-17T05:20:40.751823+00:00`
- File: `main (44).pdf`
- File checksum: `md5:d791d480e75f3d89f9a103a28a5c5001`
- File size: `2943457`

## Reconciliation

`Z1` remains parked and does not represent live release state.

`Z2` remains a closed metadata-only correction precedent. It proves that a
metadata-only update can be executed while preserving file/version/DOI/publish
hard locks.

`Z3` remains a closed metadata-refresh precedent. Because the public Zenodo
record was modified again on 2026-05-17, Z3 is not the sole latest-state
authority. Current-state claims must route through the live API/root matrix.

The Notion Zenodo root is the internal dashboard mirror for the current
publication state. It should not be used as a substitute for a live API check
when making current external claims.

## Allowed Claims

- RC01-v12 is the current public Zenodo version represented by record
  `20073579`.
- The current external citation state must be verified through Zenodo API or
  public Zenodo record before publication-sensitive claims.
- Z1, Z2 and Z3 remain useful historical state anchors.
- Z2 and Z3 can be reused as hard-lock precedents for future metadata-only
  lanes.

## Blocked Claims

- `DASH-ZEN-004` authorizes a Zenodo write.
- Z1 may be advanced from this matrix.
- Z2 or Z3 authorize new metadata edits.
- Z3 is the sole latest-state authority after the 2026-05-17 live update.
- The Notion dashboard root alone proves current external Zenodo state.
- Any raw private Notion IDs, tokens, secrets or manuscript material belong in
  this public GitHub trace.

## Causal Chain

```plain text
DASH-ZEN-003 creates Z-anchor rows
-> DASH-ZEN-004 requested
-> live Zenodo API read confirms current RC01-v12 state
-> Notion root and Z-anchor history reconciled
-> release-state matrix created in GitHub
-> one Matrix registry row created in Notion
-> CAP 0.1.0 checkpoint appended
```

## Done Criteria

`DASH-ZEN-004` is complete when:

- a release-state matrix exists in GitHub.
- one CAP registry row points to the matrix artifact.
- CAP 0.1.0 records the checkpoint.
- local checks pass with live Zenodo read.
- raw private Notion IDs are absent from GitHub artifacts.

Status: complete.
