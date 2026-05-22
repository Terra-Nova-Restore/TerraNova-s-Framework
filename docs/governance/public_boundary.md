# Public Boundary Governance

Status: BIZ / Public-boundary governance
Source: Repository-local governance file, aligned with Equilibrium public/private separation.
Trace: Required by `scripts/validate_docs.py`; supports Control Tower publication gates.
Boundary: Defines public repository boundaries only; does not authorize external publication or Notion/Zenodo mutation.
Mode: BIZ
GitHub sync state: tracked in this repository.
Notion source awareness: Notion remains the internal system of record for live workspace state.

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
