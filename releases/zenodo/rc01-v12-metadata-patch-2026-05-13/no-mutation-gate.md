# No-Mutation Gate Statement

Status: SUPERSEDED_FOR_METADATA_EXECUTION
Scope: RC01-v12 Zenodo metadata patch review package

## Gate

This package originally did not authorize any Zenodo mutation. That review gate
was superseded by explicit Silvi authorization on 2026-05-13 to execute the
metadata-only update for record `20073579`.

The remaining gate is still active for every non-metadata action.

Authorized now:

- metadata-only update on Zenodo record `20073579`;
- no file, DOI, version, release, or tag action.

## Explicitly Not Authorized

- file upload
- file deletion
- file modification
- new version creation
- DOI reservation
- publish action for a new record or new version
- GitHub release
- Git tag

## Allowed In This Package

- local JSON review
- local documentation review
- public read-only Zenodo record checks
- GitHub draft PR review
- GitHub Actions execution using repository secret `ZENODO_API`, restricted to
  the metadata-only update described in v0.2

## Current Artifact Boundary

The published artifact is still `main (44).pdf` on Zenodo record `20073579`.

`main (45).pdf` is byte-identical to `main (44).pdf`, so it is not a v13
artifact and is not part of this metadata-only patch path.

## Next Authorization Required

The explicit Silvi-Go for metadata execution has been received. A separate
explicit Silvi-Go is still required for any future file, version, DOI, release,
or tag action.
