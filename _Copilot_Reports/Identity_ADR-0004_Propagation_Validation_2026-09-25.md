# ADR-0004 documentary propagation review — 2026-09-25

## Authority and baseline

Owner-directed architecture acceptance is recorded in [the signed record](Identity_ADR-0004_Acceptance_Decision_Record.md), commit 16b720c9cb9afdd60769dcad7b2c4d8c1e2e983c. It accepts technical ADR-0004 v1.1.0 at 82ef455. Metadata commit cca3f7ad0241111e468ef2b5a5d76e67de8d7cec (ADR v1.1.1 Accepted) is the parent baseline for this propagation. The author of this report also authored the propagation; this is not independent review.

## Changes and traceability

| Accepted source | Documentary propagation |
|---|---|
| Decision 1: authenticated polling | 07 §3, 09 §6.1, services schema: distinguish guarded active evidence from historical AlreadyCompleted; historical evidence cannot authorize a new Ready transition |
| Decision 2: minimal lifetime winner binding | 07 §3.5, 09 §11, machine contract: no secret/proof retention in winner tombstone, no timed deletion/reuse in MVP |
| Decision 3: C01/C02/C03 | 01/03/04/07/09: Credential-side authoritative guard, early immutable winner, ReadyFactId and acknowledgment Outbox, replay safe after later password change |
| Decision 3: availability cost | 08/OpenAPI: retryable password-change finalization-pending response; setup completion distinguishes CandidateSelected from ExistingWinner |
| Decision 4: restricted recovery | 07 §7, services schema, 09 §11, 11 §6 and recovery runbook: preparation/admission, two actions, fixed bounded job, current authorization, atomic audit and no bypass/cancellation |
| Operational obligations | 10 §4 and machine requiredConfiguration: finite values required but deliberately unset pending deployment policy approval |
| Verification obligations | 12/13: documentary checks separate from unimplemented runtime authorization/race/crash tests |
| Upstream provenance | ADR-0002 v1.7.1 references ADR-0004's earlier winner and protocol origin; ADR-0002 remains Proposed |

Blueprint 00–16 remain DRAFT; 05 is unchanged. Public REST remains 14 protocol operations implementing the same six business Commands/five Queries. Aggregate count stays five and public event count stays ten. The event schema is unchanged in this revision. RegistrationRecovery is an internal operator service, not a new public REST endpoint or Domain Event. PrepareRegistrationRecovery and GetRegistrationRecoveryResult are concrete Draft encodings of the approved trusted operations view/result lookup, not new recovery actions.

## Reproducible checks

`python tools/check_identity_blueprint.py`: **429/429 limited package checks passed**. The checks cover document metadata/version/status, relative links in numbered Blueprint documents, manifest/catalog/route correspondence, local references including service schemas, existing configuration correspondence, and selected valid/invalid fixtures. New fixtures exercise guarded versus historical provisioning evidence, required acknowledgment bindings, action/target/state mismatch, forbidden operator inputs, setup candidate outcome, scoped approval and unset operational policy values.

`git diff --check`: passed before publication. The local schema-fixture helper is deliberately partial; it is not a general JSON Schema validator. These checks do not prove authorization, cross-field binding, atomicity, time budgets, cryptographic properties, retention or race safety. Required runtime tests remain in 13 and ADR-0004 §4.6.

GFM parser: 20 changed/new Markdown documents, 33 tables and 253 body rows parsed with consistent token column widths. All 61 relative file links in those documents resolve; section anchors were not checked. No visual browser rendering review is claimed. No CI/Actions result is asserted by this report.

## Remaining gates

- Reviewer assessment of propagated service/message encodings and runbook; architectural approval does not automatically approve every field or deployment default.
- T16 shared PersonRegistered/PersonUpdated stream remains a separate open architecture item.
- ADR-0002 and applicable ADR-0003 acceptance, consumer inventory and migration/version policy.
- Required operational values, actual operator/worker grants, key/storage policy, on-call and incident tooling.
- Full OpenAPI/JSON Schema conformance, complete applicable 065 validation and contract compatibility.
- Implementation and runtime/security/race/failure tests; none is claimed implemented or passed by this report.

PR #5 remains Draft. Nothing here certifies generation readiness or authorizes merging main. PRs #1–#4 remain superseded rather than additional merge paths. The original acceptance record is not modified by propagation.
