#!/usr/bin/env bash
set -euo pipefail

SRC="raw/exports/2026-04-30_batch_850k_raw_fuellversion.md"
DST="raw/exports/2026-04-30_batch_850k_raw.txt"
SHA="raw/exports/2026-04-30_batch_850k_raw.sha256"

awk '/^## RAW_PAYLOAD_BEGIN/{flag=1;next}/^## RAW_PAYLOAD_END/{flag=0}flag' "$SRC" > "$DST"
sha256sum "$DST" > "$SHA"
echo "Filled raw dump + checksum updated."
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/2026-04-30_batch_850k_raw_fuellversion.md"
DST="$SCRIPT_DIR/2026-04-30_batch_850k_raw.txt"
SHA="$SCRIPT_DIR/2026-04-30_batch_850k_raw.sha256"
TMP="$(mktemp)"

trap 'rm -f "$TMP"' EXIT

awk '/^## RAW_PAYLOAD_BEGIN/{flag=1;next}/^## RAW_PAYLOAD_END/{flag=0}flag' "$SRC" > "$TMP"
if ! grep -q '[^[:space:]]' "$TMP"; then
  echo "No payload found between RAW_PAYLOAD markers." >&2
  exit 1
fi
if grep -Eq 'PASTE FULL( 850K)? RAW PAYLOAD HERE|PASTE_OR_IMPORT_RAW_BATCH_CONTENT_HERE' "$TMP"; then
  echo "Template placeholder still present; refusing to overwrite raw dump." >&2
  exit 1
fi
mv "$TMP" "$DST"
sha256sum "$DST" > "$SHA"
BYTES="$(wc -c < "$DST" | tr -d '[:space:]')"
echo "Filled raw dump ($BYTES bytes) + checksum updated."
