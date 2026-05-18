# NINF-001 - CAP 0.3 Notion Infiltration Readpass

Status: STUDIO mutation applied  
Date: 2026-05-17  
Scope: CAP page, CAP registry database, CAP registry data source and registry search evidence  
External mutation: low-risk Notion visibility update applied after user approval

## Recommended Variant

Proceed in two layers:

1. Read-only Notion infiltration now.
2. Apply the low-risk Notion mutation only after explicit Silvan approval.

This is the best quality and efficiency path because it keeps Notion as the system of record while preventing silent drift, accidental schema edits or credit-consuming automation.

## Purpose

NINF-001 translates CAP 0.3 into a concrete Notion insertion package.

The mutation has now been applied after Silvan's full-speed approval.

## Readpass Sources

| Source | Observation |
| --- | --- |
| CAP page | `CAP 0.1.0 - Cognitive Ability Point` exists under `TerraNova - Entwicklungs- & Integrationszone`. |
| CAP page content | The page still says: `Next: close CAP 0.2 and create CAP 0.3 IPERKA`. |
| Registry database | `CAP 0.1.0 - Workspace Object Registry` exists under the CAP page. |
| Registry data source | `collection://f8e7df9f-e1ed-43f0-888b-39d362f2cef2` is available and schema-visible. |
| Registry views | `Default view`, `By Status`, `By Object Type`, `By Sensitivity`, `Canonical Sources`, `Prism / Zenodo Feedback`. |
| Registry search | `DUP-001`, `SENS-001`, `PRISM-001`, CAP page, registry and core anchors are searchable. |
| Query tool | SQL data-source query remains blocked by `notion-query-data-sources not found`. |

## Findings

### Finding 1 - CAP page is one step behind

The live CAP page already contains the CAP 0.2 batch history and registry state, but its next queue still points to CAP 0.3 creation. CAP 0.3 now exists repo-local, so the page should be updated.

Recommended future Notion action:

- replace the old next-queue sentence with a CAP 0.3 continuation section
- include the seven CAP 0.3 workstreams
- keep the no-credit operating boundary visible
- keep raw private workspace inventory out of the page

### Finding 2 - Registry schema is sufficient for CAP 0.3

The current registry fields are enough for CAP 0.3. No schema mutation is needed.

Recommended future Notion action:

- do not add columns yet
- add rows or views only when they create direct operational value
- prefer view additions over schema expansion

### Finding 3 - Existing views are useful but not yet operational enough

The existing views show status, object type, sensitivity, canon and Prism/Zenodo feedback. CAP 0.3 needs queue steering views.

Recommended future Notion action:

- add a `CAP 0.3 Operations` view
- add a `Duplicate Review` view
- add a `No-Credit Automation` view only if rows exist to support it

### Finding 4 - SQL query remains unreliable

The Notion data-source SQL query tool is advertised but unavailable at runtime. CAP work should not depend on it.

Recommended future Notion action:

- use fetch/search for verification
- keep local CSV/JSON as the reliable audit layer
- do not claim complete live row counts from SQL until the tool works

## Proposed Notion Mutation Package

These changes were applied after explicit approval.

| ID | Target | Action | Why | Risk |
| --- | --- | --- | --- | --- |
| NINF-001-A | CAP page | Update `Next Internal Work Queue` to CAP 0.3 status. | Removes one-step drift. | Low |
| NINF-001-B | CAP page | Add `CAP 0.3 - Operational Control` section. | Makes current steering visible. | Low |
| NINF-001-C | Registry database | Create view `CAP 0.3 Operations`. | Surfaces active CAP 0.3 workstreams. | Low |
| NINF-001-D | Registry database | Create view `Duplicate Review`. | Makes DUP-002 work controllable. | Low |
| NINF-001-E | Registry rows | Add a registry row for `CAP 0.3 - Operational Control IPERKA`. | Keeps repo-local CAP 0.3 visible in Notion. | Low |
| NINF-001-F | Registry rows | Add a registry row for `NINF-001 Notion Infiltration Package`. | Makes the infiltration package traceable. | Low |

## Applied Mutation Result

| Item | Result |
| --- | --- |
| CAP page | Updated `Current Dashboard State` and `Next Internal Work Queue`. |
| Registry rows | Added `CAP 0.3 - Operational Control IPERKA` and `NINF-001 Notion Infiltration Package`. |
| Registry views | Added `CAP 0.3 Operations` and `Duplicate Review`. |
| Current live registry rows | 27 after NINF-001. |
| Schema changes | 0 |
| Deletions | 0 |
| Raw private inventory exports | 0 |

Blocked by default:

- page deletion
- page moves
- raw ID export
- schema changes
- restricted wiki content fetch/export
- broad workspace AI summarization
- Notion Custom Agents
- scheduled Notion AI

## Exact Future GO Phrase

This was the planned approval phrase:

```text
GO Notion NINF-001 anwenden
```

Applied effect:

- updated CAP page text
- created low-risk operational views supported by the current database state
- added CAP 0.3 / NINF-001 registry rows
- no deletion, no schema change, no raw private inventory

## Control Answer

Best next operational move:

```text
NINF-001 local package
-> explicit full-speed approval
-> low-risk Notion page/view/row mutation
-> DUP-002 can start from a visible operational dashboard
```

Next recommended move: start `DUP-002` with the new Duplicate Review view as the visible control surface.
