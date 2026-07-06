# SmartCore Meta Model

Version: 1.0

---

# 1. Canonical Definition

This document defines the core semantic architecture of SmartCore.

Semantic Construct
"A Semantic Construct is the root abstraction for all core semantic meaning in SmartCore."

---

# 2. Purpose

This document defines the core semantic architecture of SmartCore.

The root abstraction is the Semantic Construct (Core Level).

All concepts in the model are interpreted as Semantic Constructs, whether they are:

- Thing (Continuant)
- Event (Occurrent)
- Relation
- Rule
- Time (dimensional overlay)

---

# 2. Core Principle

All complex systems in SmartCore must be expressible using a minimal set of Semantic Constructs.

If something cannot be expressed using these constructs, it is either:

- A derived concept
- Or a missing rule, not a new core construct

---

# 3. Core Semantic Constructs

SmartCore has five core semantic constructs:

## 3.1 Thing (Continuant)
A Thing persists through time and can be identified as a continuing entity.

## 3.2 Event (Occurrent)
An Event is something that occurs at a time or interval.

## 3.3 Relation
A Relation expresses a meaningful connection between constructs.

## 3.4 Rule
A Rule expresses a constraint, obligation, permission, or expectation.

## 3.5 Time
Time is a dimensional overlay that applies across constructs and does not represent a core semantic construct.

---

# 4. Orthogonality Principle

These constructs are peer-level and orthogonal.

There is no hierarchy between:

- Thing and Event
- Relation and Rule
- Any core construct and another

No core construct is derived from another.

---

# 5. Derived Constructs

The following are not core constructs:

- State → derived from historical semantic activity
- Property → descriptive overlay over a construct
- Identity → semantic persistence layer

---

# 6. Vocabulary Layer

The vocabulary layer is separate from the semantic layer:

- PredicateType
- PropertyType
- RoleType

These describe how semantic constructs are labeled or typed.

---

# 7. Reification Principle

An Event or Relation may be reified for reference, storage, or linkage.

Example:

```
Event → EventRecord (reference form)
Relation → RelationRecord (reference form)
```

This does not change the ontological type of the construct.

---

# 8. Constructibility Test

A concept is not a new core construct if it can be expressed from:

- Thing
- Event
- Relation
- Rule
- Time

without loss of meaning.

---

# 9. Final Statement

SmartCore is a flat semantic architecture.

It is not a hierarchy of core semantic constructs.

It is a set of orthogonal Semantic Constructs interpreted through Time, Rules, and Relations.

---

End of Document