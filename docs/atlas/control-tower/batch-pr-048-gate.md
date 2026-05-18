# PR-048-GATE - GitHub Mainline Admission Gate

Status: passed with redaction fix
Date: 2026-05-18
PR: https://github.com/Terra-Nova-Restore/TerraNova-s-Framework/pull/48
Repository visibility: public
External mutation: GitHub PR branch update only, after explicit `PR-048-GATE go`
Notion AI credits used: 0

## Purpose

PR-048-GATE checks whether the Control Tower SessionStart mainline trace can
remain in a public GitHub PR without leaking private workspace handles or
claiming stronger canon status than the sources support.

## Inputs

- `origin/main`
- `codex/control-tower-sessionstart-mainline`
- PR #48 draft state
- AUTO-001 local validation harness
- public Zenodo record `10.5281/zenodo.20073579`

## Findings

| Gate | Result | Evidence |
| --- | --- | --- |
| Mainline shape | Pass | Branch is ahead of `origin/main` and not behind. |
| AUTO-001 | Pass | `python scripts/cap_control_checks.py --live-zenodo` passed. |
| Python syntax | Pass | `python -m py_compile scripts/cap_control_checks.py` passed. |
| Whitespace check | Pass after cleanup | `git diff --check` passed on the working tree. |
| Secret/token scan | Pass | No API key, bearer token, password, GitHub token, Slack token or OpenAI key pattern was found. |
| Public Notion handle scan | Pass after redaction | Raw Notion URLs, collection IDs, UUID object IDs and local desktop paths were replaced with redacted internal handles. |
| Canon boundary | Pass | 520 and 521 remain L2/L1-L2 bounded; no L3/L4 elevation, no TRG assignment and no autonomous execution claim. |
| External mutation boundary | Pass | No Notion, Zenodo, Drive, Slack, Stripe or Linear mutation performed. GitHub branch update is the only mutation and is scoped to PR #48. |

## Redaction Fix

Because the repository is public, direct Notion URLs, `collection://` data
source handles, raw UUID object IDs and local desktop paths are not acceptable
inside the public PR trace. The gate keeps object meaning through names and
redacted handle classes only:

- `notion://redacted-internal-object`
- `notion-ds://redacted-internal-source`
- `notion-id://redacted`
- `<local-sensitive-home-ansichten-snapshot>`
- `<local-sensitive-desktop>`

The internal system of record remains Notion. GitHub keeps the public-safe
audit trace.

## Decision

PR #48 is no longer blocked by PR-048-GATE. Keep it as draft until Silvan gives
a separate ready/merge command. The next controlled action is `PR-048-READY`
or `SYNC-005 - Notion Trace Closure` after merge readiness is explicitly
confirmed.
