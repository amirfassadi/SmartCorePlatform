# ADR-0004: Identity Credential Provisioning Protocol

## Metadata

- Status: Proposed
- Version: 1.0.1
- Date Created: 2026-09-24
- Last Reviewed: 2026-09-25
- Decision Level: Level 4 — Architectural Change
- Approval Date: TBD
- Effective Date: TBD
- Related decisions: ADR-0002 Decisions 8–9 (Proposed); governance 051 §§5–7

## Context

The PR #5 Blueprint at 4f13eff proposes polling, an immutable initial Credential winner and a prohibition on independent pre-Ready replacement. ADR-0002 requires reconciliation, one active Credential and a loser no-op after Ready, but does not itself select these mechanisms or the earlier winner point. The traceability review at 9514461 records A01/A02/A03 and C01/C02/C03 as unresolved. This ADR supplies an explicit proposed disposition, not retroactive approval of the Blueprint.

The unsafe interleaving to exclude is: Credential service confirms active C1; another operation revokes/replaces C1; Identity commits Ready based on stale evidence. One-active uniqueness alone permits that interleaving. A confirmation version that is never checked at the authoritative mutation cannot prevent it.

## Scope

Initial human registration and its secure completion only. Credential may be separately deployed, but its supported mutation paths must share one authoritative durable store/serialization boundary. No sixth Aggregate, public event or distributed two-phase commit is introduced. The supporting provisioning record belongs to the Credential service's application persistence boundary.

Administrative revocation, lost-contact recovery and general password reset remain outside MVP. A service whose existing mutation paths cannot honor the guard below is incompatible with this protocol; it must not be connected on the assumption that an absent public MVP endpoint makes the race impossible.

## Decision 1 — A01: authenticated polling with durable results

Choose authenticated polling for active-Credential reconciliation. Keep the proposed internal operations EnsureInitialCredential and GetInitialCredentialResult. Use registrationId for registration identity and a separate operationId for each authorized candidate; repeated identical operations return the durable outcome. Same operationId with a changed bound request is rejected and audited.

Provisioning delivery remains at least once. Identity reconciles uncertain writes before deciding to submit another attempt. No network call runs inside Identity's local Ready transaction. Call timeouts, poll/backoff budgets and escalation thresholds remain reviewed policy in 10_Configuration, not architectural constants.

Polling is the selected proposal because it recovers a lost response without depending on receipt of a callback. It does not by itself guarantee that evidence remains valid; Decision 3 supplies that guarantee. Exhausted automatic budgets leave recovery-needed state and operational visibility; authorized re-drive uses the same identities and never creates another registration.

## Decision 2 — A02: registration-lifetime deduplication

Retain a durable initial-provisioning winner record for the lifetime of the registration. MVP has no ownership/registration deletion operation, so there is no time-based deletion of this record in MVP. Define any future erasure/archival protocol before allowing removal or reuse of registration identity; a generic audit-retention expiry must not delete this operational correctness record.

Minimum retained data: registrationId/PersonId association, winning operationId and CredentialId, immutable candidate binding fingerprint, provisioning phase/version and the acknowledged Ready fact identity when present. Do not retain a password, OTP verifier, request binding secret, recoverable material or password-derived fingerprint in this tombstone. A candidate binding fingerprint refers to high-entropy internal candidate/material identity plus non-secret immutable request metadata, not the password. Detailed schema/key-management choices remain contract work.

Per-operation retries must not grow storage without bounds: once a winner exists, every distinct later candidate receives an already-provisioned rejection/result before any mutation, with a reference to the existing outcome. Only the successful winner's accepted mutation key and binding need registration-lifetime retention; a loser is never admitted as a new successful mutation. Temporary request/proof replay records retain only their independently bounded lifetimes. This avoids promising perpetual changed-payload detection for discarded loser records; all such late mutation attempts are rejected regardless of payload. Consumed setup replay remains authorized only within its proof lifetime; registration-lifetime internal deduplication grants no public lookup or password-setting authority. Secret/proof deletion deadlines are independent and unchanged.

