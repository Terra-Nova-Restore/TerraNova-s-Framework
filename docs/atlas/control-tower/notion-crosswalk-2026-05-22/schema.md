# Notion Crosswalk Register Schema

Status: STUDIO / schema candidate
Source: GPT H.4 synthesis, Home view aggregate metrics and existing public boundary policy
Trace: GH-XW-001
Boundary: Schema only. No live Notion rows, raw URLs or raw page IDs are included.
Mode: STUDIO
GitHub sync state: Prepared as repository-side schema documentation.
Notion source awareness: Field semantics must be reconciled with the live CAP registry before any Notion implementation.

## Field Set

| Field | Public-safe function |
| --- | --- |
| `raw_url` | Original URL in local-only raw register. Must not be committed publicly. |
| `clean_url` | URL without transient copy parameters. Internal review only if it still identifies a private page. |
| `page_id` | Canonical Notion page identifier. Public commits should use hash handles or aggregate counts instead. |
| `title_slug` | Reconstructed URL title slug. Public use only after sensitivity review. |
| `view_id` | Database/view identifier when a database view is referenced. Internal by default. |
| `anchor_id` | Block anchor below page level. Internal by default and only meaningful with parent context. |
| `duplicate_type` | Public-safe when expressed as counts or classes. |
| `cluster_key` | Public-safe only if it does not reveal private titles or protected page groups. |
| `risk_class` | Public-safe classification label. |
| `domain_class` | Public-safe domain label when expressed generically. |
| `sync_priority` | Public-safe priority label when not attached to private page details. |
| `sync_action` | Public-safe action label such as `index`, `review`, `hold` or `blocked`. |

## Risk Classes

| Class | Public repository handling |
| --- | --- |
| `public` | Candidate only; still requires review before reuse. |
| `internal` | Keep in Notion/local GitHub trace unless explicitly promoted. |
| `legal_ip` | Keep blocked until IP and redaction review. |
| `adult` | Keep separate and blocked from framework, sync and public paths by default. |
| `private` | Do not publish. |
| `protected` | Do not publish without explicit scoped review. |

## Priority Labels

| Priority | Meaning |
| --- | --- |
| `P1` | Review first; not a publication approval. |
| `P2` | Operational/internal relevance. |
| `P3` | Archive, provenance or historical trace. |
| `HOLD` | Export stop until manual review. |

## Domain Labels

Public-safe domain labels may include:

- `framework`
- `github_sync`
- `zenodo`
- `patent_ip`
- `token_dao`
- `compliance`
- `personal`
- `archive`
- `product`
- `unknown`

The domain label does not override the risk class. A page can be `framework`
and still be `internal`, `protected` or `legal_ip`.
