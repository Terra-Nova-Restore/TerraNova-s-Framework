# Contributing

## What This Repository Is

`TerraNova-s-Framework` is the **GitHub Working State** for the FerrAI–Terra'Nova CIC Framework: a systems-engineering documentation of a co-creative human–AI cooperation model. It is primarily a **research monograph and evidence archive**, not a community software project.

- **Zenodo** = Reference Anchor (citable proof state)
- **GitHub** (this repo) = Working State (PR-proven implementation)
- **Notion** = Internal Index (System-of-Record)

## How to Contribute

### For External Contributors

You are welcome to:
- Open issues for questions, corrections, or discussion.
- Suggest improvements via pull requests.

Please note:
- This is a single-author research work. The author reserves the right to reject or modify contributions that do not align with the framework's architecture.
- Do not submit raw transcripts, PII, credentials, or unredacted export data.
- Read `docs/governance/public_boundary.md` before opening any PR.

### For the Author (Silvan Lenhard) and FerrAI/Codex

Internal contributions follow the Track system:

| Track | Description | Public? |
|-------|-------------|---------|
| Track A | Public Canon (synthesized framework docs) | ✅ OK |
| Track B | Evidence / Registry (aggregate indices) | ⚠️ Redacted only |
| Track C | Companion / Narrative / Private | ❌ Blocked |

All PRs must pass:
- `python scripts/validate_docs.py`
- `git diff --check`
- Secret pattern scan
- Public boundary review (no raw Notion URLs, no PII, no credentials)

## Pull Request Process

1. Create a branch from `main`.
2. Make focused, minimal changes.
3. Run local validation (`python scripts/validate_docs.py`).
4. Open a PR using the pull request template.
5. Wait for CI checks to pass.
6. Merge only after review.

See `.github/PULL_REQUEST_TEMPLATE.md` for the required PR format.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0 (see `LICENSE`).
