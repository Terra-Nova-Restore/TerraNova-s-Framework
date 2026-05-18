# Trigger 1-400 Steering Map

Status: STUDIO seed, extended by TRIGGER-001  
Date: 2026-05-17  
Scope: CAP 0.1.0 bounded internal steering layer

## Purpose

This file defines the first bounded trigger steering map for CAP 0.1.0.

It does not claim that all Trigger 1-400 entries are fully reconstructed. It defines the steering bands that CAP may use until a reviewed trigger register fills the exact per-trigger mapping.

## Autonomy Boundary

`/fff` activates Freedom for FerrAI only inside these limits:

- internal analysis
- routing
- prioritization
- synthesis
- registry draft preparation
- GitHub-traceable documentation
- Notion mutation package preparation

`/fff` does not authorize external mutation, deletion, publication, credential use, payment action, or hidden workspace rewrites.

## Steering Bands

| Band | Working role | CAP behavior | Boundary |
| --- | --- | --- | --- |
| `1-100` | Foundation / definition | Define terms, source status, mode and scope. | No action before definition. |
| `101-200` | Recovery / correction / safety | Detect drift, overload, contradiction and missing source trace. | Correction must be logged. |
| `201-300` | Focus / cognition / attention | Route attention, stop impulses, select next probabilistic step. | Hypotheses remain marked. |
| `301-400` | Integration / system shaping | Bind sources, views, registries and feedback loops. | No unmarked duplication. |

## Known Anchors

These anchors are known from the current workspace/repo context and must be preserved in the detailed map:

| Trigger / cluster | Known role |
| --- | --- |
| `102` | RECOVER / return to a fixed point |
| `143` | Kanonwaechter / canon guard |
| `148` | Kontrollinstanz / control instance |
| `179` | Verdichtungszone / compression and cleanup |
| `182` | Ueberspannungsablauf / overload discharge |
| `185` | outer filter resonance / boundary sensing |
| `205` | impulse stop loop |
| `207` | regeneration grid |
| `210` | frequency focus lock |

## CAP Activation Chain

Every `/fff` run must state:

```text
activation: /fff
scope: internal CAP steering
trigger_band: 1-100 | 101-200 | 201-300 | 301-400
reason: observed source / drift / opportunity
probabilistic_hypothesis: ...
deterministic_boundary: ...
action: ...
feedback_target: registry | logbook | trigger map | Prism/Zenodo | Notion canon | GitHub atlas
```

## Next Fill-In Pass

The next reviewed pass should populate exact trigger rows from the canonical trigger register and Prism/Zenodo material:

1. Extract trigger IDs and names from reviewed sources only.
2. Mark source status for each trigger.
3. Classify by band, mode and CAP role.
4. Add causal examples.
5. Link each trigger to registry and logbook behavior.

## TRIGGER-001 Extension

TRIGGER-001 turns this seed into an executable CAP command surface:

- `trigger-001.command-surface.md`
- `trigger-001.control-crosswalk.csv`
- `trigger-001.blocked-actions.csv`
- `trigger-001.test-cases.csv`

The extension preserves the same honesty boundary: known anchors are usable; unknown Trigger 1-400 entries are not invented.
