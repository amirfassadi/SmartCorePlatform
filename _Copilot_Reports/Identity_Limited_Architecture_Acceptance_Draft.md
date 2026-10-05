# Identity registration: limited architecture acceptance record (DRAFT v6)

**Status:** Unsigned review candidate; no architectural approval or implementation permission.  
**Governance record number:** PENDING assignment under 051.  
**Authority:** 051 §7.  
**Decision owner:** Amir (@amirfassadi), project and architecture owner.  
**Prepared:** 2026-09-29 (Asia/Tehran). Approval and effective dates: PENDING.

This is a decision form, not a claim that its prerequisites are complete. Slice 0 evidence preparation may begin now. Implementation of Slice 1 or Slice 2 additionally requires all four applicable 064 validation gates and the 065 quality-gate evidence for an explicitly defined coherent package. Owner approval alone is insufficient; no bounded package or exception is adopted by this form.

## 1. Exact source references

| Repository | Current review input, not accepted | Accepted candidate SHA |
| --- | --- | --- |
| SmartCorePlatform | PR #10 integrated review input `630a22da53195a87d780aaf3c867bdd359eab83a`; proposed #5–#9 content is in this review chain | PENDING: pin the final reviewed coherent output; incorporated #6/#7 text is not approval |
| SmartCoreIdentity | PR #1 `ee9ffb767ed84165557793d8583b0750d887027b` | PENDING: pin independently at decision time |

PR #8 (`6c50cb92cd9c15b48f5bf4d13e128fccfd620bb2`) compares T16 options. PR #9 (`db88bb07a5dfeb8498607bb3e20df546bd6a38e2`) proposes SESSION/S2 options. These are background review inputs only; neither closes its decision or becomes normative through this record. Recheck all heads before signing. Identity PR #1 is not part of the Platform commit.

**Cross-repository discrepancy table:** partial evidence exists in the publication and field reviews; selected authoritative source and final reconciliation remain PENDING. For every difference record the two exact source locations, chosen authority, required correction, affected consumer and disposition. A later commit does not automatically annul a signed scoped decision. Changes affecting accepted clauses, schemas, dependent documents, invariants or internal contracts require documented impact review and, when needed, an addendum. The addendum must state whether its baseline SHAs changed. Impact-review owner and register: PENDING.

## 2. Sequencing decision: ADR-0002 v1.8.0

**Separate owner disposition: PENDING.** ADR-0002 v1.8.0 sequencing is incorporated in the PR #10 review input, not accepted. Before limited acceptance, confirm its versioned text in the exact final Platform candidate and the owner must review the criterion-by-criterion mapping from v1.7.1. The owner records acceptance, revision or rejection of the architecture-versus-runtime sequencing separately here: PENDING attributable record.

Pre-approval evidence includes transaction boundaries, invariants, concrete failure-point test plans, cross-document/consumer review, Architecture Validation Review and applicable structural validation. Executed race/security/crash tests belong to implementation and verification after architectural approval. An unexecuted test is never marked passed. ADR-0003 criteria are evaluated independently; PR #6 does not amend ADR-0003.

## 3. Decision 8, the internal work item and T16

ADR-0002 Decision 8 requires the ownership triple, PendingCredential workflow and internal Credential-provisioning Outbox item to be committed together. That work item is not a public event or a replacement for PersonRegistered. Its versioned internal contract carries an opaque protected-material reference, not a plaintext password. Contract path, version, retention and compatibility review: PENDING.

Decision 8 separately requires confirmation of an active Credential, the one-time transition to Ready and enqueueing PersonRegistered in the same transaction. OccurredAt denotes that Ready transition; OwnershipCommittedAt denotes the earlier ownership commit. The reviewed public payload and affected consumer disposition are prerequisites to accepting this architecture, even if its implementation occurs in a later slice.

This record does not choose PersonRegistered/PersonUpdated publication or delivery ordering, consumer replay rules, or T16 option A/B. Inspect Decision 8 for wording that could imply such a choice; record any ambiguous clause and its correction here: PENDING review. T16 cannot change Decision 8's Ready-time fact merely by selecting a delivery contract.

## 4. Decision-by-decision scope proposed for owner review

All statuses below remain **Proposed**. An accepted row needs an owner decision, reviewed evidence and exact scope; an empty row conveys no permission. Do not mark the entire ADR-0002 Accepted while other decisions remain Proposed.

