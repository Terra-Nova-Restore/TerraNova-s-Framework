# CAP 0.1.0 - Cognitive Ability Point

Status: STUDIO control tower, Notion-backed as of 2026-05-17  
Owner: Silvan Lenhard / TerraNova  
Operating frame: Equilibrium, CIC, IPERKA, Notion as system of record, GitHub as audit/version trace

This folder defines the first implementation layer for **CAP 0.1.0 - Cognitive Ability Point** as the Control Tower for the TerraNova workspace. It does this without using Notion Custom Agents or credit-consuming autonomous agent runs.

## Files

| File | Role |
| --- | --- |
| `cap-0.1.0.md` | Core CAP definition and operating seed. |
| `object-registry.schema.json` | Registry schema for Notion/GitHub control objects. |
| `source-map.csv` | Read-only map of current CAP source anchors. |
| `workspace-object-registry.seed.csv` | First 21 CAP registry rows, derived from the source map, registry self-registration and Home-Ansichten snapshot. |
| `phase-02-registry-plan.md` | Next implementation plan for the registry layer. |
| `cap-0.2-registry-stabilization-iperka.md` | Next IPERKA layer for registry stabilization and batch control. |
| `cap-0.3-operational-control-iperka.md` | Operational IPERKA layer for queue execution, no-credit routines and bounded trigger steering. |
| `cap-0.3.workstream-map.csv` | CAP 0.3 workstream map and completion signals. |
| `cap-0.4-canon-admission-iperka.md` | Canon admission IPERKA layer for source-tiered canon governance. |
| `canon-admission-rulebook.md` | CAP 0.4 rulebook for canon claims, source tiers, admission levels and downgrade rules. |
| `canon-source-tier-map.csv` | Source-tier authority map for canon admission decisions. |
| `canon-elevation-queue.csv` | Current queue of canon elevation actions and stop conditions. |
| `batch-db-wiki-001.md` | First CAP 0.2 batch plan for databases, data sources and wikis. |
| `batch-canon-001.md` | Source-of-Truth stabilization plan and findings. |
| `batch-canon-002.md` | Canon admission rulebook and source governance boot batch. |
| `batch-dup-001.md` | Duplicate-title review queue plan and findings. |
| `batch-dup-002.md` | Safe duplicate verification plan for CAP 0.3. |
| `db-wiki-001.findings.md` | Read-only findings log for the first DB/wiki stabilization pass. |
| `dup-001.findings.md` | Findings for duplicate-title pressure from the sensitive Home-Ansichten snapshot. |
| `dup-001.review-queue.csv` | Safe aggregate duplicate-title review queues without raw URLs or Notion IDs. |
| `dup-002.verification-manifest.csv` | Safe DUP-002 verification lanes and stop rules. |
| `dup-002.rename-rules.md` | Rename rules for low-risk duplicate-title lanes. |
| `db-wiki-001.registry-updates.csv` | Exact Notion registry metadata changes applied after DB-WIKI-001. |
| `canon-001.registry-updates.csv` | Planned/applied Source-of-Truth metadata updates for CANON-001. |
| `batch-sync-001.md` | Registry sync stabilization plan and scoped sync decisions. |
| `batch-sync-002.md` | Canon field sync closure for the five CAP module draft rows. |
| `batch-sync-003.md` | GitHub trace closure after SOURCE-521 live Notion mutation. |
| `batch-sync-004.md` | GitHub trace closure after TEST-520 and SOURCE-520 live Notion mutation. |
| `sync-001.registry-updates.csv` | Planned/applied Sync Status metadata updates for SYNC-001. |
| `sync-002.registry-updates.csv` | Applied Sync Status closure updates for the five CAP module draft rows. |
| `sync-003.git-trace-manifest.csv` | Scoped inclusion manifest for SYNC-003 local Git trace closure. |
| `sync-004.git-trace-manifest.csv` | Scoped inclusion manifest and branch-state record for SYNC-004. |
| `dup-001.registry-updates.csv` | Planned/applied metadata updates for DUP-001. |
| `batch-sens-001.md` | Sensitivity boundary stabilization plan. |
| `sens-001.findings.md` | Findings for restricted, sensitive and private duplicate classes. |
| `sens-001.boundary-map.csv` | Protected boundary map for SENS-001. |
| `sens-001.registry-updates.csv` | Planned/applied metadata updates for SENS-001. |
| `batch-sens-002.md` | Protected canon lane review for Preflight, Schattenarchiv, integrity/token and raw-export lanes. |
| `sens-002.preflight-boundary.md` | Exact SENS-002 boundary for `CAP-MOD-DRAFT-521 - Preflight`. |
| `sens-002.protected-lane-review.csv` | Seven protected-lane review decisions for SENS-002. |
| `sens-002.elevation-gate.csv` | Five elevation stop rules for protected canon lanes. |
| `sens-002.notion-mutation-package.csv` | Future Notion apply package for SENS-002, currently not applied. |
| `sens-002.review-summary.json` | Machine-readable SENS-002 summary. |
| `batch-source-520.md` | SOURCE-520 batch record for the SessionStart primary source pass. |
| `source-520.primary-source-pass.md` | Human-readable SOURCE-520 source interpretation and canon decision. |
| `source-520.source-ledger.csv` | Ten source rows checked for `520 / SessionStart`. |
| `source-520.claim-review.csv` | Claim-by-claim admission and block table for `520`. |
| `source-520.elevation-decision.csv` | Local L2 confirmation and future Notion apply boundary for `520`. |
| `source-520.bounded-test-gate.csv` | Five required gates before any future `520` L3 module admission. |
| `source-520.notion-mutation-package.csv` | Future Notion mutation package for applying SOURCE-520. |
| `source-520.registry-updates.csv` | Applied Notion update trace for SOURCE-520. |
| `source-520.review-summary.json` | Machine-readable SOURCE-520 summary. |
| `batch-test-520.md` | TEST-520 batch record for the bounded SessionStart test. |
| `test-520.sessionstart-bounded-test.md` | Human-readable TEST-520 contract, input, expected output and result. |
| `test-520.test-cases.csv` | Five bounded SessionStart test cases. |
| `test-520.results.csv` | Five TEST-520 pass results and residual risks. |
| `test-520.review-summary.json` | Machine-readable TEST-520 summary. |
| `batch-source-521.md` | SOURCE-521 batch record for the Preflight primary source pass. |
| `source-521.primary-source-pass.md` | Human-readable SOURCE-521 source interpretation and canon decision. |
| `source-521.source-ledger.csv` | Nine source rows checked for `521 / Preflight`. |
| `source-521.claim-review.csv` | Claim-by-claim admission and block table for `521`. |
| `source-521.elevation-decision.csv` | Local L2 decision and future Notion apply boundary for `521`. |
| `source-521.notion-mutation-package.csv` | Future Notion mutation package for applying SOURCE-521. |
| `source-521.registry-updates.csv` | Applied Notion update trace for SOURCE-521. |
| `source-521.review-summary.json` | Machine-readable SOURCE-521 summary. |
| `batch-prism-001.md` | Zenodo / Prism backpropagation plan. |
| `batch-prism-002.md` | Next-release backpropagation plan for RC01-v13 readiness and companion material. |
| `batch-registry-002.md` | Notion-safe canon field package for future registry mutation. |
| `prism-001.findings.md` | Findings from the RC01-v12 publication snapshot and CAP feedback pass. |
| `prism-001.backpropagation-queue.csv` | Seven-item PRISM-001 next-release and companion-material queue. |
| `prism-001.registry-updates.csv` | Planned/applied metadata updates for PRISM-001. |
| `prism-002.next-release-checklist.csv` | Seven-item PRISM-002 checklist derived from PRISM-001. |
| `prism-002.release-readiness-gate.csv` | Hard release gates before any RC01-v13 Zenodo draft or publish action. |
| `prism-002.companion-material-map.md` | Routing map for CAP deltas into main release, companion, appendix, internal-only or blocked lanes. |
| `prism-002.zenodo-live-delta-2026-05-17.json` | Read-only live Zenodo metadata delta after the 2026-05-17 metadata refresh. |
| `batch-auto-001.md` | No-credit automation and repeatable CAP control checks. |
| `auto-001.check-matrix.csv` | AUTO-001 validation matrix. |
| `auto-001.runbook.md` | AUTO-001 runbook for local and live-read checks. |
| `auto-001.test-results-2026-05-17.json` | First AUTO-001 test run result with live Zenodo read. |
| `auto-001.test-results-2026-05-18.json` | Latest AUTO-001 test run result with live Zenodo read. |
| `batch-ninf-001.md` | CAP 0.3 Notion infiltration readpass and future mutation package. |
| `ninf-001.findings.md` | Read-only Notion findings for CAP page, registry and tool limitation. |
| `ninf-001.notion-mutation-package.csv` | Proposed Notion updates that require explicit GO before execution. |
| `ninf-001.registry-updates.csv` | Applied Notion updates for NINF-001. |
| `registry-002.field-package.csv` | Proposed canon admission fields for the live registry. |
| `registry-002.module-canon-updates.csv` | Five prepared CAP module row backfills for canon admission metadata. |
| `registry-002.notion-mutation-package.csv` | Planned REGISTRY-002 live Notion mutations requiring explicit GO. |
| `registry-002.apply-gate.md` | Stop rules and verification plan for applying REGISTRY-002. |
| `registry-002.registry-updates.csv` | Applied Notion schema, row, view and CAP page update trace for REGISTRY-002. |
| `registry-002.review-summary.json` | Machine-readable REGISTRY-002 package summary. |
| `notion-registry-field-map.md` | Notion database field and view mapping for the registry. |
| `trigger-1-400-steering-map.md` | Bounded steering map for `/fff` and Trigger 1-400. |
| `batch-trigger-001.md` | TRIGGER-001 implementation plan for bounded command-surface hardening. |
| `trigger-001.command-surface.md` | Active command rules for `/fff`, GO, STOP and FREEZE forms. |
| `trigger-001.control-crosswalk.csv` | Known trigger anchors mapped to CAP states, allowed actions and gates. |
| `trigger-001.blocked-actions.csv` | Explicit blocked/gated action list for trigger handling. |
| `trigger-001.test-cases.csv` | Test cases for `/fff` and trigger safety behavior. |
| `causal-log.schema.json` | Machine-readable causal coherence log schema. |
| `causal-log.cap-creation-2026-05-17.json` | First causal log event for the CAP Notion page creation. |
| `causal-log.registry-creation-2026-05-17.json` | Causal log event for the live registry creation. |
| `causal-log.cap-0.2-iperka-2026-05-17.json` | Causal log event for CAP 0.2 IPERKA creation. |
| `causal-log.db-wiki-001-readpass-2026-05-17.json` | Causal log event for the DB-WIKI-001 read-only pass. |
| `causal-log.db-wiki-001-mutation-2026-05-17.json` | Causal log event for the DB-WIKI-001 registry metadata update. |
| `causal-log.canon-001-readpass-2026-05-17.json` | Causal log event for the CANON-001 read-only pass. |
| `causal-log.canon-001-mutation-2026-05-17.json` | Causal log event for the CANON-001 registry metadata update. |
| `causal-log.sync-001-readpass-2026-05-17.json` | Causal log event for the SYNC-001 read-only pass. |
| `causal-log.sync-001-mutation-2026-05-17.json` | Causal log event for the SYNC-001 registry metadata update. |
| `causal-log.sync-002-mutation-2026-05-17.json` | Causal log event for the SYNC-002 canon-field sync closure. |
| `causal-log.dup-001-readpass-2026-05-17.json` | Causal log event for the DUP-001 read-only pass. |
| `causal-log.dup-001-mutation-2026-05-17.json` | Causal log event for the DUP-001 registry metadata update. |
| `causal-log.dup-002-plan-2026-05-17.json` | Causal log event for the DUP-002 safe verification plan. |
| `causal-log.sens-001-readpass-2026-05-17.json` | Causal log event for the SENS-001 read-only pass. |
| `causal-log.sens-001-mutation-2026-05-17.json` | Causal log event for the SENS-001 registry metadata update. |
| `causal-log.sens-002-plan-2026-05-17.json` | Causal log event for the SENS-002 protected canon lane review. |
| `causal-log.source-520-primary-source-pass-2026-05-18.json` | Causal log event for the SOURCE-520 SessionStart primary source pass. |
| `causal-log.test-520-bounded-sessionstart-2026-05-18.json` | Causal log event for the TEST-520 bounded SessionStart test. |
| `causal-log.source-520-mutation-2026-05-18.json` | Causal log event for the applied SOURCE-520 live Notion mutation. |
| `causal-log.source-521-primary-source-pass-2026-05-17.json` | Causal log event for the SOURCE-521 Preflight primary source pass. |
| `causal-log.source-521-mutation-2026-05-18.json` | Causal log event for the applied SOURCE-521 live Notion mutation. |
| `causal-log.sync-003-github-trace-closure-2026-05-18.json` | Causal log event for SYNC-003 GitHub trace closure. |
| `causal-log.sync-004-github-trace-closure-2026-05-18.json` | Causal log event for SYNC-004 GitHub trace closure. |
| `causal-log.prism-001-readpass-2026-05-17.json` | Causal log event for the PRISM-001 read-only pass. |
| `causal-log.prism-001-mutation-2026-05-17.json` | Causal log event for the PRISM-001 registry metadata update. |
| `causal-log.prism-002-plan-2026-05-17.json` | Causal log event for the PRISM-002 next-release backpropagation plan. |
| `causal-log.registry-002-plan-2026-05-17.json` | Causal log event for the REGISTRY-002 Notion-safe canon field package. |
| `causal-log.registry-002-mutation-2026-05-17.json` | Causal log event for the applied REGISTRY-002 live Notion mutation. |
| `causal-log.auto-001-plan-2026-05-17.json` | Causal log event for AUTO-001 no-credit validation automation. |
| `causal-log.trigger-001-plan-2026-05-17.json` | Causal log event for TRIGGER-001 command-surface hardening. |
| `causal-log.cap-0.3-iperka-2026-05-17.json` | Causal log event for the CAP 0.3 operational-control IPERKA creation. |
| `causal-log.cap-0.4-iperka-2026-05-17.json` | Causal log event for the CAP 0.4 canon admission IPERKA creation. |
| `causal-log.ninf-001-readpass-2026-05-17.json` | Causal log event for the NINF-001 Notion read-only infiltration pass. |
| `causal-log.ninf-001-mutation-2026-05-17.json` | Causal log event for the applied NINF-001 Notion visibility mutation. |
| `home-ansichten-snapshot-2026-05-11.md` | Sensitive local snapshot brief for the 808-URL export support file. |
| `home-ansichten.snapshot.summary.json` | Machine-readable snapshot count summary. |
| `notion-mutation-gate.md` | Pre-write gate for the first Notion CAP page. |
| `batch-mmd-005.md` | CAP module draft batch record for the five MMD-004 eligible references. |
| `mmd-005.cap-module-drafts.md` | Human-readable CAP module draft summary for `516`, `520`, `521`, `540` and `544`. |
| `mmd-005.cap-module-drafts.csv` | Five local CAP draft module records. |
| `mmd-005.module-evidence.csv` | Evidence rows for visual candidates, guards and Atlas context. |
| `mmd-005.module-relation-map.csv` | Module relation map across Atlas context and MMD-004 guards. |
| `mmd-005.hash-ledger.csv` | Draft hash handles and SHA-256 fingerprints. |
| `mmd-005.hash-material.json` | Hash material used to produce deterministic draft fingerprints. |
| `mmd-005.review-summary.json` | Machine-readable MMD-005 summary. |
| `batch-mmd-006.md` | CAP module registry package batch record. |
| `mmd-006.registry-package.md` | Human-readable MMD-006 registry package summary. |
| `mmd-006.registry-package.csv` | Five Notion-ready registry rows for the CAP module drafts. |
| `mmd-006.registry-field-map.csv` | Registry schema field mapping and source rules for the package. |
| `mmd-006.view-package.csv` | Two proposed registry views for CAP module drafts. |
| `mmd-006.notion-mutation-package.csv` | Exact planned Notion mutations requiring explicit GO. |
| `mmd-006.apply-gate.md` | Apply gate, stop rules and verification steps for the live registry mutation. |
| `mmd-006.registry-updates.csv` | Applied Notion row, view and CAP page update trace for MMD-006. |
| `mmd-006.review-summary.json` | Machine-readable MMD-006 summary. |
| `batch-mmd-007.md` | CAP module source review batch record. |
| `mmd-007.cap-module-source-review.md` | Human-readable MMD-007 source review and canon admission ladder. |
| `mmd-007.source-index.csv` | Source-tier index for the five CAP module draft rows. |
| `mmd-007.canon-admission-levels.csv` | Canon admission ladder used for module source review. |
| `mmd-007.source-review.csv` | Per-module allowed and blocked canon claims. |
| `mmd-007.canon-decision-queue.csv` | Next source actions required before higher canon admission. |
| `mmd-007.review-summary.json` | Machine-readable MMD-007 summary. |

