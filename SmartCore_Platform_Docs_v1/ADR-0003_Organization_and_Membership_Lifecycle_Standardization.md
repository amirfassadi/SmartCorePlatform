# ADR-0003: Organization and Membership Lifecycle Standardization

## Metadata

- **ADR Number**: ADR-0003
- **Title**: Organization and Membership Lifecycle Standardization
- **Status**: Proposed
- **Date Created**: 2026-07-08
- **Version**: 1.0

## Decision Scope

1. Organization Lifecycle
2. Membership Lifecycle

## Context

The SmartCore Platform requires standardized lifecycle models for Organizations and Memberships to ensure consistency across all Capability Platforms and to provide clear architectural constraints for future evolution.

This ADR addresses:
- Organization state transitions and constraints
- Membership state transitions and constraints
- Lifecycle operation scoping (MVP vs. future)
- Extensibility patterns for lifecycle expansion

## Decision

### 1. Organization Lifecycle

**Decision**: Organizations follow a four-state lifecycle.

**Rationale**: Four-state model provides flexibility for future operations while maintaining MVP simplicity through forward-only transitions and future scope designation.

**Statement**: Organization lifecycle SHALL follow:

```
Created → Active → Suspended → Archived
```

**State Definitions**:

- **Created**: Initial state upon organization creation. Transitions to Active upon configuration completion.
- **Active**: Normal operating state. Organization owns and manages resources. Members can access resources per authorization rules.
- **Suspended**: Organization operations are paused. Existing resources remain owned but inaccessible. Memberships remain active but non-functional.
- **Archived**: Organization is permanently retired. Historical records retained. No further state transitions.

**Transition Rules**:
- Created → Active: Automatic or explicit completion of initialization
- Active → Suspended: Explicit administrator action (future scope for MVP)
- Suspended → Active: Explicit administrator action (future scope for MVP)
- Suspended → Archived: Explicit administrator action (future scope for MVP)
- All transitions are irreversible except Suspended → Active

**MVP Scope**:
Organizations SHALL be created in Active state for MVP.
Suspend and Archive operations are future scope.

**Future Extensions**: Suspended → Active reversal allows temporary operational pause.

### 2. Membership Lifecycle

**Decision**: Memberships follow a three-state lifecycle.

**Rationale**: Three-state model supports MVP while maintaining consistent participation semantics and enabling future extensions.

**Statement**: Membership lifecycle SHALL follow:

```
Created → Active → Revoked
```

**State Definitions**:

- **Created**: Membership invitation or initial creation state. Membership not yet active for resource access.
- **Active**: Membership is active. Person may interact with Organization and its resources per authorization rules.
- **Revoked**: Membership is terminated. Person no longer participates in Organization. State is irreversible.

**Transition Rules**:
- Created → Active: Acceptance of invitation or explicit activation
- Active → Revoked: Explicit revocation (future scope for MVP)
- Revoked is a terminal state with no further transitions

**MVP Scope**:
Memberships SHALL be created in Active state for MVP.
Revocation operations are future scope.
Multiple membership roles are future scope.

**Future Extensions**: Enables role changes, delegated membership management, and multi-role support.

## Consequences

### Document Updates

- 057_SmartCore_Tenancy_and_Ownership_Model.md version: 1.1 → 1.2

### Architectural Consistency

- Establishes standard lifecycle pattern for all SmartCore Capability Platforms
- Provides template for lifecycle decisions in future Capability Blueprints
- Ensures consistent state terminology across platform documentation

### MVP Constraints

- Organizations created directly in Active state
- Memberships created directly in Active state
- Suspend, Archive, and Revoke operations deferred to future phases
- No lifecycle transition commands in Version 1.0

### Future Extensibility

- Lifecycle model accommodates future transition operations
- Provides foundation for multi-role and delegated administration
- Enables advanced organizational management patterns in future versions

## Acceptance Criteria

This ADR SHALL remain "Proposed" until:
- [ ] All related document changes (057, 059, 01_Domain_Model, 03_Aggregates, 14_MVP) have been implemented
- [ ] Architecture Validation Review has been completed
- [ ] Blueprint passes Structural Validation per 065_SmartCore_Blueprint_Validator_Specification

Upon successful Architecture Validation Review:
- Status SHALL be updated to "Accepted"
- Acceptance date SHALL be recorded
- Reference SHALL be added to all dependent ADRs and future Capability Blueprints

## References

- 019_SmartCore_Identity_and_Session_Continuity_Model.md
- 057_SmartCore_Tenancy_and_Ownership_Model.md
- 059_SmartCore_Identity_Platform.md
- 064_SmartCore_Blueprint_Standard.md
- 065_SmartCore_Blueprint_Validator_Specification.md
- 066_SmartCore_AI_Code_Generation_Specification.md
- ADR-0002_Identity_Foundation_Clarifications.md
