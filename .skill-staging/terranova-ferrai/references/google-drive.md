# Google Drive connector policy

Use Google Drive for external artifacts, shared documents, exports, PDFs,
Sheets, and Slides that support TerraNova work.

## Default role

Google Drive is strongest for:

- source documents outside Notion
- PDFs and exported research bundles
- spreadsheets, presentations, and shared reference docs
- handoff artifacts meant for external review

## Read-first behavior

Default to:

- find the file first
- fetch or export only the needed document
- summarize structure before proposing edits
- preserve filenames and document context in outputs

## Mutation rule

Only mutate Google Drive when the user explicitly asks to:

- create a file
- rewrite a Doc
- edit a Sheet or Slide deck
- move or share Drive content

If a doc supports another system of record, treat Drive as supporting evidence,
not the canonical source of intent.

## TerraNova-specific note

Drive is a good external artifact surface for:

- research packs
- investor material
- export-ready decks
- PDF snapshots

It is not the default source of workspace truth when Notion already holds the
same concept.
