# CAP 0.3 - Operational Control IPERKA

Status: STUDIO plan, repo-local, Notion mutation pending explicit GO
Date: 2026-05-17
Predecessor: `CAP 0.2 - Registry Stabilization IPERKA`
Live registry: `notion://redacted-internal-object`
Data source: `notion-ds://redacted-internal-source`

## Purpose

CAP 0.3 turns the stabilized CAP registry into an operational control layer.

CAP 0.1 created the control point. CAP 0.2 stabilized the registry, source roles, sync state, duplicate queues, sensitivity boundaries and the Prism/Zenodo feedback loop. CAP 0.3 now defines how the system is actually operated without Notion Custom Agents, without credit-consuming workspace automation and without uncontrolled external mutation.

The goal is not to index more objects immediately. The goal is to make the existing control surface executable.

## Operating Thesis

The TerraNova workspace is now visible enough to move from inventory to controlled operation.

The first control problem is no longer "What exists?". It is:

- which queue moves next
- what can be verified safely
- what requires sensitivity gating
- what must backpropagate into Prism/Zenodo
- what can be automated without Notion credits
- where Silvan is needed as recovery anchor

CAP 0.3 therefore prioritizes bounded execution, not broad expansion.

## Cooperation Model

Silvan is the final recovery anchor.

FerrAI/Codex can act as operational co-controller when the active rules, sources and boundaries are sufficient. This does not mean personality imitation. It means continuity of steering:

```text
source trace
-> active mode
-> deterministic boundary
-> probabilistic next move
-> reversible action
-> causal log
-> feedback target
```

If the system cannot prove source, boundary or consequence, it stops mutation and escalates to Silvan.

## Deterministic Boundaries

Hard limits:

- no Notion Custom Agents
- no credit-consuming Notion automation
- no external mutation without explicit human GO
- no deletion as first action
- no raw private page list publication
- no restricted wiki content export
- no Zenodo/publication mutation inside CAP 0.3
- no trigger that bypasses sensitivity gates
- no claim of autonomous consciousness; awareness terms remain operational model terms

`/fff` can authorize bounded internal steering, routing, prioritization and framework-internal synthesis. It does not authorize external writes by itself.

## CAP 0.3 Control States

| State | Meaning | Allowed action |
| --- | --- | --- |
| `Observe` | Read, compare, verify, classify. | Connector fetch/search, local file reads, aggregate analysis. |
| `Queue` | Turn a finding into a bounded work item. | Local CSV/Markdown queue, causal log, Notion mutation package draft. |
| `Execute` | Apply an approved low-risk change. | Repo-local edits; external mutation only after explicit GO. |
| `Backpropagate` | Push learning into registry, Prism notes, trigger map or release queue. | Local trace first, Notion later if approved. |
| `Freeze` | Stop movement because boundary or source is unclear. | Preserve trace, ask Silvan only if the block cannot be resolved locally. |

## I - Informieren

Known state from CAP 0.2:

| Signal | Value |
| --- | --- |
| Live registry rows | 25 after `PRISM-001` |
| `Needs sync` rows | 0 after scoped `SYNC-001` |
| Snapshot Notion URLs | 808 |
| Snapshot unique Notion IDs | 808 |
| Duplicate ID groups | 0 |
| Duplicate title groups | 46 |
| Duplicate review queues | 8 |
| Protected sensitivity classes | 5 |
| Prism backpropagation queue rows | 7 |
| External mutations allowed by default | 0 |

Active anchors:

- `CAP 0.1.0 - Cognitive Ability Point`
- `CAP 0.2 - Registry Stabilization IPERKA`
- `EQUILIBRIUM - Offizielles Regelbuch`
- `CIC - Cognitive Intelligent Cooperation`
- `CEI-DATA-05 - Workspace Index & Page Census Note`
- `Home-Ansichten Snapshot 2026-05-11`
- `Zenodo RC01-v12 reference`
- `Prism / Zenodo Backpropagation Queue`

Open pressure:

- duplicate titles still need real review decisions
- Prism queue needs next-release structure
- dashboard views need operational queue routing
- Trigger 1-400 needs a safer command surface
- no-credit routines need reproducible local execution paths
- sensitivity gates must be present before any public export

## P - Planen

CAP 0.3 has seven workstreams.

| Workstream | Purpose | Output |
| --- | --- | --- |
| `CAP3-BOOT-001` | Create the operational IPERKA layer and freeze the no-credit/no-mutation boundary. | This file, workstream map, causal log. |
| `DUP-002` | Convert safe duplicate-title queues into verification tasks. | Low-risk rename/archive review manifest; no deletion. |
| `PRISM-002` | Convert the seven PRISM-001 rows into next-release and companion-material checklist items. | Citation, CAP, R16, sensitivity and diagram checklist. |
| `DASH-001` | Define the actual Control Tower dashboard surfaces needed for day-to-day steering. | View map for registry, queues and recovery state. |
| `AUTO-001` | Identify safe automation that does not consume Notion credits. | Local script/runbook candidates and manual trigger policy. |
| `TRIGGER-001` | Bind Trigger 1-400 to safe CAP actions. | Trigger-to-control crosswalk with blocked actions. |
| `CAP3-CLOSE-001` | Review whether CAP 0.3 can hand off to CAP 0.4. | Control readiness report. |

