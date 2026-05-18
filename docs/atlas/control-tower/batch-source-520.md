# SOURCE-520 - SessionStart Primary Source Pass

Status: source pass complete, TEST-520 complete, Notion mutation applied on 2026-05-18
Date: 2026-05-18
Parent gate: `CAP 0.4 - Canon Admission`
Mutation policy: live Notion metadata update applied only after explicit command `GO Notion SOURCE-520`

## Purpose

`SOURCE-520` answers the open CAP 0.4 question:

```text
Can CAP-MOD-DRAFT-520 - SessionStart stay at L2 with stronger T2
source backing, and what must exist before L3 module semantics are allowed?
```

## Sources Checked

The pass used targeted Notion `workspace_search` plus page fetches and repo-local
source review.

Strongest sources:

- Notion `Trigger - Systemtabelle (aktiv)` as live system-of-record page.
- Notion `Trigger-Module - Terra Nova Native` as module specification page.
- Notion `Notion AI (FerrAI) - Systemhandbuch` as live reference for the
  `/start` action surface.

Supporting sources:

- Notion `Trigger_Index_TerraNova_V5.3`
- Notion `02_Codex & Trigger`
- Notion `Manifeste & Trigger - Systemarchitektur`
- Notion `TerraNova - Entwicklungs- & Integrationszone`
- `atlas/sources/trigger-complement-2026-03-30.md`
- `atlas/atlas.manifest.v1.1.json`
- MMD graph extraction outputs
- raw Prism trigger reference exports

## Decision

`520 / SessionStart` passes as source-confirmed local `L2-ROUTING-MARKER`.

Allowed now:

- `520` is the `SessionStart` anchor.
- `/start` is the active internal core entrypoint.
- SessionStart may mark the start of a work unit or session.
- SessionStart may route into the preflight chain through a bounded
  `session_opened` guard.
- SessionStart may be described as an initialization/root-state marker.

Still blocked:

- automatic module execution from `init_all_modules()`
- autonomous session control
- external mutation permission
- Notion Custom Agent behavior or credit-consuming automation
- canonical `TRG-*` assignment
- full historical trigger definition
- L3 module semantics
- public-facing trigger canon

## Notion State

The Notion mutation was applied on 2026-05-18 after explicit GO.

Live registry result:

```text
CAP-MOD-DRAFT-520 - SessionStart
Canon Level: L2-ROUTING-MARKER
Source Tier: T2 Live Notion System Record
Canon Decision: Hold at L2
Admission Review: Source Review Passed
Next Source Action: TEST-520 bounded SessionStart test before L3
```

After `TEST-520`, the live `Next Source Action` is:

```text
TEST-520 completed locally; hold at L2 until implementation contract exists.
```

## Done Criteria

`SOURCE-520` is complete when:

- primary and supporting sources are logged
- claim-by-claim admission is explicit
- L2 is confirmed without importing execution semantics
- a bounded L3 test gate is defined
- live Notion mutation is explicit and traceable
- AUTO-001 validates all new files

Status: complete.
