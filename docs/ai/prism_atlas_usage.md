# Prism Atlas Usage

Status: working architecture note

## Purpose

This note defines how the Prism editor implementation of the TerraNova atlas
material should be used inside the repository and agent workflow.

The source pack is not only a visual export. It should become a controlled
navigation, validation and publishing layer for TerraNova / FerrAI.

## Source roles

Use the current material in four roles:

| Role | Source artifact | Use |
| --- | --- | --- |
| Payload bundle | `TerraNova_AllInOne` | Archiveable full export for graph, Mermaid and README material. |
| Landing atlas | `TerraNova System Atlas - CIC Framework Overview` | Human-readable start page and onboarding map. |
| Trigger register | `Trigger-System - Deep Reference (1-992)` | Internal trigger index, gap tracking and agent routing reference. |
| Diagram registry | `Mermaid Code Library - Complete Collection` plus CSV registry | Renderable graph source and metadata truth for diagram status. |

## Internal use

1. Treat the atlas as the first orientation layer for TerraNova/CIC work.
2. Feed only reviewed extracts into Codex skills, AGENTS notes or automation
   prompts.
3. Keep sensitive trigger, token, wallet, private archive and Schattenarchiv
   details out of public exports.
4. Use the diagram registry to identify active vs legacy Mermaid diagrams before
   copying any graph into docs or presentations.
5. Track undocumented trigger ranges as gaps, not as invented content.

## Repository use

Recommended local structure:

```text
raw/exports/prism/
  source-pack/              # raw Prism/Notion exports, unchanged
docs/ai/
  prism_atlas_usage.md      # this routing note
  full_sync_terra_nova_mcp_sequence.md
docs/atlas/
  index.md                  # curated human-facing atlas, generated later
  diagrams.md               # reviewed Mermaid registry, generated later
docs/triggers/
  trigger_reference.md      # reviewed trigger subset, generated later
```

The raw source pack stays archival. Curated docs are derived from it and should
state their source and review status.

## Agent use

Use the atlas as a routing surface:

```text
User intent
  -> atlas area
  -> source artifact
  -> reviewed extract
  -> Codex action / Prism edit / GitHub doc update
```

This prevents raw chat exports from becoming system truth while still making the
workspace map useful for agents.

## Public use

The public-facing slice is:

- Mermaid as living trigger system
- TerraNova atlas as visual system navigation
- CIC as coordination and consistency framework
- Prism as internal authoring/editor layer unless naming is reviewed

Do not publish private trigger canon, deep Schattenarchiv material, wallet/token
operations, patent-sensitive mappings or raw personal logs without a separate
review decision.

## Local renderer

The local renderer is implemented at:

```text
scripts/render_prism_atlas.py
```

Current source-pack location:

```text
raw/exports/prism/source-pack/2026-05-02/
```

Generated outputs:

```text
docs/atlas/index.md
docs/atlas/diagrams.md
docs/atlas/public_overview.md
docs/atlas/operator_map.md
docs/atlas/source_inventory.csv
docs/atlas/source_manifest.json
docs/triggers/gap_ledger.md
```

This gives Prism, Codex and GitHub the same map without requiring a new Notion
page or external system mutation.

Run it with:

```powershell
python scripts/render_prism_atlas.py
```

Or pin a source pack explicitly:

```powershell
python scripts/render_prism_atlas.py --source-dir raw\exports\prism\source-pack\2026-05-02 --output-dir docs\atlas
```
