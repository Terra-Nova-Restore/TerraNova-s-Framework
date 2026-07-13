# CHATGPT-WORK-BRIDGE-001 — Cloud Work to Local Codex Handoff

Status: `awaiting-local-codex`  
Date: 2026-07-13  
Repository: `Terra-Nova-Restore/TerraNova-s-Framework`  
Branch: `codex/chatgpt-work-bridge-001`  
Base commit: `e5ddb0e15e342593d5ead8f0e92ffd89a93463ca`  
Requested by: Silvan Lenhard  
Created by: ChatGPT Work through the connected GitHub runtime  
Source of record for this test: GitHub branch and draft PR  
Mutation policy: GitHub trace only

## Purpose

Verify a bounded, auditable handoff from a cloud ChatGPT Work thread to a
locally running Codex instance and back through GitHub.

This test does **not** claim a direct runtime or remote-host connection between
the two agents. It verifies the shared, versioned bridge:

```text
ChatGPT Work
-> GitHub request artifact
-> local Codex
-> GitHub result artifact
-> ChatGPT Work verification
```

The batch extends the existing CAP Control Tower runtime and the earlier
`PAUSE-001` handoff pattern. It does not introduce a parallel inbox/outbox
architecture.

## Required reading

Before acting, local Codex must read:

- `docs/governance/public_boundary.md`
- `docs/governance/chatgpt_connector_runtime_policy.md`
- `docs/atlas/control-tower/README.md`
- `docs/atlas/control-tower/local-worktree-cleanup-001.md`
- `docs/atlas/control-tower/causal-log.pause-001-handoff-2026-05-18.json`
- `docs/atlas/control-tower/chatgpt-work-bridge-001.request.json`

## Task for local Codex

1. Fetch the remote branch `codex/chatgpt-work-bridge-001`.
2. Use an existing safe TerraNova worktree or create a new non-destructive
   worktree for this branch.
3. Confirm that this request can be read locally.
4. Perform a metadata-only local verification:
   - repository is available;
   - checked-out branch is correct;
   - the worktree is readable and writable;
   - the public-boundary documents are present;
   - the current task can be completed without exposing private local data.
5. Create these two result artifacts:
   - `docs/atlas/control-tower/chatgpt-work-bridge-001.local-result.json`
   - `docs/atlas/control-tower/causal-log.chatgpt-work-bridge-001-local-2026-07-13.json`
6. Commit and push the two artifacts to the **same branch**.
7. Do not merge the draft PR. Leave final verification to ChatGPT Work and the
   human owner.

## Result requirements

The local result must be public-safe and include:

- bridge ID;
- actor label `local-codex`;
- UTC observation time;
- repository full name;
- branch name;
- base commit observed;
- booleans for request readability, worktree readability and branch writability;
- count of local TerraNova worktrees, without absolute paths;
- labels for relevant worktree roles, without usernames or private paths;
- public-boundary check result;
- list of result files created;
- final status: `pass`, `partial` or `blocked`;
- blockers, if any.

## Hard boundaries

Do not include or expose:

- absolute local filesystem paths;
- usernames, device identifiers or hostnames;
- environment variables, credentials, cookies or tokens;
- raw Codex/ChatGPT session history;
- private prompt or conversation content;
- raw token-usage databases;
- raw Notion IDs or private workspace URLs;
- patent-sensitive, Track C, GODFATHER_LOCK or other protected material.

Do not:

- delete or clean up worktrees;
- force-reset branches;
- push directly to `main`;
- mutate Notion or Zenodo;
- dispatch workflows;
- alter existing active worktrees;
- use Notion AI credits.

## Success condition

The bridge passes when ChatGPT Work can read the two local result artifacts from
the remote branch without the user copying, pasting or uploading their contents.

## Stop rule

If any required verification would cross the public boundary, record
`status: blocked` with a redacted reason and stop.
