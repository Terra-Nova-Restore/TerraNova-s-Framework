# SENS-001 Findings - Sensitivity Boundary Stabilization

Status: findings complete, no raw sensitive content imported
Date: 2026-05-17

## Summary

`SENS-001` confirms that the next duplicate pass must not treat all duplicate-title groups equally.

The workspace has at least five protected classes that require a hard boundary before deeper action:

- restricted wiki material
- raw local snapshot inventory
- patent/IP dossier duplicates
- trigger/session/deep-system exports
- chat/person/export remnants

The safe action is to classify boundaries first, then run `DUP-002` only on the low-risk naming queues.

## Decisions

| Class | Decision |
| --- | --- |
| Restricted wiki | Existence-only. Do not export child titles, raw content or inferred page lists. |
| Raw Home-Ansichten snapshot | Aggregate-only. It supports counts and queues, not public inventory. |
| Patent/IP dossier duplicates | Block from rename/merge/archive until explicit IP/redaction review. |
| Trigger/session/deep-system exports | Keep internal and route through trigger/session canon. No public reuse by default. |
| Chat/person/export remnants | Treat as private. Archive only after source check and owner decision. |

## DUP-002 Gate

Allowed first target for `DUP-002`:

```text
Untitled placeholders
Generic low-signal titles
Navigation/working surfaces
Prompt/action templates
```

Blocked until later review:

```text
Patent/IP dossier titles
Trigger/session/deep-system exports
Chat/person/export remnants
Restricted wiki material
Raw Home-Ansichten inventory
```

## Boundary

No raw page list, Notion IDs, restricted child titles, private chat titles or IP details are exported by this batch.

No Notion schema, page content or source database content is rewritten.

