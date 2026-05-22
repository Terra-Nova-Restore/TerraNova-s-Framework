# RC01-v12 Metadata Edit Instructions v0.2

Status: REVIEW_ONLY_NO_MUTATION
Target record: `20073579`
Specific DOI: `10.5281/zenodo.20073579`
Concept DOI: `10.5281/zenodo.19774446`
Current version: `RC01-v12`

## Gate

These instructions are a review artifact only. They do not authorize or perform
any Zenodo mutation.

Explicitly not authorized in this package:

- Zenodo API write request
- file upload
- file deletion
- file modification
- new version creation
- DOI reservation
- publish action
- GitHub release
- Git tag

## Official Rule Used

Published Zenodo record metadata may be edited. Files and persistent
identifiers are not normal metadata-edit fields. File/content changes require a
separate file or version workflow and are out of scope here.

## UI Path, If Later Authorized

1. Open `https://zenodo.org/records/20073579`.
2. Use the Zenodo record edit control for the published record.
3. Edit metadata only.
4. Preserve all file settings and files unchanged.
5. Preserve DOI and concept DOI unchanged.
6. Apply only the metadata-field changes from the v0.2 payload.
7. Publish/save the metadata edit only after a separate explicit Silvi-Go for
   the visible metadata update.

## API Path, If Later Authorized

Use only after a separate explicit Silvi-Go and with a token scoped for deposit
metadata editing. Do not execute from this review package.

Conceptual flow:

```text
POST /api/deposit/depositions/20073579/actions/edit
PUT  /api/deposit/depositions/{edit_id}
POST /api/deposit/depositions/{edit_id}/actions/publish
```

The API path must be rechecked against the authenticated Zenodo deposition
response before execution, because published-record edit flows expose edit and
publish links in the deposition resource.

Resolve `{edit_id}` from the authenticated `actions/edit` response rather than
assuming that the published record id stays writable for the follow-up `PUT`
and `publish` calls.

## Fields To Preserve

- `title`
- `upload_type`
- `publication_type`
- `creators`
- `access_right`
- `license`
- `version`
- `language`
- `keywords`
- `related_identifiers`
- `references`
- `custom.code:codeRepository`
- DOI and concept DOI
- all files and file visibility

## Fields To Edit

- `description` only, replacing exported Notion wrapper markup and older
  reference-snapshot wording with the clean v0.2 Zenodo-facing description.
- `notes` only if Zenodo accepts the notes field for the authenticated edit
  payload. If unsupported, omit it rather than forcing a schema change.

## Final Payload Candidate

Use the `proposed_api_payload_candidate.metadata` object in
`zenodo_metadata_patch.rc01-v12.review.json`.

The v0.2 payload intentionally:

- preserves `custom.code:codeRepository`;
- preserves the current keyword list;
- preserves the current concept DOI reference;
- preserves the current concept DOI `isVersionOf` relation;
- does not use the record's own DOI as a normal reference;
- does not add a GitHub related identifier.

## Write-Readiness

The v0.2 package is write-ready as a metadata-only instruction package after
human review. It is not execution-authorized.

Required before execution:

- explicit Silvi-Go for Zenodo metadata edit;
- authenticated Zenodo deposition readback;
- pre-write comparison of target record `20073579`;
- confirmation that no file/version/publish-new-version path is opened.
