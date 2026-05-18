# AUTO-001 - No-Credit Control Checks

Status: STUDIO implementation, repo-local  
Date: 2026-05-17  
External mutation: none  
Credit-consuming automation: none

## Recommended Variant

Build automation as a local validation harness first.

The best path is:

```text
CAP artifacts
-> local parser/checker
-> optional public Zenodo read
-> JSON test result
-> manual decision before external mutation
```

This gives speed without letting Notion Custom Agents or scheduled Notion AI consume credits or mutate the workspace.

## Purpose

AUTO-001 makes CAP 0.3 testable.

It creates a repeatable local check that verifies:

- CAP control artifacts exist
- CSV manifests have expected row counts
- causal logs parse as JSON
- Zenodo reference reflects the 2026-05-17 metadata refresh
- public Zenodo API still matches expected record, DOI, concept DOI, version and file checksum
- no external mutation is part of the check

## Current Zenodo Live Delta

Silvan updated Zenodo metadata on 2026-05-17.

Read-only verification confirms:

| Field | Current value |
| --- | --- |
| Record | `20073579` |
| DOI | `10.5281/zenodo.20073579` |
| Concept DOI | `10.5281/zenodo.19774446` |
| Version | `RC01-v12` |
| Publication date | `2026-05-17` |
| Metadata updated | `2026-05-17T07:20:40.751823+02:00` |
| File | `main (44).pdf` |
| File checksum | `md5:d791d480e75f3d89f9a103a28a5c5001` |
| File size | `2,943,457` bytes |

Interpretation:

```text
metadata refreshed
-> citation surface changed
-> DOI and file remained stable
-> PRISM-002 blocker still artifact-readiness, not metadata-readiness
```

## Implemented Tool

```text
scripts/cap_control_checks.py
```

Default mode:

```powershell
python scripts/cap_control_checks.py
```

Live Zenodo read mode:

```powershell
python scripts/cap_control_checks.py --live-zenodo
```

Write test result:

```powershell
python scripts/cap_control_checks.py --live-zenodo --output docs/atlas/control-tower/auto-001.test-results-2026-05-17.json
```

## Boundaries

Allowed:

- local file checks
- JSON parsing
- CSV row counts
- public Zenodo API read
- local JSON result file

Blocked:

- Notion Custom Agents
- scheduled Notion AI
- Notion Autofill
- Notion page mutation
- Zenodo draft/upload/publish
- DOI reservation
- credential use
- raw private workspace export

## Control Answer

AUTO-001 is the first repeatable test harness for CAP 0.3.

It does not prove the whole workspace is correct. It proves the control surface is internally coherent enough for the next test layer.

## First Test Run

Command:

```powershell
python scripts/cap_control_checks.py --live-zenodo --output docs/atlas/control-tower/auto-001.test-results-2026-05-17.json
```

Result:

| Signal | Value |
| --- | --- |
| Status | `pass` |
| Required files | pass |
| CSV row counts | pass |
| Causal logs parsed | 21 |
| Legacy causal logs without `log_id` / `event_id` | 6 warnings |
| Zenodo reference | pass |
| Zenodo live API | pass |
| External mutation | false |
| Notion AI credits used | 0 |

## TRIGGER-001 Extension Test

After TRIGGER-001, AUTO-001 also checks:

| Signal | Value |
| --- | --- |
| Required trigger files | pass |
| Trigger crosswalk rows | 14 |
| Trigger blocked-action rows | 12 |
| Trigger test cases | 12 |
| AUTO-001 result after extension | `pass` |

## Next Recommended Step

Run `AUTO-001` after every CAP batch and before any external mutation.

The next CAP batch can be:

1. `DASH-001` if the goal is better Notion dashboard steering.
2. `TRIGGER-001` if the goal is command-surface hardening for `/fff`.
