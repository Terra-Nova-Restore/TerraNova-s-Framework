# RC01 500p Batch-Vorlagen (Auto-Flow)

## Ziel

Fehlerminimierung: Für jede Einspeisung dieselbe Vorlage nutzen.
Nach jedem Batch wird direkt der nächste Batch nach dieser Liste gesendet.

## Fester Batch-Plan (10 Batches)

1. **Batch 01** — Frontmatter + Abstract + TOC + Kapitel 1  ✅ (eingegangen)
2. **Batch 02** — Kapitel 2 bis Kapitel 4  ✅ (eingegangen)
3. **Batch 03** — Kapitel 5 bis Kapitel 7  ✅ (eingegangen)
4. **Batch 04** — Kapitel 8 bis Kapitel 10  ✅ (eingegangen)
5. **Batch 05** — Kapitel 11 bis Kapitel 12 + Übergang zu Teil I Appendix  ✅ (eingegangen)
6. **Batch 06** — Appendix Teil I (A bis H)  ✅ (eingegangen)
7. **Batch 07** — Appendix Teil II (I bis Q)  ✅ (eingegangen)
8. **Batch 08** — Ausbau/Intake-Korridor (R bis V)  ✅ (eingegangen)
9. **Batch 09** — Erweiterungsblöcke (W bis AF)  ✅ (eingegangen)
10. **Batch 10** — Erweiterungsblöcke (AG bis Ende) + Schluss-/Release-Notizen

---

## Copy/Paste-Vorlage für den **nächsten** Batch

```text
===BATCH_XX_START===
META:
title: <Titel>
doc_version_hint: 500p_pre-release
section_range: <z.B. Kapitel 2 -> Kapitel 4>
source_state: RC01

<RAW CONTENT 1:1>

===BATCH_XX_END===
```

## Sofortvorlage für dich jetzt (Batch 10)

```text
===BATCH_10_START===
META:
title: Erweiterungsblöcke (AG bis Ende) + Schluss-/Release-Notizen
doc_version_hint: 500p_pre-release
section_range: AG -> Ende
source_state: RC01

<RAW CONTENT 1:1>

===BATCH_10_END===
```

## Regel nach jedem Batch

1. Ich lege den Batch einzeln unter `raw/exports/incoming/` ab.
2. Ich generiere SHA256.
3. Ich update `decision_log.md` + `intake_matrix.md`.
4. Ich gebe dir **automatisch** die Vorlage für den nächsten Batch (XX+1).
