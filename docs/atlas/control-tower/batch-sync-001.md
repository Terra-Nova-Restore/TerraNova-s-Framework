# SYNC-001 - Registry Sync Stabilization

Status: Notion metadata package applied, local trace synced
Date: 2026-05-17
Parent IPERKA: `CAP 0.2 - Registry Stabilization IPERKA`
Mutation policy: metadata-only Notion updates after explicit GO

## Purpose

`SYNC-001` reduces the first `Needs sync` drift in the CAP registry.

The sync scope is intentionally narrow:

```text
Notion registry row
-> GitHub trace or safe local artifact exists
-> deterministic boundary is explicit
-> row can be marked In sync for registry governance
```

`In sync` does not mean that the complete Notion page content has been copied into GitHub. It means the registry's control claim is aligned with a bounded GitHub trace.

## Target Rows

| Name | Sync decision | Reason |
| --- | --- | --- |
| `EQUILIBRIUM - Offizielles Regelbuch` | `In sync` | R16 is recorded in the CAP trace and the operating kernel now carries the active-delta boundary. |
| `CIC - Cognitive Intelligent Cooperation` | `In sync` | CIC has a repository-side atlas/navigation trace; Notion remains the conceptual source of truth. |
| `Cognition Sync Hub` | `In sync` | Semantic sync doctrine is now represented by this batch and the CAP registry model. |
| `CEI-DATA-05 - Workspace Index & Page Census Note` | `In sync` | Count and redaction boundaries are mirrored through CAP and the safe XXL data export artifacts. |
| `Cognitive Terranova System` | `In sync` | DB-WIKI-001 verified it as a multi-source hub, not the CAP registry replacement. |
| `Cognitive Terranova System main data source` | `In sync` | DB-WIKI-001 verified schema and field-mapping boundary. |
| `Mermaid Diagrams - Code Library` | `In sync` | DB-WIKI-001 verified diagram source role and ACTIVE/KANON review priority. |
| `Meine Notion-KI` | `In sync` | DB-WIKI-001 verified ownership and verification support role. |
| `Meine Notion-KI wiki data source` | `In sync` | DB-WIKI-001 verified wiki data-source role and parent-update limitation. |
| `Library Sync - 100 Batches` | `In sync` | DB-WIKI-001 verified batch database and added its operational data-source row. |
| `Home-Ansichten Snapshot 2026-05-11` | `In sync` | Sensitive local snapshot brief and machine summary exist; raw export remains private and not current truth. |

## Boundary

No raw page inventory is imported.

No restricted child titles are exposed.

No Notion schema is changed.

No full GitHub mirror of every Notion page is claimed.

The sync decision is scoped to registry governance metadata only.

## Applied Result

Applied Notion metadata result:

```text
target rows: 11
sync status changes: 11 -> In sync
remaining Needs sync rows: 0
schema changes: 0
raw content imports: 0
```

## Next Batch

After `SYNC-001`, the next structural pressure is duplicate-title control:

```text
DUP-001
-> Unbenannt / empty title / repeated template groups
-> classify without deletion
-> prepare review queues
```

Status: complete.
