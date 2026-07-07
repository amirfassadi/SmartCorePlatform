# SmartCore Runtime Model
Version: 1.0

Status: Core Runtime Specification

---

# 1. Purpose

This document defines the **Runtime Model of SmartCore**.

It explains how semantic definitions (Core + Domain) are executed in a real system.

Runtime is NOT a business layer.
Runtime is NOT a domain layer.

Runtime is a **semantic execution interpreter**.

---

# 2. Fundamental Principle

> Runtime does not understand business meaning.
> Runtime only understands structured intent.

Meaning is defined in:

Core + Domain

Execution is handled in:

Runtime + Infrastructure

---

# 3. Runtime Input Model

Runtime receives only one type of input:

## Semantic Intent

A structured representation of:

- Event
- Command
- Query
- Rule Trigger
- Workflow Step

Example:

```
PaymentOccurred
{
  paymentId: 123,
  amount: 500,
  currency: EUR,
  timestamp: T1
}
```

---

# 4. Core Runtime Entities

Runtime operates on 5 fundamental constructs:

---

## 4.1 Command

> A request to perform an action

Characteristics:

- imperative
- may fail
- may trigger side effects
- NOT guaranteed to succeed

Examples:

- PayInvoice
- ApproveContract
- ReserveRoom
- CreateUser

Flow:

Command → Validation → Execution → Event(s)

---

## 4.2 Query

> A request for information

Characteristics:

- read-only
- no side effects
- deterministic

Examples:

- GetInvoiceStatus
- FetchUserProfile
- ListReservations

Flow:

Query → Resolver → Response

---

## 4.3 Event

> A fact that something happened

Characteristics:

- immutable
- time-stamped
- persisted
- broadcastable

Examples:

- PaymentCompleted
- DoorOpened
- ContractSigned

Flow:

Event → Persistence → Subscription → Reactions

---

## 4.4 Process

> A long-running coordination of multiple events

Characteristics:

- stateful in runtime
- spans multiple events
- orchestrates domain behavior

Examples:

- Purchase Process
- Onboarding Process
- Refund Process

Flow:

Event → Process Engine → Next Steps

---

## 4.5 Job

> A scheduled or background execution unit

Characteristics:

- time-based or event-based trigger
- retryable
- isolated execution

Examples:

- SendInvoiceReminder
- RetryPayment
- SyncInventory

Flow:

Trigger → Job Execution → Event

---

# 5. Runtime Execution Loop

Runtime follows this universal loop:

```
INPUT (Command / Event / Job / Query)
        ↓
Normalization
        ↓
Routing
        ↓
Execution Engine
        ↓
Side Effects
        ↓
Event Emission
        ↓
Persistence
```

---

# 6. Execution vs Meaning Separation

Runtime does NOT interpret meaning.

Example:

Semantic Layer:
```
Employment = Person + Organization + Rule + Time
```

Runtime:
```
"EmploymentCreated" event triggers workflow
```

Runtime does NOT know what employment is.

It only reacts to structured events.

---

# 7. Event Lifecycle in Runtime

Event lifecycle:

1. Received
2. Validated
3. Stored
4. Published
5. Subscribed
6. Reacted to
7. Possibly triggers new Commands/Events

Events are the backbone of Runtime.

---

# 8. Process Model (Saga-based)

Processes are implemented as:

Stateful event-driven workflows

Example:

Purchase Process:

```
PaymentRequested
   ↓
PaymentConfirmed
   ↓
InventoryReserved
   ↓
InvoiceGenerated
   ↓
OrderCompleted
```

Each step:

- triggered by Event
- may emit Commands
- may wait for external input

---

# 9. Command vs Event Rule

| Type | Direction | Meaning |
|------|----------|--------|
| Command | Future intent | "Do this" |
| Event | Past fact | "This happened" |

Command can fail.

Event cannot fail (it already happened).

---

# 10. Query Model

Query system is:

- independent from event system
- optimized for read models
- derived from events (CQRS)

Example:

```
Event stream → Projection → Query model
```

---

# 11. Runtime State Management

Runtime maintains state only for:

- Processes
- Jobs
- Workflow instances

Runtime does NOT store business state directly.

Business state is derived from Events.

---

# 12. Retry & Failure Handling

Runtime handles:

- retry logic
- idempotency
- compensation actions
- dead-letter queues

But NEVER modifies semantic meaning of events.

---

# 13. Integration Boundary

Runtime integrates with:

- APIs
- Message brokers
- Databases
- External services

All integrations are adapters.

---

# 14. Event Emission Rule

Every successful command MUST emit at least one event.

Example:

```
PayInvoice → InvoicePaidEvent
```

If no event is emitted:

→ execution is invalid

---

# 15. Determinism Rule

- Commands may be non-deterministic externally
- Events must always be deterministic once created
- Queries must always be deterministic

---

# 16. Idempotency Rule

Runtime guarantees:

- Commands may be retried safely
- Events must not be duplicated
- Jobs must be idempotent

---

# 17. Runtime vs Domain Separation

| Layer | Responsibility |
|------|---------------|
| Domain | Meaning |
| Runtime | Execution |
| Infrastructure | Transport |

Runtime is NOT allowed to:

- define business rules
- define ontology
- define vocabulary

---

# 18. Core Principle

> Runtime is a semantic execution interpreter, not a business brain.

It executes structure, not meaning.

---

# 19. Final Model

```
User Intent
    ↓
Command / Event
    ↓
Runtime Engine
    ↓
Process / Job / Handler
    ↓
Infrastructure
    ↓
New Events
    ↓
State Projections (Query Layer)
```

---

## END OF DOCUMENT