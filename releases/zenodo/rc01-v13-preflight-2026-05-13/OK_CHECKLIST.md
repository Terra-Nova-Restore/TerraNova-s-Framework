# Zenodo RC01-v13 Preflight Checklist

Status: PREPARED / NO ZENODO MUTATION

## Z1 Checks

- [x] Current Zenodo record identified: `20073579`.
- [x] Current DOI identified: `10.5281/zenodo.20073579`.
- [x] Concept DOI identified: `10.5281/zenodo.19774446`.
- [x] ORCID anchor identified: `0009-0007-8033-3508`.
- [x] GitHub repository link is present in current Zenodo metadata.
- [x] Current RC01-v12 PDF hash verified locally.
- [x] `main (45).pdf` checked and found byte-identical to `main (44).pdf`.
- [x] No RC01-v13 upload artifact staged.
- [x] No Zenodo write action performed.

## Required Before Z2 Draft Creation

- [ ] New RC01-v13 PDF exists and differs from RC01-v12.
- [ ] New artifact SHA-256 and MD5 are recorded.
- [ ] Metadata has been reviewed against the new artifact.
- [ ] Public-boundary review confirms no raw dump or private excerpts.
- [ ] Zenodo target record remains `20073579`.
- [ ] Workflow dry run passes.
- [ ] Silvi explicitly authorizes draft creation.

## Required Before Any Publish

- [ ] Zenodo draft preview reviewed manually.
- [ ] Uploaded file checksum matches the intended artifact.
- [ ] Title, version, license, ORCID, repository link, and concept DOI are correct.
- [ ] No private, token, wallet, credential, raw-chat, or patent-sensitive material is exposed.
- [ ] Silvi explicitly authorizes publish.

## Hard Locks

- Zenodo draft creation: not authorized in Z1.
- Zenodo upload: not authorized in Z1.
- Zenodo publish: not authorized in Z1.
- DOI reservation: not authorized in Z1.
- `main (45).pdf` upload as RC01-v13: blocked because it is byte-identical to RC01-v12.
