# SmartCore Foundational Principles

Version: 1.0

---

# 1. Canonical Definition

This document defines the foundational semantics of SmartCore.

Thing
"A Thing is a Core Semantic Construct representing a persistent entity."

Event
"An Event is a Core Semantic Construct representing an occurrence."

Relation
"A Relation is a Core Semantic Construct representing semantic association."

Rule
"A Rule is a Core Semantic Construct defining semantic constraint."

Time
"Time is the dimensional context in which Semantic Constructs are interpreted."

---

# 2. Core Idea

SmartCore is built on one principle:

> The core model must describe reality as a set of orthogonal Semantic Constructs, not as a hierarchy of core semantic constructs.

Everything else follows from this.

---

# 2. Separation of Concerns

SmartCore separates four independent layers:

## 2.1 Semantic Layer
Defines what things mean.

- Thing (Continuant)
- Event (Occurrent)
- Relation
- Rule
- Time (dimensional overlay)

This layer is stable and technology-independent.

---

## 2.2 Derived Constructs Layer
Defines concepts built from the semantic layer.

- State
- Property
- Identity

---

## 2.3 Vocabulary Layer
Defines reusable labels and types.

- PredicateType
- PropertyType
- RoleType

---

## 2.4 Execution and Infrastructure Layer
Defines how meaning is realized and implemented.

- Workflows
- State transitions
- Databases
- APIs
- Services

---

# 3. Core Principle: No Construct Hierarchy

No lower layer is allowed to redefine the meaning of the semantic layer.

Meaning:

- Execution must not define semantics
- Infrastructure must not define behavior
- Technology must not define meaning

The semantic layer is flat and peer-level.

---

# 4. Semantic Construct Principle

Every core concept is a Semantic Construct.

This includes:

- Thing
- Event
- Relation
- Rule
- Time (as a dimensional overlay)

There is no hierarchy such as Thing > Event or Event > Thing.

---

# 5. Stability Principle

Core semantic constructs must be:

- Rarely changing
- Domain independent
- Non-technical

If a concept changes when switching domains, it is not foundational.

---

# 6. Extensibility Principle

All domains extend the core semantic model.

They do NOT redefine it.

Examples:

- Finance extends semantics
- IoT extends semantics
- ERP extends semantics

But none modify the core semantic constructs.

---

# 7. Derived Concepts Principle

If a concept can be constructed from semantic constructs, it remains derived.

Examples:

- State
- Property
- Identity

---

# 8. Time Principle

Time is not a core semantic construct.

Time is a dimensional overlay applied to semantic constructs.

---

# 9. Identity Principle

Identity is not a core semantic construct.

Identity is a semantic persistence layer applied to a construct over time.

---

# 10. Final Statement

SmartCore is not a hierarchy of core semantic constructs.

SmartCore is a semantic foundation for systems built from orthogonal Semantic Constructs.

---

End of Document