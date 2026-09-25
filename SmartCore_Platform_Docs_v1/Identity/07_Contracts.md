<!--
Document ID: ID-07
Title: SmartCore Identity Platform Blueprint - Interoperability Contracts
Version: 1.2.0
Status: DRAFT
Purpose: Define the proposed Identity interoperability contracts contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.2.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.1.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.0.2; prior text remains in Git history.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Contract boundary

Per 064 §§8.8–8.9, this file owns transport-independent service and message contracts. REST request/response shapes previously here are consolidated in [08_API](08_API.md); there is one authoritative wire definition. Names below are internal operations, not additional public business Commands or events.

The companion `services.schema.json` defines proposed camelCase message encodings for these service operations; it does not add public REST endpoints. Transport authentication and cross-field equality checks (such as materialOwner = registrationId) are mandatory service rules, not inferred from schema type checks.

# 2. IdentityLookup v1

`GetPersonById(PersonId) -> Found(PersonId, DisplayName) | NotFound`.

Only authenticated, allowlisted capability identities may call. Return no contact, Credential, Session or readiness information. Consumers decide their own business authorization. This service cannot be used as a readiness check.

# 3. CredentialProvisioning v1.1 (accepted architecture, Draft encoding)

## 3.1 EnsureInitialCredential

Input: registrationId, personId, operationId, protectedMaterialRef, materialOwner=registrationId, purpose=`initial-registration`. Automated operationId is registrationId; a separately authorized setup uses setupChallengeId. Authenticate and authorize the Identity caller, purpose and material ownership. Client/operator input cannot directly invoke provisioning or select the winner.

In one authoritative Credential transaction, enforce C01 and commit the first active Credential, immutable C02 winner binding and phase ProvisionedAwaitingReady. Same accepted operation with identical binding returns that result; changed winning request is BindingConflict. A different candidate after a winner exists is rejected as AlreadyProvisioned with guarded winner evidence while awaiting Ready, or AlreadyCompleted after acknowledgment; it never overwrites the password. No indefinite loser-password/request retention is introduced.

Responses: Active, AlreadyProvisioned, AlreadyCompleted, RetryableUnavailable, InvalidMaterial, BindingConflict or IntegrityConflict. Only Active/AlreadyProvisioned in ProvisionedAwaitingReady assert a currently active guarded winner. Secret material is absent from all results. Winner identity is fixed at Credential commit, earlier than Ready; setup completion must distinguish whether its candidate won.

## 3.2 GetInitialCredentialResult

Input: registrationId/personId under authenticated service authorization. Responses: NotProvisioned, Active (guarded evidence), AlreadyCompleted (historical winner, no current-active assertion), Unavailable or IntegrityConflict. Poll to reconcile uncertain commits under bounded policy. Active includes credentialId, operationIdOfWinner, phase=ProvisionedAwaitingReady and immutable provisioningVersion. This token is not changed by polling/retries/counters. No network call is made inside Identity's Ready transaction.

Only matching active guarded evidence authorizes the subsequent local Ready CAS. Identity PendingCredential combined with ReadyAcknowledged/AlreadyCompleted is an integrity/recovery conflict, not a reason to recreate Ready. The Credential service protects validity by requiring every supported mutation to check the same durable guard atomically. A deployment with an unguarded write/revoke path is incompatible.

## 3.3 Ready reconciliation

Identity atomically CASes PendingCredential→Ready, persists immutable readyFactId and winner evidence, and enqueues PersonRegistered plus Ready acknowledgment. A repeated Ready confirmation is a no-op preserving timestamps/fact identity. The T16 stream-position insertion remains a separate proposed ordering requirement, not an accepted consequence of ADR-0004.

Winning candidate provenance is separate from the actual Ready actor. A synchronous Person request records PersonId; automatic or administrative recovery worker records System. Operator identity belongs to restricted audit, not the Person event actor.

## 3.4 AcknowledgeRegistrationReady

Internal request: registrationId, personId, credentialId, provisioningVersion, readyFactId. Identity's trusted Outbox sends only committed Ready facts. Credential validates all bindings and atomically changes ProvisionedAwaitingReady→ReadyAcknowledged with durable acknowledgment/audit evidence. Return Acknowledged or AlreadyAcknowledged with the same bindings; Unavailable, BindingConflict and IntegrityConflict are failures.

Check a matching stored acknowledgment before current Credential state: a duplicate after a legitimate password change remains successful and must not restore the initial Credential. A different fact/generation is rejected. No user, operator-supplied readyFactId or timer may release the guard. Lost acknowledgment responses are retried idempotently; exhausted budgets alert and preserve the guard.

Ready can permit login before acknowledgment delivery, but ChangePassword remains retryably unavailable until ReadyAcknowledged. Neither delivery failure nor administrative re-drive rolls Ready backward.

## 3.5 Retention

Keep the minimal winner/phase/acknowledgment binding for registration lifetime; MVP has no time-based deletion or registration-identity reuse. Candidate fingerprint derives from opaque internal candidate identity and non-secret request metadata, never password/OTP/binding-secret material. Delete proof verifiers and unused material on their separate deadlines. Historical results grant no current-active assertion, login or password-setting authority. Late provisioning never resurrects revoked/replaced Credentials.

# 4. Protected material and challenge delivery

The secret store supports stage(owner=verificationSessionId, expiry), bind-to-registration within Identity's durable transaction/reference protocol, authorize-read for the scoped Credential service, and invalidate/delete. Physical secret movement need not be transactional; durable references and ownership are. Failed commit leaves only pre-commit-owned expiring material, never a committed reference to disposed material.