After Ready, a provisioning retry never recreates a revoked Credential or restores an older password. GetInitialCredentialResult must distinguish a historical winner from a currently active Credential: only a currently active winner in the pre-Ready guarded phase is valid evidence for a PendingCredential→Ready transition. Post-Ready status may report AlreadyCompleted with historical identifiers, without claiming current Active state. If Identity is locally PendingCredential but observes ReadyAcknowledged/AlreadyCompleted, stop and reconcile an integrity/disaster-recovery inconsistency; do not infer a fresh Ready transition from a historical winner. The existing two-response schemas require alignment before acceptance.

## Decision 3 — A03: durable pre-Ready mutation guard and explicit release

### 3.1 Distinguish the three invariants

| Rule | Proposed guarantee | Enforcement boundary |
|---|---|---|
| C01 | At most one active Credential per Person | Storage uniqueness or equivalent durable serialized enforcement in the authoritative Credential service |
| C02 | Exactly one successful initial candidate becomes the immutable winner per registration | Atomically commit Credential plus winner binding; winner is fixed at this commit, explicitly earlier than Ready |
| C03 | That winner cannot be replaced or revoked by another supported operation before Identity commits Ready | Every Credential mutation checks the same durable provisioning guard in its local transaction; release requires the Ready acknowledgment below |

These are domain/service obligations implemented through durable concurrency control. A process-local lock, application pre-check or retry convention alone is insufficient. An immutable winner binding and a lifecycle guard require more than merely a unique index on active PersonId. Specific SQL/index/lock syntax is not chosen here.

C02 deliberately narrows the freedom left before Ready in ADR-0002. An automatic candidate that commits first can defeat a later manual candidate even if Identity has not yet reached Ready. The loser returns the existing outcome and never silently replaces the password. API wording must not promise that the last submitted password won.

### 3.2 Credential-side phases

The supporting record has an immutable registration/Person binding and two relevant phases:

- ProvisionedAwaitingReady: created atomically with the winning active Credential and operation outcome. All replacement/revocation paths are blocked while this phase holds. Duplicate provisioning is read-only; a different candidate cannot replace the winner.
- ReadyAcknowledged: entered only by the authenticated acknowledgment of a committed Identity Ready fact. Normal separately authorized Credential changes can then execute under their own rules. Repeated initial provisioning remains a no-op forever for this registration.

Before a winner exists, competing initial candidates serialize through the same authoritative registration slot and Person one-active constraint. Never accept an unrelated existing active Credential as evidence for this registration; mismatched registration/Person/Credential bindings fail closed.

The phase is internal application state, not a new Credential or Person Aggregate lifecycle status. It does not require a cross-service transaction or a Person Aggregate write.

### 3.3 Ready commit and release protocol

1. Identity obtains authenticated evidence containing registrationId, PersonId, winning CredentialId and the guarded provisioning version. The service returns usable pre-Ready evidence only for an active winner in ProvisionedAwaitingReady.
2. In one local Identity transaction, CAS PendingCredential→Ready, record immutable readyFactId and the matching winner evidence, enqueue PersonRegistered, and enqueue an internal Ready-acknowledgment Outbox item. No acknowledgment may be emitted before commit.
3. The Outbox calls the new internal operation AcknowledgeRegistrationReady(registrationId, PersonId, CredentialId, provisioningVersion, readyFactId). Credential authenticates the Identity writer, validates all bindings against its durable winner and atomically transitions its phase to ReadyAcknowledged while persisting that fact identity.
The provisioningVersion in this protocol is an immutable token identifying the guarded winner generation, not a general row version incremented by polling, attempt counters or acknowledgments. The winning generation cannot change for the registration.

4. Repeating the same acknowledgment succeeds idempotently. A different fact or mismatched winner/version is rejected and alerted. A delayed acknowledgment after later authorized password change must return its recorded acknowledgment result, never restore the original Credential. Check the durable acknowledged fact/bindings before comparing current Credential state; legitimate subsequent replacement must not make a matching duplicate acknowledgment fail. A different fact or binding still fails.

