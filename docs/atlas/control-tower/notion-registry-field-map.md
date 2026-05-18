# CAP 0.1.0 Notion Registry Field Map

Status: executed mapping, Notion registry created
Date: 2026-05-17
Input: `object-registry.schema.json` and `workspace-object-registry.seed.csv`

## Purpose

This file maps the repo-local CAP registry schema to a practical Notion database layout.

It is intentionally conservative. CAP should start with fields that can be maintained manually and by Codex without Notion Custom Agents or credit-consuming automation.

## Recommended Notion Database

Title:

```text
CAP 0.1.0 - Workspace Object Registry
```

Parent:

```text
CAP 0.1.0 - Cognitive Ability Point
notion://redacted-internal-object
```

Created database:

```text
notion://redacted-internal-object
```

Created data source:

```text
notion-ds://redacted-internal-source
```

## Required Properties

| Repo field | Notion property type | Notes |
| --- | --- | --- |
| `Name` | Title | Main object name. |
| `Object Type` | Select | Page, Database, Wiki, Data Source, View, Template, Synced Block, GitHub Artifact, Drive Artifact, External Source. |
| `Object ID / URL` | URL or Text | URL preferred; use text for `collection://...` values if URL field rejects them. |
| `Parent / Hub` | Text | Use text first; relation can come later. |
| `Source Layer` | Select | Notion Connector, Notion UI, GitHub Atlas, Export Hard Count, Historic Trigger Anchor, Google Drive, External. |
| `Count Basis` | Select | Preserve `777 / 808 / ~880` distinction. |
| `Mode` | Select | PLAY, STUDIO, BIZ, Mixed, Unknown. |
| `Trigger Band` | Select | 1-100, 101-200, 201-300, 301-400, 401+, Not applicable, Unknown. |
| `Freedom Mode` | Select | `/fff enabled`, `/fff candidate`, bounded manual, blocked, not applicable. |
| `Status` | Status | Raw, Indexed, Reviewed, Canonical, Archived, Blocked. |
| `Canon Status` | Select | Source of Truth, Reference, Duplicate, Deprecated, Candidate, Unknown. |
| `Sensitivity` | Select | Public, Internal, Sensitive, Private, Restricted, Unknown. |
| `Owner` | Person or Text | Text is acceptable if person-field mapping is awkward. |
| `Last Edited` | Date | Optional. |
| `Last Reviewed` | Date | Required in practice for CAP hygiene. |
| `Related Canonical Object` | Text | Relation later; text first avoids circular setup. |
| `Causal Chain` | Text | Required for non-trivial CAP actions. |
| `Emergent Coherence Evidence` | Text | Evidence for why the object matters. |
| `Probabilistic Hypothesis` | Text | Explicit hypothesis; not final truth. |
| `Deterministic Boundary` | Text | Hard rule, source or permission boundary. |
| `Feedback / Backpropagation Target` | Select | Registry, Logbook, Trigger Map, Prism / Zenodo, Notion Canon, GitHub Atlas, No feedback, Unknown. |
| `Prism / Zenodo Relevance` | Select | Foreground, Backpropagation, Citation, Next-release candidate, Not relevant, Unknown. |
| `Understanding State` | Select | not read, read, understood, grasped, operationalized, blocked. |
| `Duplicate Group` | Text | Empty until duplicate review starts. |
| `GitHub Path` | Text | Repo path if applicable. |
| `Sync Status` | Select or Status | Not synced, In sync, Needs sync, Conflict, Not applicable. |
| `Equilibrium Notes` | Text | Rule/gate notes. |

## Initial Views

Planned views:

| View | Type | Filter / sort |
| --- | --- | --- |
| `All Objects` | Table | Sort by `Object Type`, then `Name`. |
| `Databases & Wikis` | Table | `Object Type` is Database, Wiki or Data Source. |
| `Canonical Sources` | Table | `Canon Status` is Source of Truth. |
| `Review Needed` | Table | `Status` is Raw, Indexed or Blocked, or `Canon Status` is Unknown. |
| `Sensitive / Restricted` | Table | `Sensitivity` is Sensitive, Private, Restricted or Unknown. |
| `Trigger 1-400 Steering` | Table | `Trigger Band` is 1-100, 101-200, 201-300 or 301-400. |
| `Prism / Zenodo Feedback` | Table | `Prism / Zenodo Relevance` is Foreground, Backpropagation, Citation or Next-release candidate. |
| `Sync Conflicts` | Table | `Sync Status` is Needs sync or Conflict. |

Created views in the live Notion registry:

| View | Type | Configuration |
| --- | --- | --- |
| `Default view` | Table | All fields visible by default. |
| `By Status` | Board | Grouped by `Status`. |
| `By Object Type` | Board | Grouped by `Object Type`. |
| `By Sensitivity` | Board | Grouped by `Sensitivity`. |
| `Canonical Sources` | Table | Filter `Canon Status = Source of Truth`; sorted by `Name`. |
| `Prism / Zenodo Feedback` | Table | Filter `Feedback / Backpropagation Target = Prism / Zenodo`; sorted by `Name`. |

Created linked dashboard views on the CAP page:

| View | Type | Configuration |
| --- | --- | --- |
| `CAP Registry - By Status` | Board | Linked data source, grouped by `Status`. |
| `CAP Registry - Canonical Sources` | Table | Linked data source, filter `Canon Status = Source of Truth`, sorted by `Name`. |
| `CAP Registry - Sync Needed` | Table | Linked data source, filter `Sync Status = Needs sync`, sorted by `Name`. |

## Seed Import

Seed file:

```text
docs/atlas/control-tower/workspace-object-registry.seed.csv
```

Expected row count:

```text
21
```

The restricted wiki row is existence-only. It must not be expanded into raw sensitive page titles.

The `Home-Ansichten Snapshot 2026-05-11` row is also sensitive. It records count and duplicate signals only, not the raw page list.

## Tool Boundary

The active Notion tools created the database and rows successfully. One SQL query attempt failed with an internal `notion-query-data-sources not found` tool error, so verification used `fetch` plus data-source search instead.

If future query tooling is unavailable, the fallback is:

1. Keep the CSV as repo truth.
2. Create the database manually in Notion using this field map.
3. Let Codex populate rows only after explicit approval and schema fetch.

No automated Notion AI or Custom Agent is needed.