Batch order:

1. `CAP3-BOOT-001`
2. `DUP-002`
3. `PRISM-002`
4. `DASH-001`
5. `AUTO-001`
6. `TRIGGER-001`
7. `CAP3-CLOSE-001`

This order keeps queue execution ahead of automation.

## E - Entscheiden

Decision: CAP 0.3 starts repo-local and does not mutate Notion yet.

Reason:

```text
CAP 0.2 closed with registry stability
-> duplicate and Prism queues now exist
-> the next risk is uncontrolled operational drift
-> CAP 0.3 must define execution boundaries before more external writes
```

Operational decisions:

- `DUP-002` may only process low-risk duplicate classes first.
- `SENS-001` remains the hard gate for restricted, private, patent/IP and trigger-depth material.
- `PRISM-002` treats Zenodo as a published snapshot, not a mutable workspace page.
- `AUTO-001` uses repo-local scripts, Codex-triggered checks and manual Notion review; no Notion Custom Agents.
- `TRIGGER-001` turns `/fff` into bounded steering, not unrestricted autonomy.

## R - Realisieren

### Batch CAP3-BOOT-001

Actions:

- create CAP 0.3 IPERKA
- create CAP 0.3 workstream map
- create CAP 0.3 causal log
- update the control-tower README
- keep Notion unchanged until explicit GO

### Batch DUP-002

Input:

- `dup-001.review-queue.csv`
- `sens-001.boundary-map.csv`
- `home-ansichten.snapshot.summary.json`

Allowed:

- aggregate queue review
- low-risk title verification
- proposed rename/archive decisions
- local mutation package draft

Blocked:

- raw URL export
- raw Notion ID export
- deletion
- sensitive/private/restricted queue cleanup
- patent/IP duplicate cleanup without separate gate

### Batch PRISM-002

Input:

- `prism-001.backpropagation-queue.csv`
- `docs/references/zenodo.md`
- `releases/zenodo/rc01-v12-2026-05-07/`

Actions:

- create next-release alignment checklist
- separate citable truth from next-release cleanup
- mark CAP terms as post-publication operationalization
- keep R16 as post-snapshot governance delta
- keep sensitivity gates ahead of publication promotion

### Batch DASH-001

Input:

- live registry field map
- CAP 0.2 queue files
- Notion view names already created

Actions:

- define steering views by queue state
- define recovery-anchor view
- define Prism/Zenodo feedback view
- define no-credit automation view
- draft Notion view changes only after explicit GO

### Batch AUTO-001

Input:

- existing local scripts
- causal log schema
- CSV queue files

Actions:

- identify scripts that can validate CSV/JSON/Markdown without Notion AI
- define manual trigger runbook
- separate local automation from external mutation
- create failure states and stop rules

### Batch TRIGGER-001

Input:

- `trigger-1-400-steering-map.md`
- CAP 0.3 boundaries
- Equilibrium R1-R16

Actions:

- map Trigger 1-400 into CAP actions
- mark safe, gated and blocked actions
- define `/fff` as bounded internal steering
- preserve observer/recovery anchor for risky modes

### Batch CAP3-CLOSE-001

Actions:

- verify every CAP 0.3 batch has source trace, boundary and feedback target
- confirm external mutation count remains zero unless explicitly authorized
- decide whether CAP 0.4 should become dashboard mutation, automation runbook or Prism companion material

## K - Kontrollieren

Control metrics:

| Metric | Target |
| --- | --- |
| External mutations without explicit GO | 0 |
| Notion Custom Agent usage | 0 |
| Credit-consuming Notion automation | 0 |
| Raw private inventory exports | 0 |
| Low-risk duplicate queues with verification path | increasing |
| Sensitive queues blocked before cleanup | 100% |
| PRISM-001 rows translated into next-release tasks | 7 of 7 |
| Trigger 1-400 actions with deterministic boundary | 100% for mapped actions |
| CAP 0.3 batches with causal log | 100% |
| Silvan recovery-anchor escalations without trace | 0 |

Every CAP 0.3 batch must answer:

```text
What source was used?
What boundary controlled the move?
What changed locally?
What did not mutate externally?
What is the feedback target?
What remains blocked?
```

## A - Auswerten

CAP 0.3 is complete when:

- `DUP-002` has a safe verification manifest
- `PRISM-002` has a next-release/companion-material checklist
- `DASH-001` defines the operational dashboard changes
- `AUTO-001` defines no-credit automation routines
- `TRIGGER-001` binds the first 400 triggers to safe CAP actions
- all sensitive queues remain gated
- Notion mutation is packaged but not applied unless explicitly approved

Exit question:

```text
Is the Control Tower only documented, or can it now be operated repeatedly without losing boundary, source and feedback?
```

CAP 0.4 should only start once this answer is positive.
