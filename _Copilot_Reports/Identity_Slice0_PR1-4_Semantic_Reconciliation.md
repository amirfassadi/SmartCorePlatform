> Revision note: original findings below describe the uploaded candidate; the publication review supersedes dispositions it explicitly corrects.

# Slice 0 evidence — semantic reconciliation of superseded PRs #1–#4

Prepared: 2026-10-04. Status: DRAFT review evidence; not an architectural acceptance, not implementation permission. The uploaded review was local-only. Its publication review and corrections are recorded in Identity_Slice0_Publication_Review.md.

## 1. Inputs and scope

| Item | Value |
|---|---|
| Platform `main` | `9fa0266b381b8f185af54a51747fefff6599fa92` |
| PR #1 / #2 / #3 / #4 heads | `725ed58` (v1.6 contract), `c90af51` (Ready-time events), `37df22b` (persistence draft), `0dc9071` (readiness status) |
| Candidate compared against | local merge of PR #5 `91375b1` + #9 `db88bb0` + #7 `7ccba70` + #8 `6c50cb9` + #6 `1e57082` (local merge commit `82a400d`; clean Git merge only) |
| Status of #1–#4 | Verified through GitHub API on 2026-10-04 (Asia/Tehran): #1–#4 are closed with merged_at=null. Repository evidence: ADR-0004 states closing #1–#4 as superseded is a repository-workflow decision. All four branches fork from current `main` and are not merged into it. |

Method: (1) a raw added-line comparison, used only to find candidates; (2) for each requirement, a manual search of the candidate for the equivalent text. **Dispositions:** Preserved = same rule present; Replaced = rule changed on purpose, with reason; Partial = substance present but an explicit clause absent; Gap = not located. A Git-clean merge says nothing about semantic conflicts. Locations are file section and, where verified, line numbers in the candidate tree.

## 2. PR #1 (ADR-0002 v1.6 and 026 event timing) — 18 requirements checked

All 18 requirements were located in ADR-0002 v1.8.0 (Decisions 8–9 and Event Ownership sections) or in 026 §8 and **preserved**: OccurredAt = Ready transition (ADR-0002:429; 026:641); OwnershipCommittedAt for age/retention (ADR-0002:432–433; 026:194); distinct commit-time signal (ADR-0002:436–437); opaque verificationSessionId with absolute expiry (ADR-0002:510); no raw password persisted (ADR-0002:506); immediate invalidation and bounded deletion (ADR-0002:507–508); resend cannot extend expiry (ADR-0002:510); atomic material-reference binding and rollback leaving nothing (ADR-0002:516–519); anti-enumeration (ADR-0002:495, 524); conflict disclosed only to verified holder (ADR-0002:525); consumption/replay mapping bounded by challenge window, session id alone insufficient, replay returns only the committed outcome (ADR-0002:545–549); keyed HMAC verifier, online verification only (ADR-0002:552–553); different payload rejected and audited (ADR-0002:558); expired replay routed to secure completion without resetting the session (ADR-0002:565–572); version-pinned reference rule (ADR-0002:711–713). **Verification level:** the passages at ADR-0002:516–519, 536–560, 565–572, 709–713 and 026:190–198 were read in full and confirmed. The remaining locations (ADR-0002:429–437, 495, 506–510, 524–525; 026:641) are keyword hits that were not individually re-read, so they are located but not yet confirmed word-for-word.

## 3. PR #2 (06_Domain_Events Ready-time contract) — 10 requirements

Verification level: the rows below are keyword-located in 06_Domain_Events and not re-read line by line, except 06:310. Treat "Preserved" here as *located*, pending a read-through.

| Requirement | Disposition | Candidate location |
|---|---|---|
| ActorIdentity System for automated/recovery processing | Preserved | 06_Domain_Events:69, 241, 271 |
| CorrelationId rules (required person-initiated, optional System) | Preserved | 06:67, 271–279 |
| Person-initiated completion uses the request that caused Ready | Preserved | 06:310 |
| No PublishedAt; OccurredAt is the fact time | Preserved | 06:255, 262 |
| Same-aggregate events observable in committed order | Replaced/expanded by the per-Person stream rule | 06:622–644; 09_Persistence §6.4 |
| Email only for email contact; omitted differs from null | Preserved | 06:247, 331, 343 |
| Post-commit failure does not invalidate ownership | Preserved | 06:599 |
| Other email-dependent events reviewed for mobile-only Persons | Preserved as open item | 06:331–343, 531 |
| Draft status until propagation | Preserved | 06 header/status |
| Machine contract distinguishes omitted Email from null | Open item (not verified in this slice) | capability.machine.yaml |

