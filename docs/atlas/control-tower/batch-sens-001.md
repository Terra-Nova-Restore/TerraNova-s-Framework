# SENS-001 - Sensitivity Boundary Stabilization

Status: Notion metadata package applied, local trace synced
Date: 2026-05-17
Parent IPERKA: `CAP 0.2 - Registry Stabilization IPERKA`
Mutation policy: metadata-only Notion updates after explicit SENS-001 instruction

## Purpose

`SENS-001` protects the sensitive and restricted surfaces before deeper duplicate handling.

It does not inspect or expose raw sensitive content. It defines which classes are blocked, which can continue at aggregate level, and which require current Notion verification before any rename, merge, archive or export decision.

## Protected Inputs

| Input | Sensitivity | Boundary |
| --- | --- | --- |
| `Restricted wiki data source` | Restricted | Existence-only marker; no raw child titles or content. |
| `Home-Ansichten Snapshot 2026-05-11` | Sensitive | Aggregate counts only; no raw private page list. |
| `DUP-001 Patent/IP dossier titles` | Sensitive | No public detail expansion; no merge/rename before IP boundary review. |
| `DUP-001 Trigger/session/deep-system exports` | Internal/Restricted | No public reuse; review against trigger/session canon first. |
| `DUP-001 Chat/person/export remnants` | Private | Private review required before archive or summarization. |

## Boundary Decisions

| Boundary ID | Class | Decision |
| --- | --- | --- |
| `SENS-001-A` | Restricted wiki | Keep existence-only; never export child titles from registry work. |
| `SENS-001-B` | Raw snapshot | Keep local and sensitive; only aggregate duplicate/count signals may enter GitHub. |
| `SENS-001-C` | Patent/IP duplicates | Block DUP-002 action until IP/redaction review exists. |
| `SENS-001-D` | Trigger/session/deep-system duplicates | Keep internal; require trigger/session canon check before reuse. |
| `SENS-001-E` | Chat/person/export remnants | Treat as Private; archive candidates only after source check. |

## Applied Local Result

```text
protected boundary classes: 5
restricted raw-title exports: 0
raw snapshot exports: 0
delete actions: 0
public-release promotions: 0
credit-consuming Notion agent runs: 0
```

## Notion Metadata Package

Applied Notion metadata result:

```text
new registry row: SENS-001 Sensitivity Boundary Queue
new row id: 363f7297-de7e-817f-9641-efa61b2eb502
updated row: Restricted wiki data source
updated row: Home-Ansichten Snapshot 2026-05-11
updated row: DUP-001 Duplicate Title Review Queue
CAP page refreshed: 24 live rows and 5 protected sensitivity classes
schema changes: 0
content rewrites: 0
```

## Done Criteria

`SENS-001` is complete when:

- restricted and sensitive registry rows have explicit deterministic boundaries
- DUP-001 sensitive/private/restricted classes are blocked from automated cleanup
- CAP page reflects the added sensitivity boundary layer
- raw private inventory remains outside GitHub-facing artifacts

Status: complete.
