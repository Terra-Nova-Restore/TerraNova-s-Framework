# CHATGPT-XPORT-001 - ChatGPT Export Intake

Status: STUDIO / repo-local export intake
Source: Local ChatGPT/Codex export candidates, WORKSPACE-CORR-001, CAP Control Tower
Trace: CHATGPT-XPORT-001
Boundary: Intake metrics and hash ledger only. No raw prompts, messages, conversation titles, local paths, account data, third-party identities, secrets or unreviewed IP specifics are published by this batch.
Mode: STUDIO
GitHub sync state: Prepared locally; no commit, push or PR performed by this batch.
Notion source awareness: Notion remains the living workspace source of record; ChatGPT exports are the second correlation layer.

## Decision

`CHATGPT-XPORT-001` starts the second corpus layer after the Notion workspace
crosswalk.

The working order remains:

```text
Notion workspace corpus
-> ChatGPT/Codex export corpus
-> tokenomics and trigger module work
-> Metarotik and deep phenomenology publication tracks
```

## Intake Result

The first export intake found:

| Metric | Value |
| --- | ---: |
| Source families | 7 |
| Files | 174 |
| Conversation JSON files | 168 |
| Text/Markdown files | 6 |
| Total bytes | 13,095,583 |
| Scan characters | 16,326,635 |
| Message markers | 2,205 |
| Correlation axes | 10 |
| Review gates | 10 |

## Axis Counts

| Axis | Count |
| --- | ---: |
| ChatGPT/Codex export | 174 |
| Prism / Zenodo / LaTeX | 71 |
| Notion workspace | 61 |
| Mermaid / MMD | 60 |
| Patent / IP | 59 |
| Control Tower / CAP / CIC | 57 |
| GitHub / sync | 47 |
| Trigger | 46 |
| Tokenomics | 43 |
| Metarotik / phenomenology | 22 |

## Review Gates

`CHATGPT-XPORT-001` separates primary publication lanes from review gates.

This is important because one file can simultaneously belong to IP, tokenomics,
trigger and Metarotik. A single primary lane must not erase the other
correlations.

| Gate | Count |
| --- | ---: |
| evidence_apparatus_review | 71 |
| notion_correlation_review | 61 |
| mermaid_graph_review | 60 |
| ip_review | 59 |
| control_tower_review | 57 |
| sync_trace_review | 47 |
| trigger_source_review | 46 |
| biz_tokenomics_review | 43 |
| phenomenology_metarotik_review | 22 |
| chat_export_index_review | 100 |

## Implemented Files

| File | Role |
| --- | --- |
| `chatgpt-xport-001.intake-rules.md` | Human-readable export intake and publication rules. |
| `chatgpt-xport-001.source-families.csv` | Public-safe source-family hash ledger without paths. |
| `chatgpt-xport-001.file-ledger.csv` | Public-safe per-file hash and axis ledger without paths or titles. |
| `chatgpt-xport-001.axis-counts.csv` | Aggregate count per correlation axis. |
| `chatgpt-xport-001.file-type-counts.csv` | Aggregate file-type count. |
| `chatgpt-xport-001.publication-lane-counts.csv` | Primary publication-lane count. |
| `chatgpt-xport-001.review-gate-counts.csv` | Non-exclusive review-gate counts. |
| `chatgpt-xport-001.review-summary.json` | Machine-readable summary. |
| `causal-log.chatgpt-xport-001-2026-05-22.json` | Causal trace. |
| `scripts/build_chatgpt_export_intake.py` | Reproducible local analysis script. |

## Next

Best next action: `CHATGPT-XPORT-002`.

Goal: deduplicate equivalent text/Markdown source families, then select a
small review set for tokenomics and trigger source mapping.
