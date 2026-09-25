<!--
Document ID: ID-09
Title: SmartCore Identity Platform Blueprint - Persistence
Version: 1.3.0
Status: DRAFT
Purpose: Define the proposed Identity persistence contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.3.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.2.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.1.0; prior text remains in Git history.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Scope

Logical persistence and transaction requirements, independent of SQL dialect or broker. DDL, deployable migrations and runtime verification remain implementation deliverables. Narrative model 01 is authoritative.

# 2. Repository boundary

Exactly one Repository owns each Aggregate. Supporting stores belong to the application layer; none is a sixth Aggregate or a license to bypass domain rules.

# 3. Repository catalog

| Repository | Writes | Reads |
|---|---|---|
| PersonRepository | Create, Update | GetById, GetByVerifiedContact(type, canonicalValue) |
| OrganizationRepository | Create | GetById |
| MembershipRepository | Create | GetByPersonId, GetByOrganizationId |
| CredentialRepository | Create, Replace | GetActiveByPersonId (zero or one) |
| SessionRepository | Create, Refresh, Close, Expire | GetById, GetByAccessToken, GetByRefreshToken, GetActiveSessionsByPersonId (list) |

Lookups follow 05. Contact uniqueness checks and insertion use the same canonicalization/version. Repository writes participate in the caller's Unit of Work; they do not independently commit the ownership triple.

# 4. Schema and constraints

Persist all attributes in 01. Exactly one non-null Email/Mobile is required internally; public omission does not dictate physical SQL nullability. Unique normalized email where present and unique E.164 mobile where present cover PendingCredential as well as Ready Persons. PersonId and all root IDs are unique; membership foreign keys preserve the ownership triple. Enforce C01 one-active cardinality and C02 immutable initial winner in the authoritative Credential transaction, plus C03 a durable mutation guard checked by every supported writer. The winner is fixed at Credential commit. A uniqueness check alone cannot prevent sequential replacement; the guard releases only on acknowledgment of committed Ready. Retired credential rows are not a public PasswordHistory feature.

Sensitive values are encrypted at rest/access controlled; store tokens as protected verifiers and password as salted KDF output, never plaintext. Application versions use optimistic concurrency for updates. Soft deletion/cancellation of pending ownership is outside MVP; never cascade-delete ownership on provisioning failure.

# 5. Core ownership transaction

## 5.1 Proposed RegisterPerson exception

After valid contact proof, one local Unit of Work atomically writes Person, Personal Organization, Owner Membership, RegistrationWorkflow(PendingCredential), consumed verification mapping, protected-material ownership reference and Outbox entries for provisioning, OrganizationCreated and MembershipCreated.

### 5.1.1 Transaction ownership

The application Unit of Work owns commit/rollback across the three repositories and supporting stores. Durable references must survive that commit; a nontransactional cache is insufficient.

### 5.1.2 Race and rollback

Lock/version-check verification consumption and enforce contact uniqueness at insertion. Two attempts for the same contact cannot create duplicate ownership. A loser rolls back all its writes, retains no committed material reference, and follows verified-conflict handling. A retry of a consumed session resolves the committed mapping after authorization.

### 5.1.3 Supporting registration records

This multi-Aggregate pattern is authorized only for RegisterPerson subject to ADR acceptance; it is not precedent for other Commands. This does not prohibit a normal single-Aggregate Command from writing its own event Outbox atomically.

Binding material ownership to registrationId and inserting provisioning work happen in the same commit. Physical encryption/storage need not move the secret. Cleanup checks durable owner/generation, so a stale verification cleanup job cannot delete transferred material. Pre-commit orphans expire under verification rules. Pending work carries only scoped opaque handles.

## 5.2 Other Commands

Person update and its event commit together in Person's transaction. Credential replacement and PasswordChanged commit together. Session creation and LoginSucceeded/SessionCreated commit together. Session terminal CAS and terminal event commit together. No other Command uses the registration ownership exception.

## 5.3 Governance

No exception is self-authorizing. ADR-0002 remains Proposed. Any new cross-Aggregate transaction needs its own governed justification.

# 6. Credential and Ready transactions

## 6.1 Separate service reconciliation

Accepted ADR-0004 is encoded in 07 §3: idempotent EnsureInitialCredential, authenticated polling of guarded active evidence, then AcknowledgeRegistrationReady. Initial Credential, immutable winner and ProvisionedAwaitingReady phase commit atomically at Credential. Every supported mutation checks that guard in its local transaction. Confirm outside Identity's transaction; immutable provisioningVersion identifies the protected winner generation. The authoritative guard, not polling alone, protects the confirmation-to-Ready interval. Later authentication still checks the current Credential.

## 6.2 Retry and material lifetime

Bounded attempts/backoff in 10. Reconcile uncertain results before retrying or declaring exhaustion. Exhaustion sets recoveryNeeded while preserving PendingCredential and ownership. Post-commit material has an independent absolute lifetime starting at ownership commit; it is not an extension of pre-commit proof. On winner, expiry or terminal unusable material, revoke access immediately and delete within the cleanup bound. If no material remains and no Credential exists, only separately authorized setup can supply a fresh candidate.

## 6.3 Query visibility

Committed Person/Organization/Membership may be visible while PendingCredential. Minimal service lookup and ownership events do not imply login eligibility. Authentication/refresh read readiness and current Credential fail-closed; self Queries require an actual valid Session.

## 6.4 Ready transition and Person event position

Only PersonRegistered and PersonUpdated share the durable per-Person registration/profile stream. AggregateType=Person alone does not join it. LoginFailed and audit-only/authentication outcomes never contend on this allocator.

