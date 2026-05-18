# MMD-003 - Visual Trigger Bridge

Date: 2026-05-17

Activation: `MMD-003 - Visual Trigger Bridge / go`

Mode: repo-local synthesis from MMD-002 graph tables

External mutation: none

Notion AI credits used: 0

## Purpose

MMD-003 builds the first safe bridge from Mermaid graph structure to trigger
module candidates.

It does not define canonical `TRG-*` entries. It only marks visual trigger
evidence that can later be reviewed.

## Inputs

| File | Role |
| --- | --- |
| `mmd-002.graphs.csv` | Graph metadata, role and zoom layer. |
| `mmd-002.nodes.csv` | Node labels and degree signals. |
| `mmd-002.edges.csv` | Source/target relations. |
| `mmd-002.guard-conditions.csv` | Guard conditions and extracted trigger references. |

## Outputs

| File | Purpose |
| --- | --- |
| `mmd-003.visual-trigger-candidates.csv` | Candidate trigger/module rows from visual nodes. |
| `mmd-003.guard-bridge.csv` | Guard/edge rows relevant to trigger routing. |
| `mmd-003.sensitivity-review.csv` | Sensitive/restricted rows that need explicit review. |
| `mmd-003.bridge-summary.json` | Machine-readable summary. |
| `mmd-003.visual-trigger-bridge.md` | Human-readable bridge summary. |
| `scripts/build_visual_trigger_bridge.py` | Repeatable builder. |

## Result

| Metric | Count |
| --- | ---: |
| Visual trigger candidates | 53 |
| Guard bridge rows | 140 |
| Sensitivity review rows | 20 |
| Unique visible trigger references | 14 |

Visible trigger references:

```text
174-210, 516, 517, 520, 521, 540, 544, 600, 777, 988, 989, 990, 991, 992
```

## Boundary

MMD-003 does not:

- mutate Notion
- use Notion AI
- create Notion Custom Agents
- assign canonical `TRG-*` identities
- expand SCL or Lenhard decoder layers
- normalize Schattenarchiv or token/integrity material as routine work

## Next

Best next action:

```text
MMD-004 - Candidate Review and Canon Gate
```

MMD-004 should review the 53 candidates, split them into safe module lanes, and
decide which rows may become CAP trigger-module records.
