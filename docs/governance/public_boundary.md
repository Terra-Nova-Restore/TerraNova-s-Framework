# Public Boundary

Status: BIZ / Governance
Source: Repository-side governance policy for public-safe publication boundaries.
Trace: Issue `#25`, `docs/governance/source_of_record_policy.md`, `raw/exports/REVIEW_GATE.md`
Boundary: Public repository boundary definition only; not a raw storage or canon surface.
Mode: BIZ
GitHub sync state: tracked in this repository as a publish-safety contract.
Notion source awareness: required if this boundary is later mirrored into living governance canon.

## Purpose

This document defines what may be published in the public TerraNova repository and what must remain private, local, redacted, or patent-sensitive.

GitHub is the versioned engineering and research-operations layer. It is not the unrestricted raw memory layer.

## Allowed in the public repository

Public-safe material may include:

- reviewed architecture summaries
- reproducible scripts without secrets
- governance notes and review checklists
- citation, Zenodo, ORCID and provenance anchors
- dissertation/publication drafts after review
- curated atlas outputs with source status
- defensive security notes without exploit instructions
- high-level trigger or CIC concepts when not private, intimate, token-sensitive, or patent-sensitive

## Not allowed in the public repository

Do not commit:

- API keys, passwords, tokens, private keys, seed phrases, wallet secrets or credentials
- private contact data or personally identifying raw logs
- raw intimate logs, Schattenarchiv full texts, consent-sensitive material
- private trigger canon, GODFATHER_LOCK details, internal block-system internals, or restricted VORTEX/Instance-Council mappings
- patent-sensitive implementation mappings unless explicitly cleared
- raw chat exports without classification
- offensive security instructions or exploit playbooks
- commercial terms, prices, token/DAO claims or roadmap commitments unless independently verified and marked with source status

## Classification labels

Use these labels before adding or promoting material:

- `public-ok`: cleared for public repository use
- `internal`: useful internally, not public by default
- `redact-candidate`: requires redaction before publication
- `patent-sensitive`: may expose IP or filing-sensitive mapping
- `private`: must remain out of the public repository
- `token/wallet`: blockchain, token, wallet or credential-adjacent material; requires extra review
- `raw-chat`: raw conversation/export; never promote without review
- `trigger-depth`: trigger/canon depth beyond safe public summary

## Promotion rule

Raw material must pass through a review gate before becoming repository content:

1. Identify source and owner.
2. Assign classification label.
3. Decide target layer: Track A, A.2, B, C, atlas, governance, tooling, or archive.
4. Redact sensitive content where needed.
5. Add provenance note or checksum if relevant.
6. Commit curated material only, not unrestricted raw payloads.

## Default stance

When uncertain: keep local/private, mark `redact-candidate`, and create an issue or review note instead of committing the raw content.
