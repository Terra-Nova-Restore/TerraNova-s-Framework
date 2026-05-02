# Full Sync Terra Nova MCP Sequence

Status: captured architecture note

## Purpose

This note preserves the client-side Mermaid sequence diagram for the
`/full_sync_terra_nova_lovable_ferrai` flow. It covers read-only status checks,
Notion OAuth bootstrap, initial pull, recurring diff pulls, later writeback with
two-step confirmation, and deterministic reconciliation.

## Rendering Note

The source page renders this sequence diagram client-side with Mermaid.js v10+.
When switching to the Sequence tab, the diagram should be rendered again so
mobile browsers do not end up with an empty SVG after tab activation.

## Raw Mermaid

```mermaid
sequenceDiagram
  autonumber
  actor U as Benutzer (Silvi)
  participant UI as UI (ChatGPT/Notion)
  participant IN as Eingabe-Filter (Sicherheit)
  participant FSM as Trigger/FSM (FerrAI-Kern)
  participant MCP as MCP Client
  participant SRV as MCP Server (SSE Endpoint)
  participant AUTH as Notion OAuth
  participant N as Notion API
  participant SE as Sync Engine (Backend)
  participant DB as Canonical Store (DB)
  participant AUD as Audit + Savepoints
  participant OUT as Ausgabe-Filter (Moderation)

  U->>UI: /full_sync_terra_nova_lovable_ferrai
  UI->>IN: Benutzereingabe
  IN->>FSM: Validieren (Policy/Scope/Rate)
  FSM->>MCP: Toolcall sync.status()

  MCP->>SRV: POST /tools/sync.status (via SSE session)
  SRV->>SE: status(workspace/user)
  SE->>DB: read sync_state
  DB-->>SE: state (tokens?, cursor?, readOnly?)
  SE-->>SRV: status payload
  SRV-->>MCP: tool result
  MCP->>FSM: status data
  FSM->>OUT: Antwort entwerfe (keine Writes)
  OUT-->>UI: Status anzeige
  UI-->>U: "Ready / Needs OAuth / Cursor..."

  alt Tokens fehlen (erste Verbindung)
    FSM->>MCP: Toolcall auth.start()
    MCP->>SRV: auth.start()
    SRV->>AUTH: Redirect URL erstellen
    AUTH-->>SRV: auth_url + state
    SRV-->>MCP: auth_url
    MCP->>UI: Link anzeigen
    UI-->>U: Öffne OAuth Link

    U->>AUTH: Consent (Notion Workspace)
    AUTH-->>SRV: auth.callback(code,state)
    SRV->>SE: exchangeCode(code)
    SE->>AUTH: Token exchange
    AUTH-->>SE: access_token + refresh_token
    SE->>DB: store(encrypted tokens + workspace_id)
    SE->>AUD: log("OAuth connected")
    AUD-->>SE: ok
    SE-->>SRV: ok
    SRV-->>MCP: auth.ok
    MCP->>FSM: auth.ok
  end

  rect rgba(200, 200, 255, 0.25)
    note over FSM,SE: Phase A/B/C: Bootstrap + Schema-Mapping + Initial Pull (Read-only zuerst)
    FSM->>MCP: Toolcall sync.bootstrap(readOnly=true)
    MCP->>SRV: sync.bootstrap
    SRV->>SE: bootstrap(readOnly=true)

    SE->>N: List DBs / Query changes (initial)
    N-->>SE: Pages/DB schema + content
    SE->>SE: mapSchema -> Canonical Model + content_hash
    SE->>DB: upsert canonical records + cursor
    SE->>AUD: savepoint("bootstrap snapshot")
    AUD-->>SE: savepoint_id
    SE-->>SRV: bootstrap_done(cursor, savepoint_id)
    SRV-->>MCP: result
    MCP->>FSM: bootstrap_done
    FSM->>OUT: Summary + next steps
  end

  loop Phase D: Diff Loop (regelmässig / manuell)
    FSM->>MCP: Toolcall sync.pull(cursor)
    MCP->>SRV: sync.pull
    SRV->>SE: pull(cursor)

    SE->>N: Search changes since cursor
    N-->>SE: changed objects
    SE->>SE: diff -> patches
    SE->>DB: apply patches (idempotent)
    SE->>AUD: log("pull", counts, cursor_new)
    AUD-->>SE: ok
    SE-->>SRV: pull_done(cursor_new, stats)
    SRV-->>MCP: result
    MCP->>FSM: pull_done
    FSM->>OUT: Update anzeige
  end

  alt Writeback aktiv (spöter, nach Tests)
    note over U,SE: 2-Step Commit: erst Plan, denn bestätige
    FSM->>MCP: Toolcall sync.plan_push(changeset)
    MCP->>SRV: sync.plan_push
    SRV->>SE: plan_push(changeset)
    SE->>SE: validate scopes + policy + conflict check
    SE-->>SRV: plan_id + preview + risk_flags
    SRV-->>MCP: plan result
    MCP->>UI: Plan anzeigen (Preview)
    UI-->>U: "Bestätige?"

    U->>UI: confirm(plan_id)
    UI->>IN: confirm input
    IN->>FSM: ok
    FSM->>MCP: Toolcall sync.commit_push(plan_id)
    MCP->>SRV: sync.commit_push
    SRV->>SE: commit_push(plan_id)

    SE->>N: Write updates (patches)
    N-->>SE: write ok / errors
    SE->>AUD: savepoint("post-write snapshot")
    SE->>AUD: log("commit", results)
    AUD-->>SE: ok
    SE-->>SRV: commit_done
    SRV-->>MCP: commit_done
    MCP->>FSM: commit_done
    FSM->>OUT: Ergebnis + Konflikte (falls)
  else Konflikte / Reconciliation
    FSM->>MCP: Toolcall sync.reconcile(strategy="deterministic")
    MCP->>SRV: sync.reconcile
    SRV->>SE: reconcile(strategy)
    SE->>SE: resolve conflicts + record decisions
    SE->>DB: persist resolutions
    SE->>AUD: log("reconcile", decisions)
    SE-->>SRV: reconcile_done
    SRV-->>MCP: result
    MCP->>FSM: reconcile_done
    FSM->>OUT: Konfliktbericht
  end
```
