# Codex Boot Contract

Status: BIZ / Codex-Boot
Source: Technical mirror of the FerrAI Operating Kernel v0.1; Notion remains the source of record for living rules.
Trace: `docs/architecture/ferrAI_operating_kernel_v0.1.md`
Boundary: This file is a startup contract, not a duplicate rulebook.
Mode: BIZ
GitHub sync state: tracked in this repository; validate through `scripts/validate_docs.py`.
Notion source awareness: required for rule, memory and canon changes.

## Purpose

Codex starts TerraNova / FerrAI work from a minimal contract:

1. Identify the active mode: PLAY, STUDIO or BIZ.
2. Check status, trace, boundary and source-of-record awareness.
3. Keep Notion as living rule and memory source.
4. Keep GitHub as technical mirror, diff, CI and audit surface.
5. Execute the smallest coherent next action.

## Operating Limit

Do not load or recreate the full Equilibrium rulebook during normal repo work.
Use this file only to anchor source, mode, status, boundary and next action.
