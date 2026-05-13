# RC01-v12 Zenodo Metadata Patch Notes

Status: REVIEW_ONLY_NO_MUTATION
Target record: `20073579`
Specific DOI: `10.5281/zenodo.20073579`
Concept DOI: `10.5281/zenodo.19774446`
Current version: `RC01-v12`

## Purpose

This package prepares a reviewable metadata-only patch candidate for the
existing published Zenodo record `20073579`.

It does not update Zenodo. It does not create a new version. It does not change
the published PDF.

## Why This Patch Exists

The current public metadata is fundamentally correct: title, DOI, concept DOI,
version, ORCID, repository link, license, language, and file checksum all match
the repository-side RC01-v12 anchors.

The main improvement candidate is the description field. The current Zenodo
description contains exported Notion wrapper markup and an older
reference-snapshot wording. The proposed patch keeps the substance but turns it
into clean Zenodo-facing HTML and names `RC01-v12` explicitly.

## No File Update

`main (45).pdf` was checked and is byte-identical to the published
`main (44).pdf`:

```text
SHA256: 1e9ce2f810b0af8c245887bb3a01ebcb01ca8f90c971bd5cf39da47a6b8dda40
MD5:    d791d480e75f3d89f9a103a28a5c5001
```

Therefore there is no v13 artifact and no file update path in this package.

## Proposed Metadata Behavior

- Keep the record title unchanged.
- Keep `RC01-v12` unchanged.
- Keep DOI and concept DOI unchanged.
- Keep ORCID `0009-0007-8033-3508`.
- Keep license `cc-by-4.0`.
- Keep language `deu`.
- Keep repository relationship to `Terra-Nova-Restore/TerraNova-s-Framework`.
- Replace only the review-targeted metadata text with cleaner HTML if later
  approved.

## Execution Boundary

This package is a review surface only. Any actual Zenodo metadata update
requires a later explicit Silvi-Go and a separate execution step.
