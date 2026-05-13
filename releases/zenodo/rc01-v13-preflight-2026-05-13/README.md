# Zenodo RC01-v13 Preflight

Status: PREPARED / NO ZENODO MUTATION
Date: 2026-05-13
Target record: `20073579`
Current published version: `RC01-v12`
Next candidate version: `RC01-v13`

## Purpose

This package repairs the repository-side preflight lane for a future
`RC01-v13` Zenodo version of the TerraNova / FerrAI / CIC work monograph.

It does not create a Zenodo draft, reserve a DOI, upload a file, or publish a
record. It prepares the GitHub-controlled validation surface so a later explicit
Silvi-Go can create a draft from reviewed inputs.

## Current Findings

- The current published Zenodo record is `20073579`.
- The current DOI is `10.5281/zenodo.20073579`.
- The concept DOI is `10.5281/zenodo.19774446`.
- The current published version is `RC01-v12`.
- The repository mirror artifact is under `releases/zenodo/rc01-v12-2026-05-07/`.
- Local `main (45).pdf` is byte-identical to published `main (44).pdf`.

Because there is no distinct `RC01-v13` content artifact yet, this package does
not stage a PDF for upload.

## Included Files

- `manifest.json`: preflight facts, locks, target record, and required Z2 inputs.
- `OK_CHECKLIST.md`: human review checklist before any Zenodo draft action.
- `zenodo_api_metadata.rc01-v13.draft.json`: draft metadata payload for later review.

## Workflow

The companion workflow is:

```text
.github/workflows/zenodo-rc01-v13-preflight.yml
```

It performs repository-side validation and public Zenodo read checks only. It
must not call Zenodo write endpoints.

## Hard Locks

- Zenodo draft: no
- Zenodo upload: no
- Zenodo publish: no
- DOI reservation: no
- Raw dump or private excerpts: no
- `main (45).pdf` as v13 payload: no, because it is byte-identical to RC01-v12

## Z2 Entry Criteria

Before a later draft-creation cycle starts, provide:

- a new public-safe PDF artifact that differs from RC01-v12
- its SHA-256 and MD5
- reviewed RC01-v13 metadata
- explicit Silvi-Go for Zenodo draft creation
- confirmation that Zenodo remains a draft-only action until manual publish OK