## 4. PR #3 (persistence and aggregates) — 16 + 2 requirements

Verification level: 09_Persistence v1.3.0 was read in full; 03_Aggregates:236–246 was read; other 03 and 10_Configuration locations are keyword-located.

| ID | Requirement | Disposition | Candidate location |
|---|---|---|---|
| P1 | One Unit of Work: ownership triple + workflow + Outbox; full rollback | Preserved | 09 §5.1, §5.1.1, §5.1.2 |
| P2 | Supporting records are not Aggregates; exception not general precedent | Preserved | 09 §2, §5.1.3, §5.3 |
| P3 | Protected material bound to registrationId before Outbox is visible; rollback leaves none | Preserved | 09 §5.1.2–§5.1.3; ADR-0002:516–519 |
| P4 | Workflow: registrationId, unique PersonId, status, OwnershipCommittedAt, concurrency marker | Preserved | 09 §7 RegistrationWorkflow row |
| P4b | Workflow stores the verified contact reference needed for controlled recovery | **Gap (not located)** | not in 09 §7 or 03 §9.1; recovery is described via SetupChallenge |
| P5 | Outbox keyed by registrationId, no plaintext password | Preserved | 09 §4, §5.1.3, §7 |
| P6 | Recovery-needed and retry metadata durable across restart | Preserved | 09 §6.2, §7, §11 |
| P7 | Post-commit failure never reopens the §5.1 Unit of Work | **Partial**: substance present, explicit prohibition absent | 06:599; 059:691; structure of 09 §6 |
| P8 | Cross-service Credential: no distributed transaction | Preserved | 09 §6.1, §11 |
| P9 | Bounded backoff; exhaustion keeps PendingCredential + recovery-needed | Preserved | 09 §6.2; 10_Configuration:31–32 |
| P10 | Login needs Ready + active Credential | Preserved | 09 §6.3 |
| P11 | Ready CAS, one PersonRegistered, unique (registrationId, EventType), loser returns committed result | Preserved and extended (ReadyFactId) | 09 §6.4 |
| P12 | Shared allocator for PersonRegistered/PersonUpdated; LoginFailed excluded | Preserved | 09 §6.4; 03 §9.1 |
| P13 | Rollback leaves Pending and no event/position; crash reconciliation | Preserved | 09 §6.4, §11 |
| P14 | Outbox delivery keeps position and identity; no cross-stream order | Preserved | 09 §6.4 |
| P15 | IdentityEvents table would be an Event Store; Event Sourcing/transport/retention out of scope | **Gap (not located)** | only Event Bus exclusions at 06:86, 119 |
| P16 | Draft until propagation complete | Preserved | 09 header, §10 |
| A1 | "A profile update may precede Ready; consumers must not assume PersonRegistered is first" | **Replaced with reason**: commit `91375b1` corrects causal order (UpdatePersonProfile needs a Session, which needs Ready) | 03_Aggregates:236–246 |
| A2 | §9.1 proposed pending ADR acceptance and T16 | Preserved | 03 §9.1 |

## 5. PR #4 (readiness status) — preserved

Both purposes carried: documents marked Draft, legacy email-required contracts not usable for generation. Candidate headers: 01_Domain_Model 1.4.0 DRAFT, 07_Contracts 1.2.0 DRAFT; no Identity document claims READY_FOR_GENERATION (14_MVP:31 states the opposite).

## 6. Findings needing a human decision

1. **P4b Gap** — decide whether the workflow must store a verified-contact reference or whether SetupChallenge makes it unnecessary.
2. **P15 Gap** — decide whether to restore the explicit Event Store / Event Sourcing / transport non-goal in 09_Persistence or 06_Domain_Events.
3. **P7 Partial** — decide whether to add the explicit prohibition.
4. **Wider than #1–#4:** candidate 09_Persistence is 134 lines, versus 1447 on `main`. #1–#4 cannot explain that reduction; legacy v1.0 requirements outside #1–#4 need their own comparison before 09 is accepted.

No candidate text was edited to close these items.
