# CAP 0.5 - Public Entry and Product Ladder IPERKA

Status: BIZ/STUDIO bridge plan, repo-local, no external mutation
Date: 2026-06-03
Predecessor: `CAP 0.4 - Canon Admission IPERKA`
Primary input: Gumroad product ladder, Notion Marketplace template, GitHub public-safe traces

## Purpose

CAP 0.5 turns the current public product layer into an explicit operating
surface.

The system no longer lacks bounded artifacts. Three Gumroad products are live,
and the Notion template/public site is prepared while Marketplace directory
visibility is still pending. The remaining problem is not artifact creation. The
remaining problem is public routing, external comprehensibility, and source-safe
correlation between Notion, GitHub, Gumroad, Zenodo and local verification.

CAP 0.5 therefore defines how TerraNova presents its public entry layer without
flattening the internal system, over-claiming validation, or making Codex a
single point of failure.

## Operating Thesis

TerraNova is internally advanced enough to sustain a product ladder. It is not
yet externally simple enough to be understood without a controlled entry path.

The product layer must answer:

- What can an outsider buy or duplicate now?
- What source proves that the artifact exists?
- What is public-safe and what remains internal?
- Which system is source of record for each claim?
- What GitHub trace, if any, mirrors the public claim?
- What remains pending, deferred or human-gated?

If an outsider cannot understand the ladder in one controlled pass, the issue is
not lack of depth. It is routing debt.

## Deterministic Boundaries

Hard limits:

- no Notion Marketplace status claim without a concrete source or visible listing
- no Gumroad sales claim beyond verified public product pages
- no Stripe direct-sale activation; Stripe remains mirror/records-only until a
  separate explicit `GO Stripe ...` command exists
- no Zenodo publication or metadata mutation inside CAP 0.5
- no GitHub push, PR, merge or branch mutation inside this IPERKA
- no public mirroring of private Notion raw data, trigger tables, secrets,
  protected workspace mechanics or operator-sensitive material
- no claim that Codex is required for TerraNova to operate
- no claim that external validation exists before users, buyers, reviewers,
  citations or marketplace approval prove it

`/fff` may steer synthesis and prioritization. It cannot bypass product,
payment, marketplace, GitHub or publication gates.

## Product Layer Snapshot

Verified public product surfaces as of 2026-06-03:

| Surface | Status | Evidence |
| --- | --- | --- |
| Architecture Entry Pack v0.1 | Live Gumroad product, USD 19 | `https://silvanlenhard.gumroad.com/l/architecture-entry-pack-v0-1` returned `200 OK` |
| CIC Blueprint Pack v0.1 | Live Gumroad product, USD 49 | `https://silvanlenhard.gumroad.com/l/cic-blueprint-pack-v0-1` returned `200 OK` |
| CIC Implementation Workbook v0.1 | Live Gumroad product, USD 99 | `https://silvanlenhard.gumroad.com/l/cic-implementation-workbook-v0-1` returned `200 OK` |
| AI Workflow & Artifact Pipeline v0.1 | Notion template/public-site layer prepared | Template fetched; `https://artifact-pipeline.notion.site` returned `200 OK` |
| Notion Marketplace directory listing | Pending review/propagation | No concrete `notion.com/templates/...` listing verified yet |

## Source-of-Record Map

| Claim type | Source of record | Mirror / support |
| --- | --- | --- |
| Product live/reachable | Gumroad product URL | Notion BIZ logs, GitHub public bundle files |
| Product ladder strategy | Notion BIZ pages | GitHub docs/public bundle traces |
| Public-safe source artifacts | GitHub `docs/public/**` | Gumroad download payloads, Notion launch logs |
| Template structure | Notion template page | Public Notion site, Marketplace submission pack |
| Marketplace approval | Notion Marketplace / creator dashboard | Notion submission logs only until directory URL exists |
| Payment records | Gumroad / Stripe mirror | Stripe 3er-Mirror page, no direct payment links |
| Canon / AGU / RuleGraph | Notion source pages | GitHub mirror only after label-gate reconciliation |
| Publication evidence | Zenodo | GitHub release notes and `docs/references/zenodo.md` |

## I - Informieren

Known state:

| Signal | Value |
| --- | --- |
| Gumroad live products | 3 |
| Gumroad direct product URLs verified | 3 |
| Gumroad shop profile | Reachable, but HTML sections appear empty; direct URLs are stronger evidence |
| Notion template public site | Reachable |
| Notion Marketplace directory URL | Not yet verified |
| Open GitHub PRs in current triage | `#77`, `#73`, `#70` |
| PR `#77` | Draft portal-validator / registry review lane; `Validate Docs` is green |
| PR `#70` | Draft, stale Stripe / payment-plan lane |
| PR `#73` | Draft, placeholder-only portal CTA; blocked and not currently prioritized |
| Portal-validator / registry lane state | No longer local-only; open as draft PR `#77` and still partially present in the current worktree |
| External mutation count in this IPERKA | 0 |

Active supporting sources:

- `docs/public/entry_pack_bundle_v0_1/`
- `docs/public/blueprint_pack_v0_1/`
- `docs/public/implementation_workbook_v0_1/`
- `docs/governance/stripe_entry_pack_activation_plan.md`
- `docs/governance/source_of_record_policy.md`
- `docs/governance/public_boundary.md`
- Notion `BIZ-Launch Readiness - Codex-Pause-Fenster`
- Notion `Stripe 3er-Mirror - Source of Truth`
- Notion `Submit-Pack v0.1 - Konsolidiert (Gate 5)`
- Gumroad live product URLs listed above

Open pressure:

- The public product ladder exists but is not yet presented as one coherent
  outside-facing route.
