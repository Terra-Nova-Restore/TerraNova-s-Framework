# REGISTRY-002 Apply Gate

Status: prepared, not applied
Date: 2026-05-17
Target: live CAP Workspace Object Registry

## Purpose

REGISTRY-002 prepares the live Notion registry to show canon admission state for CAP module draft rows.

The registry already contains the five module rows created by MMD-006. REGISTRY-002 does not create new module rows. It adds canon admission fields and backfills those five rows with the bounded MMD-007/CAP 0.4 decisions.

## Why This Was Not Applied Immediately

Live Notion mutation changes the system-of-record. The user message asked "anwenden?" as a question, not as an explicit apply command.

Required apply command:

```text
GO Notion REGISTRY-002 anwenden
```

## Planned Mutations

| Mutation | Target | Effect |
| --- | --- | --- |
| `REG2-M001` | Registry database schema | Add canon admission fields. |
| `REG2-M002` | Five CAP module draft rows | Backfill L1/L2 canon metadata. |
| `REG2-M003` | Registry database views | Add `CAP Canon Admission Queue`. |
| `REG2-M004` | CAP page | Append checkpoint. |

## Stop Rules

Stop before mutation if:

- the registry database cannot be resolved
- any of the five MMD-006 Notion row URLs no longer resolves
- a field already exists with incompatible type
- adding fields would overwrite existing data
- the connector cannot create database properties safely
- Notion asks for AI agent/autofill credit use
- the apply command is not explicit

## Invariants

- no deletion
- no raw private page inventory
- no canonical `TRG-*` assignment
- no L3/L4 elevation
- no Status or Canon Status demotion
- no Notion AI credit use

## Verification After Apply

After a future apply:

1. Fetch or inspect the five module rows.
2. Confirm each row has `Canon Level`, `Source Tier`, `Canon Decision`, `Blocked Claims` and `Admission Review`.
3. Confirm `521` is `Sensitivity Review Required`.
4. Confirm no row claims L3/L4.
5. Write `registry-002.registry-updates.csv`.
6. Write `causal-log.registry-002-mutation-2026-05-17.json`.
7. Re-run AUTO-001.
