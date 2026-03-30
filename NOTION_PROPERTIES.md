# Notion Properties Needed (AI_Incidents_and_Changes)

This controller expects these properties in the **Changes** database:

## Required Environment Variables

Before running sync, ensure these are configured:

```bash
NOTION_TOKEN=ntn_xxxx...                # Notion Integration API key
NOTION_DATABASE_ID_CHANGES=abc123...    # Database ID to sync from
GH_PAT=ghp_xxxx...                      # GitHub Personal Access Token
TARGET_GITHUB_REPO=owner/repo           # Optional cross-repo override (highest priority)
GITHUB_REPO=owner/repo                  # Optional fallback target repository
```

**See `.env.example` for template and detailed documentation.**
**Note:** In workflow runs, `GITHUB_REPO` defaults to `${{ github.repository }}`.

## Required Notion Properties

These properties must exist in the **Changes** database:

- `Export_to_GitHub` (Checkbox) — mark rows to export
- `GitHub_Issue_URL` (URL) — will be filled after export
- `Exported_At` (Date) — will be filled after export

## Recommended Properties (for rich issue bodies)

To create more detailed GitHub issues, add these optional properties:

- `Change_ID` (Rich text) – Issue title
- `Change_Type` (Select) – Issue label
- `Beschreibung` (Rich text) – Issue body content
- `Incident_Flag` (Checkbox) – Priority indicator
- `Incident_Severity` (Select) – Severity label
- `Evidence_URL` (URL) – Reference link
- `Evidence_SHA256` (Rich text) – Integrity hash
- `Evidence_CID` (Rich text) – Content ID
- `Wesentliche_Aenderung` (Select) – Change category
- `Human_Oversight` (Checkbox) – Review required

## Configuration

If your property names differ, edit:
- `scripts/notion_to_github.py` – API client and filters
- `config/notion_map.json` – Property mappings and defaults

## Secret Management

Never commit `.env` with real credentials. Use:
- `.env` for local development
- `.env.example` as template
- GitHub encrypted secrets for CI/CD pipelines

See `scripts/PREFLIGHT_README.md` for troubleshooting and detailed diagnostics.
