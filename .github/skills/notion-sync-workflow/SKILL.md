---
description: "Use when: setting up a new Notion-GitHub sync, automating recurring syncs, establishing sync workflow from scratch, or implementing sync for new teams"
---

# Notion-GitHub Sync Workflow

A step-by-step guided workflow to set up, validate, execute, and monitor Notion-to-GitHub synchronization with built-in safety checks and templates.

## When to Use This Skill

- **New Integration**: First time syncing a Notion database to GitHub
- **New Database**: Adding another Notion database to existing integration
- **Process Setup**: Establishing repeated/automated sync for a team
- **Troubleshooting**: Recovering from failed syncs with structured diagnostics
- **Handoff**: Documenting sync configuration for team knowledge sharing

## Workflow Stages

### Stage 1: Discovery & Planning
Understand your Notion database and GitHub target before syncing.

**Actions:**
1. Identify source Notion database (name, ID)
2. Identify target GitHub repository and issue type (issues vs PR)
3. Document current state: How many records in Notion? Expected GitHub items?
4. Review NOTION_PROPERTIES.md to understand existing mappings

**Template: `sync-plan.md`**
```markdown
## Sync Plan: [Database Name]

### Source
- Notion Database: [Name]
- Database ID: [ID]
- Record Count: [N]
- Key Fields: [list property names]

### Target
- GitHub Repo: [owner/repo]
- Sync To: [Issues / Pull Requests / Discussions]
- Expected Items: [N]

### Property Mappings
| Notion Field | Type | GitHub Field | Notes |
|---|---|---|---|
| Name | Title | Issue Title | |
| Status | Select | Labels | Map values below |
| Assignee | Person | Assignee | |

### Status Values
- Notion: [value] → GitHub: [label]
- Notion: [value] → GitHub: [label]
```

**Output:** Completed sync plan document

---

### Stage 2: Preflight Validation
Verify prerequisites before attempting sync.

**Actions:**
1. Validate API credentials exist (`NOTION_API_KEY`, `GH_PAT`/`GITHUB_TOKEN`)
2. Test Notion database access (can read at least 1 record)
3. Test GitHub repo access (can read repo details)
4. Verify property mappings in NOTION_PROPERTIES.md match actual database schema
5. Check concurrency: No other sync processes running

**Template: Preflight Checklist**
```
Preflight Validation for [Database Name]

✓ Secrets Configured
  - NOTION_API_KEY: [present/missing]
  - GH_PAT or GITHUB_TOKEN: [present/missing]

✓ Notion Database Access
  - Database ID: [ID]
  - Can read records: [yes/no]
  - Record count: [N]
  - Last error (if any): [error message]

✓ GitHub Repository Access
  - Repository: [owner/repo]
  - Can read: [yes/no]
  - Can create issues: [yes/no]
  - Last error (if any): [error message]

✓ Property Mappings
  - Mappings in NOTION_PROPERTIES.md: [N]
  - Properties in Notion DB: [N]
  - Match: [yes/no] – [list mismatches if any]

✓ Concurrency Check
  - Running sync processes: [N]
  - Safe to proceed: [yes/no]

PREFLIGHT STATUS: [PASS / FAIL – reason]
```

---

### Stage 3: Safety Dry Run
Simulate sync without committing to GitHub.

**Actions:**
1. Fetch all Notion records (don't create GitHub issues yet)
2. Validate each record against GitHub schema
3. Report what WOULD be created (counts, potential issues)
4. Identify any records that can't be synced (missing fields, type mismatches)
5. Get user approval before actual sync

**Template: Dry Run Report**
```markdown
## Dry Run Report: [Database Name]

### Summary
- Records fetched: [N]
- Valid for sync: [N]
- Issues found: [N]

### Would Create
- [N] GitHub Issues
- [N] with existing labels
- [N] with new labels
- [N] with assignees

### Issues & Warnings
- Record "[title]" missing assignee (will skip or use default: [value])
- Record "[title]" uses label "[label]" that doesn't exist in GitHub (will create)
- [Additional issues]

### Before Proceeding
Confirm:
- [ ] Expected item count matches your database
- [ ] GitHub labels will be created if needed (or map to existing)
- [ ] Assignees are valid GitHub users
- [ ] OK to proceed with actual sync?
```

---

### Stage 4: Execute Sync
Run the actual sync with monitoring.

**Actions:**
1. Execute `notion_to_github.py` with full logging enabled
2. Monitor for errors in real-time
3. Track progress (X of Y records synced)
4. Record any items that failed to sync

**Template: Sync Execution Log**
```markdown
## Sync Execution: [Database Name]
**Start Time**: [ISO 8601]
**Status**: [In Progress / Complete / Failed]

### Progress
- Records processed: [X/Y]
- Successfully synced: [N]
- Failed: [N]
- Skipped: [N]

### Issues During Sync
[List any errors with context]

**End Time**: [ISO 8601]
**Duration**: [HH:MM:SS]
```

---

### Stage 5: Post-Sync Verification
Confirm sync completed successfully.

**Actions:**
1. Count GitHub issues created/updated
2. Verify property values synced correctly (labels, assignees, etc.)
3. Check for duplicates (same Notion record → multiple GitHub issues)
4. Document any manual fixes needed

**Template: Verification Report**
```markdown
## Post-Sync Verification: [Database Name]

### Results
- GitHub Issues Created: [N]
- GitHub Issues Updated: [N]
- Total: [N]

### Spot Checks
✓ Issue "[title]" has correct labels
✓ Issue "[title]" has correct assignee
✓ Issue "[title]" has correct title

### Issues Requiring Manual Fix
- Issue #[ID]: [description of issue]

### Next Steps
- [ ] Review GitHub issues
- [ ] Assign to team if needed
- [ ] Set up recurring sync (if applicable)
- [ ] Document sync schedule in team wiki
```

---

### Stage 6: Schedule & Monitor (Optional)
Set up recurring sync and monitoring.

**Actions:**
1. Configure cron job or GitHub Actions workflow for regular syncs
2. Set up monitoring/alerting for sync failures
3. Document runbook for team (when to sync, how to handle conflicts)
4. Archive this workflow documentation for future reference

**Template: Sync Runbook**
```markdown
# Sync Runbook: [Database Name]

## Schedule
- Frequency: [Daily / Weekly / Manual]
- Time: [HH:MM UTC] (if automated)
- Owner: [Team / Person]

## Prerequisites
- Notion API key still valid
- GitHub PAT still valid
- No ongoing GitHub incidents

## Sync Procedure
1. Run: `python scripts/notion_to_github.py`
2. Monitor for errors (check logs)
3. Verify issue count in GitHub
4. Report any failures to [Slack / issue board]

## Common Issues & Fixes
- Sync timeout: [step]
- Invalid assignee: [step]
- Label mismatch: [step]

## Escalation
If sync fails:
1. Check logs for Notion/GitHub errors
2. Run validation prompt: `/notion-validator [db-id]`
3. Alert [owner] if critical properties missing
```

---

## Summary

This workflow guides you through:
1. **Planning** what to sync
2. **Validating** prerequisites
3. **Testing** with a dry run
4. **Executing** the sync
5. **Verifying** results
6. **Scheduling** ongoing syncs

By following this structure, you reduce errors, gain confidence, and create reproducible sync processes for your team.

---

## Related Tools & Prompts

- **Notion Sync Agent** (`/notion-sync`): Execute and troubleshoot syncs
- **Notion Properties Validator** (`/validate-notion-properties`): Check property mappings
- **File Instructions** (`notion_to_github.py`): Modify sync script safely
- **NOTION_PROPERTIES.md**: Reference current mappings
