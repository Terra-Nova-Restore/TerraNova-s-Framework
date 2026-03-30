# Linear connector policy

Use Linear for issue, project, and execution tracking when the team is actively
using it as an operational tracker.

## Default role

Linear is strongest for:

- issue status and ownership
- project milestones and cycles
- triage and prioritization
- planned work that is not yet represented in code

## Read-first behavior

Default to:

- search issues, projects, or docs first
- summarize status, blockers, and next steps
- reconcile with GitHub before claiming engineering completion

## Mutation rule

Only mutate Linear when the user explicitly asks to:

- create or update an issue
- change status, priority, or assignee
- create or update project artifacts

If the request touches both GitHub and Linear, prefer a coordinated draft before
cross-system mutation.

## Conflict rule

Linear can be the tracker of record for execution, but it does not override:

- GitHub for code truth
- Notion for canon and design intent
- Stripe for commercial truth