The acknowledgment is not a public Domain Event and must never be accepted from a user or inferred from seeing a registrationId. The authenticated Identity writer is trusted to send only committed facts from its durable Outbox. This trust assumption, service authorization and transactional Outbox guarantee require implementation verification; a client-supplied claim of Ready is insufficient.

The guard has no TTL-based release. Timeouts do not prove Ready. Guarded evidence remains valid until the corresponding Ready fact can release it, subject to the authoritative service's durability and mutation-coverage assumptions. Stale/out-of-order observations cannot transition Identity twice because Ready is a local monotonic CAS. Cross-service disaster recovery must preserve/reconcile the durable facts; restoring mutually inconsistent snapshots and continuing blindly is unsupported.

### 3.4 Crash and availability behavior

| Failure/interleaving | Required behavior |
|---|---|
| Credential commit succeeds; response lost | Poll returns the same guarded winner; no second Credential |
| Identity Ready transaction rolls back | No Ready/event/acknowledgment is committed; Credential remains guarded; reconciliation retries |
| Identity commits Ready; crashes before sending acknowledgment | Durable Outbox retries release; existing active Credential permits login when Identity reports Ready |
| Acknowledgment commits; response lost | Retry returns the same recorded acknowledgment, without another mutation |
| ChangePassword arrives while Identity is Ready but Credential remains guarded | No replacement; return retryable provisioning-finalization/unavailable outcome and reconcile acknowledgment; do not report password change success |
| Acknowledgment retries exhaust their automatic budget | Keep guard, alert and support authenticated idempotent re-drive; do not delete ownership, roll Ready back or bypass guard |
| Concurrent manual/automatic candidates | Credential commit selects one winner; all losers are read-only; Identity emits one Ready event |

This trades availability of immediate post-Ready password changes for safety. Ready still means registration can authenticate with its active Credential; it does not mean every downstream cleanup/acknowledgment has completed. Missing acknowledgment must be observable so a Person is not silently left unable to change a password indefinitely.

No independent emergency revoke bypass is granted by this proposal. Introducing such a path requires its own consistency/security decision, including how to prevent stale Ready evidence. If that capability is required now, this ADR cannot be accepted unchanged.

### 3.5 Stalled provisioning and administrative recovery limitation

Contact verification precedes ownership commit and Credential provisioning under ADR-0002 Decision 9. Abandoning or losing the pre-commit verification challenge therefore does not itself create a Credential in ProvisionedAwaitingReady. This limitation concerns a committed registration whose Credential exists but whose Ready reconciliation stalls, or a committed Ready fact whose acknowledgment cannot be delivered.

The guard can remain indefinitely while the cause is unresolved. User inactivity or elapsed time is not a reason to release it. PendingCredential still denies login; Ready with a pending acknowledgment can permit login while blocking Credential replacement. Operational re-drive may resume the existing authorized workflow or resend its committed Ready acknowledgment; it cannot synthesize Ready evidence, replace the winner, revoke it or bypass the guard.

Before acceptance, architecture/security and the accountable operations/support owner must explicitly accept this MVP limitation or require a separate governed recovery/cancellation decision. Acceptance must identify the monitoring/escalation owner, the auditable authorized re-drive procedure, and the support response when re-drive cannot resolve the registration. There is no implied self-service or administrative unlock. No new numeric deadline, TTL release or emergency-revoke behavior is introduced by documenting the gap.

## Rationale

C01 protects a cardinality invariant; C02 makes uncertain duplicate provisioning recoverable; C03 protects the validity interval between remote confirmation and local Ready. The explicit post-commit acknowledgment makes the release condition verifiable at the authoritative Credential writer without introducing distributed 2PC. It exposes the availability cost instead of hiding it in a blanket no-replacement sentence.

## Alternatives considered

