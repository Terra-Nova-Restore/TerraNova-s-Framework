# CORE_GRID — Deterministic Core Grid (Spec v0.1)

Source: Notion master page `CORE_GRID — Deterministic Core Grid (Spec v0.1)`  
Status: real content import from Notion master  
Imported: 2026-04-28

## Ziel

Deterministische Rekonstruierbarkeit aller Inhalte durch explizite Trennung von:

- Objekt (`OID`)
- Zustand (`STATE`)
- Domäne (`DOMAIN`)
- Relation (`RELATION`)

## Axiome (nicht verhandelbar)

- Nichts überschreiben
- Alles versionieren
- Alles verknüpfen

## Achsen / Kontrollfelder

| Feld | Bedeutung |
|---|---|
| `OID` | eindeutige Objektidentität, persistent |
| `STATE` | `RAW` / `FIX` / `FINAL` / `SNAP` / `VAR` |
| `DOMAIN` | `GEN` / `SYS` / `MED` / `DIA` / `BUS` |
| `RELATION` | `ORIGIN` / `DERIVE` / `LINK` / `CLUSTER` |

## Naming-Schema

```text
[OID]__[DOMAIN]__[STATE]__[TIMESTAMP]__[HASH]
```

Beispiele:

```text
C001__GEN__RAW__2026-04__f92a.txt
C001__GEN__SNAP__2026-04__a77b.txt
C845__MED__FIX__2026-04__e31d.png
```

## Ordner-Index (ASCII)

```text
CORE_GRID
├─ GENESIS/
│  ├─ RAW/
│  ├─ SNAP/
│  └─ META/
├─ DOMAIN/
│  ├─ SYSTEM/
│  ├─ MEDIA/
│  ├─ DIALOG/
│  └─ BUSINESS/
├─ STATE/
│  ├─ RAW/
│  ├─ FIX/
│  ├─ FINAL/
│  ├─ SNAP/
│  └─ VAR/
├─ REL/
│  ├─ GRAPH.json
│  └─ CLUSTER.map
└─ ARCHIVE/
   └─ SHADOW_REF/
```

## Relationsgraph (Shape)

```json
{
  "C001": {
    "origin": null,
    "states": ["RAW", "SNAP"],
    "links": ["C845", "C902"],
    "cluster": "GENESIS_CORE",
    "tags": ["origin", "primary"]
  }
}
```

## Validierungslogik (K)

Zwingend:

- `OID` eindeutig
- `STATE`-Kette vollständig
- `RELATION >= 1`

Fehlerklassen:

| Fehlerklasse | Bedeutung |
|---|---|
| `ORPHAN` | keine Verknüpfung |
| `DUPLICATE` | redundante Instanzen ohne Bezug |
| `STATE_BREAK` | fehlender `RAW`-Ursprung |

Behandlung:

- automatisches Flagging
- Verschiebung nach `ARCHIVE/SHADOW_REF`

## Minimaler Workflow (R)

1. Neues Objekt entsteht immer als `STATE=RAW`.
2. Jede Änderung erzeugt neuen `STATE`, kein Replace.
3. Jede Einheit erhält sofort mindestens eine `RELATION`, mindestens `ORIGIN` oder `LINK`.
4. Jeder Import/Altbestand, der unklar ist, wird referenziert (`Shadow-Ref`), nicht gelöscht.

## Offene Entscheidungen (E)

- `OID`-Format: rein numerisch (`C001`) vs. domänenspezifisch (`G001`, `M001`, ...)
- `TIMESTAMP`-Granularität: `YYYY-MM` vs. `YYYYMMDD_HHMM`
- `HASH`: SHA256 kurz vs. full

## Boundary

This file mirrors the Notion master. It contains structural and operational schema only. Private trigger canon, internal VORTEX details, instance council internals, API/contract internals, GODFATHER_LOCK and restricted patent mappings are intentionally excluded.
