# Identity architecture alignment review — preliminary findings

Status: DRAFT / NOT an Architecture Validation Review PASS
Date: 2026-09-28
Candidate: SmartCorePlatform PR #6 at its review branch; source branch derives from integrated Identity PR #5 commit `91375b192dd0ec778529c4c7d8a785c94231269a`.
Purpose: Identify specific 026/027/057/059 and Identity Blueprint consistency work before ADR-0002's architecture gate can be marked complete. No runtime, consumer or 065 result is asserted.

## Reviewed relationships

| Source | Observed alignment | Remaining finding |
|---|---|---|
| 026 §8/§9 and Identity/06 §4.2 | PersonRegistered OccurredAt follows Ready; OwnershipCommittedAt records earlier core commit. LoginFailed is a Security Event. | Consumer inventory and timing/payload compatibility remain unevidenced. T16 ordering is separately open. |
| 027 §14/§17.1 | Failed authentication can publish a Security Event; RegisterPerson exception is narrowly proposed and pending acceptance. | No general multi-Aggregate permission inferred. |
| 057 §8/§9 | Ownership triple atomic; PendingCredential workflow/Outbox in the same commit; direct Active Organization/Membership lifecycle and future transitions stated. | ADR-0002/0003 references remain explicitly Proposed, correctly awaiting governance. |
| 059 §6/§7 and Identity/00, Identity/08, Identity/14 | Verification precedes ownership; Ready and active Credential gate login. | **A1:** 059 §6 still diagrams an optional “Create Initial Session” and “Return authenticated result” immediately after Ready, whereas the active proposed Identity/00 §2 and Identity/14 §2 require explicit login after registration with no initial authenticated Session. Align 059 before approving contract consistency. |
| 059 §7 and Identity/00 §3 | Login creates Session and issues tokens. | **A2:** 059 §7 says “No domain data is modified during login,” but its own flow creates a Session Aggregate and the event catalog includes LoginSucceeded/SessionCreated. Clarify what state is meant; do not assert no state modification. |
| 059 final Event Timing Note and ADR-0004 Decisions 1–4 | Ready and PersonRegistered timing agree. | **A3:** The final note says “Post-commit recovery and operational handling are implementation-specific.” ADR-0004 now accepts specific polling, durable guard/acknowledgment and restricted administrative recovery architecture. Qualify this note to mean only delegated deployment parameters remain implementation-specific. |

A1–A3 are documentation alignment findings in the integrated branch, not proof of runtime defects. [Draft PR #7](https://github.com/amirfassadi/SmartCorePlatform/pull/7) proposes the 059 v1.5.1 corrections on a separate branch. They remain open in the integrated base until reviewed and merged; PR #7 itself is not architecture approval. Resolve them in the platform proposal and recheck downstream examples/contracts. Avoid treating a versioned review report as approval of the underlying proposal.

## Evidence still missing for ADR-0002 architecture gate

- An explicit consumer inventory for PersonRegistered, PersonUpdated and LoginFailed, including schema/timestamp/order expectations and migration decisions. Searching only this repository cannot prove that deployed or external consumers do not exist.
- Reviewed exact candidate revision across narrative, machine, OpenAPI, service/event JSON schemas, including a compatibility decision for A1–A3 and T16.
- Documented Architecture Validation Review signed by the responsible authority after findings are resolved.
- Independently reproducible applicable Structural Validation under 065 §5 for the exact candidate. The limited Python package checker does not implement the entire 065 validator and has not been executed as part of this report.
- Separate disposition of ADR-0003's criteria and of Session policy. Neither is satisfied by ADR-0002 sequencing clarification.

These findings keep GOV open. They should be resolved before an acceptance record marks ADR-0002's cross-document consistency or architecture review criteria complete.
