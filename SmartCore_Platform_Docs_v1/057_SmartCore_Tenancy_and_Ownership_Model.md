# 057_SmartCore_Tenancy_and_Ownership_Model.md

Version: 1.4

Status: **Normative**

**Governance qualification**: Registration clarifications and the coordination
exception in §8 reflect ADR-0002 v1.4 (Proposed); Organization/Membership
lifecycle clarifications in §9 reflect ADR-0003 v1.2.1 (Proposed). These
synchronized descriptions do not approve either ADR or clear implementation.
The ADR acceptance criteria and 051/065 governance checks still apply.

------------------------------------------------------------------------

# 1. Purpose

This document defines the canonical ownership and tenancy model of the
SmartCore Platform.

Its purpose is to establish a single architectural boundary for
ownership, authorization, resource management, and future multi-tenant
capabilities.

This document does **not** define semantic constructs. Those remain
defined by the SmartCore Semantic Foundation Model (SFMM).

------------------------------------------------------------------------

# 2. Scope

This document defines:

-   Ownership boundaries
-   Tenancy boundaries
-   Membership model
-   Registration model
-   Responsibility assignment
-   Architectural constraints

This document does **not** define:

-   Semantic constructs
-   Rule Engine implementation
-   Policy Engine implementation
-   Authentication protocols
-   Runtime architecture
-   Platform taxonomy

------------------------------------------------------------------------

# 3. Architectural Principle

The SmartCore Platform adopts **Organization-Centric Ownership**.

Every managed resource belongs to an Organization.

Persons interact with resources through Memberships.

Ownership is therefore indirect.

The canonical relationship is:

``` text
Person
    │
Membership
    │
Organization
    │
Owns
    │
Resources
```

Direct ownership between a Person and a Resource is not part of the
SmartCore architecture.

------------------------------------------------------------------------

# 4. Core Definitions

## Person

A Person represents an identity capable of interacting with the
platform.

A Person owns:

-   Identity
-   Credentials
-   Personal profile
-   Personal preferences

A Person does not directly own platform resources.

------------------------------------------------------------------------

## Organization

An Organization represents the primary ownership boundary of the
platform.

An Organization may represent:

-   Individual
-   Family
-   Company
-   Factory
-   School
-   Hospital
-   Hotel
-   Farm
-   Government agency
-   Community
-   Any other managed entity

Every Organization acts as an independent tenant.

------------------------------------------------------------------------

## Membership

A Membership connects a Person to an Organization.

Membership is the only architectural path through which a Person
interacts with organizational resources.

Membership is independent from authentication.

------------------------------------------------------------------------

## Resource

A Resource represents any managed asset within SmartCore.

Examples include:

-   Devices
-   Buildings
-   Rooms
-   Parking spaces
-   Machines
-   Vehicles
-   Financial accounts
-   Inventories
-   Contracts
-   Digital assets

Every Resource belongs to exactly one Organization.

------------------------------------------------------------------------

# 5. Ownership Model

The following principles are normative.

## Principle 1

Every Person SHALL belong to at least one Organization.

------------------------------------------------------------------------

## Principle 2

Every Organization SHALL own its Resources.

------------------------------------------------------------------------

## Principle 3

Resources SHALL NOT be directly owned by Persons.

------------------------------------------------------------------------

## Principle 4

Ownership SHALL remain independent from authentication.

------------------------------------------------------------------------

## Principle 5

Ownership SHALL remain independent from implementation technology.

------------------------------------------------------------------------

# 6. Membership Model

Membership is the canonical mechanism that grants participation within
an Organization.

Membership attributes may include:

-   Role
-   Responsibility
-   Permissions
-   Effective period
-   Status

This platform-level participation relationship is realized by Membership.
For the Identity MVP described in ADR-0002 Decision 3 and ADR-0003 §2
(both Proposed), the initial Membership also has Role = Owner and
Status = Active. Role is a Membership attribute; this clarification does not
introduce a Role Aggregate or capability-specific permission rules.

The interpretation of roles and permissions is defined by higher
platform layers.

------------------------------------------------------------------------

# 7. Authorization Boundary

Authorization SHALL always be evaluated through Membership.

The canonical evaluation path is:

``` text
Person
      ↓
Membership
      ↓
Organization
      ↓
Resource
```