In one Identity transaction: CAS PendingCredential→Ready, set ReadyAt, persist immutable ReadyFactId plus winner CredentialId/ProvisioningVersion, insert unique `(registrationId, EventType=PersonRegistered)` Outbox entry with stable EventId and original OwnershipCommittedAt, and insert Ready-acknowledgment Outbox work referencing the same fact. The shared per-Person counter remains the separate proposed T16 insertion, not an accepted requirement of ADR-0004. Rollback commits neither counter nor event. Ready transaction changes no Person Aggregate state. Concurrent losers return the committed result; they never create/replace another Credential. After crash, reconcile the same service result and retry.

PersonUpdated uses the same allocator in its Person update transaction. Publish unique stream positions in order; delivery is at least once, so duplicates can arrive after later messages. Consumers deduplicate stable EventId and apply unique positions monotonically, buffering/reconciling gaps rather than inventing state. A permanently failed lower position blocks/alerts that stream; no silent skip. No cross-stream order is promised. Position is transport metadata, not Person lifecycle version.

# 7. Supporting records and disposal

| Record | Identity / lifetime | Required protection |
|---|---|---|
| VerificationSession | verificationSessionId; absolute 10-minute maximum in proposed defaults | keyed proof/binding verifiers; attempt/resend budgets; single mutation consumption |
| Initiation deduplication | client key + keyed input digest; same session expiry | no raw password or fast unkeyed digest; no authorization from key alone |
| Consumed replay/conflict mapping | verificationSessionId→registrationId or authorized setup target; only until original expiry | same successful proof/binding, online bounded verification; no extend-on-read |
| SetupChallenge | setupChallengeId→pending registration; distinct absolute expiry | keyed verifier/binding and single consumed candidate; request digest for replay |
| RegistrationWorkflow | registrationId unique; PersonId unique; registration lifetime | CAS version, ownership/Ready timestamps, winner reference, retry/recovery state |
| Material record | session-owned then registration-owned, or authorized setup candidate | encryption, purpose/owner-bound access; invalidate first; bounded delete; no plaintext backups |
| Provisioning outcome | registrationId + operationId; lifetime tombstone | winner identity/input binding, no retained secret; prevent delayed retry creating another Credential |
| Event Outbox / stream | stable EventId and per-stream position | atomic enqueue, durable retries, restricted payload access |

Expiry immediately denies access logically, even before the physical sweep runs. Deletion must complete within the configured bound, including replicas/caches; encrypted backup copies use cryptographic key disposal or documented backup expiry with no restorable usable secret beyond the bound. Alert on breach; do not silently label delayed cleanup compliant. Audit retains identifiers/outcomes under policy, not proof verifiers after expiry. Operational counters must not require serializing LoginFailed on the Person stream.

Refresh tokens remain internal Session storage. LoginHistory is optional audit projection, not an authoritative readiness store. Generic IdentityEvents/AuditLogs stores and PasswordHistory business features are not added by this contract.

# 8. Concurrency and security

Use database uniqueness and optimistic versions, not check-then-insert alone. Code attempts atomically increment before verification; parallel requests share one cumulative budget. Resend is synchronized with consumption/expiry. Material cleanup and owner transfer serialize on owner version. Setup and automatic provisioning serialize at Credential's unique initial slot, before either attempts Ready.

# 9. Cross-document alignment

01 defines attributes; 03 §9.1 defines application workflow; 06 §6.1 defines the limited event stream; 07 §3 defines external Credential confirmation; 10–13 define bounds, threats, validation and tests. Proposed details require architecture review before implementation.

# 10. Acceptance checklist

- [x] Proposed workflow ownership, Credential polling contract and two-event stream documented across the package.
- [x] ADR-0004 architecture accepted by owner; no runtime or contract-verification result is implied.
- [ ] ADR-0002, T16 and the remaining governance/service-contract review gates.
- [ ] Database constraints, crash/retry/race/cleanup and delivery tests implemented and passed.
- [ ] Full 065 semantic/contract/dependency/machine and quality-gate validation passed.

# 11. Accepted guard, acknowledgment and recovery persistence

Credential application storage owns InitialProvisioningRecord with immutable registration/Person/winner/generation binding, phase and optional acknowledged readyFactId. Phase changes only ProvisionedAwaitingReady→ReadyAcknowledged under authenticated Ready acknowledgment. Check stored matching acknowledgment before current Credential status, so later ChangePassword cannot invalidate an acknowledgment replay. Never restore a replaced Credential. Timers, worker leases and retry exhaustion cannot release this phase guard.

Identity ReadyFactId/winner evidence/acknowledgment Outbox share the Ready/event local transaction. Lost delivery retries the same fact. Ready with pending acknowledgment may authenticate; ChangePassword checks the guard and returns finalization-pending. A historical AlreadyCompleted result cannot move a locally PendingCredential workflow forward; inconsistent cross-service restore requires investigation.

Recovery jobs and request fingerprints are durable supporting records. Admission atomically validates eligible snapshot and persists authorization/audit intent plus dispatch; invalidation locks the same verification consumption/material owner record as ownership commit. If transfer won, record AlreadyCommitted and do not invalidate transferred material. Post-commit recovery uses canonical Ready/acknowledgment operations and re-reads current phase on each step. Admin is not an extra writer outside C01–C03.

Every effectful local transaction contains audit journal or audit Outbox evidence; the remote Credential transaction does likewise. No cross-service audit transaction is assumed. Recovery result is reconstructed from durable facts after crashes. Retain deduplication through permit expiry AND termination of admitted execution, then the configured result window; unknown expired permits cannot reopen deleted jobs. Append-only audit has separate retention and cannot be purged by the operator. Winner tombstones retain only non-secret identity/fingerprint/phase data for registration lifetime; proof/material deadlines remain unchanged.
