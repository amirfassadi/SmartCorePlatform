# SmartCore Composition Rules

Version: 1.0

---

# 1. Canonical Definition

This document defines how Semantic Constructs are combined to form complex semantic structures.

Composition
"Composition is the semantic assembly of multiple constructs into a larger construct without changing their individual semantics."

---

# 2. Purpose

This document defines how Semantic Constructs are combined to form complex semantic structures.

SmartCore is not expanded by adding new core constructs.

It is expanded by composing existing ones.

---

# 2. Core Principle

> Complexity emerges from composition, not from new core semantic constructs.

All new concepts must be expressible as combinations of:

- Thing
- Event
- Relation
- Rule
- Time

---

# 3. Fundamental Composition Patterns

## 3.1 Thing + Relation Pattern
Used to model ownership, association, membership.

## 3.2 Thing + Event Pattern
Used to model actions or occurrences involving entities.

## 3.3 Event + Relation Pattern
Used when an Event modifies or creates a relation.

## 3.4 Rule + Everything Pattern
Rules apply across all semantic structures.

---

# 4. Reification Rule

A construct may be reified for reference, storage, or linkage.

This does not change its ontological type.

Example:

```
Event → EventRecord
Relation → RelationRecord
```

---

# 5. No Type Mutation Rule

An Event must not become a Thing by type conversion.

A Thing must not become an Event by type conversion.

Reification is reference-only.

---

# 6. No New Core Construct Rule

If a new concept appears:

1. Try decomposition
2. Try composition
3. Try reification

Only if all fail should it be considered a new vocabulary or derived concept, not a new core construct.

---

# 7. Final Statement

SmartCore grows horizontally through composition, not vertically through core semantic construct hierarchy.

---

End of Document