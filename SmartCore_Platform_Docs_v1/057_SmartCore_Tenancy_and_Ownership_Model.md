# 057_SmartCore_Tenancy_and_Ownership_Model.md

Version: 1.2

Status: **Normative**

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

A Membership may later include:

-   Role
-   Responsibility
-   Permissions
-   Effective period
-   Status

Version 1.0 requires only the existence of Membership.

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

Organizations SHALL follow this lifecycle unless superseded by a future
ADR:

    Created → Active → Suspended → Archived

## Membership Lifecycle

Memberships SHALL follow this lifecycle unless superseded by a future
ADR:

    Created → Active → Revoked

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

# Change Log

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
