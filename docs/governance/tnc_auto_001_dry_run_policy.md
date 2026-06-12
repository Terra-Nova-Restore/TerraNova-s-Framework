# TNC-AUTO-001 Dry-Run Policy

Status: BIZ / Governance
Source: Codex-local quartet concordance closure and TerraNova source-of-record policy.
Trace: `raw/exports/local-private/tncic-quartet-concordance-automation-closure-2026-06-04.md`
Boundary: Defines the local dry-run controller policy only; does not mutate Notion, GitHub remote, Zenodo, Gumroad, Stripe, Netlify, VORTEX, EQUILIBRIUM or public portal state.
Mode: BIZ
GitHub sync state: draft local policy in a clean worktree; validate through `scripts/validate_docs.py`.
Notion source awareness: required before any rule, canon, Reflexions-Log or workspace-memory mutation.

## Purpose

`TNC-AUTO-001` is the first local dry-run controller for TerraNovaCIC
self-extension. It turns quartet outputs into source manifests, lane
classification, risk reports and proposed changes without changing external
systems.

## Operating Rule

The controller may read local-private source packages and repo-visible
governance/configuration files. It may write ignored local-private reports. It
must refuse external mutation by default.

## Allowed MVP Actions

- read `raw/exports/local-private/`
- read repo-visible governance and policy files
- classify material into lanes
- detect public/private boundary risks
- emit dry-run reports
- run local validators and tests
- report commit-safety

## Blocked MVP Actions

- Notion writes
- GitHub push or PR creation
- merge, rebase, reset, stash or branch deletion
- Zenodo, Gumroad, Stripe or Netlify mutation
- public exposure of private, operator-sensitive or raw export material
- protected IP, tokenization, licensing or payment claim expansion

Exact sensitive taxonomy terms and local blocker patterns are kept in a
gitignored local-private lexicon. The tracked controller only carries generic
category names.

## Human Gate

Silvan remains the explicit gate for external reality. The MVP can recommend a
next command, but it cannot execute public, payment, publication, Notion or
GitHub-remote mutation.

## Completion Signal

The MVP is complete when it emits:

- source manifest
- claim ledger
- model vote matrix
- contradiction ledger
- boundary report
- risk report
- proposed changes
- next gate
- dry-run report

and when validators confirm:

- no external mutation
- no `#77` or CAP/Control Tower contamination beyond report-only references
- `raw/exports/local-private/` remains ignored by git
- commit-safety is explicitly assessed