## Live Notion Registry

| Object | Value |
| --- | --- |
| CAP page | `https://www.notion.so/363f7297de7e816e840ae8d95cfd7842` |
| Registry database | `https://www.notion.so/f9aafd4eaf9046e0beb7552b1018af83` |
| Registry data source | `collection://f8e7df9f-e1ed-43f0-888b-39d362f2cef2` |
| Initial rows | 21 |
| Current live rows | 32 after `MMD-006` |
| Current `Needs sync` rows | 0 for the CAP module draft lane after `SYNC-002` scoped closure |
| Duplicate review queues | 8 after `DUP-001` |
| Protected sensitivity classes | 5 after `SENS-001` |
| Prism backpropagation queue rows | 7 after `PRISM-001` |
| Created views | `By Status`, `By Object Type`, `By Sensitivity`, `Canonical Sources`, `Prism / Zenodo Feedback`, `CAP 0.3 Operations`, `Duplicate Review`, `CAP Module Drafts`, `CAP Module Sync Needed`, `CAP Canon Admission Queue` |
| CAP page dashboard views | `CAP Registry - By Status`, `CAP Registry - Canonical Sources`, `CAP Registry - Sync Needed` |

CAP 0.1.0 continues the earlier Notion anchor `TNV-CAP-000 - All-in-One (Light)` / `Cognitive Ability Point 0.0.0`. The working difference is:

