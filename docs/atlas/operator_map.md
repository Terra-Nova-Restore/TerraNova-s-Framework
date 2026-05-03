# TerraNova Operator Map

Status: internal routing map generated from the Prism source pack

Generated: 2026-05-02

## Purpose

This file tells Codex, Prism and future agents which source to consult first
for common TerraNova tasks. It is internal operating material, not a public
landing page.

## Routing Table

| Intent | First source | Action | Guard |
| --- | --- | --- | --- |
| Orient a new session | `TerraNova System Atlas — CIC Framework Overview fcd6cce055c843069b46ec82b2e99bac (2).md` | Read atlas summary, then choose diagram or source lane. | Keep raw exports as context, not truth. |
| Build or update diagrams | `Mermaid Code Library – Complete Collection 999ce78e7102420cbf7a2a4385c28603 (2).md` | Use ACTIVE rows from `docs/atlas/diagrams.md`. | Do not revive LEGACY rows unless explicitly needed. |
| Prepare public copy | `Mermaid-Diagramme als lebende Systeme Von der Visu e0ca072cf0224d16b558dcec5132f81d (2).md` | Draft from public overview and selected diagrams. | Redact sensitivity flags first. |
| Work on triggers | `⚡ Trigger-System — Deep Reference (1–992) 76520fbd9e7842a086abd8623caa0bea (2).md` | Check `docs/triggers/gap_ledger.md` before adding or naming ranges. | Open gaps stay open until sourced. |
| Investigate provenance | `Chatverlauf (Quelle) a62a25945fc74eedbcd6929ff04e09fb (2).md` | Use as background only; extract reviewed claims separately. | Raw chat cannot become canonical truth. |
| Archive source payload | `TerraNova_AllInOne (2).md` | Preserve unchanged and derive curated docs from it. | Do not edit raw source-pack files. |
| Review repository/IP context | `Deep Research Review FerrAI_fff Repository, Commit 2fdf7297de7e8040a6abfc56de024e6c (2).md` | Use as a review input for repo-facing claims. | Verify against GitHub before treating as current state. |

## Agent Procedure

1. Identify the user's intent and pick one routing row.
2. Read the first source and any generated atlas file named in the row.
3. Produce a reviewed extract or local diff.
4. Keep external writes gated behind explicit user confirmation.
5. Update generated atlas docs by re-running `scripts/render_prism_atlas.py`, not by hand-editing generated files.

## Output Targets

| Need | Target |
| --- | --- |
| Human-facing atlas | `docs/atlas/index.md` |
| Public-facing slice | `docs/atlas/public_overview.md` |
| Internal routing | `docs/atlas/operator_map.md` |
| Diagram selection | `docs/atlas/diagrams.md` |
| Trigger gaps | `docs/triggers/gap_ledger.md` |
| Machine inventory | `docs/atlas/source_inventory.csv` and `source_manifest.json` |

## Mutation Boundary

- Local docs and generated files can be updated as part of repository work.
- Git commits, pushes, PR actions and connector writes need explicit user confirmation.
- Notion remains source-of-record where explicitly defined; GitHub remains the reviewed engineering mirror.
