# Slice 0 upload review and publication corrections

Date: 2026-10-04 (Asia/Tehran). Status: DRAFT review evidence; no architectural decision accepted.

## Source provenance

Uploaded bundle branch tip: `752e2a8d80c1303d9f91bd197eca1aca8c400f36`; original integrated merge: `82a400d27cbb4d01966ed0c19ef27ed9d764df28`. Five standalone Markdown reports match the bundle copies. README mentions two patches, but the ZIP contains no patch files; the bundle contains the reports and checker, so publication does not depend on those missing patches.

Reviewed Platform sources: main `9fa0266b381b8f185af54a51747fefff6599fa92`; #5 `91375b192dd0ec778529c4c7d8a785c94231269a`; #6 `1e570825c74efbeee49b2ee864719992af5397ff`; #7 `7ccba7035572913670af43e19818958103ce345d`; #8 `6c50cb92cd9c15b48f5bf4d13e128fccfd620bb2`; #9 `db88bb07a5dfeb8498607bb3e20df546bd6a38e2`. Identity review input: `ee9ffb767ed84165557793d8583b0750d887027b`.

Publication uses a GitHub-created commit with #5 as first parent and #6–#9 as additional parents, containing the integrated bundle tree and proposed corrections. Its commit identity differs from the locally generated merge; no assertion of identical history is made. GitHub branch/PR and returned commit identify the published review state. Existing branches and main are preserved.

## Comparison with the user's prior summary

The archive contains all five reported outputs and the bundled `tools/slice0_structural_065.py`. The local-only publication claim, incomplete architecture/semantic/field-level review, and 88 PASS / 6 WARN counts agree with the delivered files. The count was reproduced with the declared dependencies. GitHub API now verifies Platform #1–#4 closed with `merged_at=null`; #5–#9 and Identity #1 remain open at the pinned heads.

## Corrected semantic dispositions

| Uploaded finding | Reviewed disposition and proposed correction |
|---|---|
| P4b: no verified-contact reference on workflow | Workflow already uniquely references PersonId; Person stores the selected verified contact. This is a representation ambiguity, not proven absence of a recovery route. ID-09 §7 now explicitly requires authoritative resolution through that durable association and rejects caller-supplied recovery destinations. No duplicate contact field or new public schema is introduced. This proposed representation is visible for architecture review. |
| P7: no explicit prohibition on reopening ownership | The uploaded report correctly calls this Partial: existing retry/recovery preserves ownership. ID-09 §6 now restores the explicit SHALL NOT reopen/rollback/re-run clause. Replay reads the prior result; it does not create ownership again. |
| P15: Event Store/Event Sourcing non-goal absent | ID-09 §7 already excludes generic IdentityEvents/AuditLogs stores; ID-06 §5.5 delegates delivery mechanics. ID-09 §1 now makes Event Sourcing and historical Event Store exclusions explicit, while preserving mandatory Outbox and proposed delivery guarantees. This is a clarity restoration, not proof the entire prior intent was absent. |
| A1: pre-Ready profile update | Intentionally replaced by the current Ready-gated command causal order in ID-03 §9.1. No delivery-order decision is inferred. |
| Broad 09 compression | Still open. Most of the old file includes rationale and historical changelogs, so line count alone is not a loss metric. A full requirement-level review is still needed; this publication does not certify every legacy clause preserved. |

The upload's partial verification levels remain explicit. This follow-up read ID-09 in full, ID-03 §9.1, ID-06 envelope/Ready/ordering clauses and ADR-0002 Decisions 8–9 passages. It does not upgrade every keyword-located row to independently verified. “Preserved” in those rows retains the upload's limited meaning.

## Cross-repository amendments

D1: Identity deliberately pins #5. The integrated review is not yet an accepted baseline, so changing its authoritative pin now would imply adoption. Re-pin after candidate review with a separate recorded disposition.

D2: ID-13 §4 now points to the immutable Identity R01–R20 catalogue and maps scenario ranges. Both catalogues remain Draft requirements; neither repository has executed those behavioral tests. No exclusive new authority is invented for the external test list.

D3: 900-second access and 86400-second absolute Session values exist in proposed Platform configuration. S2/BFF/rotation/revocation still require review/propagation; T16 and SESSION remain open.

D4: six extra files are permitted during drafting by 064 §7. WARN is a published-package membership question, not a current drafting FAIL. Schema validation demonstrates well-formed schemas/OpenAPI, not approved package membership or narrative equality.

D5: broad legacy review remains open. D6: published candidate enables review; a clean merge is not semantic acceptance. D7: `f96f11f` is an earlier documentary review baseline, not necessarily an erroneous claim of current head. Preserve it as history and identify the current input above.

ADR version references were not globally replaced. Changelog mentions remain historical, and contractual references require semantic/adoption review. No updated Accepted status or accepted-version pin is fabricated.

## Additional governance finding G1

064 §§9/12/15 require four validation gates before implementation and a complete package. The unsigned limited-acceptance draft §7 suggests Slice 1/2 may start after scoped evidence/owner approval. The draft must explicitly reconcile that effect with 064. Either supply the applicable validation evidence for a bounded package or obtain a governed exception/amendment before implementation. This report does not choose an exception or change the standard. ADR-0002's architecture-versus-runtime sequencing does not itself waive 064.

## Verification scope and checker corrections

`tools/check_identity_blueprint.py`: 430/430 limited checks passed on the corrected tree.

`tools/slice0_structural_065.py`: 88 PASS, 6 WARN, 1 INFO reproduced. It omits mandatory section/heading coverage from 065 §5; therefore even full Structural Validation remains incomplete. Schema checks do validate schema syntax/OpenAPI structure, so their evidence is stronger than parsing alone, but not behavior, examples, or field equality. V-001/V-005 checks only detect repository/producer presence, not complete rule conformance. S6 compares counts to a pinned hardcoded expectation, not dynamically to ID-14 prose. Labels and exclusions now say that explicitly. Missing machine specification and missing versioned changelog now yield FAIL rather than a traceback/silent skip. Direct dependency versions are in `tools/slice0-requirements.txt`.

Negative controls: missing 05, mismatched ID-09 header version, and missing machine specification must exit nonzero. They are checker controls, not service tests. No R01–R20, architecture gate, consumer audit, full 065 or generation PASS is claimed.

## Reviewable changes

ID-09 1.3.1 and ID-13 1.1.1 plus matching machine manifest; five imported reports with historical-scope notes; this publication review; limited-acceptance draft addendum; checker/dependency corrections. All Blueprint statuses remain DRAFT. Identity repository remains unchanged. Remaining findings above are not silently converted to owner approvals.
