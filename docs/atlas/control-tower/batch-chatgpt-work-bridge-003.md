# CHATGPT-WORK-BRIDGE-003 — Network-free Offline Sync Validation

Status: `awaiting-local-codex`  
Date: 2026-07-13  
Repository: `Terra-Nova-Restore/TerraNova-s-Framework`  
Branch: `codex/chatgpt-work-bridge-003`  
Stack base: `codex/chatgpt-work-bridge-002` at `17ccc08a6c0b01591dcefaf26c5cfbc0043a9222`  
Requested by: Silvan Lenhard  
Created by: ChatGPT Work through the connected GitHub runtime  
Mutation policy: exact two-path implementation plus two gated result artifacts

## Purpose

Bridge cycle 3 is the first controlled code-change handoff. It converts the
Bridge 002 finding into a useful safety feature: an explicit
`offline-validate` mode that proves repository-local configuration and
workflow structure without touching a live service.

The existing `validate` and `dry-run` modes are not offline. Both reach the
live preflight/query path. They must not be executed or silently redefined in
this cycle.

## Exact implementation scope

Modify or create only:

- `scripts/notion_to_github.py`
- `tests/test_notion_to_github_offline.py`

Then create:

- `docs/atlas/control-tower/chatgpt-work-bridge-003.local-result.json`
- `docs/atlas/control-tower/causal-log.chatgpt-work-bridge-003-local-2026-07-13.json`

The deterministic publisher must see exactly these four dirty paths and create
one exact-scope commit. No other file may be staged, committed or pushed.

## Required behaviour

The new `offline-validate` mode must:

1. branch before `setup_logging`, `preflight_check`, credential reads,
   `requests.Session`, NC/GH construction, locks and live API work;
2. read only repository-local files needed to validate the sync contract;
3. validate at least the committed config mapping and workflow structure;
4. emit a public-safe machine-readable result;
5. create no log, hash, lock, shadow or other runtime artifact;
6. succeed with Notion and GitHub credentials absent;
7. return non-zero with a public-safe error when local config/workflow evidence
   is missing or invalid.

The existing `full`, `dry-run` and `validate` semantics must not be
intentionally changed.

## Required refusal tests

The new test file must prove that the offline path does not:

- call `preflight_check`;
- instantiate `requests.Session`;
- read credential values;
- create live-runtime artifacts.

Tests must fail loudly if either preflight or a requests session is used. Safe
existing unit and documentation tests may also run. No live mode may run.

## Direct local-Codex procedure

Use a new non-destructive worktree for
`codex/chatgpt-work-bridge-003`. Leave all existing worktrees and TNC-WATCH
untouched.

Because the desktop agent is already local Codex, do not invoke the receiver's
nested `run` action.

1. Read the request, config, governance files, Bridge 002 result and all source
   evidence in full.
2. Implement only the two named implementation paths.
3. Run the offline CLI with credential variables absent and network guards
   active.
4. Run the new refusal tests plus relevant existing non-network tests.
5. Confirm the offline run created no extra files.
6. Create exactly the two result artifacts.
7. Run:
   - `python scripts/chatgpt_work_bridge_003.py validate-result`
8. After validation is green, publish exactly four paths:
   - `python scripts/chatgpt_work_bridge_003.py publish --gate "PUBLISH CHATGPT-WORK-BRIDGE-003"`
9. Report status, commit SHA, push result and redacted blockers. Do not merge.

## Public boundary

Do not include absolute local paths, usernames, host/device identifiers,
credential values, private URLs, raw session or token data, pending-record
content, Notion database IDs or protected material.

Repository-relative paths, public workflow structure and documented environment
variable names are allowed. Values are not.

## Success condition

ChatGPT Work independently verifies one exact four-path return commit, the
offline implementation, refusal tests, public-safe result, successful CI and
unchanged PR #94, PR #95 and TNC-WATCH state.

## Stop rule

If any requirement needs a live API, credential value, private source, fifth
dirty path or mutation outside the exact publication scope, record `blocked`
with a redacted reason and stop.
