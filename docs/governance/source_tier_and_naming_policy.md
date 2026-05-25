# Source-Tier and Naming Policy

Status: BIZ / Governance
Source: Issue #13 K-020/K-021 and repository-side naming cleanup already present in CIC atlas docs.
Trace: Issue #13; `docs/governance/source_of_record_policy.md`; `docs/ai/cic_atlas_usage.md`; `docs/ai/prism_atlas_usage.md`.
Boundary: Public naming and source-tier policy only. It does not decide a final external product name.
Mode: BIZ
GitHub sync state: tracked in this repository; validate with `scripts/validate_docs.py`.
Notion source awareness: Notion may contain richer source pages, but public claims require reviewed repository or publication anchors.

## K-020: Reference Is Not Canon

Repository work distinguishes source tiers before upgrading a claim.

| Tier | Meaning | Default use |
| --- | --- | --- |
| `canonical` | Reviewed source treated as current canon for a defined scope | Stable docs, release anchors, approved rule mirrors |
| `verified` | Directly checked against an inspectable source | Facts, dates, IDs, checksums, CI state |
| `reference` | Useful supporting source, not final truth | Notion pages, FAQs, runbooks, dashboard notes |
| `historical` | Accurate for a prior state, superseded by newer evidence | Older issues, old release notes, old metadata deltas |
| `volatile` | Likely to change or externally dependent | stats, traffic, prices, product status, public platform state |
| `open` | Not yet resolved | decisions, naming, unresolved status questions |
| `redact-candidate` | Structurally useful but sensitive until reviewed | raw exports, private IDs, protected source lanes |

## Promotion Rule

A claim can move upward only when the next artifact carries enough evidence for
the target tier.

```text
reference -> verified -> canonical
```

Promotion requires:

- a source path, DOI, issue, PR, commit, checksum or live read;
- a clear scope boundary;
- no unresolved public-boundary or redaction blocker;
- a date when the source is volatile.

## K-021: Prism Naming Boundary

`Prism` is not hardened as a TerraNova external product name.

Use this public distinction:

- `CIC atlas` = repository-facing TerraNova atlas and governance layer.
- `OpenAI Prism` = external editor/source context where explicitly meant.
- `Prism` alone = legacy/internal shorthand only, not a market-facing product name.
- `[WedgeName]` or `Authoring Cockpit` = placeholder for future naming review.

## Public Wording Rule

Do not publish landing-page, pitch or website copy that presents `Prism` as the
final external product name before a naming review is complete.

Preferred public category:

```text
high-trust authoring cockpit for complex, source-critical, versioned documents
```

## Relationship To Existing Docs

`docs/ai/cic_atlas_usage.md` already applies the naming direction by using CIC
as the project-facing atlas name while allowing OpenAI Prism as an external
source/editor context.

`docs/ai/prism_atlas_usage.md` remains a legacy compatibility note and must not
be read as external naming approval.
