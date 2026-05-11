# Source of Record Policy

Status: BIZ / Governance
Source: Technical mirror of the FerrAI Operating Kernel v0.1 operating split.
Trace: `docs/architecture/ferrAI_operating_kernel_v0.1.md`
Boundary: Defines repository-side source roles; does not copy Notion rule content.
Mode: BIZ
GitHub sync state: tracked in this repository; validate through `scripts/validate_docs.py`.
Notion source awareness: required for rule, memory, canon and reference changes.

## Source Roles

Notion is the living source of record for rules, workspace memory, canon,
reference pages and unresolved operating decisions.

GitHub is the technical mirror for reviewed docs, scripts, schemas, issues, PRs,
release packages, diffs, CI checks and audit history.

Zenodo is the citable publication anchor for released artifacts.

Chat is the operational decision and correction layer.

Codex skills and boot files are startup hints. They must stay small and must not
become parallel rulebooks.

## Promotion Rule

A repository artifact may be treated as BIZ-relevant only when it carries:

- Status
- Source
- Trace
- Boundary
- Mode
- GitHub sync state when repo-, release- or structure-relevant
- Notion source awareness when rule-, memory- or canon-relevant

## Conflict Rule

When Notion and GitHub disagree on living rules, Notion wins until a human
decision updates the mirror. GitHub remains the audit trail for technical
changes and release history.
