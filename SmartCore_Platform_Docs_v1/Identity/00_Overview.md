<!--
Document ID: ID-00
Title: SmartCore Identity Platform Blueprint - Overview
Version: 1.2.0
Status: DRAFT
Purpose: Define the proposed Identity overview contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.2.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.1.0; prior text remains in Git history.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Purpose and boundary

Identity owns Person identity, Personal Organization ownership, Membership, Credential and Session. Business authorization remains with consuming capabilities. Resources belong to Organizations, not Persons. Membership is the participation path. Authentication and authorization are separate.

# 2. Registration

`RegisterPerson` is one application process with multiple protocol operations:

1. Accept exactly one email or mobile, password and DisplayName. Stage protected password material under a verification session; send a purpose-bound code. Neither Person nor ownership exists yet.
2. After proof, commit Person, Personal Organization and Owner Membership atomically with the workflow, consumed verification mapping, transferred material reference and Outbox work. Return the stable `registrationId` and `PendingCredential`; no authentication tokens.
3. Provision Credential idempotently. Confirm the committed active Credential, then atomically transition the application workflow to `Ready` and enqueue `PersonRegistered`. The response may already report Ready if this completed. The client signs in through `AuthenticatePerson` afterwards.

Ownership failure rolls back the whole ownership transaction. Credential failure retains ownership, blocks login and enters bounded retry/secure completion. An abandoned PendingCredential registration need never produce PersonRegistered. No automatic deletion/compensation is implied.

# 3. Model and surfaces

Five Aggregates: Person, Organization, Membership, Credential, Session. Verification, registration workflow, Outbox and stream counters are supporting application records, not Aggregates.

Six business Commands: RegisterPerson, AuthenticatePerson, UpdatePersonProfile, LogoutSession, RefreshSession, ChangePassword.

Five Queries: GetCurrentPerson, GetOrganizationsForPerson, GetMembershipsForPerson, GetSessionsForPerson, GetPersonById.

Ten public Identity events remain: nine Domain Events and the Security Event LoginFailed. Internal provisioning work and verification operations do not add public events or Commands. Definitions are in [04](04_Commands.md), [05](05_Queries.md), [06](06_Domain_Events.md), [07](07_Contracts.md) and [08](08_API.md).

# 4. Dependencies

Use Core infrastructure for persistence, delivery, key management and authenticated service transport; no dependency on a business Communication capability is introduced by technical SMS/email delivery. No Shared Kernel or Core dependency may point back to Identity. External consumers resolve minimal Person identity through GetPersonById and must not infer permission to authenticate from ownership events.

# 5. Integrated merge and readiness

This package incorporates the proposals of PRs #1–#4 as a coherent alternative to merging their overlapping branches separately. Review and merge one consistent snapshot; do not cherry-pick readiness headers alone. If the earlier PRs merge first, rebase and reconcile this package before merging. Partial merges do not authorize generation.

All 00–16 documents remain DRAFT. Acceptance requires ADR governance, consumer compatibility review, full 065 validation and the runtime/security tests in [13](13_Testing.md). Existing implementation or deployed consumer compatibility is not asserted.
