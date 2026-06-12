# TerraNova / FerrAI CIC

A human–AI **research-operations framework** for moving work from private notes,
signals and conversations into reviewed, versioned, public-safe artifacts.

> **This repository is not the whole system.**
> It is the *public-safe, versioned evidence and release surface* of
> TerraNova / FerrAI CIC — not the live working core.

## What it is

An auditable framework for human–AI cooperation (Cognitive Intelligent
Cooperation, "CIC"): every step moves from a living source-of-record into
reviewed, citable, public-safe output.

## What problem it solves

Most AI-assisted work leaves no clean trail. TerraNova separates **where work
lives**, **where it is reviewed**, and **where it is citable** — so progress
stays traceable instead of disappearing into chat logs.

## Architecture

| Layer | Role |
|-------|------|
| **Notion** | Living source-of-record (working core) |
| **GitHub** (this repo) | Public-safe working & audit mirror / release surface |
| **Zenodo** | Citable long-form archive — DOI 10.5281/zenodo.20073579 |

## Public-safe boundaries

- Draft PRs are used **intentionally** as review gates — not signs of an unfinished mess.
- Files under `raw/exports/` are sanitized placeholders / fill-versions, not live data dumps. Other export-related directories require separate review before being described publicly.
- Internal terms (Prism, Trigger Registry, Equilibrium) are legacy/internal vocabulary; see the governance docs before reading them as products.

## Current status

**Advanced prototype / active research workbench — not a finished SaaS product.**
Strong governance and technical substrate; public onboarding is being hardened.

## Where to start

1. Read this README (you are here).
2. [`docs/public/README.md`](docs/public/README.md) — public artifacts index & lexicon.
3. Zenodo record — citable reference, *not* the entry point.

---

## Notion → GitHub Controller (minimal sync)

### What it does
- Polls a Notion database (`AI_Incidents_and_Changes`)
- For rows where `Export_to_GitHub` is ✅ and `GitHub_Issue_URL` is empty:
  - Creates a GitHub Issue
  - Writes the Issue URL + timestamp back to Notion

### Repo layers
- `Notion -> GitHub sync`: the existing production path for `AI_Incidents_and_Changes`.
- `Atlas layer`: a canonical workspace-atlas seed in [`atlas/README.md`](atlas/README.md) and [`atlas/atlas.manifest.v1.json`](atlas/atlas.manifest.v1.json).
- `Prism atlas layer`: reviewed local docs generated from Prism/Notion exports in [`docs/atlas/README.md`](docs/atlas/README.md), with trigger gaps tracked in [`docs/triggers/gap_ledger.md`](docs/triggers/gap_ledger.md).

The atlas does not change the production sync workflow. It is a separate, machine-readable workspace inventory seeded from a user-provided TerraNova workspace export so future exporters or visualizers have a stable contract to build on.

### Setup (GitHub Actions – RECOMMENDED)

**See [SETUP_RUNBOOK.md](SETUP_RUNBOOK.md) for complete step-by-step guide.**

**TL;DR:**
1. Create GitHub repo secrets:
   - `NOTION_TOKEN` (Notion integration token)
   - `NOTION_DATABASE_ID_CHANGES` (Notion database ID)
   - `GH_PAT` (GitHub Personal Access Token with `repo` + `issues` scopes)
2. Share Notion database with integration (in Notion UI)
3. Workflow runs automatically every 10 minutes

The workflow resolves `GITHUB_REPO` automatically from the GitHub Actions `github.repository` context expression.
Optional override for cross-repo sync: set `TARGET_GITHUB_REPO` (secret or variable) to `owner/repo`.

**Trigger manually:**
```bash
gh workflow run tnv_notion_to_github.yml --repo owner/repo
```

### Safety defaults
- The script only exports rows you explicitly mark (`Export_to_GitHub`).
- No automatic mutation of compliance risk fields.
- Tokens are never stored in Notion or in the repo – only GitHub encrypted secrets.

### Local run (not recommended – use workflow instead)
```bash
export NOTION_TOKEN="..."
export NOTION_DATABASE_ID_CHANGES="..."
export GH_PAT="..."
# Optional: override target repo (cross-repo)
export TARGET_GITHUB_REPO="owner/other-repo"
# Optional fallback if TARGET_GITHUB_REPO is not set
export GITHUB_REPO="owner/repo"
python scripts/notion_to_github.py
```

