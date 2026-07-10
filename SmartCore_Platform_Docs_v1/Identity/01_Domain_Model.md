<!--
Document ID: ID-01
Title: SmartCore Identity Platform Blueprint - Domain Model
Version: 1.1.0
Status: READY_FOR_GENERATION
Purpose: Define the domain model, aggregates, entities, and value objects for the Identity Platform Blueprint
Dependencies: 019_SmartCore_Identity_and_Session_Continuity_Model, 041_SmartCore_Identity_Model, 064_SmartCore_Blueprint_Standard
Change Log:
  - Version 1.1.0 (2026-07-08): Added metadata completion, relationships section, missing domain services, session lifecycle correction, SessionToken resolution (added AccessTokenId), event audit requirements
  - Version 1.0.0 (2026-06-01): Initial domain model definition
-->

# 1. Domain Model Overview

The Identity Domain consists of five Aggregates:

- Person
- Organization
- Membership
- Credential
- Session

All state changes SHALL occur through Aggregate Roots.

Cross-Aggregate coordination SHALL occur through Domain Services.

---

# 2. Entities

## Person

Represents a human identity.

Attributes:

- PersonId
- Email
- DisplayName
- Status
- CreatedAt
- UpdatedAt

Identity is immutable.

Email may change.

DisplayName may change.

---

## Organization

Represents ownership boundary.

Attributes:

- OrganizationId
- Name
- Category
- Status
- CreatedAt

Category MVP:

- Personal

Future categories belong to future scope.

---

## Membership

Represents participation.

Attributes:

- MembershipId
- PersonId
- OrganizationId
- Role
- Status
- CreatedAt

MVP Role:

- Owner

---

## Credential

Represents authentication material.

Attributes:

- CredentialId
- PersonId
- PasswordHash
- PasswordVersion
- CreatedAt

Credential never stores plain text passwords.

---

## Session

Represents authenticated execution context.

Attributes:

- SessionId
- PersonId
- AccessTokenId
- RefreshTokenId
- DeviceInfo
- IpAddress
- ExpiresAt
- Status
- CreatedAt

---

# Relationships

Person (1) → (1..*) Membership
Organization (1) → (1..*) Membership
Membership (1) → (1) Person
Membership (1) → (1) Organization
Person (1) → (0..*) Session
Person (1) → (1) Active Credential

Note: Do NOT introduce Credential History in MVP. Credential History belongs to future extensibility.

---

# 3. Value Objects

## EmailAddress

Represents normalized email.

Rules:

- Required
- Valid format
- Case-insensitive comparison

---

## PasswordHash

Represents credential hash.

Rules:

- Immutable
- Generated using approved hashing algorithm

---

## AccessTokenId

Represents access token identity.

Token content is implementation-specific.

Note: This Value Object replaces the former SessionToken to maintain consistency with Session attributes.

---

## RefreshToken

Represents session continuation token.

Must be revocable.

---

# 4. Aggregate Definitions

Aggregate Roots:

- Person
- Organization
- Membership
- Credential
- Session

Each Aggregate owns its internal consistency.

Cross Aggregate consistency belongs to Domain Services.

---

# 5. Aggregate Lifecycles

## Person Lifecycle

Registered
↓
Active
↓
Suspended
↓
Archived

---

## Organization Lifecycle

Created
↓
Active
↓
Suspended
↓
Archived

Lifecycle diagrams represent MVP-visible lifecycle flow.

Full lifecycle transition rules, including reversible transitions such as Suspended → Active, are defined in ADR-0003.

No lifecycle transition commands are part of MVP.

---

## Membership Lifecycle

Created
↓
Active
↓
Revoked

---

## Credential Lifecycle

Created
↓
Active
↓
Replaced
↓
Revoked

---

## Session Lifecycle

Created
↓
Authenticated
↓
Active
↓
Suspended (optional)
↓
Expired
↓
Closed

Note: Suspended state is optional and aligns with Document 019 §6.

---

# 6. Domain Invariants

