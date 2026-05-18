# CAP 0.1.0 Phase 02 - Registry Seed Plan

Status: executed, Notion registry created  
Date: 2026-05-17  
Scope: first `Workspace Object Registry` seed after CAP page creation

## Purpose

Phase 02 turns CAP 0.1.0 from a control page into a structured registry layer.

The first seed now has 21 rows, derived from `source-map.csv`, the Home-Ansichten snapshot and registry self-registration. It is aligned to `object-registry.schema.json`.

## Notion Result

| Item | Value |
| --- | --- |
| Registry database | `https://www.notion.so/f9aafd4eaf9046e0beb7552b1018af83` |
| Registry data source | `collection://f8e7df9f-e1ed-43f0-888b-39d362f2cef2` |
| Parent page | `CAP 0.1.0 - Cognitive Ability Point` |
| Seed rows created | 21 |
| Database views created | 5 plus default table |
| CAP page linked views created | 3 |
| Snapshot source | `C:\Users\Silvan\Desktop\[Home-Ansichten](httpswww.notion.so.txt` |

## Created Local Artifacts

| File | Role |
| --- | --- |
| `workspace-object-registry.seed.csv` | 21 seed rows for the first CAP registry. |
| `object-registry.schema.json` | Field model for the registry. |
| `source-map.csv` | Source anchor list and current CAP references. |
| `causal-log.cap-creation-2026-05-17.json` | First causal log event for CAP page creation. |
| `causal-log.registry-creation-2026-05-17.json` | Causal log event for registry creation and snapshot ingestion. |
| `notion-registry-field-map.md` | Notion database property and view mapping. |
| `home-ansichten-snapshot-2026-05-11.md` | Sensitive local snapshot brief. |
| `home-ansichten.snapshot.summary.json` | Machine-readable snapshot count summary. |

## Phase 02 Operating Rule

The explicit user phrase `GO Notion CAP Registry erstellen` authorized registry creation. That action is complete.

Further Notion mutation is not authorized by this file unless a new explicit GO is given.

## Why This Comes Next

The CAP page gives a control surface. The registry gives control over objects.

Without a registry, CAP remains readable but not operational. With a registry, the system can answer:

- what exists
- where it belongs
- whether it is canon, reference, duplicate or blocked
- whether it is safe, internal or restricted
- whether it has a causal chain
- whether it feeds Prism/Zenodo, GitHub, Notion canon or trigger maps

## Gate For Next Notion Action

Required before any database creation:

- fetch the CAP page again
- decide whether to create a standalone database or use an existing database
- inspect `Cognitive Terranova System` again if reusing it is considered
- keep restricted wiki objects as existence-only rows
- no raw 880-page inventory
- no custom Notion agent / no AI credit automation

Suggested approval phrase:

```text
GO Notion CAP Registry erstellen
```

## Immediate Next Work Without Notion Mutation

- Validate CSV import shape. Done: 21 rows.
- Add row-count checks. Done: 21 rows via PowerShell `Import-Csv`.
- Draft Notion database field mapping. Done: `notion-registry-field-map.md`.
- Prepare view list. Done in the field map.
- Create registry database in Notion. Done.
- Create initial control views. Done.
- Add direct linked dashboard views to the CAP page. Done.
- Register the Home-Ansichten snapshot. Done.

## Current Phase 02 Result

CAP now has:

- one verified Notion control page
- one live Notion registry database
- one live registry data source
- three linked registry dashboard views on the CAP page
- one repo-local registry schema
- one 21-row registry seed
- one Notion field map
- one causal log event for the first CAP mutation
- one causal log event for registry creation
- one sensitive local snapshot brief for the 2026-05-11 Home-Ansichten export
