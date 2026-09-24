# 026_SmartCore_Event_Model.md

# SmartCore Event Model

Version: 1.1.1
Status: Draft
Layer: Core

Related Decision: ADR-0002_Identity_Foundation_Clarifications.md v1.4, Decision 5
(Proposed). The LoginFailed-specific clarifications below record that pending
ADR; they do not constitute full ADR acceptance or generation clearance.

---

# 1. Purpose

This document defines the SmartCore Event Model.

Events represent facts that have occurred in the system.

Events are immutable.

They describe **what happened**, never **what should happen**.

The Event Model is the foundation for:

- Audit
- Automation
- Ledger
- Notifications
- Analytics
- Workflow
- Integration
- AI
- Event Sourcing (optional)

---

# 2. Fundamental Principle

An Event represents a completed fact.

Examples:

✔ Payment Completed

✔ Contract Activated

✔ Employee Hired

✔ Door Opened

✘ Create Payment

✘ Activate Contract

The latter are Commands.

---

# 3. Event Characteristics

Every Event is:

- immutable
- timestamped
- uniquely identified
- traceable
- replayable
- observable

An Event can never be modified.

Corrections are represented by new Events.

---

# 4. Event vs Command

Command

```
Activate Contract
```

↓

Event

```
Contract Activated
```

Commands express intent.

Events express facts.

---

# 5. Event Lifecycle

```
Command
      ↓
Validation
      ↓
Business Rules
      ↓
State Change
      ↓
Event Emitted
```

Domain Events in this lifecycle are emitted only after successful execution.
LoginFailed is the specifically classified Security Event described by
ADR-0002 Decision 5: it records a completed failed-authentication outcome and
therefore does not require a successful authentication Command or business-state
commit. This clarification does not authorize Domain Events for failed Commands.

---

# 6. Event Structure

Every Event contains:

```
EventId

EventType

OccurredAt

CorrelationId

CausationId

AggregateId

ActorId

TenantId

Payload

Metadata

Version
```

---

For LoginFailed, the generic structure above does not require a fabricated
AggregateId, ActorId, or TenantId when authentication cannot resolve the relevant
identity/context. The existing Identity Blueprint envelope and conditional
reference rules define its concrete contract; this clarification changes no
wire field or nullability rule.

# 7. Event Identity

Each Event has a globally unique identifier.

Example

```
evt_01HX...
```

Identity never changes.

---

# 8. Event Time

Every Event has:

```
OccurredAt
```

Optional:

```
RecordedAt

ProcessedAt
```

OccurredAt represents business reality.

---

# 9. Event Categories

SmartCore defines four Event families.

## Domain Events

Business facts.

Examples:

```
PaymentCompleted

ContractSigned

EmploymentStarted
```

---

## System Events

Infrastructure events.

Examples:

```
CacheRefreshed

IndexBuilt

JobCompleted
```

---

## Integration Events

Published to external systems.

Examples:

```
WebhookDelivered

ERPExportCompleted
```

---

## Security Events

Authentication and authorization.

LoginFailed is an Identity-owned Security Event used for audit, per
ADR-0002 Decision 5. Its required Identity MVP publication records an unsuccessful
authentication attempt without asserting a successful Domain state change.
Its unchanged name and ownership do not make it a Domain Event.

Examples:

```
UserLoggedIn

PermissionGranted

RoleRevoked
```

---

# 10. Event Naming

Events use past tense.

Good

```
PaymentCompleted

PersonRegistered

DoorOpened

AssetTransferred
```

Avoid

```
CompletePayment

OpenDoor

RegisterPerson
```

---

# 11. Event Ordering

Ordering is guaranteed only inside one Aggregate.

Never assume global ordering.

---

# 12. Event Immutability

Events cannot be updated.

Never:

```
UPDATE Event
```

Instead:

```
PaymentCorrected

PaymentCancelled

PaymentReversed
```

---

# 13. Event Replay

Events may be replayed.

Replay must produce identical business meaning.

Replay must never duplicate side effects.

---

# 14. Event Versioning

Events evolve.

Rules:

- never remove fields
- add optional fields
- preserve compatibility

