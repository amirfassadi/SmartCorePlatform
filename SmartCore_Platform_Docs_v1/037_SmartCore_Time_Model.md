# SmartCore Time Model
Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the Time model in SmartCore.

Time is a dimensional overlay that applies across all semantic constructs:

- Events
- Relations
- States
- Rules
- Processes

Time is NOT a domain concept.

Time is NOT a business concept.

Time is a universal semantic dimension.

---

# 2. Definition

Time is a semantic ordering and validity dimension that allows SmartCore to:

- order Events
- define validity windows for Relations
- constrain Rules temporally
- interpret State evolution
- manage lifecycle transitions

Time does not exist as an entity in the domain.

Time exists as a **semantic overlay**.

---

# 3. Core Principle

> Time does not change meaning.
> Time organizes meaning.

---

# 4. Types of Time

SmartCore defines multiple independent time dimensions:

---

## 4.1 Occurrence Time (Event Time)

The time at which an Event actually happened.

Example:

PaymentCompleted.occurredAt = T1

DoorOpened.occurredAt = T2

This is immutable.

---

## 4.2 Recording Time (System Time)

The time at which the system recorded the Event.

Example:

Event happened at T1
System recorded at T2

T1 ≠ T2 is valid.

---

## 4.3 Validity Time (Business Time)

The time during which a Relation or State is considered valid.

Example:

Employment:

start = 2020
end = 2025

Validity is semantic, not technical.

---

## 4.4 Processing Time (Runtime Time)

The time at which Runtime processes Events.

Used for:

- ordering
- retries
- scheduling
- execution

Processing Time does NOT affect semantics.

---

# 5. Time vs Event

Events are anchored in Occurrence Time.

Each Event MUST have:

OccurredAt

Example:

PaymentCompleted @ 10:05:32

Time does not modify Event meaning.

---

# 6. Time vs Relation

Relations may span time intervals.

Example:

Employment(Person, Organization)

Valid:

2020 → 2025

Relations are not instantaneous by default.

They exist across Time intervals.

---

# 7. Time vs State

State is a snapshot at a given Time.

Example:

DoorState @ T3 = Open

State = function(Event history, Time)

State is derived from Events over Time.

---

# 8. Time vs Rule

Rules may depend on Time dimensions.

Examples:

- Contract expires after 1 year
- Access allowed only between 08:00–18:00
- Payment must occur before DueDate

Rules interpret Time but do not control it.

---

# 9. Temporal Dimensions Separation

SmartCore separates Time into orthogonal axes:

| Dimension | Purpose |
|----------|--------|
| Occurrence | reality of events |
| Recording | system logging |
| Validity | business meaning |
| Processing | runtime execution |

These must NEVER be conflated.

---

# 10. Temporal Identity Principle

An Event identity is independent of Time representation.

Changing timestamps does NOT change the Event.

Example:

PaymentCompleted(EVT-123)

Still same Event even if:

- reprocessed
- replayed
- migrated

---

# 11. Temporal Consistency Rule

A valid SmartCore model must ensure:

- Events have consistent ordering
- Relations do not violate validity intervals
- States do not contradict Event history
- Rules respect temporal constraints

---

# 12. Time Granularity

Time may be represented at multiple levels:

- milliseconds
- seconds
- minutes
- business days
- fiscal periods

Granularity is domain-specific.

Core does NOT enforce resolution.

---

# 13. Time Reversibility

Events are NOT reversible in time.

You cannot "undo" Time.

You can only create new Events:

Example:

PaymentCompleted
→ PaymentReversed

History remains intact.

---

# 14. Time as a Dimension, Not a Type

Time is NOT:

- a Thing
- a Relation
- an Event

Time is a **dimension applied to all constructs**.

---

# 15. Temporal Projection Model

All current State is derived from:

Event Stream × Time Window → State Projection

This enables:

- CQRS
- Event Sourcing
- Historical queries

But these are implementation strategies.

Not semantic requirements.

---

# 16. Causality vs Time

Time ordering ≠ Causality

Example:

Event A occurred before Event B
BUT
Event B may not be caused by Event A

SmartCore distinguishes:

- temporal order
- causal dependency

---

# 17. Temporal Rules Engine

Rules may evaluate:

- past
- present
- future constraints

Examples:

- Future validity checks
- Expiry conditions
- Scheduling constraints

---

# 18. Time Integrity Constraints

System must ensure:

- No impossible intervals (end < start)
- No overlapping exclusive relations
- No invalid temporal transitions

---

# 19. Time in Distributed Systems

Clock skew is NOT a semantic problem.

SmartCore relies on:

- logical ordering
- causal ordering
- event IDs

Not physical clock accuracy.

---

# 20. Architectural Principle

Time is a universal semantic overlay.

It applies equally to:

- Events
- Relations
- States
- Rules

But never defines them.

---

# 21. Final Principle

Time organizes reality in SmartCore but never defines reality itself.

Meaning exists without Time.

But execution and interpretation require Time.

---

## END OF DOCUMENT