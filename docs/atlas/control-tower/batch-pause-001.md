# PAUSE-001 - One Week Resume Handoff

Status: applied to Notion CAP checkpoint on 2026-05-18
Date: 2026-05-18
Expected resume window: 2026-05-25 or later
Mutation policy: live Notion checkpoint appended after explicit user request to
close and make continuation traceable.

## Situation

Codex usage is expected to pause for about one week. This handoff preserves the
current operational state so the next session can resume without reconstructing
the full thread.

Current branch:

```plain text
codex/control-tower-sessionstart-mainline
```

Current head before `PAUSE-001`:

```plain text
91c0781 docs(control-tower): add zenodo release matrix
```

Pull request:

```plain text
PR #48
```

## Completed Control Tower State

The Control Tower is no longer just an idea. It has an operational spine:

- CAP 0.1.0 created as the central Notion control surface.
- CAP registry exists and has canon/source/sensitivity fields.
- MMD-001 through MMD-007 extracted Mermaid/trigger/module bridge material.
- SOURCE-520, TEST-520 and SOURCE-521 stabilized SessionStart and Preflight.
- DASH-ZEN-001 through DASH-ZEN-004 stabilized the Zenodo dashboard lane.
- PR #48 carries the GitHub Atlas trace and validates through `AUTO-001`.

## Current Zenodo Authority Model

Use this order until changed:

1. `T0 Zenodo API / public record` is current external citation truth.
2. `T2 Notion Zenodo root` is internal dashboard/mirror/routing.
3. `T2 Z1/Z2/Z3 anchors` are historical routing-state and hard-lock precedent.
4. `T1 GitHub Atlas` is auditable interpretation/control trace.

Important live state from `DASH-ZEN-004`:

- Record: `20073579`
- DOI: `10.5281/zenodo.20073579`
- Concept DOI: `10.5281/zenodo.19774446`
- Version: `RC01-v12`
- Publication date: `2026-05-17`
- File: `main (44).pdf`
- Checksum: `md5:d791d480e75f3d89f9a103a28a5c5001`

## Best Next Step

Resume with:

```plain text
PR-048-READY-GATE
```

This should check whether PR #48 is ready to move from draft/work-in-progress
into a final review/merge path.

Decision rule:

- If local + GitHub checks are green and no raw private IDs are detected, mark
  PR #48 as ready for Silvan review.
- If checks fail, fix only the failing control-tower trace.
- If Notion/GitHub conflict, trust Notion for workspace state, GitHub for PR
  proof, Zenodo API for public release truth.

## Hard Boundaries

Do not do these without explicit new instruction:

- delete or move Notion pages.
- expose raw private Notion IDs in GitHub artifacts.
- run Notion Custom Agents or credit-consuming Notion AI automation.
- execute Zenodo writes, workflow dispatches, new versions, uploads, DOI
  changes or publish events.
- advance PR #40 / Z1.
- treat Z3 as latest live authority without live Zenodo API verification.
- elevate sensitive monographie material from Teil II / Teil III.

## Resume Checklist

Run:

```powershell
git status --short --branch
git log -5 --oneline
python -m py_compile scripts\cap_control_checks.py
python scripts\cap_control_checks.py --live-zenodo
git diff --check
rg -n "https://www\.notion\.so/[0-9a-f]|collection://[0-9a-f]" docs\atlas\control-tower scripts -g "*.md" -g "*.csv" -g "*.json" -g "*.py"
```

Then verify PR #48 head checks in GitHub.

## Minimal Resume Prompt

Use this when Codex returns:

```plain text
Read the TerraNova skill first. Resume from PAUSE-001 in
docs/atlas/control-tower/batch-pause-001.md.

Current goal: PR-048-READY-GATE.

Rules:
- Swiss German in chat, Hochdeutsch/English in workspace.
- No external mutation unless explicitly requested.
- Notion is workspace memory, GitHub is PR proof, Zenodo API is public release truth.
- Keep raw private Notion IDs out of GitHub.
- Do not use Notion Custom Agents or credit-consuming Notion AI automation.

Start by running git status, AUTO-001 with live Zenodo, diff check, raw-ID scan,
then inspect PR #48 checks and decide whether the PR is ready for Silvan review.
```

## Status

Pause handoff complete.
