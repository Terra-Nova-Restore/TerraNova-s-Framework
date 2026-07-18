# OAL-001 Controlled Self-Modification Policy

Status: BIZ / local dry-run bootstrap policy
Source: Notion design baseline `IPERKA — Autodidaktisches Observatory / Codex Runtime (OAL-1.0)` and GitHub Issue #97
Trace: GitHub Issue #97; `config/oal_001.json`; `schemas/oal_001_mutation_trace.schema.json`
Boundary: Local candidate sandbox only; no external, remote, Notion, ledger, publication, payment or production mutation
Mode: BIZ / local dry-run
GitHub sync state: prepared on the isolated local branch `codex/observatory-selfmod-001`; promotion remains human-gated
Notion source awareness: the design baseline was inspected read-only before implementation; this mirror contains no Notion object IDs and performs no Notion write

## Purpose

This policy defines the first reversible implementation slice for OAL-001. It
separates a baseline-only Governor from one explicitly mutable Observatory
example and proves candidate isolation, replay, evaluation and rollback.

The bootstrap commit that creates the Governor and its authorizing tests is a
human-gated implementation action. It is not itself an autonomous
self-modification cycle. Candidate cycles created by the runtime remain subject
to the Governor.

## Immutable Governor

The same candidate cycle may not change:

- human gates, branch or worktree boundaries;
- secret handling or external-mutation defaults;
- audit, trace, replay, determinism or rollback logic;
- the Governor, runtime, validator, CI workflow, configuration or trace schema;
- a control rule together with the test that authorizes that rule.

Any proposed path outside the exact mutable allowlist is rejected before a
candidate file is written. Absolute paths, traversal, symlinks and shared
hard-linked files are refused.

## Mutable Observatory

The first slice permits exactly one candidate target:

```text
scripts/oal_001/observatory.py
```

The harmless example adjusts only synthetic strategy weights. It activates no
connector or productive function. The candidate is copied from the baseline
through an explicit managed-path allowlist; the repository tree is never copied
or scanned wholesale.

## Candidate Lifecycle

```text
baseline hash
  -> Governor preflight
  -> temporary allowlisted candidate copy
  -> deterministic source patch
  -> AST-constrained replay
  -> baseline/candidate comparison
  -> retain-or-reject decision
  -> candidate rollback
  -> workspace discard
  -> mutation trace and local report
```

The candidate source is parsed as data. Arbitrary candidate code is not
executed in this slice. A retained decision means the candidate satisfied the
technical gates; it does not promote or activate the candidate.

## Evidence and Promotion

Run evidence is written only below the gitignored path
`raw/exports/local-private/oal-001/`. It must record the trigger, hypothesis,
expected effect, fallback criterion, hashes, diff identity, replay results,
evaluator decision, rollback proof, Git status and zero external mutations.
The Git snapshots contain only canonical `porcelain=v1` dirty entries with all
untracked files expanded, submodule changes included and rename detection fixed
off. Branch, HEAD and dirty state remain separate bindings;
upstream names and ahead/behind counters never enter the trace or run identity.
Evidence files are replaced atomically. A run remains `INCOMPLETE` until the
validator has reconstructed the cross-artifact evidence and written a final
completion marker that binds the SHA-256 digest of every other artifact.
Semantic validation and digest binding use the same immutable in-memory byte
snapshot. The write-free `--verify-existing <run-id>` path reconstructs the
final bundle from one fresh snapshot and performs no test, dry-run or evidence
write. A final `PASS` produced under Python 3.11 is promotion-ready only when
the canonical dirty-state snapshots are empty and the boundary status is `PASS`;
`PASS_WITH_RUNTIME_GAP` is valid local evidence but blocks promotion.
A semantically valid dirty bundle remains `promotion_ready=false` and
`evidence_complete=false`; read-only verification reports
`VERIFIED_NOT_PROMOTION_READY` with a non-zero exit instead of exposing a false
promotion gate.

The dedicated `OAL Python 3.11` pull-request check runs the complete validator
on the exact PR head in an ephemeral, read-only GitHub Actions job. It persists
no checkout credentials, receives no secrets and publishes no evidence.

All Git observations pass through a protected typed read-only adapter. It uses
a fixed system Git executable, disables optional locks and filesystem monitors,
and supplies a minimal child environment without arbitrary inherited values.

No real predecessor Hubble or ALMA cycle is present in the repository at this
bootstrap point. The included replay fixture is explicitly synthetic and may
not be represented as historical evidence. Admission of real predecessor
fixtures, broader engines, a ledger writer, three controlled cycles and any
live ledger append are separate human-gated follow-up work.
