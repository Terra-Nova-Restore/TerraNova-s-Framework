# Canon Admission Rulebook

Status: CAP 0.4 rulebook, repo-local
Date: 2026-05-17
Scope: TerraNova CAP canon admission, source governance and elevation control

## Core Rule

Canon is admitted, not assumed.

A claim may enter canon only when its source tier, allowed level, blocked claims and downgrade rule are visible. If a claim is useful but incomplete, it stays as Candidate, Draft, Routing Marker or Sensitivity Hold.

## Admission Fields

| Field | Meaning |
| --- | --- |
| `Claim` | The exact statement proposed for canon. |
| `Object` | The module, trigger reference, page, registry row or document the claim concerns. |
| `Source Tier` | The strongest source tier currently supporting the claim. |
| `Canon Level` | The highest level allowed now: L0 to L4. |
| `Decision` | Admit, Hold, Downgrade, Block, or Queue. |
| `Allowed Claims` | What may be stated now. |
| `Blocked Claims` | What must not be stated yet. |
| `Next Source Action` | What must be found, curated or tested before elevation. |
| `Downgrade Rule` | Condition that lowers or removes the claim. |
| `Sensitivity Gate` | Whether SENS review is required before elevation. |

## Claim States

| State | Meaning | Registry Behavior |
| --- | --- | --- |
| `Draft` | Locally useful but not admitted. | Keep out of public canon; may be linked as working material. |
| `Candidate` | Source-supported enough for review. | Registry row may exist; no execution/public claim. |
| `Admitted L0` | Anchor exists. | ID/object can be referenced internally. |
| `Admitted L1` | Name and cluster are supported. | Internal registry metadata may use the name. |
| `Admitted L2` | Routing marker is supported. | CAP may route work through it. |
| `Admitted L3` | Module semantics are supported. | Internal canon may describe behavior. |
| `Admitted L4` | Execution or public canon is supported. | Can drive tested rules or public-facing material. |
| `Sensitivity Hold` | Source exists but protected. | No elevation until SENS review. |
| `Blocked` | Claim is unsafe or unsupported. | Keep as explicit blocked claim. |

## Source Precedence

When sources conflict, use this precedence:

1. Published/reference anchor with stable citation.
2. Reviewed repo-local governance artifact.
3. Live Notion system-of-record page or database row.
4. Extracted Mermaid/Atlas graph with parser trace.
5. Trigger/gap ledger or source complement.
6. Raw export or private snapshot.
7. Session directive.
8. Assistant inference.

Session directives authorize work. They do not create source truth.

## Admission Tests

Before admitting a claim, all six tests must be answered:

1. What exactly is the claim?
2. Which exact source supports it?
3. What is the strongest source tier?
4. What level is allowed now?
5. What is explicitly blocked?
6. What would downgrade or reverse the claim?

If one answer is missing, the claim stays below the requested level.

## Elevation Rules

| From | To | Required Evidence |
| --- | --- | --- |
| Draft | L0 | Reviewed source shows the anchor exists and no sensitivity block applies. |
| L0 | L1 | Source supports name, cluster or basic role. |
| L1 | L2 | Guard, relation or bounded routing context exists. |
| L2 | L3 | Direct primary definition plus corroboration and blocked claims. |
| L3 | L4 | Test case, SENS clearance, Equilibrium check and publication boundary. |

## Downgrade Rules

Downgrade a claim when:

- a higher-precedence source contradicts it
- the source tier was misclassified
- a sensitivity boundary was missed
- the claim included execution behavior without test support
- public wording exceeds internal evidence
- the source was raw/session-only and treated as reviewed

Downgrade is not failure. It is normal canon maintenance.

## Sensitivity Rules

The following lanes require SENS review before L3 or L4:

- Schattenarchiv-depth material
- private workspace exports
- token, wallet, commercial or financial material
- integrity/security trigger suites
- patent/IP or publication boundary material
- raw chat/session material involving private context

Protected material may still create an internal L0/L1 anchor if the anchor itself is safe and redacted.

## Current CAP 0.4 Decision

The five MMD-007 module drafts stay bounded:

| Reference | Allowed Now | Blocked |
| --- | --- | --- |
| `516` | L2 internal routing marker. | AutoFlow sibling semantics, execution, public trigger canon. |
| `520` | L2 internal routing marker confirmed by `SOURCE-520` and `TEST-520`; live Notion source tier is now T2. | L3 semantics, `init_all_modules` execution, external mutation, autonomous session control, public canon. |
| `521` | L2 protected internal routing marker after `SOURCE-521`; live Notion update applied on 2026-05-18. | L3 semantics, protection execution, Schattenarchiv-depth behavior, preflight automation, public canon. |
| `540` | L2 internal routing marker. | Proof finality, metric finality, public scientific claim. |
| `544` | L2 internal routing marker. | Full workspace sync claim, automatic sync, public canon. |

## Notion Rule

Notion may receive canon fields only through an explicit mutation package and explicit GO.

Until then, CAP 0.4 is the local admission source, and the live registry remains the operational dashboard rather than the full canon authority.
