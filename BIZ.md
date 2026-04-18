# TerraNova `/biz` Brief

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
- GitHub token and target `owner/repo`.
- Stable Notion property schema documented in `NOTION_PROPERTIES.md`.

## Suggested KPIs
- Export throughput: number of exported rows/week.
- Time-to-triage: median duration from Notion creation to first GitHub assignee/comment.
- Backlog hygiene: percentage of exported issues triaged or closed within SLA.
- Data quality: export failures due to missing/invalid Notion properties.

## Risk and controls
- **Risk:** Schema drift in Notion property names.
  - **Control:** Keep mapping centralized in `scripts/notion_to_github.py` and review on schema changes.
- **Risk:** Token misconfiguration or expiration.
  - **Control:** Secrets managed in GitHub repository settings with periodic rotation.
- **Risk:** Over-exporting noisy items.
  - **Control:** Explicit checkbox gate (`Export_to_GitHub`) and optional severity-based triage policy.

## `/biz` operating cadence
- Weekly: review KPI dashboard and stale exported GitHub Issues.
- Monthly: verify Notion property compatibility and secret health.
- Quarterly: review governance fields and escalation rules for incident severity.
