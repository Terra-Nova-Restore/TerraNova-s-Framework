#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/2026-04-30_batch_850k_raw_fuellversion.md"
PRIVATE_DIR="$SCRIPT_DIR/local-private"
DST="$PRIVATE_DIR/2026-04-30_batch_850k_raw.txt"
SHA="$PRIVATE_DIR/2026-04-30_batch_850k_raw.sha256"
TMP="$(mktemp)"

trap 'rm -f "$TMP"' EXIT

if [[ "${TNV_ALLOW_PRIVATE_RAW_FILL:-}" != "1" ]]; then
  echo "Refusing to fill raw export without TNV_ALLOW_PRIVATE_RAW_FILL=1." >&2
  echo "This helper writes only to raw/exports/local-private/, which is ignored by git." >&2
  exit 1
fi

awk '/^## RAW_PAYLOAD_BEGIN/{flag=1;next}/^## RAW_PAYLOAD_END/{flag=0}flag' "$SRC" > "$TMP"
if ! grep -q '[^[:space:]]' "$TMP"; then
  echo "No payload found between RAW_PAYLOAD markers." >&2
  exit 1
fi
if grep -Eq 'PASTE FULL( 850K)? RAW PAYLOAD HERE|PASTE_OR_IMPORT_RAW_BATCH_CONTENT_HERE' "$TMP"; then
  echo "Template placeholder still present; refusing to overwrite raw dump." >&2
  exit 1
fi
mkdir -p "$PRIVATE_DIR"
mv "$TMP" "$DST"
sha256sum "$DST" > "$SHA"
BYTES="$(wc -c < "$DST" | tr -d '[:space:]')"
echo "Filled private raw dump ($BYTES bytes) + checksum updated under local-private/."
