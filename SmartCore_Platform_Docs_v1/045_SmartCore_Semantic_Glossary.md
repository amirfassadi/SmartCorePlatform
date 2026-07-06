# SmartCore Semantic Glossary

Version: 1.0

Status: Core Reference Standard

---

# 1. Purpose

This document defines the official semantic glossary of SmartCore.

## Scope

This document defines the canonical semantic terminology used by SmartCore. It does not define platform architecture, platform taxonomy, module standards, or implementation details. It depends on [001_SmartCore_Foundational_Principles.md](001_SmartCore_Foundational_Principles.md) and [002_SmartCore_Meta_Model.md](002_SmartCore_Meta_Model.md).

It provides precise, non-ambiguous definitions for all core semantic constructs used throughout the SmartCore framework.

This glossary is the final reference for interpretation of all SmartCore models.

---

# 2. Scope

This glossary covers:

- Core Semantic Constructs
- Derived Constructs
- Dimensional Constructs
- Governance Concepts
- Vocabulary-Level Terms

It does not include domain-specific vocabulary unless explicitly referenced.

---

# 3. Core Semantic Constructs

---

## 3.1 Thing

A Thing is a semantic construct that represents a persistent entity.

Things may be:

- Continuant (persisting over time)
- Occurrent (occurring as an event)

Things have identity and may participate in relations, events, and states.

---

## 3.2 Event

An Event is a semantic construct representing something that occurs at a point or interval in time.

Events are immutable and time-anchored.

Events may affect States and Relations but are not themselves states.

---

## 3.3 Relation

A Relation is a semantic construct that connects two or more Things or Events.

Relations define structure, not properties or behavior.

Relations may have types defined by vocabulary.

---

## 3.4 Rule

A Rule is a semantic constraint that governs validity, transitions, or allowed behaviors of constructs.

Rules do not execute actions; they validate or constrain them.

---

## 3.5 Time

Time is a dimensional construct that provides ordering, validity windows, and temporal context.

Time is not a Thing, Event, Relation, or Rule.

Time is applied to constructs.

---

# 4. Derived Constructs

---

## 4.1 State

A State is a temporal projection of a Thing or Relation at a specific point in time.

States are derived from Events and Relations.

---

## 4.2 Property

A Property is a descriptive attribute attached to a Thing, Relation, or Event.

Properties do not exist independently.

---

## 4.3 Capability

A Capability is the potential ability of a Thing to perform actions.

Capabilities represent potential, not execution.

---

## 4.4 Identity

Identity is the persistent semantic continuity of a Thing across time and change.

Identity does not change under any circumstances.

---

## 4.5 Lifecycle

A Lifecycle is the set of valid state transitions a construct may undergo over time.

Lifecycle defines evolution rules, not execution.

---

## 4.6 Composition

Composition is the structural assembly of multiple semantic constructs into a larger construct.

Composition preserves identity of participants.

---

# 5. Dimensional Constructs

---

## 5.1 Time Dimensions

- Occurrence Time
- Recording Time
- Validity Time
- Processing Time

These dimensions provide temporal interpretation layers.

---

# 6. Vocabulary Layer

Vocabulary defines the names and types used within constructs.

Includes:

- Predicate Types
- Property Types
- Role Types
- Capability Types
- Relation Kinds

Vocabulary does not define semantics; it labels them.

---

# 7. Governance Constructs

---

## 7.1 Governance

Governance defines how semantic models evolve, are versioned, reviewed, and maintained.

Governance ensures consistency across all SmartCore domains.

---

## 7.2 Version

A Version represents a controlled snapshot of a semantic model at a point in its evolution.

---

## 7.3 Extension

An Extension is a domain-specific addition to the Core without modification of Core semantics.

---

# 8. Semantic Rules Summary

---

- Things define identity
- Events define occurrence
- Relations define structure
- Rules define constraints
- States define observation
- Properties define description
- Capabilities define potential
- Lifecycle defines evolution
- Composition defines structure
- Time defines context
- Governance defines evolution control

---

# 9. Fundamental Separation Principles

---

## 9.1 No Mixing Principle

- Properties are not Relations
- Events are not States
- Capabilities are not Events
- Identity is not a Property

---

## 9.2 Orthogonality Principle

Each construct has a single responsibility:

- Identity → persistence
- Event → change
- State → snapshot
- Relation → connection
- Rule → constraint
- Capability → potential

---

# 10. System Interpretation Rule

All SmartCore models must be interpreted as:

A set of Semantic Constructs interacting through Time under Rule constraints.

No construct is meaningful in isolation.

---

# 11. Final Principle

SmartCore defines a universal semantic language for modeling systems.

It is not a framework of objects.

It is a system of meaning.

---

## END OF DOCUMENT