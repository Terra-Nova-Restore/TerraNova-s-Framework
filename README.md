# TerraNova Notion -> GitHub Controller (Minimal)

## What it does
- Polls a Notion database (`AI_Incidents_and_Changes`)
- For rows where `Export_to_GitHub` is ✅ and `GitHub_Issue_URL` is empty:
  - Creates a GitHub Issue
  - Writes the Issue URL + timestamp back to Notion

## Setup (GitHub Actions)
1) Copy this folder into your GitHub repo (or merge the contents).
2) Create these GitHub repo secrets:
   - `NOTION_TOKEN`                     (Notion integration token)
   - `NOTION_DATABASE_ID_CHANGES`       (DB id for AI_Incidents_and_Changes)
   - `GITHUB_TOKEN_TNV`                 (fine-grained PAT or GitHub App token)
   - `GITHUB_REPO`                      ("owner/repo")
3) Ensure the Notion DB has required properties (see `NOTION_PROPERTIES.md`).
4) Run the workflow manually once, then let the schedule run.

## Safety defaults
- The script only exports rows you explicitly mark (`Export_to_GitHub`).
- No automatic mutation of compliance risk fields.
- Tokens are never stored in Notion or in the repo.

## Local run
```bash
export NOTION_TOKEN="..."
export NOTION_DATABASE_ID_CHANGES="..."
export GITHUB_TOKEN="..."
export GITHUB_REPO="owner/repo"
python scripts/notion_to_github.py
```


## GitHub Project (Projects v2) – optional
- Add repo secret `PROJECTV2_ID` (ProjectV2 node id, e.g. `PVT_...`).
- Exported issues will be added to the project and set `Status=Todo`.
