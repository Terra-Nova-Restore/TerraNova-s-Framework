# Repository Roles

## Purpose

This document defines the intended roles of repositories and repository areas in the TerraNova / FerrAI / CIC stack.

A repository role is a boundary contract. It helps prevent mixing public publication, raw evidence, private app code, research drafts and archive material.

## Role vocabulary

### `core`

Primary framework and engineering layer. Contains reviewed docs, scripts, reproducible workflows, public-safe architecture, CI and governance.

### `research`

Scholarly and dissertation-oriented material: drafts, citations, evidence ledgers, source registers, claim/evidence matrices, release notes and Zenodo anchors.

### `raw-docs`

Large or semi-raw source material, incoming batches, export containers, checksums and manifests. Requires review gates before promotion.

### `archive`

Historical snapshots, lockpoints, parked artefacts and frozen references. Archive does not imply public-safe or canonical.

### `release`

Clean publication packages, fixed snapshots, release notes and DOI/Zenodo-facing artefacts. Release material should be reviewed, source-stable and clearly versioned.

### `fork`

Experimental or external-development branch/repo. Forks may diverge and should not be treated as canonical without reconciliation.

### `private-app`

Private implementation, product code, credentials-adjacent logic, internal automation or app surfaces. This role should not be public by default.

## Current public repository stance

`TerraNova-s-Framework` currently acts as a combined `core` + `research` + controlled `raw-docs` repository.

Because it is public, the stricter boundary wins:

- raw material must be gated
- private/patent/token material must be excluded or redacted
- research claims must keep source status
- generated artefacts must be labelled as generated or snapshot where relevant

## Routing rule

When adding material, decide the role before committing:

1. `core`: reviewed framework/tooling/governance
2. `research`: dissertation/evidence/citation layer
3. `raw-docs`: incoming source material with gate
4. `archive`: historical snapshot or lockpoint
5. `release`: publication-ready package
6. `fork`: experiment or divergence
7. `private-app`: keep out of public repo

## Conflict rule

If a file fits multiple roles, use the most restrictive role until reviewed.

Example: a raw export with public passages, patent-sensitive passages and private notes remains `raw-docs` / `redact-candidate`, not `public-ok`.
