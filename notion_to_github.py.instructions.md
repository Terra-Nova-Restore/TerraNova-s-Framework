---
description: "Use when: modifying notion_to_github.py, debugging sync script, extending property mappings, or troubleshooting sync failures"
applyTo: "scripts/notion_to_github.py"
---

# `notion_to_github.py` – Sync Script Guidelines

This is the core Notion-to-GitHub sync engine. Changes here affect all downstream integrations. Treat with care.

## Architecture Overview

The script orchestrates:
1. **Notion API Client**: Fetches database records with field mapping
2. **Property Translator**: Maps Notion fields → GitHub fields (labels, assignees, milestones)
3. **GitHub API Client**: Creates/updates issues and pull requests
4. **Error Recovery**: Logs failures, attempts retries on transient errors
5. **State Tracking**: Records synced IDs to prevent duplicates

## Before Modifying

**MANDATORY CHECKS** before any change:
- [ ] Read NOTION_PROPERTIES.md to understand current field mappings
- [ ] Review GITHUB_PROJECT_HELP.md to understand GitHub integration points
- [ ] Check requirements.txt for current dependency versions
- [ ] Verify all environment variables: `NOTION_TOKEN`, `NOTION_DATABASE_ID_CHANGES`, `GH_PAT`, `GITHUB_REPO`
- [ ] Test locally with a **test database** (not production)

## Critical Patterns

### API Error Handling
Always distinguish between:
- **Transient errors** (rate limits, temporary outages): Implement exponential backoff
- **Permanent errors** (auth failures, invalid DB/repo): Fail loudly with diagnostic info
- **Notion access issues**: Log `database_id`, failed API endpoint, and permission error explicitly—this is the #1 source of sync failures

### Environment Variable Consistency
- Use `NOTION_TOKEN` (current workflow convention)
- Use `GH_PAT` (current workflow convention)
- Script accepts `NOTION_API_KEY` and `GITHUB_TOKEN` as fallbacks for flexibility, but workflow sends the primary names
- **After any change**: Verify the source is `.github/workflows/tnv_notion_to_github.yml`

### Concurrency & Idempotency
- Assume the script may run in parallel; implement file-based locking or database state tracking
- Sync operations must be idempotent (running twice = same result as running once)
- Never assume a GitHub issue exists just because Notion record exists; verify state

### Property Mapping
- ALL field translations must be **documented in NOTION_PROPERTIES.md**
- Before mapping a new field, confirm it exists in both Notion and GitHub schemas
- Log when a Notion field doesn't map (e.g., custom fields without GitHub counterpart)

## Common Modifications

### Adding a New Property Mapping
1. Declare mapping in NOTION_PROPERTIES.md with type and validation rules
2. Add translator function: `translate_notion_<property>() → github_<field>`
3. Add test case covering edge cases (empty value, wrong type, special characters)
4. Document in script comments what happens when Notion field is missing

### Extending to New Database
1. Create new function `sync_<database_name>()`
2. Test independently with small record set
3. Document database ID and expected schema in NOTION_PROPERTIES.md
4. Update `main()` to conditionally call new sync function (default: disabled)

### Debugging Sync Failures
1. Add detailed logging at API boundaries (Notion fetch, GitHub create/update)
2. For Notion failures, log: `database_id`, `api_endpoint`, `filter_query`, `error_code`, `error_message`
3. For GitHub failures, log: `repo_slug`, `issue_title`, `error_code`, `rate_limit_remaining`
4. Never swallow exceptions—re-raise with context or exit(1)

## Testing & Validation

- **Unit tests**: Import and test translator functions in isolation
- **Integration tests**: Use `.env.test` with test database/repo credentials
- **Before deployment**: Run against test database, verify X records synced correctly, verify no duplicates created
- **After deployment**: Monitor first 10 syncs; log all errors; alert on Notion access failures

## Do Not

- ✗ Hardcode API keys or credentials
- ✗ Make breaking changes to property mappings without updating NOTION_PROPERTIES.md
- ✗ Remove error logging or flatten error details
- ✗ Assume environment is always valid; replicate preflight checks from Notion Sync Agent
- ✗ Change the primary token variable names in the workflow (NOTION_TOKEN, GH_PAT) without coordination
- ✗ Delete or archive GitHub issues without explicit user confirmation in log

## Preflight Validation (Required)

Your modifications should include or preserve:
```python
def preflight_check():
    """Validate all prerequisites before sync."""
    checks = {
        "NOTION_TOKEN": os.getenv("NOTION_TOKEN"),
        "GH_PAT": os.getenv("GH_PAT"),
        "NOTION_DATABASE_ID_CHANGES": os.getenv("NOTION_DATABASE_ID_CHANGES"),
        "GITHUB_REPO": os.getenv("GITHUB_REPO"),
    }
    for key, value in checks.items():
        if not value:
            raise ValueError(f"Missing required env var: {key}")
    # Add Notion DB access check
    # Add GitHub repo access check
    return True
```

## Related Files
- [NOTION_PROPERTIES.md](../../NOTION_PROPERTIES.md) – Field mapping reference
- [GITHUB_PROJECT_HELP.md](../../GITHUB_PROJECT_HELP.md) – GitHub integration details
- [requirements.txt](../../requirements.txt) – Dependencies
