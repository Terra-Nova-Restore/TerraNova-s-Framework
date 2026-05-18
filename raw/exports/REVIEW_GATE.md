# Raw-Export Review Gate

## Hard Rule
**No new raw data may be committed to this repository without explicit classification.**

Before any raw export is pushed, it must be assigned one of the following classifications:

- `public-ok`: Fully sanitized, safe for public repository viewing.
- `internal`: For organization/local use only. DO NOT PUSH to public repo.
- `redact-candidate`: Needs scrubbing of PII/Notion IDs before it can become `public-ok`.
- `patent-sensitive`: Protected under TNPX-01 filing hold. DO NOT PUSH.
- `private`: Personal, `GODFATHER_LOCK` or Track C sensitive logs. DO NOT PUSH.
