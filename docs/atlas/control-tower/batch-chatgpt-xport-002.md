# CHATGPT-XPORT-002 - Dedupe and Review Samples

Status: STUDIO / repo-local correlation hardening
Source: CHATGPT-XPORT-001 public-safe ledgers
Trace: CHATGPT-XPORT-002
Boundary: Dedupe families, duplicate hash groups and review samples only. No raw prompts, messages, titles, local paths, conversation IDs, account data or third-party identities are published.
Mode: STUDIO
GitHub sync state: Prepared locally by script; no push or PR performed by this batch.
Notion source awareness: Notion remains the primary workspace corpus; ChatGPT exports stay a second correlation layer.

## Decision

CHATGPT-XPORT-002 keeps correlation and removes only obvious duplicate surfaces.

Equivalent TXT/Markdown mirrors remain visible as aliases instead of being deleted from the evidence corridor.
Repeated file hashes are grouped before trigger/tokenomics review, so the next pass does not re-read the same content twice.

## Dedupe Result

- Raw source families: `7`
- Canonical source families after hash collapse: `5`
- Collapsed alias source copies: `2`
- Unique file hashes: `155`
- Duplicate hash groups: `19`
- Duplicate file rows removed from repeat-review: `19`

## Alias Families

| Canonical | Aliases | Hash |
| --- | --- | --- |
| `xport-src-002` | `xport-src-003` | `f34ea7e20b1fb1629ced0e00b06d3f7b6871988d04ebcd6eab91935c260ef000` |
| `xport-src-004` | `xport-src-005` | `19285eff50809de5f30c871676cfb9a6384e743f47e084db0d08b2906bbf6e7a` |

## Review Corridor

- `tokenomics_only`: 3
- `tokenomics_trigger_shared`: 6
- `trigger_only`: 3

| Sample | Focus | File | Axes | Markers | Copies |
| --- | --- | --- | ---: | ---: | ---: |
| `xport2-sample-001` | `tokenomics_trigger_shared` | `xport-src-001-file-0079` | 10 | 976 | 1 |
| `xport2-sample-002` | `tokenomics_trigger_shared` | `xport-src-001-file-0091` | 10 | 310 | 1 |
| `xport2-sample-003` | `tokenomics_trigger_shared` | `xport-src-001-file-0054` | 10 | 90 | 1 |
| `xport2-sample-004` | `tokenomics_trigger_shared` | `xport-src-001-file-0093` | 10 | 84 | 1 |
| `xport2-sample-005` | `tokenomics_trigger_shared` | `xport-src-001-file-0121` | 10 | 30 | 2 |
| `xport2-sample-006` | `tokenomics_trigger_shared` | `xport-src-001-file-0057` | 10 | 24 | 1 |
| `xport2-sample-007` | `tokenomics_only` | `xport-src-001-file-0001` | 9 | 12 | 1 |
| `xport2-sample-008` | `tokenomics_only` | `xport-src-001-file-0014` | 8 | 48 | 1 |
| `xport2-sample-009` | `tokenomics_only` | `xport-src-001-file-0020` | 8 | 6 | 1 |
| `xport2-sample-010` | `trigger_only` | `xport-src-001-file-0053` | 8 | 0 | 1 |
| `xport2-sample-011` | `trigger_only` | `xport-src-001-file-0015` | 7 | 18 | 1 |
| `xport2-sample-012` | `trigger_only` | `xport-src-001-file-0127` | 6 | 76 | 2 |

## Next

Best next action: `TRIGGER-MAP-001`.

Goal: use the selected sample corridor to start trigger/module and tokenomics source mapping without breaking the correlation chain.