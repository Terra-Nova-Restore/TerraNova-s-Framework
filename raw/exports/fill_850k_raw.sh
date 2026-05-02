#!/usr/bin/env bash
set -euo pipefail

SRC="raw/exports/2026-04-30_batch_850k_raw_fuellversion.md"
DST="raw/exports/2026-04-30_batch_850k_raw.txt"
SHA="raw/exports/2026-04-30_batch_850k_raw.sha256"

awk '/^## RAW_PAYLOAD_BEGIN/{flag=1;next}/^## RAW_PAYLOAD_END/{flag=0}flag' "$SRC" > "$DST"
sha256sum "$DST" > "$SHA"
echo "Filled raw dump + checksum updated."
