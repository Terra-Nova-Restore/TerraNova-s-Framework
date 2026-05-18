# Home-Ansichten Snapshot - 2026-05-11

Status: sensitive local snapshot, indexed as CAP reference  
Reviewed: 2026-05-17  
Source file: `C:\Users\Silvan\Desktop\[Home-Ansichten](httpswww.notion.so.txt`

## Role In CAP 0.1.0

This file is not the current Notion truth. It is a local support snapshot for the CAP 0.1.0 registry and the `808 export_hard_count` layer from `CEI-DATA-05`.

The snapshot is useful for scope control because it exposes the workspace scale without claiming that every page is current, canonical, or safe to publish.

## Measured Facts

| Measure | Value |
| --- | ---: |
| File last write time | 2026-05-11 05:43:22 |
| File size | 108362 bytes |
| Lines | 1746 |
| Words | 3856 |
| Characters | 106862 |
| Markdown Notion links | 801 |
| Notion URLs | 808 |
| Unique Notion IDs | 808 |
| Duplicate Notion ID groups | 0 |
| Empty link titles | 30 |
| Duplicate title groups | 46 |

## Main Control Signals

The export confirms that the hard-count layer is link-based, not title-based:

```text
808 Notion URLs
-> 808 unique Notion IDs
-> 0 duplicate ID groups
```

The main control problem visible in this snapshot is title coherence:

```text
46 duplicate title groups
-> 74x "Unbenannt"
-> 30 empty titles
-> repeated prompt/template titles
```

CAP should therefore treat title cleanup, canonical naming and duplicate grouping as early registry work before any broad content review.

## Top Duplicate Title Groups

| Title | Count |
| --- | ---: |
| Unbenannt | 74 |
| empty title | 30 |
| **Korrekturlesen** | 6 |
| **Verbessere den Schreibstil** | 6 |
| **Erklaeren** | 6 |
| KI-Faehigkeiten | 6 |
| Patent_3_TNIAP | 4 |
| Patent_2_TNAV | 4 |
| Patent_1_Mindcode | 4 |
| Umformatieren | 4 |
| Patent_4_Tokenisierung | 4 |
| Meine Notion-KI | 3 |
| Meine Links | 3 |
| Hey | 3 |
| jori | 3 |
| Codex139+_TriggerExport_174-210_SilviModus | 3 |
| Analyse_Umsetzungsplan_Berserker_Modis_Resonanz | 3 |
| Codex170_Plus_FINAL | 3 |
| RAS_Rekursiver_Affinitaetsspeicher | 3 |

## Keyword Signals From Titles

| Keyword | Title count |
| --- | ---: |
| FerrAI | 60 |
| TerraNova | 55 |
| Trigger | 45 |
| Notion | 23 |
| Sync | 18 |
| IPERKA | 17 |
| CIC | 13 |
| GitHub | 13 |
| Framework | 9 |
| CAP | 7 |
| Dashboard | 7 |
| VORTEX | 6 |
| Control | 5 |
| Library | 3 |
| Cognitive | 2 |
| EQUILIBRIUM | 1 |
| Zenodo | 1 |
| Database | 1 |
| Wiki | 1 |
| Prism | 0 |

## Deterministic Boundary

- The raw snapshot remains sensitive and local.
- It must not be copied into public release material.
- It is not a replacement for Notion connector verification.
- It can seed CAP review queues, duplicate groups and page census work.

## CAP Registry Effect

The snapshot is registered as:

```text
Name: Home-Ansichten Snapshot 2026-05-11
Object Type: External Source
Source Layer: Export Hard Count
Count Basis: 808 export_hard_count
Canon Status: Reference
Sensitivity: Sensitive
Sync Status: In sync
```

## DUP-001 Effect

`DUP-001` classifies the 46 duplicate title groups into 8 review queues without exporting raw URLs, raw Notion IDs or a private page list.

The first cleanup target is title governance, not deletion.
