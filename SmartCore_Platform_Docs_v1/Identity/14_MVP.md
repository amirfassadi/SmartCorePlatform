<!--
Document ID: ID-14
Title: SmartCore Identity Platform Blueprint - MVP Scope
Version: 1.4.0
Status: DRAFT
Purpose: Define the proposed Identity mvp scope contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.4.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.3.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.1.1; prior text remains in Git history.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. MVP features

Exactly five Aggregates, six business Commands, five Queries and ten public Identity events. Verified email OR mobile, password and DisplayName registration includes bounded verification, atomic ownership, PendingCredential provisioning/recovery and Ready gating. The MVP creates one Personal Organization and one Owner Membership. Profile update changes DisplayName only. Password authentication/change, self queries and Session login/refresh/logout/expiry remain supported.

# 2. Explicit protocol choices

Registration has multiple API operations within RegisterPerson; no initial authenticated Session is returned. Login follows Ready. Omitted contact properties are absent, not null. Internal provisioning and setup challenges are not public event types. PersonRegistered keeps its name and records Ready time plus OwnershipCommittedAt.

# 3. Future scope

Contact changes/addition, lost-contact/general account recovery, MFA/social login, delegated administration, multiple Organization creation, membership invitations/roles, suspension/archive/revoke Commands, PasswordHistory and resource authorization. No new business field is mandatory for Identity registration.

# 4. Readiness

MVP scope is a proposal, not READY_FOR_GENERATION. Complete the gates in 12 and tests in 13; do not treat historical checklist ticks or an isolated PR merge as acceptance.

# 5. Accepted operational recovery scope

Internal AdminRecoverStalledRegistration and Ready acknowledgment are included as accepted architectural support operations under ADR-0004, without adding public Person Commands/endpoints/events. Two actions only: guarded invalidation before commit and canonical reconciliation after commit. General administrative cancellation, emergency revocation, password reset and direct database unlock remain excluded. Operational design must be implemented and verified before rollout; accepting indefinite waiting alone is not sufficient.