- Polling alone: recovers lost responses but does not close the stale-confirmation race.
- Callback/event-only confirmation: possible alternative, but also requires durable deduplication and a validity/mutation protocol; selected polling is simpler for explicit retry reconciliation in this proposal.
- One-active uniqueness alone: prevents two simultaneous active records, not sequential replacement between confirmation and Ready.
- Local application lock/retry: insufficient across workers and crashes.
- Guard released by timer: rejected; elapsed time is not evidence of committed Ready.
- Co-located Credential/Identity persistence with a shared transaction/guard: viable architectural alternative with a different deployment constraint. Not selected because this proposal preserves the separate-service case; reconsider if release-protocol cost is not justified for MVP.
- Distributed 2PC: not required; both services make local durable commits and reconcile forward.

## Consequences and propagation gates

These dispositions are Proposed, not accepted. They do not retroactively validate 07/09 or authorize implementation under 051 §7. Before acceptance, update and review together:

- ADR-0002: explicitly reference the earlier C02 winner point and this protocol without rewriting its existing history as if it selected polling.
- Identity 01/03/04/07/09: authoritative guard ownership, all mutation paths, early winner, acknowledgment and post-Ready retryable password-change behavior.
- Identity 08 and OpenAPI: distinguish completion from winning password, and expose the retryable finalization failure without leaking secrets.
- machine YAML and services schema: typed guarded confirmation, phase/version, AlreadyCompleted and AcknowledgeRegistrationReady messages; Ready transaction includes acknowledgment Outbox. Do not silently treat the old schemas as sufficient.
- Identity 10/11/13: acknowledgment retries/escalation, service trust, no timer release, tombstone minimization, and crash/race/late-request tests.
- Identity 12: require this ADR's acceptance and full contract/065/security validation, not just a presence check.

## Related open issue: T16

This ADR does not approve the PersonRegistered/PersonUpdated shared stream. T16 remains a separate architecture-review item; the fact that prior Draft PRs describe it is not an authority for acceptance. It need not prevent choosing one Draft review branch, but it prevents representing all architecture questions as closed.

## PR path and governance

Choosing PR #5 as the sole review vehicle and closing #1–#4 as superseded is a repository-workflow decision, distinct from accepting ADRs or enabling generation. Do not represent publication of this proposal as the user's approval of its architecture or authorization to merge. PR closure remains a separate explicit action after review-path confirmation; this change closes none.

## Acceptance criteria

- [ ] Architecture review accepts/revises A01/A02/A03, including early winner and release-protocol availability cost.
- [ ] Architecture/security and the accountable operations/support owner explicitly record acceptance of the potentially indefinite stalled-registration guard and absence of an administrative unlock in MVP, with monitoring/escalation ownership, an audited authorized re-drive procedure and a support response for unresolved cases (§3.5); otherwise a separate recovery/cancellation decision must be approved and propagated before accepting this protocol. This limitation is not accepted merely by adding this checklist item.
- [ ] Every supported Credential mutation path is demonstrably guarded; deployment assumptions are enforceable.
- [ ] ADR/Blueprint/API/machine propagation above is completed and reviewed.
- [ ] Cross-service binding, replay, crash, rollback, stale evidence, acknowledgment loss and late-duplicate tests pass.
- [ ] Tombstone erasure/retention and service trust policies approved for MVP; no secret/proof retention is extended.
- [ ] Full applicable 065 validation and ADR-0002 acceptance requirements completed.

## Change history

| Version | Status | Change |
|---|---|---|
| 1.0.1 | Proposed | 2026-09-25: Recorded stalled-registration administrative recovery as an explicit acceptance choice; distinguished pre-commit contact abandonment from post-provisioning reconciliation failure. No unlock, TTL or protocol change. |
| 1.0.0 | Proposed | Explicit A01/A02/A03 disposition with durable mutation guard, early winner, registration-lifetime deduplication and post-Ready acknowledgment. No Blueprint behavior or acceptance status changed by this document. |
