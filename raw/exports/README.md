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
- `2026-04-30_batch_850k_raw.txt` (legacy-named full-dump container)
- `2026-04-30_batch_850k_raw.sha256` (integrity hash)
- `prism/prism_full_pack_495p_2026-05-02.*` (current full-pack snapshot; exceeds the old 850k planning label)

The `850k` segment in older file names is a historical RC01 planning label, not
an active size limit.

## Usage

1. Paste/import the complete current raw payload into `2026-04-30_batch_850k_raw_fuellversion.md` between the `RAW_PAYLOAD` markers.
2. Run `./fill_850k_raw.sh` from `raw/exports/`, or `raw/exports/fill_850k_raw.sh` from repo root, to extract the payload and recompute the checksum.
3. The helper aborts if the payload block is empty or still contains a template placeholder.
4. Reference the artifact in intake and decision logs before promotion attempts.
