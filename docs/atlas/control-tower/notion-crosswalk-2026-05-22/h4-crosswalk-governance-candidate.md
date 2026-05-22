# H.4 Notion-Crosswalk, Linkregister und Export-Governance

Status: STUDIO / next-build candidate
Source: Home view aggregate export from 2026-05-22, GPT H.4 synthesis, Notion Zenodo page with Monographie Teil I-III, local RC01-v12 PDF/LaTeX inspection
Trace: GH-XW-001
Boundary: Candidate text only. No raw Notion URL list, raw page IDs, private titles or register rows are included.
Mode: STUDIO
GitHub sync state: Prepared as public-safe GitHub candidate for a future LaTeX build.
Notion source awareness: The live Notion workspace remains the source of record for page content, page status and internal review state.

## Placement Note

This module is designed to fit into the evidence apparatus after the current
`H.3` section of the monograph. In the published RC01-v12 PDF, `H.4-H.9` already
exist. Therefore this text is not a silent patch to the published Zenodo
snapshot. It is a next-build candidate that would require a controlled LaTeX
renumbering pass.

## Status, Function and Scope

This module documents the first normalized crosswalk run for the Notion Home
view of 2026-05-22. It is not an argumentative extension of the main text.
It is an apparatus layer inside the evidence, register and governance area of
the monograph.

Its function is to turn a visible Notion navigation and export surface into a
controlled, auditable and processable register format. The crosswalk does not
create a new primary claim about the FerrAI/TerraNova CIC system. It shifts the
focus from system interpretation to controlled addressability of the underlying
working corpus.

The core contribution is a reference grid between Notion, GitHub, Zenodo, local
working states, PDF versions and later public surfaces. The register makes the
corpus identifiable, clusterable and reviewable. It does not make it
automatically publishable.

## Corpus Relation

The Notion Zenodo page links internal monograph parts I-III and connects them to
the published Zenodo artifact. This establishes a distinction between published
snapshot, local comparison base, living workspace state and possible future
builds.

The crosswalk belongs to the appendix and evidence apparatus because it does not
add system doctrine. It structures the proof space itself. It connects existing
layers such as source register, chapter-to-source matrix, terminology sheet,
conflict list, claim ledger, material atlas and document inventory to a more
machine-readable and reviewable address layer.

## Purpose

The crosswalk supports four operations:

1. Identification: separating raw URLs, clean URLs, page identifiers, view
   parameters and block anchors.
2. Classification: separating public, internal, legal/IP-adjacent, private,
   protected and sensitive material.
3. Review routing: creating P1, P2, P3 and HOLD lanes without treating them as
   publication decisions.
4. Future mapping: preparing selective alignment between Notion elements,
   GitHub artifacts, Zenodo records, PDF versions and public surfaces.

Negative definition is equally important. The crosswalk is not a full sync, not
a scraping protocol, not a new publication version and not a replacement for the
claim/evidence apparatus. It is a pre-filter and control instrument.

## Persistence Layers

| Layer | Function | Crosswalk role |
| --- | --- | --- |
| Notion | Internal index and living system of record | Identify page-level and workspace-level references. |
| GitHub | Working state and technical trace | Store public-safe scripts, gates, summaries and release candidates. |
| Zenodo | Citable reference anchor | Bind published snapshots, DOI logic and evidence status. |
| PDF | Stable reading version | Preserve chapter and appendix logic. |
| Website / Public Surface | Public narrative | Receive only reviewed, redacted and released content. |

This separation prevents Notion visibility from being confused with GitHub
traceability or Zenodo evidence status.

## First Register Run

Aggregate metrics from the local raw export:

| Metric | Value |
| --- | ---: |
| Non-empty lines | 877 |
| Notion URLs found | 877 |
| Unique raw URLs | 864 |
| Unique Notion page IDs | 841 |
| Database/view URLs with `v=` | 93 |
| Block-anchor URLs with `#...` | 23 |
| Page IDs with multiple occurrences | 24 |
| Page IDs with multiple distinct raw URL forms | 11 |
| Page IDs with multiple distinct clean URL forms | 0 |
| Title groups with multiple page IDs | 48 |