Breaking changes require new Event type.

---

# 15. Correlation

CorrelationId connects multiple Events.

Example

```
Create Contract

↓

ContractCreated

↓

PaymentCreated

↓

InvoiceGenerated

↓

NotificationSent
```

All share one CorrelationId.

---

# 16. Causation

Each Event records its immediate cause.

```
PaymentCompleted

↓

InvoiceGenerated

↓

RewardGranted
```

InvoiceGenerated stores

```
CausationId = PaymentCompleted
```

---

# 17. Aggregate Boundary

Every Domain Event belongs to exactly one Aggregate.
For the LoginFailed Security Event, identity resolution may fail before any
Aggregate instance is available. The existing conditional identity-reference
rules apply; no Aggregate is created solely to satisfy an event reference.
This revision does not redefine aggregate associations of other event families.

Examples

```
Person

Contract

Payment

Organization

Device
```

---

# 18. Event Metadata

Metadata is optional.

Examples

```
IP Address

User Agent

Region

Source System

SDK Version
```

Metadata never changes business meaning.

---

# 19. Event Payload

Payload contains business data.

Example

```
PaymentCompleted

Amount

Currency

Payer

Payee
```

Payload should be minimal.

Do not duplicate entity state.

---

# 20. Event Publishing

Domain Events are published after transaction success, never before.
LoginFailed publication follows the completed failed-authentication outcome;
it does not wait for a successful authentication transaction or Session creation.
This classification does not prescribe a different transport, topic, or delivery
guarantee for the existing event.

Publication failures must not invalidate committed business state.

Reliable delivery is handled by the Outbox Pattern or equivalent mechanisms.

---

# 21. Event Consumers

Consumers include:

- Automation Engine
- Notification Service
- Ledger
- Reporting
- AI
- External Integrations

Consumers must be independent.

---

# 22. Idempotent Consumption

Consumers must tolerate duplicate delivery.

Processing the same Event multiple times must not produce inconsistent state.

---

# 23. Event Retention

Business Events are retained according to retention policies.

Critical financial Events should be retained indefinitely unless legal requirements dictate otherwise.

---

# 24. Event Security

Events may contain sensitive data.

Support:

- encryption
- masking
- access control
- audit logging

---

# 25. Event Store

SmartCore does not require Event Sourcing.

Events may be stored in:

- relational databases
- event stores
- message brokers
- append-only logs

Storage technology is an implementation decision.

---

# 26. Event Sourcing

Event Sourcing is optional.

If enabled:

Current state is reconstructed from Events.

If disabled:

Events remain an immutable audit trail.

Business semantics remain identical.

---

# 27. Event Driven Architecture

SmartCore is Event-Driven by design.

Business capabilities communicate through Events whenever practical.

Direct synchronous coupling should be minimized.

---

# 28. Testing

Every Event should be testable.

Validation includes:

- payload correctness
- ordering
- replay safety
- idempotency
- version compatibility

---

# 29. Design Checklist

Before introducing a new Event verify:

✓ Represents a completed fact

✓ Uses past-tense naming

✓ Immutable

✓ Domain Event belongs to one Aggregate; LoginFailed uses the conditional references described in §17

✓ Contains minimal payload

✓ Versioned

✓ Replay-safe

✓ Idempotent for consumers

✓ Business meaningful

---

# Summary

Events are immutable facts that describe what has happened in SmartCore.

They form the foundation of auditability, automation, integrations, analytics, workflows, and optional Event Sourcing while remaining independent of implementation technology.

Commands express intent.

Events preserve truth.


# Change Log

## Version 1.1.1 (2026-09-24)

- Updated the reference to the current Proposed ADR-0002 v1.4; Decision 5 classification and all event rules remain unchanged.

## Version 1.1 (2026-09-24)

- Synchronized LoginFailed classification with ADR-0002 v1.3 Decision 5.
- Clarified the Domain Event scope of successful execution/commit requirements and the existing conditional identity references for LoginFailed.
- Retained Draft status, the four existing event families, and the semantic definition of an Event. Other event families are not reclassified by this revision.
