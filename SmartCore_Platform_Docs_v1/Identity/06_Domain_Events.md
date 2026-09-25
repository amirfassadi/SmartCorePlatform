<!--
Document ID: ID-06
Title: SmartCore Identity Platform Blueprint - Domain Events
Version: 1.3.0
Status: DRAFT

Purpose:
Define the Domain Event Contract of the Identity Platform: the common
event envelope (including the Event Audit Requirements named but not
specified by 01_Domain_Model.md), event ownership, and the per-event
payload schema for all 10 MVP Identity events (nine Domain Events and LoginFailed, a Security Event). This is the
document 01_Domain_Model.md's "Event Audit Requirements" section
explicitly defers to ("Detailed event contracts are defined in
06_Domain_Events.md").

Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol,
- 00_Overview.md
- 01_Domain_Model.md
- 03_Aggregates.md
- 04_Commands.md
- 14_MVP.md
- 059_SmartCore_Identity_Platform.md
- ADR-0002_Identity_Foundation_Clarifications.md

Cross-Checked Against (Optional / informative only):
- 02_Use_Cases.md
- 05_Queries.md

Contract boundaries:
This file owns PascalCase event envelopes/payloads. 07_Contracts.md references them for interoperability; 08_API.md independently owns camelCase REST schemas. See 09, 11 and 12 for persistence, security and acceptance gates.

Change Log:
  - Version 1.3.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.2.0 (2026-09-24): Aligned optional Email snapshots, selected-contact LoginFailed audit and machine omission rules; retained the ten-event catalog and limited registration/profile stream.
  - Version 1.1.0 (2026-09-24): Proposed alignment with ADR-0002
    Decisions 8–9: PersonRegistered is enqueued on Ready, its
    OccurredAt is the Ready transition, and its payload includes
    OwnershipCommittedAt. Email is optional for mobile-only
    registration, and no initial SessionReference is attached.
    Updated publishing and ordering language; full Blueprint and
    contract validation remain pending.
  - Version 1.0.2 (2026-07-14): Architect-review refinement pass —
    approved with minor non-blocking comments, both addressed. (1)
    §6.1 reworded to stop implying `OccurredAt` is itself the
    per-Aggregate ordering mechanism: two events on the same Aggregate
    committed in the same transaction, or at coarse timestamp
    resolution, could carry equal or non-monotonic `OccurredAt`
    values. The guarantee is now stated as "observable in actual
    occurrence order", with `OccurredAt` merely expected to be
    consistent with that order, not the enforcement mechanism itself
    (a sequence/version/stream-position concept, left out of scope
    per §1.2). (2) Added an explicit note on the deliberate absence of
    an `EventVersion`/`SchemaVersion` envelope field: not needed while
    there is a single internal consumer context and no external
    Integration Event surface, but flagged as the most likely first
    envelope addition if either changes in a future version. No new
    Aggregates, Commands, Queries, or Events introduced; no MVP scope
    changed.
  - Version 1.0.1 (2026-07-14): Review-driven correction pass.
    (1) **Contradiction resolved**: `AggregateId` was previously
    unconditionally Required, contradicting `LoginFailed`'s own §4.6
    exception for `Reason = PersonNotFound` (no Person, hence no
    Aggregate, exists). `AggregateId` now explicitly shares the same
    exception as `ActorIdentity`, and `AggregateType` is fixed to
    `Person` for all `LoginFailed` events regardless of Reason. This
    was the one item flagged as blocking before v1.0.0 lock. (2)
    `CorrelationId` changed from unconditionally Optional to Required
    for all Person-initiated events, Optional only when
    `ActorIdentity = System` (i.e. `SessionExpired`), strengthening
    the audit-trail guarantee. (3) Added an explicit note
    distinguishing `OccurredAt` (commit time) from any future
    publish/delivery timestamp, anticipating Outbox-style delivery
    delay. (4) Added a forward-compatibility note to `PersonUpdated`
    flagging the full-snapshot payload as an MVP-appropriate choice
    that may need revisiting (delta shape, or field-specific events)
    if Person's mutable attribute set grows substantially. No new
    Aggregates, Commands, Queries, or Events introduced; no MVP scope
    changed.
  - Version 1.0.0 (2026-07-14): Initial Domain Events Blueprint.
    Defines the common Event Envelope satisfying 01_Domain_Model.md's
    Event Audit Requirements (Actor Identity, Session Reference,
    Delegated Identity, Timestamp, Execution Context); specifies all
    10 MVP events' payloads; defines Publishing Rules and Event
    Ordering guarantees; verifies alignment against 059, 01, 04, 14,
    and ADR-0002. No new Aggregates, Commands, Queries, or Events
    introduced. No Event Bus, Outbox, or Integration Event mechanics
    defined — explicitly out of scope (§1.2).
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

# 1. Overview

This document defines the **Domain Event Contract** of the Identity
Platform: what a Domain Event *is*, structurally, and what each of the
10 MVP Identity Events *contains*.

A Domain Event answers:

> "What business fact has already, irreversibly, happened?"

Domain Events are immutable records of completed state transitions.
They are published only after the underlying Aggregate state change
has been durably committed (§5).

## 1.1 What This Document Defines

- The common Event Envelope (§4.1) — satisfying the Event Audit
  Requirements named by 01_Domain_Model.md but left unspecified there
- Event ownership (§3, restating and confirming ADR-0002 Decision 5)
- The payload schema for each of the 10 MVP events (§4.2–§4.11)
- Publishing Rules (§5) — when an event SHALL and SHALL NOT be
  published
- Event Ordering guarantees (§6) — what a consumer MAY and MAY NOT
  assume about the relative order of events

## 1.2 What This Document Does NOT Define

- **Event Bus / Message Broker technology** (Kafka, RabbitMQ, SNS/SQS,
  etc.) — an infrastructure choice, out of scope
- **Outbox pattern or delivery guarantee mechanics** (at-least-once,
  exactly-once, retry/dedup strategy) — an infrastructure/reliability
  concern, out of scope
- **Integration Event contracts** — whether, how, or in what shape
  these Domain Events cross the Identity Platform's boundary to be
  consumed by other Capability Platforms is a separate concern
  (Integration Event design is typically a translation/adapter layer
  over Domain Events, not the Domain Event itself) and is deferred to
  a future Integration/Messaging document
- **REST/Wire representation** — how (or whether) an event's data
  might ever be surfaced through a REST API is a 07_Contracts.md /
  08_API.md concern, not this one; those documents are explicitly not
  dependencies of this one (see header)

This document introduces no new:

- Aggregates
- Commands
- Queries
- Events beyond the 10 already declared in 059 §9 / ADR-0002 Decision 5
- Business Rules

---

# 2. Event Design Principles

## 2.1 Events Represent Completed Facts

Per ADR-0002 Decision 5: "Events represent completed business facts."

Every event name is a past-tense statement (`PersonRegistered`, not
`RegisterPerson`; `SessionExpired`, not `ExpireSession`). An event is
never published speculatively or in advance of the state change it
describes.

## 2.2 Events Are Immutable

Per 059 §10: "Events SHALL be immutable." Once published, an event's
content SHALL NOT be revised. A correction, if ever needed, is
expressed as a new, later event — never as a mutation of a
previously published one.

## 2.3 Events SHALL NOT Coordinate Initial Ownership Creation

Per ADR-0002 Decision 5: "Events SHALL NOT be used to coordinate
initial ownership creation." The atomicity of Person + Personal
Organization + Owner Membership creation is guaranteed by the Core
Ownership Transaction (ADR-0002 Decision 1; 059 §6), not by any
event-driven saga. `PersonRegistered`, `OrganizationCreated`, and
`MembershipCreated` are announcements of an already-consistent,
already-committed fact — never a mechanism used to *achieve* that
consistency. This principle directly shapes the Event Ordering
guarantees in §6.3.

## 2.4 Payload Fields Trace to the Domain Model

Payload fields in §4 trace to existing domain attributes and Aggregate
references, except `OwnershipCommittedAt`: this timestamp records the
Decision 1 ownership transaction separately from the Decision 8 Ready
transition. The dependent Domain Model and machine contracts require
alignment before this Blueprint is generation ready.

## 2.5 Credential Secrets Are Never Present in Any Event

No event payload SHALL ever contain `PasswordHash`, a plaintext
password, or any other Credential secret material. Where a Credential
lifecycle change must be represented (`PasswordChanged`), the payload
carries only the Credential's identity (`CredentialId`), never its
content. This follows directly from 01_Domain_Model.md §2 ("Credential
never stores plain text passwords") and 059 §13 ("Passwords SHALL
never be stored in plain text") — the same principle extended to the
event stream, where a leak would be equally damaging.

## 2.6 Security classification

LoginFailed is a Security Event under ADR-0002 Decision 5. The remaining nine events are Domain Events. Field-level access, logging and retention requirements are now specified in 11_Security.md. ContactValue is restricted personal data; a resolved PersonId on failed login identifies the target, not an authenticated caller. None of these fields may be treated as proof of authorization.

---

# 3. Event Ownership

Per 059 §9 (Event Ownership Table) and ADR-0002 Decision 5, the
Identity Platform owns and exclusively publishes the following 10
events. Both source documents agree on this table exactly; no
discrepancy exists.

| Event | Owner | MVP | Producing Service (01_Domain_Model §§7–8) |
|---|---|---|---|
| PersonRegistered | Identity | Yes | RegistrationApplicationService |
| OrganizationCreated | Identity | Yes | RegistrationApplicationService |
| MembershipCreated | Identity | Yes | RegistrationApplicationService |
| LoginSucceeded | Identity | Yes | AuthenticationDomainService |
| LoginFailed | Identity | Yes | AuthenticationDomainService |
| SessionCreated | Identity | Yes | AuthenticationDomainService |
| SessionExpired | Identity | Yes | SessionManagementDomainService |
| LogoutCompleted | Identity | Yes | SessionManagementDomainService |
| PersonUpdated | Identity | Yes | PersonManagementDomainService |
| PasswordChanged | Identity | Yes | CredentialManagementDomainService |

No event in this table is owned by, or co-published with, any other
Capability Platform. No additional Identity event exists beyond these
10 in Version 1.0 (14_MVP §1).

---

# 4. Event Specifications

## 4.1 Common Event Envelope

Every event published by the Identity Platform SHARES this envelope.
Per-event payload schemas (§4.2–§4.11) define only the `Payload`
field's contents; every other envelope field below applies uniformly.

| Field | Type | Required | Description |
|---|---|---|---|
| EventId | string (UUID) | Required | Unique identifier of this event instance |
| EventType | string | Required | Exact event name, e.g. `PersonRegistered` |
| AggregateType | string enum: `Person` \| `Organization` \| `Membership` \| `Session` \| `Credential` | Required | Which Aggregate (01_Domain_Model §1) this event pertains to |
| AggregateId | string (UUID) | Required — see exception in §4.6 | The identifier of the specific Aggregate instance this event is about (e.g. PersonId for a Person-type event, SessionId for a Session-type event) |
| OccurredAt | string (timestamp, ISO 8601 UTC) | Required | When the fact described by the event was committed; for PersonRegistered, the registration workflow's transition to Ready (§4.2) |
| ActorIdentity | string (PersonId), or the reserved value `System` | Required — see exception in §4.6 | The actor of the completed fact: PersonId for a Person-initiated transition, `System` for automated processing (including registration recovery and scheduled jobs) |
| SessionReference | string (SessionId) | Optional | The Session under which the causing request was made, if any (see per-event tables for when this applies) |
| DelegatedIdentity | string (PersonId) | Optional — always absent in MVP | Reserved for a future delegation feature (14_MVP §3 / 059 §17). No MVP Command or Use Case populates this field; it exists so the envelope shape does not need to change when delegation is introduced |
| ExecutionContext | object (§4.1.1) | Optional | Operational context describing how the causing request was made |
| Payload | object | Required | Event-specific business data; schema defined per event in §4.2–§4.11 |

Audit-related fields identify the fact's actor and execution context. Optional fields are omitted, never null. DelegatedIdentity is prohibited in the MVP machine schema and can only be introduced by a separately versioned delegation contract.

**On `OccurredAt` vs. publish time**: `OccurredAt` is the commit time
of the fact described by the event. For `PersonRegistered`, that fact
is the durable registration workflow's transition to Ready, atomically
enqueued with the event, rather than a new Person Aggregate transition
or the earlier ownership commit (§4.2). It is **not** the moment the
event was published, transmitted, or received by any consumer. This
document defines no `PublishedAt` field, since
publication timing is a delivery-mechanism concern (§1.2, §5.5) outside
this Contract's scope. If a future Event Bus/Outbox implementation
introduces a delay between commit and publish (which is expected and
normal for outbox-style delivery), that delay is invisible to this
Contract: `OccurredAt` remains fixed at commit time regardless of when
the event actually reaches a consumer. A future Transport/delivery
document, not this one, would be the place to add a `PublishedAt`
field if a consumer-facing need for it is demonstrated.

**Schema versioning**: This proposal retains the existing envelope without adding EventVersion. The versioned schema is events.schema.json. A consumer inventory and compatibility/migration decision remain required before deployment; this repository does not prove there are no existing consumers. Preserve event names under ADR-0002 and do not silently replace an incompatible deployed contract.

### 4.1.1 ExecutionContext Object

| Field | Type | Required |
|---|---|---|
| CorrelationId | string | Required, except Optional when `ActorIdentity = System` |
| IpAddress | string | Optional |
| DeviceInfo | string | Optional |

**On `CorrelationId`**: A Person-initiated event (i.e. `ActorIdentity`
is a real PersonId) SHALL carry a `CorrelationId` linking it back to
the request that caused the event's fact,
since a full audit trail for a Person-initiated action requires being
able to trace the event to the request that caused it. `CorrelationId`
is Optional when `ActorIdentity = System`, including scheduled
`SessionExpired` (§4.8) or automated registration recovery (§4.2).
`IpAddress` and `DeviceInfo` remain
Optional throughout, since not every request transport surfaces them
(e.g. an internal service-to-service call may have no meaningful
client IP/device to report).

`ExecutionContext` is the single place operational request metadata
lives for every event — including events on Aggregates that have no
`DeviceInfo`/`IpAddress` attribute of their own (Person, Organization,
Membership, Credential). For Session-related events, this is
populated from the same source data as the Session Aggregate's own
`DeviceInfo`/`IpAddress` attributes (01_Domain_Model §2), but it is
captured here at the envelope level rather than duplicated inside the
event-specific Payload, so that every event — not only Session events
— has one consistent place for this information.

## 4.2 PersonRegistered

**Producer**: RegistrationApplicationService (§3)

**ActorIdentity**: The actor that caused the Ready transition, not
necessarily the actor of the earlier ownership commit. Use the
registered PersonId when the Person completes the distinct secure
Credential challenge; use `System` when automated provisioning or
reconciliation completes registration. This does not imply that a
password-authenticated Session already exists. A future administrator
completion path requires its own governed actor rule.

**ExecutionContext**: For synchronous Person-initiated completion, use the request
that actually caused Ready (including its CorrelationId), not the
original registration request. For automated completion, do not
attribute the original request's IP/device to the worker; System
correlation and other context are optional under §4.1.1.

**SessionReference**: Absent. `PersonRegistered` is enqueued atomically
with the transition to Ready, before any optional initial Session is
created. A later Session, whether successful or failed, SHALL NOT
retroactively change this immutable event (ADR-0002 Decision 8).

**OccurredAt**: The timestamp of the atomic Ready transition and
`PersonRegistered` enqueue. `OwnershipCommittedAt` in the payload is
the earlier ownership commit timestamp; manual Credential completion
may separate them by hours or days. Consumers SHALL use the latter
for account age or ownership-based retention, not receipt time.

### Payload

| Field | Type | Required |
|---|---|---|
| PersonId | string (UUID) | Required |
| Email | string | Optional; absent for mobile-only registration |
| DisplayName | string | Required |
| OrganizationId | string (UUID) | Required |
| MembershipId | string (UUID) | Required |
| OwnershipCommittedAt | string (timestamp, ISO 8601 UTC) | Required |

`OrganizationId` and `MembershipId` are included directly on this
payload — rather than requiring a consumer to separately correlate
`OrganizationCreated`/`MembershipCreated` — because, per ADR-0002
Decision 1, a Person without ownership context is an invalid Identity
state: by the time `PersonRegistered` exists at all, these two
references are guaranteed to already exist and be valid (§2.3, §6.3).
`Email` is present only if the registered contact is email; a mobile-only
Person is identified by `PersonId` without inventing a mobile payload
field in this revision. No Credential secret or verification code is
included. Optional fields are omitted, never null. The contact contract is defined in 01, 07 and 08; consumer compatibility and runtime validation remain acceptance gates.

## 4.3 OrganizationCreated

**Producer**: RegistrationApplicationService (§3)

**ActorIdentity**: The PersonId of the registering Person (the
Organization's Owner).

**SessionReference**: Absent. Organization creation is part of the
Core Ownership Transaction, which precedes any authenticated Session
context (059 §6) — there is no session to reference at this point in
the flow.

**OccurredAt**: The atomic ownership commit time, which may precede
`PersonRegistered.OccurredAt` by a prolonged recovery interval.

### Payload

| Field | Type | Required |
|---|---|---|
| OrganizationId | string (UUID) | Required |
| Name | string | Required |
| Category | string enum: `Personal` | Required |
| Status | string enum: `Active` | Required |

**MVP Constraint**: `Category` is always `Personal` and `Status` is
always `Active` in MVP (01_Domain_Model §2; 14_MVP §1).

## 4.4 MembershipCreated

**Producer**: RegistrationApplicationService (§3)

**ActorIdentity**: The PersonId of the registering Person.

**SessionReference**: Absent — same rationale as §4.3.

**OccurredAt**: The same atomic ownership commit time as
`OrganizationCreated`, not the later Ready transition (§4.2).

### Payload

| Field | Type | Required |
|---|---|---|
| MembershipId | string (UUID) | Required |
| PersonId | string (UUID) | Required |
| OrganizationId | string (UUID) | Required |
| Role | string enum: `Owner` | Required |
| Status | string enum: `Active` | Required |

**MVP Constraint**: `Role` is always `Owner` and `Status` is always
`Active` in MVP (14_MVP §1; 059 §9 Role Model).

## 4.5 LoginSucceeded

**Producer**: AuthenticationDomainService (§3)

**ActorIdentity**: The authenticated Person's PersonId.

**SessionReference**: The SessionId of the Session created as part of
this same authentication (04_Commands §4.2). See §6.2 for the ordering
relationship between `LoginSucceeded` and `SessionCreated`.

### Payload

| Field | Type | Required |
|---|---|---|
| PersonId | string (UUID) | Required |
| SessionId | string (UUID) | Required |

## 4.6 LoginFailed

**Producer**: AuthenticationDomainService (§3)

**ActorIdentity**: **Exception to the envelope's general rule** — this
field is Optional for `LoginFailed` only, and is absent specifically
when `Reason = PersonNotFound` (there is no Person to identify as the
actor). When `Reason` is `CredentialMissing`, `RegistrationNotReady`, `PersonInactive`, or `InvalidPassword`, a
Person record does exist and `ActorIdentity` SHALL be populated with
that PersonId.

**AggregateType / AggregateId — same exception, extended**: `AggregateType`
is always `Person` for `LoginFailed` (a login attempt is conceptually
an operation against a Person, whether or not resolution succeeds).
`AggregateId`, however, follows exactly the same rule as `ActorIdentity`
above: it SHALL be populated with the resolved PersonId when `Reason`
is `CredentialMissing`, `RegistrationNotReady`, `PersonInactive`, or `InvalidPassword` (a Person record exists),
and SHALL be absent when `Reason = PersonNotFound` (there is no
Aggregate instance to identify — no Person, and therefore no
Aggregate, exists to attempt authentication against). This is the same
underlying exception stated once, not a second independent one: both
`ActorIdentity` and `AggregateId` are populated from the same resolved
PersonId when a Person exists, and both are absent together when one
does not.

**SessionReference**: Always absent — no Session is created on a
failed authentication attempt (04_Commands §4.2 Postconditions).

### Payload

| Field | Type | Required |
|---|---|---|
| ContactType | string enum: `Email` \| `Mobile` | Required |
| ContactValue | string | Required; canonical attempted contact, restricted security data |
| Reason | string enum: `PersonNotFound` \| `CredentialMissing` \| `RegistrationNotReady` \| `PersonInactive` \| `InvalidPassword` | Required |

**Security Note**: `Reason` carries the precise internal cause for
audit purposes, as required by 04_Commands §4.2 even though any external-facing surface built on top of this
event (e.g. a REST API) is expected to collapse these reasons
into a single generic outcome to prevent account enumeration. The API must collapse these reasons into its generic authentication failure; this Security Event preserves the restricted internal audit trail.

## 4.7 SessionCreated

**Producer**: AuthenticationDomainService (§3)

**ActorIdentity**: The Person the Session belongs to.

**SessionReference**: Not applicable as a separate field — this event
*is* the Session's own creation; `AggregateId` (envelope) already
carries the SessionId.

### Payload

| Field | Type | Required |
|---|---|---|
| SessionId | string (UUID) | Required |
| PersonId | string (UUID) | Required |
| ExpiresAt | string (timestamp) | Required |

`DeviceInfo` and `IpAddress` are deliberately not duplicated into this
Payload — they are available on this same event via
`ExecutionContext` (§4.1.1), which is where all request-execution
metadata lives uniformly across every event, not only Session events.

## 4.8 SessionExpired

**Producer**: SessionManagementDomainService (§3)

**ActorIdentity**: The reserved value `System`. Per 02_Use_Cases UC-007
"Main Flow (System Expiration)", this event originates from a
scheduled job, not a Person-initiated request — there is no human
actor to name.

**SessionReference**: Not applicable as a separate field; `AggregateId`
carries the SessionId.

### Payload

| Field | Type | Required |
|---|---|---|
| SessionId | string (UUID) | Required |
| PersonId | string (UUID) | Required |

## 4.9 LogoutCompleted

**Producer**: SessionManagementDomainService (§3)

**ActorIdentity**: The Person who performed the logout.

**SessionReference**: Not applicable as a separate field; `AggregateId`
carries the SessionId (the same Session being closed).

### Payload

| Field | Type | Required |
|---|---|---|
| SessionId | string (UUID) | Required |
| PersonId | string (UUID) | Required |

## 4.10 PersonUpdated

**Producer**: PersonManagementDomainService (§3)

**ActorIdentity**: The Person whose profile was updated (Session
ownership validation in 04_Commands §4.3 guarantees the caller is
always this same Person — self-service update only in MVP).

**SessionReference**: The Session under which the update request was
authenticated.

### Payload

| Field | Type | Required |
|---|---|---|
| PersonId | string (UUID) | Required |
| Email | string | Optional; omitted for mobile-only Person |
| DisplayName | string | Required |

**Design Note**: Snapshot of PersonId, optional Email and DisplayName after a DisplayName update. Contact mutation is outside this MVP. Email is omitted for mobile-only Persons, never null; Mobile is intentionally excluded from the public event for data minimization. Consumers identify the Person by PersonId. This does not authorize a contact lookup through GetPersonById.

## 4.11 PasswordChanged

**Producer**: CredentialManagementDomainService (§3)

**ActorIdentity**: The Person whose Credential was replaced.

**SessionReference**: The Session under which the change request was
authenticated.

### Payload

| Field | Type | Required |
|---|---|---|
| PersonId | string (UUID) | Required |
| CredentialId | string (UUID) | Required |

Per §2.5, this payload SHALL NEVER include `PasswordHash` or any
password value, plain or hashed. `CredentialId` identifies *which*
Credential record became active — it is an identity reference, not
secret material, consistent with the distinction 01_Domain_Model.md
§3 draws between `AccessTokenId` (an identity) and token content
(implementation-specific, and in that case client-facing) — here, by
contrast, `CredentialId` is deliberately never accompanied by its
underlying secret in any form.

---

# 5. Publishing Rules

## 5.1 Publish-After-Commit

An event SHALL only be published after the fact it describes has been
durably committed. For `PersonRegistered`, the Ready workflow change and
event enqueue are atomic; publication may occur later through the Outbox.
No event is published speculatively, optimistically, or before commit.

## 5.2 Failed Persistence Never Produces an Event

If a required state change fails to persist, no event describing that
(non-)change is published. A failed Core Ownership Transaction (rolled
back per ADR-0002 Decision 1) produces none of `PersonRegistered`,
`OrganizationCreated`, or `MembershipCreated`. After a successful
ownership commit, a failed Credential provision or a failed transition
to Ready does not yet produce `PersonRegistered`; Decision 8 recovery
must reach Ready first.

## 5.3 LoginFailed Describes a Completed Failure Rather Than a State Change

`LoginFailed` describes a completed failure without a committed state
change: no Aggregate state changes on a failed
authentication attempt (04_Commands §4.2 Postconditions: "Authentication
attempts do not modify: Person identity state, Credential state").
`LoginFailed` instead reports a completed *business fact of a
different kind* — "this authentication attempt was rejected" — which
is why it is still governed by the same immutability and audit rules
as every other event (§2.1, §2.2) even though §5.1's "state change"
framing does not literally apply to it. It is published once the
authentication decision itself (accept/reject) is finalized, not tied
to any Aggregate persistence.

## 5.4 Post-Commit Failures and Event Timing

Per ADR-0002 Decisions 1 and 8, a failed Credential provision or
initial Session creation does not invalidate the ownership commit.
`OrganizationCreated` and `MembershipCreated` still describe the
committed ownership facts. `PersonRegistered` is enqueued only when
Credential readiness is confirmed; a failed Credential provision
delays this event until recovery reaches Ready. Once Ready is committed,
an initial Session failure neither withdraws nor changes the event.

## 5.5 Delivery Mechanics Are Out of Scope

Whether publishing is at-least-once or exactly-once, whether retries
occur, and how a consumer deduplicates are Event Bus / Messaging
Engine concerns (00_Overview §4 lists messaging infrastructure as a
dependency of the Identity Platform, not a component the Identity
Platform itself implements) and are explicitly out of scope for this
document (§1.2).

---

# 6. Event Ordering

## 6.1 Per-Aggregate Ordering

Consumers SHALL apply unique events describing committed state transitions on the same Aggregate
instance in the order those transitions occurred (deduplicating EventId and handling redelivery as described in 09 §6.4)
— e.g. for a single Session:
`SessionCreated` always precedes that same Session's eventual
`SessionExpired` or `LogoutCompleted` (never the reverse).

`PersonRegistered` retains `AggregateType = Person` and
`AggregateId = PersonId` for identity and correlation, although Ready
is a registration-workflow transition. The proposed shared per-Person
registration/profile stream includes `PersonRegistered` and
`PersonUpdated` only (03_Aggregates.md §9.1 and 09_Persistence.md §6.4,
both Draft). This ordering guarantee depends on their durable stream
position and producer/delivery alignment. `AggregateType = Person`
or the presence of a resolved PersonId alone does not opt an event in:
audit-only `LoginFailed` and other authentication outcomes without a
Person state transition SHALL NOT acquire this stream position. Their
audit ordering is governed separately; no publish-order guarantee
relative to these registration/profile events is claimed here.

`OccurredAt` (§4.1) is expected to be consistent with an applicable
stream's order, but is **not itself the ordering mechanism**: two events on the same
Aggregate committed within the same transaction, or at timestamp
resolutions too coarse to distinguish, could carry equal or
non-monotonic `OccurredAt` values. The ordering guarantee comes from
a strict position in the applicable Aggregate or registration/profile
stream. The physical sequencer and delivery mechanism remain
implementation concerns (§1.2); `OccurredAt` does not enforce order.

## 6.2 Cross-Event Ordering Is Not Guaranteed Except Where Stated

No ordering is guaranteed between events on *different* Aggregate
instances unless explicitly stated below. In particular:

- `LoginSucceeded` and `SessionCreated` (same AuthenticatePerson call):
  **no publish-order guarantee**. A consumer needing both SHALL
  correlate them via the shared `SessionId`/`PersonId`, not via the
  order in which it happens to receive them.
- `PersonRegistered`, `OrganizationCreated`, `MembershipCreated`:
  **no publish-order guarantee among the three**. The ownership
  transaction precedes Ready, but delivery order need not follow
  occurrence order across their distinct Aggregate identities (§6.3).

## 6.3 Why Unordered Registration Events Are Safe

Per §2.3 (Events SHALL NOT coordinate initial ownership creation) and
ADR-0002 Decisions 1 and 8, the Core Ownership Transaction commits
Person + Organization + Membership atomically before these events can
be published. `PersonRegistered` additionally waits until Ready and may
be delayed by manual Credential completion. A consumer that receives
`OrganizationCreated` before `PersonRegistered` is not observing a
race condition or an inconsistent intermediate state — the Person and
Membership already exist, fully committed, regardless of which event
arrives first. Consumers may observe these two ownership events while
registration remains PendingCredential. If recovery never reaches Ready,
`PersonRegistered` is never emitted under this decision; ownership
events alone SHALL NOT be interpreted as evidence of an active
Credential or permission to authenticate. This distinguishes an event
*announcing* a fact from an event *coordinating* one (§2.3): ordering
would only matter if the events were themselves part of achieving
consistency, and per ADR-0002 Decision 1 they are not.

## 6.4 SessionExpired and LogoutCompleted Are Mutually Exclusive

Per the Session lifecycle (01_Domain_Model §5 — a Session transitions
to exactly one terminal state, `Expired` or `Closed`), at most one of
`SessionExpired` / `LogoutCompleted` SHALL ever be published for a
given `SessionId`. A consumer SHALL treat these as alternative,
not sequential, outcomes for the same Session instance.

---

# 7. Cross-Document Alignment

The ten-event names and producer ownership remain aligned with 059 and ADR-0002 Decision 5. 01/04 describe production points; 03 §9.1 and 09 §6.4 own workflow/stream persistence; 07 defines interoperability; 08 defines separate camelCase REST shapes. events.schema.json encodes all ten envelopes/payloads and omit-not-null behavior.

The registration/profile stream includes only PersonRegistered and PersonUpdated. Actor and execution context describe the actual Ready transition: an asynchronous reconciliation worker is System even when the winning Credential candidate originally came from a Person; candidate provenance is separate internal metadata.

# 8. MVP Readiness Checklist

- [x] Documentary alignment of Ready/ownership timestamps, optional Email and no initial SessionReference.
- [x] Optional Email in PersonUpdated; selected ContactType/ContactValue and RegistrationNotReady in restricted LoginFailed audit.
- [x] Workflow/stream and machine omission rules specified across 03, 07 and 09.
- [ ] Consumer compatibility/version migration review and architecture approval.
- [ ] Full 065 validation and runtime/security/event ordering tests in 13.

These are documentary completion marks only. The document remains DRAFT and ADR-0002 remains Proposed.

---

# 9. Change Log

## Version 1.2.0 (2026-09-24)

Aligned the complete proposed package, restricted LoginFailed contact audit, optional Email snapshots and event schema. Retained ten event names. Full validation and consumer review remain open.

## Version 1.1.0 (2026-09-24)

Proposed alignment with ADR-0002 Decisions 8–9. PersonRegistered now
records the Ready transition in OccurredAt and the earlier ownership
commit in its required OwnershipCommittedAt payload field. Email is
optional for mobile-only registration and SessionReference is absent;
publishing and ordering rules reflect delayed Credential readiness.
ActorIdentity and ExecutionContext now identify the Ready actor and
request; ownership events retain ownership-commit timestamps. The
workflow-derived ordering guarantee is scoped to the proposed
PersonRegistered/PersonUpdated stream, excluding audit-only LoginFailed;
it remains pending persistence and producer/delivery alignment.
Status is Draft until dependent Identity documents, contracts, consumers,
and structural validation are reconciled. No new event type is added.

## Version 1.0.2 (2026-07-14)

Architect-review refinement pass. Approved with minor non-blocking
comments; both addressed here.

- §6.1: reworded the per-Aggregate ordering guarantee so it no longer
  implies `OccurredAt` itself enforces ordering. Two events on the
  same Aggregate could share an `OccurredAt` value (same transaction,
  or coarse timestamp resolution); the actual guarantee is that
  consumers observe true occurrence order via whatever sequencing
  mechanism the Event Bus/store provides (out of scope, §1.2) —
  `OccurredAt` is expected to be consistent with that order, not the
  mechanism itself.
- §4.1: added an explicit note on why no `EventVersion`/`SchemaVersion`
  field exists in Version 1.0, and under what future condition
  (external/cross-platform consumers, non-additive payload evolution)
  it would likely become the first envelope addition.

No new Aggregates, Commands, Queries, or Events introduced. No MVP
scope changed.

## Version 1.0.1 (2026-07-14)

Review-driven correction pass.

- **Resolved the one flagged contradiction**: `AggregateId` is no
  longer unconditionally Required. It now explicitly follows the same
  `LoginFailed(PersonNotFound)` exception already established for
  `ActorIdentity` (§4.6) — absent when no Person can be resolved,
  since there is then no Aggregate instance to identify.
  `AggregateType` for `LoginFailed` is fixed to `Person` regardless of
  `Reason`, since a login attempt is conceptually always an operation
  against a Person, resolved or not.
- `CorrelationId` (§4.1.1) changed from unconditionally Optional to
  Required for every Person-initiated event, and Optional only for
  `System`-actor events (`SessionExpired`), closing an audit-trail gap.
- §4.1 now explicitly states `OccurredAt` is commit time, not publish
  time, and that no `PublishedAt` field is defined here — anticipating
  that Outbox-style delivery may introduce a commit/publish delay in a
  future Transport/delivery document without affecting this Contract.
- §4.10 `PersonUpdated` now carries a forward-compatibility note
  flagging that its full-snapshot payload is an MVP-appropriate choice
  that may need revisiting if Person's mutable attribute set grows.

No new Aggregates, Commands, Queries, or Events introduced. No MVP
scope changed.

## Version 1.0.0 (2026-07-14)

Initial Domain Events Blueprint.

- Defined the Common Event Envelope (§4.1), giving concrete shape to
  the five Event Audit Requirement fields named but not specified by
  01_Domain_Model.md
- Specified per-event Producer, ActorIdentity behavior,
  SessionReference applicability, and Payload schema for all 10 MVP
  events (§4.2–§4.11)
- Documented two intentional exceptions to the general envelope rule:
  `LoginFailed`'s optional `ActorIdentity` when the Person cannot be
  resolved (§4.6), and `SessionExpired`'s `System`-valued
  `ActorIdentity` for scheduled-job-triggered expiration (§4.8)
- Established Publishing Rules (§5), including the Post-Commit
  non-invalidation carry-through (§5.4) and `LoginFailed`'s status as
  the one event not tied to an Aggregate state change (§5.3)
- Established Event Ordering guarantees (§6): per-aggregate ordering
  (§6.1), explicit non-guarantees for `LoginSucceeded`/`SessionCreated`
  and the three registration events (§6.2), the architectural
  rationale for why unordered registration events remain safe (§6.3),
  and the mutual exclusivity of `SessionExpired`/`LogoutCompleted`
  (§6.4)
- Verified full alignment against 059, 01_Domain_Model, 04_Commands,
  14_MVP, and ADR-0002 (§7)
- Explicitly excluded Event Bus, Outbox, and Integration Event
  mechanics from scope (§1.2), per this Blueprint's stated intent to
  define only the Domain Event Contract

---

**END OF DOCUMENT**

## Integrated validation note (v1.2.0)

LoginFailed is a Security Event per ADR-0002 Decision 5; its resolved PersonId identifies the target, not authenticated actor proof. ContactValue/ExecutionContext subscriptions and retention are restricted under 11_Security. The service/stream definitions are now documented in 07 §3 and 09 §6.4; implementation tests remain unexecuted. Historical baseline checklist claims do not establish current readiness. Full acceptance is tracked in 12_Validation.

## Accepted ADR-0004 propagation (v1.3.0)

Ready's local transaction also persists ReadyFactId/winner evidence and internal acknowledgment Outbox; these do not add fields to public event payloads or an eleventh event. Administrative recovery executes through the service worker with ActorIdentity=System; restricted append-only audit separately retains the initiating operator and correlation to ReadyFactId/EventId. It must not impersonate the Person or copy the original registration IP/device. Re-drive preserves the original event identity and timestamps.

Ready acknowledgment and administrative audit are internal service/journal records, not public Identity events. T16 (the two-event Person stream) is still Proposed and cannot inherit acceptance from ADR-0004. Public event schemas remain v1.2.0 because this propagation changes neither payload shape nor catalog.
