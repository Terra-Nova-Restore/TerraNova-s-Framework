# SOURCE-520 Primary Source Pass

## Result

`CAP-MOD-DRAFT-520 - SessionStart` is locally confirmed as
`L2-ROUTING-MARKER` with strongest source tier upgraded to
`T2 Live Notion System Record`.

The pass does not assign a canonical `TRG-*` ID and does not admit L3 module
semantics. It confirms only the bounded internal routing role for session start
and prepares a test gate for any future L3 move.

## Source Interpretation

The decisive source is the active Notion trigger system table. It maps `520` to
the active `/start` entrypoint, marks it as `core`, and links it to the Terra
Nova Native trigger module page.

The supporting module page defines `520 SessionStart` as an initialization
module with sub-components such as Nullpunkt, Echo Null, Systemstart and
Kognitiv Punkt Null. Its JSON export names `SessionStart`, `id: 520` and
`state: initialization`. That page is explicitly marked as specification
material rather than the master, so its `init_all_modules()` action is not
admitted as executable canon.

The Notion system handbook supports the active action surface by listing `520`
or `/start` as `SessionStart` and routing it toward preflight, tacho and context
loading. Older trigger index and architecture pages corroborate the simple
mapping: `520` is SessionStart and each work unit begins there.

Repo-local Atlas and MMD outputs independently preserve the same shape: the core
system band `520-530` contains SessionStart, Preflight, Sync and Health; the
visual guard bridge routes `T520` toward `T521` only through a bounded
`session_opened` relation.

## Canon Decision

Allowed canon wording:

```text
520 / SessionStart is an active internal core routing marker. It can mark the
opening of a work unit or session, load bounded context, and route to Preflight
through an internal session_opened guard.
```

Blocked wording:

```text
520 autonomously controls sessions.
520 executes init_all_modules().
520 grants external mutation permission.
520 consumes Notion AI credits or starts Notion Custom Agents.
520 is a canonical historical TRG assignment.
520 is public-facing trigger canon.
```

## Elevation Boundary

L2 is supported because the source set provides:

- active `/start` entrypoint
- core role
- SessionStart name mapping
- initialization/root-state language
- start-of-work-unit support
- bounded handoff toward Preflight

L3 is still blocked because the source set does not yet provide:

- reviewed implementation contract
- bounded test case for neutral session start
- explicit non-mutation runtime behavior
- clear context-loading output contract
- publication boundary

## Backpropagation

`MMD-007` already held `520` at L2. `SOURCE-520` does not change the level; it
raises the local source basis from graph/Atlas support to live Notion T2 support.
`TEST-520` passed all five bounded gates locally, and SOURCE-520 was applied to
the live Notion registry on 2026-05-18 after the explicit command
`GO Notion SOURCE-520`.
