# TerraNova Notion -> GitHub Controller (Minimal)

## What it does
- Polls a Notion database (`AI_Incidents_and_Changes`)
- For rows where `Export_to_GitHub` is ✅ and `GitHub_Issue_URL` is empty:
  - Creates a GitHub Issue
  - Writes the Issue URL + timestamp back to Notion

## Repo layers
- `Notion -> GitHub sync`: the existing production path for `AI_Incidents_and_Changes`.
- `Atlas layer`: a canonical workspace-atlas seed in [`atlas/README.md`](atlas/README.md) and [`atlas/atlas.manifest.v1.json`](atlas/atlas.manifest.v1.json).

The atlas does not change the production sync workflow. It is a separate, machine-readable workspace inventory seeded from a user-provided TerraNova workspace export so future exporters or visualizers have a stable contract to build on.

## Setup (GitHub Actions – RECOMMENDED)

**See [SETUP_RUNBOOK.md](SETUP_RUNBOOK.md) for complete step-by-step guide.**

**TL;DR:**
1. Create GitHub repo secrets:
   - `NOTION_TOKEN` (Notion integration token)
   - `NOTION_DATABASE_ID_CHANGES` (Notion database ID)
   - `GH_PAT` (GitHub Personal Access Token with `repo` + `issues` scopes)
2. Share Notion database with integration (in Notion UI)
3. Workflow runs automatically every 10 minutes

The workflow resolves `GITHUB_REPO` automatically from `${{ github.repository }}`.
Optional override for cross-repo sync: set `TARGET_GITHUB_REPO` (secret or variable) to `owner/repo`.

**Trigger manually:**
```bash
gh workflow run tnv_notion_to_github.yml --repo owner/repo
```

## Safety defaults
- The script only exports rows you explicitly mark (`Export_to_GitHub`).
- No automatic mutation of compliance risk fields.
- Tokens are never stored in Notion or in the repo – only GitHub encrypted secrets.

## Local run (not recommended – use workflow instead)
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

## GitHub Projects v2
The controller does not mutate GitHub Projects v2. It creates Issues and writes
the Issue URL back to Notion. Add exported Issues to a project manually or with
a separate automation if project backlog state is required.

## Business brief
- See `BIZ.md` for a concise `/biz` business-facing overview, KPI suggestions, and operating cadence.

## Atlas validation
Validate the atlas manifest from the repo root:

```bash
python scripts/validate_atlas.py atlas/atlas.manifest.v1.json
```
