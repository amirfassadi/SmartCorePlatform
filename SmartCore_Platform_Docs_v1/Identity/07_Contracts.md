<!--
Document ID: ID-07
Title: SmartCore Identity Platform Blueprint - Interoperability Contracts
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity interoperability contracts contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.0.2; prior text remains in Git history.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Contract boundary

Per 064 §§8.8–8.9, this file owns transport-independent service and message contracts. REST request/response shapes previously here are consolidated in [08_API](08_API.md); there is one authoritative wire definition. Names below are internal operations, not additional public business Commands or events.

The companion `services.schema.json` defines proposed camelCase message encodings for these service operations; it does not add public REST endpoints. Transport authentication and cross-field equality checks (such as materialOwner = registrationId) are mandatory service rules, not inferred from schema type checks.

# 2. IdentityLookup v1

`GetPersonById(PersonId) -> Found(PersonId, DisplayName) | NotFound`.

Only authenticated, allowlisted capability identities may call. Return no contact, Credential, Session or readiness information. Consumers decide their own business authorization. This service cannot be used as a readiness check.

# 3. CredentialProvisioning v1 (proposed)

## 3.1 EnsureInitialCredential

Input: registrationId, PersonId, operationId, protectedMaterialRef, materialOwner=registrationId, purpose=`initial-registration`. Automated operationId is registrationId; authorized setup uses its distinct setupChallengeId. Identity authenticates to the Credential service with purpose-scoped service credentials. Client input cannot directly call this operation or supply a material reference.

Credential service atomically enforces unique initial-registration slot per registrationId and the one-active-Credential invariant per Person. The first successful candidate creates the active Credential and a durable operation result; later candidates return the winning CredentialId without changing its password. Same operationId with different bound input is conflict. All outcomes are durable before acknowledgment. No speculative replacement is allowed when a competing request's response was lost.

Output: `Active(registrationId, PersonId, CredentialId, operationIdOfWinner, confirmationVersion)` or `RetryableUnavailable` or terminal `InvalidMaterial`/`BindingConflict`. No password hash is returned. Initial setup emits no new public event.

## 3.2 GetInitialCredentialResult

Input: registrationId and PersonId, authenticated Identity service. Output: `NotProvisioned`, `Active` as above, or `Unavailable`. Identity polls this operation after timeouts/crashes and before retry exhaustion; transport retries do not authorize another Credential. Polling uses the bounded policy in 10; no callback or new public event is required.

The service verifies matching Person/registration and current active status. An authenticated response is evidence for Identity's subsequent local Ready transaction, not a cross-service transaction. In MVP, no independent revoke/replace of an initial Credential is permitted before Ready is reconciled. Any administrative Credential operations added later must coordinate this race explicitly. Authentication always checks current active Credential separately, even after Ready.

Durable initial outcome/deduplication tombstones live for the registration lifetime (without secret material). Retries after material disposal can still return an existing winner. An unavailable result never becomes proof of readiness.

## 3.3 Ready reconciliation

Identity verifies response binding, then locally CASes PendingCredential→Ready and atomically inserts one PersonRegistered and stream position. If local commit fails, poll the same result and retry. A repeated confirmation for Ready is a no-op. The winning Credential operation provenance is persisted separately from the Ready actor. A synchronous Person request causing Ready records PersonId; a later reconciliation worker causing Ready records System, even if the original candidate was manual. It does not reuse the original ownership request's IP/device. See 06 §4.2.

# 4. Protected material and challenge delivery

The secret store supports stage(owner=verificationSessionId, expiry), bind-to-registration within Identity's durable transaction/reference protocol, authorize-read for the scoped Credential service, and invalidate/delete. Physical secret movement need not be transactional; durable references and ownership are. Failed commit leaves only pre-commit-owned expiring material, never a committed reference to disposed material.

Delivery accepts selected canonical contact, purpose and code; it reveals no account-existence result to the caller. Templates never include passwords. Technical delivery is infrastructure, not a business Communication dependency. Setup delivery reads the verified contact from committed Person; it does not trust a caller-supplied destination.

# 5. Event integration contract

The ten events and PascalCase payload/envelope fields are authoritative in [06](06_Domain_Events.md). Optional fields are omitted, never null. PersonRegistered has optional Email, deliberately no Mobile contact payload, required OwnershipCommittedAt, Ready-time OccurredAt and no SessionReference. Consumers identify mobile-only Persons by PersonId; adding Mobile later requires consumer/privacy review rather than silently widening exposure.

PersonUpdated follows the same optional-Email minimization; LoginFailed accepts selected ContactType/ContactValue in its restricted security payload. No secrets are included. Registration/profile stream position is transport metadata preserved through Outbox and broker; it is not Aggregate version. Consumers deduplicate by EventId before applying monotonically ordered positions. Only PersonRegistered and PersonUpdated join that stream.

# 6. Compatibility and acceptance

These contracts are proposed version 1.1.0. Confirm deployed consumers and contract-version policy before acceptance; absence of consumers has not been demonstrated by this repository. Optional Email, changed timestamps, narrowed profile updates and registration responses are real contract changes. Do not silently deploy to an existing v1 client. Governance must select migration/version routing if any such consumer exists.
