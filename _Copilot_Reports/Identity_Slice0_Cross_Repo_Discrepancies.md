> Revision note: original findings below describe the uploaded candidate; the publication review supersedes dispositions it explicitly corrects.

# Slice 0 evidence — cross-repository discrepancy table

Prepared: 2026-10-04. Status: DRAFT review evidence; not an architectural acceptance, not implementation permission. The uploaded review was local-only. Its publication review and corrections are recorded in Identity_Slice0_Publication_Review.md.

Inputs: SmartCorePlatform candidate (local merge `82a400d` of #5 `91375b1`, #6 `1e57082`, #7 `7ccba70`, #8 `6c50cb9`, #9 `db88bb0`; base `main` `9fa0266`) and SmartCoreIdentity PR #1 `ee9ffb767ed84165557793d8583b0750d887027b` (base `main` `f72a4fdf9f29edd3970b4bd719bfbf8040089534`). Authority column follows the Identity plan: Platform owns schemas and contracts; Identity owns behavior tests.

| ID | Platform source | Identity source | Difference and effect | Governing source | Required correction | Consumer affected |
|---|---|---|---|---|---|---|
| D1 | ADR-0002 header: v1.7.1 at `91375b1`, v1.8.0 at `1e57082` | registration/README.md:9, 28–33; source-manifest.json (platformReference `91375b1`) | Identity pins PR #5 only. Its gov-review-dossier.md:42 acknowledges PR #6 (v1.8.0) as a separate draft, so this is a documented staging, not hidden drift. Once #6 enters the candidate the pin is stale. | Platform candidate | Re-pin Identity to the final candidate SHA at decision time | Identity implementation plan |
| D2 | 13_Testing.md (65 lines) defines no R-ids | validation-and-tests.md defines R01–R20 | Behavior test catalogue exists only in Identity | Identity for behavior tests | Add a pointer or mapping in Platform 13_Testing, or record that R01–R20 is authoritative | Test planning |
| D3 | 10_Configuration:37–38 has sessionLifetimeSeconds 86400 (absolute) and accessTokenLifetimeSeconds 900; no refresh lifetime or rotation row | capability.validation_notes.md 0.1.7–0.1.11 records owner-selected S2 direction; gov-review-dossier.md:69 lists SESSION as Open | The two numbers are already in Platform config, but refresh, rotation, revocation and BFF policy are not. Open/selected status differs between documents. | Open until owner accepts SESSION | Close SESSION, then propagate to 10, 08, openapi, machine spec | Refresh/logout slices |
| D4 | package directory holds 09_Persistence_CHANGELOG.md, Registration_Recovery_Runbook.md, TASK_Identity_Foundation_Hardening.md, openapi.yaml, events.schema.json, services.schema.json | README.md:35 requires using those schemas | 064 §7 lists 17 documents + machine spec; extras are not standardized | 064 §7 | Owner decision: standardize schemas as package members or move working docs out | Validator, generators |
| D5 | 09_Persistence 134 lines (v1.3.0) | none | Down from 1447 lines on `main`; legacy requirements outside #1–#4 need review | Platform | Section-by-section comparison of v1.0 vs v1.3.0 | Persistence implementer |
| D6 | PR #6 v1.8.0 sequencing text and PR #7 059 corrections are separate drafts | acceptance draft v4 §1 expects one coherent tree | Local merge is Git-clean only; not yet reviewed semantically | Owner | Publish one candidate branch and re-run D-checks | Everyone |
| D7 | PR #1 head `ee9ffb7` | capability.validation_notes.md:12 names Identity PR #1 at `f96f11f` | Review baseline in the notes is older than the PR head | Identity | Update baseline SHA or mark historical | Reviewers |

Not examined: field-level equality between openapi/services/events schemas and the Identity docs; consumer repositories.
