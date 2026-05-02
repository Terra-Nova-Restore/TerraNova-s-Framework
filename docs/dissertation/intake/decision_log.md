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

## Entry 2026-05-01-G

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-TOC-REVIEW-CHECKPOINT
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| TOC/Abstract/Kapitel-1 Review-Checkpoint | neu | `C_COMPANION` | C | Struktursicherung vor weiterer Batch-Ingestion reduziert spätere Korrekturlast. | Übergabepaket (TOC+Abstract+Kap1) prüfen und Checkliste ausfüllen. |

### Konflikte / Doppelstatus

- Keine; reiner Struktur-Checkpoint.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] TOC-Checkpoint angelegt
- [x] Review-Output definiert
- [x] Delta-Upload vorbereitet

## Entry 2026-05-01-H

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-01-TOC-ABS-K1K2
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 01 (TOC+Abstract+Kapitel 1/2) | neu | `B_EVIDENCE` | B | Logikbasierter Erstbatch für Strukturreview und spätere Zusammenführung. | TOC-Checkpoint ausfüllen, dann Batch 02 aufnehmen. |

### Konflikte / Doppelstatus

- Transfer wurde als Rohtext abgelegt; strukturelle Qualität wird im TOC-Checkpoint validiert.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 02

## Entry 2026-05-01-I

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-01-490P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 01 (490p Frontmatter+Abstract+TOC+Kapitel 1) | neu | `B_EVIDENCE` | B | Neue Fassung mit erweitertem TOC/Appendix-Korridor und 500er-Nähe wurde als eigener Rohbatch gesichert. | TOC-Checkpoint gegen 490p-Version prüfen, dann Batch 02 aufnehmen. |

### Konflikte / Doppelstatus

- Parallelität zu früherem Batch-01-Stand (455p) vorhanden; beide Versionen bewusst getrennt archiviert.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 02

## Entry 2026-05-01-J

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-TEMPLATE-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Standardisierte 10er-Batchvorlage | neu | `C_COMPANION` | C | Fehlerreduktion und konsistente Einspeisung durch fixe Struktur und Kapitelgrenzen. | Batch 02 gemäß Vorlage einspeisen. |

### Konflikte / Doppelstatus

- Keine; reine Prozessstabilisierung.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] 10er-Plan fixiert
- [x] Batch-02-Vorlage bereitgestellt
- [x] Auto-Flow-Regel dokumentiert

## Entry 2026-05-01-K

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-02-K2K4-490P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 02 (Kapitel 2–4) | neu | `B_EVIDENCE` | B | Kapitelcluster für Korpuslage, Forschungsobjekt und Systemarchitektur als logikbasierter Folgebatch gesichert. | Batch 03 (Kapitel 5–7) einspeisen. |

### Konflikte / Doppelstatus

- Keine neuen Konflikte; Folgebatch im erwarteten 500p-Flow.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 03

## Entry 2026-05-01-L

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-03-K5K7-490P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 03 (Kapitel 5–7) | neu | `B_EVIDENCE` | B | Operativer Prozess-, Claim/Evidence- und Patentcluster als nächster Kernblock für 500p-Lauf gesichert. | Batch 04 (Kapitel 8–10) einspeisen. |

### Konflikte / Doppelstatus

- Keine neuen Konflikte; Batchfolge konsistent mit 10er-Plan.

### Datierung / Namensstufe

- Erlebnisdatum geprüft: n/a
- Schreibdatum geprüft: ja
- Publikationsdatum geprüft: ja
- Verra/FerrAI-Stufe gesetzt: n/a

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 04


## Entry 2026-05-01-M

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-04-K8K10-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 04 (Kapitel 8–10) | neu | `B_EVIDENCE` | B | Token-/Governance-/Meta-Verfassungsblock als nächster Kerncluster übernommen. | Batch 05 (Kapitel 11–12 + Übergang Appendix I) einspeisen. |

### Konflikte / Doppelstatus

- Keine neuen Konflikte; Reihenfolge folgt 10er-Batchplan.

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 05


## Entry 2026-05-01-N

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-05A-K11K12-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 05a (Kapitel 11–12 + Appendix-I-Übergang) | neu | `B_EVIDENCE` | B | Teilupload für Trigger-/Resilienz- und Syntheseblock sauber als Zwischenstand gesichert. | Batch 05b ergänzen und dann Batch 06 vorbereiten. |

### Konflikte / Doppelstatus

- Kein Konflikt; als Teilupload markiert (05a), Vollbatch noch offen.

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 05b


## Entry 2026-05-01-O

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-05B-K11K12-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 05b (Kapitel 11–12 + Appendix-I-Übergang) | neu | `B_EVIDENCE` | B | Zweiter Teilupload des Blocks als ergänzende Intake-Einheit gesichert (05a/05b). | Batch 06 (Appendix Teil I A-H) einspeisen. |

### Konflikte / Doppelstatus

- Kein Konflikt; 05a/05b als geteilter Vollblock dokumentiert.

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 06


## Entry 2026-05-01-P

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-METRICS-ZENODO-V6
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Zenodo Snapshot (v6) | neu | `C_CONTEXT` | C | Öffentliche Resonanzmetrik als datierter Kontextanker erfasst (81 Views / 43 Downloads). | Bei neuem Versionssprung erneut datiert sichern. |

### Konflikte / Doppelstatus

- Snapshot-Metrik ist zeitabhängig und nicht als kanonischer Endstand zu lesen.

### Freigabe für nächsten Schritt

- [x] Snapshot dokumentiert
- [x] Kontextanker abgelegt
- [x] Decision-Log aktualisiert


## Entry 2026-05-01-Q

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-06A-APP-I-AH-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 06a (Appendix I A-H, Teil 1) | neu | `B_EVIDENCE` | B | Korrigierter Startpunkt (Übergang Kapitel→Appendix) als eigener Teilupload sauber übernommen. | Batch 06b ergänzen, danach Batch 07 vorbereiten. |

### Konflikte / Doppelstatus

- Kein Konflikt; zweigeteilte Batch-Logik (06a/06b) explizit dokumentiert.

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 06b


## Entry 2026-05-01-R

- Datum (UTC): 2026-05-01
- Charge-ID: RC01-BATCH-06B-APP-I-AH-500P
- Lockpoint-Bezug: RC01-LP-2026-04-30-CODEXGPT347
- Bearbeiter: Codex

### Segment-Entscheide

| Segment | Vorstatus | Entscheidung | Ziel-Track | Begründung | Nächste Aktion |
|---|---|---|---|---|---|
| Batch 06b (Appendix I A-H, Teil 2) | neu | `B_EVIDENCE` | B | Zweiter Teil der Appendix-I-Inventarspur vollständig als 06b ergänzt. | Batch 07 (Appendix Teil II I-Q) einspeisen. |

### Konflikte / Doppelstatus

- Kein Konflikt; 06a/06b als zusammengehöriger Appendix-I-Block dokumentiert.

### Freigabe für nächsten Schritt

- [x] Batch einzeln abgelegt
- [x] Batch-SHA256 erzeugt
- [x] Intake aktualisiert
- [x] Bereit für Batch 07
