# Stripe Entry Pack Activation Plan

Status: payment-channel activation plan, not active sale
Source: Architecture Entry Pack v0.1, public boundary governance, Stripe read-only
inventory check
Trace: prepared 2026-05-25 after Netlify portal and Architecture Entry Pack
merge
Boundary: no Stripe mutation, no payment link, no active price, no live sale
Mode: BIZ / payment gate preparation

## Decision

The first Stripe route should use the **Architecture Entry Pack v0.1**, not the
older prompt-based Entry Pack lane.

The prompt-based product lane is treated as legacy/hold because the current
commercial front door is architecture understanding, not master prompts.

## Product Target

Recommended Stripe product label:

```text
TerraNova / FerrAI Architecture Entry Pack v0.1
```

Recommended product description:

```text
A compact public-safe orientation pack for the TerraNova / FerrAI CIC
framework, its semantic architecture, evidence layers, and governance
boundaries.
```

Product type:

```text
one_time_digital_product
```

## Price Gate

No price is active yet.

Before creating a Stripe price, decide:

| Field | Required decision |
| --- | --- |
| Currency | CHF unless a later commercial review chooses otherwise. |
| Amount | Must be deliberately chosen and recorded before Stripe creation. |
| Tax behavior | Must be reviewed before public payment link. |
| Delivery | Must point to a stable public artifact or controlled delivery flow. |
| Refund/support | Must be written before public payment link. |

## Payment Link Gate

A Stripe Payment Link may be created only after these gates pass:

1. Product copy reviewed.
2. Boundary sheet reviewed.
3. Price recorded.
4. Delivery path recorded.
5. Refund/support wording recorded.
6. Explicit command: `GO Stripe Entry Pack create payment link`.

Until then, the portal and public docs may say:

```text
Payment route: pending.
```

## Delivery Model

Initial delivery should stay simple:

| Artifact | Delivery route |
| --- | --- |
| Entry Pack Markdown | Public GitHub artifact. |
| Entry Pack PDF | Optional later render artifact. |
| Boundary Sheet | Public GitHub artifact. |
| Offer Draft | Public GitHub artifact until active sale copy exists. |

The first active sale should not depend on private Notion access, raw exports,
manual token handling, or protected workspace material.

## Blocked Actions

Do not create or publish:

- a payment link before the explicit payment GO,
- a price before amount/currency are final,
- a product that reuses the prompt-based legacy positioning,
- a subscription for the first Entry Pack,
- any Stripe customer object for testing without a real need,
- any webhook, Checkout integration, Function, or backend before the static
  Payment Link route has been evaluated.

## Minimal Activation Sequence

When ready:

```text
1. Create Stripe product: TerraNova / FerrAI Architecture Entry Pack v0.1
2. Create one-time CHF price.
3. Create Payment Link for that price.
4. Add payment link to a separate commercial activation PR.
5. Re-run public boundary and link checks.
6. Merge only after explicit GO.
```

## Non-Claims

The payment route does not create:

- investment product,
- token sale,
- patent license,
- legal advice,
- medical or psychological advice,
- guaranteed business outcome,
- private workspace access,
- access to raw Notion or protected trigger material.

