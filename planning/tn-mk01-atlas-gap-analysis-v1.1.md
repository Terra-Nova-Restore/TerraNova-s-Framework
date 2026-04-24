# TN-MK01 -> Atlas Gap Analysis (v1.1)

## Purpose

This is a read-only planning artifact for GitHub Issue #5,
`TN-MK01: Repo Extract (Kernel) + Palandirer Routing`.

It compares the Notion source page against the current repo, especially
`atlas/atlas.manifest.v1.1.json`, and separates repo-safe work from canon-only
or ambiguous material. It does not implement any TN-MK01 content.

## Sources Checked

- Notion source page: `TN-MK01: Repo Extract (Kernel) + Palandirer Routing`
  (`19e75cd1-ceed-47c2-9d1d-3ea89cdf4cb6`), fetched read-only.
- GitHub Issue #5 generated from that Notion page.
- `atlas/atlas.manifest.v1.1.json`
- `atlas/sources/trigger-complement-2026-03-30.md`
- `atlas/sources/workspace-export-2026-03-27.md`
- Current sync docs and implementation:
  `README.md`, `SETUP_RUNBOOK.md`, `BIZ.md`,
  `.github/workflows/tnv_notion_to_github.yml`,
  `scripts/notion_to_github.py`, and `config/notion_map.json`.

## Already Represented In Atlas v1.1

- Trigger architecture exists as a five-layer model with core, Schattenarchiv,
  Codex, meta-emergent, and active-live layers.
- Trigger 517, 520, 521, and 777 exist as single-trigger anchors.
- Trigger clusters exist for:
  - Core system 520-530
  - Creative flow 516-517
  - Protection layer 182 / 521 / 777
  - Schattenarchiv 777
- CAP-II is represented through contract/page objects and token/blockchain
  relations.
- Schattenarchiv is represented as a framework, page hub, trigger layer, and
  trigger cluster.
- Notion-to-GitHub sync is represented as the production integration path; the
  current script creates GitHub Issues and writes the Issue URL plus export date
  back to Notion.

## Repo-Safe But Missing

- TN-MK01 folder contract:
  `docs/TN-MK01/` with a short kernel extract overview and explicit repo policy.
- Templates:
  - `docs/TN-MK01/templates/schattenarchiv_3lines.md`
  - `docs/TN-MK01/templates/manifest_example.json`
- CNC/NC to Python mapping documentation as a repo-safe abstraction, with no
  private machine, credential, or operationally sensitive details.
- Versioning standard for TrueMode, limited to documentation and naming rules.
- Defensive security briefing, limited to safe operating principles and review
  gates.
- Lockchain-defence simulation, only if framed as defensive validation and
  without attack instructions.
- Model-routing policy and Palandirer guard documentation, if limited to
  high-level SIM/PROD separation and CI gate intent.
- `ops/notion_github_sync.md` or equivalent operational overview if the current
  README/runbook is not considered sufficient for TN-MK01.

## Canon-Only / Not Suitable For Public Repo

- Private contact data, personal identifiers, tokens, credentials, and secrets.
- Intimate Schattenarchiv full texts or consent-sensitive raw logs.
- Explicit attack instructions or offensive security procedures.
- Any private prompt, routing, or model-control material that would expose
  sensitive operating behavior rather than a high-level safety contract.
- Any raw Notion export content that has not been curated into repo-safe form.

## Ambiguous And Needs Silvan Confirmation

- Trigger 179 and 519 are named in the TN-MK01 kernel list but are not present as
  single-trigger anchors in Atlas v1.1. Their labels, layer assignment, and
  repo-safe summaries need source confirmation before adding them.
- Palandirer guard scope needs a decision: documentation-only policy, CI lint
  rule, or actual workflow gate. The Notion source says CI gate, but no current
  repo implementation exists.
- GPT-5 SIM / GPT-4 PROD policy should be confirmed before publication because
  model naming and operational routing can drift.
- SMT command mappings and shortcuts need exact source material and a
  repo-safety pass before inclusion.
- CNC/NC mapping needs boundary confirmation: conceptual mapping only versus
  executable examples.
- Lockchain-defence simulation needs a safety boundary: defensive tabletop
  simulation only versus any executable or adversarial procedure.
- The ASCII poster says the GitHub workflow writes docs/policies, but the
  current workflow only runs the Notion-to-Issue sync and commits shadow state.
  Treat that as intended TN-MK01 folder layout, not current behavior, unless
  Silvan confirms otherwise.

## Recommended Next Authorization Boundary

The next task should not implement all gaps at once. It should choose one of
these explicitly:

1. Documentation-only TN-MK01 scaffold under `docs/TN-MK01/`, `policies/`, and
   `ops/`.
2. Atlas v1.2 extension for missing trigger anchors and TN-MK01 relations.
3. Palandirer CI gate design only, without implementation.
4. Palandirer CI gate implementation, after the design is approved.

Until that authorization exists, this file remains the persistent gap record and
no TN-MK01 gap content should be added.
