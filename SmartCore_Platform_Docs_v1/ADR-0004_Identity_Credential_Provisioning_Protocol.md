# ADR-0004: Identity Credential Provisioning Protocol

## Metadata

- Status: Accepted
- Version: 1.1.1
- Date Created: 2026-09-24
- Last Reviewed: 2026-09-25
- Decision Level: Level 4 — Architectural Change
- Approval Date: 2026-09-25
- Effective Date: 2026-09-25 (architectural decision only; deployment/generation gates remain open)
- Related decisions: ADR-0002 Decisions 8–9 (Proposed); governance 051 §§5–7

## Approval record and limits

The repository owner **@amirfassadi**, acting as both architecture/security approver and accountable operations/support owner, accepted the architectural content of v1.1.0 at `82ef455eda661064b69bd6f2f080010a341d014e` on 2026-09-25. The [signed acceptance record](../_Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md) was introduced in commit [`16b720c9cb9afdd60769dcad7b2c4d8c1e2e983c`](https://github.com/amirfassadi/SmartCorePlatform/blob/16b720c9cb9afdd60769dcad7b2c4d8c1e2e983c/_Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md). Version 1.1.1 records that approval without changing the technical decisions.

This is owner-directed approval with disclosed combined author/reviewer roles, not an independent review or GPG/SSH signing claim. ADR-0002 remains Proposed; T16 is not accepted. Blueprint propagation, implementation, runtime verification, deployment configuration and full validation are separate pending obligations. All original “before acceptance” implementation/verification conditions below are now explicitly tracked as subsequent implementation/verification/rollout gates under the owner's scoped approval; they are not certified complete or waived.

## Context

The PR #5 Blueprint at 4f13eff proposes polling, an immutable initial Credential winner and a prohibition on independent pre-Ready replacement. ADR-0002 requires reconciliation, one active Credential and a loser no-op after Ready, but does not itself select these mechanisms or the earlier winner point. The traceability review at 9514461 records A01/A02/A03 and C01/C02/C03 as unresolved. This ADR records the accepted architectural disposition; the approval record above does not retroactively approve the existing Blueprint or implementation.

The unsafe interleaving to exclude is: Credential service confirms active C1; another operation revokes/replaces C1; Identity commits Ready based on stale evidence. One-active uniqueness alone permits that interleaving. A confirmation version that is never checked at the authoritative mutation cannot prevent it.

## Scope

Initial human registration, its secure completion, and the restricted internal administrative recovery operation in Decision 4. Credential may be separately deployed, but its supported mutation paths must share one authoritative durable store/serialization boundary. No sixth Aggregate, public event or distributed two-phase commit is introduced. The supporting provisioning record belongs to the Credential service's application persistence boundary.

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
4. Repeating the same acknowledgment succeeds idempotently. A different fact or mismatched winner/version is rejected and alerted. A delayed acknowledgment after later authorized password change must return its recorded acknowledgment result, never restore the original Credential. Check the durable acknowledged fact/bindings before comparing current Credential state; legitimate subsequent replacement must not make a matching duplicate acknowledgment fail. A different fact or binding still fails.

The provisioningVersion in this protocol is an immutable token identifying the guarded winner generation, not a general row version incremented by polling, attempt counters or acknowledgments. The winning generation cannot change for the registration.

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

Before acceptance, the restricted administrative operation in Decision 4 must be designed, propagated and verified as part of this ADR. Accepting indefinite waiting as an MVP limitation alone is no longer an alternative acceptance path. The accountable operations/support owner must identify monitoring, escalation, authorized execution and the response to unresolved infrastructure/integrity incidents. There is no self-service or administrative unlock bypass; no timer releases the guard.


## Decision 4 — restricted administrative recovery before acceptance

### 4.1 Operation and explicit boundary

Introduce the internal operation `AdminRecoverStalledRegistration`, with exactly two actions: `InvalidatePreCommitAttempt` and `ReconcileCommittedRegistration`. It is an application/operations contract, not a new Person-facing business Command, public REST endpoint, Domain Event or Aggregate. Design and propagation are part of this ADR's acceptance gates, not deferred to a future ADR. No implementation or operator access is claimed by this proposal.

This is deliberately recovery, not `AdminCancelStalledRegistration` after ownership commit. Post-commit cancellation/revocation would require a durable Identity cancellation state that races with Ready, rejection of every outstanding confirmation/acknowledgment and ownership/contact-retention semantics. A Credential-side guard alone cannot cancel a Ready transaction already in flight at Identity. No such cancellation is smuggled in as a third caller of the existing guard. Pre-commit invalidation is safe because it serializes with the original ownership commit and affects no committed ownership.

### 4.2 Authentication, scope and request

Only a trusted internal operations surface may invoke the operation. Require a strongly authenticated operator identity with MFA/step-up and an explicit action-specific `Identity.RegistrationRecovery` grant constrained to the operational environment and authorized target scope. A Person Session, general support read access, guessed identifier or possession of a contact is not sufficient. An authenticated worker uses a separate least-privilege service identity; neither operator nor worker receives direct table-write privileges.

Request fields:

| Field | Rule |
|---|---|
| recoveryRequestId | Server-issued opaque idempotency key from the authorized operations view, scoped to operator/environment; immutable request binding |
| admissionPermit | Server-authenticated, expiring permit binding recoveryRequestId, operator/environment, action/target and snapshot; never logged as a reusable token |
| action | One of the two actions above; no arbitrary command/script |
| targetKind / targetId | VerificationSession / verificationSessionId for invalidation; Registration / registrationId for reconciliation |
| expectedState / expectedVersion | Versioned snapshot from the authorized operations read view; checked when accepting the job, never trusted as current state |
| reasonCode / ticketReference | Required incident justification; reason from an allowlist, validated ticket reference; no free-form password/contact/proof dump |
| correlationId | Required audit/work correlation; generated/validated by trusted ingress |

Operator identity, authorization context and request time are derived from authenticated context, not from request fields. Do not accept password material, new contact, winning CredentialId, readyFactId, replacement phase or a `force` flag from the operator. Those facts are read from their authoritative stores.

The operations view issues a signed/MAC-protected admission permit only after authorization. Issuance alone authorizes no mutation. Verify its binding and absolute expiry at job admission as well as the operator's current grant; a fresh arbitrary identifier is not an admissible job. Reauthorize before showing an idempotent result or accepting a job. Bind the operation to the validated target and grant; identical authorized retries return the same job/result, changed input under the same key is conflict and audited. The action requires an atomic current eligibility/version check, so a stale snapshot cannot cancel a newly committed registration. Unauthorized callers get no target-existence detail.

### 4.3 Durable job and permitted state effects

Persist an accepted recovery job, authenticated initiating principal, bounded execution authorization, request fingerprint and audit intent atomically in Identity's operational store before execution. A dispatch Outbox survives loss of the HTTP/CLI response. Acceptance means only `Accepted`, not that recovery succeeded. Reject `StaleTarget` or `NotEligible` without mutation if the initial guarded check fails; an independently audited fresh request is required to choose a different action or target.

The execution authorization is non-transferable, action/target-bound and expires under configured policy. Every new effectful dispatch must revalidate the grant/authorization deadline; revocation or expiry stops further dispatches and is audited. An already admitted transactional step may finish, and committed ordinary reconciliation/acknowledgment work remains governed by its normal service authorization. Operator permission withdrawal cannot roll back an already committed fact. The execution deadline is fixed at admission under policy and does not extend on retry; it may differ from the admission-permit expiry. A deadline/worker lease is never a Credential-guard release signal.

| Authoritative state when executing | Allowed effect and outcome |
|---|---|
| Unconsumed pre-commit VerificationSession, no registration binding | Under the same session consumption/owner-version lock or CAS as registration, invalidate the session, deny future proof use, revoke access to session-owned unused material and enqueue bounded disposal. `Invalidated` is reported only after invalidation commits; physical disposal is separately tracked to `CleanupCompleted` |
| Pre-commit session already expired/invalidated | Idempotent `AlreadyInvalidated`; ensure any required cleanup work is durably present; no proof/session lifetime extension |
| Registration binding won the race, or protected material transferred | `AlreadyCommitted`; no invalidation/deletion of transferred material, no implicit switch to post-commit action. An authorized request must explicitly target the existing registration |
| PendingCredential with active winner in ProvisionedAwaitingReady | Read matching guarded evidence through the normal Credential service, then perform the same Identity Ready CAS/event/acknowledgment-Outbox transaction as §3.3. Never set Ready directly from operator input |
| Identity Ready with acknowledgment still pending | Recover/re-drive the durable acknowledgment of that existing readyFactId; verify winner/version bindings; do not create another Ready event or rewrite timestamps |
| Identity Ready and matching acknowledgment already recorded | `AlreadyReconciled`, no Credential mutation |
| PendingCredential, authoritative result NotProvisioned | This action creates no new candidate and stages no password. Leave any existing ordinary provisioning process intact; return `RequiresNormalProvisioning` or, if its material is unusable/exhausted, `RequiresUserSetup`. Only the existing registration process or separately proven setup can supply a candidate |
| Identity PendingCredential but service ReadyAcknowledged, mismatched bindings, or missing/inactive recorded winner | `IntegrityConflict`; no Ready, deletion, credential rewrite or guard release. Record incident and escalate to controlled integrity repair review |
| Dependency unavailable or state cannot be proven | `RetryableUnavailable`; preserve guard and ownership, retry only within the recovery job's bounded budget |

After job acceptance, ordinary concurrent progress may move the target forward. The worker re-reads current authoritative facts for every attempt and takes only the safe branch above. It never interprets a stale expected version as permission to force the original effect. Pre-commit invalidation uses the verification/session transaction boundary because there is no Credential guard yet. Post-commit reconciliation and acknowledgment go through the existing workflow CAS and Credential-side C01–C03 enforcement, including atomic audit evidence for any local mutation.

Concurrent operators or an automatic worker may race. A lease can reduce duplicate work, but correctness comes from the original durable CAS/unique winner/acknowledgment checks, not a process-local lock. A loser observes the committed outcome and adds audit evidence; it cannot emit another PersonRegistered or replace the winner. Recovery-issued Ready runs as the service worker (`System`); the actual initiating operator is separately preserved in restricted audit with correlation to the Ready fact, not falsely attributed as the Person or as the original registration request.

### 4.4 Mandatory append-only audit

Record request/authorization outcome, reason/ticket reference, authenticated operator and executor, recoveryRequestId, target/action, observed pre/post state and versions, correlation, committed fact identifiers, time, attempt and outcome. Log no OTP, password, bearer token, admission permit, binding secret, usable secret handle or unnecessary contact value. Denials and conflicts are audited as well as successful actions.

Each effectful local transaction must atomically append its audit journal entry or durable audit Outbox entry with the state change. A remote Credential acknowledgment likewise records the correlation, authenticated caller and phase mutation atomically in its authoritative store. A crash after that commit must leave recoverable evidence even if the worker never records its final job response. Final job status is reconciled from recorded facts; no cross-service atomic audit write is claimed.

If the local transaction cannot durably record audit evidence, perform no mutation and return `AuditUnavailable`. An external audit collector outage may be retried from the durable journal/Outbox only within an explicitly configured backlog/time bound; once that bound is exceeded, pause new administrative mutations and alert. Bounds must be configured and reviewed before deployment, not left unlimited.

Audit is append-only: this operation, the invoking operator and ordinary support roles have no edit/delete/purge authority, including after job completion. Corrections append linked records rather than overwriting evidence. Export to retention-protected immutable storage in a separately controlled audit trust boundary, with integrity/tamper detection and access separation. Operators cannot shorten retention or erase their actions. This is an enforceable permission/retention guarantee, not a claim that a compromised storage superuser can never destroy bits or that all audit data must be retained forever.

Operational database access must be restricted to prevent this formal path being bypassed in routine support. Any break-glass infrastructure access requires separate controls, authorization and external audit; it is not an administrative unlock granted by this ADR. Destructive manual changes cannot be represented as normal recovery.

### 4.5 Outcomes, limits and support procedure

An accepted job exposes a restricted read-only result by recoveryRequestId to currently authorized operations staff. Distinguish `Accepted`/`Running` from a confirmed result: `Invalidated` (cleanup may remain pending), `Reconciled`, `AlreadyReconciled`, `AlreadyCommitted`, `RequiresNormalProvisioning`, `RequiresUserSetup`, `IntegrityConflict`, `RetryableUnavailable`, `AuthorizationExpired` or `BudgetExhausted`. No response includes login tokens or secrets. `Reconciled` requires evidence of Identity Ready and matching recorded Credential acknowledgment; an enqueued acknowledgment alone is not recovery completion.

A lost response reuses the same recoveryRequestId; it does not create a new job. Exhausted jobs never reset themselves on retry. A fresh authorized request with a fresh current snapshot and reason can re-drive the same canonical registration/acknowledgment identities, under per-target/operator limits. It cannot reset proof attempts, extend challenge/material expiry, bypass Credential's immutable winner, or resurrect expired provisioning material. Retain the non-secret job/deduplication binding until both its admission permit has expired and all admitted execution/reconciliation has terminated, and for the approved result/replay retention period thereafter. A fresh admission is possible only under an unexpired authenticated permit; retain its deduplication record for that entire window. Once the permit expires, repeating submission is rejected even if the job record is later purged; a currently authorized result lookup may still read an existing retained record. Do not reactivate an expired or unknown job identifier. Thus retention cleanup cannot turn an old signed request into a new mutation. Audit retention is separate and cannot be shortened by job cleanup.

Before acceptance, the runbook must specify who monitors stalled age/cleanup/acknowledgment and audit backlog, who can invoke each action, how authorization is provisioned/revoked, the bounded attempt/deadline/rate-limit policies, how outcomes are communicated to support, and who owns escalation. Permanent integrity damage or an unavailable dependency cannot be safely repaired by pretending this operation succeeded. Those outcomes produce a ticketed diagnosis and accountable escalation, rather than an instruction to edit a database or an unowned “wait indefinitely.”

The minimal operation thus provides a formal, audited recovery entry point for recoverable stalls. It is not a guarantee that every damaged state can be repaired automatically, and it does not grant post-commit cancellation, password reset or emergency revocation.

### 4.6 Required failure and authorization verification

Before accepting this ADR, verify unauthorized/expired/revoked operator access, target scope, admission-permit tampering/expiry/replay after job cleanup, stale versions, same-key changed requests, duplicate operators, invalidation-versus-ownership-commit/material-transfer races, recovery-versus-automatic Ready races, acknowledgment replay after password change, audit-store failure and backlog, crash after remote commit before job completion, execution deadline expiry and all non-success outcomes above. Assert that C01–C03, original timestamps, single Ready/event identity and secret disposal remain intact. These are required tests, not claims of tests implemented or passed.

## Rationale

C01 protects a cardinality invariant; C02 makes uncertain duplicate provisioning recoverable; C03 protects the validity interval between remote confirmation and local Ready. The explicit post-commit acknowledgment makes the release condition verifiable at the authoritative Credential writer without introducing distributed 2PC. It exposes the availability cost instead of hiding it in a blanket no-replacement sentence.

## Alternatives considered

- Polling alone: recovers lost responses but does not close the stale-confirmation race.
- Callback/event-only confirmation: possible alternative, but also requires durable deduplication and a validity/mutation protocol; selected polling is simpler for explicit retry reconciliation in this proposal.
- One-active uniqueness alone: prevents two simultaneous active records, not sequential replacement between confirmation and Ready.
- Local application lock/retry: insufficient across workers and crashes.
- Guard released by timer: rejected; elapsed time is not evidence of committed Ready.
- Accept indefinite stalls with alerting alone: not selected; Decision 4 requires a formal restricted recovery operation before acceptance.
- Generic AdminCancel or direct database unlock: not selected; a single Credential guard cannot cancel an in-flight Identity Ready transaction and would require additional cancellation/ownership semantics.
- Co-located Credential/Identity persistence with a shared transaction/guard: viable architectural alternative with a different deployment constraint. Not selected because this proposal preserves the separate-service case; reconsider if release-protocol cost is not justified for MVP.
- Distributed 2PC: not required; both services make local durable commits and reconcile forward.

## Consequences and propagation gates

These architectural dispositions are accepted within the signed record's scope. They do not certify 07/09, schemas or implementation. Propagation is authorized; generation remains blocked by the upstream decisions and validation gates. Before implementation/rollout clearance, update and review together:

- ADR-0002: explicitly reference the earlier C02 winner point and this protocol without rewriting its existing history as if it selected polling.
- Identity 01/03/04/07/09: authoritative guard ownership, all mutation paths, early winner, acknowledgment, internal administrative recovery job/audit persistence and post-Ready retryable password-change behavior.
- Identity 06: recovery worker attribution as System, distinct initiating-operator audit provenance and preservation of one Ready/event identity.
- Identity 08 and OpenAPI: distinguish completion from winning password, and expose the retryable finalization failure without leaking secrets.
- machine YAML and services schema: typed guarded confirmation, phase/version, AlreadyCompleted, AcknowledgeRegistrationReady, and internal AdminRecoverStalledRegistration request/result/read contracts; Ready transaction includes acknowledgment Outbox. Internal administration remains separate from the six Person-facing business Commands. Do not silently treat the old schemas as sufficient.
- Identity 10/11/13: acknowledgment retries/escalation, operator grants/step-up, job/replay expiry and rate limits, audit backlog/retention controls, service trust, no timer release, tombstone minimization, and administrative crash/race/authorization tests.
- Identity 12: require this ADR's acceptance and full contract/065/security validation, not just a presence check.

## Related open issue: T16

This ADR does not approve the PersonRegistered/PersonUpdated shared stream. T16 remains a separate architecture-review item; the fact that prior Draft PRs describe it is not an authority for acceptance. It need not prevent choosing one Draft review branch, but it prevents representing all architecture questions as closed.

## PR path and governance

Choosing PR #5 as the sole review vehicle and closing #1–#4 as superseded is a repository-workflow decision, distinct from accepting ADRs or enabling generation. Do not represent publication of this proposal as the user's approval of its architecture or authorization to merge. The maintainer selected PR #5 as the review path and PRs #1–#4 were closed unmerged as superseded. That repository action does not accept any architectural decision; this change neither merges nor reopens a PR.

## Architectural approval and remaining delivery gates

- [x] Owner architectural approval of A01/A02/A03 and Decision 4, including early winner, availability cost and restricted administrative recovery design; signed record at commit 16b720c.
- [ ] Decision 4 administrative recovery contract, state/guard/audit rules, restricted result access and bounded runbook are reviewed and propagated within this ADR; accepting the MVP limitation alone cannot satisfy this gate.
- [ ] Architecture/security and the accountable operations/support owner approve permissions, monitoring/escalation, recovery/audit/replay budgets and responses for unresolved outcomes; no generic unlock or post-commit cancellation is granted.
- [ ] Administrative invalidation/reconciliation races, access revocation, idempotency, audit atomicity/immutability, cleanup and failure outcomes in §4.6 are verified. Listing these requirements is not evidence that they passed.
- [ ] Every supported Credential mutation path is demonstrably guarded; deployment assumptions are enforceable.
- [ ] ADR/Blueprint/API/machine propagation above is completed and reviewed.
- [ ] Cross-service binding, replay, crash, rollback, stale evidence, acknowledgment loss and late-duplicate tests pass.
- [ ] Tombstone erasure/retention and service trust policies approved for MVP; no secret/proof retention is extended.
- [ ] Full applicable 065 validation and ADR-0002 acceptance requirements completed.

## Change history

| Version | Status | Change |
|---|---|---|
| 1.1.1 | Accepted | 2026-09-25: Owner @amirfassadi accepted v1.1.0 architectural content via Identity_ADR-0004_Acceptance_Decision_Record.md at commit 16b720c9cb9afdd60769dcad7b2c4d8c1e2e983c. No technical decision changed; delivery/runtime gates remain open. |
| 1.1.0 | Proposed | 2026-09-25: Added restricted internal AdminRecoverStalledRegistration to this ADR, with two actions, guarded race handling, operator authorization, mandatory append-only audit and bounded support outcomes. Removed limitation-only acceptance; Blueprint/schema propagation remains pending. |
| 1.0.1 | Proposed | 2026-09-25: Recorded stalled-registration administrative recovery as an explicit acceptance choice; distinguished pre-commit contact abandonment from post-provisioning reconciliation failure. No unlock, TTL or protocol change. |
| 1.0.0 | Proposed | Explicit A01/A02/A03 disposition with durable mutation guard, early winner, registration-lifetime deduplication and post-Ready acknowledgment. No Blueprint behavior or acceptance status changed by this document. |
