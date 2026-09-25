# Acceptance Decision Record — ADR-0004 (Identity Credential Provisioning Protocol)

## Metadata

- Document type: Acceptance Decision Record (governance artifact, not an ADR itself)
- Records: the Approval step of `051_SmartCore_Governance_and_Decision_Model.md` §7 (Proposal → Review → Discussion → Revision → **Approval** → Implementation → Verification → Documentation Update)
- Applies to: `ADR-0004_Identity_Credential_Provisioning_Protocol.md`, Version 1.1.0, Decision Level 4 — Architectural Change (per 051 §5)
- Pinned source commit: PR #5 (`docs/identity-blueprint-completion`) at `82ef455eda661064b69bd6f2f080010a341d014e`
- Related: ADR-0002 Decisions 8–9 (remains Proposed; this record does not accept ADR-0002 itself), `Identity_Decision_8_9_Traceability_Review.md`, `Identity_Integrated_Proposal_Validation_2026-09-24.md`
- Date of this record / signing: 2026-09-25 (Asia/Tehran)
- Status: Signed — scoped architectural approval recorded at the owner's explicit direction

## 1. Purpose

ADR-0004's Acceptance Criteria and Consequences section require sign-off from architecture/security and the accountable operations/support owner. This project has a single maintainer, so both roles are held by the same person. This record makes that authority explicit rather than implying approval from the presence of a commit in the proposal PR.

This record does not re-derive, re-argue or restate the technical content of ADR-0004. It records who is deciding, in what capacity, exactly what is accepted, what is not accepted and what happens next.

## 2. Decision-making authority

I, @amirfassadi, am the sole maintainer and repository owner of `amirfassadi/SmartCorePlatform`. For 051 §7's Approval step and ADR-0004's Acceptance Criteria, I act as both:

- the architecture/security approver; and
- the accountable operations/support owner.

No independent external reviewer has evaluated this proposal. The traceability review and design work disclose that the reviewer also authored the integrated proposal. This record resolves the approval-authority question through an explicit accountable owner decision; it does not claim that independent review occurred.

## 3. What is accepted by this record

This signature accepts the following as architectural decisions, not as verified, tested or propagated implementation:

- **A01** — Authenticated polling (`EnsureInitialCredential` / `GetInitialCredentialResult`) as the selected mechanism for Credential-confirmation reconciliation, per ADR-0004 Decision 1.
- **A02** — Registration-lifetime deduplication with minimized retention (no secrets or proof material), per Decision 2.
- **A03 / C01–C03** — The durable pre-Ready mutation guard, explicit `AcknowledgeRegistrationReady` release protocol and three-invariant distinction (C01 one active Credential, C02 immutable early winner fixed at Credential commit, C03 no independent replacement before Ready), per Decision 3, including the availability cost of temporarily blocking post-Ready password changes pending acknowledgment.
- **Decision 4** — The design, not implementation, of `AdminRecoverStalledRegistration`, its two actions (`InvalidatePreCommitAttempt`, `ReconcileCommittedRegistration`), authorization model, state-effect table, mandatory append-only audit and outcome/support-procedure design in §§4.1–4.6; including the explicit exclusion of post-commit cancellation in §4.1.
- The traceability review's §§3–5 classification of upstream Proposed requirements (U), delegated Blueprint detail (D), and additional architectural choices requiring this sign-off (A), as the basis for understanding how the above go beyond, but do not contradict, ADR-0002 Decisions 8–9. This does not approve T16 or other unlisted policy defaults merely because they appear in that classification.

## 4. What is explicitly NOT accepted by this record

- **ADR-0002 itself remains Proposed.** This accepts ADR-0004's protocol built on Decisions 8–9, not ADR-0002 retroactively. ADR-0003 is likewise not accepted by this record.
- **T16**, the shared PersonRegistered/PersonUpdated per-Person event stream, remains a separate open architecture item.
- **No propagation is certified complete at signing.** Identity 01/03/04/06/07/08/09, OpenAPI/machine YAML/JSON Schema, and 10/11/13/12 have not yet been aligned with ADR-0004. This record authorizes that work; completion must be evidenced by subsequent changes/review.
- **No runtime verification has occurred.** ADR-0004 §4.6's required authorization/race/failure tests remain unimplemented and unverified at signing.
- **No generation readiness is granted.** This supplies 051 §7 architectural approval only for §3's listed items; no document is thereby READY_FOR_GENERATION. Unaccepted upstream decisions and all remaining validation/deployment gates continue to apply.
- **PR #5 remains Draft.** Approval does not make the PR ready, merge it, or change main.

## 5. Effect of signing

1. ADR-0004's Status may change from Proposed to Accepted, with Approval Date 2026-09-25 and Change History referencing this record's filename and introducing commit.
2. Blueprint/API/machine-contract propagation may begin on an explicit accepted architectural basis.
3. Commit this record to `_Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md` for attributable governance evidence.

Architectural acceptance and later implementation/verification/rollout gates are distinct. Unchecked propagation or test items are retained as obligations, not asserted complete or silently waived.

## 6. Signature and provenance

```
Decision:  ACCEPTED — items listed in §3 only, subject to §4
Signed by: @amirfassadi
Capacity:  Architecture/security AND accountable operations/support owner
           (sole maintainer, per §2)
Date:      2026-09-25 (Asia/Tehran)
Commit ref: The commit introducing this file; pinned explicitly in the subsequent
            ADR-0004 acceptance metadata/history update.
```

Recorded by the assistant at the owner's explicit instruction in the project conversation; the authenticated GitHub connector returned login `amirfassadi` when publishing. This is an owner-directed recorded signature, not a claim of GPG/SSH commit signing or independent identity attestation. No cryptographic signature has been supplied by the assistant.

The introducing commit is discoverable with `git log --diff-filter=A -- _Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md`. Its hash cannot be embedded into its own content without changing that hash; the subsequent ADR reference provides the explicit immutable binding.
