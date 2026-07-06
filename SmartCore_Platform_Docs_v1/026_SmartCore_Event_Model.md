# 026_SmartCore_Event_Model.md

# SmartCore Event Model

Version: 1.0
Status: Draft
Layer: Core

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

Events are emitted only after successful execution.

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

Every Event belongs to exactly one Aggregate.

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

Events are published after transaction success.

Never before.

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

✓ Belongs to one Aggregate

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
