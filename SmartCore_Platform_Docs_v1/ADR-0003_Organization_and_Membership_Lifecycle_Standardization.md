# ADR-0003: Organization and Membership Lifecycle Standardization

## Metadata

- **ADR Number**: ADR-0003
- **Title**: Organization and Membership Lifecycle Standardization
- **Status**: Proposed
- **Version**: 1.2.1
- **Date Created**: 2026-07-08
- **Author**: SmartCore Architecture Team
- **Approval Date**: TBD
- **Effective Date**: TBD
- **Decision Type**: Architectural Decision
- **Decision Level**: Level 3 — Architectural Refinement

## Review Revision — 2026-09-24

This revision is a documentation correction candidate. Status remains Proposed;
Approval Date and Effective Date remain TBD. Decision requirements describe the
proposed architecture and do not constitute approval or implementation clearance.
Acceptance remains subject to the criteria below and Document 051.

---

## Decision Scope

1. Organization Lifecycle
2. Membership Lifecycle

---

## Scope

This ADR applies to:

* The Organization Aggregate lifecycle
* The Membership Aggregate lifecycle
* All Capability Platforms that adopt the SmartCore Tenancy and Ownership Model (057)

This ADR does not:

* Introduce lifecycle transition Commands, APIs, or Use Cases for Version 1.0 (MVP)
* Modify the Person or Credential lifecycles
* Redefine the SmartCore Command Model (027)
* Redefine Aggregate boundaries established in 03_Aggregates.md

---

## Context

The SmartCore Platform requires standardized lifecycle models for Organizations and Memberships to ensure consistency across all Capability Platforms and to provide clear architectural constraints for future evolution.

This ADR addresses:
- Organization state transitions and constraints
- Membership state transitions and constraints
- Lifecycle operation scoping (MVP vs. future)
- Extensibility patterns for lifecycle expansion

This ADR establishes a standard lifecycle template applicable to all SmartCore Capability Platforms that adopt the SmartCore Tenancy and Ownership Model. It does not introduce a new architectural layer, a new platform, or override an upstream Core standard; it is therefore classified as Level 3 — Architectural Refinement per 051§5.

## Decision

### 1. Organization Lifecycle

**Decision**: Organizations follow a four-state lifecycle.

**Rationale**: Four-state model supports future suspension, resumption, and retirement while keeping MVP Organizations directly Active and deferring transition operations.

**Statement**: Organization lifecycle SHALL follow:

```
Created → Active → Suspended → Archived
```

**State Definitions**:

- **Created**: Initial state upon organization creation. Transitions to Active upon configuration completion. Reserved lifecycle state for future staged organization initialization workflows. MVP registration bypasses this state and initializes Organizations directly as Active.
- **Active**: Normal operating state. Organization owns and manages resources. Members can access resources per authorization rules.
- **Suspended**: Organization operations are paused. Existing resources remain owned but inaccessible. Memberships remain active but non-functional.
- **Archived**: Organization is permanently retired. Historical records retained. No further state transitions.

**Transition Rules**:
- Created → Active: Automatic or explicit completion of initialization
- Active → Suspended: Explicit administrator action (future scope for MVP)
- Suspended → Active: Explicit administrator action (future scope for MVP)
- Suspended → Archived: Explicit administrator action (future scope for MVP)
- The transitions listed above are the complete allowed transition set.
- Active → Suspended and Suspended → Active form a reversible pair; entering Suspended does not prevent later resumption to Active.
- No transition returns to Created.
- Archived is terminal and permits no outgoing transition.
- The linear diagram shows the lifecycle states; it does not replace the transition rules.

**MVP Scope**:
Organizations SHALL be created in Active state for MVP.
Suspend and Archive operations are future scope.

**Future Extensions**: Suspended → Active reversal allows temporary operational pause.

**Alternatives Considered**:

*Alternative A — Two-state lifecycle (Active / Archived only)*
Rejected. Provides no mechanism for temporary operational pause (Suspended), which is a documented future requirement. Would require a breaking change to reintroduce Suspended later.

*Alternative B — Hard deletion instead of Archived*
Rejected. Conflicts with 057's requirement that historical ownership records remain traceable. Archived preserves auditability; deletion does not.

*Alternative C — Fully reversible lifecycle (all transitions bidirectional)*
Rejected. Undermines the intended semantics of Archived as a permanent terminal state and increases state-machine complexity without a documented business need.

---

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

The **Created** state exists in the lifecycle model to support future invitation-based workflows (e.g., pending invitations awaiting acceptance). In Version 1.0 (MVP), RegisterPerson's Owner Membership creation bypasses the Created state and initializes Membership directly as Active, since MVP has no invitation flow.

