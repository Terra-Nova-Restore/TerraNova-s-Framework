# Raw Exports Review Gate

## Purpose

`raw/exports/` is an intake and evidence area. It may contain placeholders, manifests, checksums, incoming batches and reviewed raw-export infrastructure. It must not become an unrestricted dump zone.

No new raw export should be added without classification.

## Required metadata for new raw exports

Before adding a new raw payload, record:

- source name
- source date
- importer/reviewer
- expected size or line count
- checksum if available
- related issue or decision log
- classification label
- intended target layer
- promotion decision: hold, redact, split, archive, or public-ok

## Classification labels

Use one or more:

- `public-ok`
- `internal`
- `redact-candidate`
- `patent-sensitive`
- `private`
- `token/wallet`
- `raw-chat`
- `trigger-depth`

## Gate checklist

- [ ] Source is identified.
- [ ] File is intentionally placed under `raw/exports/`.
- [ ] Classification label is assigned.
- [ ] Sensitive content was checked.
- [ ] Patent/IP relevance was checked.
- [ ] Token/wallet/credential content was checked.
- [ ] Raw-chat or personal-log status was checked.
- [ ] Target layer is documented.
- [ ] Checksum or manifest exists where useful.
- [ ] Promotion decision is recorded.

## Promotion decisions

- `hold`: keep as local/private or placeholder only.
- `redact`: redact before further use.
- `split`: divide into public and restricted parts.
- `archive`: keep as evidence/archive, not active repo content.
- `public-ok`: cleared for curated public use.

## Operating rule

Incoming raw material may support later Track A/A.2/B/C work, but raw intake is not automatically canonical. Treat raw exports as evidence candidates until reviewed.
