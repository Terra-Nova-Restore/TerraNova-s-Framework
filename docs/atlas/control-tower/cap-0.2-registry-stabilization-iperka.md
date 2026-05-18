# CAP 0.2 - Registry Stabilization IPERKA

Status: STUDIO execution complete, repo-local
Date: 2026-05-17
Predecessor: `CAP 0.1.0 - Cognitive Ability Point`
Live registry: `notion://redacted-internal-object`
Data source: `notion-ds://redacted-internal-source`

## Purpose

CAP 0.2 turns the created registry into a stabilizing control layer.

CAP 0.1 created the page, schema, initial rows, dashboard views and the sensitive `Home-Ansichten` snapshot reference. CAP 0.2 now makes those objects useful for decision-making without importing the raw workspace into public or semi-public material.

The goal is not more content. The goal is better control.

## Operating Thesis

The TerraNova workspace is over-rich and under-indexed.

The first visible control problem is not missing material. It is weak object state:

- duplicate and empty titles
- mixed PLAY / STUDIO / BIZ material
- unclear canon status
- sync drift between Notion and GitHub
- sensitive objects without explicit handling path
- publication feedback not yet fully backpropagated into the living framework

CAP 0.2 therefore prioritizes status, boundary, canon and sync before deep content interpretation.

## Recovery Anchor Rule

Silvan is not the model.

Silvan is the final recovery anchor when source coherence, boundary logic or operational continuity fails.

Normal operation follows:

```text
Equilibrium
-> CAP Registry
-> canonical sources
-> active mode
-> task
-> reversible action
```

Conflict operation follows:

```text
source conflict
-> boundary unclear
-> status unknown
-> stop mutation
-> preserve trace
-> Silvan recovery anchor
```

The system must not imitate Silvan's personality or transient state. It must preserve operational continuity and use Silvan only as the final reference when the rule system cannot resolve the situation.

## I - Informieren

Known live state:

| Signal | Value |
| --- | --- |
| Registry rows | 25 after PRISM-001 |
| Source-map rows | 22 |
| Snapshot Notion URLs | 808 |
| Snapshot unique Notion IDs | 808 |
| Snapshot duplicate ID groups | 0 |
| Snapshot duplicate title groups | 46 |
| Empty link titles | 30 |
| `Unbenannt` title count | 74 |
| Registry `Needs sync` rows | 11 before SYNC-001; 0 after scoped metadata sync |
| Restricted rows | 1 |
| Sensitive rows | 1 |

Primary anchors:

- `EQUILIBRIUM - Offizielles Regelbuch`
- `CIC - Cognitive Intelligent Cooperation`
- `CAP 0.1.0 - Cognitive Ability Point`
- `CAP 0.1.0 - Workspace Object Registry`
- `CEI-DATA-05 - Workspace Index & Page Census Note`
- `Home-Ansichten Snapshot 2026-05-11`
- `Zenodo RC01-v12 reference`

Hard constraints:

- no Notion Custom Agents
- no credit-consuming Notion automation
- no raw private page list publication
- no deletion as first move
- no broad external mutation without explicit GO
- no personality imitation as governance model
- conscious rule breaks must be marked; unmarked rule forgetting is not allowed

## P - Planen

CAP 0.2 has six workstreams.

| Workstream | Purpose | First input |
| --- | --- | --- |
| `DB-WIKI-001` | Stabilize databases, data sources and wikis. | Current 9 database/wiki/data-source rows. |
| `CANON-001` | Confirm source-of-truth objects and reference objects. | Current `Source of Truth` rows. |
| `SYNC-001` | Reduce `Needs sync` drift. | Current 11 `Needs sync` rows. |
| `DUP-001` | Turn duplicate-title pressure into review queues. | 46 duplicate title groups from snapshot. |
| `SENS-001` | Keep restricted/sensitive material controlled. | Restricted wiki row and Home-Ansichten snapshot. |
| `PRISM-001` | Backpropagate Zenodo/Prism gaps into registry. | RC01-v12 reference and release mirror. |

Batch order:

1. `DB-WIKI-001`
2. `CANON-001`
3. `SYNC-001`
4. `DUP-001`
5. `SENS-001`
6. `PRISM-001`

This order keeps structure ahead of interpretation.

## E - Entscheiden

Decision: CAP 0.2 starts with object governance, not content analysis.

Reason:

```text
808 unique object IDs
-> 0 duplicate ID groups
-> 46 duplicate title groups
-> title/canon/sync coherence is the immediate bottleneck
```

The registry must first tell the system what an object is before the system tries to understand everything inside that object.

Current deterministic boundaries:

- Notion remains the system of record for workspace memory.
- GitHub remains the execution and audit trace.
- Zenodo remains publication snapshot, not live truth.
- Silvan remains recovery anchor, not imitation target.
- `/fff` can steer internally but cannot mutate external systems without explicit GO.

## R - Realisieren

### Batch DB-WIKI-001

Target rows:

- `Cognitive Terranova System`
- `Cognitive Terranova System main data source`
- `Restricted wiki data source`
- `Mermaid Diagrams - Code Library`
- `Meine Notion-KI`
- `Meine Notion-KI wiki data source`
- `Library Sync - 100 Batches`
- `CAP 0.1.0 - Workspace Object Registry`
- `CAP 0.1.0 Registry data source`

Actions:

- verify whether each object still exists
- confirm parent/hub
- mark exact role: source, reference, candidate or restricted
- keep restricted wiki existence-only
- do not import raw child pages

### Batch CANON-001

Target: all `Canon Status = Source of Truth`.

Actions:

- verify each source-of-truth claim
- demote weak source-of-truth rows to `Reference` or `Candidate`
- preserve why a row is canonical in `Causal Chain`
- link deterministic boundary to Equilibrium or CAP rule

### Batch SYNC-001

Target: all `Sync Status = Needs sync`.

Actions:

- decide whether sync means GitHub doc update, Notion row update, or both
- create no external changes without explicit GO
- keep local planned mutations as GitHub trace first

Applied scope:

- reduce the first 11 `Needs sync` rows to `In sync` at registry-governance level
- keep the meaning narrow: GitHub/local trace plus deterministic boundary, not full Notion content mirror
- preserve sensitive snapshot and restricted wiki boundaries
- change no Notion schema and import no raw page inventory

### Batch DUP-001

Target: snapshot duplicate-title groups.

Actions:

- start with `Unbenannt`, empty title, repeated prompt/template titles
- create duplicate groups by title and likely source context
- classify duplicate groups as archive, rename, template, import remnant or active object
- no deletion as first action

Applied scope:

- classify 46 duplicate-title groups into 8 safe review queues
- preserve 0 duplicate-ID-groups finding as the hard boundary
- keep raw URLs, raw Notion IDs and private page lists out of GitHub-facing outputs
- make `Unbenannt` and empty-title groups the first rename-verification target

### Batch SENS-001

Target: restricted and sensitive rows.

Actions:

- ensure sensitive objects have deterministic boundaries
- keep raw snapshot private/local
- do not expose raw restricted wiki titles
- define redaction rule before any export

Applied scope:

- protect five classes: restricted wiki, raw snapshot, patent/IP duplicates, trigger/session exports and private chat/export remnants
- block sensitive/private/restricted duplicate queues from automated DUP-002 cleanup
- allow only aggregate signals and boundary metadata into GitHub-facing artifacts
- preserve no-deletion policy and no raw-title export policy

### Batch PRISM-001

Target: Zenodo / Prism feedback loop.

Actions:

- compare live CAP concepts against RC01-v12 reference
- mark next-release candidates
- keep publication as citable snapshot, not completion
- backpropagate gaps into registry rows and GitHub docs

Applied scope:

- verify RC01-v12 as citable snapshot and foreground anchor
- create seven backpropagation queue rows for citation alignment, CAP hardening, R16, registry logs, sensitivity gates, visual apparatus and no-credit operating policy
- keep Zenodo unchanged
- close CAP 0.2 into CAP 0.3 preparation

## K - Kontrollieren

Control metrics:

| Metric | Target |
| --- | --- |
| `Needs sync` rows | decreasing |
| `Unknown` canon status | zero for control anchors |
| sensitive objects without boundary | zero |
| duplicate groups without decision | decreasing |
| source-of-truth rows without causal chain | zero |
| Prism/Zenodo feedback rows without understanding state | zero |
| external mutations without explicit GO | zero |

Every batch must produce:

- source trace
- selected action
- deterministic boundary
- feedback target
- local GitHub trace
- Notion mutation package only if explicitly authorized

## A - Auswerten

After each batch:

```text
What changed?
What became more coherent?
What is still unknown?
What needs Silvan as recovery anchor?
What can be safely automated later without Notion credits?
```

CAP 0.2 is complete when:

- databases and wikis are role-stable
- canonical anchors are defensible
- sync-needed rows are triaged
- duplicate-title groups have review queues
- sensitive sources have clear boundaries
- Prism/Zenodo feedback has a first backpropagation queue

## Next Action

After `PRISM-001`, CAP 0.2 hands off to `CAP 0.3 - Operational Control IPERKA`.

Local CAP 0.3 trace:

```text
docs/atlas/control-tower/cap-0.3-operational-control-iperka.md
```

The next Notion mutation requires an explicit GO.