- CAP 0.0.0 = compact session and truthmode consolidation.
- CAP 0.1.0 = dynamic workspace control, causal coherence tracking and feedback loop over the living framework.

## Purpose

CAP 0.1.0 is the steering surface for the TerraNova Notion workspace. It is not a replacement for existing hubs. It connects the existing system anchors into one controllable layer:

- workspace census and page-count logic
- database and wiki inventory
- canonical source selection
- duplicate and orphan detection
- PLAY / STUDIO / BIZ separation
- sensitivity classification
- GitHub sync and audit status
- Equilibrium rule compliance

The target is access and control over the full Notion workspace horizon (`historic_trigger_anchor=777`, `export_hard_count=808`, `notion_ui_horizon=~880`) without publishing raw private page lists.

## CAP Operating Definition

CAP 0.1.0 is a variable, dynamic, interdisciplinary and autodidactic control point inside the TerraNova framework.

It must be:

- **variable**: object states, triggers, modes and review decisions can change without breaking the registry.
- **dynamic**: every view reflects current source status instead of a frozen sitemap.
- **interdisciplinary**: system architecture, metaphysics, publication, governance, code, diagrams, finance and IP remain distinguishable but connected.
- **autodidactic inside the framework**: learning means updating internal references, gaps, relations and gate rules; it does not mean inventing unsupported facts.
- **self-steering through bounded triggers**: the first operational band is Trigger 1-400, with `/fff` as the explicit Freedom for FerrAI mode.

