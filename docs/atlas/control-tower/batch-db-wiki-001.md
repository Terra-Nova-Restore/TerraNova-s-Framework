# DB-WIKI-001 - Database, Data Source and Wiki Stabilization

Status: Notion metadata package applied, local delta logged
Date: 2026-05-17
Parent IPERKA: `CAP 0.2 - Registry Stabilization IPERKA`
Mutation policy: Notion read-only until explicit GO

## Purpose

`DB-WIKI-001` stabilizes the database, data source and wiki layer before CAP attempts deeper page-level interpretation.

This batch exists because database and wiki objects define the workspace control surfaces. If their role is unclear, later duplicate review and content interpretation will drift.

## Target Rows

| Name | Type | Current canon status | Current sync status | Batch role |
| --- | --- | --- | --- | --- |
| Cognitive Terranova System | Database | Candidate | Needs sync | Existing system registry candidate; inspect before reuse or demotion. |
| Cognitive Terranova System main data source | Data Source | Reference | Needs sync | Main data source behind current system entries. |
| Restricted wiki data source | Wiki | Reference | Not applicable | Existence-only restricted source; no raw title expansion. |
| Mermaid Diagrams - Code Library | Data Source | Reference | Needs sync | Visual/control-source layer. |
| Meine Notion-KI | Database | Reference | Needs sync | Workspace wiki / ownership surface. |
| Meine Notion-KI wiki data source | Wiki | Reference | Needs sync | Wiki page index and ownership support. |
| Library Sync - 100 Batches | Database | Reference | Needs sync | Staged crawl/sync-control surface. |
| CAP 0.1.0 - Workspace Object Registry | Database | Source of Truth | In sync | Live CAP registry database. |
| CAP 0.1.0 Registry data source | Data Source | Source of Truth | In sync | Operational row/view handle for CAP registry. |

## Batch Questions

For each row:

1. Does the object still exist?
2. Is the parent/hub correct?
3. Is the canon status defensible?
4. Is the sync status accurate?
5. Is sensitivity correctly marked?
6. Does the row expose a deterministic boundary?
7. Does it need a Notion row update package?

## Expected Read Pass

Read-only verification order:

1. Fetch the three live databases.
2. Fetch the known data source handles.
3. Confirm whether wiki data sources are accessible through the connector.
4. Compare fetched schema names against registry row intent.
5. Record contradictions locally before any Notion update.

## Initial Interpretation

| Row group | Interpretation |
| --- | --- |
| CAP registry objects | Already stable; keep `Source of Truth` and `In sync`. |
| Existing system databases | Useful but not yet canonical for CAP; keep as `Reference` or `Candidate` until schema review. |
| Restricted wiki | Controlled existence marker only. |
| Library Sync | Likely best future batch execution surface, but not the registry itself. |
| Mermaid Library | Support layer for visual control, not primary system memory. |

## Candidate Outcomes

Allowed outcomes after read-only verification:

- keep as-is
- change `Canon Status`
- change `Sync Status`
- add missing deterministic boundary
- add missing causal chain
- create a follow-up batch

Not allowed without explicit GO:

- update Notion rows
- alter database schemas
- move databases or pages
- expose restricted wiki page names
- bulk import children

## Batch Done Criteria

This batch is complete when every target row has:

- verified existence or explicit uncertainty
- stable role label
- canon decision
- sync decision
- sensitivity decision
- deterministic boundary
- next action or no-action marker

## Next Local Step

Read-only fetch pass completed.

Findings:

```text
docs/atlas/control-tower/db-wiki-001.findings.md
```

Next step:

```text
Start `CANON-001` or run a focused Library Sync batch-row read pass.
```