Authorization SHALL NOT be evaluated directly between a Person and a
Resource.

Permission evaluation is defined by the Security Model and Rule Model.

------------------------------------------------------------------------

# 8. Registration Model

Platform registration follows the ownership registration flow defined
below.

A successful registration SHALL establish ownership consistency by
completing:

1.  Create Person
2.  Create Personal Organization
3.  Create Owner Membership
4.  Commit ownership transaction

Partial ownership registration states are prohibited.

The platform SHALL NOT allow a Person to exist without belonging to at
least one Organization.

## Registration Core Transaction

The atomic ownership transaction SHALL include:

-   Person creation
-   Organization creation
-   Membership creation

The transaction SHALL commit after these ownership entities are
successfully created.

Additional Identity Platform operations MAY occur after successful
commit, including:

-   Credential creation
-   Initial session creation
-   Domain event publication

These operations SHALL NOT invalidate ownership consistency.

Under ADR-0002 v1.4 Decision 8 (Proposed), the durable registration workflow
starts PendingCredential. The initial Outbox provisioning work item and workflow
record commit with the Person/Organization/Membership triple, while Credential
creation remains after commit. This internal workflow state does not change the
Active Organization/Membership states or the ownership invariant. Password
login requires both an active Credential and a Ready registration workflow.
Provisioning retries and secure user completion may make the workflow Ready;
retry exhaustion preserves the ownership triple. See 059 §6 for the full
proposed flow and its PersonRegistered timing.

## Command Model Coordination Exception

The Registration Core Transaction coordinates creation of three distinct Aggregates (Person, Organization, Membership) within a single atomic consistency boundary.

This is a proposed, narrowly-scoped exception to the default cross-Aggregate coordination rule defined in 027_SmartCore_Command_Model.md, under which a Command SHALL target exactly one Aggregate and cross-Aggregate work SHALL be coordinated through Events.

This exception:

-   Applies ONLY to the RegisterPerson operation.
-   Is proposed by ADR-0002_Identity_Foundation_Clarifications.md v1.4, Decision 7 (Command Model Coordination Exception for Identity Registration), pending acceptance.
-   SHALL NOT be interpreted as a general precedent for multi-Aggregate transactional Commands elsewhere in the platform.
-   Does NOT redefine or supersede 027_SmartCore_Command_Model.md, which SHALL continue to govern all other Commands.

------------------------------------------------------------------------

# 9. Personal Organization

A Personal Organization is a standard Organization.

It is **not** a distinct semantic construct.

Its only distinguishing characteristic is its purpose.

Typical Organization categories include:

-   Personal
-   Family
-   Business
-   Factory
-   School
-   Hospital
-   Hotel
-   Government
-   Community

Additional categories may be introduced without changing this
architecture.

## Organization Lifecycle

The full lifecycle described by ADR-0003 v1.2.1 §1 (Proposed) has
Created, Active, Suspended, and Archived states. Its complete transition set is:

| From | To |
| --- | --- |
| Created | Active |
| Active | Suspended |
| Suspended | Active |
| Suspended | Archived |

No transition returns to Created. Archived is terminal. Active and Suspended
form a reversible pair. These rules describe the proposed full lifecycle,
including future operations; they do not make transition commands part of MVP.

In the Identity MVP, Organizations are created directly in Active state.
Organization suspension, resumption, and archival commands remain future scope.
A suspended Organization retains its resources; its Memberships remain active
but non-functional, as described by ADR-0003 §1.

## Membership Lifecycle

The full lifecycle described by ADR-0003 v1.2.1 §2 (Proposed) is:

    Created → Active → Revoked

Revoked is terminal. In the Identity MVP, initial Owner Memberships are
created directly in Active state. Created is reserved for future invitation
workflows; invitation and revocation operations remain future scope. No
Organization or Membership lifecycle transition command is introduced in MVP.

------------------------------------------------------------------------

# 10. Architectural Consequences

This model provides a uniform ownership architecture for all SmartCore
platforms.

The same ownership principles apply to:

-   SmartCore Identity
-   SmartCore Business
-   SmartCore Finance
-   SmartCore IoT
-   SmartCore Manufacturing
-   SmartCore Resource
-   SmartCore Reservation
-   SmartCore Communication

