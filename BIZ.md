# TerraNova `/biz` Brief

Status: BIZ / Business Brief
Source: GitHub technical mirror for the Notion-driven operations workflow.
Trace: `scripts/notion_to_github.py`, `NOTION_PROPERTIES.md`, `.github/workflows/tnv_notion_to_github.yml`
Boundary: Business-facing summary only; not a living rulebook or source-of-record replacement.
Mode: BIZ
GitHub sync state: tracked in this repository.
Notion source awareness: required for operational database schema or rule changes.

## Business purpose
TerraNova automates a controlled handoff from a Notion operations database into GitHub Issues.
This supports auditability, clearer ownership, and consistent incident/change tracking without
manual copy/paste.

## Core workflow (business view)
1. A team member flags a Notion row via `Export_to_GitHub`.
2. The controller creates a GitHub Issue in the configured repository.
3. The issue URL and export timestamp are written back to Notion.

## Value delivered
- **Faster triage:** Operations items appear where engineering already works (GitHub Issues).
- **Governance by default:** Only explicitly flagged rows are exported.
- **Traceability:** Bidirectional linkage (`GitHub_Issue_URL`) for audits and postmortems.
- **Low operational overhead:** Runs from GitHub Actions on a schedule.

## Required operating inputs
- Notion integration token and database id.
- Automatic GitHub Actions `GITHUB_TOKEN` for the same-repository sync; the job retains `contents: write` and `issues: write`.
- Target repository `owner/repo`, defaulting to the workflow repository.
- Stable Notion property schema documented in `NOTION_PROPERTIES.md`.

## Suggested KPIs
- Export throughput: number of exported rows/week.
- Time-to-triage: median duration from Notion creation to first GitHub assignee/comment.
- Backlog hygiene: percentage of exported issues triaged or closed within SLA.
- Data quality: export failures due to missing/invalid Notion properties.

## Risk and controls
- **Risk:** Schema drift in Notion property names.
  - **Control:** Keep mapping centralized in `scripts/notion_to_github.py` and review on schema changes.
- **Risk:** Notion credential misconfiguration or expiration.
  - **Control:** Store Notion credentials in GitHub repository secrets and rotate them when needed.
- **Risk:** GitHub Actions permissions drift.
  - **Control:** Keep the TNV workflow job permissions at `contents: write` and `issues: write`.
- **Risk:** Over-exporting noisy items.
  - **Control:** Explicit checkbox gate (`Export_to_GitHub`) and optional severity-based triage policy.

## `/biz` operating cadence
- Weekly: review KPI dashboard and stale exported GitHub Issues.
- Monthly: verify Notion property compatibility, Notion credential health, and Actions workflow permissions.
- Quarterly: review governance fields and escalation rules for incident severity.