Delivery accepts selected canonical contact, purpose and code; it reveals no account-existence result to the caller. Templates never include passwords. Technical delivery is infrastructure, not a business Communication dependency. Setup delivery reads the verified contact from committed Person; it does not trust a caller-supplied destination.

# 5. Event integration contract

The ten events and PascalCase payload/envelope fields are authoritative in [06](06_Domain_Events.md). Optional fields are omitted, never null. PersonRegistered has optional Email, deliberately no Mobile contact payload, required OwnershipCommittedAt, Ready-time OccurredAt and no SessionReference. Consumers identify mobile-only Persons by PersonId; adding Mobile later requires consumer/privacy review rather than silently widening exposure.

PersonUpdated follows the same optional-Email minimization; LoginFailed accepts selected ContactType/ContactValue in its restricted security payload. No secrets are included. Registration/profile stream position is transport metadata preserved through Outbox and broker; it is not Aggregate version. Consumers deduplicate by EventId before applying monotonically ordered positions. Only PersonRegistered and PersonUpdated join that stream.

# 6. Compatibility and acceptance

These wire/service encodings are Draft; ADR-0004 architecture is accepted, while ADR-0002 and T16 are not. Confirm deployed consumers and contract-version policy before acceptance; absence of consumers has not been demonstrated by this repository. Optional Email, changed timestamps, narrowed profile updates and registration responses are real contract changes. Do not silently deploy to an existing v1 client. Governance must select migration/version routing if any such consumer exists.

# 7. RegistrationRecovery v1.0 — internal operator contract

The exact message shapes are in services.schema.json. This is not part of public OpenAPI. The administrative model implements ADR-0004 Decision 4; concrete encodings remain reviewable Blueprint detail.

## 7.1 PrepareRegistrationRecovery

The authorized operations view takes action, targetKind/targetId, allowlisted reasonCode, validated ticketReference and correlationId. It reads the current eligible state/version and issues a server-generated recoveryRequestId and signed/MAC-protected admissionPermit binding the operator/environment, action/target, snapshot and immutable request descriptor, with admissionExpiresAt. Responses: Prepared or a restricted error (Unauthorized/Forbidden/InvalidRequest/NotEligible/RateLimited/Unavailable/AuditUnavailable). Preparation creates no recovery job or domain mutation. No target details are exposed to unauthorized callers.

## 7.2 AdminRecoverStalledRegistration

Input is the prepared immutable descriptor plus recoveryRequestId, admissionPermit and expectedState/expectedVersion. Exactly two action/target pairs are valid: InvalidatePreCommitAttempt→VerificationSession, or ReconcileCommittedRegistration→Registration. Reject supplied secrets, replacement contacts, credentialId, readyFactId and force flags. Operator identity comes from authenticated context; check MFA/step-up, explicit action scope, target/environment and current grant at admission and before every new effectful dispatch.

Current eligibility/version, request binding and audit intent are committed atomically with durable job/dispatch work. StaleTarget/NotEligible/AdmissionExpired/BindingConflict/AuditUnavailable create no mutation. The same authorized request under a still-valid admission permit returns its existing job. After admission expiry, submission is rejected; a currently authorized GetRegistrationRecoveryResult may still read the retained job. Execution deadline is fixed at admission; retry cannot extend it or reset budgets. Previously committed ordinary reconciliation may finish after operator authorization expires; no rollback or guard bypass follows.

| State/action | Required result |
|---|---|
| Unconsumed verification attempt | Invalidate under consumption/owner-version guard and enqueue disposal; Invalidated with cleanupState=Pending until CleanupCompleted |
| Already expired/invalidated | AlreadyInvalidated; ensure disposal remains scheduled durably |
| Registration/material transfer won race | AlreadyCommitted; do not delete transferred material or switch targets |
| PendingCredential + active guarded winner | Canonical Ready CAS and acknowledgment; Reconciled only after matching acknowledgment confirmed |
| Ready + pending acknowledgment | Re-drive existing readyFactId; no new event/time |
| Ready + recorded matching acknowledgment | AlreadyReconciled |
| No provisioned winner | RequiresNormalProvisioning or RequiresUserSetup; no candidate supplied by admin |
| Binding/phase/winner inconsistency | IntegrityConflict; no mutation, ticketed escalation |
| Outage/deadline/budget | RetryableUnavailable, AuthorizationExpired or BudgetExhausted; retain guard |

The worker always re-reads authoritative state; an expected version never authorizes forcing an old effect. See [runbook](Registration_Recovery_Runbook.md) for non-success handling.

## 7.3 GetRegistrationRecoveryResult

A currently authorized operations caller supplies recoveryRequestId; result is Accepted/Running, or Completed/Stopped with a typed outcome, correlation and relevant non-secret state evidence. Cleanup and acknowledgment milestones remain distinct. An expired admission permit cannot authorize a new job, but current operator authorization may read a retained result. NotFound for an absent authorized lookup; no registration/secret data to unauthorized callers.

Completion requires recorded effects, not merely dispatch. An immutable audit trail records intermediate observations even if a job stops before normal service work completes; a later read may additionally observe current registration state without claiming the old job performed new authorized work. Recovery request deduplication survives both permit expiry and execution termination, plus configured result retention. Purging a finished job cannot make an expired signed request admissible again.

## 7.4 Audit and support

Each local effect commits audit journal/Outbox evidence atomically. Credential acknowledgment similarly records caller/correlation and phase mutation. No durable audit evidence means no mutation. External collector outages are buffered only within configured bounds; exceeded bounds pause new administrative effects. Audit is append-only and non-deletable by operator/support roles, with retention-protected external storage and separate control. No raw permit, proof, password or bearer value is logged. Typed schemas cannot prove authorization, cross-field equality, transaction atomicity or retention; those remain runtime tests in 13.
