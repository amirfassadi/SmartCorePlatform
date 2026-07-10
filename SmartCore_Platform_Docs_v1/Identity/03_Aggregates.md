<!--
Document ID: ID-03
Title: SmartCore Identity Platform Blueprint - Aggregates
Version: 1.0.0
Status: READY_FOR_GENERATION
Purpose: Define aggregate design rationale and boundaries for the Identity Platform Blueprint
Dependencies: 01_Domain_Model.md, 064_SmartCore_Blueprint_Standard
Change Log:
  - Version 1.0.0 (2026-07-08): Initial aggregate design rationale for Session and Credential
-->

# 1. Aggregate Overview

The Identity Domain consists of five Aggregates:

- Person
- Organization
- Membership
- Session
- Credential

Each Aggregate owns an independent lifecycle and consistency boundary.

---

# 2. Person Aggregate

**Aggregate Root**: Person

**Root Entity Responsibilities**:
- Owns identity
- Manages profile attributes (Email, DisplayName)
- Tracks lifecycle status

**Child Entities**: None in MVP

**Child Value Objects**: EmailAddress

**Independent Lifecycle**:
- Registered → Active → Suspended → Archived
- Person identity persists across Session and Credential changes

---

# 3. Organization Aggregate

**Aggregate Root**: Organization

**Root Entity Responsibilities**:
- Owns organizational boundary
- Manages resource ownership
- Tracks lifecycle status

**Child Entities**: None in MVP

**Child Value Objects**: None

**Independent Lifecycle**:
- Created → Active → Suspended → Archived
- Future versions will implement suspend/resume/archive operations

Lifecycle diagrams represent MVP-visible lifecycle flow.

Full lifecycle transition rules, including reversible transitions such as Suspended → Active, are defined in ADR-0003.

No lifecycle transition commands are part of MVP.

---

# 4. Membership Aggregate

**Aggregate Root**: Membership

**Root Entity Responsibilities**:
- Connects Person to Organization
- Stores role and status
- Manages participation lifecycle

**Child Entities**: None in MVP

**Child Value Objects**: Role

**Independent Lifecycle**:
- Created → Active → Revoked
- Future versions will support multiple roles and delegated management

---

# 5. Session Aggregate

**Aggregate Root**: Session

**Root Entity Responsibilities**:
- Owns authenticated context
- Manages token lifecycle
- Tracks device and IP information

**Child Entities**: None in MVP

**Child Value Objects**: AccessTokenId, RefreshToken

**Independent Lifecycle**:
- Created → Authenticated → Active → Suspended (optional) → Expired → Closed
- Sessions are temporary; they have no effect on Person identity or Membership status

---

# 6. Credential Aggregate

**Aggregate Root**: Credential

**Root Entity Responsibilities**:
- Owns authentication material
- Manages credential lifecycle
- Handles password changes

**Child Entities**: None in MVP

**Child Value Objects**: PasswordHash

**Independent Lifecycle**:
- Created → Active → Replaced → Revoked
- Credential changes do not affect Person identity
- Version 1.x supports exactly one active Credential per Person

---

# 7. Session Aggregate Rationale

Session is modeled as an independent Aggregate because:

- It owns an independent lifecycle (Created → Authenticated → Active → Suspended (optional) → Expired → Closed)
- It may be revoked independently without affecting Person identity
- Multiple sessions may exist for a single Person simultaneously
- Session consistency is independent from Person consistency
- Session expiration SHALL NOT affect Person identity or Membership status
- Sessions represent temporary execution context, distinct from identity ownership

**Design Consequence**: Session changes do not cascade to Person. Person changes do not invalidate Sessions. Each maintains independent state.

---

# 8. Credential Aggregate Rationale

Credential is modeled as an independent Aggregate because:

- Credential lifecycle differs from Person lifecycle (Created → Active → Replaced → Revoked)
- Credential replacement is independent from Person profile updates
- Future authentication mechanisms may coexist with existing Credentials
- Credential consistency is independent from Person consistency
- Credential history and rotation do not affect Person identity
- Multiple credentials may be managed through future extensibility

**Design Note**: Version 1.x SHALL support exactly one active Credential per Person. Credential History is future scope.

**Design Consequence**: Credential changes represent authentication mechanism evolution, not identity change. Person identity remains stable across credential rotations.

---

# 9. Aggregate Consistency Boundaries

Each Aggregate maintains:

- **Consistency Boundary**: Internal state is consistent without external coordination
- **Root Entity**: Single aggregate root entity owns all internal entities
- **Transaction Scope**: All changes to an aggregate occur within a single transaction
- **Cross-Aggregate Consistency**: Maintained by Domain Services, not aggregates

---

# 10. Future Persistence Considerations

Persistence layer design (Repository patterns, storage strategies, consistency mechanisms) will be defined in blueprint document 09_Persistence.md.

Each Aggregate Root will have exactly one owning Repository, to be specified in the Persistence blueprint.

This document establishes Aggregate boundaries; persistence implementation is deferred to the dedicated Persistence document.

---

# 11. Future Aggregate Considerations

Future versions MAY introduce:

- Device Identity as separate Aggregate
- Service Identity as separate Aggregate
- AI Agent Identity as separate Aggregate
- Organization Hierarchy as separate Aggregate
- Delegation as separate Aggregate
- Audit Log as separate Aggregate

Each future Aggregate MUST articulate its independent lifecycle and consistency boundary per this pattern.

---

**END OF DOCUMENT**
