# CAP 0.4 - Canon Admission IPERKA

Status: STUDIO plan, repo-local, Notion mutation pending explicit GO  
Date: 2026-05-17  
Predecessor: `CAP 0.3 - Operational Control IPERKA`  
Primary input: `MMD-007 - CAP Module Source Review`

## Purpose

CAP 0.4 turns the canon problem into an explicit admission system.

CAP 0.3 made the Control Tower operable. MMD-001 through MMD-007 then built a repeatable path from Mermaid visual structure to CAP module drafts and source review. The remaining risk is not lack of material. The risk is uncontrolled canon growth: raw exports, plausible module stories, visual references and historical trigger memory can look authoritative before they are actually source-safe.

CAP 0.4 therefore defines how material may enter canon, what level it may enter at, and when it must stay in draft, candidate, sensitivity hold or source review.

## Operating Thesis

Canon is not discovered by intensity, familiarity or narrative fit. Canon is admitted.

Admission requires:

- exact source trace
- source tier classification
- boundary statement
- reversibility
- sensitivity clearance
- Equilibrium check
- feedback target

If any requirement is missing, the claim may still be useful, but it stays below canon.

## Deterministic Boundaries

Hard limits:

- no canonical `TRG-*` assignment from visual evidence alone
- no execution rule from a draft module
- no public canon from raw Notion export, chat memory or private snapshot
- no Schattenarchiv-depth expansion without separate sensitivity review
- no AutoFlow expansion from sibling references
- no public Prism/Zenodo claim unless the publication boundary is explicit
- no Notion registry mutation without explicit GO
- no deletion or demotion of existing canon without a separate review package

`/fff` may accelerate source routing and candidate review. It cannot bypass the admission ladder.

## Canon Admission Ladder

| Level | Meaning | Admission Threshold |
| --- | --- | --- |
| `L0-ID-ANCHOR` | A number, object or label exists as a usable internal anchor. | One reviewed source or controlled registry trace; no sensitivity block. |
| `L1-NAME-CLUSTER` | Name, cluster and basic role are source-supported. | L0 plus source-tier classification and no conflicting higher-priority source. |
| `L2-ROUTING-MARKER` | The object can steer internal routing inside CAP. | L1 plus guard, relation or bounded operational context. |
| `L3-MODULE-SEMANTICS` | The object has source-supported module semantics. | Direct primary definition plus corroboration plus explicit blocked claims. |
| `L4-EXECUTION-OR-PUBLIC` | The object can drive execution or public canon. | L3 plus tests, SENS clearance, Equilibrium check and publication boundary. |

## Source Tier Model

CAP 0.4 uses `canon-source-tier-map.csv` as the admission map.

The short rule:

```text
Published/reference anchor beats repo draft.
Repo reviewed artifact beats extracted graph.
Extracted graph beats raw export.
Raw export never creates public canon by itself.
Session directive can authorize work, not truth.
Inference can suggest a queue item, not canon.
```

## I - Informieren

Current state:

| Signal | Value |
| --- | --- |
| Live registry rows | 32 after `MMD-006` |
| CAP module drafts | 5 |
| MMD-007 reviewed modules | 5 |
| Current admitted L2 candidates | `516`, `520`, `540`, `544` |
| Current protected L1 candidate | `521` |
| Canonical `TRG-*` assignments from MMD path | 0 |
| External mutation in CAP 0.4 boot | 0 |

Active sources:

- `mmd-007.cap-module-source-review.md`
- `mmd-007.source-review.csv`
- `mmd-007.canon-decision-queue.csv`
- `mmd-005.cap-module-drafts.csv`
- `mmd-004.candidate-review.csv`
- `mmd-003.visual-trigger-candidates.csv`
- `trigger-001.command-surface.md`
- `sens-001.boundary-map.csv`
- `docs/references/zenodo.md`

Open pressure:

- CAP module draft rows exist in Notion, but their canon level is local only.
- Canon admission needs a registry-ready field vocabulary before live update.
- Trigger history remains much larger than the current five safe module candidates.
- Mermaid and VORTEX material can guide review, but cannot alone become public canon.

## P - Planen

CAP 0.4 has six workstreams.

