# TerraNova Notion -> GitHub Controller (Minimal)

## What it does
- Polls a Notion database (`AI_Incidents_and_Changes`)
- For rows where `Export_to_GitHub` is ✅ and `GitHub_Issue_URL` is empty:
  - Creates a GitHub Issue
  - Writes the Issue URL + timestamp back to Notion

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
export GITHUB_REPO="owner/repo"
python scripts/notion_to_github.py
```


## GitHub Project (Projects v2) – optional
- Add repo secret `PROJECTV2_ID` (ProjectV2 node id, e.g. `PVT_...`).
- Exported issues will be added to the project and set `Status=Todo`.

## Business brief
- See `BIZ.md` for a concise `/biz` business-facing overview, KPI suggestions, and operating cadence.
