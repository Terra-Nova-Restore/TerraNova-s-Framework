# Prism Source Packs

Status: archival input area

This directory stores local Prism/Notion source exports used by
`scripts/render_prism_atlas.py`.

Dated source-pack directories are intentionally ignored by git because they can
contain private, token, wallet, raw-chat or patent-sensitive material. Commit the
generated reviewed docs under `docs/atlas/` and `docs/triggers/` instead.

## Current Pack

| Directory | Use |
| --- | --- |
| `2026-05-02/` | Source pack used to generate the current `docs/atlas/` and `docs/triggers/` files. |

## Rule

Do not edit source-pack files in place. Add a new dated source-pack directory
for a new Prism export, then regenerate the atlas.
