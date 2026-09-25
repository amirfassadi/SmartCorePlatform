<!--
Document ID: ID-16
Title: SmartCore Identity Platform Blueprint - Examples
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity examples contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Informative mobile-only registration

Initial request to POST /auth/register (synthetic values; generate real random binding/key in clients):

```json
{"mobile":"+12025550123","password":"example-only-long-password","displayName":"Example Person","bindingSecret":"<256-bit-random-value>"}
```

202 contains verificationSessionId and absolute expiresAt. Submit its code and binding to /auth/register/verify. First ownership commit returns:

```json
{"registrationId":"7aad209e-11f0-4ad0-9415-f4854a8e6904","status":"PendingCredential","ownershipCommittedAt":"2026-09-24T10:00:00Z"}
```

Replay with the same proof within expiry may return Ready with readyAt. After that, sign in with mobile/password. No email:null or Session tokens appear in registration results.

# 2. Delayed readiness

Ownership commits at 10:00; Credential becomes usable at 13:00. OrganizationCreated/MembershipCreated have OccurredAt 10:00. PersonRegistered has OccurredAt 13:00 and OwnershipCommittedAt 10:00, no SessionReference and no Email for this Person. Delivery at 13:05 changes neither timestamp.

# 3. Lost response after expiry

Fresh contact verification discovers an existing PendingCredential registration. Its newly entered password is discarded. Request a distinct setup code and submit a new candidate through /auth/register/complete. The automatic winner, if already present, cannot be replaced by that candidate. The client never treats a registrationId as password-setting authority.

# 4. Lost Ready acknowledgment (informative)

Ready commits with ReadyFactId and acknowledgment Outbox, but delivery is interrupted. The Person may sign in; ChangePassword returns 503 PROVISIONING_FINALIZATION_PENDING until the Credential guard records the acknowledgment. A scoped operator prepares a ReconcileCommittedRegistration job from the trusted operations view, submits the unchanged permit-bound request and follows its authorized result. Only confirmation of the same acknowledged fact yields Reconciled. No timer or operator-provided credentialId releases the guard.

# 5. Setup candidate did not win

A setup completion may return status Ready with credentialOutcome ExistingWinner. This means the earlier initial Credential remains selected; the just-submitted password was not installed. It does not expose the Credential or grant a password reset.
