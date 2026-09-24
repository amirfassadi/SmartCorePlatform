# ADR-0002: Identity Foundation Clarifications

## Metadata

* **ADR Number**: ADR-0002
* **Title**: Identity Foundation Clarifications
* **Status**: Proposed
* **Version**: 1.2.1
* **Date Created**: 2026-07-08
* **Author**: SmartCore Architecture Team
* **Approval Date**: TBD
* **Effective Date**: TBD
* **Decision Type**: Architectural Decision
* **Decision Level**: Level 4 — Architectural Change (applies to Decision 7; Decisions 1–6 are Level 2 Documentation clarifications)

## Review Revision — 2026-09-24

This revision is a documentation correction candidate. Status remains Proposed;
Approval Date and Effective Date remain TBD. Decision requirements describe the
proposed architecture and do not constitute approval or implementation clearance.
Acceptance remains subject to the criteria below and Document 051.

---

# Decision Scope

1. Registration Boundary Clarification
2. Authorization Boundary Clarification
3. Membership Role Model Clarification
4. Identity Platform Person-Centric Boundary
5. Event Ownership Documentation
6. Future Identity Types Documentation
7. Command Model Coordination Exception for Identity Registration

---

# Context

The SmartCore Identity Platform requires architectural clarification before Version 1.0 freeze to ensure consistency, governance alignment, and future extensibility.

This ADR defines foundational decisions related to:

* Identity registration boundaries
* Authorization responsibility separation
* Membership role modeling
* Person-centric Identity boundaries
* Event ownership
* Future identity extensions
* Command coordination rules for initial Identity registration

The SmartCore Command Model defines a general rule that Commands operate within a single Aggregate boundary and that cross-aggregate coordination should normally be achieved through domain events.

Identity Registration requires an explicit architectural exception to this general rule.

The initial Identity ownership boundary consists of:

* Person
* Personal Organization
* Membership

These entities represent a single business invariant.

A Person without ownership context is considered an invalid Identity state.

Therefore, initial registration requires strong consistency and atomic creation.

---

# Decision

## 1. Registration Boundary Clarification

### Decision

Registration is an atomic operation that creates the initial Identity ownership boundary.

### Rationale

Identity ownership must exist as a complete and consistent state after successful registration.

### Statement

The RegisterPerson operation SHALL create:

* Person
* Personal Organization
* Membership with Owner role

within a single atomic transaction boundary.

Partial registration states are prohibited.

Post-registration operations MAY include:

* Credential creation
* Session creation
* Event publication

These operations SHALL NOT invalidate ownership consistency.

---

## 2. Authorization Boundary Clarification

### Decision

Identity Platform authentication and business authorization responsibilities SHALL remain separated.

### Statement

Identity Platform SHALL provide:

* Authentication results
* Identity context
* Membership context
* Organization context

Identity Platform SHALL NOT implement Capability-specific business authorization rules.

Business authorization SHALL remain the responsibility of consuming Capability Platforms.

---

## 3. Membership Role Model Clarification

### Decision

Role SHALL remain an attribute of Membership.

### Statement

Version 1.0 SHALL support:

* Owner

Future roles MAY be introduced without creating a separate Role Aggregate.

---

## 4. Identity Platform Person-Centric Boundary

### Decision

Identity Platform SHALL remain Person-centric during Version 1.x.

### Statement

Future identity types such as:

* Device Identity
* Service Identity
* AI Agent Identity

MAY be introduced through future architectural decisions.

They SHALL NOT modify existing Person identity semantics.

---

## 5. Event Ownership Documentation

### Decision

Identity Platform SHALL explicitly own and publish Identity-related domain events.

### Event Ownership

| Event               | Owner    | MVP |
| ------------------- | -------- | --- |
| PersonRegistered    | Identity | Yes |
| PersonUpdated       | Identity | Yes |
| PasswordChanged     | Identity | Yes |
| LoginSucceeded      | Identity | Yes |
| LoginFailed         | Identity | Yes |
| SessionCreated      | Identity | Yes |
| SessionExpired      | Identity | Yes |
| LogoutCompleted     | Identity | Yes |
| OrganizationCreated | Identity | Yes |
| MembershipCreated   | Identity | Yes |

