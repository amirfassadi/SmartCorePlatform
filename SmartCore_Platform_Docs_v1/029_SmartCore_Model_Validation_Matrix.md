# SmartCore Model Validation Matrix (v1.0)

## 1. Purpose

This document defines the **validation framework** for SmartCore’s foundational semantic grammar.

It is used to verify whether any concept belongs to:
- Core Grammar
- Domain Layer
- Execution Layer
- or should be rejected as non-reducible semantic inflation

The goal is to prevent:
- ontology explosion
- redundant semantic constructs
- mixing semantic vs execution concerns
- invalid abstraction layering

---

## 2. Core Semantic Grammar (Final Hypothesis)

SmartCore assumes the following minimal Semantic Constructs:

### 2.1 Continuant
Entities that persist through time.

Examples:
Person, Organization, Device, Account, Asset

---

### 2.2 Occurrent
Events that happen.

Examples:
Payment, Birth, DoorOpen, TemperatureChange

---

### 2.3 Relation
A typed association between Semantic Constructs.

Forms:
- Continuant ↔ Continuant
- Continuant ↔ Occurrent
- Occurrent ↔ Occurrent

Examples:
owns, employs, triggers, causes, evidences, constitutes

---

### 2.4 Rule
Constraints over relations/events.

Examples:
- salary must be paid monthly
- access requires permission
- refund allowed only within 7 days

---

### 2.5 Time (Dimensional Overlay)
A dimensional overlay applied to all semantic constructs.

Examples:
- valid_from / valid_to
- event_timestamp
- interval constraints

---

## 3. Key Composition Rules

### Rule 1 — Occurrent Reification Rule
Any Occurrent may be referenced as a Continuant-like entity after occurrence.

Example:
Payment#123 (Occurrent instance) becomes referenceable in system

Note:
This does NOT change its ontological type.

---

### Rule 2 — Evidence vs Constitution

Relations are classified into:

#### 3.1 Evidentiary
Represents observation of reality.

Example:
Log → evidences → Event

#### 3.2 Constitutive
Defines existence of institutional facts.

Example:
Contract → constitutes → Employment

---

### Rule 3 — Predicate is Vocabulary (Not a Core Semantic Construct)

PredicateType is not a core semantic construct.

It belongs to:
- Domain Vocabulary Layer

Structure:
Relation = (Subject, PredicateType, Object)

PredicateType examples:
owns, pays, employs, logs, approves

---

### Rule 4 — Time is Orthogonal

Time is not a semantic entity.

It is a dimension applied to:
- Relations
- Events
- Property assignments

---

## 4. Validation Matrix Schema

Each concept must be evaluated using the following matrix:

| Concept | Type (Continuant / Occurrent / Relation / Rule) | Composition Breakdown | Evidentiary / Constitutive | Breaks Grammar? | Notes |
|--------|--------------------------------------------------|------------------------|-----------------------------|------------------|------|

---

## 5. Sample Validations

### 5.1 Employment

| Concept | Type | Composition | Evidence/Constitution | Breaks |
|--------|------|-------------|----------------------|--------|
| Employment | Relation | Person ↔ Organization + Rule + Time | Constitutive | No |

---

### 5.2 Payment

| Concept | Type | Composition | Evidence/Constitution | Breaks |
|--------|------|-------------|----------------------|--------|
| Payment | Occurrent | Agent ↔ Value Transfer + Time | Both (Event + Record) | No |

---

### 5.3 Invoice

| Concept | Type | Composition | Evidence/Constitution | Breaks |
|--------|------|-------------|----------------------|--------|
| Invoice | Continuant | Record + Relation(describes Payment) | Evidentiary | No |

---

### 5.4 Log

| Concept | Type | Composition | Evidence/Constitution | Breaks |
|--------|------|-------------|----------------------|--------|
| Log | Continuant | Record + Relation(evidences Event) | Evidentiary | No |

---

### 5.5 Access Permission

| Concept | Type | Composition | Evidence/Constitution | Breaks |
|--------|------|-------------|----------------------|--------|
| AccessPermission | Rule + Relation | Subject ↔ Resource + Constraint | Constitutive | No |

---

## 6. Classification Outcome

### 6.1 Core Grammar (Stable)
- Continuant
- Occurrent
- Relation
- Rule
- Time (Dimensional)

---

### 6.2 Domain Vocabulary (Expandable)
- PredicateType
- RoleType
- PropertyType
- RelationKind
- Domain-specific labels

---

### 6.3 Derived Concepts (NOT Core Semantic Constructs)
- Role
- Value
- State
- Ownership
- Contract
- Invoice
- Payment (as record)
- Employment

---

### 6.4 Execution Layer (Explicitly NOT Core)
- StateMachine / Statechart
- Saga / Workflow Engine
- Event Sourcing
- CQRS
- Rule Engine (implementation)

---

## 7. Principle Summary

> SmartCore Core Grammar must remain independent of all execution models and domain-specific ontologies.

> Any concept that can be constructed from the Core Grammar is NOT a core semantic construct.

> Any execution mechanism must exist outside the Core as an adapter.

---

## END OF DOCUMENT