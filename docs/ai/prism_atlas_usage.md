# Legacy: Prism Atlas Usage

Status: legacy compatibility note

The TerraNova framework naming has moved from **PRISM** to **CIC** to avoid confusion with OpenAI Prism.

Use the active note instead:

```text
docs/ai/cic_atlas_usage.md
```

## Naming rule

- **CIC** = TerraNova framework / atlas / consistency layer.
- **OpenAI Prism** = external editor/source context, only where explicitly meant.
- Raw source paths under `raw/exports/prism/` remain unchanged for provenance unless a separate migration explicitly moves them.

## Renderer

Preferred:

```powershell
python scripts/render_cic_atlas.py
```

Legacy compatibility:

```powershell
python scripts/render_prism_atlas.py
```
