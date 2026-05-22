# TerraNova Atlas Docs

Status: local reviewed CIC atlas workspace

## Entry Points

| File | Use |
| --- | --- |
| `index.md` | Main local CIC atlas start page and source-pack orientation. |
| `public_overview.md` | Public-candidate slice for Mermaid/CIC/Systemnavigation material. |
| `operator_map.md` | Internal routing map for Codex, OpenAI Prism source context and future agents. |
| `diagrams.md` | Active/legacy/unknown Mermaid diagram registry. |
| `control-tower/` | CAP 0.1.0 / Control Tower CIC plan, registry schema and source map for Notion workspace governance. |
| `source_inventory.csv` | Machine-readable source file inventory. |
| `source_manifest.json` | Full generated source and diagram manifest. |

## Regenerate

From the repository root:

```powershell
python scripts/render_cic_atlas.py
```

Legacy compatibility remains available:

```powershell
python scripts/render_prism_atlas.py
```

The renderer picks the latest local dated source pack under
`raw/exports/prism/source-pack/` when no explicit `--source-dir` is provided.
That raw path is kept for provenance because the exports came from OpenAI Prism / Notion context.

## Naming boundary

- TerraNova framework / atlas name: **CIC**.
- External/editor source context: **OpenAI Prism**.
- Raw source exports remain archival and can contain private or sensitive material.

Edit the renderer or local source pack, then regenerate these docs instead of hand-editing generated files.