Events represent completed business facts.

Events SHALL NOT be used to coordinate initial ownership creation.

Security and audit classification of events is outside the scope of this ADR.

---

## 6. Future Identity Types Documentation

### Decision

Future Identity types SHALL be introduced through explicit architectural decisions.

### Statement

The following are considered future extensions:

* Device Identity
* Service Identity
* AI Agent Identity

These SHALL extend Identity capabilities without changing Person identity semantics.

---

## 7. Command Model Coordination Exception for Identity Registration

### Decision

This ADR proposes a narrowly scoped exception for Identity Registration to the default cross-aggregate coordination model defined in:

`027_SmartCore_Command_Model.md`

The RegisterPerson operation MAY coordinate creation of multiple Identity Aggregates within a single atomic consistency boundary.

This permission is what Decision 1 of this ADR already requires in practice: Decision 1 mandates atomic creation of Person, Personal Organization, and Membership. Decision 7 exists solely to formally except that mandated behavior from the default cross-aggregate coordination rule in 027, not to introduce a new requirement.

This exception applies ONLY to initial Identity ownership creation.

It SHALL NOT redefine the general SmartCore Command Model.

All other Commands SHALL follow standard cross-aggregate coordination rules.

---

### Rationale

Initial Identity registration requires strong consistency.

The following entities must exist together:

* Person
* Personal Organization
* Membership

Using an event-driven Saga approach would allow temporary invalid states.

Examples:

* Person exists without ownership
* Organization exists without Membership
* Membership exists without valid Person relationship

These states violate Identity ownership invariants.

---

### Alternatives Considered

#### Alternative 1 — Event-driven Saga Registration

Rejected.

Reasons:

* Allows partial ownership states.
* Requires compensation workflows.
* Introduces unnecessary complexity.
* Violates registration invariants.

---

#### Alternative 2 — Separate Registration Commands

Rejected.

Reasons:

* Allows invalid sequencing.
* Weakens Identity ownership guarantees.

---

#### Alternative 3 — Single Large Registration Aggregate

Rejected.

Reasons:

* Creates excessive Aggregate responsibility.
* Violates established Identity Aggregate boundaries.

---

## 7.1 Registration Orchestration Responsibility

The orchestration component responsible for RegisterPerson SHALL be classified as an Application Service according to:

`064_SmartCore_Blueprint_Standard.md`

It SHALL NOT be modeled as a Domain Service.

The responsibility is application-level orchestration of multiple Aggregate operations.

Dependent documents SHALL update terminology accordingly:

```
RegistrationDomainService
        ↓
RegistrationApplicationService
```

(or an equivalent name aligned with implementation standards)

---

# Consequences

## Positive Consequences

* Guarantees valid Identity ownership after registration.
* Prevents partial ownership states.
* Maintains Identity invariants.
* Preserves general Command Model rules while documenting a controlled exception.

---

## Negative Consequences

* Registration requires coordinated transaction handling.
* Similar exceptions cannot be introduced without governance review.
* Additional validation is required when modifying Identity lifecycle flows.

---

## Backward Compatibility

All changes introduced by this ADR, including the Command Model Coordination Exception in Section 7, are additive and clarifying.

No breaking changes are introduced to the existing Person identity model.

The Command Model Coordination Exception does not alter the behavior of any previously implemented Command. It documents and formalizes the pre-existing RegisterPerson design.

---

## Future Decisions

This ADR establishes the foundation for:

* Future identity type extensions (Device, Service, AI Agent)
* Role extension mechanisms
* Event extension patterns
* Any future request for a similar cross-aggregate atomic coordination exception, which SHALL require its own independent architectural review and SHALL NOT cite this ADR as a general precedent

---

# Scope Limitation

This exception applies ONLY to:

```
RegisterPerson
```

It SHALL NOT be interpreted as permission for general multi-Aggregate transactional Commands.

