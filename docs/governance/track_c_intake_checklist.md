# Track C Intake Checklist

Status: BIZ / Governance
Source: Issues #10 and #11 Track C intake/review markers.
Trace: Issues #10, #11; `docs/governance/public_boundary.md`; `raw/exports/incoming/README.md`.
Boundary: Public-safe checklist only. It does not ingest, publish, delete or canonicalize Track C material.
Mode: BIZ
GitHub sync state: tracked in this repository; validate with `scripts/validate_docs.py`.
Notion source awareness: Notion may hold lightweight indexes, but full Track C text should remain outside Notion unless separately approved.

## Purpose

Track C contains narrative, mythopoetic, literary-symbolic or companion material.
It must not collapse into the scientific Track A line by accident.

This checklist defines the minimum intake frame before any Track C material is
merged, indexed, summarized or promoted.

## Intake Fields

| Field | Required decision |
| --- | --- |
| Work title | Exact current title or working title |
| Volume/chapter count | Number of volumes, chapters, pages or files |
| Narrative status | Fiction, memoir-like, symbolic companion, hybrid or unknown |
| Relationship to TerraNova/FerrAI/CIC | Contextual relation, not evidence claim by default |
| Sensitivity | Public, redact-candidate, private, `GODFATHER_LOCK`, patent-sensitive |
| Storage lane | Local archive, Notion index, GitHub manifest, release candidate |
| Promotion target | Track C only, Band 2 appendix candidate, companion publication, reject/defer |
| Review owner | Human/operator or named review pass |

## Default Classification

```text
Track C material is companion/workshop material until reviewed.
It is not canonical evidence for Track A by default.
```

## Allowed First Step

The safe first step is a slim index or manifest:

- title;
- date/source;
- high-level chapter map;
- sensitivity class;
- relation to TerraNova/FerrAI/CIC;
- storage pointer without exposing private raw text.

## Blocked Moves

Do not:

- merge Track C directly into `main.tex` or the scientific dissertation line;
- delete source material just because it is not Track A;
- treat fictional/narrative material as factual system evidence;
- paste full private companion text into Notion or GitHub;
- accept deletion of uploaded companion files without an explicit archive decision.

## Promotion Rule

Selected excerpts may move only after a review pass states:

- why the excerpt is needed;
- which track receives it;
- whether it is evidence, illustration, appendix context or companion literature;
- what redaction or sensitivity gates passed.

## Issue Linkage

This checklist is the repository working surface for:

- Issue #10: Track C intake: NeoGilgamesch / FerrAI / Noa separation.
- Issue #11: Review required: Prism workspace changes before merge.

Both issues should remain open until a real Track C batch is classified against
this checklist or superseded by a stronger intake artifact.
