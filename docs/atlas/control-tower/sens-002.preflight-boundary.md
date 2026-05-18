# SENS-002 Preflight Boundary

`CAP-MOD-DRAFT-521 - Preflight` is admitted only as a protected
`L1-NAME-CLUSTER` row.

Allowed now:

- visible reference `521`
- working name `Preflight`
- Core System membership
- Protection Layer membership
- internal source-review marker that a Preflight lane exists

Blocked now:

- preflight automation
- protection execution behavior
- Schattenarchiv-depth behavior
- use of `777` as a semantic expansion source
- canonical `TRG-*` assignment
- public canon claim
- L2/L3/L4 elevation

Elevation requirement:

```text
direct Preflight/protection source
-> explicit separation from 777-depth behavior
-> redaction-safe allowed/blocked claims
-> SENS review pass
-> CAP canon admission update
```

Rationale: `MMD-007` found enough evidence for name and cluster, but not enough
evidence for execution semantics. The protection-layer overlap is useful, but
it is also the risk. It must not silently import Schattenarchiv-depth behavior
into a normal module record.