### GitHub Projects v2
The controller does not mutate GitHub Projects v2. It creates Issues and writes
the Issue URL back to Notion. Add exported Issues to a project manually or with
a separate automation if project backlog state is required.

### Business brief
- See `BIZ.md` for a concise `/biz` business-facing overview, KPI suggestions, and operating cadence.

### Governance and public boundary
- Public repository boundary: [`docs/governance/public_boundary.md`](docs/governance/public_boundary.md)
- Repository role vocabulary: [`docs/governance/repo_roles.md`](docs/governance/repo_roles.md)
- Source-of-record policy: [`docs/governance/source_of_record_policy.md`](docs/governance/source_of_record_policy.md)
- Source-tier and naming policy: [`docs/governance/source_tier_and_naming_policy.md`](docs/governance/source_tier_and_naming_policy.md)
- Governance issue status registry: [`docs/governance/issue_status_registry.md`](docs/governance/issue_status_registry.md)
- Prism import manifest: [`docs/governance/prism_import_manifest.md`](docs/governance/prism_import_manifest.md)
- Track C intake checklist: [`docs/governance/track_c_intake_checklist.md`](docs/governance/track_c_intake_checklist.md)
- ChatGPT connector runtime policy: [`docs/governance/chatgpt_connector_runtime_policy.md`](docs/governance/chatgpt_connector_runtime_policy.md)
- Repository maturity note: [`docs/governance/repository_maturity.md`](docs/governance/repository_maturity.md)
- Raw export review gate: [`raw/exports/REVIEW_GATE.md`](raw/exports/REVIEW_GATE.md)

### Public semantic architecture
- Architecture index: [`docs/architecture/README.md`](docs/architecture/README.md)
- Public semantic spine: [`docs/architecture/public_semantic_architecture_spine.md`](docs/architecture/public_semantic_architecture_spine.md)
- Semantic Trigger Architecture: [`docs/architecture/semantic_trigger_architecture.md`](docs/architecture/semantic_trigger_architecture.md)
- Semantic Core Layer: [`docs/architecture/semantic_core_layer.md`](docs/architecture/semantic_core_layer.md)
- Iterative Interaction Collapse: [`docs/architecture/iterative_interaction_collapse.md`](docs/architecture/iterative_interaction_collapse.md)
- Recursive-Iterative Interaction Collapse: [`docs/architecture/recursive_iterative_interaction_collapse.md`](docs/architecture/recursive_iterative_interaction_collapse.md)
- Lenhard Decoding Module: [`docs/architecture/lenhard_decoding_module.md`](docs/architecture/lenhard_decoding_module.md)
- Lenhard Model: [`docs/architecture/lenhard_model.md`](docs/architecture/lenhard_model.md)
- Mermaid Cluster: [`docs/atlas/mermaid_cluster.md`](docs/atlas/mermaid_cluster.md)
- Semantic spine registry: [`docs/atlas/semantic_spine_registry.md`](docs/atlas/semantic_spine_registry.md)
- Public release candidate: [`docs/public/semantic_architecture_public_release_v0_1.md`](docs/public/semantic_architecture_public_release_v0_1.md)
- Public artifacts index: [`docs/public/README.md`](docs/public/README.md)
- Architecture Entry Pack v0.1: [`docs/public/entry_pack_architecture_v0_1.md`](docs/public/entry_pack_architecture_v0_1.md)

### Current published release

The current citable Zenodo release is RC01-v12:

- DOI: https://doi.org/10.5281/zenodo.20073579
- Record: https://zenodo.org/records/20073579
- GitHub mirror artifact: `releases/zenodo/rc01-v12-2026-05-07/`

### Atlas validation
Validate the atlas manifest from the repo root:

```bash
python scripts/validate_atlas.py atlas/atlas.manifest.v1.json
```

### Prism atlas renderer
Render the current Prism source pack into reviewed local docs:

```bash
python scripts/render_prism_atlas.py
```

The renderer writes `docs/atlas/` and `docs/triggers/gap_ledger.md` from the
latest dated source pack under `raw/exports/prism/source-pack/`.
