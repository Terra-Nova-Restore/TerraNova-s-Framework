# CAP-RT-001-BREAK - Runtime Branch End Control

Status: break marker created on 2026-05-18
Date: 2026-05-18
Parent gate: `CAP-RT-001`
Mutation policy: GitHub trace only. No Notion mutation, no Zenodo mutation, no
Notion AI credit use.

## Purpose

This break marker closes the current Codex window after the Control Tower
runtime contract was created.

It exists so the next session can resume from GitHub without reconstructing the
chat context.

## Current GitHub State

Branch:

```plain text
codex/cap-rt-001-control-tower-runtime
```

Current branch head before this break marker:

```plain text
8fd66ce docs(control-tower): add cap runtime contract
```

Base:

```plain text
origin/main after PR #48 merge
```

Mainline anchor:

```plain text
a81135b Merge PR #48: Control Tower SessionStart mainline trace
```

## Completed In CAP-RT-001

- Runtime contract created.
- Bedienungshandbuch created for Silvan.
- Dashboard lanes defined.
- Source routing defined.
- Guardrails defined.
- Action queue defined.
- Validator extended.
- Local and GitHub checks passed for the first CAP-RT-001 commit.

## Final End Control Checklist

Required before calling the break safe:

```powershell
python -m py_compile scripts\cap_control_checks.py
python scripts\cap_control_checks.py --live-zenodo
git diff --check
rg -n "https://www\.notion\.so/[0-9a-f]|collection://[0-9a-f]" docs\atlas\control-tower scripts -g "*.md" -g "*.csv" -g "*.json" -g "*.py"
```

Expected:

- Python compile: pass
- `AUTO-001 --live-zenodo`: pass
- Diff check: pass
- Raw private Notion ID scan: no hits
- GitHub branch checks: success

## Boundaries Preserved

- No Notion mutation.
- No Zenodo mutation.
- No Notion Custom Agents.
- No credit-consuming automation.
- No workflow dispatch.
- No raw private Notion IDs in GitHub trace.
- No merge decision for this CAP-RT branch.

## Resume Prompt

Use this after the break:

```plain text
Read the TerraNova skill first. Resume from CAP-RT-001-BREAK in
docs/atlas/control-tower/batch-cap-rt-001-break.md.

Current goal: CAP-RT-002.

Rules:
- Swiss German in chat, Hochdeutsch/English in workspace.
- No Notion or Zenodo mutation unless explicitly requested.
- No Notion Custom Agents or credit-consuming automation.
- Keep raw private Notion IDs out of GitHub.
- Start with git status, AUTO-001 live Zenodo, diff check and raw-ID scan.
```

## Best Next Gate

```plain text
CAP-RT-002
```

Recommended decision for `CAP-RT-002`:

- choose the first visible runtime surface.
- compare Notion View Package vs GitHub Markdown Dashboard vs local mini
  prototype.
- do not start all three at once.

