# Identity Decisions 8–9: independent PR #1 review and traceability

Status: Review findings / OPEN architectural questions; no approval or remediation decision.
Review date: 2026-09-24.

## 1. Evidence and scope

Independently read the complete two-file diff of PR #1: base `9fa0266b381b8f185af54a51747fefff6599fa92` to head `725ed588cc98a49ffebb3da1b43158226d72f567`. GitHub metadata confirms five commits, two changed files, open and unmerged. Read Decisions 8–9 and the relevant Blueprint contracts at PR #5 head `4f13efff84b377e2aca32d8405492737e258eb56`. PR #5 is independently based on the same main commit; it incorporates content, not the ancestry of PRs #1–#4.

Sources:

- [PR #1 diff](https://github.com/amirfassadi/SmartCorePlatform/pull/1/files)
- [Pinned PR #1 ADR](https://github.com/amirfassadi/SmartCorePlatform/blob/725ed588cc98a49ffebb3da1b43158226d72f567/SmartCore_Platform_Docs_v1/ADR-0002_Identity_Foundation_Clarifications.md)
- [Pinned PR #5 ADR](https://github.com/amirfassadi/SmartCorePlatform/blob/4f13efff84b377e2aca32d8405492737e258eb56/SmartCore_Platform_Docs_v1/ADR-0002_Identity_Foundation_Clarifications.md)
- [Pinned Blueprint](https://github.com/amirfassadi/SmartCorePlatform/tree/4f13efff84b377e2aca32d8405492737e258eb56/SmartCore_Platform_Docs_v1/Identity)

This is an independent reading of source changes, not independent organizational approval: the reviewer also authored the integrated proposal. Prior use of “reviewed proposals” in the integrated report must not substitute for this evidence or an architecture review. No PR is closed, merged or accepted by this report.

## 2. PR #1 findings

| Finding | Direct evidence | Assessment |
|---|---|---|
| Verification material and replay | ADR Decision 9 adds opaque verificationSessionId, absolute expiry, bounded cleanup, atomic material ownership transfer, keyed online replay proof and retention within original validity | Matches stated scope; concrete interval/record/API design is explicitly delegated |
| Lost response / second password | Decision 9 routes a verified PendingCredential conflict to distinct Decision 8 setup; second attempt material must be invalidated/disposed and cannot replace existing material | Matches scope; does not define a general password reset |
| Timestamp semantics | Decision 8 and 026 §8 define Ready-time OccurredAt and separate OwnershipCommittedAt; distinct future commit signal | Consistent between both changed files; consumer compatibility remains unproven |
| Metadata / history | ADR v1.6, Level 4 for Decisions 8–9, repaired history table; 026 v1.1.2 history names timestamp change | Matches diff; all acceptance gates remain open |
| Inherited compatibility overclaim | ADR v1.6 Backward Compatibility still says all changes are additive/clarifying and no breaking changes are introduced | Must not endorse this claim. PR #5 v1.7 corrects it; it is not corrected in PR #1 itself |
| Inherited machine-file provenance claim | ADR v1.6 says a supplied capability_machine.yaml already has a governance block | Not established by the tracked baseline. PR #5 correctly distinguishes newly tracked machine files from unseen attachments |

Conclusion: the additions satisfy the declared documentary scope. This is not acceptance of the whole ADR, consumer migration, machine compatibility or the inherited claims above. If PR #1 is selected as the merge path, its unresolved claims require correction there; a correction existing only in PR #5 cannot be attributed to PR #1.

## 3. Classification

**U** = explicit requirement in the upstream *Proposed* ADR, not an accepted decision.
**D** = delegated Blueprint detail; proposed concrete value/representation, not an ADR mandate.
**A** = additional architectural choice or stronger invariant requiring explicit review/disposition.
Rows may contain both an upstream obligation and a separately classified implementation choice. Agreement with an obligation does not approve every means of implementing it.

## 4. Requirement mapping (PR #5 snapshot)

| ID | Requirement / choice | Upstream source | Blueprint / machine location | Class and open boundary |
|---|---|---|---|---|
| T01 | Durable registrationId, PendingCredential/Ready; no sixth Aggregate | D8 “Boundary and state” | 01 §9; 03 §9.1; 09 §§5–7; machine.workflow | U; actual record layout is D |
| T02 | Ownership triple + workflow + provisioning Outbox commit atomically | D8 “Reliable provisioning and retry” | 04 §4.1; 09 §5.1; machine.workflow.initialTransaction | U; local store topology/DDL remain implementation evidence |
| T03 | Gate login/Session on Ready and active Credential | D8 “Boundary and state”; D9 final paragraphs | 04 §4.2; 08 §§3–5; machine.workflow.authenticationRequires | U; explicit extension to refresh is a Blueprint policy requiring review |
| T04 | Deduplicate registration deliveries, reconcile crashes, reject changed payload under same key | D8 “Reliable provisioning and retry” | 07 §§3.1–3.3; 09 §§4,6,8; services.schema.json | U for result; exact service protocol and early winner are A (C02/A01 below) |
| T05 | Bounded retries, recovery-needed pending state, no ownership compensation | D8 “Reliable provisioning and retry” and “Scope and alternatives” | 09 §6.2; 10 §1; 13 test matrix | U for behavior; 8 attempts/backoff/timeouts are D defaults |
| T06 | Separate one-time setup challenge, verified channel, own idempotency, loser no-op after Ready | D8 “Secure completion path” | 01 §9; 04 §4.1; 08 §3; 09 §7 | U for challenge; SetupChallenge name, record fields, setup routes and budgets are D; winner before Ready is A |
| T07 | Exactly-once logical Ready/event enqueue and two timestamps | D8 “Completion and event timing”; PR #1 adds explicit timestamp contract | 06 §§4.1–4.2; 09 §6.4; events.schema.json | U for atomic fact/identity; CAS and unique Outbox key are D mechanisms, subject to concurrency verification |
| T08 | One verified contact before commit; mobile-only permitted | D9 “Required registration input” and “Verification before the ownership commit” | 01 §§2–3; 04 §4.1; openapi Person/StartRegistration | U; exactly one in MVP narrows the ADR's optional both-contact extension (D choice), not a universal prohibition |
| T09 | Verification session identity, absolute expiry, limits, bounded deletion | D9 verification/material paragraphs added by PR #1 | 01 §9; 09 §7; 10 §1; machine.configuration | U for properties; VerificationSession record, 600 seconds and deletion deadline are D, not ADR values |
| T10 | Atomic material owner transfer; cleanup must respect new owner | D9 material binding paragraph | 07 §4; 09 §5.1.3 and §8 | U for durability/security; secret-store protocol is D and still needs transactional/race proof |
| T11 | Non-enumerating initial/resend behavior, including delivery/timing/throttling | D9 enumeration paragraph | 08 §§3,5; 11 §3; 13 matrix | U; exact status bodies and numerical budgets are D |
| T12 | Same successful proof + binding; keyed online verifier; replay within original validity | D9 replay paragraphs | 08 §3; 09 §7; 11 §2; machine.security | U; 256-bit client bindingSecret and initiation Idempotency-Key are D choices, not named in ADR |
| T13 | Expired replay: no duplicate ownership, discard second password, distinct authorized setup | D9 expired-response/conflict paragraphs | 04 §4.1; 08 §3; 09 §7; 13 matrix | U; conflict mapping and setup-request response design are D |
| T14 | Optional initial Session | D8 “Completion and event timing” says MAY follow | 00 §2; 04 §4.1; 08 §3 | No initial Session + separate login is permitted D choice, not an ADR requirement |
| T15 | Contact changes require separate governed rules | D9 “Required registration input” | 01 §2; 04 §4.3; openapi UpdateProfile | U boundary; DisplayName-only MVP and strict unknown-field rejection are D contract changes needing consumer review |
| T16 | Shared PersonRegistered/PersonUpdated stream | Not specified by D8/9 beyond atomic Ready/event | 03 §9.1; 06 §6.1; 09 §6.4; machine.events.stream | A introduced through PRs #2/#3; not justified solely by AggregateType=Person; LoginFailed exclusion remains explicit |
| T17 | Polling and named EnsureInitialCredential/GetInitialCredentialResult operations | D8 requires reconciliation and active-Credential confirmation but selects no transport | 07 §3; 09 §6.1; machine.workflow.credentialConfirmation; services.schema.json | A01 open; schema presence does not approve polling |
| T18 | Registration-lifetime deduplication tombstone | D8 requires stable deduplication, no concrete lifetime selected | 07 §3.2; 09 §7 | A02 open retention/late-delivery choice; define lifetime, deletion and reuse behavior before acceptance |
| T19 | No independent revoke/replace before Ready | No explicit blanket rule in D8/9 | 07 §3.2; 09 §6.1 | A03 open; stronger than one-active uniqueness or loser no-op |
| T20 | KDF/password/session defaults, refresh retention, session cap | Not selected by D8/9 | 04 §§4.5–4.6; 10; 11 | Separate proposed policies, not derived ADR requirements; outside a claim of completed D8/9 traceability approval |

## 5. Three Credential rules — do not conflate them

| Rule | Meaning and provenance | Required enforcement question |
|---|---|---|
| C01: at most one active Credential per Person | Explicit D8 safety property under concurrent/duplicate delivery and secure setup | Must hold under multi-worker concurrency and crash recovery. A DB constraint or equivalent durable serialized authority can enforce it; application check-then-write/retry alone is insufficient. ADR does not mandate a particular SQL index |
| C02: one immutable initial winner per registration | PR #5 fixes the winner at Credential commit, earlier than ADR's “wins and marks it Ready” condition | A unique durable registration slot plus atomic winner binding/CAS is the proposed mechanism. Uniqueness alone does not forbid updating the winner. Which operation establishes the winner, can it ever be superseded before Ready, and what does the loser return? Open architectural choice |
| C03: no independent replacement/revocation before Ready | Broader exclusion in 07 §3.2; used to justify trusting a remote confirmation outside Identity's transaction | Covers all mutation paths, not just retry losers. Requires a service-enforced guard/fence or an explicitly justified equivalent; one-active DB uniqueness cannot prevent sequential replacement. How does a separate Credential service learn the phase safely and survive acknowledgment loss? Not currently specified |

The answer is not simply “database versus application.” The invariant belongs to an authoritative service/domain boundary; its concurrency guarantee must be durable across processes. A process-local lock or retry convention is not equivalent. The choice of constraint, transactional CAS, fencing or another mechanism remains unapproved here.

A concrete unresolved interleaving: Credential service returns Active(C1); another actor revokes/replaces C1; Identity commits Ready using stale evidence. The sentence in 09 §6.1 claiming the no-replacement rule closes this race is conditional on C03 actually being enforced. Declaring administrative commands outside MVP is not proof that every mutation path in a separately deployed service is excluded. Conversely, no implementation evidence was inspected that such an unsafe path currently exists.

Review must select a justified alternative: enforce a durable pre-Ready provisioning phase/fence (including a reliable release protocol), use a safely validated confirmation protocol, or constrain/co-locate the transaction boundary with explicit governance. Merely naming confirmationVersion is not fencing unless someone checks it at the authoritative write. This report selects none of these alternatives.

## 6. Required architectural dispositions before acceptance

- A01: Select polling, callback, messaging or co-located confirmation; document deployment assumptions, outages, retry budget and evidence freshness. The current two operation names are a proposal, not an upstream mandate.
- A02: Define deduplication tombstone lifetime and late requests after deletion; do not conflate it with secret/proof disposal.
- A03/C02/C03: Define winner linearization point, allowed pre-Ready mutation, cross-service phase knowledge and lost-ack recovery. Specify concurrency tests for each rule separately.
- T16: Record authority for the two-event stream scope and ordering/consumer obligations; preserved text from an earlier Draft PR is not accepted architecture.
- D defaults: Review numerical bounds and contract choices in 08/10 separately. In particular “absolute 10-minute maximum in proposed defaults” (09 §7) must not be interpreted as an ADR-imposed hard ceiling or silently diverge from configurable policy.

Until dispositions exist, the normative-looking SHALL/enforcement wording in Draft 07/09 and machine contracts is candidate design, not approved derivation. Record the accepted decision through project governance before normative remediation; do not close a traceability issue just because YAML and prose agree.

## 7. Validation-file provenance

After fetching complete ancestry (`git fetch --unshallow origin`, shallow status false), `git log --all -- *12_Validation*` finds only the addition at `4f13eff`; the same query restricted to baseline `9fa0266` finds no entry. The available workspace search found only the current file; the repository files.zip contains two ADR attachments and no validation document. This establishes absence in the inspected reachable Git history and local candidates, not absence in other repositories, deleted/unreachable history or unsearched Library attachments. The alleged v1.0.1 remains unlocated. The current 12_Validation v1.0.0 distinguishes Domain/Policy/Infrastructure in §1, but that is not proof that a previously mentioned v1.0.1 was recovered or preserved byte-for-byte. No invented version bump or reconstruction of the missing version is justified.

## 8. Outcome

PR #1 has now been directly reviewed at a pinned head. D8/9 obligations and Blueprint additions are mapped; A01–A03/C02–C03 and T16 remain open architecture items. This report adds review evidence only, changes no protocol, approves no invariant and closes no PR. Main and all ADR acceptance statuses remain unchanged.
