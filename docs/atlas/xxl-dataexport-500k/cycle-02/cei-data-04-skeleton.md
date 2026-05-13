# CEI-DATA-04 -- Data Note

Status: DRAFT / PAGE-SCAFFOLD
Cycle: 2
Boundary: aggregate-only / no raw dump
Zenodo Target: HOLD / no push
Target Parent: XXL DatenExport 500k -- Top-5 Quellenfund / Snapshotanalyse

## Purpose

CEI-DATA-04 is the data-note lane for the private `XXL_DatenExport_500_000Zeilen.zip`
corpus. It records safe metadata, non-claims, citation anchors, and release
gates without moving raw material into Notion, GitHub, or Zenodo.

## Corpus Anchor

| Field | Value |
| --- | --- |
| ZIP | `XXL_DatenExport_500_000Zeilen.zip` |
| TXT | `XXL_DatenExport_500_000Zeilen.txt` |
| ZIP SHA-256 | `4e804d279535d273b9363e0171200ca6462fee52fbb75bd5b3ed070d7fb42f81` |
| TXT SHA-256 | `06bc44cfda1226db6324e5261449b095b0be2bf124e9a5a416af5f3f1fc6df5d` |
| Lines | `553000` |
| Bytes | `30957838` (`30.96 MB`) |
| Characters | `30065300` |
| Cycle 1 PR | `https://github.com/Terra-Nova-Restore/TerraNova-s-Framework/pull/38` |
| Cycle 1 Merge SHA | `3d61a6f27ce08573c71b39f979853535793dad9f` |
| Safe Index Path | `docs/atlas/xxl-dataexport-500k/cycle-01/` |
| ORCID Anchor | `0009-0007-8033-3508` |

## Boundary

- No raw dump.
- No raw corpus excerpts.
- No inline chat export.
- No Zenodo push.
- No claim that the corpus is publicly reusable.
- No merge or phase transition without explicit Silvi-Go.

## Routing Notes

- CEI-DATA-04 is a data-note lane.
- CEI-DATA-05 remains a workspace index, trigger matrix, and companion reference.
- CEI-04 / CEI-04A / CEI-04B / CEI-04C remain the sensitive-review and public-gate lane.
- Corpus home remains `XXL DatenExport 500k -- Top-5 Quellenfund / Snapshotanalyse`
  plus CEI-00 / CEI-04-family references where appropriate.

## Data Note Fields To Fill

- Summary of aggregate-only corpus scope.
- Method note for how metrics and hashes were derived.
- Citation and license posture.
- Non-claims and known limitations.
- Cluster-frequency references after GPT Cycle 2 analysis.
- Trigger-matrix references from CEI-DATA-05.
- Risk-token aggregate notes without raw lines.
- Release-gate decision log for R-Phase 3-5.

## Zenodo Hold Gate

Zenodo remains on hold for this data note. A later release decision must be
recorded separately and must not be inferred from this scaffold.

## Phase Checklist

- [x] B / Codex: schema, metadata instance, and Notion skeleton drafted.
- [ ] C / FerrAI: create CEI-DATA-04 Notion page from this skeleton.
- [ ] A / GPT: fill data-note content after the Notion skeleton exists.
- [ ] R-Phase 3: data-note review.
- [ ] R-Phase 4: Zenodo release decision.
- [ ] R-Phase 5: final sync and closure.
