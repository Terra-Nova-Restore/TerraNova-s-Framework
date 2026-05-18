# DB-WIKI-001 Findings - Read-only Pass

Status: findings complete, Notion metadata package applied after explicit GO
Date: 2026-05-17
Batch: `DB-WIKI-001`
Scope: databases, data sources and wikis from the CAP 0.1.0 registry seed

## Summary

The read pass confirms that the database/wiki layer is real and usable, but it is not yet fully stabilized as a control system.

The strongest structural finding is that `Cognitive Terranova System` is a multi-source database container:

```text
Cognitive Terranova System
-> main data source
-> restricted wiki data source
-> Mermaid Diagrams - Code Library data source
```

This means CAP must treat it as a hub/container, not as a clean single registry database.

## Object Findings

| Object | Verified | Finding | Decision |
| --- | --- | --- | --- |
| Cognitive Terranova System | yes | Top-level multi-source database with default template `(parked) GitHub-Sync-Template`. | Keep `Candidate`; do not use as CAP registry replacement. |
| Cognitive Terranova System main data source | yes | Main source has broad system fields: `Name`, `Status`, `Prioritaet`, `Kategorie`, `Abhaengigkeiten`, `Beschreibung`, `Fortschritt (%)`, resources and ownership fields. | Keep `Reference`; map before any row mutation. |
| Restricted wiki data source | yes | Wiki source under Cognitive Terranova System. Connector exposes schema and wiki page URL. Custom properties are not generally updateable through current tooling; verification may be updateable. | Keep `Restricted`, `Reference`, `Not applicable`; existence-only marker. |
| Mermaid Diagrams - Code Library | yes | Data source under Cognitive Terranova System. Has `Role` values `KANON`, `ZOOM`, `APPENDIX`, `DEPOT` and status values including `ACTIVE`, `ORPHAN`, `LEGACY`. | Keep `Reference`; future query should focus `ACTIVE` and `KANON`. |
| Meine Notion-KI | yes | Top-level wiki database. Data source has owner, verification, tags and last edited time. | Keep `Reference`; use as ownership/verification surface. |
| Meine Notion-KI wiki data source | yes | Wiki source tied to `Meine Notion-KI`; parent updates must use wiki page URL, not data source parent. | Keep `Reference`; respect wiki update limits. |
| Library Sync - 100 Batches | yes | Inline database under `Projektbeschrieb - TerraNova / FerrAI`. Has batch fields: status, sync state, mode, owner, scope, result and agents. | Keep `Reference`; use as future batch execution surface. |
| CAP 0.1.0 - Workspace Object Registry | yes | Live registry database under CAP page. Schema matches CAP object model and dashboard views exist. | Keep `Source of Truth`, `In sync`. |
| CAP 0.1.0 Registry data source | yes | Operational data source for registry rows and views. | Keep `Source of Truth`, `In sync`. |

## Structural Corrections

### Library Sync data source is missing as its own registry row

The `Library Sync - 100 Batches` database has a data source:

```text
notion-ds://redacted-internal-source
```

The current registry has the database row, but not a separate data-source row. CAP should add this as an explicit row in a future mutation package because it is the operational handle for batch rows.

### Cognitive Terranova System should stay Candidate

The database is useful, but it has mixed sources and a parked default GitHub sync template. It should not become the CAP source of truth. CAP registry remains the source of truth for workspace object governance.

### Restricted wiki remains existence-only

The restricted wiki schema was verified, but no raw child titles or page content were imported. This matches the sensitivity boundary.

### Meine Notion-KI is ownership support, not registry source

The wiki is valuable for owner/verification logic. It should not become the main CAP registry.

## Recommended Registry Updates

Initial read pass performed no Notion mutation. After explicit GO, the metadata-only package below was applied.

| Target row | Proposed update |
| --- | --- |
| Cognitive Terranova System | Keep `Canon Status = Candidate`; update notes to `multi-source hub; not CAP registry replacement`. |
| Cognitive Terranova System main data source | Keep `Reference`; add deterministic boundary: `map fields before mutation`. |
| Restricted wiki data source | Keep `Restricted`; add boundary: `existence-only; no raw page titles`. |
| Mermaid Diagrams - Code Library | Keep `Reference`; add future filter note: `ACTIVE + KANON first`. |
| Meine Notion-KI | Keep `Reference`; add role note: `ownership and verification surface`. |
| Meine Notion-KI wiki data source | Keep `Reference`; add boundary: `wiki parent/page update limitation`. |
| Library Sync - 100 Batches | Keep `Reference`; add note: `future batch execution surface`. |
| New row | Add `Library Sync - 100 Batches data source` with ID `notion-ds://redacted-internal-source`. |

Applied result:

```text
new row: Library Sync - 100 Batches data source
new row id: notion-id://redacted
updated rows: 9
live registry rows: 22
```

## Decision

`DB-WIKI-001` should move from plan to findings complete.

The next useful action is a controlled Notion mutation package for:

1. adding the missing `Library Sync - 100 Batches data source` row
2. tightening notes/boundaries for the verified DB/wiki rows
3. changing verified-but-not-final rows from `Indexed` to `Reviewed` only if Silvan wants CAP to mark read-pass completion in Notion

## Boundary

No content rows were queried from restricted wiki sources.

Only registry metadata rows were updated after explicit GO.

No database schemas were changed.
