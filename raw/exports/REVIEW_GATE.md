# Raw Export Review Gate

Status: required review checklist for public raw-export paths  
Scope: `raw/exports/`

Raw exports can contain private, volatile, patent-sensitive or context-heavy material. They must not be treated as public-safe just because they are technically exportable.

## Required classification

Before adding or promoting a raw-export file, assign one primary classification:

| Classification | Use when |
| --- | --- |
| `public-ok` | Reviewed and safe for the public repository. |
| `internal` | Useful, but should stay in a private/local working layer. |
| `redact-candidate` | Potentially useful after redaction. |
| `patent-sensitive` | Could affect IP, novelty, disclosure timing or claim strategy. |
| `private` | Contains private logs, personal content, access data or non-public system material. |
| `volatile` | Contains metrics, status, pricing, roadmap or time-sensitive claims. |

## Minimum checks

Each raw-export candidate should answer:

- Source: where did it come from?
- Date: when was it exported or generated?
- Scope: what system or document does it represent?
- Purpose: why does it need to be in GitHub?
- Sensitivity: does it contain private, token, wallet, patent, trigger or personal material?
- Status: is it canonical, reference, draft, placeholder or raw corpus?
- Redaction: what was removed or intentionally kept out?

## Commit rule

Do not commit raw exports directly to `main` unless they are already classified as `public-ok` or deliberately committed as a clearly marked placeholder.

For all uncertain material:

1. keep it local or private,
2. create a summary or manifest instead,
3. open a review issue,
4. promote only after classification.

## Placeholder rule

Placeholders must be explicit and must not pretend to be complete evidence.

Use wording such as:

- `placeholder`
- `manifest only`
- `source intentionally omitted`
- `redacted summary`
- `local/private source pack not committed`

## No-delete default

This gate does not instruct deletion. If a file is risky or unclear, prefer:

- move to private storage,
- replace with a redacted manifest,
- mark as `hold`,
- open a review issue.

Archive is safer than blind deletion.