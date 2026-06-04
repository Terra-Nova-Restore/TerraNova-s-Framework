# Operating Model — Blueprint Pack v0.1

Status: public-safe operating model draft  
Boundary: no private workspace export

## Operating Stack

The public operating model separates roles instead of merging everything into one black box.

```text
Notion -> GitHub -> Zenodo -> Public Portal -> Gumroad / Stripe
```

| Layer | Function |
| --- | --- |
| Notion | Living internal source layer, planning, rules, logs and state. |
| GitHub | Public working state, pull requests, traceable diffs and documentation mirrors. |
| Zenodo | Citable proof state with DOI, metadata and archive reference. |
| Public portal | External navigation surface for selected public-safe artifacts. |
| Gumroad | First commercial delivery wrapper for digital documentation products. |
| Stripe | Optional secondary payment infrastructure, not the default public route in this pack. |

## Why Separation Matters

The system becomes easier to trust when each layer has a bounded role.

Notion is not dumped raw into public. GitHub is not treated as the living workspace. Zenodo is not used as a scratchpad. Gumroad is not treated as the architecture itself.

## Core Movement

```text
conversation -> decision -> document -> pull request -> merge -> release or product bundle
```

This movement is the important part. It creates reviewable artifacts instead of relying on memory.

## Gate Types

| Gate | Meaning |
| --- | --- |
| Boundary gate | Checks what must stay private or protected. |
| Source gate | Checks which layer is allowed to carry the claim. |
| Write gate | Requires explicit permission before external mutation. |
| Product gate | Checks buyer expectation, price, delivery and non-claims. |
| Release gate | Checks DOI, version, checksum and publication readiness. |

## Buyer Gain

A reader can use this operating model as a reference pattern for designing their own source-aware AI workflow without copying private TerraNova material.
