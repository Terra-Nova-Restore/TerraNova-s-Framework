# Review: 10 Master-Prompts — TerraNova Edition v1.0

Status: pre-export review
Date: 2026-04-28
Scope: product, structure, licensing, clarity, GitHub readiness

## Executive verdict

The asset is commercially usable as a lightweight entry product, but it should not yet be treated as a flagship scientific TerraNova artifact.

It works best as:

- a beginner-friendly prompt pack
- a Gumroad / lead-magnet product
- a public-facing introduction to TerraNova-style prompt orchestration
- a bridge from simple prompting into deeper CIC / Codex / System work

It should not be positioned as:

- the scientific core of TerraNova
- proof of the full FerrAI architecture
- the complete prompt operating system
- a high-ticket product by itself

## Strengths

1. Clear entry point

The document is understandable for non-technical users. It explains use cases directly and does not require prior knowledge of TerraNova, CIC, Trigger systems, Notion, or GitHub.

2. Productizable structure

The ten-prompt format is marketable. It is easy to package as PDF, Markdown, Notion template, Gumroad product, or GitHub public asset.

3. Good operational categories

The strongest categories are:

- System-Initialisierung
- Context-Stacking
- Trigger-basierter Flow
- Output-Modulation
- Error-Recovery
- Tool-Orchestration
- Resonanz-Check

These are practical and immediately useful.

4. Strong funnel role

The asset can function as a low-friction front door into larger TerraNova products:

- Prompt Framework v2.0
- TerraNova Scientific Core
- CIC workbooks
- Notion/GitHub operating system
- Genesis Pass / advanced system access

## Problems to fix before export

### 1. Numbering error

There are two sections numbered `5`:

- 5. Output-Modulation
- 5. Error-Recovery

Recommended correction:

5. Output-Modulation
6. Error-Recovery
7. Meta-Learning
8. Codex-Integration
9. Tool-Orchestration
10. Resonanz-Check

### 2. Encoding artifacts

The text contains repeated broken symbols such as:

- ``
- ``
- odd placeholder markers
- broken hyphenation and OCR-like spacing

These must be cleaned before GitHub/PDF export. Replace them with standard Markdown:

- `-`
- `→`
- `[...]`
- `**bold**`

### 3. Tone mismatch

The introduction says:

> 10 der kraftvollsten Prompts

This is strong marketing language. For a professional export, soften slightly:

> 10 erprobte Master-Prompts aus 16 Monaten intensiver KI-Arbeit.

This is still confident but less exaggerated.

### 4. Platform promise risk

The line:

> Beobachte die Magie

is catchy but weakens credibility. Suggested replacement:

> Beobachte, wie Struktur, Kontext und Outputqualität spürbar klarer werden.

### 5. License ambiguity

The license says `CRC Basic Lizenz`, but the legal terms are not fully defined.

Minimum fix:

- define CRC
- specify permitted personal/commercial use
- specify no resale / no redistribution
- specify whether modified versions may be shared internally
- add version/date/contact

### 6. Product ladder needs separation

The document jumps from a beginner prompt pack to:

- Metarotik Werkbuch CHF 149
- Genesis Pass CHF 5'000

This may create tonal discontinuity for first-time buyers. Better product ladder:

1. Free / low-cost: 10 Master-Prompts
2. CHF 29–49: Prompt Framework v2.0
3. CHF 149: advanced workbook / applied system module
4. CHF 500+: workshop / audit / implementation
5. CHF 5'000: Genesis / full system package

## Suggested GitHub placement

Recommended path:

```text
docs/public/prompts/10-master-prompts-terranova-v1.md
```

Alternative product path:

```text
products/prompt-packs/10-master-prompts-terranova-v1.md
```

Do not place this in the scientific core as a canonical research artifact. It belongs in `public` or `products`, with cross-links into the deeper architecture.

## Suggested repo mapping

```json
{
  "title": "10 Master-Prompts — TerraNova Edition v1.0",
  "source_type": "product_asset",
  "status": "export_ready_after_cleanup",
  "target_path": "docs/public/prompts/10-master-prompts-terranova-v1.md",
  "visibility": "public_candidate",
  "risk_level": "low",
  "needs_redaction": false,
  "needs_cleanup": true,
  "contains_private_data": false,
  "contains_commercial_terms": true,
  "license": "CRC Basic — needs formal definition"
}
```

## Recommended final positioning

Use this as:

> TerraNova Entry Pack: 10 resonanzbasierte Master-Prompts für strukturierte KI-Arbeit mit ChatGPT, Claude und Notion AI.

Avoid positioning it as:

> Full TerraNova Operating System.

Better phrase:

> Ein Einstieg in das TerraNova Operating System für KI-Arbeit.

## Action checklist

- [ ] Fix numbering
- [ ] Clean broken characters
- [ ] Normalize placeholders
- [ ] Define CRC Basic License
- [ ] Add short disclaimer: AI outputs must be reviewed by the user
- [ ] Separate product ladder from core content
- [ ] Add version metadata block
- [ ] Export Markdown first, then PDF
- [ ] Add to GitHub under `docs/public/prompts/`
- [ ] Link from scientific core as public-facing entry artifact

## Final assessment

This is a good entry-level commercial artifact. It should be cleaned, normalized and committed as a public/product asset. It is not the scientific core, but it is useful as a front door into the scientific and architectural core.