| Source | Architectural scope to review | Implementation slice | Boundary / open issue | Evidence | Owner disposition |
| --- | --- | --- | --- | --- | --- |
| ADR-0002 D9 | Minimal verified mobile OR email, DisplayName/password; challenge, expiry, online attempts, durable bounded replay and pre-commit protected material | Slice 1; commit binding in Slice 2 | Challenge proof is not an authenticated Session; exact API/security values require review | PENDING | Proposed |
| ADR-0002 D8 | Entire architectural decision: atomic PendingCredential/work item, protected material, idempotent provisioning, secure completion, Ready fact and public event timing | Slice 1 material preparation; Slice 2 ownership commit; subsequent provisioning/Ready slice | Public delivery order remains T16. Full architectural evidence for D8 is required even if implementation is phased | PENDING | Proposed |
| ADR-0002 D1 | Atomic Person, Personal Organization and Owner Membership creation; no partial ownership | Slice 2 | Transaction invariant and rollback boundary | PENDING | Proposed |
| ADR-0002 D3 | Owner is Membership role attribute | Slice 2 | Future roles are not an MVP command obligation | PENDING | Proposed |
| ADR-0002 D7 and D7.1 | Narrow RegisterPerson cross-Aggregate exception and RegistrationApplicationService ownership | Slice 2 | No general multi-Aggregate exception | PENDING | Proposed |
| ADR-0002 D2 | Authentication versus business authorization boundary | Constraint where registration/authentication responses expose context; owner to classify as required constraint or context | No business authorization grant from registration | PENDING | Proposed |
| ADR-0002 D4 | Person-centric human Identity v1.x boundary | Owner to classify as required constraint or context | Future non-human identities not authorized by this record | PENDING | Proposed |
| ADR-0002 D5 | Identity event ownership and LoginFailed classification | Relevant public-event slice; owner to specify | Event ownership is not delivery ordering | PENDING | Proposed |
| ADR-0002 D6 | Documentation of future identity types | No MVP implementation | Independent future scope; not deferred merely because of T16/SESSION | PENDING | Proposed |
| ADR-0003 D1 and D2 | Direct Active initialization of Personal Organization and Owner Membership in MVP | Slice 2 | Future transition commands excluded | PENDING | Proposed |
| ADR-0004 | Previously accepted scoped provisioning/recovery protocol | Applicable dependent slices | No new approval or test PASS granted here | Prior scoped acceptance record | Accepted in prior record |

If all of D8 cannot pass architectural review, revise and version the ADR under 051 before approving a narrower decision. Do not call a change to decision scope an editorial split.

## 5. Pre-signature evidence

| Requirement | Responsible person | Gate | Evidence / status |
| --- | --- | --- | --- |
| Cross-repository discrepancy and consumer compatibility dispositions | PENDING | Before applicable slice approval | PENDING |
| Decision mapping above, D8/T16 wording inspection, transaction design and invariants | PENDING | Before applicable slice approval | PENDING |
| Architecture Validation Review for both pinned inputs | PENDING | Before signature | Not done |
| Applicable 065 §5 Structural Validation on exact candidate: files, sections, headings, references, versions, statuses and 064 package structure | PENDING | Before signature | Not done; limited package script is insufficient |
| ADR-0003 criteria: document synchronization, architecture review, structural validation and accepted references | PENDING | Before ADR-0003 scoped approval | Not done |
| Separate owner disposition of #6 criterion mapping | Amir | Before limited acceptance | PENDING |

For the structural report record executor, method, coverage, results, excluded checks and both relevant SHAs. A separate reviewer is preferred, not required by 065 §5. Full 065 §13 governance/quality gates and READY_FOR_GENERATION are separate. No PASS is asserted here.

## 6. Failure-point plans (not executed results)

The design review must name the failure point, invariant, expected observation, test layer and responsible implementer. Actual reports must give code SHA, environment, commands and outcomes before the related code merge.

| Slice | Failure point | Expected invariant to verify |
| --- | --- | --- |
| 1 | Proof at or after absolute expiry | Expired verification cannot authorize an ownership commit; precise boundary is defined in API/security contract |
| 1 | Attempt/resend limit or unknown contact | Bounded online attempts and non-enumerating pre-proof responses |
| 1 | Successful proof before ownership commit | No Person, ownership triple, active Credential or authenticated Session yet |
| 1 | Same consumed proof, same bound request, within bounded replay window | Authorized replay retrieves only the already committed registration result; never creates a second triple or Session |
| 1 | Different bound request/proof, or replay after window | Reject safely and audit mismatched payload; no new ownership from consumed proof |
| 1 | Protected material staging, expiry and cleanup | Raw password not persisted; password/code absent from logs and Outbox; only opaque durable reference crosses the ownership commit |
| 2 | Crash before ownership commit | No committed Person, Personal Organization, Owner Membership, registration workflow or registration-owned Outbox/material reference; staged material follows bounded cleanup |
| 2 | Crash after commit before internal Outbox processing | All five committed components recover; protected material reference remains valid; replay cannot create a second triple or active Credential |
| 2 | Two registration attempts with same verified normalized contact | Unique Person/contact ownership; safe retry resolves existing outcome when authorized |
| 2 or later provisioning slice | Two workers/duplicate provisioning delivery | At most one active Credential and one legitimate Ready transition; same key returns existing result, different payload is rejected and audited |
| Later Ready slice | Active Credential confirmed; failure around Ready commit | Ready transition and PersonRegistered enqueue are atomic and occur once; delivery order versus PersonUpdated is not asserted |
| 2 | Failure creating Organization or Membership | Transaction rolls back entire ownership triple, workflow and Outbox; no partial ownership |
| Later authentication slice | Person remains PendingCredential | Password login and Session creation denied until Ready and active Credential |