These metrics show that the list is viable as a page-ID register, but not as a
flat page inventory. It contains page-level references, database views, block
anchors, repeated references, import variants and title-equal but ID-distinct
pages.

## Risk and Visibility Classes

The first classification is conservative. It is a review pre-sort, not a final
release approval.

| Class | Reading rule |
| --- | --- |
| `public` | Potentially public-compatible, still review-required. |
| `internal` | Internal working and context material. |
| `legal_ip` | Patent, governance, compliance or rights-chain adjacency. |
| `adult` | Separately handled sensitive side corpus. |
| `private` | Personal or identity-adjacent traces. |
| `protected` | IP, token, wallet, security or legal sensitive zone. |

The class `public` does not mean publication. `HOLD` does not mean deletion.
Both are routing signals.

## Priority and Gate Logic

| Priority | Meaning |
| --- | --- |
| `P1` | Review first; not approval. |
| `P2` | Operational or internal relevance without automatic public use. |
| `P3` | Archive, provenance or historical trace. |
| `HOLD` | Export stop until manual review. |

P1 candidates must be checked against the existing PDF, Zenodo metadata and
GitHub state before any public or citable use.

## Relation to Claim/Evidence

The crosswalk operates before the claim/evidence apparatus. It stabilizes the
objects that may later enter source registers, claim ledgers or chapter matrices.

The required sequence is:

1. Identify the Notion reference.
2. Determine its type: page, view, block anchor, import trace, archive item or
   public-surface candidate.
3. Assign risk and domain class.
4. Only then route it toward source, appendix, GitHub artifact, Zenodo-adjacent
   reference or public candidate.

This prevents raw workspace visibility from being mistaken for evidence status.

## Domain Logic

Domain labels describe technical or conceptual location without overriding risk:

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

A page can be highly relevant to the framework and still remain internal,
protected or legal/IP-adjacent.

## Work Artifacts

The broader internal workflow may produce:

- normalized raw register
- duplicate and multi-reference list
- cluster table
- public-candidate table
- HOLD review table
- summary report
- spreadsheet review workbook

In GitHub public-safe form, these are represented only by aggregate metrics,
schema, gate rules and reproducibility scripts unless a separate redaction pass
clears a specific artifact.

## Negative Rule for Future Builds

No automatic full sync may be derived from this register.

Future builds must obey:

- `private`, `protected`, `adult` and `legal_ip` stay blocked without manual
  review.
- Database views with `v=` are not page-level sources.
- Block anchors with `#` are interpreted only with parent-page context.
- Title-equal pages with different IDs are drift or variant cases.
- P1 candidates are checked against GitHub, Zenodo metadata and the existing
  PDF before promotion.
- A new Zenodo state requires an explicit release or metadata-refresh decision.

Register creation is not a publication event.

## Quality Review Path

The next review layers are:

1. Technical plausibility: URL parsing, page-ID extraction, view separation and
   block-anchor marking.
2. Semantic plausibility: title slug, cluster and domain review.
3. Risk review: conservative classification and HOLD handling.
4. Apparatus binding: alignment with source register, claim ledger, matrix,
   GitHub and Zenodo.
5. Redaction readiness: remove personal, operational, legal/IP or over-strong
   market claims before any public use.

## Minimal Follow-Up Process

1. Freeze the raw artifact locally.
2. Keep this GitHub package aggregate-only.
3. Review P1 candidates against PDF, Zenodo and GitHub.
4. Keep HOLD closed except for explicit single-case review.
5. Resolve dedupe and cluster cases before mapping.
6. Draft a sync runbook only for selected, reviewed pages.

## Status

The 2026-05-22 crosswalk run is a credible working state, not a final source
decision. Its value is controlled addressability. It allows the workspace to be
split into public framework candidates, technical sync paths, IP-sensitive
zones, private traces, archive material, product narratives and sensitive side
material without opening the raw corpus.

This module is strong enough to be treated as a next-build candidate for the
evidence apparatus. It remains open enough for later correction, additional
review columns, GitHub mapping, redaction decisions and Zenodo back-binding.
