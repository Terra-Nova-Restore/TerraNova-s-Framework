# GitHub Prepublish Package (2026-04-30)

## Ziel

Dieses Dokument bündelt den **sofort veröffentlichbaren Stand** für GitHub, damit möglichst viel des aktuellen Arbeitsstands online gestellt werden kann, ohne die spätere Verdichtung zu blockieren.

## Enthaltene Kernartefakte (bereits im Repo)

1. `docs/dissertation/b10_window_export_excerpt_056_207.md`
   - B10/B11-Arbeitskontext
   - Zielraum-/Track-Logik
   - U.6/U.7-Arbeitsreihenfolge
2. `notes/rc01_lockpoint_2026-04-30_codex_gpt_347_seiten.md`
   - formaler Lockpoint
   - Rückführungsregel für weitere Commits
3. `notes/rc01_lockpoint_2026-04-30_codex_gpt_347_seiten.sha256`
   - SHA256-Anker für das PDF-Artefakt

## Veröffentlichungsempfehlung: „So viel wie möglich, aber kontrolliert"

### Direkt auf GitHub

- Markdown-/LaTeX-Quellen
- Intake-/Decision-/Rückführungsdokumente
- Lockpoints, Manifeste, Prüfsummen

### Nur referenzieren (nicht als Rohmasse ins Repo kippen)

- große Rohcontainer (mehrere 100 MB/GB)
- Audio-/Video-Rohmaterial
- massive ungefilterte Exporte

## Minimaler Online-Satz (ab sofort)

Für einen sofortigen und robusten Online-Stand sollten diese Dateien als „Milestone-Set RC01" bestehen bleiben:

- `docs/dissertation/b10_window_export_excerpt_056_207.md`
- `notes/rc01_lockpoint_2026-04-30_codex_gpt_347_seiten.md`
- `notes/rc01_lockpoint_2026-04-30_codex_gpt_347_seiten.sha256`
- `neuempfindung_gesamtdokument_compile (1).pdf` (optional im Repo; alternativ nur als extern referenziertes Artefakt)

## Nächster Uploadschritt (wenn Prism-Stand weiter wächst)

1. Neuen Lockpoint erzeugen (`RC01-LP-...` fortlaufend).
2. SHA256 für neues Zielartefakt ergänzen.
3. Nur Delta-Dokumente hochladen (nicht jedes Mal Voll-Rohkorpus).
4. Decision-Log kurz nachziehen (was neu ist, was Track A/B/C bleibt).

## Governance-Kurzregel

- Erst **Sichtbarkeit + Reproduzierbarkeit**, dann Verdichtung.
- Jeder größere Upload erhält:
  - Lockpoint-ID,
  - Artefaktbezug,
  - Prüfsumme,
  - Kurzentscheid zur Track-Zuordnung.
