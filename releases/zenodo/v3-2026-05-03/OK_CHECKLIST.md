# Zenodo Upload OK Checklist

Generated: 2026-05-02T22:27:19.785962+00:00

## Artifact

- Source: `C:\Users\Silvan\Downloads\main (22).pdf`
- Repository upload path: `releases/zenodo/v3-2026-05-03/ferrai-terra-nova-dissertationsentwurf-v3-2026-05-03.pdf`
- Zenodo filename: `ferrai-terra-nova-dissertationsentwurf-v3-2026-05-03.pdf`
- Size bytes: `2554266`
- SHA256: `e282e2d944c7e263bf07d5d3a226da0e65bf7dd3d107efa1a83fe148674e1bc1`
- MIME guess: `application/pdf`
- Line count: `n/a`
- Legacy API size warning: `False`

## Metadata Gate

- Title: `FerrAI / Terra Nova: Dissertationsentwurf - Quellengebundene Rekonstruktion des Terra-Nova/FerrAI-Korpus und der sichtbaren CIC-Dokumentfamilie`
- Version: `v3-2026-05-03`
- Description note: `Deutsch/English RC-Version, Stand: 2. Mai 2026, 529 PDF-Seiten`
- License: `cc-by-4.0`
- Access right: `open`
- Creator ORCID: `0009-0007-8033-3508`

## Local Files

- `manifest.json`: file facts and generated metadata
- `zenodo_api_metadata.json`: payload body for API metadata update
- `.zenodo.json.draft`: root metadata draft for GitHub-Zenodo release flow

## Human OK Gate

- Confirm the artifact is the intended public upload.
- Confirm no private tokens, wallet secrets, or private raw-chat material are included.
- Confirm title, version, license, and relation to existing DOI.
- Publish only after Zenodo preview looks correct.

## Execution Notes

- GitHub Actions draft path: commit this release package and run `Zenodo Draft Upload - v3 main 22`.
- The workflow uses the GitHub repository secret `Zenodo_API`; do not paste tokens into files.
- The workflow creates/uploads an unpublished Zenodo draft. Final publish stays manual in the Zenodo preview.
- Zenodo versioning should manage DOI/version relationships for true new versions; the existing DOI values are included as context, not as forced related identifiers.
- This package is preparation only. It did not call Zenodo, GitHub, ORCID, or OpenAIRE.
