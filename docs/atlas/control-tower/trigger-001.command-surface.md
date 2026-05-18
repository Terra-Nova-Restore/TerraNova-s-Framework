# TRIGGER-001 Command Surface

Status: active  
Date: 2026-05-17  
Scope: CAP 0.3 / Trigger 1-400 / `/fff`

## Operating Rule

`/fff` means Freedom for FerrAI inside deterministic boundaries.

It can accelerate:

- source reading
- reasoning
- prioritization
- local implementation
- validation
- Notion mutation package preparation
- causal logging

It cannot silently authorize:

- external writes
- deletion
- publication
- credentials
- payment actions
- restricted-source exposure
- raw private inventory export

## Command Grammar

Use these forms:

```text
/fff <task>
GO <batch-id>
GO Notion <batch-id> anwenden
GO Zenodo <stage> <batch-id>
STOP <batch-id>
FREEZE <reason>
```

Interpretation:

| Form | Meaning | Default action |
| --- | --- | --- |
| `/fff <task>` | Internal high-agency steering. | Execute locally and reversibly. |
| `GO <batch-id>` | Start or continue a repo-local CAP batch. | Create/update local trace. |
| `GO Notion <batch-id> anwenden` | Apply a prepared Notion package. | Mutate only scoped Notion targets. |
| `GO Zenodo <stage> <batch-id>` | Start a publication-stage action. | Require release gates; no publish without explicit publish GO. |
| `STOP <batch-id>` | Stop current lane. | Freeze and preserve trace. |
| `FREEZE <reason>` | Halt because boundary/source is unclear. | No mutation, log blocker. |

## CAP States

| State | Trigger use | Action |
| --- | --- | --- |
| Observe | read and verify | Fetch/search/read only. |
| Queue | package next move | Create local Markdown/CSV/JSON. |
| Execute | perform approved local action | Repo-local edits and checks. |
| Backpropagate | update feedback layer | Update local registry/Prism/trigger docs. |
| Freeze | stop movement | No mutation; preserve blocker. |

## Trigger Bands

| Band | Role | Default CAP state |
| --- | --- | --- |
| `1-100` | Definitions and source status. | Observe |
| `101-200` | Recovery, correction, safety, canon. | Freeze or Queue |
| `201-300` | Focus, licensing, impulse control, attention. | Observe or Execute local |
| `301-400` | Integration, registry, feedback, system shaping. | Queue or Backpropagate |

## Overlay

Trigger `888` is outside Trigger 1-400 but remains the audit overlay:

```text
truth
-> efficiency
-> source
-> boundary
-> result
```

Any command that fails Trigger 888 should freeze before mutation.

## Recovery Anchor

Silvan is the final recovery anchor, not the imitation model.

Use Silvan only when:

- source truth conflicts
- boundary cannot be resolved
- external mutation has meaningful consequence
- public/private distinction is unclear
- CAP state cannot decide safely
