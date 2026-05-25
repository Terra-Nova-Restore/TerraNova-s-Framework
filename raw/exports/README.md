# Raw Export Archive

Status: public repository boundary layer

This folder documents raw-export containers, derived intake batches, checksums
and review gates. It is not a place for unreviewed private dumps.

## Current public-safe shape

The legacy `850k` artifact is a prepared container and historical planning
label. The tracked file is a placeholder, not the raw dump.

```text
2026-04-30_batch_850k_raw.txt                 placeholder only
2026-04-30_batch_850k_raw_fuellversion.md     placeholder/fill template
2026-04-30_batch_850k_raw.sha256              integrity pointer
fill_850k_raw.sh                              private-only fill helper
```

Actual private raw payloads stay outside the public repository unless a later
review gate explicitly classifies a redacted derivative as public-safe.

`fill_850k_raw.sh` refuses to run unless `TNV_ALLOW_PRIVATE_RAW_FILL=1` is set
and writes to `raw/exports/local-private/`, which is ignored by git.

## Incoming derivatives

`raw/exports/incoming/` contains derived manuscript and appendix intake batches.
These files are larger than aggregate index rows and therefore have their own
boundary policy:

- They are not treated as private raw ChatGPT dumps.
- They are not a precedent for committing unreviewed raw exports.
- New files in this lane require classification, checksum and sensitivity scan.
- Promotion from this lane must produce curated docs, release notes or public
  indexes outside `raw/exports/`.
- Files that later prove private, credential-bearing, patent-sensitive or
  Track-C/GODFATHER_LOCK-sensitive must be moved out of the public lane.

See `incoming/README.md` and `REVIEW_GATE.md` for the operative rules.

## Hard rule

No unclassified raw export may be committed to this public repository. Raw or
private source material lands in local/private storage first; GitHub receives
only placeholders, hashes, reviewed derivatives, or redacted public outputs.
