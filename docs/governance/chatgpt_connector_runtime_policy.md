# ChatGPT Connector Runtime Policy

Status: BIZ / Public governance note
Source: Observed ChatGPT interaction plus OpenAI connector/app documentation.
Trace: TerraNova GitHub governance layer; discussion captured in Codex session on 2026-05-25.
Boundary: Public-facing operating policy only; not a claim of unrestricted access or permanent memory.
Mode: BIZ
GitHub sync state: tracked in this repository.
Notion source awareness: required when Notion is used as source of record.

## Purpose

This note records the operating distinction between automatic/synced connector
use and manual connector invocation in normal ChatGPT interactions.

It prevents two opposite errors:

- treating invisible UI state as proof that no source access happened
- treating automatic source access as unlimited or magical access

## Core Observation

In normal ChatGPT use, the visible UI state and the model runtime/source state
can diverge.

The public-safe rule is:

> A connector or app may be unavailable in the visible UI selection surface and
> still be available to the active runtime through synced data, project context,
> app/tool state, file context or previously enabled workspace configuration.

This must not be overstated. The correct claim is not "ChatGPT can always access
everything." The correct claim is:

> When a connector/app, synced source or file context is available to the active
> ChatGPT runtime, ChatGPT may use it even if the user did not manually select a
> visible connector in that prompt.

## Operating Modes

| Mode | Behavior | Strength | Boundary |
| --- | --- | --- | --- |
| Automatic / synced source use | ChatGPT can decide to reference indexed or synced data when it is relevant. | Broad, fast and sometimes surprising. | Less visible; must be checked before BIZ or publication use. |
| Manual connector invocation | The user explicitly selects or mentions a connector/app. | Controlled, targeted and easier to audit. | Can be narrower than automatic retrieval. |
| Deep research / multi-source pass | ChatGPT is asked to analyze across multiple sources with citations. | More systematic and citation-heavy. | Slower and still scope-limited. |
| No internal search | The user tells ChatGPT not to search internal sources. | Useful for reasoning-only or memory-only work. | Depends on the model respecting the current instruction and tool policy. |

## Manual Is Not Always Stronger

Manual activation is not automatically the strongest mode.

Automatic or synced retrieval can be broader because the model may combine
memory, project context, indexed sources and available app/tool state without a
single visible manual source selection.

Manual connector invocation is stronger for audit and control because it makes
the intended source route explicit.

Therefore:

- automatic/synced = broader, opportunistic, less visible
- manual = narrower, explicit, easier to review
- deep research = broader and more formal, but slower
- no-internal-search = explicit negative gate

## TerraNova / Equilibrium Rule

For TerraNova work, apply this source-state split:

| Layer | Meaning |
| --- | --- |
| UI state | What the user sees as selected, active or inactive in the ChatGPT UI. |
| Runtime state | What tools, apps, synced sources or file context are actually available to the model. |
| Source result | What files, pages, issues, commits or citations the response actually used. |
| Claim status | Whether a statement is memory, live/source-backed, inferred, or unresolved. |

The Equilibrium-compatible rule is:

> Do not infer "no connection" from missing visible connector activation. Treat
> it as a UI-state observation until runtime/source evidence confirms or denies
> access.

## Public Claim Boundary

Allowed public wording:

- "ChatGPT may use synced or connected sources automatically when available."
- "Manual connector selection improves control and auditability."
- "A visible UI connector state is not always the same as runtime source state."
- "Source-backed answers still need scope labels: targeted search, not full crawl."

Avoid public wording:

- "ChatGPT has unrestricted access."
- "The system magically discovered the source."
- "No visible connector means no source access."
- "A source-backed answer proves full workspace completeness."

## Source-of-Record Routing

For the current TerraNova stack:

- Notion remains the living source of record for rules, workspace memory, canon and unresolved operating decisions.
- GitHub remains the technical mirror for public-safe docs, diffs, issues, PRs, commits and CI/audit trace.
- ChatGPT is the operational reasoning and source-comparison surface.
- Codex/GitHub PR work remains the implementation and validation surface.

## Practical Prompt Rules

Use these only when precision matters:

```text
Use available synced/internal sources if relevant, but label memory vs live/source-backed vs inference.
```

```text
Use GitHub and Notion if available. Return the files/pages/IDs you actually used.
```

```text
Do not search internally. Answer only from this chat and general reasoning.
```

## External References

- OpenAI Help: Apps / connectors in ChatGPT: https://help.openai.com/en/articles/11487775/
- OpenAI Help: ChatGPT apps with sync: https://help.openai.com/en/articles/10847137-chatgpt-synced-con
