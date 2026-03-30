# Slack connector policy

Use Slack for live collaboration context, response drafting, and channel-level
signal around TerraNova work.

## Default role

Slack is strongest for:

- current discussion context
- open questions waiting on a reply
- alignment drafts for channels or threads
- lightweight coordination summaries

## Read-first behavior

Default to:

- read channels or threads before drafting
- summarize the state of the conversation
- prepare a draft first
- keep tone aligned with the audience and urgency

## Mutation rule

Only send or schedule Slack messages when the user explicitly asks.

Prefer:

- draft over immediate send
- concise reply over long memo
- thread reply over channel blast when context already exists

## Safety rule

Do not treat Slack as authoritative for architecture, billing, or code state.
Use it as intent and coordination context, then verify against stronger systems.
