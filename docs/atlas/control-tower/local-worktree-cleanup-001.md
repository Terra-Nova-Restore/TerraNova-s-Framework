# LOCAL-WORKTREE-CLEANUP-001

Status: local worktree operating rule
Date: 2026-05-24
Scope: local Git worktree roles after PR #57 merge

## Purpose

This document prevents confusion between several local working folders.
It does not delete branches, delete worktrees, force-reset anything, or push
anything to GitHub.

## Current Worktree Roles

| Path label | Current role | Branch / state | Action |
| --- | --- | --- | --- |
| `TerraNova-s-Framework-z3` | main-derived execution lane | `codex/post-merge-snapshot-001` | Use for the current post-merge documentation lane. |
| `TerraNova-s-Framework` | completed release lane | `release/trigger-map-001` at merge commit | Keep as archive until explicit delete/cleanup GO. |
| `TerraNova-s-Framework-cycle03` | existing feature lane | `codex/cei-data-04-v0-3-cycle03` | Leave untouched. |
| `TerraNova-s-Framework-sessionstart-mainline` | existing control-tower runtime lane | `codex/cap-rt-001-control-tower-runtime` | Leave untouched. |
| `TerraNova-s-Framework-z2-worktree` | existing Zenodo lane | `codex/zenodo-z2-legacy-deposit-retry` | Leave untouched. |
| `TerraNova-s-Framework-zenodo-v3-main22` | existing Zenodo v3 lane | `codex/zenodo-v3-main22` | Leave untouched. |
| Codex detached worktrees | tool/cache lanes | detached HEAD | Leave untouched unless a separate cleanup pass is requested. |

## Operating Rule

New repo work should start from the clean main-derived worktree and use a
short-lived `codex/...` branch unless Silvan explicitly requests a release
branch or a direct main operation.

For this lane, the active local branch is:

`codex/post-merge-snapshot-001`

## Safe Cleanup Decision

No local worktree was deleted in this pass.

Reason: multiple worktrees represent active or historical lanes, and deleting
them would be a destructive local operation. The correct next step is to keep
them visible and only remove one after Silvan gives an explicit cleanup command
for that specific worktree or branch.

## Verified Facts

| Fact | Result |
| --- | --- |
| `main` was fast-forwarded to PR #57 merge commit before this lane started | `true` |
| `origin/main` merge commit | `5b6c30118ec8edb3a0e26bb6cab7d4283a78db6e` |
| Stale worktree metadata dry-run | no stale entries reported |
| External systems mutated | `none` |

## Next Safe Command

If this local documentation lane should be published later, use a normal PR
flow from `codex/post-merge-snapshot-001`. Do not push directly to `main`.