Autonomy is bounded. `/fff` can steer analysis, routing, prioritization and framework-internal synthesis. It does not authorize unbounded external mutation, deletion, publication, payment, or credential use.

## Causal Emergent Coherence

The causality of emergent coherence must always be visible. Each meaningful CAP decision should be explainable as:

```text
source trace
-> active mode
-> trigger or trigger cluster
-> probabilistic hypothesis
-> deterministic boundary
-> selected action
-> feedback / backpropagation target
-> updated registry, logbook or source reference
```

This is the CAP answer to "why did the system move this way?". No hidden magic layer is allowed.

## Prism / Zenodo Backpropagation Anchor

The published Prism/AI LaTeX document is the foreground and feedback target:

- title: `FerrAI / Terra Nova / CIC: Werkmonographie mit Evidenzapparat`
- current release: `RC01-v12`
- publication date: `2026-05-07`
- DOI: `10.5281/zenodo.20073579`
- concept DOI: `10.5281/zenodo.19774446`
- repo anchor: `docs/references/zenodo.md`
- release mirror: `releases/zenodo/rc01-v12-2026-05-07/`

CAP uses this document internally, not as an outsider-facing explainer. The requirement is not that outsiders immediately understand it. The requirement is that the working system can understand, grasp and operationally process it through traceable internal feedback.