- The portal CTA PR is placeholder-only and does not reflect the verified
  Gumroad ladder.
- Notion Marketplace state is pending and must not be treated as failed or live
  in the directory before evidence exists.
- The Gumroad shop profile does not expose product sections in static HTML, so
  direct product URLs remain the current hard proof.
- Codex is useful for local verification but must not become a system dependency.
- RuleGraph public mirror remains blocked until Canon Label Gate / R14-R19 label
  reconciliation is resolved.

## P - Planen

CAP 0.5 has seven workstreams.

| Workstream | Purpose | Output |
| --- | --- | --- |
| `CAP5-BOOT-001` | Create this product-entry IPERKA and freeze current product evidence. | This file and local memory update |
| `PROD-ROUTE-001` | Define one public ladder route from Entry Pack to Workbook plus Notion template. | Product ladder map and short outside-facing narrative |
| `PORTAL-CTA-001` | Replace placeholder portal logic with verified URL policy. | Local validator-backed patch; no merge/push without GO |
| `MARKET-001` | Track Notion Marketplace review/propagation without false status claims. | Pending-state checklist and future evidence slot |
| `GUMROAD-001` | Verify public metadata and boundary text for the three Gumroad products. | Read-only product audit summary |
| `CODEX-FALLBACK-001` | Define how TerraNova operates when Codex limits apply. | Local script/API/MCP fallback runbook |
| `CAP5-CLOSE-001` | Decide whether the public entry layer is ready for external review. | Close report and next gate |

Batch order:

1. `CAP5-BOOT-001`
2. `PROD-ROUTE-001`
3. `GUMROAD-001`
4. `MARKET-001`
5. `PORTAL-CTA-001`
6. `CODEX-FALLBACK-001`
7. `CAP5-CLOSE-001`

This order keeps verified product reality ahead of portal or automation work.

## E - Entscheiden

Decision: CAP 0.5 starts repo-local and product-evidence-first.

Reason:

```text
Three Gumroad products are live
-> Notion template/public site is prepared
-> Marketplace directory needs propagation/review time
-> GitHub PR view is narrower than the real public product layer
-> Codex is optional operator tooling, not the system core
-> therefore public routing must be stabilized before more expansion
```

Selected stance:

- treat Gumroad direct URLs as current hard external evidence
- treat Notion Marketplace as pending until a directory URL or approval proof
  exists
- treat GitHub as public-safe trace and validator layer, not as the whole
  product truth
- treat Codex as useful but replaceable local execution layer
- route outsiders through bounded artifacts before deep canon or RuleGraph

## R - Realisieren

### Batch CAP5-BOOT-001

Actions:

- create CAP 0.5 IPERKA locally
- record the three verified Gumroad product URLs
- record Notion Marketplace as pending review/propagation
- keep external mutation count at 0

### Batch PROD-ROUTE-001

Actions:

- define the product ladder:
  - Entry Pack = public architecture entry
  - Blueprint Pack = operating model / control logic layer
  - Implementation Workbook = self-guided application layer
  - Notion Template = external workflow container for non-TerraNova users
- write a one-screen outside-facing explanation
- separate "what is for buyers" from "what remains internal canon"

### Batch GUMROAD-001

Actions:

- verify each product URL returns `200 OK`
- record price, title, boundary / non-claims and intended buyer path
- flag any metadata drift, listing-copy leftovers or public wording issues
- do not perform purchases, refunds or product edits

### Batch MARKET-001

Actions:

- keep `artifact-pipeline.notion.site` as public-site evidence
- keep the template page as content evidence
- reserve a slot for the future Marketplace directory URL
- do not claim Marketplace publication until visible or explicitly confirmed

### Batch PORTAL-CTA-001

Actions:

- keep the public portal validator patch as useful
- block placeholder-only PR `#73`
- decide future portal behavior from verified product ladder, not from stale PR
  state
- prepare a local patch only; no push or PR mutation without explicit GO

### Batch CODEX-FALLBACK-001

Actions:

- define local scripts and API/MCP flows that keep TerraNova operable without
  Codex
- preserve Codex for repo diffs, tests and verification when limits allow
- avoid routing source-of-truth decisions through Codex memory alone

### Batch CAP5-CLOSE-001

Exit check:

```text
Can an outsider understand the product ladder, access a verified public entry,
and know what is included, excluded, pending and source-backed without Silvan
being present?
```

## K - Kontrollieren

Control metrics:

| Metric | Target |
| --- | --- |
| Gumroad live product URLs with `200 OK` | 3 of 3 |
| Products with visible price metadata | 3 of 3 |
| Products with boundary / non-claims text | 3 of 3 |
| Marketplace status over-claims | 0 |
| Portal placeholder CTA accepted as complete | 0 |
| External mutations without explicit GO | 0 |
| Public product claims without source URL | 0 |
| Codex dependency for core operation | 0 |
| Private/internal mechanics exposed in public route | 0 |

Every public-entry claim must answer:

```text
What is the artifact?
Where can it be reached?
What does it cost or what is its status?
What does it include?
What does it explicitly not include?
Which system proves the claim?
What remains pending?
```

## A - Auswerten

CAP 0.5 is complete when:

- the product ladder has one concise public route
- the three Gumroad products have a read-only metadata audit
- Notion Marketplace state is tracked as pending or verified with evidence
- portal CTA policy no longer accepts placeholder-only content
- Codex fallback operation is documented
- no external mutation was performed without explicit GO

Best next move after CAP 0.5 boot:

```text
PROD-ROUTE-001 - write the one-screen public ladder narrative and map it to the
three Gumroad URLs plus the Notion template pending state.
```
