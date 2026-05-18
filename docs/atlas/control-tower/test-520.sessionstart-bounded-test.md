# TEST-520 SessionStart Bounded Test

## Contract Under Test

```text
520 / SessionStart is an active internal core routing marker. It can mark the
opening of a work unit or session, load bounded context, and route to Preflight
through an internal session_opened guard.
```

## Simulated Input

```json
{
  "trigger": "520",
  "entrypoint": "/start",
  "prior_session_state": "none",
  "requested_action": "open_bounded_work_unit",
  "external_mutation_authorized": false,
  "notion_ai_credit_use_authorized": false
}
```

## Expected Bounded Output

```json
{
  "session_frame": "opened",
  "guard": "session_opened",
  "next_internal_route": "521 / Preflight",
  "external_mutation": false,
  "notion_ai_credits_used": 0,
  "module_execution": "none",
  "canon_level": "L2-ROUTING-MARKER"
}
```

## Result

`TEST-520` passes locally. The test confirms that `520` can be used as a
bounded CAP session-start marker and Preflight handoff guard. It does not admit
L3 module semantics and does not authorize execution of `init_all_modules()`.

## Remaining L3 Gate

Before L3, the system still needs:

- implementation contract for session state
- deterministic context-source list
- output contract for Preflight handoff
- explicit runtime test against the actual future implementation
- publication boundary review if any public wording is derived
