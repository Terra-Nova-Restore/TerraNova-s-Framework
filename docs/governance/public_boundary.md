# Public Boundary Policy

Status: working governance rule  
Scope: public GitHub repository `Terra-Nova-Restore/TerraNova-s-Framework`

This repository is a public engineering, release, audit and documentation layer. It is not a raw private archive.

## Default stance

Public material must be safe, intentional and reviewable.

Do not add raw exports, private logs, wallet or token details, patent-sensitive mappings, internal trigger canon, restricted security internals or personal data unless the material has been explicitly reviewed and classified as public-safe.

## Allowed in public

The following can be public when reviewed:

- general architecture descriptions
- reviewed dissertation or publication text
- citation metadata and DOI references
- reproducible scripts without secrets
- public release manifests and checksums
- high-level governance rules
- redacted summaries of internal workflows
- non-sensitive issue trackers and review notes

## Keep private or local

The following should stay private, local or in a restricted system unless there is a deliberate review decision:

- API tokens, private keys, access tokens, wallet secrets, seed phrases
- private Notion exports and raw chat exports
- unredacted personal logs, intimate material or private correspondence
- unreleased patent mappings or claim charts
- restricted trigger canon, block-system internals and operational kill-switch details
- raw wallet, token, licence or contract administration data
- unreviewed source packs from Prism, Notion or other working systems

## Classification labels

Use these labels before moving material into public paths:

| Label | Meaning |
| --- | --- |
| `public-ok` | Reviewed and safe for public repository storage. |
| `internal` | Useful for the system but should not be public by default. |
| `redact-candidate` | May become public after removal of sensitive parts. |
| `patent-sensitive` | May affect IP strategy, novelty, claim scope or disclosure timing. |
| `private` | Should not be committed to a public repository. |
| `volatile` | Status, metrics, pricing, roadmap or product claims may change and require re-checking. |
| `canonical` | Reviewed reference source for public-facing claims. |
| `reference` | Useful reference, not automatically canonical. |

## Raw-export rule

Raw exports are not automatically evidence and not automatically public.

Before committing raw exports under `raw/exports/`, confirm:

1. source and date are known,
2. public/private status is classified,
3. sensitive names, tokens, wallet data and private logs are absent or redacted,
4. patent-sensitive material has been reviewed,
5. the file has a purpose beyond volume preservation.

If any item is unclear, use `redact-candidate` or keep the material out of the public repository.

## Zenodo and release rule

Zenodo drafts may be prepared through GitHub Actions only when:

- the artifact path is intentional,
- SHA256 is checked,
- metadata is valid,
- the workflow remains draft-only,
- human review happens before publish.

No automated publish step should be added without a separate governance decision.

## Issue and PR rule

Issues and PRs should describe status honestly:

- Do not inflate maturity.
- Do not convert raw material into canonical claims by wording alone.
- Mark stubs, placeholders and partial exports clearly.
- Prefer `archive` or `hold` over deletion when uncertain.

## Decision rule

When uncertain, choose the safer path:

1. keep local/private,
2. create a redacted summary,
3. open a review issue,
4. only then promote to public.

This file is a guardrail, not a deletion instruction.