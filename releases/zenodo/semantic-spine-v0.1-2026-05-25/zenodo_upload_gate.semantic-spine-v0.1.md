# Zenodo Upload Gate: semantic-spine-v0.1

Status: explicit-GO gate
Source: semantic spine release package
Trace: generated 2026-05-25 by `scripts/build_semantic_spine_release.py`
Boundary: no external Zenodo action is authorized by this gate alone
Mode: SYNC / publication gate
GitHub sync state: package prepared in repository
Notion source awareness: public-safe GitHub synthesis; no raw Notion material in upload package

## Upload Preconditions

| Gate | State |
| --- | --- |
| Public release Markdown exists | ready |
| HTML artifact exists | ready |
| PDF artifact exists | generated when local browser renderer is available |
| Zenodo metadata JSON exists | ready for review |
| Raw Notion URLs / page IDs | blocked |
| Raw exports | blocked |
| Protected TNPX-01 draft details | blocked |
| External upload | requires explicit GO |

## Exact GO Wording

Use this only when the external upload should actually happen:

```text
GO Zenodo semantic-spine-v0.1 upload
```

## Upload Payload

- `docs/public/semantic_architecture_public_release_v0_1.md`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/semantic_architecture_public_release_v0_1.html`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/semantic_architecture_public_release_v0_1.pdf`
- `releases/zenodo/semantic-spine-v0.1-2026-05-25/zenodo_metadata.semantic-spine-v0.1.review.json`
