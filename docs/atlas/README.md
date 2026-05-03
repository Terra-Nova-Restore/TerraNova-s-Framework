# TerraNova Atlas Docs

Status: local reviewed atlas workspace

## Entry Points

| File | Use |
| --- | --- |
| `index.md` | Main local atlas start page and source-pack orientation. |
| `public_overview.md` | Public-candidate slice for Mermaid/CIC/Systemnavigation material. |
| `operator_map.md` | Internal routing map for Codex, Prism and future agents. |
| `diagrams.md` | Active/legacy/unknown Mermaid diagram registry. |
| `source_inventory.csv` | Machine-readable source file inventory. |
| `source_manifest.json` | Full generated source and diagram manifest. |

## Regenerate

From the repository root:

```powershell
python scripts/render_prism_atlas.py
```

The renderer picks the latest local dated source pack under
`raw/exports/prism/source-pack/` when no explicit `--source-dir` is provided.

## Boundary

Raw source exports remain archival and are git-ignored by default because they
can contain private or sensitive material. Edit the renderer or local source
pack, then regenerate these docs instead of hand-editing generated files.
