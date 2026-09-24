<!--
Document ID: ID-11
Title: SmartCore Identity Platform Blueprint - Security
Version: 1.0.0
Status: DRAFT
Purpose: Define the proposed Identity security contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

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

Threats: code guessing/replay, session fixation, request-binding theft, identifier enumeration, contact takeover, stale cleanup deletion, duplicate provisioning, service spoofing, stolen refresh tokens, logging leakage and denial of service. Tests are in 13. Lost-contact recovery, general password reset, contact changes, MFA and administrator setup remain outside this proposal.
