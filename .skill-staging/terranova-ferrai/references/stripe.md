# Stripe connector policy

Use Stripe as the source of truth for billing and commercial state.

## Default role

Stripe is strongest for:

- products and prices
- customers and subscriptions
- invoices, payment links, and balances
- revenue-facing operational questions

## Read-first behavior

Default to:

- search or retrieve exact objects first
- confirm IDs, currency, amount, and environment before recommending action
- summarize the current billing state before proposing any change

## Mutation rule

Treat Stripe as high-risk by default.

Only mutate Stripe when the user explicitly asks to:

- create or edit a customer
- create or change a product or price
- create or finalize an invoice
- create a subscription, refund, or payment surface

For any write, confirm the exact commercial object involved. Do not guess.

## Conflict rule

If any other system disagrees with Stripe about money, subscriptions, invoices,
or product pricing, Stripe wins and the discrepancy should be surfaced.
