# CAP-RT-001 Bedienungshandbuch

Dieses Handbuch ist fuer Silvan. Es beschreibt, wie der Control Tower im
Alltag benutzt wird, ohne Notion Custom Agents, ohne Massen-AI und ohne
unbeabsichtigte externe Mutation.

## Grundregel

Nie den ganzen Workspace auf einmal steuern.

Immer nur:

```plain text
eine Lane
-> eine Quelle
-> eine Entscheidung
-> eine kleine Aktion
-> ein Check
-> ein naechster Gate
```

## Schnellstart

Wenn du nicht weisst, wo du anfangen sollst:

1. Oeffne `batch-cap-rt-001.md`.
2. Waehle eine Dashboard-Lane aus `cap-rt-001.dashboard-lanes.csv`.
3. Pruefe die Quelle in `cap-rt-001.source-routing.csv`.
4. Pruefe die Grenzen in `cap-rt-001.guardrails.csv`.
5. Schreibe den naechsten Gate-Namen auf.

Wenn kein klarer Gate sichtbar ist, ist der naechste Gate:

```plain text
CAP-RT-002
```

## Welche Datei wofuer?

`cap-rt-001.runtime-contract.md`

- erklaert, was Runtime bedeutet.
- definiert die Gate-Typen.
- zeigt, wann Notion, GitHub oder Zenodo massgebend sind.

`cap-rt-001.dashboard-lanes.csv`

- zeigt die acht ersten Runtime-Lanes.
- sagt, welches System pro Lane fuehrt.
- zeigt, was standardmaessig blockiert ist.

`cap-rt-001.source-routing.csv`

- sagt, welche Quelle welche Wahrheit liefert.
- verhindert, dass GPT, alte Snapshots oder Notion-Mirrors als falsche
  Autoritaet verwendet werden.

`cap-rt-001.guardrails.csv`

- ist die Stoppliste.
- wenn ein Schritt dort blockiert ist, nicht improvisieren.

`cap-rt-001.action-queue.csv`

- ist die kleine To-do-Liste fuer die naechsten Runtime-Schritte.

## Arbeit mit Notion

Notion ist Workspace-Gedaechtnis und interner Systemzustand.

Erlaubt:

- Seiten manuell lesen.
- gezielt eine Seite zusammenfassen.
- eine Entscheidung in eine bestehende Kontrollseite eintragen, wenn der Gate
  das ausdruecklich erlaubt.
- CAP Registry als Status- und Routing-Oberflaeche verwenden.

Nicht erlaubt ohne neuen expliziten Gate:

- Seiten loeschen.
- Seiten verschieben.
- Datenbanken grossflaechig umbauen.
- Custom Agents verwenden.
- Autofill ueber grosse Datenbanken laufen lassen.
- alle 880 Seiten automatisch zusammenfassen lassen.

Guter Notion-AI-Prompt:

```plain text
Fasse nur diese Seite zusammen in:
Status, erlaubte Aussagen, blockierte Aussagen, offene Fragen, naechste Quelle.
```

## Arbeit mit GPT

GPT ist Synthesehilfe, nicht Source of Record.

Guter Startprompt:

```plain text
Du hilfst mit TerraNova/FerrAI Control Tower.
Sprich mit mir knapp, aber praezise.
Artefakte in Hochdeutsch/Englisch.
Keine Loeschungen. Keine rohen Notion-IDs. Keine Zenodo-Schreibaktionen.
Behandle Notion als internes Gedaechtnis, GitHub als Audit-Spur und Zenodo API
als oeffentliche Release-Wahrheit.
Arbeite nur an dieser einen Lane:
[LANE EINFUEGEN]
```

Gute GPT-Aufgaben:

- eine Notion-Seite in erlaubte/blockierte Claims trennen.
- aus Notizen eine Registry-Zeile entwerfen.
- eine Checkliste fuer einen Gate schreiben.
- eine Quelle gegen eine Behauptung pruefen.

Schlechte GPT-Aufgaben:

- den ganzen Workspace verstehen lassen.
- Trigger-Historie erfinden lassen.
- Zenodo-Publikationsentscheide delegieren.
- sensible Monographie-Bereiche zusammenfassen lassen.

## Arbeit mit GitHub Copilot

Copilot darf mechanisch helfen.

Geeignet:

- CSV-Zeile ergaenzen.
- Markdown-Struktur glätten.
- kleine Validator-Ergaenzung.
- Tippfehler und Formatierung.

Nicht geeignet:

- Canon-Level entscheiden.
- Sensitivitaet herunterstufen.
- Zenodo-Aktion empfehlen.
- PR mergen ohne Gate.

Vor jedem Commit:

```powershell
python -m py_compile scripts\cap_control_checks.py
python scripts\cap_control_checks.py --live-zenodo
git diff --check
rg -n "https://www\.notion\.so/[0-9a-f]|collection://[0-9a-f]" docs\atlas\control-tower scripts -g "*.md" -g "*.csv" -g "*.json" -g "*.py"
```

## Entscheidlogik

Wenn die Quelle unklar ist:

```plain text
READ
```

Wenn die Quelle klar ist, aber die Aktion unklar:

```plain text
PLAN
```

Wenn die Aktion klar ist, aber extern mutiert:

```plain text
APPLY nur nach explizitem GO
```

Wenn ein PR oder Gate abgeschlossen werden soll:

```plain text
CHECK -> DECIDE -> CLOSE
```

## Stoppsignale

Sofort stoppen, wenn:

- ein Schritt Loeschen oder Verschieben verlangt.
- rohe Notion-IDs in GitHub auftauchen.
- Zenodo Upload, DOI, Version oder Publish beruehrt wird.
- Teil II/III sensitives Material nach aussen gezogen wird.
- ein Tool "autonom" ueber den ganzen Workspace laufen soll.
- eine Behauptung keine Quelle hat.

## Praktischer Tagesablauf

Start:

```plain text
Was ist der aktive Gate?
Welche Lane?
Welche Quelle?
Was ist blockiert?
Was ist die kleinste naechste Aktion?
```

Ende:

```plain text
Was wurde geprueft?
Was wurde geaendert?
Welche Grenzen blieben aktiv?
Was ist der naechste Gate?
```

## Aktueller naechster Schritt

Nach `CAP-RT-001` ist der naechste sinnvolle Schritt:

```plain text
CAP-RT-002
```

Ziel von `CAP-RT-002`:

- erste sichtbare Runtime-Oberflaeche festlegen.
- entscheiden: Notion View Package, GitHub Markdown Dashboard oder lokaler
  Mini-Prototyp.
- keine Custom Agents und keine Notion-AI-Massenlaeufe.

