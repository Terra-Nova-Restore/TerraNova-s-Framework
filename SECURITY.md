# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository or its linked systems (Zenodo, Notion workspace), please report it privately through GitHub's Security Advisory feature (Security tab → Report a vulnerability).

**Do NOT open a public issue** for security-sensitive findings.

## Response Expectations

- First acknowledgement: within 5 business days.
- Status update: within 14 business days, or sooner if validated.
- If accepted: the finding will be fixed, rotated, or quarantined according to the repository's Public Boundary Governance (`docs/governance/public_boundary.md`).
- If declined: a short explanation will be provided.

## Supported Scope

| Area | Supported |
|------|-----------|
| Public repository files (committed to `main`) | ✅ |
| Zenodo published record (`10.5281/zenodo.20073579`) | ✅ |
| GitHub Actions workflows and secrets | ✅ |
| Private raw export archives (not in repo) | ❌ (see `raw/exports/REVIEW_GATE.md`) |
| Notion workspace internals | ❌ (out of scope for this repo) |

## Security Boundaries

This repository enforces a hard public boundary:

- **Public-OK:** Synthesized framework documentation (Track A), hardened control tower metrics, redacted architecture artifacts, abstracted CIC procedures.
- **Blocked:** Raw Notion IDs, unredacted XXL exports, wallet secrets, API keys, patent-sensitive TNPX-01 drafts, `GODFATHER_LOCK` personal logs, private Track C content.

Full policy: `docs/governance/public_boundary.md`

## Credential Hygiene

- No real API keys, tokens, passwords, or secrets may be committed to this repository.
- The repository uses GitHub encrypted secrets (`NOTION_TOKEN`, `GH_PAT`, `ZENODO_API`) for CI/CD.
- If you believe a secret has been leaked, report it immediately and rotate the affected credential.

## Redaction Policy

Redaction tokens used in sanitized public material:
- `[EMAIL_REDACTED]`, `[PHONE_REDACTED]`, `[IBAN_REDACTED]`
- `[WALLET_ADDRESS_REDACTED]`, `[PASSWORD_OR_SECRET_REDACTED]`
- `[PII_CONTEXT_REDACTED]`, `[LOCAL_PATH_REDACTED]`, `[IP_ADDRESS_REDACTED]`

Full policy: `docs/atlas/xxl-dataexport-500k/cycle-01/redaction-policy.md`
