<!--
Document ID: ID-05
Title: SmartCore Identity Platform Blueprint - Queries
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity queries contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.0.2; prior text remains in Git history.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Query boundary

Five read-only Queries; none mutates a workflow or creates a Session. Self queries require a valid authenticated Session and resolve caller identity from that Session. No client PersonId can widen access. DTOs use [08](08_API.md); service lookup uses [07](07_Contracts.md).

# 2. Query catalog

| Query | Input and authorization | Output | Filtering / ordering / pagination |
|---|---|---|---|
| GetCurrentPerson | Current authenticated Session | Own PersonId, optional Email/Mobile, DisplayName, Status, CreatedAt, UpdatedAt | One object; exactly one verified contact; no pagination |
| GetOrganizationsForPerson | Current authenticated Session | OrganizationId, Name, Category, Status, CreatedAt via own Membership | One Personal Organization in MVP; no arbitrary filters or pagination |
| GetMembershipsForPerson | Current authenticated Session | MembershipId, PersonId, OrganizationId, Role, Status, CreatedAt | Own Owner Membership in MVP; no arbitrary filters or pagination |
| GetSessionsForPerson | Current authenticated Session | SessionId, optional DeviceInfo/IpAddress, ExpiresAt, Status, CreatedAt | Own active unexpired Sessions, CreatedAt descending then SessionId ascending; no pagination in MVP; bounded by configured session cap |
| GetPersonById | PersonId; authenticated allowlisted service identity | PersonId and DisplayName only | One object, not found if absent; no public REST route |

No token, password material, registration mapping or Credential data appears in Query responses. GetPersonById does not expose Email, Mobile, Status or readiness; it can resolve a committed PendingCredential Person and is not an authentication/authorization guarantee. Business permission decisions remain with the consumer.

# 3. Failures

Invalid self Session is unauthorized. Missing Person behind a valid Session is an integrity failure and operational alert, not a fabricated Person. Service lookup rejects untrusted callers and malformed IDs; absent ID is not found. Repository unavailability returns unavailable without partial fabricated success.

# 4. Acceptance

Read scope, contact omission and token exclusion are tested under [13](13_Testing.md). Query narrowing for GetPersonById is intentional.
