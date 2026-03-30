# Notion connector policy

Use Notion as the primary memory surface for TerraNova / FerrAI work.

## Default role

Notion is the system of record for:

- canon and framework pages
- workspace memory
- architecture and governance docs
- operational dashboards
- page and database structure

## Read-first behavior

Default to:

- search before asking for page URLs
- fetch the smallest useful set of pages or databases
- compare current page content before proposing edits
- summarize with page-aware provenance

## Mutation rule

Only mutate Notion when the user explicitly asks to:

- create or rewrite a page
- update database rows or schema
- move or rename workspace objects
- append meeting notes, decisions, or logs

If the request is ambiguous, draft the structure first.

## Output pattern

When reporting Notion findings, prefer:

- page or database used
- what is confirmed from Notion
- what still needs another source
- recommended next action

## TerraNova-specific note

If Notion and another system disagree on canon, architecture intent, or process,
Notion wins unless the conflict is about code state, billing state, or a clearly
newer execution tracker.
