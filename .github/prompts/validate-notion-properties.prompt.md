---
description: "Use when: validating Notion database schema, checking property mappings are compatible, ensuring Notion DB is sync-ready, or diagnosing property-related sync failures"
argument-hint: "Database name or ID to validate"
---

# Notion Properties Validator

Validate that your Notion database schema matches the expected property mappings and is ready for GitHub sync.

## Validation Checklist

When validating a Notion database, systematically check:

### 1. **Property Existence & Types**
- [ ] Database accessible via API (can fetch records without auth errors)
- [ ] All expected properties exist in the database
- [ ] Each property has the correct Notion type (Text, Multi-select, Date, Relation, etc.)
- [ ] No critical properties are missing or hidden in Notion UI

### 2. **Property Mappings**
Using `NOTION_PROPERTIES.md`:
- [ ] Each Notion property name exactly matches the schema (case-sensitive)
- [ ] GitHub field mapping is defined for each property
- [ ] Data type conversions are supported (e.g., Notion Multi-select → GitHub labels)
- [ ] No unmapped Notion properties will cause sync to fail

### 3. **Data Format & Validation**
- [ ] Sample records contain valid data for each property
- [ ] Multi-select fields use only values defined in the GitHub label set
- [ ] Date fields are in ISO 8601 format (YYYY-MM-DD)
- [ ] Text fields don't exceed GitHub's field limits (e.g., issue title max 256 chars)
- [ ] Person fields reference valid GitHub users or have fallback handling

### 4. **Access & Permissions**
- [ ] Notion API key has database access (not just workspace level)
- [ ] API token can read the specific database ID
- [ ] No property requires additional permissions to access

### 5. **Sync Readiness**
- [ ] No circular relations (parent → child → parent)
- [ ] No properties that are marked "read-only" or managed by automations
- [ ] Database is not in archived state
- [ ] Configuration section in NOTION_PROPERTIES.md matches actual database

## Common Issues & Solutions

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| "Unauthorized" when fetching Notion DB | Invalid API key or no database access | Verify `NOTION_API_KEY` and database is shared with integration |
| Property not found in sync results | Property is marked "archived" in Notion | Un-archive or remove from NOTION_PROPERTIES.md |
| Data type mismatch (expected text, got array) | Notion property type changed after mapping | Update NOTION_PROPERTIES.md and translator function |
| Sync succeeds but labels don't appear | Multi-select values don't match GitHub labels | Create GitHub labels or update Notion field values |
| Rate limit hit during sync | Too many rapid API calls | Implement backoff in script or split sync into batches |
| Circular relation error | Notion formula/relation references parent | Simplify Notion schema or split into separate databases |

## Validation Output

After validation, provide:
- **Status**: ✓ All properties valid OR ✗ Issues found
- **Checked Properties**: List of properties validated with their types
- **Mapping Status**: Which properties map to GitHub, which don't
- **Issues**: Detailed list of any discrepancies or missing mappings
- **Sync Readiness**: Can this database be synced now? What needs fixing first?
- **Next Steps**: If issues exist, what to do next (update mappings, fix property types, etc.)

## Example Validation Report

```
Database: TerraNova Tasks
Database ID: abc123xyz789

PROPERTIES CHECKED (4/4):
  ✓ Name (Title) → GitHub issue title
  ✓ Status (Select) → GitHub labels [To Do, In Progress, Done]
  ✓ Assignee (Person) → GitHub assignee
  ✓ Due Date (Date) → GitHub milestone (or custom field)

MAPPING STATUS:
  ✓ All properties mapped
  ✓ No unmapped properties in database

ISSUES FOUND:
  ✗ Status field value "On Hold" not in NOTION_PROPERTIES.md
  ✗ Assignee field includes person "Jane Doe" not in GitHub team

SYNC READINESS: ⚠ NOT READY
  Fix required before sync:
  1. Add "On Hold" to Status mapping (decide GitHub equivalent: label or automation)
  2. Map "Jane Doe" to GitHub user or create fallback handling

NEXT STEPS:
  → Update NOTION_PROPERTIES.md with missing status value
  → Verify Jane Doe has GitHub account or assign to team lead
  → Re-validate database
  → Then run sync
```

---

**Usage**: Invoke this prompt with a Notion database name or ID to validate sync readiness.

Example prompts:
- "Validate my TerraNova Tasks database"
- "Check if the 'Backlog' database is ready to sync to GitHub"
- "Validate database ID: abc123xyz789"
