# Public Gate Status — XXL 553k Snapshot

Status: **BLOCKED**

## Current decision

```text
PUBLIC_STATUS: BLOCKED
RAW_PUBLICATION: NO
PUBLIC_EXTRACTS: NO
SAFE_AGGREGATES_ONLY: YES
GITHUB_RAW_PUSH: NO
```

## Gate sources

- CEI-04: automated sensitive review and public gate
- CEI-04A: manual class-3 review and K4 override
- CEI-04B: PII / account / payment scan
- CEI-04C: redaction map and safe public index skeleton

## Sensitive pre-triage summary

| Class | Count | Meaning |
| --- | ---: | --- |
| K0 | 185 | term mentions |
| K1 | 398 | public / technical contexts |
| K2 | 59 | example / placeholder / config contexts |
| K3 | 27 | potential credential / wallet traces |
| K4 | >= 1 | manual override: explicit password / credential-like trace |

## PII / payment blocker summary

| Category | Matches | Lines | Unique | Gate |
| --- | ---: | ---: | ---: | --- |
| Email addresses | 259 | 243 | 59 | redact / never raw-public |
| IBAN | 14 | 14 | 2 | quarantine / redact |
| Phone numbers | 25 | 24 | 15 | redact |
| Wallet / 0x addresses | 15 | 15 | 3 | redact |
| Sensitive URL query traces | 2 | 2 | 2 | quarantine |
| Local user paths | 16 | 16 | 3 | redact |
| IPv4 addresses | 28 | 27 | 10 | review / abstract |

Direct high-risk union: 337 lines contain at least one direct blocker category.

## Stop criteria

Public release remains blocked if any of the following are true:

- raw transcript text would be exposed
- split files would be exposed
- contextual extracts would be exposed
- credential-like values remain present
- PII, account, payment, wallet, local-path, or sensitive URL traces remain unredacted
- claim language treats the snapshot as a complete primary source

## Allowed in public repository

Allowed only as aggregate / index material:

- README
- source classification
- public gate status
- redaction policy
- CEI overview

No raw or contextual content is permitted.
