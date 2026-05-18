# CAP-RT-001 Runtime Contract

## Scope

The CAP runtime is a cooperative control system for the TerraNova/FerrAI
workspace. It coordinates source state, canon admission, sensitivity boundaries,
GitHub trace and Zenodo release truth.

It is not:

- an autonomous Notion agent.
- a deletion or cleanup bot.
- a publication tool.
- a claim that the whole workspace is fully understood.

## Authority Stack

Use this authority order unless a later gate changes it:

1. Live external/public source when the claim is external-facing.
2. Notion workspace memory for internal object state and decisions.
3. GitHub Atlas for audit trace, validation and PR proof.
4. Local snapshots only as historical inputs, never as current truth alone.
5. GPT/Copilot outputs only as drafts until source-backed.

## Gate Types

Runtime gates:

- `READ`: fetch/search/review only.
- `PLAN`: create repo-local plan artifacts.
- `APPLY`: mutate a named system after explicit activation.
- `CHECK`: run validation and boundary scans.
- `DECIDE`: select one of hold, apply, review, merge, close or defer.
- `CLOSE`: record final state and next gate.

## Runtime State Model

Each active lane must track:

- lane id
- object or page cluster
- source of record
- last verified source action
- canon level
- sensitivity class
- current blocker
- next gate
- feedback target

## IPERKA Mapping

Informieren:

- identify source, object, last known gate and conflicting state.

Planen:

- choose one lane and one bounded output.

Entscheiden:

- select apply, hold, review, merge, close or defer.

Realisieren:

- perform the smallest authorized mutation or repo-local artifact update.

Kontrollieren:

- run validator, raw-ID scan and source-specific checks.

Auswerten:

- write causal log, review summary and next gate.

## Default Boundary

No runtime gate may silently:

- delete Notion content.
- move Notion pages.
- expose raw private Notion IDs.
- use Notion Custom Agents or mass AI autofill.
- mutate Zenodo.
- dispatch workflows.
- elevate sensitive Monographie Teil II/III material.
- canonicalize unresolved trigger/SCL/Mermaid material.

## Runtime Success Criteria

The runtime is useful when a future session can answer:

- what is active?
- what is blocked?
- what is allowed?
- what was verified?
- what must happen next?

without reading the entire prior conversation.

