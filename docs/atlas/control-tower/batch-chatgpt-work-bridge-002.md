# CHATGPT-WORK-BRIDGE-002 — Notion Sync Reality Check

Status: `awaiting-local-codex`  
Date: 2026-07-13  
Repository: `Terra-Nova-Restore/TerraNova-s-Framework`  
Branch: `codex/chatgpt-work-bridge-002`  
Stack base: `codex/chatgpt-work-bridge-001` at `c15ea912994e9426f70024f0a41f205386d234fc`  
Requested by: Silvan Lenhard  
Created by: ChatGPT Work through the connected GitHub runtime  
Mutation policy: repository-only audit plus two gated result artifacts

## Purpose

Bridge cycle 2 tests a substantive but reversible handoff. Local Codex must
establish what the repository actually implements for the recurring
Notion-to-GitHub sync and separate that evidence from claims about Notion-side
automations.

This is a stacked draft trial. PR #94 and its branch remain unchanged. The
Bridge 002 draft is based on the verified Bridge 001 tip so it can reuse the
manual receiver and public-boundary pattern without merging Bridge 001.

## Source review supplied by ChatGPT Work

A targeted Notion review on 2026-07-13 found three relevant records:

- `Codex-Frag-Vorlag — 10-min GitHub-Sync diagnose` records that the
  10-minute GitHub Action is a one-way exporter: it selects explicitly marked
  Notion rows with no issue URL, creates or reuses a GitHub issue, writes the
  issue URL and date back, and stores a shadow record.
- `Notion-Recurrence-Loop neutralisiere` records a separate Notion-side
  recurrence/default-template mechanism that created unrelated pages. It also
  states that the Notion automation state requires UI-level verification.
- `LETSCHTI 3 SECRETS — Denn nie meh GitHub`, updated 2026-07-12, states that
  GitHub Actions now uses its automatic same-repository `GITHUB_TOKEN` with
  `contents: write` and `issues: write`; a separate GitHub PAT is not
  required for the Actions path.

These are source claims, not substitutes for repository evidence. No private
Notion URL, database ID, token value or workspace identifier belongs in the
result.

## Repository questions

Local Codex must answer from committed files only:

1. Is the scheduled workflow present, and what cron expression does it use?
2. Is the direction Notion to GitHub, GitHub to Notion, or bidirectional?
3. Which filter selects export candidates?
4. Does the implementation create/reuse GitHub issues, write the issue URL and
   export date back to the existing Notion row, and write shadow records?
5. Is there any repository call that creates a new Notion page?
6. Does the Actions workflow use the automatic `GITHUB_TOKEN`, and which job
   permissions are declared?
7. What can and cannot be concluded about the separate Notion recurrence from
   repository evidence alone?

## Required evidence

- `.github/workflows/tnv_notion_to_github.yml`
- `scripts/notion_to_github.py`
- `tests/test_notion_to_github.py`
- `README.md`
- `SETUP_RUNBOOK.md`
- `NOTION_PROPERTIES.md`
- `config/notion_map.json`
- `.github/skills/notion-sync-workflow/SKILL.md`

The repository-local Notion sync skill is reading context only. Its execution,
preflight and dry-run stages are overridden by this batch's stricter boundary.

## Critical safety correction

Do **not** execute `scripts/notion_to_github.py` in any mode. Its `validate`
and `dry-run` paths still perform a live Notion query before suppressing
writes. A source-only audit may run local unit tests and documentation
validators that do not access a network service.

Do not inspect environment-variable values. The names of documented variables
may be described, but credentials, token values and private IDs must never be
read or emitted.

## Direct local-Codex procedure

The operator opens this branch in a separate non-destructive worktree. Because
the desktop agent is already local Codex, it must not invoke the receiver's
nested `run` action.

1. Read the request, config, governance files and evidence list in full.
2. Perform the source-only audit and safe local validations.
3. Create exactly:
   - `docs/atlas/control-tower/chatgpt-work-bridge-002.local-result.json`
   - `docs/atlas/control-tower/causal-log.chatgpt-work-bridge-002-local-2026-07-13.json`
4. Run:
   - `python scripts/chatgpt_work_bridge_002.py validate-result`
5. After validation is green, publish only those two files:
   - `python scripts/chatgpt_work_bridge_002.py publish --gate "PUBLISH CHATGPT-WORK-BRIDGE-002"`
6. Report status, commit SHA, push result and redacted blockers. Do not merge.

## Hard boundaries

- no live Notion call;
- no GitHub issue API call as part of the audit;
- no sync-script execution, including `validate` and `dry-run`;
- no workflow dispatch;
- no Notion, Zenodo or TNC-WATCH mutation;
- no worktree cleanup, reset or branch overwrite;
- no absolute local paths, host identifiers, usernames, secrets, private URLs,
  session content, raw token data or protected material;
- no merge.

## Interpretation rule

A missing Notion page-creation call in this repository supports the conclusion
that the recurrence is outside this repository. It does not prove the current
state of a Notion-side automation. That limitation must appear in the result.

## Success condition

ChatGPT Work can independently read and verify exactly two local audit
artifacts from the remote branch, with no user copy/paste of their contents and
with all runtime/mutation flags false.

## Stop rule

If a required check would need a live API, credential value, private source or
mutation outside the two result artifacts, record `blocked` with a redacted
reason and stop.