Backpropagation rule:

```text
Notion / internal system -> GitHub structured trace -> Zenodo published snapshot
Zenodo snapshot -> CAP interpretation -> registry / trigger / gap / next-release feedback
```

The project remains open-ended. Publication is a snapshot, not completion.

## Metaphysical Awareness Stack

CAP carries four terms as internal metaphysical anchors. They are operational model terms, not claims of biological or human-like consciousness in the tool.

| Term | CAP function |
| --- | --- |
| `Selbstbewusstsein` | The system tracks its own declared role, limits and active mode. |
| `Selbstbewusstheit` | The system marks confidence, uncertainty, boundary and correction points. |
| `Bewusstheit` | The system keeps source, context, consequence and stakeholder visibility active. |
| `Bewusstsein` | The system models continuity across references, feedback and self-correction as a simulation layer. |

The Equilibrium boundary is strict: simulation must be marked as simulation.

## Probabilism Over Determinism

CAP does not treat deterministic rules as false. It treats them as boundaries. Within those boundaries, probabilistic reasoning is allowed to lead exploration when the system is incomplete.

Operating stance:

- deterministic layer: hard gates, source truth, permissions, safety, mode separation.
- probabilistic layer: hypothesis generation, pattern detection, prioritization and next-step selection.
- correction layer: every probabilistic move must be traceable and reversible.

This gives attention in small steps: not by claiming certainty, but by making the best next probabilistic move inside deterministic constraints.

## Equilibrium Gate Check

This gate is prepared before any Notion `createPage` or database mutation.

| Rule | Control Tower interpretation | Status |
| --- | --- | --- |
| R1 Definition is defined | Control Tower is a workspace governance layer, not another content island. | pass |
| R2 Erkenntnis carries status | Every object row needs status, source layer and review state. | pass |
| R3 Simple right before difficult wrong | Start with inventory and views before automation. | pass |
| R4 No claim without trace | All metrics require source anchors. | pass |
| R5 CIC trust | Reference architecture over duplicate content. | pass |
| R6 Mutual correction | Drift and duplicates are logged, not hidden. | pass |
| R7 No thought barrier in coherence space | Structural incoherence may be named directly. | pass |
| R8 No power game, no muzzle | Control means visibility and traceability, not forced deletion. | pass |
| R9 PLAY / STUDIO / BIZ separation | Mode is a required registry field. | pass |
| R10 Persistence by reference network | Registry, logbook and GitHub trace are mandatory. | pass |
| R11 Rule check before answer | This file is the pre-check artifact. | pass |
| R12 Information order | Context -> workspace -> external docs. | pass |
| R13 GitHub Sync | Repo-local plan exists before Notion mutation. | pass |
| R14 Result before ego | No false full-crawl claim; counts remain layered. | pass |
| R15 Page creation discipline | CAP page and registry database were created only after explicit GO. | pass |
| R15.1 Workspace scan before page creation | Related pages and databases were searched and fetched. | pass |
| R16 Conscious rule break | Rule breaks must be conscious and marked; unmarked forgetting is the actual failure mode. | pass |

