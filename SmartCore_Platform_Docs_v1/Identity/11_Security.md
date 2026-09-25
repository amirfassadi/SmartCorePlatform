<!--
Document ID: ID-11
Title: SmartCore Identity Platform Blueprint - Security
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity security contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Authentication and authorization

Registration code possession proves selected contact control for registration only. A verificationSessionId, registrationId, email or phone alone never authorizes replay or password setup. Same proof and high-entropy binding are required for replay. Setup uses a separately delivered, purpose/registration-bound code; it is not general account recovery. Ready plus an active Credential is mandatory at login/refresh; availability failure denies issuance.

Self operations derive Person from Session and enforce ownership. Service calls use authenticated allowlisted identities with minimum purpose scopes. Business authorization remains outside Identity.

# 2. Secret lifecycle

Use CSPRNG six-digit codes and at least 128-bit opaque session/challenge IDs. Codes remain low entropy and require the configured strict attempt/delivery limits; no offline verification endpoint is permitted. Store code/binding/request verifiers using domain-separated HMAC with server-managed keys, session ID and purpose; constant-time comparison online only under cumulative budgets. A plain OTP hash is forbidden because low-entropy codes are enumerable offline. Never log raw proof, password, binding secret or bearer token. Key rotation, compromise revocation and key IDs are operationally managed, with no validity extension.

Stage password-provisioning material with authenticated encryption and restricted Credential-service access; bind owner/purpose and absolute expiry as authenticated metadata. Long-term Credential uses an approved salted password KDF with versioned cost configuration, not reversible storage. Choose/benchmark KDF parameters under platform security approval before deployment; this document does not claim a cryptographic implementation.

Invalidation is immediate logical denial; disposal is mandatory within 10's bound. Transfer reference ownership atomically at commit so cleanup cannot destroy live provisioning work. On a second conflicting attempt, discard its password; setup must obtain a new candidate through its own proof. No raw passwords in Outbox/public events/backups.

# 3. Enumeration and abuse

Initial and resend status/body/headers/timing class/delivery behavior must not reveal contact uniqueness. Deliver verification for valid-format contacts regardless of whether they exist, under the same budgets. Invalid/expired identifiers use uniform responses without sending secrets to arbitrary destinations. Login unknown/pending/missing-Credential/wrong-password share one response and comparable work; avoid expensive KDF work before abuse throttles. Test latency distributions under load rather than promising identical nanosecond timing.

Verification conflict detail is available only after valid proof. Setup response must not disclose state without its prerequisite proof and cannot issue a working challenge for a Ready registration. Counts are shared across workers; concurrent requests cannot exceed limits. Rate-limit based on normalized contact, trusted IP and global/provider budgets, with consistent treatment of nonexistent contacts.

# 4. Data minimization and audit

Person self DTO exposes its chosen verified contact; service lookup exposes neither. PersonRegistered/PersonUpdated omit Mobile and optional missing Email intentionally. LoginFailed is a restricted Security Event; ContactValue and execution metadata are personal data with purpose-limited subscriptions, encrypted storage and retention policy. Treat PersonId in failed login as resolved target attribution, not evidence that the caller authenticated as that Person. Never expose detailed audit Reason through public API.

# 5. Required security review

Threats: code guessing/replay, session fixation, request-binding theft, identifier enumeration, contact takeover, stale cleanup deletion, duplicate provisioning, service spoofing, stolen refresh tokens, logging leakage and denial of service. Tests are in 13. Lost-contact recovery, general password reset, contact changes and Person MFA remain outside this MVP. Operator MFA/step-up for accepted administrative recovery is required; it is not a Person login feature.

# 6. Accepted provisioning/administrative controls

Authenticate the Identity acknowledgment writer and bind registrationId/personId/winner/generation/ReadyFactId. Acknowledge only committed facts from the transactional Outbox. Check every Credential mutation against authoritative phase; an unguarded administrative/service path invalidates the deployment assumptions. Historical results and timed leases do not release the guard.

Operator recovery requires current step-up/MFA and action/environment/target-scoped Identity.RegistrationRecovery permission. Recheck at preparation, admission, result access and every new effectful dispatch. Admission permit is server-authenticated, absolute-expiry, and binds recoveryRequestId plus immutable target/action/snapshot/request descriptor/operator/environment. Log no permit. Execution authorization is bounded/nontransferable and separate from permit expiry; revocation stops new dispatches, not already committed facts.

Schema rejection of force/credential/Ready/password fields is only one layer; service checks must derive facts from authoritative records. Pre-commit invalidation cannot erase transferred material. No administrative reset, cancellation, guard bypass or timer unlock exists.

Audit intent and every local effect commit together; remote acknowledgment records authenticated caller/correlation atomically. Durable audit failure denies mutation; external backlog may buffer only within configured limits. Operator/support/executor roles cannot edit/delete audit evidence or shorten retention. Use separately controlled retention-protected storage and integrity monitoring. Infrastructure break-glass access needs separate external accountability and grants no safe bypass of protocol invariants. See the [runbook](Registration_Recovery_Runbook.md).
