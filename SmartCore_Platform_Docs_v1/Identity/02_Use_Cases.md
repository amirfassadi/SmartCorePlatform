<!--
Document ID: ID-02
Title: SmartCore Identity Platform Blueprint - Use Cases
Version: 1.4.1
Status: DRAFT
Purpose: Define the proposed Identity use cases contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.4.1 (2026-10-04): Made required-content and preserved constraints explicit from existing sources; decisions, generation status and runtime evidence unchanged.
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

# 6. Explicit required-content mapping

The following makes the seven 064 §8.3 fields explicit for each existing case. It indexes the current Draft behavior, not SESSION/S2 adoption or a new public operation. Shared proof/material failures remain governed by 08/11/13; internal substeps are not callable independently.

| Use case | Goal | Actors | Preconditions | Main Flow | Alternative Flows | Failure Conditions | Postconditions |
|---|---|---|---|---|---|---|---|
| UC-001 | Establish verified-contact ownership and eventually usable registration | Prospective Person; authorized registration coordinator | One contact, password/name, proof and binding gates in 04 §4.1 | Initiate/verify, commit ownership/PendingCredential, provision/reconcile under 04 §4.1 and 07 §3 | Bounded authorized replay, verified pending conflict and distinct setup in §3 | Proof/expiry/budget/uniqueness/outage failures in 04 §4.1 and 08 §5 | No ownership before proof; atomic committed ownership; Pending or Ready; no initial Session |
| UC-002 | Establish one guarded initial Credential | Authorized worker or completion process | Committed registration; authorized work or distinct setup proof | Ensure initial Credential under 07 §3.1 | Same binding returns winner; uncertain result is polled; automatic/setup candidates race under 07 §3 | Unavailable, binding/integrity/expired-material failures in 07 §3 | One active initial winner, guard retained; ownership is preserved |
| UC-003 | Authenticate an eligible Person | Person presenting password | Active Person, Ready workflow, current active Credential, 04 §4.2 | Validate chosen contact/password; create Session and success facts | Definitive rejection versus unavailable dependency, 04 §4.2 | Invalid credentials/gates or dependency unavailable; generic response, restricted final-rejection audit | Active Session and success events on commit; rejected/unavailable paths issue no Session |
| UC-004 | Create the authenticated Session within authentication | AuthenticationDomainService | UC-003 succeeds, including current eligibility gates | Session creation and success-event enqueue share 09 §5.2 transaction | Session persistence failure follows unavailable branch; no independent Session-creation route | Existing 02 §2 unavailable/no-token outcome; 04 §4.2 capacity and persistence limits | Committed Active Session or no Session/tokens; registration remains Ready |
| UC-005 | Change own DisplayName | Authenticated self | Valid Session, name policy and expected Person version | 04 §4.3 atomic Person mutation and PersonUpdated | Same normalized value is no-op; stale version conflicts | Invalid/contact-mutation input, unauthorized caller, conflict/unavailable | Changed snapshot/event on commit, otherwise unchanged state; contact stays verified and unchanged |
| UC-006 | Replace own active password Credential | Authenticated self | Current password/new policy, current Session and ReadyAcknowledged guard | 04 §4.6 Credential replacement and PasswordChanged | Guard pending returns finalization-pending without mutation, §5 | Invalid password/policy/auth or unavailable guard/store, 08 §7 | One active Credential and event on success; Sessions unchanged in active Draft, SESSION candidate not adopted |
| UC-007 | End a Session once | Authenticated self or expiration worker | Caller-owned Active Session for logout; elapsed Active Session for expiry | Winning terminal CAS under 04 §4.4 / 06 §6.4 | Logout or expiry wins; stale duplicate emits no additional terminal fact | Missing/foreign/terminal logout is rejected per 04 §4.4; failed persistence emits no terminal fact | Exactly one applicable terminal transition/event; Person/ownership preserved |
| UC-008 | Create initial Owner Membership atomically | Registration process | Authorized ownership transaction with Person/Personal Organization | Membership creation in 09 §5.1 ownership UoW | A failed substep rolls back the entire UoW; retry/conflict follows UC-001, no independent membership flow | Any required ownership write fails, 09 §5.1.2 | One initial Owner Membership with complete committed ownership, or none of the ownership writes commit |
| UC-009 | Continue eligible Session within its fixed lifetime | Refresh-token holder | Token and current eligibility/Session/deadline checks, 04 §4.5 | Reissue bounded access token under the current nonrotation Draft | Invalid, expired or revoked token is rejected; no independently selected grace/S2 path | 04 §4.5 token/gate rejection or dependency unavailable | Same Session/refresh token and absolute deadline; bounded access reissue, no public event; V-002 remains OPEN |
