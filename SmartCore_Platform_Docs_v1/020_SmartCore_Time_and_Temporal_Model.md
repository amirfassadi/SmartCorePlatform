# SmartCore Platform

## Document 020 — Time & Temporal Model

Version: 1.0
Status: Core Architecture Spec

---

# 1. Purpose

این سند تعریف می‌کند:

- Time در SmartCore چیست
- چگونه Eventها زمان‌دار می‌شوند
- تفاوت Time در Semantic Layer و Execution Layer
- چرا Time یک Semantic Construct فیزیکی نیست، بلکه یک "Semantic Overlay" است

---

# 2. Core Principle

> Time does not exist in the model.
> Time is a constraint on ordering of Events.

---

# 3. Fundamental Insight

SmartCore does NOT model “time as a thing”.

Instead:

```
Time := ordering constraint over Occurrents (Events)
``` id="t1"

یعنی:

- ما “زمان” نداریم
- ما فقط “ترتیب وقوع” داریم

---

# 4. Event Ordering Model

Every Event has:

- causal order
- logical order
- optional physical timestamp

But only one is authoritative:

```
Event Order > Wall Clock Time
``` id="t2"

---

# 5. Types of Time

SmartCore distinguishes three temporal concepts:

## 5.1 Logical Time (Primary)

- defines ordering
- deterministic
- derived from Event graph

Example:

PaymentCreated → PaymentAuthorized → PaymentCaptured

---

## 5.2 Physical Time (Secondary)

- timestamp from external world
- non-authoritative
- used for audit only

Example:

2026-07-04 18:32:10

---

## 5.3 Valid Time (Semantic Time)

- time during which a Relation is valid
- used in Contracts, Ownership, Permissions

Example:

```
owns(A, B, valid_from → valid_to)
``` id="t3"

---

# 6. Time is NOT a Core Semantic Construct Entity

Time is NOT:

- Thing
- Event
- Relation
- Rule

Time is:

> a dimension attached to all Semantic constructs

---

# 7. Temporal Attachment Rule

All Semantic constructs may carry time metadata:

- Event → occurrence time
- Relation → validity interval
- Rule → activation interval
- Identity → lifetime (conceptual)

---

# 8. Time vs Event Dependency

Important rule:

> Events define time, not vice versa.

We do NOT say:

- "Event happened at time T"

Instead:

- "Time T exists because Event ordering defines it"

---

# 9. Event Time Model

Each Event has:

```
Event {
    causal_parent_events
    logical_position
    optional physical_timestamp
}
``` id="t4"

But execution correctness depends only on:

- causal graph
- ordering constraints

---

# 10. Temporal Consistency

A system state is valid if:

```
∀ Events:
    causal_order is preserved
``` id="t5"

Not:

- wall clock consistency
- distributed clock sync

---

# 11. Time Travel Principle

SmartCore allows:

- replay
- rollback
- reconstruction

Because:

> Time is not stored — it is reconstructed.

---

# 12. Temporal Rebuild Model

System state is derived via:

```
State = Fold(EventStream)
``` id="t6"

Time is a side effect of reconstruction.

---

# 13. Time in Contracts

Contract uses:

- valid_from
- valid_to
- execution_time

But:

Contract does NOT “live in time”

Contract defines time boundaries for Events.

---

# 14. Time in Identity

Identity has:

- conceptual lifetime
- not a temporal object

Identity does NOT expire
Sessions do.

---

# 15. Time in Rules

Rules may have:

- activation time
- expiration time

But rules are still semantic constraints, not temporal entities.

---

# 16. Clock Independence Principle

SmartCore must function without:

- synchronized clocks
- global time source
- external time authority

Because:

> Time is emergent from Event structure

---

# 17. Distributed Systems Implication

In distributed systems:

- clocks are unreliable
- ordering is partial

So SmartCore relies on:

```
Causal Ordering (not Clock Ordering)
``` id="t7"

---

# 18. Failure & Time

If time is inconsistent:

- Events are still valid
- ordering is repaired via replay
- no semantic corruption occurs

---

# 19. Relationship to Previous Documents

- 017 Failure Model → recovery uses Event ordering
- 018 Security → authorization is time-dependent
- 019 Identity → identity persists across temporal reconstruction

---

# 20. Key Insight

> Time is not a dimension of reality in SmartCore.
> Time is a reconstruction of Event causality.

---

End of Document 020