No platform defines an alternative ownership model.

------------------------------------------------------------------------

# 11. Relationship to SFMM

This document builds upon the SmartCore Semantic Foundation Model.

It does not modify or extend the SFMM semantic language.

Instead, it defines a canonical architectural application of the
semantic model within the SmartCore Platform.

Semantic meaning remains governed by SFMM.

Ownership and tenancy remain governed by this document.

------------------------------------------------------------------------

# 12. Governance

Changes to this ownership model require an Architecture Decision Record
(ADR).

Breaking changes affecting ownership boundaries are prohibited within
Version 1.x.

Future enhancements may introduce:

-   Multiple memberships
-   Cross-organization collaboration
-   Delegated administration
-   Organization federation
-   Hierarchical organizations

Such enhancements SHALL preserve the architectural principles defined in
this document.

------------------------------------------------------------------------

# References

-   027_SmartCore_Command_Model.md (see §8 Command Model Coordination
    Exception)
-   ADR-0002_Identity_Foundation_Clarifications.md
-   ADR-0003_Organization_and_Membership_Lifecycle_Standardization.md

------------------------------------------------------------------------

# Change Log

## Version 1.4 (2026-09-24)

- Propagated ADR-0002 v1.4 Decision 8 as Proposed: durable PendingCredential workflow and Outbox work commit alongside the ownership triple; Credential creation and recovery occur after commit.
- Preserved the atomic three-Aggregate ownership invariant and direct Active Organization/Membership creation.
- Did not accept ADR-0002 or introduce logical ownership cancellation.

## Version 1.3.1 (2026-09-24)

- Qualified registration/lifecycle references as pending ADR acceptance.
- Synchronized the already-proposed Owner/Active defaults and full lifecycle transition rules with ADR-0002/0003 v1.2.1.
- Distinguished future lifecycle transitions from direct Active initialization in MVP.
- Preserved ownership invariants, the registration transaction boundary, and future-scope operations.
- Historical authorization wording below records earlier documentation revisions and does not establish approval of the Proposed ADRs.

## Version 1.3 (2026-07-12)

**Decisions Implemented:** - Command Model Coordination Exception
reference: documents that the Registration Core Transaction is a
narrowly-scoped, approved exception to the default single-Aggregate
Command rule in 027_SmartCore_Command_Model.md, applicable only to
RegisterPerson.

**Authorizing Decision Records:** -
ADR-0002_Identity_Foundation_Clarifications.md, Decision 7

**Changes:** - Added "Command Model Coordination Exception" subsection
under §8 Registration Model - Added 027_SmartCore_Command_Model.md to
References

------------------------------------------------------------------------

## Version 1.2 (2026-07-08)

**Decisions Implemented:** - Organization Lifecycle standardization:
Created → Active → Suspended → Archived - Membership Lifecycle
standardization: Created → Active → Revoked

**Authorizing Decision Records:** -
ADR-0003_Organization_and_Membership_Lifecycle_Standardization.md

**Changes:** - Added Organization Lifecycle specification section -
Added Membership Lifecycle specification section - Added lifecycle state
transition definitions

------------------------------------------------------------------------

## Version 1.1 (2026-07-08)

**Decisions Implemented:** - Registration Boundary Clarification: Core
transaction vs. post-commit operations - Person-centric Identity
Platform boundary established

**Authorizing Decision Records:** -
ADR-0002_Identity_Foundation_Clarifications.md

**Changes:** - Added Registration Core Transaction section detailing
atomic transaction boundaries - Clarified transaction commit
requirements and consistency guarantees - Added explicit example of
post-commit operation non-invalidation policy

------------------------------------------------------------------------

## Version 1.0 (2026-06-01)

-   Initial release
-   Established Organization-Centric Ownership model
-   Defined core ownership boundaries and tenancy model

------------------------------------------------------------------------

# 13. Final Statement

The SmartCore Platform adopts Organization-Centric Ownership as its
canonical ownership model.

Every Person participates through Membership.

Every Resource belongs to an Organization.

Every platform built upon SmartCore SHALL follow this ownership model
unless superseded by a formally accepted Architecture Decision Record.

------------------------------------------------------------------------

**END OF DOCUMENT**

