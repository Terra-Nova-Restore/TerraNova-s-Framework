# CEI-DATA-04 v0.3 Recommendation

Status: ACCEPTED_PENDING_REVIEW
Cycle: 3
Boundary: aggregate-only / no raw dump
Zenodo Target: HOLD / no push
Notion Page: https://www.notion.so/1cd470f1c9104e2d9b064e9a2830d0f4

## Purpose

This note records the Cycle 3 v0.3 recommendation for CEI-DATA-04 after the
Notion/FerrAI cross-check accepted the promoted canonical aggregate values.

It is a repository-side scaffold update only. It does not publish raw data, does
not include excerpts or context windows, does not update the public safe index,
and does not authorize a Zenodo action.

## Routing State

Source sequence:

1. GPT produced the v0.3 recommendation.
2. Notion/FerrAI persisted and reviewed the v0.3 material on CEI-DATA-04.
3. Notion/FerrAI cross-checked the promoted canonical values against the P1/P2/P3/P4 audit-trail persistence.
4. Codex records the accepted aggregate-only repository scaffold.

Routing baseline after this note:

```text
GPT -> Notion/FerrAI -> Codex
```

This avoids circular handoff wording when GPT is already the active drafting
instance.

## Cross-Check Result

Notion/FerrAI verdict: `ACCEPTED`

Cross-check result: `18 / 18 verified`

No drift was reported across the promoted canonical values:

| Layer | Phase | Values | Count |
| --- | --- | --- | --- |
| Token | P1 | `144`, `72` | `2` |
| Family | P2 | `6392`, `6174`, `449`, `0`, `0` | `5` |
| Risk | P3 | `3495`, `497`, `11`, `459`, `692` | `5` |
| Cluster | P4 | `28477`, `7174`, `2942`, `2672`, `1411`, `1355` | `6` |

The promoted model is a four-layer structure:

```text
Token -> Family -> Risk -> Cluster
```

The values above are promoted as canonical aggregate counts for the Cycle 3
v0.3 recommendation. The repository records the values and their phase slots;
semantic naming remains governed by the CEI-DATA-04 Notion review layer.

## Canonical Values

| ID | Layer | Phase | Value |
| --- | --- | --- | ---: |
| `p1_token_01` | Token | P1 | `144` |
| `p1_token_02` | Token | P1 | `72` |
| `p2_family_01` | Family | P2 | `6392` |
| `p2_family_02` | Family | P2 | `6174` |
| `p2_family_03` | Family | P2 | `449` |
| `p2_family_04` | Family | P2 | `0` |
| `p2_family_05` | Family | P2 | `0` |
| `p3_risk_01` | Risk | P3 | `3495` |
| `p3_risk_02` | Risk | P3 | `497` |
| `p3_risk_03` | Risk | P3 | `11` |
| `p3_risk_04` | Risk | P3 | `459` |
| `p3_risk_05` | Risk | P3 | `692` |
| `p4_cluster_01` | Cluster | P4 | `28477` |
| `p4_cluster_02` | Cluster | P4 | `7174` |
| `p4_cluster_03` | Cluster | P4 | `2942` |
| `p4_cluster_04` | Cluster | P4 | `2672` |
| `p4_cluster_05` | Cluster | P4 | `1411` |
| `p4_cluster_06` | Cluster | P4 | `1355` |

## Demoted / Non-Canonical Counts

The following trigger-model counts remain demoted until a later reconciliation
explicitly promotes them:

- `45`
- `56-62`
- `77`
- UI-scale estimate `~880`
- floor estimate `808`

They are not used as canonical v0.3 values in this scaffold.

## Boundary and Anti-Goal Frames

Active locks:

- No raw dump.
- No raw corpus excerpts.
- No context windows.
- No private material.
- No Zenodo push.
- No Zenodo draft, upload, DOI reservation, or publication decision.
- No safe-index mutation unless a later Silvi-Go opens that scope.
- No merge without explicit Silvi-Go.

This recommendation is aggregate-only. It is not a corpus-publication event and
does not change the Cycle 1 safe index.

## Follow-Up Backlog

These items are noted for later work and are not authorized by this note:

- Phase C pipeline hardening for reproducible metadata inputs and CI checks.
- Unicode-aware safe-index handling for Unicode hyphens such as `U+2011` and curly apostrophes such as `U+2019`.
- CEI-DATA-04 v0.3 narrative integration after P3-P5 are complete.

## Next Gate

Current state: `ACCEPTED_PENDING_CODEX_DISPATCH`

Codex action in this PR:

- add `cei-data-04-v0.3-recommendation.md`;
- add `metrics_v0.3.canonical.json`;
- keep the PR draft/unmerged until Silvi explicitly authorizes the next transition.