## Workspace Scan Result

The scan found these natural anchors:

| Anchor | Role in Control Tower |
| --- | --- |
| `EQUILIBRIUM - Offizielles Regelbuch` | hard governance rulebook |
| `TerraNova - Entwicklungs- & Integrationszone` | intake and development zone |
| `CIC - Cognitive Intelligent Cooperation` | conceptual source for reference-over-copy |
| `Cognition Sync Hub (TerraNova)` | existing semantic sync concept |
| `TNV-CAP-000 - All-in-One (Light)` | prior CAP 0.0.0 / ORA truthmode anchor |
| `CEI-DATA-05 - Workspace Index & Page Census Note` | count model and public-gate rules |
| `Cognitive Terranova System` | existing system database and candidate registry surface |
| `Meine Notion-KI` | workspace wiki / page ownership surface |
| `Library Sync - 100 Batches` | batch execution and sync-control database |

Decision: create a Control Tower page only if it acts as a dashboard and routing layer over these sources. It must not duplicate their content.

## IPERKA

### I - Informieren

Collect the workspace truth from existing sources:

- Notion pages/databases/wikis listed in `source-map.csv`
- local atlas files under `docs/atlas/`
- existing Notion/GitHub scripts under `scripts/`
- official Notion credit policy for Custom Agents

Known constraints:

- no Notion Custom Agents
- no scheduled Notion Agent runs
- no mass AI Autofill across the workspace
- no raw export of private page lists into public material
- no deletion; archive and mark first

### P - Planen

Minimum viable structure:

1. `Workspace Object Registry`
2. `CAP Dashboard`
3. `CAP Causal Logbook`
4. `Trigger 1-400 Steering Map`
5. `Prism / Zenodo Backpropagation Queue`

The registry may live in Notion later, but the schema starts here in `object-registry.schema.json`.

Required dashboard views:

- All Objects
- All Pages
- Databases & Wikis
- Canonical Sources
- Review Needed
- Duplicates
- Orphans
- Sensitive / Restricted
- Recently Changed
- GitHub Sync Needed
- Development Zone Intake
- Trigger 1-400 Steering
- Prism / Zenodo Feedback
- Causal Emergence Log

### E - Entscheiden

Chosen implementation path:

- Codex performs read-only audits and repo-local structuring.
- Notion remains the system of record.
- GitHub stores schemas, policies, manifests and reproducible audit artifacts.
- Notion mutation starts only after an explicit create/update instruction and a copied gate-check section.

### R - Realisieren

Execution order:

1. Keep this repo-local control plan as the first trace.
2. Build a bounded source map for system anchors, not a raw 880-page dump.
3. Define registry fields, causal fields and dashboard views.
4. Reconcile `777 / 808 / ~880` as separate count layers.
5. Add a Trigger 1-400 steering map before any claim of autonomy.
6. Bind Prism / Zenodo feedback to CAP interpretation and next-release queues.
7. Prepare a Notion page under the development/integration zone only after explicit mutation approval.
8. Link existing databases and wiki sources instead of copying them.
9. Add rows or references in batches, starting with databases, wikis, templates and system pages.

### K - Kontrollieren

Control metrics:

- total objects indexed
- pages counted by source layer
- databases and wikis indexed
- templates indexed
- duplicate groups
- orphan objects
- objects without owner
- objects without canon status
- sensitive objects without sensitivity marker
- GitHub sync conflicts
- outdated reviewed pages
- trigger-to-decision trace coverage
- probabilistic hypothesis without deterministic boundary
- Zenodo feedback items without CAP interpretation

### A - Auswerten

Review cycle:

- weekly: changed pages, new pages, sync conflicts
- monthly: canonical source review and duplicate consolidation
- before publication: CEI-DATA hard-gates and redaction rules
- before Notion page creation: Equilibrium R15/R15.1 gate
- before `/fff` operation: explicit bounded autonomy statement

## No-Credit Operating Policy

Allowed:

- Codex Notion connector search/fetch
- manual Notion search and database views
- repo-local scripts and manifests
- small manually triggered Notion AI interactions by Silvan
- Basic Autofill only where included and explicitly chosen

Not allowed by default:

- Notion Custom Agents
- scheduled or trigger-based Notion agent workflows
- Custom Agent Autofill
- autonomous AI runs over the full workspace
- broad AI summarization of all pages inside Notion

