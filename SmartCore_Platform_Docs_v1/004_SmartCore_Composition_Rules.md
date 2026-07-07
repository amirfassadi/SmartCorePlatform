# SmartCore Composition Rules

Version: 1.1

---

# 1. Canonical Definition

This document defines how Semantic Constructs are combined to form complex semantic structures.

**Composition**

> Composition is the semantic assembly of multiple constructs into a larger construct without changing their individual semantics.

---

# 2. Purpose

This document defines how Semantic Constructs are combined to form complex semantic structures.

SmartCore is not expanded by adding new core constructs.

It is expanded by composing existing ones.

---

# 3. Core Principle

> Complexity emerges from composition, not from new core semantic constructs.

All new concepts SHALL be expressible as combinations of the five foundational semantic constructs:

- Thing
- Event
- Relation
- Rule
- Time

---

# 4. Fundamental Composition Patterns

## 4.1 Thing + Relation Pattern

Used to model ownership, association, membership, dependency, and structural connections.

---

## 4.2 Thing + Event Pattern

Used to model actions or occurrences involving entities.

---

## 4.3 Event + Relation Pattern

Used when an Event creates, modifies, or terminates a Relation.

---

## 4.4 Rule + Everything Pattern

Rules may constrain or govern any semantic construct.

---

# 5. Reification Rule

A semantic construct MAY be reified for reference, storage, persistence, or linkage.

Reification SHALL NOT change the ontological type of the construct.

Examples:

```
Event → EventRecord

Relation → RelationRecord
```

Reification exists solely as an implementation representation of a semantic construct.

---

# 6. No Type Mutation Rule

A Thing SHALL NOT become an Event through type conversion.

An Event SHALL NOT become a Thing through type conversion.

A Relation SHALL NOT become a Thing through type conversion.

Reification is representation only.

It is never semantic transformation.

---

# 7. No New Core Construct Rule

Whenever a new concept is proposed, the following order SHALL be followed:

1. Decomposition
2. Composition
3. Reification

Only if all three approaches fail MAY the concept be introduced as new vocabulary or a derived concept.

It SHALL NOT become a new foundational semantic construct.

---

# 8. Aggregate and Service Composition Principles

## 8.1 Purpose

This section defines architectural composition principles governing Aggregate boundaries, Domain Services, Application Services, configurable Policies, and semantic ownership.

These principles extend semantic composition into architectural composition.

They introduce no additional semantic constructs.

---

## 8.2 Aggregate Boundary Principle

Aggregate boundaries SHALL be defined by the transactional invariants they are responsible for enforcing.

Conceptual association, ownership, lifecycle dependency, implementation convenience, or persistence strategy SHALL NOT determine aggregate boundaries.

An Aggregate represents a consistency boundary.

It is not merely a structural grouping of related concepts.

---

## 8.3 Cross-Aggregate Invariant Principle

Business rules spanning multiple Aggregates SHALL be enforced outside individual Aggregates.

Such rules belong to Domain Services within the owning Capability Platform.

Every Blueprint implementing such an invariant SHALL explicitly define its consistency strategy.

This document intentionally does not prescribe any implementation mechanism.

---

## 8.4 Service Responsibility Principle

### Application Services

Application Services SHALL:

- orchestrate workflows;
- coordinate repositories;
- invoke domain behavior;
- publish events.

Application Services SHALL NOT contain intrinsic business rules.

---

### Domain Services

Domain Services SHALL:

- enforce intrinsic business rules spanning multiple Aggregates;
- operate exclusively on supplied domain objects;
- remain independent of infrastructure concerns.

Domain Services SHALL NOT perform persistence operations.

Domain Services SHALL NOT access repositories directly.

---

### Policy Engines

Policy Engines SHALL:

- evaluate configurable policies;
- remain independent from domain state;
- remain reusable across Capability Platforms.

Policy Engines SHALL NOT enforce intrinsic domain invariants.

---
### Aggregates

Aggregates SHALL enforce all intrinsic invariants within their own consistency boundary.

Aggregates SHALL NOT enforce rules requiring knowledge of other Aggregates.

Such rules belong to Domain Services.

## 8.5 Domain Rule vs Policy Principle

Stable domain truths belong to the Domain Model.

Variable organizational behavior belongs to configurable policies.

The following design test SHALL be applied:

- If changing a rule requires modifying source code, it is a Domain Rule.
- If changing a rule SHOULD be possible through configuration without modifying source code, it is a Policy.

---

## 8.6 Reference Independence Principle

References between Aggregates SHALL NOT imply aggregate ownership.

Referencing another Aggregate establishes identity linkage only.

Aggregate ownership SHALL be determined exclusively by transactional consistency requirements.

---

## 8.7 Transaction Independence Principle

Transaction strategy is an implementation concern.

Implementation decisions SHALL NOT influence aggregate boundaries.

Aggregate design SHALL always be derived from domain consistency requirements rather than persistence mechanisms.

---

## 8.8 Semantic Ownership Principle

Ownership SHALL be expressed as a semantic relation between domain concepts.

When polymorphic ownership is required, implementations MAY represent that relation using implementation-specific mechanisms.

Such representations SHALL NOT redefine, replace, or alter the underlying semantic relation.

Architectural semantics SHALL remain independent from implementation representations.

---

## 8.9 Composition Consistency

The principles defined in this section extend the Composition Rules established by this document.

They SHALL NOT be interpreted as introducing additional semantic constructs.

All architectural patterns SHALL remain expressible through the five foundational semantic constructs defined by SmartCore.

---

# 9. Final Statement

Composition exists at multiple architectural levels.

Semantic constructs compose concepts.

Aggregates compose consistency boundaries.

Services compose behavior.

Capability Platforms compose business capabilities.

At every architectural level, SmartCore evolves through composition rather than by introducing additional foundational abstractions.

---

End of Document