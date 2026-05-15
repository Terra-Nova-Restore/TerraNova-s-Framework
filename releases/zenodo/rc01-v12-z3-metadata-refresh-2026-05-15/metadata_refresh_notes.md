# RC01-v12 Z3 Metadata Refresh Notes

Status: REVIEW_ONLY_NO_MUTATION
Source: external independent triage 2026-05-15 04:06 CEST
Authority: Silvi lane-opening 2026-05-15 04:08-04:15 CEST
Notion anchor: `Zenodo-Z3 -- Routing-State Anchor (Metadata Refresh, RC01-v12)`

## Purpose

This package prepares a metadata-only refresh for the existing Zenodo record
`20073579`. It updates the public-facing title, description/abstract, and
keywords to match the current FerrAI-TerraNova CIC framework positioning after
ZIP Cycle 3 closeout.

This is a refresh, not a republish. It does not request a new version, file
upload, DOI mutation, concept DOI change, related-identifier change, license
change, upload-type change, or publication-chain change.

## Target

- Record ID: `20073579`
- DOI: `10.5281/zenodo.20073579`
- Concept DOI: `10.5281/zenodo.19774446`
- Version: `RC01-v12`
- File: `main (44).pdf`

## Fields Intended To Change

- `metadata.title`
- `metadata.description`
- `metadata.keywords`
- `metadata.notes` only to document the metadata-only Z3 refresh boundary

## Fields Intended To Remain Unchanged

- `metadata.custom.code:codeRepository`
- `metadata.related_identifiers`
- `metadata.references`
- `metadata.license`
- `metadata.upload_type`
- `metadata.publication_type`
- `metadata.publication_date`
- `metadata.creators`
- `metadata.version`
- file list and file checksum
- DOI and concept DOI

## Cross-Lane Constraints

- Cycle 3 is closed; this lane does not reopen it.
- Cycle 4 is not opened by this lane.
- Z1 / PR #40 remains parked and untouched.
- Z2 is closed and remains untouched except as precedent.
- CEI-DATA-05 remains deferred.
- Phase C pipeline hardening remains deferred.