## Person Invariants

- PersonId is immutable
- Person MUST belong to at least one Organization
- Person MUST own at least one Membership after registration
- Identity survives Session expiration

---

## Organization Invariants

- OrganizationId is immutable
- Organization owns resources
- Organization is tenancy boundary
- Organization MUST have at least one Membership

---

## Membership Invariants

- Membership MUST reference one Person
- Membership MUST reference one Organization
- Membership is the only participation path

---

## Credential Invariants

- Password SHALL NOT be stored in plain text
- Credential MUST belong to one Person

---

## Session Invariants

- Session MUST reference one Person
- Session expiration SHALL NOT remove Identity
- Session MAY be revoked

---

# 7. Domain Services

## RegistrationDomainService

Coordinates atomic registration across core ownership transaction and post-commit operations.

### Core Transaction Phase

Responsibilities (atomic, single transaction):

- Create Person
- Create Organization (Personal Organization)
- Create Membership (Owner role)

Transaction Commit: All three ownership entities must be successfully persisted.

### Post-Commit Phase

Responsibilities (after transaction commit, non-blocking):

- Create Credential
- Request Initial Session creation through Authentication lifecycle
- Publish Registration Events

Produces:

- PersonRegistered
- OrganizationCreated
- MembershipCreated

**Note**: SessionCreated is produced by AuthenticationDomainService after successful Initial Session creation.
RegistrationDomainService coordinates the registration flow but does
not own Session lifecycle events.

**Transaction Semantics**: Core transaction failure rolls back all ownership changes. Post-commit operation failures do not invalidate ownership relationships.

---

## AuthenticationDomainService

Responsibilities:

- Validate Credential
- Resolve Person
- Create Session

Produces:

- LoginSucceeded
- LoginFailed
- SessionCreated

---

## SessionManagementDomainService

Responsibilities:

- Refresh Session
- Revoke Session
- Expire Session

Produces:

- SessionExpired
- LogoutCompleted

---

## PersonManagementDomainService

Responsibilities:

- Update Person Profile

Produces:

- PersonUpdated

---

## CredentialManagementDomainService

Responsibilities:

- Change Password
- Replace Credential

Produces:

- PasswordChanged

Note: Do NOT introduce `OrganizationManagementDomainService` or `MembershipManagementDomainService` into MVP. Lifecycle transition commands for Suspended / Archived / Revoked are future scope.

---

# Event Producer Mapping

The following Domain Services produce the events declared in 059_SmartCore_Identity_Platform.md Event Ownership Table.

This mapping ensures event ownership traceability and MVP scope validation.

## RegistrationDomainService Produces

- PersonRegistered
- OrganizationCreated
- MembershipCreated

## AuthenticationDomainService Produces

- LoginSucceeded
- LoginFailed
- SessionCreated

## SessionManagementDomainService Produces

- SessionExpired
- LogoutCompleted

## PersonManagementDomainService Produces

- PersonUpdated

## CredentialManagementDomainService Produces

- PasswordChanged

**Validation Note**: All 10 events in 059 Event Ownership Table are accounted for by MVP Domain Services. No orphaned or unclassified events exist.

---

# 8. Domain Rules

Rule-001

Every Person SHALL belong to at least one Organization.

Rule-002

Registration SHALL be atomic.

Rule-003

Resources SHALL NOT belong directly to Persons.

Rule-004

Authorization SHALL be evaluated through Membership.

Rule-005

Authentication SHALL remain independent from Authorization.

Rule-006

Identity SHALL remain independent from Session.

---
# Event Audit Requirements

All Domain Events SHALL support:
- Actor Identity
- Session Reference (optional)
- Delegated Identity (optional)
- Timestamp
- Execution Context

Detailed event contracts are defined in 06_Domain_Events.md.

---
# 9. Future Extensions

Future versions MAY introduce:

- MFA Credential
- OAuth Credential
- Social Identity
- Delegated Identity
- Organization Switching
- Multiple Membership Roles
- Federation
- SSO