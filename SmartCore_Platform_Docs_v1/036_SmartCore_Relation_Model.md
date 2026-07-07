# SmartCore Relation Model
Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the semantic model of Relations in SmartCore.

Relations are one of the core Semantic Constructs of the SmartCore Meta Model (SFMM).

Every domain in SmartCore relies on Relations to describe how Things are connected.

This specification defines:

- What a Relation is
- Relation structure and semantics
- Relation participants
- Relation lifecycle
- Relation types
- Relation composition rules
- Relation vs Event vs State vs Rule boundaries
- Architectural constraints

This document is technology-independent.

---

# 2. Definition

A Relation is a first-class semantic construct that expresses a meaningful connection between two or more Things.

A Relation is NOT:

- a database foreign key
- a pointer
- a message link
- a runtime reference

A Relation IS:

- a semantic fact about the world model
- a typed connection between entities
- an element that can exist independently of runtime representation

Examples:

- Person owns Car
- Organization employs Person
- Device locatedIn Room
- Invoice belongsTo Organization
- Contract binds Party A and Party B

---

# 3. Core Properties of Relations

Every Relation has:

- Identity
- Relation Type
- Participants
- Cardinality
- Directionality
- Optional Attributes
- Optional Time Scope
- Optional Rules
- Metadata

Relations are first-class semantic entities.

---

# 4. Relation Structure

Formally:

Relation := (Type, Participants, Attributes?, Time?, Metadata?)

Example:

Employment Relation:

Type: employs

Participants:
- Organization
- Person

Attributes:
- roleTitle
- salary
- department

Time Scope:
- startDate
- endDate

Metadata:
- source
- confidence

---

# 5. Participants

Relations can connect:

## 5.1 Continuant ↔ Continuant

- Person owns Car
- Organization employs Person
- Company owns Subsidiary

## 5.2 Continuant ↔ Occurrent

- Invoice references PaymentEvent
- Certificate evidences BirthEvent
- Refund references PaymentCompletedEvent

## 5.3 Occurrent ↔ Occurrent

- Refund compensates Payment
- Delivery completes Shipment
- Activation triggers BillingEvent

Relations are NOT restricted by participant type.

---

# 6. Cardinality

Relations may be:

- 1 → 1
- 1 → N
- N → N

Cardinality is domain-specific and NOT part of the core semantic definition.

---

# 7. Directionality

Relations may be:

## Directed

- Person owns Car
- Organization employs Person

## Symmetric

- Person marriedTo Person
- Node connectedTo Node

Direction is semantic, not technical.

---

# 8. Relation vs Event

## Event

- represents something that happened
- immutable occurrence
- time-bound

Example:
PaymentCompleted

## Relation

- represents a connection between Things
- may persist over time
- may span multiple Events

Example:
Employment(Person, Organization)

---

Key difference:

Event = occurrence
Relation = structure of meaning

---

# 9. Relation vs State

## State

- describes current condition of a Thing

Example:
Door = Open

## Relation

- describes connection between Things

Example:
Person owns Car

State is a snapshot.
Relation is a semantic link.

---

# 10. Relation vs Rule

Relations describe "what is connected".

Rules describe "what must/should happen".

Example:

Relation:
Person employedBy Organization

Rule:
If employedBy exists → salary must be defined

Rules constrain Relations but are not Relations themselves.

---

# 11. Temporal Behavior

Relations may:

- start
- end
- evolve

Example:

Employment exists from 2020 → 2025

Temporal scope does NOT change the identity of the Relation.

---

# 12. Reified Relations (Important)

Some Relations can be promoted into Entities.

Example:

Employment Relation becomes EmploymentContract Entity

This happens when:

- Relation needs lifecycle
- Relation needs attributes
- Relation needs participation in Events
- Relation needs governance

This is NOT a different concept.
It is a reification pattern.

---

# 13. Higher-Order Relations

Relations may reference:

- other Relations
- Events
- Rules

Example:

AuditLog references (Employment Relation + Modification Event)

This enables full traceability graph.

---

# 14. Relation Types

Relation Types are part of Domain Vocabulary:

Examples:

- owns
- employs
- belongsTo
- locatedIn
- triggers
- compensates
- evidences
- constitutes

These are NOT core semantic constructs.

They are domain-level labels.

---

# 15. Constitutive vs Evidentiary Relations

## Evidentiary

- Relation describes or proves existence of something

Example:
Log evidences TemperatureEvent

## Constitutive

- Relation creates the existence of something

Example:
SignedContract constitutes EmploymentRelation

This distinction is critical in SmartCore.

---

# 16. Constraints

Relations may have constraints:

- cardinality constraints
- temporal constraints
- rule constraints
- type constraints

Constraints belong to Rule layer, not Relation core.

---

# 17. Lifecycle of Relations

A Relation may have lifecycle:

- Created
- Active
- Suspended
- Terminated

Lifecycle is derived from Events, not intrinsic.

---

# 18. Identity

Each Relation has immutable identity.

Even if participants change (in allowed models), identity remains stable.

---

# 19. Composition Rule

Complex systems are built from:

Thing + Relation + Event + Rule + Time

Relations are the backbone of composition.

---

# 20. Architectural Principle

Relations are semantic constructs.

They are independent of:

- storage model
- message system
- workflow engine
- database schema

---

# 21. Final Principle

A Relation is a persistent semantic connection between Things that forms the structural backbone of SmartCore systems.

Everything else (Events, State, Rules, Execution) operates on top of Relations.

---

## END OF DOCUMENT