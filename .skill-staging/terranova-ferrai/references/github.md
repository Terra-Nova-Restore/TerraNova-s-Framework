# GitHub connector policy

Use GitHub for code truth, repo history, issues, pull requests, and engineering
execution context.

## Default role

GitHub is strongest for:

- repository structure and file history
- issue and PR status
- review comments and requested changes
- CI status and engineering audit trail

## Read-first behavior

Default to:

- inspect repo, issue, PR, and check state first
- summarize diffs and risks before changing anything
- compare GitHub tracker state against Notion or Linear when needed

## Mutation rule

Only mutate GitHub when the user explicitly asks to:

- open or edit an issue
- create or update a pull request
- push, label, assign, or close work
- respond in a review thread

Prefer a draft summary before a write when the intent is not fully explicit.

## Conflict rule

If GitHub conflicts with Notion:

- GitHub wins for code, PR, branch, and CI truth
- Notion wins for intended architecture or planning canon

If GitHub conflicts with Linear on execution tracking, follow the team tracker
of record and say which one you used.
