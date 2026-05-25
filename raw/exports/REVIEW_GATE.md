# Raw-Export Review Gate

## Hard Rule
**No new raw data may be committed to this repository without explicit classification.**

Before any raw export is pushed, it must be assigned one of the following classifications:

- `public-ok`: Fully sanitized, safe for public repository viewing.
- `internal`: For organization/local use only. DO NOT PUSH to public repo.
- `redact-candidate`: Needs scrubbing of PII/Notion IDs before it can become `public-ok`.
- `patent-sensitive`: Protected under TNPX-01 filing hold. DO NOT PUSH.
- `private`: Personal, `GODFATHER_LOCK` or Track C sensitive logs. DO NOT PUSH.

## Incoming Derivative Lane

`raw/exports/incoming/` is a bounded derivative lane for manuscript, appendix
and pre-release intake batches. It is not a general raw-dump folder.

Allowed in this lane:

- public-safe manuscript or appendix derivatives;
- checksum sidecars for those derivatives;
- short intake fragments that have passed the same boundary scan as the parent
  artifact;
- transitional material needed to reconstruct a public release package.

Blocked in this lane:

- unredacted transcript dumps;
- raw Notion exports or internal page/database ID lists;
- credential-like strings, wallet secrets, API keys, private keys or bearer
  tokens;
- direct personal contact, banking, account, payment or device-path data;
- unreviewed TNPX-01 patent source packages;
- Track C, `GODFATHER_LOCK`, intimate or private-session material unless a
  separate publication gate explicitly clears a redacted excerpt.

The legacy fill helper must keep generated raw payloads under
`raw/exports/local-private/`. The tracked placeholder files are not publication
targets.

## Retention and Promotion

Tracked incoming derivatives are temporary review artifacts. They may remain in
the public repository only while they serve one of these purposes:

- release reconstruction;
- checksum-backed provenance;
- public-safe appendix/manuscript review;
- controlled migration into curated docs.

Promotion path:

```text
incoming derivative
  -> sensitivity scan
  -> classification note
  -> curated doc / public index / release artifact
  -> keep checksum or retire source derivative
```

Exit path:

```text
private or sensitive finding
  -> remove from public lane
  -> preserve checksum/audit pointer only
  -> store source in private/local archive
```

## Required Checks

Every new or changed incoming derivative must pass:

- `git diff --check`;
- secret-pattern scan for GitHub, Notion, Zenodo, OpenAI, wallet and private-key
  markers;
- PII/account scan for email, phone, IBAN, IP address and local user paths;
- manual boundary review for patent-sensitive and Track-C material.
