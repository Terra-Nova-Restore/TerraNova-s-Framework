# Zenodo-Ready Package: Semantic Spine v0.1

Status: release-ready review package, not externally uploaded
Source: GitHub public semantic architecture spine and public release candidate
Trace: prepared 2026-05-25 after PR #62 publication
Boundary: no Zenodo mutation in this package; no raw Notion URLs, no raw exports, no protected TNPX-01 draft details
Mode: SYNC / release preparation
GitHub sync state: prepared for public GitHub review
Notion source awareness: Notion remains a living source layer; this package cites only GitHub-visible public-safe artifacts

## Package Purpose

This directory stages the citable public semantic architecture release for a
future Zenodo metadata/upload step.

It is intentionally a review package, not proof of a completed Zenodo upload.

## Primary Artifact

| Field | Value |
| --- | --- |
| Title | TerraNova / FerrAI Semantic Architecture Public Release v0.1 |
| Version | v0.1 |
| Prepared | 2026-05-25 |
| Primary file | `docs/public/semantic_architecture_public_release_v0_1.md` |
| Rendered HTML | `semantic_architecture_public_release_v0_1.html` |
| Rendered PDF | `semantic_architecture_public_release_v0_1.pdf` |
| Registry bridge | `docs/atlas/semantic_spine_registry.md` |
| Architecture spine | `docs/architecture/public_semantic_architecture_spine.md` |

## Living Flow

The four release steps are represented as local artifacts:

| Step | Artifact | State |
| --- | --- | --- |
| 1. Render whitepaper/PDF | `semantic_architecture_public_release_v0_1.html` and `.pdf` | Generated |
| 2. Prepare Zenodo metadata | `zenodo_metadata.semantic-spine-v0.1.review.json` | Review-ready |
| 3. Prepare GitHub tag/release | `github_release_draft.semantic-spine-v0.1.md` | Draft-ready |
| 4. Gate Zenodo upload | `zenodo_upload_gate.semantic-spine-v0.1.md` | Explicit-GO gate |

The reproducible builder is:

```powershell
python scripts/build_semantic_spine_release.py --github-commit ad8da3e67d1f27b144d5585908df4c42626ee70e
```

## Release Scope

The release covers:

- Semantic Trigger Architecture
- Semantic Core Layer (SCL)
- Iterative Interaction Collapse
- Recursive-Iterative Interaction Collapse
- Lenhard Decoding Module (LDM)
- Lenhard Model
- Mermaid Cluster

## Publication Boundary

Blocked from this package:

- raw Notion page URLs and page IDs
- raw exports or chat transcripts
- protected TNPX-01 filing drafts or claim mechanics
- private trigger tables
- wallet, token or operational secret material
- medical, psychological, legal or patent grant claims

## Next External Step

Before Zenodo upload:

1. Confirm metadata and license.
2. Decide whether to upload Markdown only or render an additional PDF.
3. Attach the source GitHub commit/PR reference.
4. Perform the explicit Zenodo upload/update action.

