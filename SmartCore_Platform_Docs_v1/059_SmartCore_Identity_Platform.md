# 059_SmartCore_Identity_Platform.md

Version: 1.1.1

Status: **Normative**

Related Decision Records:

- ADR-0002_Identity_Foundation_Clarifications.md (v1.2.1, Proposed)
- ADR-0003_Organization_and_Membership_Lifecycle_Standardization.md (v1.2.1, Proposed)

**Governance qualification**: The related registration, role, authorization,
event-ownership, and lifecycle descriptions reflect these pending proposals.
Synchronizing this document does not accept either ADR or clear code generation.
Acceptance remains subject to the ADR criteria and Documents 051/065.

---

# 1. Purpose

This document defines the first executable platform of SmartCore.

The Identity Platform establishes the foundational services required by every other SmartCore Platform.

It provides identity, authentication, organization ownership, membership management, and session management.

All subsequent platforms SHALL depend on this platform.

---

# 2. Objectives

The Identity Platform SHALL provide:

* Person identity management
* Authentication
* Session management
* Personal Organization creation
* Membership management
* Foundation for Authorization Context
* Identity APIs
* Identity events

It SHALL remain independent of IoT, Finance, Manufacturing, or any other business domain.

---

# 3. Responsibilities

The Identity Platform is responsible for:

* Registering Persons
* Authenticating users
* Maintaining active sessions
* Creating Personal Organizations
* Creating Owner Memberships
* Managing identity lifecycle
* Publishing identity-related events

The Identity Platform SHALL NOT contain business-specific logic.

---

# 4. Core Domain Objects

The Identity Platform consists of the following primary domain objects.

## Person

Represents a human identity.

Examples:

* Customer
* Employee
* Administrator

---

## Organization

Represents the ownership boundary of SmartCore.

Every resource belongs to exactly one Organization.

Every newly registered Person automatically receives one Personal Organization.

---

## Membership

Represents participation of a Person inside an Organization.

Version 1.0 supports only:

* Owner

Future versions may introduce:

* Admin
* Member
* Guest
* Operator

---

## Session

Represents an authenticated login session.

Sessions are temporary.

Identity is permanent.

---

## Credential

Represents authentication information.

Supported:

* Password

Future:

* OAuth
* Google
* Apple
* Telegram
* Enterprise SSO

---

# 5. Domain Relationships

```text
Person
    │
    │ owns
    ▼
Personal Organization

Person
    │
    │ member of
    ▼
Membership
    │
    ▼
Organization

Organization
    │
    │ owns
    ▼
Resources
```

Resources are never owned directly by Persons.

Ownership always flows through Organizations.

---

# 6. Registration Process

Registration SHALL be executed through coordinated transaction phases.

Under the proposal in ADR-0002 Decisions 1, 7, and 7.1,
RegistrationApplicationService coordinates the Person, Personal Organization,
and Owner Membership creation within the core ownership transaction. It is an
Application Service. The proposed exception applies only to RegisterPerson;
027 §17 continues to define the general Command rule. Credential and Session
creation remain post-commit operations as described below.

## Core Ownership Transaction

The atomic ownership transaction SHALL be committed before post-commit operations:

```text
Register Request

↓

Create Person

↓

Create Personal Organization

↓

Create Owner Membership

↓

[COMMIT]
```

This core transaction creates the foundational ownership relationships.

**Commit Requirement**: All three ownership entities MUST be successfully persisted before proceeding.

**Rollback Policy**: If any step fails, the entire transaction rolls back. Partial ownership states are prohibited.

## Post-Commit Identity Operations

After successful commit, the following operations MAY occur:

```text
[Transaction Committed]

↓

Create Credential

↓

Create Initial Session

↓

Publish PersonRegistered Event

↓

Return Authentication Result
```

**Non-Invalidating Policy**: Post-commit operations SHALL NOT invalidate ownership consistency. If post-commit operations fail, the ownership relationships remain valid.

**Example**: If Session creation fails, the Person, Organization, and Membership are still valid for future login attempts.

**Consistency Guarantee**: Ownership is fully established after core transaction commit and survives independent of credential or session state.

---

## Organization and Membership Lifecycle Scope

This subsection synchronizes ADR-0003 v1.2.1 §§1–2 (Proposed) with registration.

| Aggregate | Initial state in Identity MVP | Future operations excluded from MVP |
| --- | --- | --- |
| Organization | Active | Staged initialization, suspend, resume, archive |
| Membership | Active, with Role = Owner | Invitation, activation from Created, revocation |

The full Organization transition set is Created → Active, Active → Suspended,
Suspended → Active, and Suspended → Archived. Archived is terminal; no
transition returns to Created. Organization suspension retains ownership;
Memberships remain active but non-functional while the Organization is suspended.

The full Membership transition set is Created → Active and Active → Revoked;
Revoked is terminal. These full lifecycles describe future operations as well as
MVP defaults. No Organization or Membership lifecycle transition Command, API,
or Use Case is added to Version 1.0 by this clarification.

---

# 7. Authentication Flow

```text
Login Request

↓

Validate Credential

↓

Create Session

↓

Issue Access Token

↓

Issue Refresh Token

↓

Return Authentication Response
```

No domain data is modified during login.

---

# 8. Session Model

Each authenticated device receives its own Session.

A Person may own multiple active Sessions.

Example:

* Web Browser
* Mobile App
* Telegram Bot
* Desktop Application

Sessions are independent.

---

# 9. Authorization Model (MVP)

Authorization is Organization-centric.

The only supported role is:

* Owner

Permission evaluation:

```text
Person

↓

Membership

↓

Organization

↓

Resource
```

