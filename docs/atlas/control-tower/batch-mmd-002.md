# MMD-002 - Mermaid Graph Extraction

Date: 2026-05-17

Activation: `MMD-002 - Mermaid Graph Extraction / Go`

Mode: repo-local extraction

External mutation: none

Notion AI credits used: 0

## Purpose

MMD-002 turns the Mermaid universe from a readpass into a machine-readable
graph layer.

It extracts:

- graphs
- nodes
- edges
- guard conditions
- trigger references visible in node labels or edge conditions
- extraction gaps

This creates the first usable bridge from Mermaid diagrams to the future CAP
trigger registry without forcing the full 675-trigger history open.

## Sources

MMD-002 uses local source artifacts only:

| Source | Role |
| --- | --- |
| `raw/exports/prism/source-pack/2026-05-02/*Mermaid Diagrams*_all (2).csv` | Active registry truth for status, role, type and zoom. |
| `raw/exports/prism/source-pack/2026-05-02/Mermaid Code Library - Complete Collection ...md` | Primary Mermaid code depot. |
| `raw/exports/prism/source-pack/2026-05-02/Mermaid als lebendiger Trigger-Organismus ...md` | SESSION_ROOT living trigger graph. |
| `docs/ai/full_sync_terra_nova_mcp_sequence.md` | Existing sync sequence diagram. |
| `docs/atlas/control-tower/mmd-001.mermaid-universe-readpass.md` | CAP visual control model. |

## Extraction Result

| Metric | Count |
| --- | ---: |
| Source specs | 11 |
| Graphs | 11 |
| Nodes | 277 |
| Edges | 363 |
| Guard rows | 363 |
| Extraction gaps | 4 |

The four gaps are low-severity registry/code declaration mismatches, for
example `flowchart` in the registry while the exported code begins with
`graph TB`. The graph content still parsed.

## Outputs

| File | Purpose |
| --- | --- |
| `mmd-002.graphs.csv` | One row per extracted graph. |
| `mmd-002.nodes.csv` | Normalized node inventory. |
| `mmd-002.edges.csv` | Normalized edge inventory. |
| `mmd-002.guard-conditions.csv` | Edge guards and trigger/VORTEX signals. |
| `mmd-002.extraction-gaps.csv` | Parser and source consistency gaps. |
| `mmd-002.extraction-summary.json` | Machine-readable run summary. |
| `mmd-002.graph-extraction.md` | Human-readable summary. |
| `scripts/extract_mermaid_graphs.py` | Repeatable extractor. |

## Boundary

MMD-002 does not:

- write to Notion
- run Notion AI
- infer missing trigger canon
- treat Mermaid edges as execution permission
- expose raw private trigger internals
- open SCL or Lenhard decoder work

## Next

Best next action:

```text
MMD-003 - Visual Trigger Bridge
```

MMD-003 should use `mmd-002.nodes.csv` and
`mmd-002.guard-conditions.csv` to build the first safe bridge from visible
Mermaid trigger nodes to CAP trigger module candidates.
