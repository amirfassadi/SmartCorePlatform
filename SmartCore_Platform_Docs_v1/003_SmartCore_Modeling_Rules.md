# SmartCore Modeling Rules

Version: 1.0

---

# 1. Canonical Definition

This document defines how real-world concepts are modeled using the SmartCore semantic architecture.

Modeling Rule
"A Modeling Rule is a formal guideline for expressing a concept as a composition of Semantic Constructs."

---

# 2. Purpose

This document defines how real-world concepts are modeled using the SmartCore semantic architecture.

It translates reality into formal structures using:

- Thing
- Event
- Relation
- Rule
- Time

---

# 2. Core Modeling Principle

> Everything must be expressed as a composition of Semantic Constructs.

No concept is allowed to introduce a new core ontological construct.

---

# 3. Modeling Pattern Types

All models in SmartCore fall into one of the following patterns:

## 3.1 Structural Pattern
Defines static existence.

Example:

```
Person owns Car
Organization has Employee
```

Mapping:

- Thing ↔ Thing
- Relation
- Time optional

---

## 3.2 Event Pattern
Defines something that happens.

Example:

```
Payment occurred
User logged in
Sensor detected temperature
```

Mapping:

- Event
- Involves Thing(s)
- Has Time

---

## 3.3 Relational Event Pattern
A hybrid pattern where an Event affects a Relation.

Mapping:

- Event modifies Relation
- Creates or destroys a relation instance

---

## 3.4 Rule Pattern
Defines constraints or behavior.

Mapping:

- Rule
- Applies to Thing / Relation / Event

---

# 4. Reification Rule

When a Relation or Event requires:

- Lifecycle
- Identity
- History
- References

it may be reified for reference only.

Example:

```
Employment (Relation)
→ EmploymentRecord (reference form)
```

Reification does not change ontological type.

---

# 5. Time Binding Rule

Time is attached to:

- Events (mandatory)
- Relations (optional)
- Derived states

Time is not modeled as a standalone construct.

---

# 6. No Direct Business Concepts Rule

Business terms are not core constructs.

Examples:

- Invoice ❌
- Payment ❌
- Salary ❌

All are modeled as:

- Events OR
- Reified Relations OR
- Derived constructs

---

# 7. Identity Rule

Identity belongs to semantic persistence and is not a type conversion mechanism.

An Event does not become a Thing by virtue of being recorded.

---

# 8. Constructibility Validation Rule

Before introducing any model:

Check:

1. Can it be expressed using Semantic Constructs?
2. Does it introduce new semantics?
3. Does it exist across multiple domains?

If the answer is no to the first and yes to the latter two, the concept should be treated as vocabulary or a derived construct rather than a new core construct.

---

# 9. Anti-Pattern: Over-Modeling

Do NOT create new entities when composition is sufficient.

Correct:

```
Relation(Person owns Car)
```

---

# 10. Final Principle

Modeling is not about naming things.

It is about decomposing reality into Semantic Constructs.

---

End of Document