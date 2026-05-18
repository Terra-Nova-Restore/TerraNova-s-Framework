# PAUSE-001 - Solo Operating Playbook

This page is for Silvan working without Codex during the one-week pause.

## Best Solo Setup

Use the tools in this order:

1. **Notion** for truth-state and decisions.
2. **GPT** for synthesis, prompts, summaries and decision checks.
3. **GitHub Copilot / VS Code** for file edits.
4. **GitHub web UI** for PR status, checks and review.
5. **Zenodo web/API** only for read verification unless a separate explicit
   Zenodo write opening exists.

## Solo Rule

Do not try to make the whole system smarter at once.

Work one lane at a time:

```plain text
Read source
-> write short decision
-> update Notion or GitHub
-> run/check validation
-> stop
```

## If Using GPT

Paste this header first:

```plain text
You are helping with TerraNova/FerrAI Control Tower continuity.
Use Swiss German in chat and Hochdeutsch/English for artifacts.
No deletion. No raw Notion IDs in public text. No Zenodo writes.
Treat Notion as workspace memory, GitHub as PR proof and Zenodo API as public release truth.
Focus only on the named lane.
```

Then paste only the relevant file or Notion excerpt, not the whole workspace.

Recommended GPT tasks:

- summarize a Notion page into allowed/blocked claims.
- draft a registry row in plain text.
- check whether a claim is source-supported.
- turn rough notes into a small Markdown artifact.
- produce a PR review checklist.

Avoid asking GPT to:

- infer all 880 pages.
- rewrite the canon.
- invent trigger history.
- decide Zenodo publication action.
- process private IDs or secrets.

## If Using Notion AI

Use it manually and narrowly.

Good prompts:

```plain text
Summarize this page into: Status, Allowed claims, Blocked claims, Next source action.
```

```plain text
Extract only the decisions and unresolved questions from this page.
```

Avoid:

- Custom Agents.
- scheduled AI runs.
- autofill over large databases.
- mass summarization of all pages.

## If Using GitHub Copilot

Use Copilot for mechanical edits only:

- add a row to a CSV.
- update a Markdown checklist.
- adjust a small validation script.
- fix formatting.

Before commit:

```powershell
python -m py_compile scripts\cap_control_checks.py
python scripts\cap_control_checks.py --live-zenodo
git diff --check
```

Also search for raw Notion IDs:

```powershell
rg -n "https://www\.notion\.so/[0-9a-f]|collection://[0-9a-f]" docs\atlas\control-tower scripts -g "*.md" -g "*.csv" -g "*.json" -g "*.py"
```

## If Continuing PR #48 Manually

The safest next move is a review gate, not more expansion.

Checklist:

- PR branch is not behind `main`.
- `Validate Prism Atlas` is green.
- Netlify deploy preview is green.
- `AUTO-001 --live-zenodo` passes locally.
- no raw private Notion IDs in GitHub artifacts.
- `DASH-ZEN-004` is understood as the release-state matrix.

If all green, write a short PR comment:

```plain text
Control Tower trace is complete through DASH-ZEN-004.
Zenodo authority order is documented.
No Zenodo write, workflow execution, DOI/file/version mutation, or Notion AI credit use occurred in the control-tower closure.
Ready for Silvan review.
```

## Stop Conditions

Stop and wait for Codex/GPT review if:

- Zenodo state conflicts with Notion.
- a file contains raw private Notion IDs.
- a Notion operation would delete/move pages.
- a step asks for token/secret handling.
- anything touches publication, DOI, upload, workflow dispatch or PR #40.
