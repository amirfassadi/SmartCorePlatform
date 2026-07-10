<!--
Document ID: ID-14
Title: SmartCore Identity Platform Blueprint - MVP Scope
Version: 1.0.0
Status: READY_FOR_GENERATION
Purpose: Define MVP scope and explicitly exclude future lifecycle operations from Version 1.0
Dependencies: 01_Domain_Model.md, 03_Aggregates.md, 14_MVP.md, 064_SmartCore_Blueprint_Standard
Change Log:
  - Version 1.0.0 (2026-07-08): Initial MVP scope clarification, explicit exclusion of Suspend/Archive/Revoke operations
-->

# 1. MVP Scope Definition

The Identity Platform Version 1.0 supports the following operations:

**Person Management**
- Register Person
- Update Person Profile
- Retrieve Person Information

**Authentication**
- Login (create session)
- Logout (close session)
- Refresh Session

**Organization Management**
- Create Personal Organization (automatic during registration)
- Retrieve Organization Information

**Membership Management**
- Create Membership (automatic during registration)
- Retrieve Membership Information

**Session Management**
- Create Session
- Refresh Token
- Close Session

**Credential Management**
- Create Credential (during registration)
- Change Password

---

# 2. Future Lifecycle Operations

The following operations are NOT part of MVP:

- SuspendOrganization
- ResumeOrganization
- ArchiveOrganization
- RevokeMembership
- RevokePerson
- RestoreArchivedOrganization

**Rationale**: Lifecycle states (Suspended, Archived, Revoked) exist in the domain model for architectural completeness and future evolution. Version 1.0 does not implement the Commands, Use Cases, or APIs required to transition through these states.

---

# 3. Lifecycle State Constraints for MVP

**Organization Lifecycle in MVP**:

- Organizations created in Active state
- No transitions to Suspended, Archived, or other states
- Active state is operational for entire Version 1.0 lifecycle

**Membership Lifecycle in MVP**:

- Memberships created in Active state
- No transitions to Revoked or other states
- Active state is operational for entire Version 1.0 lifecycle

**Session Lifecycle in MVP**:

- All transitions (Created → Authenticated → Active → Expired → Closed) are implemented
- Optional Suspended state is supported but not required
- Session expiration is implemented

**Person Lifecycle in MVP**:

- Persons created in Active state
- No transitions to Suspended, Archived, or other states
- Active state is operational for entire Version 1.0 lifecycle

**Credential Lifecycle in MVP**:

- Credentials created in Active state
- Password change creates new Active credential (no history)
- No Credential History tracking in Version 1.0

---

# 4. No Unreachable States

Every lifecycle state in the Identity Domain Model is either:

1. **Reachable via MVP Command/Use Case**: Directly transitioned to through implemented operations
   - Examples: Session → Expired (via Session Expiration), Session → Closed (via Logout)

2. **Explicitly Marked Future Scope**: Documented as excluded from Version 1.0
   - Examples: Organization → Suspended (future), Membership → Revoked (future)

**No orphaned or unclassified states exist.**

---

# 5. Event Ownership Alignment

All events published in MVP are declared in 059_SmartCore_Identity_Platform.md Event Ownership Table:

MVP Events:
- PersonRegistered
- PersonUpdated
- PasswordChanged
- LoginSucceeded
- LoginFailed
- SessionCreated
- SessionExpired
- LogoutCompleted
- OrganizationCreated
- MembershipCreated

Future events (SuspendOrganizationRequested, RevokeMembershipCompleted, etc.) are explicitly scoped as future.

---

# 6. Domain Service Scope for MVP

Implemented Domain Services in MVP:

1. **RegistrationDomainService**: Atomic registration coordination
2. **AuthenticationDomainService**: Credential validation and session creation
3. **SessionManagementDomainService**: Session refresh, expiration, and closure
4. **PersonManagementDomainService**: Person profile updates
5. **CredentialManagementDomainService**: Password changes

Future Domain Services (deferred to future versions):

- OrganizationManagementDomainService (suspend, archive, restore)
- MembershipManagementDomainService (revoke, reinstate, role change)
- DelegationDomainService
- AuditingDomainService

---

# 7. API Scope for MVP

Public REST APIs implemented in MVP:

```
POST   /auth/register         - User registration
POST   /auth/login            - User login (create session)
POST   /auth/logout           - User logout (close session)
POST   /auth/refresh          - Refresh access token
GET    /me                    - Get current user (Person) info
GET    /organizations         - List user's organizations
GET    /sessions              - List active sessions
POST   /me/password           - Change password
GET    /me/memberships        - List user's memberships
```

Future APIs (deferred):

- Suspend / Resume / Archive Organization
- Revoke / Reinstate Membership
- Role management and assignment
- Delegated administration

---

# 8. MVP Readiness Checklist

Identity Platform Version 1.0 is complete when:

✓ User registration succeeds (atomic Person + Organization + Membership creation)
✓ Login succeeds (Session creation, token issuance)
✓ Logout succeeds (Session closure)
✓ Refresh token works (Session refresh)
✓ Personal Organization is created automatically
✓ Owner Membership is created automatically
✓ Session management functions correctly
✓ Password change is implemented
✓ Identity events are published per Event Ownership Table
✓ REST APIs are operational per API Scope
✓ All MVP Domain Services are implemented
✓ No unreachable states exist
✓ All lifecycle states are classified (MVP or Future)
✓ Blueprint passes Structural Validation per 065_SmartCore_Blueprint_Validator_Specification
✓ Blueprint remains compatible with 066_SmartCore_AI_Code_Generation_Specification

---

**END OF DOCUMENT**
