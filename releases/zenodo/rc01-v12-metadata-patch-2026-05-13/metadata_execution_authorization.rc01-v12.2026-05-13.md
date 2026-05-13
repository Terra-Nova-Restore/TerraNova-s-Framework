# RC01-v12 Metadata Execution Authorization

Status: AUTHORIZED_METADATA_ONLY
Authorized by: Silvi
Authorization date: 2026-05-13
Target record: `20073579`
Specific DOI: `10.5281/zenodo.20073579`
Concept DOI: `10.5281/zenodo.19774446`
Current version: `RC01-v12`

## Authorization

Silvi explicitly authorized execution of the Zenodo metadata update after v0.2
review.

Execution route:

- GitHub Actions;
- repository secret `ZENODO_API`;
- workflow `.github/workflows/zenodo-rc01-v12-metadata-update.yml`;
- one-shot merge-commit gate `execute-zenodo-z2-metadata-update`.

Implementation note:

- Attempt 1 used the legacy `/api/deposit/depositions/{id}` path and failed
  before opening an edit because Zenodo returned `403 Permission denied`.
- Attempt 2 uses the current record draft path `/api/records/{id}/draft` for
  metadata-only edit/publish.

## Authorized Scope

- update published record metadata only;
- preserve record ID `20073579`;
- preserve DOI `10.5281/zenodo.20073579`;
- preserve concept DOI `10.5281/zenodo.19774446`;
- preserve version `RC01-v12`;
- preserve file `main (44).pdf`;
- preserve `custom.code:codeRepository`;
- preserve current keywords;
- preserve current concept DOI reference;
- preserve current `isVersionOf` relation.

## Still Forbidden

- file upload;
- file deletion;
- file modification;
- new version creation;
- DOI reservation;
- GitHub release;
- Git tag;
- raw dump or private excerpt publication.

## Expected Result

The public Zenodo description is replaced by the clean v0.2 description while
the file, DOI, concept DOI, version, repository link, keywords, references, and
related identifier remain unchanged.
