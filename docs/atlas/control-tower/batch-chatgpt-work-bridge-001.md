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
-> local receiver
-> local Codex
-> validated GitHub result artifact
-> ChatGPT Work verification
```

The batch extends the existing CAP Control Tower runtime and the earlier
`PAUSE-001` handoff pattern. It does not introduce a parallel inbox/outbox
architecture.

## Source review and architecture correction

A targeted Notion and GitHub source review on 2026-07-13 established:

- The production 10-minute workflow is a one-way Notion-to-GitHub issue
  exporter. It selects database rows with `Export_to_GitHub=true` and an empty
  `GitHub_Issue_URL`, creates or reuses a GitHub issue, writes the issue URL and
  export date back to Notion, and stores a shadow record.
- That workflow is an intake and trace mechanism. It is **not** a Codex runtime
  trigger and must not be silently redefined as one.
- The existing local architecture deliberately keeps Codex as the local
  implementation hand, GitHub as the technical trace, and Notion as the living
  source of record.
- Existing Codex handoffs require a Silvan-forward. A laconic instruction is
  sufficient, but the human dispatch gate remains explicit.
- `TNC-AUTO-001` already provides local-only, default-deny controller and
  validation patterns. The limited-live watcher remains manual-gated and has
  not completed its three clean live-push promotion cycles.

Therefore this trial adds a **manual local receiver** without modifying the
production Notion sync and without enabling a background loop.

## Local receiver v0.1

Tracked components:

- `.codex/chatgpt-work-bridge-001.json` — activation, Codex and publish policy;
- `scripts/chatgpt_work_bridge_001.py` — observe, run, validate and publish
  state machine;
- `tests/test_chatgpt_work_bridge_001.py` — contract and refusal tests;
- `docs/atlas/control-tower/chatgpt-work-bridge-001.request.json` — bounded
  request contract.

Initial state:

```text
activation_mode: manual-only
polling_enabled: false
notion_issue_intake_enabled: false
publish_enabled_by_default: false
clean_manual_cycles: 0/3
```

The receiver uses `codex exec` in ephemeral `workspace-write` mode. It does not
use `danger-full-access`, does not ignore project rules or user configuration,
and does not give Codex responsibility for the GitHub push. Codex writes the
two local result artifacts; the deterministic receiver validates and publishes
only those files after a separate exact gate.

## Required reading

Before acting, local Codex must read:

- `docs/governance/public_boundary.md`
- `docs/governance/chatgpt_connector_runtime_policy.md`
- `docs/atlas/control-tower/README.md`
- `docs/atlas/control-tower/local-worktree-cleanup-001.md`
- `docs/atlas/control-tower/causal-log.pause-001-handoff-2026-05-18.json`
- `docs/atlas/control-tower/chatgpt-work-bridge-001.request.json`

## Initial manual cycle

Run from a clean checkout of `codex/chatgpt-work-bridge-001`:

```text
python scripts/chatgpt_work_bridge_001.py observe
python scripts/chatgpt_work_bridge_001.py run
python scripts/chatgpt_work_bridge_001.py validate-result
```

The first three commands perform no GitHub remote mutation. After reviewing the
two generated files, publish them with the explicit, separately scoped gate:

```text
python scripts/chatgpt_work_bridge_001.py publish \
  --gate "PUBLISH CHATGPT-WORK-BRIDGE-001"
```

The publish step refuses unrelated staged or worktree changes, stages exactly
the two expected outputs, creates one commit, pushes only to the named branch,
and never merges.

## Task for local Codex

1. Confirm that the repository-local request can be read.
2. Perform a metadata-only local verification:
   - repository is available;
   - checked-out branch is correct;
   - the worktree is readable and writable;
   - the public-boundary documents are present;
   - the current task can be completed without exposing private local data.
3. Create these two result artifacts:
   - `docs/atlas/control-tower/chatgpt-work-bridge-001.local-result.json`
   - `docs/atlas/control-tower/causal-log.chatgpt-work-bridge-001-local-2026-07-13.json`
4. Do not commit, push or merge. Publishing belongs to the receiver's separate
   exact gate.

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
- execute a Notion-exported GitHub issue body as a prompt;
- enable polling or a scheduler during the initial trial;
- use Notion AI credits.

## Promotion path

The existing 10-minute Notion exporter may become an optional intake signal
only after three clean manual bridge cycles and a separate activation gate.
Even then, an issue body remains untrusted data: it may point to a committed,
validated request contract but is never executed directly.

No scheduler, daemon, self-hosted runner, generic issue trigger or automatic
publish is authorized by this draft.

## Success condition

The bridge passes when ChatGPT Work can read the two local result artifacts from
the remote branch without the user copying, pasting or uploading their contents.

## Stop rule

If any required verification would cross the public boundary, record
`status: blocked` with a redacted reason and stop.
