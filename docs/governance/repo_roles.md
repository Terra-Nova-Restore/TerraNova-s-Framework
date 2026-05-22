# Repository Roles

Status: BIZ / Repository governance
Source: Repository-local role map, aligned with Control Tower and public-boundary rules.
Trace: Required by `scripts/validate_docs.py`; supports repo hygiene checks.
Boundary: Describes repository artifact roles only; does not move raw data or mutate external systems.
Mode: BIZ
GitHub sync state: tracked in this repository.
Notion source awareness: Notion remains the internal system of record for live workspace state.

This repository defines strict roles for sub-systems and related artifacts to maintain operational hygiene.

- **`core`**: The main framework logic, control tower, and architecture documents.
- **`fork`**: Derivatives or external sync points.
- **`research`**: Experimental or speculative papers and analyses.
- **`private-app`**: Local integrations (e.g., Python sync engine) that stay off-chain and local.
- **`archive`**: Immutable historic states and Zenith artifacts.
- **`release`**: Officially cut Zenodo mirrors and public artifacts.
- **`raw-docs`**: Ingested exports pending processing (must pass `REVIEW_GATE`).
