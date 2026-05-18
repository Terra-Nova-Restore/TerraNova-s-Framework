# CANON-001 - Source-of-Truth Stabilization

Status: Notion metadata package applied, local trace synced
Date: 2026-05-17
Parent IPERKA: `CAP 0.2 - Registry Stabilization IPERKA`
Mutation policy: metadata-only Notion updates after explicit GO

## Purpose

`CANON-001` stabilizes the current Source-of-Truth rows in the CAP registry.

The goal is not to make every important object canonical. The goal is to define exactly what each canonical object is canonical for.

## Target Rows

| Name | Canon role | Decision |
| --- | --- | --- |
| CAP 0.1.0 - Cognitive Ability Point | Internal control surface for CAP operations. | Keep `Source of Truth`; refresh live-state notes. |
| EQUILIBRIUM - Offizielles Regelbuch | Governance and rule boundary. | Keep `Source of Truth`; add R16 awareness. |
| CIC - Cognitive Intelligent Cooperation | Conceptual source for reference architecture, negative redundancy and CIC cooperation model. | Keep `Source of Truth`; retain `Needs sync` until GitHub mirror status is checked. |
| CEI-DATA-05 - Workspace Index & Page Census Note | Count model and publication/redaction gate for workspace census. | Keep `Source of Truth` for count/gate layer only. |
| Zenodo RC01-v12 reference | Published citable snapshot reference. | Keep `Source of Truth`; publication is snapshot, not live truth. |
| CAP 0.1.0 - Workspace Object Registry | Live object-governance registry. | Keep `Source of Truth`; already verified by DB-WIKI-001. |
| CAP 0.1.0 Registry data source | Operational data-source handle for CAP rows/views. | Keep `Source of Truth`; already verified by DB-WIKI-001. |

## Read Findings

### CAP 0.1.0

The CAP page exists under the development zone and has direct linked dashboard views.

Finding: it still says `Initial registry rows: 21`, while the live registry now has 22 rows after `DB-WIKI-001`.

Decision: keep as Source of Truth, but refresh its current dashboard state.

### EQUILIBRIUM

Equilibrium is clearly canonical for rules and boundary logic.

Finding: the page now includes `Regel 16 - Regeln sind zum bewussten Bruch da, nicht zum unbewussten Vergessen`.

Decision: keep as Source of Truth; update CAP/GitHub trace to include R16.

### CIC

CIC is clearly canonical for:

- Single Source of Truth
- reference over copy
- negative redundancy
- 3D structure model
- Notion as master over GitHub mirror for CIC annex material

Decision: keep as Source of Truth, but keep `Needs sync` until GitHub mirror alignment is checked.

### CEI-DATA-05

CEI-DATA-05 is canonical for:

- `777 historic_trigger_anchor`
- `808 export_hard_count`
- `~880 notion_ui_horizon`
- raw-export boundaries
- safe-index/publication gates

Decision: keep as Source of Truth for count and redaction logic only. It is not the universal data source for all workspace content.

### Zenodo RC01-v12 Reference

The local Zenodo reference and release mirror are consistent:

- DOI: `10.5281/zenodo.20073579`
- Concept DOI: `10.5281/zenodo.19774446`
- Version: `RC01-v12`
- Publication date: `2026-05-07`
- File size: `2,943,457` bytes

Decision: keep as Source of Truth for the published citable snapshot. It is not the living workspace truth.

### CAP Registry and Data Source

The CAP registry database and data source were verified in `DB-WIKI-001`.

Decision: keep both as Source of Truth for object-governance state.

## Canon Boundary Matrix

| Canon object | Canon for | Not canon for |
| --- | --- | --- |
| Equilibrium | rules, boundaries, response discipline | page inventory, publication metadata |
| CIC | cooperation model, reference architecture, redundancy control | current operational status |
| CEI-DATA-05 | count model, redaction gates, safe-index logic | raw workspace content |
| CAP page | active control surface | every registry row detail |
| CAP registry | object state, canon/sync/sensitivity decisions | full page content |
| Zenodo reference | published citation snapshot | living framework state |

## Recommended Notion Metadata Updates

Applied after explicit GO:

- Mark all seven canon target rows `Reviewed`.
- Keep all seven `Canon Status = Source of Truth`.
- Keep CIC and CEI-DATA-05 as `Needs sync` where GitHub mirror or companion work remains open.
- Refresh CAP page current state from 21 to 22 live rows.
- Add R16 awareness to GitHub/CAP local trace.

Applied result:

```text
canon rows updated: 7
canon demotions: 0
CAP page refreshed: yes
Equilibrium R16 mirrored: yes
live registry rows: 22
```

## Done Criteria

`CANON-001` is complete when:

- every Source-of-Truth row has a scoped canon role
- none of the seven canon rows are demoted
- Equilibrium R16 is recorded in the local CAP trace
- CAP page no longer presents the registry as only 21 live rows

Status: complete.
