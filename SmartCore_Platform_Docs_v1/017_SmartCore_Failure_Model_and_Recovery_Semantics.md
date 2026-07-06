# SmartCore Platform
## Document 017 — Failure Model & Recovery Semantics

Version: 1.0
Status: Core Architecture Spec

---

## 1. Purpose

این سند تعریف می‌کند سیستم SmartCore در مواجهه با خطا چگونه رفتار می‌کند و چگونه از آن بازیابی می‌شود
بدون اینکه Semantic Model یا Ledger دچار corruption شود.

---

## 2. Core Principle

> Failure is not an exception — it is a first-class event.

در SmartCore:

- هیچ خطایی "ناپدید" نمی‌شود
- هیچ state‌ای "گم" نمی‌شود
- هیچ executionی "نیمه‌کاره" نمی‌ماند بدون ثبت

---

## 3. Failure Ontology

Failure خودش یک Event است:
FailureEvent := Occurrent

Types of Failure Events:

- NodeFailure
- ExecutionFailure
- RuleViolationFailure
- EventReplayFailure
- ConsistencyFailure

---

## 4. Failure Scope Model

هر Failure همیشه scope دارد:
FailureScope:
- Single Event
- Contract Execution
- Tenant Session
- Node
- Cluster

Rule:

> Failure cannot exceed its causality boundary.

---

## 5. Deterministic Recovery Principle

> If the Event Log is intact, the system is always recoverable.

Recovery does NOT depend on:

- memory
- runtime state
- cache
- node status

Only depends on:

- Event Store

---

## 6. Recovery Strategy

### 6.1 Stateless Recovery
Rebuild State = Replay(Event Stream)

Any node can rebuild any state at any time.

---

### 6.2 Partial Failure Recovery

If execution fails mid-process:
Event committed? → yes → continue
Event not committed? → discard execution result

No partial mutation allowed.

---

### 6.3 Replay Recovery

If corruption detected:
Stop Execution Node
Fetch Event Stream
Replay deterministically
Replace corrupted projection

---

## 7. Idempotency Rule

> Every Event Handler must be idempotent.

Meaning:

- Same Event replayed → same result
- No side-effect duplication

---

## 8. Split Brain Prevention

Distributed nodes may diverge temporarily

Solution:

- Event Store is single source of truth
- Conflicts resolved by:
Event Ordering (global or partition-level)

No node has authority over truth.

---

## 9. Consistency Recovery Model

### 9.1 Eventual Convergence

All nodes converge via replay.

### 9.2 Contract-Level Consistency

Strong consistency only guaranteed inside:

- single Contract
- single Event partition

---

## 10. Compensation Model (Undo ≠ Delete)

SmartCore does NOT delete events.

Instead:
CompensatingEvent := Occurrent that negates previous Event

Example:

- PaymentCompleted
- PaymentReversed

---

## 11. Failure Propagation Rules

Failure does NOT propagate randomly.

It follows causal graph:
Event → Derived Event → Side Effect Event

Only downstream causal events are affected.

---

## 12. Observability of Failure

Every failure is observable as:

- FailureEvent
- Log Event
- Compensation Event (if recovery occurs)

No silent failure allowed.

---

## 13. Node Failure Handling

If node fails:

- Event processing stops
- No data is lost
- Another node resumes via partition takeover

---

## 14. Time and Failure

Time does NOT affect correctness.

Only ordering matters:
Event Order > Wall Clock Time

---

## 15. Key Insight

SmartCore does NOT “recover from failure”.

It simply:

> Reconstructs reality from immutable history.

---

## 16. Relationship to Previous Documents

- 015 Runtime → defines execution model
- 016 Deployment → distributes execution
- 017 Failure Model → ensures correctness under breakdown

---

## End of Document 017