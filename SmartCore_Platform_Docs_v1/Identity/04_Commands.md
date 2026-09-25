<!--
Document ID: ID-04
Title: SmartCore Identity Platform Blueprint - Commands
Version: 1.3.0
Status: DRAFT
Purpose: Define the proposed Identity commands contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.3.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.2.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.1.0; prior text remains in Git history.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Overview

Six business Commands remain. REST protocol operations refine RegisterPerson rather than introducing additional business Commands. Transport-independent service contracts are in [07](07_Contracts.md); wire schemas are in [08](08_API.md).

# 2. Shared rules

Validate input before domain mutation; never reveal contact existence before proof. Self-service Commands resolve Person from the authenticated Session, not a client-supplied PersonId. Infrastructure failure is not domain rejection. No password, code or token may enter event payloads or logs.

# 3. Coordination

RegisterPerson alone uses RegistrationApplicationService for the initial ownership triple and supporting records. Other Commands follow their Aggregate boundaries. Credential setup and later Ready are separate local transactions, never distributed 2PC.

# 4. Specifications

## 4.1 RegisterPerson

Input: exactly one Email or Mobile, Password, DisplayName. Initiation additionally requires a client idempotency key and request binding secret (high entropy). Session identifier alone grants nothing. Verification requires Code plus the same binding secret. Validation: contact syntax, password policy, name limits, code purpose/expiry/attempt budget, and storage-enforced uniqueness after proof.

Pre-commit operations maintain a bounded verification session and encrypted, purpose-bound password-provisioning material. Resend rotates the code, invalidates the old verifier, preserves original expiry and cumulative attempt budget. Responses for initiation/resend are independent of account existence.

After proof, atomically create Person/Personal Organization/Owner Membership, PendingCredential workflow and provisioning Outbox, consume verification and transfer material ownership. Emit OrganizationCreated/MembershipCreated at commit. Return registrationId, state and ownershipCommittedAt; no tokens. ReadyAt appears only after Ready. Secure replay returns the existing result within the original code window.

On verified uniqueness conflict: Ready Person produces generic verified-contact conflict; PendingCredential offers a distinct setup challenge through the stored verified channel. Destroy the second attempt's unused material under the cleanup bound; never attach it to the existing registration. Invalid/expired proof returns a uniform verification error. Storage race loser follows the same verified-conflict path.

Provision asynchronously using registrationId. Bounded exhaustion retains PendingCredential with recoveryNeeded. Setup uses its own proof and idempotency key and cannot replace an already-created initial Credential. Confirm active Credential in ProvisionedAwaitingReady with matching immutable generation, then CAS workflow to Ready, persist ReadyFactId and winner evidence, and atomically enqueue PersonRegistered plus Ready acknowledgment exactly once. Failure never deletes committed ownership.

## 4.2 AuthenticatePerson

Input: exactly one Email or Mobile, Password; optional DeviceInfo. Resolve normalized contact. Require Active Person, Ready workflow and current active Credential; validate password. Create Session and enqueue LoginSucceeded/SessionCreated atomically in Session's local transaction. Return Person plus bearer tokens. Unknown contact, pending registration, missing Credential and invalid password share the same external failure and throttling policy; LoginFailed preserves restricted internal reason. Dependency outage is unavailable and grants no Session.

## 4.3 UpdatePersonProfile

Input: DisplayName (required), authenticated Session, expected Person version. Self only. Reject Email/Mobile and unknown fields. Validate limits, compare version, commit Person update and PersonUpdated with shared stream position in one local transaction. No contact change is authorized. A stale version returns conflict; an unchanged value returns current Person without an event.

## 4.4 LogoutSession

Input: SessionId belonging to caller, authenticated Session. CAS Active to Closed; enqueue LogoutCompleted with terminal transition. Missing Session is not found; foreign Session forbidden; already terminal is conflict. Duplicate delivery emits no second event.

## 4.5 RefreshSession

Input: refresh token. Validate token, Session state/expiry, current Person/registration/Credential gates. Reissue access token with expiry no later than Session expiry; keep refresh token and absolute Session expiry unchanged in this MVP. Return Session token response; no public event. Invalid/expired/revoked token is unauthorized. Token rotation/reuse detection requires a separately versioned policy before adoption.

## 4.6 ChangePassword

Input: currentPassword, newPassword, authenticated self Session. Validate current active Credential and new password policy. In the same authoritative Credential transaction, check the initial provisioning guard. ProvisionedAwaitingReady yields retryable ProvisioningFinalizationPending without mutation/event. Only ReadyAcknowledged permits normal replacement; replace Credential atomically, enforce single active Credential and enqueue PasswordChanged. Invalid current password is unauthorized; policy failure is invalid input. Existing Sessions are unchanged in MVP; general password reset is not introduced.

# 5. Events and ownership

## 5.1 Registration phases

Ownership commit emits OrganizationCreated and MembershipCreated. Ready emits PersonRegistered. Login emits LoginSucceeded and SessionCreated. Login failure is the Security Event LoginFailed. Other mappings are as above. A future ownership-commit signal must be separate; PersonRegistered must never move back to commit time.

# 6. Acceptance

All Commands are proposed and depend on [12](12_Validation.md) and [13](13_Testing.md). Error transport and retry semantics are in [08](08_API.md).

# 7. Internal operations boundary

AdminRecoverStalledRegistration is a separate internal operator contract (07 §7), not a seventh public business Command. It accepts no password, replacement contact, Credential winner, readyFactId or force flag. ReconcileCommittedRegistration executes the existing workflow/acknowledgment path; InvalidatePreCommitAttempt uses the existing verification-consumption/owner-transfer guard. Neither grants another multi-Aggregate ownership exception. Formal audit and current operator authorization are mandatory.
