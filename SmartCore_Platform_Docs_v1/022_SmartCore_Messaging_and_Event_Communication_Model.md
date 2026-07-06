# SmartCore Platform

## Document 022 — Messaging & Event Communication Model

Version: 1.0
Status: Core Architecture Specification

---

# 1. Purpose

This document defines how semantic information flows between different
parts of the SmartCore platform.

It specifies the communication model independently of any transport
technology.

This document does not define:

- Kafka
- RabbitMQ
- NATS
- MQTT
- HTTP
- gRPC

Those belong to the implementation layer.

---

# 2. Core Principle

> Components never communicate directly.

They communicate only through semantic messages.

---

# 3. Communication Model

SmartCore defines three communication semantic patterns.

```
Command

↓

Event

↓

Query
```

Each has a completely different semantic meaning.

---

# 4. Command

A Command represents an intention.

It asks the system to perform an action.

Characteristics:

- has one intended receiver
- may be accepted
- may be rejected
- does not describe reality
- requests a state transition

Examples

Create Contract

Approve Invoice

Reserve Room

Start Machine

Grant Permission

---

# 5. Event

An Event represents something that has already happened.

Characteristics

- immutable
- historical
- factual
- broadcastable
- cannot be rejected

Examples

Contract Created

Invoice Approved

Room Reserved

Payment Completed

Door Opened

Temperature Changed

---

# 6. Query

A Query requests information.

Characteristics

- read only
- does not modify semantic state
- produces no Event by itself
- may be cached

Examples

Get Balance

Get Active Contracts

Get Employee List

Get Building Status

---

# 7. Communication Rule

The communication flow is always

```
Command

↓

Validation

↓

Event

↓

Projection

↓

Query
```

Commands create Events.

Queries never create Events.

---

# 8. Event Publication

Every successful semantic change produces an Event.

```
Semantic Change

↓

Event

↓

Publication
```

No silent state mutation is allowed.

---

# 9. Event Subscription

Components never subscribe to internal state.

They subscribe only to Events.

This guarantees loose coupling.

---

# 10. Event Immutability

Once published

an Event

must never change.

If correction is needed

another Event must be emitted.

Example

PaymentCompleted

↓

PaymentReversed

---

# 11. Ordering

Ordering is guaranteed only inside a semantic stream.

Example

Contract Stream

ContractCreated

↓

ContractActivated

↓

ContractTerminated

No global ordering is required.

---

# 12. Delivery Principle

The Core defines only semantic delivery.

It does not require

- at most once
- at least once
- exactly once

These are transport concerns.

Core only requires:

```
Eventually every valid Event becomes observable.
```

---

# 13. Message Identity

Every message has:

- Message Identity
- Semantic Type
- Producer
- Creation Time
- Correlation Reference (optional)
- Causation Reference (optional)

Identity never changes.

---

# 14. Correlation

Correlation links multiple messages that belong to the same business process.

Example

Reservation Requested

↓

Payment Requested

↓

Payment Completed

↓

Reservation Confirmed

All share one Correlation Identity.

---

# 15. Causation

Every Event may reference its direct cause.

Example

ApproveInvoice Command

↓

InvoiceApproved Event

↓

PaymentRequested Event

↓

PaymentCompleted Event

Causation builds the semantic execution graph.

---

# 16. Message Reliability

SmartCore assumes

messages may

- arrive late
- arrive twice
- arrive out of order

Correctness must never depend on transport guarantees.

Correctness depends on semantic reconstruction.

---

# 17. Communication Boundary

Communication always occurs across bounded contexts.

No context may directly modify another context's internal model.

Only semantic messages may cross boundaries.

---

# 18. External Systems

External systems communicate exactly like internal systems.

Examples

ERP

Payment Gateway

IoT Platform

Government API

AI Service

All are simply message producers and consumers.

No special semantic treatment exists.

---

# 19. Relationship to Previous Documents

015 Runtime

↓

016 Deployment

↓

017 Failure

↓

018 Security

↓

019 Identity

↓

020 Time

↓

021 Economic Model

↓

022 Messaging

Messaging becomes the semantic nervous system of SmartCore.

---

# 20. Key Insight

Commands express intention.

Events express facts.

Queries express information needs.

The platform communicates through facts,
not through shared state.

---

# End of Document 022