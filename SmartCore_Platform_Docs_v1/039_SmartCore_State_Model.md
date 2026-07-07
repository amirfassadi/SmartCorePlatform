# SmartCore State Model
Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the semantic meaning of State within SmartCore.

The purpose of this document is to distinguish State from:

- Thing
- Relation
- Event
- Rule
- Time

and establish State as a derived semantic construct rather than a foundational semantic construct.

This specification is technology-independent.

---

# 2. Definition

A State represents the condition of a Thing or Relation at a specific point in Time.

A State does not describe what happened.

A State describes what is currently true.

Examples

Door = Open

Contract = Active

Payment = Completed

Battery = 82%

Machine = Running

---

# 3. Core Principle

State is a semantic projection.

It is never an independent source of truth.

---

# 4. State Derivation

State is derived from:

- Events
- Relations
- Rules
- Time

Conceptually:

State =
Projection(
Events,
Relations,
Rules,
Time
)

State never exists without semantic history.

---

# 5. State vs Event

Event answers:

"What happened?"

Examples

DoorOpened

PaymentCompleted

ContractSigned

State answers:

"What is true now?"

Examples

Door = Open

Payment = Completed

Contract = Active

Events generate State.

State never generates Events.

---

# 6. State vs Relation

Relations describe semantic connections.

Example

Person employedBy Organization

State describes the current condition of that Relation.

Example

Employment = Suspended

Relation identity remains unchanged.

State changes over time.

---

# 7. State vs Thing

Things persist.

States vary.

Example

Thing:

Door

State:

Open

Closed

Locked

Maintenance

The Thing remains the same.

Only its State changes.

---

# 8. State vs Rule

Rules define valid States.

Rules never become States.

Example

Rule

Contract cannot become Active before Signature.

State

Contract = Active

Rules constrain State.

They do not create it.

---

# 9. Time Dependency

Every State exists only relative to Time.

Example

Door

08:00 Closed

08:03 Open

08:15 Locked

Without Time,

State has no meaning.

---

# 10. State Identity

States do not require independent identity.

The identity belongs to the Thing.

Examples

Door #42

State = Open

Later

State = Closed

The identity never changes.

The projected State changes.

---

# 11. Mutable Nature

States are mutable.

Events are immutable.

Example

Payment

Pending

Authorized

Completed

Refunded

Each State transition is caused by one or more Events.

---

# 12. State Transition

A State Transition is NOT a core semantic construct.

A State Transition is the semantic interpretation of Events.

Example

Event

ContractActivated

↓

Projection

Draft → Active

---

# 13. State Categories

Domains may define States.

Examples

Lifecycle States

Draft

Active

Closed

Operational States

Running

Stopped

Fault

Availability States

Online

Offline

Maintenance

Business States

Pending

Approved

Rejected

The Core defines no fixed State vocabulary.

---

# 14. State Persistence

SmartCore does not require State persistence.

Possible implementations:

Current State Table

Projection Cache

Materialized View

Runtime Memory

State Store

Event Projection

All are implementation choices.

---

# 15. Historical State

Historical States may be reconstructed.

Example

"What was Contract #25 state last Monday?"

Projection:

Events
+
Time

↓

Historical State

---

# 16. State Consistency

A valid State must never contradict:

Event history

Active Relations

Rules

Time constraints

---

# 17. State Completeness

A State should represent only observable facts.

Derived calculations belong elsewhere.

Example

Door

Open

Correct

Door

Likely Open

Not a State

That is an inference.

---

# 18. Unknown State

Unknown is a valid State.

Example

Sensor disconnected.

Temperature = Unknown.

Unknown is different from:

Null

Missing

Undefined

---

# 19. State Granularity

Different domains may expose different State detail.

Example

Vehicle

Simple

Running

Stopped

Detailed

Running

Idle

Charging

Maintenance

Emergency

The semantic model permits multiple levels of granularity.

---

# 20. Snapshot Principle

A State is always a snapshot.

Snapshots do not replace history.

History is preserved through Events.

---

# 21. Projection Principle

Multiple projections may exist.

Example

Financial State

Operational State

Maintenance State

Customer State

Each projection observes the same semantic reality from a different viewpoint.

---

# 22. Architectural Principles

State belongs to the Semantic Layer.

State is:

Derived

Mutable

Observable

Time-dependent

Technology-independent

---

# 23. Validation Checklist

Before introducing a new State ask:

Does it describe the current condition?

Can it change over Time?

Is it derived from Events or Relations?

Is it independent from implementation?

If the answer is yes,

it belongs in the State Model.

---

# 24. Final Principle

State is a semantic projection of reality at a specific point in Time.

Events preserve history.

Relations preserve structure.

Rules preserve correctness.

State preserves the current view.

None of them replace one another.

---

## END OF DOCUMENT