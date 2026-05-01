# Decision Log (RC01)

## Entry 2026-04-30-A

- Datum (UTC): 2026-04-30
- Charge-ID: RC01-BOOTSTRAP-A
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| B10/B11 Export-Arbeitskontext | offen | `B_EVIDENCE` | B | Inhalt ist strukturrelevant, aber noch nicht voll quellengehärtet für Kernintegration. | In Intake-Matrix als B führen und später selektiv promoten. |
| RC01 Governance/Runbook-Artefakte | offen | `C_COMPANION` | C | Operative Steuerdokumente, nicht Teil des argumentativen Hauptkerns. | Als Companion-/Prozessspur stabil halten. |
| Lockpoint + SHA256 | offen | `B_EVIDENCE` | B | Reproduzierbarkeitsanker mit hoher Verifikationsfunktion. | Bei jedem neuen Meilenstein fortschreiben. |

### Konflikte / Doppelstatus

- Keine inhaltlichen Widersprüche markiert; Status aktuell methodisch/prozessual.
- Doppelstatus-Risiko: Governance-Texte könnten fälschlich als Kernargument gelesen werden.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: nein
- Schreibdatum geprüft: teilklar
- Publikationsdatum geprüft: ja (Dokumentdatum)
- Verra/FerrAI-Stufe gesetzt: teilklar

### Freigabe für nächsten Schritt

- [x] Intake-Matrix aktualisiert
- [x] Promotion-Kandidaten extrahiert
- [x] Rückführungsnotiz erstellt
- [x] Delta-Upload vorbereitet


## Entry 2026-04-30-B

- Datum (UTC): 2026-04-30
- Charge-ID: RC01-BOOTSTRAP-B
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| IPERKA Runbook + Four-Step Plan | aktiv | `C_COMPANION` | C | Methodische Steuerdokumente; notwendig für Prozesskonsistenz, aber nicht als Primärargument im Kerntext. | Als Companion-Regelwerk weiterführen und bei jeder Charge referenzieren. |
| Decision/Intake Templates + aktive Logs | aktiv | `B_EVIDENCE` | B | Artefakte dokumentieren belastbar den Weg von Rohmaterial zu Kernkandidaten. | Bei jeder Charge Delta-Einträge ergänzen. |
| Prepublish/GitHub-Policy-Dokument | aktiv | `C_COMPANION` | C | Veröffentlichungsguideline mit Governance-Charakter statt inhaltlicher Kernthese. | Nur bei Upload-Policy-Änderung aktualisieren. |

### Konflikte / Doppelstatus

- Risiko: B-Evidence-Prozessdokumente könnten mit inhaltlichen Aussagen verwechselt werden.
- Maßnahme: Jede Promotion muss weiterhin separat in `promotion_candidates.md` begründet sein.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: nein
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: teilklar

### Freigabe für nächsten Schritt

- [x] Intake-Matrix aktualisiert
- [x] Promotion-Kandidaten überprüft
- [x] Rückführungsnotiz ergänzt
- [x] Delta-Upload vorbereitet

## Entry 2026-04-30-C

- Datum (UTC): 2026-04-30
- Charge-ID: RC01-BOOTSTRAP-C
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Full-Dump Container (`raw/exports/2026-04-30_batch_850k_raw.txt`) | neu | `B_EVIDENCE` | B | Rohmassenspeicher für spätere Auswertung, noch ohne finalen Payload. | Finalen 850k-Rawtext einfügen und SHA256 neu berechnen. |
| Raw-Export Readme + SHA256 | neu | `B_EVIDENCE` | B | Archiv- und Integritätslogik dokumentiert, keine Kerntext-Promotion. | Bei jeder Dump-Aktualisierung Prüfsumme aktualisieren. |

### Konflikte / Doppelstatus

- Container enthält aktuell Platzhalter statt finalem Vollinhalt.
- Promotion ist bis zur vollständigen Befüllung strikt gesperrt.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: nein
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Intake-Matrix aktualisiert
- [x] Promotion-Sperre dokumentiert
- [x] Rückführungsnotiz ergänzt
- [x] Delta-Upload vorbereitet

## Entry 2026-04-30-D

- Datum (UTC): 2026-04-30
- Charge-ID: RC01-BOOTSTRAP-D
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Befüllungsversion (`2026-04-30_batch_850k_raw_fuellversion.md`) | neu | `B_EVIDENCE` | B | Übergabefähige Befüllungsschablone für den Voll-Dump, ohne Rohdatenverlust durch Copy/Paste-Fehler. | Payload einfügen, Script ausführen, SHA erneuern. |
| Fill-Script (`fill_850k_raw.sh`) | neu | `C_COMPANION` | C | Technisches Hilfsartefakt zur reproduzierbaren Extraktion/Checksum-Bildung. | Nach Befüllung Commit mit neuem Hash erzeugen. |

### Konflikte / Doppelstatus

- Finaler 850k-Payload liegt noch nicht im Repository vor.
- Promotion bleibt gesperrt bis `filled=true` und SHA-Update erfolgt.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: nein
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Befüllungsschablone erstellt
- [x] Automationsskript bereitgestellt
- [x] Rückführungsnotiz ergänzt
- [x] Delta-Upload vorbereitet

## Entry 2026-05-01-E

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-PLAN-UPDATE-450
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Ausbauziel-Planänderung auf 450 Seiten | neu | `C_COMPANION` | C | Strategische Meilensteinsteuerung für den nächsten Gate-Punkt, ohne direkte Kerntext-Promotion. | Bei 450 Seiten neues Lockpoint-Artefakt erstellen. |

### Konflikte / Doppelstatus

- Keine inhaltlichen Konflikte; reine Planungs-/Governance-Änderung.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Planupdate dokumentiert
- [x] Gate-Label gesetzt (`RC01-GATE-450`)
- [x] Delta-Upload vorbereitet

## Entry 2026-05-01-F

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-PLAN-UPDATE-500
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Planänderung 450 -> 500 Seiten | neu | `C_COMPANION` | C | Materiallage rechtfertigt den größeren Ausbaukorridor vor der Verdichtung. | Gate-Label auf `RC01-GATE-500` umstellen und beim Erreichen Lockpoint setzen. |
| Materialprovenienz-Hinweis (95% eigen / <5% extern) | neu | `B_EVIDENCE` | B | Relevante Kontextangabe für spätere Quellenhärtung und Transparenz. | Bei Verdichtung explizit in Quellenstatus-Prüfung aufnehmen. |

### Konflikte / Doppelstatus

- Keine direkten Konflikte; Gate-Verschiebung ersetzt vorherigen 450-Gate-Plan.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] 500er-Plan dokumentiert
- [x] Gate-Label auf 500 umgestellt
- [x] Delta-Upload vorbereitet
