# Redaction Policy — XXL 553k Snapshot

Status: **PUBLIC-SAFE INDEX ONLY**

## Marker

- NICHTS davon ist ewig.
- NICHTS ist fix.
- NICHTS ist nicht weiter belegbar.

## Purpose

This policy defines the public-safe redaction rules for the restricted XXL snapshot index. It does not publish raw transcript content, contextual extracts, sensitive matches, or review lines.

## Redaction tokens

| Risk source | Token | Public rule |
| --- | --- | --- |
| Email address | `[EMAIL_REDACTED]` | never publish full value |
| Phone number | `[PHONE_REDACTED]` | never publish full value |
| IBAN / bank trace | `[IBAN_REDACTED]` | quarantine and redact |
| Wallet / 0x address | `[WALLET_ADDRESS_REDACTED]` | publish only as abstract category |
| Sensitive URL query | `[SENSITIVE_URL_REDACTED]` | quarantine; no query strings |
| Local user path | `[LOCAL_PATH_REDACTED]` | generic category only |
| IP address | `[IP_ADDRESS_REDACTED]` | aggregate or abstract only |
| Password / secret / key | `[PASSWORD_OR_SECRET_REDACTED]` | rotate/quarantine; never public |
| Person / account context | `[PII_CONTEXT_REDACTED]` | review before any public mention |

## Public gate rules

```text
IF raw_content THEN reject
IF split_file THEN reject
IF contextual_extract THEN reject
IF credential_like_value THEN quarantine
IF pii_or_payment_trace THEN redact
IF aggregate_only THEN candidate_safe
IF candidate_safe AND wording_review THEN safe_index_allowed
```

## Explicitly forbidden in this public repository

- raw dump files
- split transcript files
- contextual extracts
- sensitive match CSV files
- manual review context files
- complete wallet addresses
- API keys, secrets, passwords, tokens, bearer strings
- personal contact details
- banking or payment identifiers
- local device or account paths

## Allowed as public-safe index material

- line counts
- file hashes
- source classification
- aggregate class counts
- redaction policy
- gate status
- CEI layer overview
- links to issue / PR / public-safe docs

## Batch footer requirement

Every future analysis batch must include a short Gedankennotiz:

- What could still be missing?
- What next source would be useful?
- Which suggestions should be saved for the final evaluation discussion?

## Status

```text
RAW_PUBLICATION: no
PUBLIC_EXTRACTS: no
SAFE_AGGREGATES_ONLY: yes
NEXT_GATE: CEI overview and draft PR review
```
