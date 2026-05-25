# Public Boundary Governance

## Purpose
Defines the absolute boundary of what can be committed to the public `TerraNova-s-Framework` repository.

## Allowed in Public (Public-OK)
- Synthesized framework documentation (Track A).
- Hardened control tower metrics, matrices, and gates.
- Redacted architecture artifacts.
- Abstracted CIC procedures.

## Strictly Private / Local (Blocked)
- Raw Notion ID links (`collection://`, workspace internals).
- Unredacted `XXL_DatenExport` files.
- Wallet secrets, API keys, or raw token deployment artifacts.
- Patent-sensitive (TNPX-01) internal draft documents.
- `GODFATHER_LOCK` flagged personal/intimate logs.
- Internal triggers and private Metarotik (Track C) content not cleared for public release.

## The `redact-candidate` Class
Items classified as `redact-candidate` hold structural value but currently contain PII, private IDs, or sensitive paths. They must undergo the Sensitive Review Gate (e.g., DASH-VIEW-02) and be fully sanitized before pushing.

## Raw-Exports
Raw exports must never touch the `main` branch unless pre-classified and heavily scrubbed. All raw exports land in local staging or isolated private storage first.

## Public Derivative Exception

Some tracked files under `raw/exports/incoming/` are manuscript or appendix
derivatives rather than private raw dumps. They are allowed only as bounded
public-review artifacts when they have checksum sidecars, classification, and no
detected secrets or direct PII. They do not weaken the raw-export rule.

Any future derivative that contains credential-like values, direct PII, raw
Notion IDs, protected patent-source material, Track C, `GODFATHER_LOCK`, or
private-session content must leave the public lane and be represented only by a
redacted manifest or checksum pointer.
