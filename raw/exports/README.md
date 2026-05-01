# Raw Export Archive

This folder holds large raw export payloads that should not be mixed directly into the core manuscript.

## Current artifact

- `2026-04-30_batch_850k_raw.txt` (prepared full-dump container)
- `2026-04-30_batch_850k_raw.sha256` (integrity hash)

## Usage

1. Paste/import the full raw 850k-character batch into the `.txt` file.
2. Recompute checksum:
   - `sha256sum raw/exports/2026-04-30_batch_850k_raw.txt > raw/exports/2026-04-30_batch_850k_raw.sha256`
3. Reference the artifact in intake and decision logs before promotion attempts.
