# GPT / Codex Integration — TerraNova / FerrAI

Status: initial controlled export

## Purpose

This document defines how GPT, Codex-style agents and AI-assisted workflows are represented inside the TerraNova / FerrAI GitHub framework.

GPT is not stored as an identity or private conversation archive. It is represented as an operational layer:

- reasoning and drafting support
- code and repository operations
- validation and refactoring assistance
- LaTeX / Markdown transformation
- Notion → GitHub export support
- review, audit and redaction assistance

## Boundary

This file does not claim persistent model identity, autonomous agency, or private memory beyond explicit exported artifacts.

Accepted representation:

```text
Human intent → GPT/Codex assistance → reviewed artifact → GitHub commit
```

Rejected representation:

```text
Raw chat dump → unreviewed system truth
```

## Role in the repository

GPT/Codex belongs in the tooling and methodology layer, not in the scientific claim layer.

Recommended locations:

```text
docs/ai/
scripts/
.github/workflows/
docs/sync/
docs/evidence/
```

## Current integrations

- Notion map design and validation
- GitHub workflow creation
- controlled export stubs
- text cleaning scripts
- science-core routing
- repository documentation
- MCP/Notion sync sequence architecture in [`full_sync_terra_nova_mcp_sequence.md`](full_sync_terra_nova_mcp_sequence.md)
- Prism atlas routing and source-pack usage in [`prism_atlas_usage.md`](prism_atlas_usage.md)

## Citation / acknowledgement pattern

When AI assistance materially shaped an artifact, use a short note:

```text
AI assistance: Drafting, structural refactoring and repository automation support were performed with GPT/Codex-style tooling under human review.
```

## Safety rule

No secrets, private raw notes, wallet data, identity keys, intimate material, or unredacted chat exports should be committed as AI context.

## Next steps

- add AI-assisted workflow notes to README
- link this document from science README
- add PR template checkbox for AI-assisted changes
