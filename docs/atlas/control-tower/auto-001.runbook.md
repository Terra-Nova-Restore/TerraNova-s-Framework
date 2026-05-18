# AUTO-001 Runbook

Status: active  
Date: 2026-05-17

## Best Default

Run local checks before external mutation.

```powershell
python scripts/cap_control_checks.py
```

Run live Zenodo read when publication metadata matters.

```powershell
python scripts/cap_control_checks.py --live-zenodo
```

Record a test result when closing a CAP batch.

```powershell
python scripts/cap_control_checks.py --live-zenodo --output docs/atlas/control-tower/auto-001.test-results-2026-05-17.json
```

## What Counts As Pass

- Script exits with code `0`.
- `status` is `pass`.
- No errors are listed.
- `external_mutation` remains `false`.
- `notion_ai_credits_used` remains `0`.

## What Counts As Fail

- Any required file is missing.
- CSV row counts drift without an intentional update.
- A causal log fails JSON parsing.
- Legacy causal logs without `log_id`/`event_id` are warnings, not failure, unless they block the current batch.
- Zenodo reference does not match the current metadata state.
- Live Zenodo API differs from expected DOI/version/file checksum.

## Stop Rules

Stop before external mutation if:

- AUTO-001 fails.
- Zenodo live metadata differs from the local delta file.
- A CAP batch has no causal log.
- A change would require Notion Custom Agents or scheduled Notion AI.
- A change would expose raw private inventory.

## Escalation

Escalate to Silvan only when the failure cannot be resolved from local files, public Zenodo read, or Notion read-only checks.
