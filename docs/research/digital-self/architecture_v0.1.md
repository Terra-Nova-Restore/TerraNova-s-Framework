# TNV-DIGITAL-SELF-001 — Two-axis architecture candidate v0.1

Status: EXPLORATORY / methodology candidate / not deployed or validated
Source: 17-page TNV-DIGITAL-SELF-001 research report dated 2026-11-21, followed by an owner-requested separation of current requirements from future technological hypotheses; non-public source content not reproduced
Trace: TNV-DIGITAL-SELF-001; 90-day plan proposed for 2026-11-21 through 2027-02-18
Boundary: Abstract public methodology only. No personal original records, private workspace paths/IDs, secrets, source corpus or private repository cross-links.
Mode: STUDIO / research proposal; no implementation authorization, no new governance norm
GitHub sync state: public review branch / proposed v0.1; not merged
Notion source awareness: Notion governs living project decisions and definitions. Existing Edentität, KSE and Identität distinctions remain unchanged.

## Research question

Which actions are worth undertaking **now** to preserve authentic, verifiable longitudinal evidence, without prematurely building models that future technologies may improve or replace?

A future model can generate plausible accounts of unrecorded events, but plausibility alone cannot verify what somebody actually observed or meant at an earlier time.

This document therefore separates two axes:

- **Axis A — contemporary evidence and preservation:** deliberately authorized source capture, provenance, date, versioning, preservation, privacy, exportability and restoration.
- **Axis B — conditional future capabilities:** model-derived interpretation, long-term pattern analysis, temporal evaluation, adaptive simulation and their scientific prerequisites.

Do not conflate a biographical archive, a personality model, a simulated persona, a continuously running agent, and continuity of first-person consciousness.

## Priority matrix

| Priority | Proposed action | Reason / boundary |
| --- | --- | --- |
| Essential **if** authentic evidence is retained | Keep original records separate from summaries, translations and interpretations | Later model outputs must not retroactively replace historical evidence |
| Essential **if** a record is retained | Record provenance, event time, capture time, rights and changes | Prevent false attribution and ambiguous consent |
| Essential **if** any sensitive archive exists | Access restrictions, encryption, backup and **tested** restore process | Retention without recoverability/security is a liability |
| Important now | Minimal inventory of source types, time coverage, missing periods and permissions | An inventory does not authorize ingesting the content |
| Important now | Portable, inspectable file formats and explicit unknown fields | Minimize model or provider lock-in |
| Optional, separately authorized | Small decision episodes, audio/video, blind tests or independent reviewers | Require specific benefit, time budget and purpose approval |
| Defer without demonstrated need | Large personalized models, permanent capture, complex multi-agent systems | Complexity is not a proxy for evidence or research progress |
| Future-dependent | Higher-fidelity multimodal longitudinal modeling and independent predictive assessment | Capability, transferability and timing need fresh evidence |
| Unresolved scientific question | Continuity/transfer of subjective human experience | No demonstrated identity-continuity mechanism is claimed |

These are **design judgments**, not facts about a particular individual's existing archive and not blanket consent for collecting personal data.

## Minimal architecture sketch — entirely proposed

```text
[Optional consented record OR fully synthetic case]
                       |
                       v
[Private source store and access restrictions]
         |                         |
         v                         v
[Provenance + checksums] [Purpose/consent/revocation register]
         |                         |
         +------------+------------+
                      v
            [Permission gate]
                      |
                      v
      [Versioned, dated derived interpretation]
                      |
                      v
        [Optional blinded evaluation and error log]
```

Minimal candidate metadata (not a deployed schema):

`record_id`, `record_type`, `source_format`, `language`, `event_time_or_range`, `captured_at`, `source_role`, `checksum`, `provenance`, `permission_scope`, `access_class`, `revocation_state`, `related_record_id`, `uncertainty_note`.

Required design properties (to be tested, not asserted as already working):

1. Historical originals remain distinguishable from model-generated statements; corrections are separate dated events.
2. Inference records cite permitted source references and model/tool version; unknowns and contrary evidence remain visible.
3. Sensitive information stays off public repositories; public examples are fully synthetic or independently cleared.
4. Consent is purpose-bound and revocable for future processing. A restored backup must reapply current restrictions before reuse. Actual deletion/retention guarantees require separate technical and legal analysis.
5. Encrypted backups, key recovery, checksum verification and export readability must be empirically tested.
6. The archive must remain interpretable without the original AI model or vendor.

## Revised 90-day concept (proposed; NOT started)

The initial report proposed a 90-day IPERKA cycle **2026-11-21 to 2027-02-18** emphasizing early decision documentation and prediction checks. The later scope correction changes the first research question to **what cannot responsibly wait**.

| Window | Suggested focus | Verifiable output |
| --- | --- | --- |
| Days 1–30 | Inform / Plan: assess available tools, inventory source categories and gaps; define privacy and purpose boundaries | A methodology-only inventory, scope, constraints and stop conditions; no bulk import |
| Days 31–60 | Decide / Realize: build a minimal synthetic-only preservation demonstrator or obtain narrow authorization for real content | Versioned draft schema, example record, restoration and revocation test plan |
| Days 61–90 | Control / Evaluate: test actual portability, integrity, access restrictions, restore behavior and workload; assess future technology scenarios | Evidence log, failures, estimated vs. measured effort, next-step decision |

A blind personality prediction is **optional**, not a prerequisite for preserving trustworthy sources. An evaluation date is a planning value, not proof of experiment launch.

## Future capability radar: no technological promises

Classify each capability with a **date of review**, evidence source, observable acceptance test and disconfirming condition.

| Evidence class | Meaning |
| --- | --- |
| AVAILABLE / VERIFIED IN PROJECT | Reproduced with documented implementation and observable result |
| RESEARCH DEMONSTRATION | Evidence in bounded research settings; not assumed generalizable |
| CONDITIONAL HYPOTHESIS | Plausible dependency chain, explicit uncertainty, measurable trigger |
| SPECULATIVE / UNKNOWN | No verified implementation for this objective; no guaranteed feasibility or date |

No year (2028, 2031, 2036, 2043 or 2046) entails a guarantee of model capability. Advancement depends on scientific evidence and reproducible tests, not schedule.

## Open choices before implementation

- Define minimal viable preservation target, purpose, retention and acceptable time burden.
- Decide if any real records may be included; synthetic test material is the default.
- Choose archive medium, access owner, key-management/recovery mechanism and export method.
- Specify objective completion criteria for backup, revocation and provenance tests.
- Distinguish independently assessed personality-model fidelity from philosophically unresolved personal identity or consciousness continuity.
- Make a fresh go/no-go decision before personal-data ingest, production rollout or publication of a larger research paper.

## Non-claims

This document establishes **no** deployed software, independent validation, verified archive completeness, prediction accuracy, consciousness, personhood, identity transfer, or entitlement to personal data. A publication of this methodology must not be mistaken for publishing any personal evidence.

## Framework trace

- [TerraNova public source-of-record policy](../../governance/source_of_record_policy.md)
- [TerraNova public boundary](../../governance/public_boundary.md)
- [FerrAI/TerraNova CIC v16 snapshot (context only)](https://doi.org/10.5281/zenodo.20732376)
