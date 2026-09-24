<!--
Document ID: ID-01
Title: SmartCore Identity Platform Blueprint - Domain Model
Version: 1.3.0
Status: DRAFT
Purpose: Define the proposed Identity domain model contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.3.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.2.1; prior text remains in Git history.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Domain Model Overview

Five Aggregates own their domain state: Person, Organization, Membership, Credential and Session. Application verification/readiness state belongs to durable supporting records. RegisterPerson's multi-Aggregate ownership transaction is the narrowly proposed ADR-0002 exception, not a general coordination pattern.

# 2. Entities

| Entity | Attributes |
|---|---|
| Person | PersonId, Email (optional), Mobile (optional), DisplayName, Status, CreatedAt, UpdatedAt |
| Organization | OrganizationId, Name, Category, Status, CreatedAt |
| Membership | MembershipId, PersonId, OrganizationId, Role, Status, CreatedAt |
| Credential | CredentialId, PersonId, PasswordHash, PasswordVersion, Status, CreatedAt |
| Session | SessionId, PersonId, AccessTokenId, RefreshTokenId, DeviceInfo, IpAddress, ExpiresAt, Status, CreatedAt |

Exactly one of Email/Mobile is present on an MVP Person and is verified before creation. Absence is omission in public JSON; `null` is not accepted or emitted. Mobile-only Persons do not receive synthetic email addresses. IDs are immutable. DisplayName is mutable; changing or adding a contact requires a separately governed verification/recovery contract and is outside this MVP. Password hashes never leave Credential's security boundary.

## Relationships

Person has exactly one Personal Organization through one Owner Membership in MVP (future model supports more). Membership references one Person and one Organization. Person has zero or one active Credential while PendingCredential and exactly one on the transition to Ready. Multiple Sessions may exist after successful authentication. Ready is a historical registration completion fact, not a perpetual assertion that a Credential can never later be revoked. Authentication checks current Credential state as well as Ready.

# 3. Value Objects

- EmailAddress: syntactically valid normalized email; trim surrounding whitespace and use the existing case-insensitive comparison policy. Do not strip plus tags or provider-specific dots. Delivery and uniqueness use the same normalization version.
- MobileNumber: explicit country code in E.164 representation; no guessed country. Delivery and uniqueness use the same canonical value.
- PasswordHash: approved salted password KDF output with algorithm/version metadata; not reusable encrypted plaintext.
- AccessTokenId: token identity; public bearer material is distinct from persistence identifiers.
- RefreshToken: revocable continuation credential stored using a protected verifier.

Exactly one selected verified contact is an entity invariant, not a requirement that each optional value object exist.

# 4. Aggregate Definitions

Each Aggregate has exactly one owning Repository. Supporting records cannot write Aggregate state directly. Credential and Session are independent lifecycle boundaries. See [03](03_Aggregates.md).

# 5. Aggregate Lifecycles

Person: Registered → Active → Suspended → Archived. Organization: Created → Active → Suspended → Archived. Membership: Created → Active → Revoked. Credential: Created → Active → Replaced/Revoked. Session: Created → Authenticated → Active → Suspended (future) → Expired or Closed.

MVP commits Person/Organization/Membership as Active. Replacement Credential and Session expiration/logout are supported; other administrative lifecycle commands remain future scope under ADR-0003. These lifecycle summaries do not add Commands.

# 6. Invariants

Every Person has ownership context; ownership triple creation is atomic. Contact uniqueness is enforced in storage, including PendingCredential Persons. At most one active Credential exists for a Person. Password setup cannot bypass this invariant. No Session is issued unless Person is Active, registration is Ready and the current active Credential validates. Session termination never removes Person or ownership.

# 7. Domain Services

| Service | Responsibility | Events |
|---|---|---|
| AuthenticationDomainService | Check readiness/current Credential; create Session | LoginSucceeded, LoginFailed, SessionCreated |
| PersonManagementDomainService | Self-service DisplayName update | PersonUpdated |
| CredentialManagementDomainService | Provision/replace Credential with one-active invariant | PasswordChanged on authenticated change only |
| SessionManagementDomainService | Refresh, expire, close Session | SessionExpired, LogoutCompleted |

# 8. Application Services

RegistrationApplicationService owns pre-commit verification, atomic ownership creation and post-commit provisioning coordination. The initial Unit of Work contains three Aggregate writes plus registration/verification records and Outbox inserts. Ready uses a later local workflow/event transaction; it writes no Person lifecycle state. Domain Credential rules remain in CredentialManagementDomainService.

OrganizationCreated and MembershipCreated are enqueued with ownership commit. PersonRegistered is enqueued only with Ready, with separate OwnershipCommittedAt. Initial setup does not produce PasswordChanged. No initial Session is created by the proposed REST registration contract.

# 9. Domain Rules and supporting records

`RegistrationWorkflow`: registrationId, PersonId, OrganizationId, MembershipId, OwnershipCommittedAt, state (PendingCredential/Ready), ReadyAt if Ready, provisioning correlation, retry/recovery metadata and version. References to secrets are protected opaque handles, never public fields.

`VerificationSession`: verificationSessionId, purpose, normalized selected contact, request binding, keyed code verifier, protected material reference, absolute expiresAt, attempt/resend counters, state and optional consumed registration mapping. Lifetime and disposal are in [09](09_Persistence.md) and [10](10_Configuration.md).

# 10. Future Extensions

Contact changes/addition, lost-contact recovery, social login, MFA, Organization administration and general account recovery require separate governance. They are not implied by PendingCredential completion.
