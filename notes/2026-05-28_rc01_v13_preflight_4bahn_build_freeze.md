# RC01-v13-preflight — 4-Bahn-Theorem integrated build freeze

Date: 2026-05-28
Mode: STUDIO / RC01-v13-preflight
Status: BUILD SUCCESS / FROZEN / NOT PUBLISH-READY

## Summary

The local Ubuntu/LaTeX branch `main_rc01_v13_preflight.tex` successfully built a new integrated monography preflight PDF with Chapter 90: `4-Bahn-Theorem as Zenodo-calibrated CIC case`.

This is a local preflight freeze only. It is not a Zenodo release, not a BIZ-claim, and not a final publication state.

## Build facts

- Working file: `main_rc01_v13_preflight.tex`
- Integrated chapter: `chapters/90_4_bahn_theorem_zenodo_calibrated_cic_case.tex`
- PDF artifact: `main_rc01_v13_preflight.pdf`
- Exported local copy: `RC01-v13-preflight_4-Bahn-Theorem_integrated_FINAL_FREEZE.pdf`
- Pages: 686
- PDF size: 2,573,987 bytes
- PDF Producer: `pdfTeX-1.40.28`
- Creation/Mod time observed: 2026-05-28 07:54:57 CEST
- Blocker check: clean

## Final SHA256

```text
65b679555d95170b28171be334c8a43bfe5421764b2643ee0bad9cedebc37dea  main_rc01_v13_preflight.tex
613722d60692af558920456919f9fd27cca75923f93c1c665eba8c62e69a39bb  chapters/90_4_bahn_theorem_zenodo_calibrated_cic_case.tex
4ca59ec91f5aeee45cd767362dd66e21f88b6e2cc1c16795f2fead328d824ec6  main_rc01_v13_preflight.pdf
```

## Source planes

- Control Plane: `MONOGRAPHIE-INTEGRATION — 4-Bahn-Theorem → RC01-Next (Zenodo-Calibrated)`
- Content Plane: `4-Bahn-Theorem — Zenodo-kalibrierter Integrationslayer für Monographie`
- Measurement Plane: `Zenodo / DOI / metrics layer`
- Publication Prep: `Zenodo-Publikationsvorbereitung — 4-Bahn-Theorem (STUDIO → BIZ-Pfad)`

## Safety gates

- `main_build01.tex` remains untouched.
- No Zenodo upload without R19-Finalcheck.
- No Zenodo upload without Human Gate Silvi.
- Current PDF is a local preflight freeze, not publication-ready.

## Next steps

1. Visual check: TOC + Chapter 90 beginning/middle/end.
2. Rendering audit: remaining raw Notion/Markdown artifacts, if any.
3. Optional local commit of full source artifacts from Ubuntu.
4. Only after R19 + Human Gate: prepare Zenodo release candidate.

## Sync note

This note is the GitHub-side sync anchor for the Notion/GitHub handoff after the local Ubuntu build freeze.
