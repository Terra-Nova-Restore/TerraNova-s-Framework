# DUP-002 - Safe Duplicate Verification

Status: STUDIO plan, repo-local
Date: 2026-05-17
Predecessor: `DUP-001 Duplicate Title Review Queue`
External mutation: none

## Recommended Variant

Run DUP-002 as a safe verification pass, not as cleanup.

The best quality path is:

```text
aggregate duplicate queues
-> sensitivity gate
-> low-risk verification lanes
-> rename/archive proposals
-> explicit Notion mutation later
```

This avoids the main failure mode: treating duplicate titles as duplicate content.

## Purpose

DUP-002 turns the eight DUP-001 review queues into actionable verification lanes.

It does not delete, merge, move or rename any Notion page. It prepares controlled decisions for later Notion work.

## Input State

| Signal | Value |
| --- | --- |
| Snapshot Notion URLs | 808 |
| Unique Notion IDs | 808 |
| Duplicate ID groups | 0 |
| Duplicate title groups | 46 |
| Duplicate title occurrences | 226 |
| Untitled + empty occurrences | 104 |
| Sensitive boundary classes | 5 |

## Decision

DUP-002 starts with low-risk internal queues only.

Immediate lanes:

- `DUP-002-A`: untitled placeholders
- `DUP-002-B`: prompt/action templates
- `DUP-002-E`: navigation/working surfaces
- `DUP-002-F`: generic low-signal titles
- `DUP-002-H`: capability/governance concepts

Gated lanes:

- `DUP-002-C`: patent/IP dossier titles
- `DUP-002-D`: trigger/session/deep-system exports
- `DUP-002-G`: chat/person/export remnants

Reason:

```text
DUP-001 title signal
-> SENS-001 boundary map
-> low-risk lanes first
-> protected lanes stay blocked
```

## Verification Rules

Every candidate must be classified before any Notion mutation:

| Class | Meaning | Allowed next action |
| --- | --- | --- |
| `Active source` | Current page is a real hub/source. | Keep and improve title only if needed. |
| `Template family` | Repeated title is intentional template behavior. | Consolidate naming; do not archive. |
| `Import remnant` | Weak/stale page with no active role. | Propose archive, not deletion. |
| `Working note` | In-progress page with unclear role. | Rename into inbox/workbench pattern. |
| `Protected object` | Sensitive/private/restricted content. | Stop and route to SENS gate. |
| `Unknown` | Not enough source evidence. | No mutation. |

## Rename Pattern

Use clear, reversible names:

```text
[Domain] - [Specific object] - [Role]
```

Examples:

- `INBOX - Untitled Note - Needs Source Check`
- `Prompt Library - Korrekturlesen`
- `Prompt Library - Schreibstil verbessern`
- `Dashboard - TerraNova Workspace Control`
- `Governance - CAP Support Concept`

Blocked names:

- vague single words
- hidden private references
- raw UUID fragments
- names that imply deletion or completion

## Batch Plan

1. Build the DUP-002 verification manifest.
2. Apply SENS-001 gates before each queue.
3. Prepare rename/archive proposals only for low-risk lanes.
4. Keep raw Notion URLs and raw IDs out of GitHub-facing artifacts.
5. Use the live `Duplicate Review` Notion view for manual inspection later.
6. Mutate Notion pages only after a separate explicit GO.

## Control Metrics

| Metric | Target |
| --- | --- |
| Deletions | 0 |
| Raw private ID exports | 0 |
| Protected lanes touched | 0 |
| Low-risk lanes with review path | 5 of 5 |
| Gated lanes with stop rule | 3 of 3 |
| Mutation package before Notion writes | required |

## Next Action

Create:

- `dup-002.verification-manifest.csv`
- `dup-002.rename-rules.md`
- `causal-log.dup-002-plan-2026-05-17.json`

Then move to `PRISM-002` or apply DUP-002 to Notion only after explicit mutation approval.