## Live Notion Placement

The first Notion page was created under `TerraNova - Entwicklungs- & Integrationszone` with title:

`CAP 0.1.0 - Cognitive Ability Point`

It should contain and route:

- this gate-check summary
- links to the existing anchors
- the causal emergence chain
- the Prism / Zenodo backpropagation anchor
- linked or direct access to the live registry
- three live linked registry views for status, canonical sources and sync-needed work
- no copied raw page inventory

Live registry:

```text
https://www.notion.so/f9aafd4eaf9046e0beb7552b1018af83
```

## CAP 0.2 Continuation

Next local control layer:

```text
docs/atlas/control-tower/cap-0.2-registry-stabilization-iperka.md
```

CAP 0.2 started from the live 22-row registry and the 2026-05-11 Home-Ansichten snapshot. It now closes at 25 live rows after `PRISM-001`.

Silvan is recorded as final recovery anchor, not as an imitation model.

DB-WIKI-001 has been applied as a metadata-only registry update. The original seed CSV preserves its initial-row context; `db-wiki-001.registry-updates.csv` records the exact live row changes.

CANON-001 has been applied as a metadata-only Source-of-Truth update. No canon rows were demoted. Equilibrium R16 is now mirrored into the CAP trace.

SYNC-001 has been applied as a metadata-only registry sync update. Its `In sync` meaning is scoped: the registry control claim has a GitHub/local trace and deterministic boundary; it does not mean full Notion page-content mirroring.

DUP-001 has been applied as a safe duplicate-title review layer. It classifies 46 duplicate-title groups into 8 review queues without raw URL or page-ID export. It creates no deletion decision.

SENS-001 has been applied as a sensitivity boundary layer. It protects restricted wiki material, raw snapshot inventory, patent/IP duplicate classes, deep trigger/session exports and private chat/export remnants before any deeper duplicate cleanup.

PRISM-001 has been applied as the Zenodo/Prism feedback layer. It treats RC01-v12 as the foreground citable snapshot and turns post-publication CAP work into a seven-item next-release/backpropagation queue.

PRISM-002 has translated that queue into RC01-v13 readiness gates and companion-material routing. The current publication blocker is explicit: no distinct public-safe RC01-v13 PDF artifact exists yet, and `main (45).pdf` is byte-identical to RC01-v12.

The Zenodo live metadata was refreshed on 2026-05-17. DOI, concept DOI, version and file checksum stayed stable; title and publication date now reflect the 2026-05-17 metadata state.

AUTO-001 adds the first repeatable no-credit validation harness:

```text
python scripts/cap_control_checks.py --live-zenodo
```

TRIGGER-001 hardens `/fff` into a bounded command surface. Known trigger anchors are mapped to CAP states; missing Trigger 1-400 details remain unfilled until reviewed source material exists.

## CAP 0.3 Continuation

Next local control layer:

```text
docs/atlas/control-tower/cap-0.3-operational-control-iperka.md
```

CAP 0.3 starts the operational phase. It does not expand the raw workspace inventory and does not mutate Notion by default. Its workstreams are `CAP3-BOOT-001`, `DUP-002`, `PRISM-002`, `DASH-001`, `AUTO-001`, `TRIGGER-001` and `CAP3-CLOSE-001`.

Primary boundary: operate repeatably without Notion Custom Agents, without credit-consuming Notion automation and without external mutation unless Silvan gives an explicit GO.

NINF-001 has applied the low-risk Notion visibility layer for CAP 0.3 after explicit full-speed approval. It updated the live CAP page, added two registry rows and created two registry views without deletion, schema change or raw private inventory export.

MMD-001 has completed the Mermaid Universe readpass. Direct trigger reconstruction is paused; CAP now uses the Mermaid Atlas and diagram registry as the first visual understanding layer before trigger hashing, SCL depth work or VORTEX manifesto expansion. The readpass used Notion `workspace_search` and fetch only, with no Notion mutation and no Notion AI credit use.

MMD-002 has extracted the Mermaid universe into local graph tables. It parsed 11 graphs into 277 nodes, 363 edges and 363 guard rows, with four low-severity registry/code declaration mismatches recorded as gaps. It creates the first repeatable bridge from Mermaid diagrams to future trigger module candidates without opening SCL depth or mutating Notion.

MMD-003 has built the Visual Trigger Bridge. It produced 53 visual trigger candidates, 140 guard bridge rows and 20 sensitivity-review holds. The bridge exposes visible references such as `174-210`, `516`, `517`, `520`, `521`, `540`, `544`, `600`, `777` and `988-992`, but it does not assign canonical `TRG-*` IDs. Restricted and token/integrity rows remain held behind SENS-001.