Direct Person → Resource permissions are prohibited.

## Authorization Boundary

The Identity Platform SHALL provide:
- Identity context
- Authentication outcomes
- Membership information
- Organization information

The Identity Platform SHALL NOT evaluate business permissions.

Business authorization remains the responsibility of consuming Capability Platforms.

## Role Model

In Version 1.0:
Role SHALL be an attribute of Membership.

Supported value:
- Owner

Future versions MAY introduce additional role values without introducing a separate Role Aggregate.

## Event Ownership Table

| Event               | Owner Capability |
|---------------------|------------------|
| PersonRegistered    | Identity |
| PersonUpdated       | Identity |
| PasswordChanged     | Identity |
| LoginSucceeded      | Identity |
| LoginFailed         | Identity |
| SessionCreated      | Identity |
| SessionExpired      | Identity |
| LogoutCompleted     | Identity |
| OrganizationCreated | Identity |
| MembershipCreated   | Identity |

This hardening task SHALL NOT introduce additional lifecycle events.

Lifecycle events beyond those listed above are outside the scope of Identity Blueprint Version 1.0 and MAY be introduced through future ADRs.

## Future Identity Types

Future versions MAY introduce:
- Device Identity
- Service Identity
- AI Agent Identity

These identity types SHALL extend the platform without modifying Person identity semantics.

---

# 10. Identity Events

The platform SHALL publish domain events.

Events declared in Event Ownership Table §9:

* PersonRegistered
* PersonUpdated
* PasswordChanged
* LoginSucceeded
* LoginFailed
* SessionCreated
* SessionExpired
* LogoutCompleted
* OrganizationCreated
* MembershipCreated

Events SHALL be immutable.

**Consistency Note**: This list matches the Event Ownership Table exactly. Identity Platform owns and publishes all 10 events listed in the Event Ownership Table.

---

# 11. Public APIs

Minimum endpoints:

```text
POST   /auth/register

POST   /auth/login

POST   /auth/logout

POST   /auth/refresh

GET    /me

GET    /organizations

GET    /sessions
```

Future APIs may extend this list without breaking existing contracts.

---

# 12. Data Model

Minimum persistent entities:

* Persons
* Organizations
* Memberships
* Credentials
* Sessions

Supporting persistence structures may include:

* PasswordHistory
* LoginHistory
* RefreshTokens
* IdentityEvents
* AuditLogs

The schema SHALL be extensible without redesign.

---

# 13. Security Principles

Passwords SHALL never be stored in plain text.

Authentication SHALL use secure hashing algorithms.

Tokens SHALL be revocable.

Sessions SHALL support expiration.

Security policies SHALL be configurable.

---

# 14. Dependencies

The Identity Platform depends on:

* SFMM
* Reference Architecture
* Platform Taxonomy
* Foundation MVP

No dependency on:

* Finance
* IoT
* Manufacturing
* Reservation
* Messaging

---

# 15. Platforms Depending on Identity

The following platforms SHALL use the Identity Platform:

* SmartCore IoT
* SmartCore Finance
* SmartCore Manufacturing
* SmartCore Business
* SmartCore Resource
* SmartCore Reservation
* SmartCore Communication
* SmartCore Workflow

Identity SHALL be implemented only once and reused everywhere.

---

# 16. MVP Deliverables

The Identity Platform MVP is complete when:

✓ User registration succeeds.

✓ Login succeeds.

✓ Logout succeeds.

✓ Refresh token works.

✓ Personal Organization is created automatically.

✓ Membership is created automatically.

✓ Session management functions correctly.

✓ Identity events are published.

✓ REST APIs are operational.

---

# 17. Future Evolution

Future versions may introduce:

* Multi-factor Authentication (MFA)
* Social Login
* Enterprise SSO
* Multiple Organization Membership
* Delegated Administration
* Invitation System
* Organization Switching
* Advanced Authorization
* Policy Engine
* Rule Engine Integration

These enhancements SHALL extend the platform without changing its core responsibilities.

---

# 18. Final Statement

The Identity Platform is the foundational execution platform of SmartCore.

It establishes the identity, ownership, authentication, and organizational model upon which every other SmartCore Platform is built.

No business platform SHALL bypass or replace the Identity Platform.

---

# Change Log

## Version 1.1.1 (2026-09-24)

- Added explicit Proposed ADR references and governance qualification.
- Documented the existing RegistrationApplicationService mapping from ADR-0002 Decision 7.1 without changing transaction phases.
- Synchronized Owner/Active registration defaults, full lifecycle descriptions, and MVP exclusions with ADR-0003.
- Preserved the event catalog, event timing, APIs, and post-commit recovery policy.
- Earlier authorization wording below describes historical documentation edits; it does not establish acceptance of ADR-0002.

## Version 1.1 (2026-07-08)

- Added Authorization Boundary clarification: Identity Platform provides context, not permission evaluation
- Added Role Model specification: Role as Membership attribute, Version 1.0 supports Owner only
- Added Event Ownership Table with 10 core Identity Platform events
- Added Future Identity Types documentation: Device, Service, AI Agent as future extensions
- Changes authorized by ADR-0002_Identity_Foundation_Clarifications.md

## Version 1.0 (2026-06-01)

- Initial release
- Defined core Identity Platform responsibilities
- Established authentication and session management model

---

## Event Timing Note

PersonRegistered is published after Credential and initial Session creation to represent completed registration including initial authentication capability.

Ownership consistency is guaranteed independently by the Core Ownership Transaction.

Failure of post-commit operations SHALL NOT invalidate:
- Person
- Organization
- Membership

Post-commit recovery and operational handling are implementation-specific.

**END OF DOCUMENT**