The later-slice rows are obligations of accepting D8, not a claim that Slice 2 already implements them. Include ADR-0004 guard/acknowledgment and race/failure tests in the relevant later verification plan.

## 7. Scoped permission, post-approval obligations and exceptions

Slice 0 (pin sources, resolve discrepancies, map decisions, conduct review and produce structural evidence) starts before approval. After the owner signs exact scope on two pinned SHAs and all applicable pre-signature evidence is complete, only the explicitly accepted Slice 1/2 architectural scope may be implemented after all applicable 064/065 implementation gates are evidenced. If Slice 2 evidence lags, a scoped Slice 1 approval still needs an explicitly governed scope and all applicable gate evidence; a later Slice 2 addendum identifies its baseline and additional evidence. If D8 as a whole is a prerequisite and cannot be approved, Slice 1 cannot claim D8 acceptance by implementation partition alone.

| Later obligation | Responsible person | Gate | Evidence |
| --- | --- | --- | --- |
| Execute applicable Slice 1 tests above | PENDING | Before Slice 1 code merge | PENDING run report |
| Execute applicable Slice 2 tests above | PENDING | Before Slice 2 code merge | PENDING run report |
| Decide T16 and shared consumer contract | PENDING | Before dependent public event publication/consumer slice | PENDING attributable decision |
| Decide SESSION in separate ADR, complete S-01–S-10 and propagate accepted contract | PENDING | Before Session/refresh slice | PENDING |
| Complete remaining applicable 065 categories and §13 quality gate | PENDING | Before READY_FOR_GENERATION | PENDING |
| Complete production/security/runtime and operational verification | PENDING | Before applicable release | PENDING |

This record does not grant READY_FOR_GENERATION, overall 065 §13 PASS, deployment approval, runtime test PASS or PR merge. A PR merge alone is not architecture approval.

## 8. Alternatives and attributable decision

Owner to accept or revise each reason: (1) Waiting for the whole roadmap blocks an independent registration slice; (2) accepting all ADR-0002 decisions at once obscures unresolved scope; (3) requiring executed runtime tests before 051 §7 approval reverses the governance lifecycle, while a concrete plan remains required; (4) splitting D8 only to defer T16 is unnecessary if the event fact/timing and delivery-order boundary survive review.

| Field | Value |
| --- | --- |
| Platform candidate SHA and Identity SHA | PENDING / PENDING |
| Accepted ADR-0002 decisions, exact scope and remaining Proposed decisions | PENDING |
| Accepted ADR-0003 scope and criteria evidence | PENDING |
| #6 sequencing owner decision | PENDING |
| Owner approval, capacity, date and effective date | PENDING |
| Attributable repository record/commit | PENDING |
| Evidence executor, security reviewer, operations owner and later test owners | PENDING |

A cryptographically signed commit is desirable but is not a new requirement of 051. The owner must explicitly record the decision; approving or merging a PR by itself does not fill this table.

## 9. Slice 0 publication review — 2026-10-04

See [publication review](Identity_Slice0_Publication_Review.md) and the uploaded Slice 0 evidence reports. This remains unsigned. In particular, 064 §§9/12/15 require all four validation gates before implementation. This form’s limited Slice 1/2 permission must not be used to bypass that rule: either provide the applicable gate evidence for an explicitly bounded package or obtain an explicit governed disposition/amendment before implementation. ADR-0002 sequencing alone does not amend 064. The partial structural checker omits required section/heading validation, so it cannot close 065 §5. No gate is marked complete by this addendum.

## 10. Gate follow-up — 2026-10-04

[Gate and foundation review](Identity_Slice0_Gate_Review.md) maps 064/065/066 and records structural coverage, foundation findings and remaining evidence. This revision corrects the implementation-permission wording; it does not approve a narrowed Blueprint or amend any foundational standard. Runtime implementation verification remains separate from pre-implementation documentary gate evidence.

## 11. Next decision packet — 2026-10-04

[Prepared choices and gate work](Identity_Next_Decision_Packet.md) replace stale preparation assumptions with exact integrated inputs. The recommended full-MVP single-Blueprint scope is not adopted; this limited form remains an alternative unsigned scope proposal. Field review and expanded structural evidence exist, but neither constitutes complete gate evidence. Accepted SHAs, attributable decision and implementation permission remain PENDING.
