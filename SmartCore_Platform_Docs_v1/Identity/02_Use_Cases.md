<!--
Document ID: ID-02
Title: SmartCore Identity Platform Blueprint - Use Cases
Version: 1.4.0
Status: DRAFT
Purpose: Define the proposed Identity use cases contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.4.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.3.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.2.0; prior text remains in Git history.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Scope

All cases follow [Commands](04_Commands.md), [API](08_API.md), [Security](11_Security.md) and [Persistence](09_Persistence.md). Unauthenticated verification is not a Session. No public command is added for an internal substep.

# 2. Use cases

| ID | Case and actor | Preconditions / main flow | Result and failures |
|---|---|---|---|
| UC-001 | Register Person; prospective Person | Submit one contact/password/DisplayName; verify code; atomically commit ownership and PendingCredential workflow; provision and reconcile | Pending or Ready with stable reference; generic pre-proof responses; verified uniqueness conflict routes pending registration to secure completion; no tokens |
| UC-002 | Create Credential; authorized registration worker or completion process | Committed registration; authorized provisioning work or distinct setup proof; idempotent ensure-initial-Credential | One active Credential; bounded retries; existing winner returned without replacement; no ownership compensation |
| UC-003 | Authenticate Person; Person | Resolve chosen normalized contact; check Active Person, Ready workflow and active Credential; validate password | Session plus LoginSucceeded/SessionCreated, or generic failure with restricted LoginFailed audit |
| UC-004 | Create Session; AuthenticationDomainService | Successful authentication including readiness gate | Active Session; failure returns unavailable without tokens; registration remains Ready |
| UC-005 | Manage Person Profile; authenticated self | Validate DisplayName and optimistic version; update Person and enqueue event atomically | PersonUpdated snapshot; contact mutation rejected |
| UC-006 | Change Credential; authenticated self | Validate current password and policy for new password; replace active Credential atomically | One active Credential and PasswordChanged; unrelated Sessions unchanged in MVP |
| UC-007 | End Session; self or expiration worker | Self logout closes active Session; worker expires an elapsed active Session with CAS | Exactly one winning terminal transition/event (LogoutCompleted or SessionExpired); stale duplicate does not emit again |
| UC-008 | Create Organization Membership; registration process | Internal substep of ownership UoW | One Owner Membership in Personal Organization; rollback with all ownership writes on failure; no standalone public route |
| UC-009 | Refresh Session; token holder | Validate refresh token and active, unexpired Session; check current readiness/identity/credential gate | Reissue access token; retain current refresh token until Session expiry in MVP; no public event; no lifetime extension |

# 3. Interrupted registration

Lost pre-commit responses are retried with the same initiation idempotency key and identical input. Lost ownership responses are recovered by the same verified-session proof and request binding within its original validity; no second ownership commit. After expiry, verify contact through a new attempt. A PendingCredential conflict invalidates that attempt's staged password and directs the holder to a distinct setup challenge. Only proof of that setup challenge can authorize a new password candidate. Automatic provisioning and setup race through a single initial-Credential winner; the loser never replaces it.

# 4. Out of scope and acceptance

No contact editing, lost-contact recovery, invitations, general password reset, administrative lifecycle commands or new public events. The failure, race and leakage cases in [13](13_Testing.md) remain implementation acceptance gates, not executed tests.

# 5. Accepted protocol refinements

UC-002 commits the winning Credential and its guarded initial outcome atomically. UC-001 confirms only active guarded evidence, then commits Ready, ReadyFactId, PersonRegistered and acknowledgment work together. It never treats a historical AlreadyCompleted result as a fresh active confirmation.

UC-006 additionally checks the durable Credential guard in its mutation transaction. If acknowledgment is pending, return retryable finalization-pending without a password change or PasswordChanged event. UC-003 may authenticate once Identity is Ready and the current Credential validates even while acknowledgment delivery is pending.

Internal operations staff may prepare and invoke AdminRecoverStalledRegistration (07 §7). This is not UC-005 or a new public user Command: invalidation races with pre-commit consumption; committed recovery uses canonical Ready/acknowledgment transactions. Recovery cannot supply a password, create Ready evidence or revoke/replace the winner.