Revocation operations are future scope.
Multiple membership roles are future scope.

**Future Extensions**: Enables role changes, delegated membership management, and multi-role support.

**Alternatives Considered**:

*Alternative A — Two-state lifecycle (Active / Revoked only, no Created)*
Rejected. Would require a breaking change to the state machine when invitation-based Membership creation is introduced in a future version.

*Alternative B — Role encoded as a separate lifecycle dimension*
Rejected for Version 1.0. Adds complexity not required by MVP scope (single Owner role only, per ADR-0002 Decision 3, pending acceptance). Role remains a Membership attribute, not a parallel lifecycle.

---

## Consequences

### Document Updates

The supplied 057 is already version 1.3; version 1.2 was the historical lifecycle
update, not a target to which the document should be reverted. Track any further
correction using 051 §9.

| Document | Remaining synchronization work |
| --- | --- |
| 057_SmartCore_Tenancy_and_Ownership_Model.md | Clarify the complete transition set, including Suspended → Active, and direct Active initialization in MVP. |
| 059_SmartCore_Identity_Platform.md | Add the Organization/Membership lifecycle scope and an explicit reference to this Proposed ADR; record the final accepted reference upon approval. |
| 01_Domain_Model.md | Replace the misleading “MVP-visible lifecycle flow” description with a full lifecycle description; keep MVP initialization and exclusions explicit. |
| 03_Aggregates.md | Apply the same lifecycle-diagram clarification without changing Aggregate boundaries. |
| 14_MVP.md | Preserve direct Active initialization and excluded transition commands; synchronize this ADR reference. |

This table records work identified during review; it does not mark any acceptance
criterion as complete.

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

### Backward Compatibility

This ADR formalizes lifecycle states already present in 057 v1.1 and 01_Domain_Model.md. No breaking changes are introduced to any existing MVP behavior; Organizations and Memberships continue to be created directly in Active state.

### Future Decisions

This ADR establishes the foundation for:

* Future lifecycle transition Commands (SuspendOrganization, ArchiveOrganization, RevokeMembership)
* Future invitation-based Membership creation workflows
* Any future request to alter these state machines, which SHALL require its own architectural review and SHALL NOT be treated as automatically approved by this ADR

---

## Acceptance Criteria

This ADR SHALL remain "Proposed" until:
- [ ] All related document changes (057, 059, 01_Domain_Model, 03_Aggregates, 14_MVP) have been implemented
- [ ] Architecture Validation Review has been completed
- [ ] Blueprint passes Structural Validation per 065_SmartCore_Blueprint_Validator_Specification
- [ ] All affected documents reference ADR-0003 after acceptance
- [ ] Lifecycle terminology is synchronized across 057, 059, 01_Domain_Model, and 03_Aggregates

Upon successful Architecture Validation Review:
- Status SHALL be updated to "Accepted"
- Acceptance date SHALL be recorded
- Reference SHALL be added to all dependent ADRs and future Capability Blueprints

## References

> *Document 019 is retained as a referenced architectural context
> document for the identity/session-continuity concepts underlying this
> ADR. Its long-term
> lineage status (relative to 041 and 059) remains subject to future
> Architecture Board review under a separate governance track, and this
> reference does not constitute a supersession determination.*

- 019_SmartCore_Identity_and_Session_Continuity_Model.md
- 057_SmartCore_Tenancy_and_Ownership_Model.md
- 059_SmartCore_Identity_Platform.md
- 064_SmartCore_Blueprint_Standard.md
- 065_SmartCore_Blueprint_Validator_Specification.md
- 066_SmartCore_AI_Code_Generation_Specification.md
- ADR-0002_Identity_Foundation_Clarifications.md

---

## Change History

| Version | Status   | Description                                                                                                                   |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | Proposed | Initial organization and membership lifecycle standardization                                                                   |
| 1.1     | Proposed | Added governance metadata (Author, Decision Level, Approval/Effective Date), explicit Scope section, Alternatives Considered for both decisions, clarified Organization and Membership transition/Created-state wording, hedged reference to ADR-0002 pending its acceptance, added terminology-synchronization and document-reference Acceptance Criteria, made 057 version target conditional on acceptance, and added Change History |
| 1.2     | Proposed | Added a clarifying note to the References section stating that Document 019 is retained as an architectural context document for this ADR without constituting a lineage/supersession determination relative to 041/059; that determination is deferred to a separate Architecture Board governance track. No substantive decision content changed. |
| 1.2.1 | Proposed | 2026-09-24 review candidate: removed wording that contradicted the explicitly allowed Suspended → Active transition, clarified the complete allowed transition set, and updated document synchronization tracking. No new transition or MVP operation was introduced. |

---

**END OF DOCUMENT**