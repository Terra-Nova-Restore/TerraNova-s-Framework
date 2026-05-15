# RC01-v12 Z3 Metadata Refresh Execution Authorization

Status: AUTHORIZED_FOR_PR_ONLY_WAITING_SILVI_MERGE_GO
Authorized by: Silvi
Authorization date: 2026-05-15
Target record: `20073579`
Specific DOI: `10.5281/zenodo.20073579`
Concept DOI: `10.5281/zenodo.19774446`
Current version: `RC01-v12`

## Authorization

Silvi authorized Codex to open a pull request for a Z3 metadata-only refresh.
This package must wait for explicit Silvi merge-go before any Zenodo workflow
execution is triggered.

Execution route after merge-go:

- GitHub Actions;
- repository secret `ZENODO_API`;
- workflow `.github/workflows/zenodo-rc01-v12-z3-metadata-refresh.yml`;
- one-shot merge-commit gate `execute-zenodo-z3-metadata-refresh` or manual
  workflow dispatch after review.

## Authorized Scope

- update published record metadata only;
- preserve record ID `20073579`;
- preserve DOI `10.5281/zenodo.20073579`;
- preserve concept DOI `10.5281/zenodo.19774446`;
- preserve version `RC01-v12`;
- preserve file `main (44).pdf`;
- preserve `custom.code:codeRepository`;
- preserve current `isVersionOf` relation;
- preserve references;
- preserve license, upload type, publication date, creators, and contributors;
- replace title, description/abstract, and keyword list according to the Z3
  payload.

## Still Forbidden

- file upload;
- file deletion or replacement;
- file modification;
- new version creation;
- DOI reservation or mutation;
- concept DOI mutation;
- related identifier mutation;
- license change;
- upload type change;
- GitHub release;
- Git tag;
- Cycle 4 opening;
- Z1 reactivation;
- CEI-DATA-05 reciprocal edit;
- raw dump or private excerpt publication.

## Expected Result

The public Zenodo metadata is refreshed to the framework-oriented Z3 title,
parallel DE/EN abstract, mandatory non-claim disclaimer, persistence-layer map,
and new keyword list while file, DOI, concept DOI, version label, repository
link, references, related identifier, license, upload type, and publication date
remain unchanged.

## Execution Go

Status: AUTHORIZED_FOR_ZENODO_EXECUTION
Authorized by: Silvi
Authorization timestamp: 2026-05-15 ~05:22 CEST
Trigger route: GitHub Actions push gate
Required commit marker: `execute-zenodo-z3-metadata-refresh`

Post-run verification required:

- live Zenodo title equals
  `FerrAI–TerraNova CIC Framework — System Architecture, State Logic and Governance Boundaries`;
- DE/EN abstract includes the mandatory anti-claim disclaimer;
- keywords are replaced by the 11-entry Z3 list;
- DOI, concept DOI, version label, publication date, file, license, upload type,
  related identifiers, references, and repository custom field remain unchanged;
- modified timestamp updates while publication date remains `2026-05-13`.
