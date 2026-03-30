# Notion-GitHub Sync – Preflight Validation

This module validates the sync environment before executing any sync operations.

## Architecture

The sync pipeline consists of:
1. **Preflight Validation** (`preflight.py`) – Validates prerequisites
2. **Sync Execution** (`notion_to_github.py`) – Only runs if preflight passes
3. **Lock Management** – Prevents concurrent syncs

## Preflight Checks (5 mandatory validations)

### 1. **Secrets Validation**
Ensures API credentials are configured.

- ✓ `NOTION_API_KEY` is set (or legacy `NOTION_TOKEN` as fallback)
- ✓ `GH_PAT` is set (or `GITHUB_TOKEN` as fallback)

**Failure Diagnostic**:
```
Missing NOTION_API_KEY (or legacy NOTION_TOKEN)
→ Solution: Set NOTION_API_KEY env var or .env file
```

### 2. **Configuration File Validation**
Validates configuration JSON structure.

- ✓ Config file exists at specified path
- ✓ JSON is valid
- ✓ Required keys present (`github_repo`)

**Failure Diagnostic**:
```
Missing required config key: github_repo
→ Solution: Add github_repo to config/notion_map.json
```

### 3. **Notion Database Access**
Tests actual read access to Notion database.

- ✓ Notion API responds
- ✓ Database ID exists
- ✓ Integration has database access

**Failure Diagnostics**:

| Error | Cause | Solution |
|-------|-------|----------|
| `Notion auth failed: API key invalid or expired` | Wrong/expired API key | Regenerate API key in Notion integrations |
| `Notion permission denied: integration lacks database access` | Integration not shared with database | Open database in Notion → Share → Select integration |
| `Notion database not found` | Wrong database ID | Copy correct ID from Notion URL |

### 4. **GitHub Repository Access**
Tests read/write access to GitHub repository.

- ✓ GitHub API responds
- ✓ Repository exists and is accessible
- ✓ Token has write permission (push)

**Failure Diagnostics**:

| Error | Cause | Solution |
|-------|-------|----------|
| `GitHub auth failed: token invalid or expired` | Wrong/expired token | Regenerate PAT in GitHub settings |
| `GitHub permission denied: token lacks repo access` | Token has insufficient scopes | Regenerate with `repo` scope |
| `GitHub repository not found` | Wrong owner/repo format | Use format: `owner/repo` |
| `GitHub token lacks write permission to repository` | Token is read-only | Regenerate with `repo` scope (includes write) |

### 5. **Concurrency Check**
Prevents multiple sync processes from running simultaneously.

- ✓ No sync lock file exists
- ✓ Or existing lock is from terminated process

**Failure Diagnostic**:
```
Another sync process is running.
→ Solution: Wait for completion or remove .tnv_sync.lock manually if process crashed
```

## Secret Names & Precedence

| Variable | Type | Source | Status |
|----------|------|--------|--------|
| `NOTION_TOKEN` | Notion | Workflow | ✓ Currently used |
| `NOTION_API_KEY` | Notion | Alternative | ⚠️ Flexible fallback |
| `GH_PAT` | GitHub | Workflow | ✓ Currently used |
| `GITHUB_TOKEN` | GitHub | Alternative | ⚠️ Flexible fallback |
| `TARGET_GITHUB_REPO` | GitHub Repo | Secret/Variable/Local env | ✓ Optional override |
| `GITHUB_REPO` | GitHub Repo | Workflow/local env | ✓ Default/fallback |

**Current Practice**: Workflow sends `NOTION_TOKEN` and `GH_PAT`. Script accepts both the current names and alternatives for flexibility, but expects the workflow names.

**Repository resolution order**: `TARGET_GITHUB_REPO` → `GITHUB_REPO` → `config/notion_map.json (github_repo)`.

**Future Migration**: If renaming to `NOTION_API_KEY` is decided, update workflow secrets and this documentation consistently across all jobs.

## Configuration Loading

```python
from preflight import preflight_check

# Run validation
try:
    results, concurrency = preflight_check(
        database_id='abc123...',
        config_path='config/notion_map.json'
    )
    print(f"✓ Passed {results['passed']}/5 checks")
    
    # Now safe to run sync
    # ...
    
finally:
    # Always release lock
    concurrency.release()
```

## Error Diagnosis Flow

When preflight fails, the system provides structured diagnostics:

```
Preflight validation failed:
├─ Secrets: ✓ OK
├─ Config: ✓ OK
├─ Notion Access: ✗ FAILED
│  └─ Error: Notion database not found
│     Database ID: wrong-id-here
│     Solution: Copy correct ID from Notion URL
└─ GitHub Access: (not checked, stopped at Notion)
└─ Concurrency: (not checked, stopped at Notion)
```

The script stops at the first failure and provides actionable diagnostics.

## Common Scenarios

### Scenario 1: First-time Setup
```bash
export NOTION_API_KEY=ntn_xxxx...
export GH_PAT=ghp_xxxx...
export NOTION_DATABASE_ID_CHANGES=xxx...
python scripts/notion_to_github.py
# Preflight will guide you through any missing config
```

### Scenario 2: Token Expired
```
Preflight validation failed:
Notion auth failed: API key invalid or expired
→ Regenerate at: https://www.notion.com/my-integrations
```

### Scenario 3: Database Not Shared
```
Preflight validation failed:
Notion permission denied: integration lacks database access
→ In Notion: Open database → Share → Select your integration
```

### Scenario 4: Concurrent Sync
```
Preflight validation failed:
Another sync process is running.
→ Wait for completion, or manually: rm .tnv_sync.lock
```

## Testing Without Full Sync

To test preflight validation without running the full sync:

```python
from scripts.preflight import PreflightChecker
import logging

logging.basicConfig(level=logging.INFO)
checker = PreflightChecker()

# This will test everything except actually syncing
try:
    results, concurrency = checker.run(
        database_id='YOUR_DB_ID',
        config_path='config/notion_map.json'
    )
    print("All checks passed!")
    concurrency.release()
except Exception as e:
    print(f"Validation failed: {e}")
```

## Lock File Management

The sync uses a lock file (`.tnv_sync.lock`) to prevent concurrent execution:

```bash
# Lock acquired when sync starts
# Lock released when sync completes or fails

# Manual unlock (only if process crashed):
rm .tnv_sync.lock

# Check if sync is running:
cat .tnv_sync.lock  # Shows PID of running process
```

## Related Files

- [`.env.example`](../.env.example) – Template for environment variables
- [`notion_to_github.py`](./notion_to_github.py) – Main sync script
- [`NOTION_PROPERTIES.md`](../NOTION_PROPERTIES.md) – Property mappings
- [`.github/instructions/notion_to_github.py.instructions.md`](../.github/instructions/notion_to_github.py.instructions.md) – Development guidelines
