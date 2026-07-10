# ADR-0002: Identity Foundation Clarifications

## Metadata

- **ADR Number**: ADR-0002
- **Title**: Identity Foundation Clarifications
- **Status**: Proposed
- **Date Created**: 2026-07-08
- **Version**: 1.0

## Decision Scope

1. Registration Boundary Clarification
2. Authorization Boundary Clarification
3. Membership Role Model Clarification
4. Identity Platform Person-Centric Boundary
5. Event Ownership Documentation
6. Future Identity Types Documentation

## Context

The Identity Platform requires architectural clarifications before Version 1.0 freeze to ensure consistency, clarity, and extensibility for future SmartCore Capability Platforms.

This ADR addresses ambiguities in:
- Registration atomicity and boundary
- Authorization responsibilities and separation of concerns
- Membership role structure and future evolution
- Event ownership and lifecycle management
- Support for future identity types while maintaining backward compatibility

## Decision

### 1. Registration Boundary Clarification

**Decision**: Registration is an atomic operation that creates three core ownership entities.

**Rationale**: Atomic registration ensures that no Person can exist outside organizational ownership context.

**Statement**: The atomic registration transaction SHALL include:
- Person creation
- Organization creation (Personal Organization)
- Membership creation (Owner role)

The transaction SHALL commit after these ownership entities are successfully created.

Additional Identity Platform operations MAY occur after successful commit, including:
- Credential creation
- Initial session creation
- Domain event publication

These operations SHALL NOT invalidate ownership consistency.

### 2. Authorization Boundary Clarification

**Decision**: The Identity Platform provides authentication and membership context, not business authorization.

**Rationale**: Separation of concerns allows each Capability Platform to implement domain-specific authorization rules.

**Statement**: The Identity Platform SHALL provide:
- Identity context
- Authentication outcomes
- Membership information
- Organization information

The Identity Platform SHALL NOT evaluate business permissions.

Business authorization remains the responsibility of consuming Capability Platforms.

### 3. Membership Role Model Clarification

**Decision**: In Version 1.0, Role is an attribute of Membership, supporting only the "Owner" value.

**Rationale**: Simple role structure enables MVP while maintaining extensibility.

**Statement**: Role SHALL be an attribute of Membership.

Supported value in Version 1.0:
- Owner

Future versions MAY introduce additional role values (Admin, Member, Guest, Operator) without introducing a separate Role Aggregate.

### 4. Identity Platform Person-Centric Boundary

**Decision**: Identity Platform remains Person-centric in Version 1.x.

**Rationale**: Human identity is the foundation. Other identity types require distinct design patterns and threat models.

**Statement**: Identity Platform SHALL remain Person-centric in Version 1.x.

Future identity types including:
- Device Identity
- Service Identity
- AI Agent Identity

SHALL be introduced through extension and SHALL NOT alter existing Person identity semantics.

### 5. Event Ownership Documentation

**Decision**: Explicit Event Ownership Table declares which domain events belong to Identity Platform.

**Rationale**: Clear ownership prevents event orphaning and enables consistent deployment patterns.

**Statement**: The Identity Platform owns and publishes the following domain events:

| Event               | Owner Capability | MVP |
|---------------------|------------------|-----|
| PersonRegistered    | Identity         | Yes |
| PersonUpdated       | Identity         | Yes |
| PasswordChanged     | Identity         | Yes |
| LoginSucceeded      | Identity         | Yes |
| LoginFailed         | Identity         | Yes |
| SessionCreated      | Identity         | Yes |
| SessionExpired      | Identity         | Yes |
| LogoutCompleted     | Identity         | Yes |
| OrganizationCreated | Identity         | Yes |
| MembershipCreated   | Identity         | Yes |

Lifecycle events beyond those listed above are outside the scope of Identity Blueprint Version 1.0 and MAY be introduced through future ADRs.

### 6. Future Identity Types Documentation

**Decision**: Future identity types are explicitly scoped as future extensions.

**Rationale**: Supports long-term platform extensibility while maintaining MVP simplicity.

**Statement**: Future versions MAY introduce:
- Device Identity
- Service Identity
- AI Agent Identity

These identity types SHALL extend the platform without modifying Person identity semantics.

## Consequences

### Document Updates

- 057_SmartCore_Tenancy_and_Ownership_Model.md version: 1.0 → 1.1
- 059_SmartCore_Identity_Platform.md version: 1.0 → 1.1

### Backward Compatibility

All changes are additive and clarifying. No breaking changes to existing Person identity model.

### Future Decisions

This ADR establishes the foundation for:
- Future identity type extensions (Device, Service, AI Agent)
- Role extension mechanisms
- Event extension patterns

## Acceptance Criteria

This ADR SHALL remain "Proposed" until:
- [ ] All related document changes (057, 059, 01_Domain_Model) have been implemented
- [ ] Architecture Validation Review has been completed
- [ ] Blueprint passes Structural Validation per 065_SmartCore_Blueprint_Validator_Specification

Upon successful Architecture Validation Review:
- Status SHALL be updated to "Accepted"
- Acceptance date SHALL be recorded
- Reference SHALL be added to all dependent ADRs

## References

- 019_SmartCore_Identity_and_Session_Continuity_Model.md
- 041_SmartCore_Identity_Model.md
- 057_SmartCore_Tenancy_and_Ownership_Model.md
- 059_SmartCore_Identity_Platform.md
- 064_SmartCore_Blueprint_Standard.md
- 065_SmartCore_Blueprint_Validator_Specification.md
- 066_SmartCore_AI_Code_Generation_Specification.md
- ADR-0003_Organization_and_Membership_Lifecycle_Standardization.md
