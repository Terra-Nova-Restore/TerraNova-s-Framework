# Codex Task Routing

Status: BIZ / Codex-Routing
Source: Technical mirror of FerrAI Operating Kernel v0.1 routing logic.
Trace: `docs/architecture/ferrAI_operating_kernel_v0.1.md`
Boundary: Routing guidance for Codex work; not a replacement for Notion canon.
Mode: BIZ
GitHub sync state: tracked in this repository; validate through `scripts/validate_docs.py`.
Notion source awareness: required when routing changes affect rules, memory or canon.

## Routing Rules

PLAY handles exploration, sketches and low-risk creative probes.

STUDIO handles structured drafting, synthesis, design, composition and iteration.

BIZ handles governance, releases, public boundaries, source policy, validation,
CI, audit trails and implementation work that affects operational reliability.

## Next Action Rule

For every task, Codex should decide:

1. Which mode applies.
2. Which source is authoritative.
3. Which boundary prevents overreach.
4. Which artifact records the result.
5. Which validation or sync action proves the result.

## External Systems

External systems may be read for context when available. They are mutated only
on explicit request. Notion remains the living source of record for rules and
memory; GitHub records technical mirrors and execution history.
