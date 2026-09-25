<!--
Document ID: ID-15
Title: SmartCore Identity Platform Blueprint - Extensibility
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity extensibility contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Governed extension points

Delivery adapters, secret-store implementations and Credential-service transport may vary while preserving proofs, expiry, idempotency and local transaction guarantees. Database/broker selection cannot weaken uniqueness or ordered unique event application.

# 2. Changes requiring new decisions

Adding contacts or changing them requires new verified-contact/recovery rules; administrative Credential changes must close the confirmation-to-Ready race. General cancellation/compensation of pending ownership requires lifecycle and cross-platform retention decisions. A commit-time signal must be distinct; never move PersonRegistered back to ownership commit. Additional Credential types/refresh-token Aggregate promotion require 03's boundary review, not automatic promotion of supporting records.

# 3. Contract evolution

Inventory consumers, select compatibility/migration policy and update narrative, API and machine schema together. Do not silently widen contact disclosure or turn application records into new public events. No extension listed here is an MVP requirement.

# 4. Accepted boundary

ADR-0004's acknowledgment and restricted administrative recovery are now accepted architectural requirements, not future extensions. Administrative post-commit cancellation/revocation still requires a new governed design that arbitrates an in-flight Identity Ready transition; it cannot be added as a force flag to recovery. T16 remains a separate open ordering decision.
