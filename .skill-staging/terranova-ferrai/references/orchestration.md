# Cross-app orchestration

Use this reference when more than one connector is relevant.

## System-of-record selection

Pick the primary source before doing anything else:

- Notion: canon, workspace memory, plans, pages, databases
- GitHub: code truth, repo state, engineering tasks, PR history
- Google Drive: external documents, PDFs, Sheets, Slides
- Slack: conversational context, live coordination, draft messaging
- Linear: issue/project tracking if the work is intentionally tracked there
- Stripe: billing, products, invoices, subscriptions, commercial state

## Precedence rules

If sources disagree, use this order:

1. Stripe for billing/commercial truth
2. GitHub or Linear for execution-tracker truth, depending on the team's chosen tracker
3. Notion for canon, architecture, and intended process
4. Google Drive for artifact/document content
5. Slack for conversational context and intent clues

Do not silently merge contradictory states. Surface the conflict.

## Default multi-app flow

1. Clarify the object of work.
2. Identify the primary system.
3. Pull only the supporting evidence needed from secondary systems.
4. Summarize what is confirmed, what is inferred, and what is still missing.
5. Draft the next action.
6. Mutate only on explicit instruction.

## Output wording

When reporting cross-app findings, keep this shape:

- Source of record
- Supporting sources
- Confirmed state
- Open conflict or uncertainty
- Recommended next action

## Draft-before-send rule

Prefer drafts when a human-facing communication channel is involved:

- Slack -> draft before send
- GitHub -> summarize before opening/updating unless explicitly asked
- Linear -> summarize before create/update unless explicitly asked
- Stripe -> confirm exact customer/product/amount/currency before any mutation