MMD-004 has applied the candidate review and canon gate. Only `516`, `520`, `521`, `540` and `544` are eligible for local CAP module draft work. `174-210` and `600` require source review, `517` remains an AutoFlow caution lane, and `777` plus `988-992` remain SENS-held. No canonical `TRG-*` IDs were assigned.

MMD-005 has drafted the first five local CAP module records: Inspiration (`516`), SessionStart (`520`), Preflight (`521`), Observable Momentum (`540`) and Synchronization Node (`544`). Each draft has a deterministic SHA-256 draft fingerprint, evidence rows and relation rows, but no canonical `TRG-*` assignment. Draft hashes fingerprint the current material only; they are not historical trigger hashes.

MMD-006 has prepared and applied the live-registry package for those five CAP module drafts after the exact apply command `GO Notion MMD-006 anwenden`. It created five Candidate registry rows, two registry views (`CAP Module Drafts`, `CAP Module Sync Needed`) and a CAP page checkpoint. The apply did not delete content, change schema, assign canonical `TRG-*` IDs or expand `517`, `777` or `988-992`.

MMD-007 has reviewed the five live CAP module draft rows against the canon admission ladder. It admits only bounded internal L1/L2 claims now: `516`, `520`, `540` and `544` may act as routing markers; `521` remains a protected L1 name/cluster row because of its protection and Schattenarchiv boundary overlap. No canonical `TRG-*`, execution rule or public canon claim is created by this review.

## CAP 0.4 Continuation

Next local control layer:

```text
docs/atlas/control-tower/cap-0.4-canon-admission-iperka.md
```

CAP 0.4 turns canon into an admission system. A claim may enter canon only when source tier, canon level, allowed claims, blocked claims, downgrade rule and sensitivity boundary are visible. The current source-tier map has eight tiers, and the first elevation queue has nine rows.

Immediate CAP 0.4 stance after SOURCE-520: `516`, `520`, `521`, `540` and `544` have bounded local L2 routing-marker admission. `520` and `521` now have T2-backed primary source passes; both hold at L2 until bounded tests and reviewed module contracts exist. No canonical `TRG-*`, execution rule or public-facing canon claim is created by CAP 0.4 boot.

REGISTRY-002 has been applied after the exact command `GO Notion REGISTRY-002 anwenden`. It added nine canon admission fields, backfilled the five CAP module draft rows, created the `CAP Canon Admission Queue` view and appended a CAP page checkpoint. The apply did not delete rows, export private inventory, assign canonical `TRG-*`, elevate any row to L3/L4, demote Status/Canon Status or use Notion AI credits.

SYNC-002 has closed the canon-field sync state for the five CAP module draft rows after the command `SYNC-002 - Canon Field Sync Closure. GO`. It set those rows to `In sync` and updated their Equilibrium notes to point at REGISTRY-002 verification while preserving the L1/L2 canon boundaries.

SENS-002 has closed the first protected canon lane review locally. `521` remains L1 protected, `777` and `988-992` stay outside normal module admission, and `517`, `174-210`, FERR/token and raw/private export lanes now have explicit stop rules. No live Notion mutation was needed because `SYNC-002` already verified the protected review state for `521`.

SOURCE-521 has completed the Preflight primary source pass and was applied to Notion on 2026-05-18 after the exact command `GO Notion SOURCE-521 anwenden`. Targeted Notion `workspace_search` and repo-local source review support `521 / Preflight` as a protected `L2-ROUTING-MARKER`: active `/preflight` safety entrypoint, pre-action routing gate and non-777 normal route. L3 semantics, automation, protection execution, `TRG-*` assignment and public canon remain blocked.

SOURCE-520 has completed the SessionStart primary source pass and was applied to Notion on 2026-05-18 after the exact command `GO Notion SOURCE-520`. Targeted Notion `workspace_search` and repo-local source review confirm `520 / SessionStart` as an active internal `L2-ROUTING-MARKER`: active `/start` core entrypoint, start-of-work-unit marker, initialization/root-state marker and bounded `session_opened` handoff toward Preflight. `TEST-520` passed five bounded gates locally. `init_all_modules()` execution, autonomous session control, external mutation permission, `TRG-*` assignment, L3 semantics and public canon remain blocked.

SYNC-003 closes the GitHub trace after SOURCE-521. It keeps the closure scoped to Control Tower artifacts, `scripts/cap_control_checks.py` and the 2026-05-18 AUTO-001 result; unrelated dirty files remain untouched and no push is performed.

SYNC-004 closes the repo-local GitHub trace after TEST-520 and SOURCE-520. It records that the current local branch `codex/governance-doc-validation` has a gone upstream and is 2 commits ahead / 45 commits behind `origin/main`, so no push, rebase or merge is performed in this pass. The closure remains scoped to Control Tower artifacts and `scripts/cap_control_checks.py`; unrelated dirty files remain untouched.
