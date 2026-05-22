# GH-XW-001 Release Gate

Status: STUDIO / gate candidate
Source: GPT H.4 synthesis, local LaTeX/PDF inspection, Notion Zenodo page, Zenodo RC01-v12 release mirror
Trace: GH-XW-001
Boundary: Gate only. Does not create, upload, publish or mutate a release.
Mode: STUDIO
GitHub sync state: Prepared as repository-side next-build gate.
Notion source awareness: Any Notion checkpoint or registry update requires a separate explicit GO and Equilibrium page-creation/update gate.

## Current Published Structure

The current 661-page RC01-v12 PDF already contains:

- `H` = Dokumentinventar und Verarbeitungsplan
- `H.3` = Erste Steckbriefmatrix der offenen Dokumentfamilien
- `H.4` = Dokumentfamilien des bereits sichtbaren Bestands
- `H.9` = Status des Inventar- und Verarbeitungsplans

The crosswalk candidate belongs methodically after `H.3`, but inserting it as
new `H.4` requires downstream renumbering of the existing `H.4-H.9` sections in
a future LaTeX build.

## Gate Conditions

Before any LaTeX or Zenodo follow-up:

1. Confirm that the raw export hash still matches the source used for the aggregate metrics.
2. Rebuild aggregate metrics with `scripts/analyze_notion_home_export.py`.
3. Confirm that no raw URLs, page IDs or sensitive titles are included in GitHub-facing files.
4. Confirm that P1/P2/P3/HOLD classifications are backed by the actual register tables before citing them as verified counts.
5. Decide whether the candidate is inserted as new `H.4` or routed to a later appendix/register family.
6. If inserted after `H.3`, renumber the current `H.4-H.9` to `H.5-H.10`.
7. Run LaTeX build and PDF page-count/readability checks.
8. Treat any Zenodo action as separate: no draft, upload, metadata edit or publish without explicit Zenodo-stage GO.

## Stop Conditions

Stop the build path if:

- raw Notion inventory would need to be committed
- HOLD/private/protected/adult/legal_ip rows are not isolated
- the register XLSX/CSV cannot be located or checked
- the monograph insertion would silently rewrite the RC01-v12 public snapshot
- Zenodo action is implied instead of explicitly authorized