Future exceptions require separate architectural review.

---

# Document Updates Required

The following is the reviewed baseline from the supplied Platform and Identity
packages, not a claim that acceptance conditions have passed. Further revisions
must follow 051 §9; versions must not be reduced to historical targets.

| Document | Observed baseline | Required work / verification |
| --- | --- | --- |
| 027_SmartCore_Command_Model.md | 1.2 | §17.1 already records the exception; qualify its pending approval and verify the exact RegisterPerson-only scope. |
| 057_SmartCore_Tenancy_and_Ownership_Model.md | 1.3 | §8 already records the exception; qualify pending approval and verify the core ownership boundary. |
| 059_SmartCore_Identity_Platform.md | 1.1 | §6 already separates ownership commit from Credential/Session operations; synchronize approval wording, lifecycle references, and revision history. |
| 01_Domain_Model.md | Header 1.1.0; Change Log includes 1.2.0 | Application Service reclassification already exists; reconcile version metadata and pending-approval wording. |
| 03_Aggregates.md | 1.1.1 | Atomic registration exception already exists; verify consistency and qualify pending approval. |
| 04_Commands.md | 1.1.0 | Application Service mapping already exists; verify consistency and qualify pending approval. |

Also verify dependent references and readiness labels in 02_Use_Cases.md,
14_MVP.md, and the machine specification. The supplied machine file is named
`capability_machine.yaml`; 064 §7 requires `capability.machine.yaml`.
Its governance block already requires acceptance of ADR-0002 and ADR-0003.
These package corrections are prerequisites for a new validation result, not
proof that Structural Validation has passed.

---

# Acceptance Criteria

This ADR SHALL remain Proposed until:

* [ ] Related document updates are completed
* [ ] Architecture Validation Review is completed
* [ ] Blueprint passes Structural Validation
* [ ] All affected Blueprint documents reference ADR-0002 (latest accepted version)

After approval:

* Status SHALL change to Accepted
* Approval Date SHALL be recorded
* Effective Date SHALL be recorded

---

# References

> *Document 019 is retained as a referenced architectural context
> document for the identity/session-continuity concepts underlying this
> ADR. Its long-term
> lineage status (relative to 041 and 059) remains subject to future
> Architecture Board review under a separate governance track, and this
> reference does not constitute a supersession determination.*

* 019_SmartCore_Identity_and_Session_Continuity_Model.md
* 027_SmartCore_Command_Model.md
* 041_SmartCore_Identity_Model.md
* 051_SmartCore_Governance_and_Decision_Model.md
* 057_SmartCore_Tenancy_and_Ownership_Model.md
* 059_SmartCore_Identity_Platform.md
* 064_SmartCore_Blueprint_Standard.md
* 065_SmartCore_Blueprint_Validator_Specification.md
* 066_SmartCore_AI_Code_Generation_Specification.md
* ADR-0003_Organization_and_Membership_Lifecycle_Standardization.md

---

# Change History

| Version | Status   | Description                                                                                                                                         |
| ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | Proposed | Initial Identity Foundation Clarifications                                                                                                          |
| 1.1     | Proposed | Added Command Model coordination exception for Identity Registration, clarified Application Service responsibility, added governance metadata, and documented compatibility boundaries. Clarified that the exception applies only to RegisterPerson and does not establish a general multi-Aggregate transaction rule. |
| 1.2     | Proposed | Added a clarifying note to the References section stating that Document 019 is retained as an architectural context document for this ADR without constituting a lineage/supersession determination relative to 041/059; that determination is deferred to a separate Architecture Board governance track. Corrected a stale version-pinned self-reference in Acceptance Criteria (ADR-0002 v1.1 → latest accepted version). No substantive decision content changed. |
| 1.2.1 | Proposed | 2026-09-24 review candidate: clarified pending approval, replaced stale document-update assumptions with observed package baselines, and recorded dependent validation work. No transaction boundary, role, event, authentication, or MVP behavior changed. |

---

**END OF DOCUMENT**