| Workstream | Purpose | Output |
| --- | --- | --- |
| `CAP4-BOOT-001` | Create the canon admission IPERKA and freeze the admission boundary. | This file and causal log. |
| `CANON-002` | Define the admission rulebook and source tiers. | `canon-admission-rulebook.md`, `canon-source-tier-map.csv`. |
| `CANON-003` | Convert MMD-007 decisions into an elevation queue. | `canon-elevation-queue.csv`. |
| `REGISTRY-002` | Prepare a future Notion field/update package for canon level, source tier and blocked claims. | Mutation package later; no live write in CAP4 boot. |
| `SENS-002` | Bind sensitivity holds to canon admission. | Protected lane review before L3/L4. |
| `CAP4-CLOSE-001` | Decide whether canon admission is ready for live registry update. | Close report or Notion apply package. |

Batch order:

1. `CAP4-BOOT-001`
2. `CANON-002`
3. `CANON-003`
4. `REGISTRY-002`
5. `SENS-002`
6. `CAP4-CLOSE-001`

## E - Entscheiden

Decision: CAP 0.4 starts repo-local.

Reason:

```text
MMD-007 found valid L1/L2 candidates
-> live registry rows still only know Candidate/Needs sync
-> adding canon levels live would be useful but not urgent
-> first we need the source-tier rulebook and elevation queue
-> only then should Notion receive a mutation package
```

Selected stance:

- admit weak claims at low level instead of pretending they are complete
- preserve module usefulness without over-claiming origin or execution semantics
- make blocked claims first-class data, not footnotes
- keep every elevation reversible

## R - Realisieren

### Batch CAP4-BOOT-001

Actions:

- create CAP 0.4 IPERKA
- create canon admission rulebook
- create source-tier map
- create canon elevation queue
- create CANON-002 batch record
- create CAP 0.4 causal log
- update README and AUTO-001 control checks

### Batch CANON-002

Actions:

- define admission fields
- define source tiers
- define claim states
- define stop rules
- define downgrade rules

### Batch CANON-003

Input:

- `mmd-007.source-review.csv`
- `mmd-007.canon-decision-queue.csv`

Actions:

- keep `516`, `520`, `540`, `544` at L2 until primary definitions exist
- keep `521` at L1 until protection/preflight source review exists
- create next-source actions for L3 admission
- block L4 until tests and publication boundary exist

### Batch REGISTRY-002

Future Notion fields to prepare:

- `Canon Level`
- `Source Tier`
- `Canon Decision`
- `Blocked Claims`
- `Next Source Action`
- `Admission Review`

No field or row mutation is allowed until an explicit Notion apply command exists.

### Batch SENS-002

Actions:

- review `521`, `777`, `988-992`, private exports and token/integrity material before any elevation
- keep raw snapshot sources below public canon
- require redaction before public-facing source maps

### Batch CAP4-CLOSE-001

Exit check:

```text
Can a future reviewer explain exactly why a claim entered canon,
why it stopped at a level,
what source supported it,
and what would downgrade it?
```

## K - Kontrollieren

Control metrics:

| Metric | Target |
| --- | --- |
| Canon claims without source tier | 0 |
| L3 claims without primary definition | 0 |
| L4 claims without test and publication boundary | 0 |
| Source-review rows with blocked claims | 100% |
| Elevation queue rows with next action | 100% |
| Sensitivity-held rows elevated without SENS review | 0 |
| Notion mutations without explicit GO | 0 |
| Notion AI credits used | 0 |

Every canon admission record must answer:

```text
What is the claim?
Which source tier supports it?
Which level is allowed now?
Which claims are blocked?
What source action is required for the next level?
What would reverse or downgrade it?
```

## A - Auswerten

CAP 0.4 is complete when:

- the rulebook exists and is referenced by AUTO-001
- source tiers are stable enough for registry use
- the MMD-007 module candidates have elevation queue rows
- protected material remains below L3/L4 until reviewed
- a future Notion mutation package can be generated without inventing fields or claims

Next likely batch after CAP 0.4 boot:

```text
CANON-002 - Admission Rulebook Application
```

Best next move after this file: prepare a Notion-safe registry update package for canon fields, but do not apply it until Silvan gives explicit GO.
