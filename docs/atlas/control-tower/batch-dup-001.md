# DUP-001 - Duplicate Title Review Queues

Status: Notion metadata package applied, local trace synced
Date: 2026-05-17
Parent IPERKA: `CAP 0.2 - Registry Stabilization IPERKA`
Mutation policy: metadata-only Notion updates after explicit DUP-001 instruction

## Purpose

`DUP-001` turns duplicate-title pressure into bounded review queues.

The snapshot shows no duplicate Notion IDs. The problem is therefore not object collision. The problem is weak title coherence:

```text
808 Notion URLs
-> 808 unique Notion IDs
-> 0 duplicate ID groups
-> 46 duplicate title groups
-> 226 duplicate-title occurrences
```

## Boundary

No raw page list is published.

No Notion pages are deleted.

No restricted child titles are exposed.

No current-live truth is claimed from the 2026-05-11 snapshot.

Duplicate handling starts as review queues, not cleanup automation.

## Queue Model

| Queue | Group count | Occurrences | Decision |
| --- | ---: | ---: | --- |
| Untitled placeholders | 2 | 104 | First rename queue. Must be matched to current Notion objects before any archive decision. |
| Prompt/action templates | 5 | 24 | Likely reusable prompt/template family; consolidate by canonical template names. |
| Patent/IP dossier titles | 11 | 30 | Sensitive/IP-controlled queue; defer content decisions to `SENS-001`. |
| Trigger/session/deep-system exports | 8 | 20 | Internal/depth queue; classify before any public or automated reuse. |
| Navigation/working surfaces | 5 | 12 | Verify active hubs and dashboards; keep live surfaces, rename weak copies. |
| Generic low-signal titles | 8 | 16 | Rename or archive candidates after ID-level verification. |
| Chat/person/export remnants | 4 | 10 | Private/import-remnant candidates; archive only after source check. |
| Capability/governance concepts | 3 | 10 | Potential canon/support objects; compare with existing canonical pages. |

## Applied Local Result

```text
duplicate title groups classified: 46
duplicate-title occurrences classified: 226
review queues created: 8
raw URLs exported: 0
raw Notion IDs exported: 0
delete actions: 0
```

## Applied Notion Result

```text
new registry row: DUP-001 Duplicate Title Review Queue
new row id: notion-id://redacted
updated registry row: Home-Ansichten Snapshot 2026-05-11
CAP page refreshed: 23 live rows and 8 duplicate review queues
schema changes: 0
content rewrites: 0
delete actions: 0
```

## Next Action

The next safe step is either:

```text
DUP-002
-> current Notion verification for the Untitled and Empty-title queues
-> no deletion
-> create rename candidates only
```

or:

```text
SENS-001
-> protect patent/IP, private, restricted and deep-trigger queues before any deeper duplicate handling
```

Status: complete.
