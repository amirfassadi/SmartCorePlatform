# SmartCore Domain Modeling Rules
Version: 1.0

Status: Core Architectural Standard

---

# 1. Purpose

This document defines the **rules for building domain models** on top of SmartCore Core Grammar and Core Vocabulary.

It ensures that:
- all domains remain consistent
- no domain introduces new core semantic constructs
- execution logic stays outside Core
- semantic integrity is preserved across systems

---

# 2. Fundamental Principle

> Domains are NOT extensions of Core.
> Domains are CONFIGURATIONS of Core.

A domain does not add new reality types.
It only defines:
- which Core concepts are used
- how they are composed
- what constraints are applied

---

# 3. Allowed Operations in Domain Layer

A domain MAY:

## 3.1 Compose Core Concepts

Example:
```
Employment = Person + Organization + Relation + Rule + Time
```

---

## 3.2 Define New Relations (Vocabulary Only)

Example:
```
employs
owns
reserves
approves
measures
```

These are NOT core semantic constructs.
They are typed labels over Relation.

---

## 3.3 Define Constraints (Domain Rules)

Example:
```
Rule:
Employee.salary must be paid monthly
```

---

## 3.4 Define Lifecycle Behavior (Declarative Only)

Example:
```
Contract lifecycle:
Draft → Active → Suspended → Terminated
```

---

## 4. Forbidden Operations in Domain Layer

A domain MUST NOT:

## 4.1 Introduce New Core Semantic Constructs

Forbidden:
```
introducing "Money" as a core semantic construct
introducing "Invoice" as a core semantic construct type
introducing "Ownership" as a core semantic construct entity
```

All must reduce to Core Grammar.

---

## 4.2 Encode Execution Logic

Forbidden:
```
if payment_received then trigger_event()
spawn_worker()
call_microservice()
emit_kafka_event()
```

Execution belongs to adapters.

---

## 4.3 Break Type Boundaries

Forbidden:
```
Treating Event as Continuant
Treating Rule as Entity
Treating Time as Object
```

---

## 5. Domain Construction Model

Every domain must be built using this structure:

```
Domain Model =

Core Grammar
+ Core Vocabulary
+ Composition Rules
+ Domain Constraints
+ Lifecycle Definitions
```

NOT:

```
Domain Model ≠ New Ontology
Domain Model ≠ New Core Semantic Construct System
```

---

# 6. Valid Domain Patterns

## 6.1 Finance Domain

```
Payment = Occurrent
Invoice = Document + Relation
Wallet = Continuant + Relation
Ledger = Continuant + Relation
```

---

## 6.2 HR Domain

```
Employment = Relation(Person, Organization) + Rule + Time
Salary Payment = Occurrent
Attendance = Measurement
```

---

## 6.3 IoT Domain

```
Sensor = Continuant
Reading = Occurrent
Device = Continuant
Alert = Occurrent + Rule
```

---

# 7. Domain Isolation Rule

Each domain:

- must NOT depend on other domains directly
- may ONLY depend on Core Grammar
- may optionally depend on shared Vocabulary

Example:

Finance must NOT import HR concepts.

Instead:

Both map to Core independently.

---

# 8. Cross-Domain Consistency Rule

If two domains define the same concept:

Example:
- HR: Employee
- Finance: Contractor

They MUST resolve to:

```
Person + Role + Relation
```

NOT:
```
two different semantic constructs
```

---

# 9. Composition Validity Rule

A domain model is valid only if:

- every concept maps to Core Grammar
- no undefined semantic constructs exist
- all relations are typed
- all rules are explicit

---

# 10. Anti-Pattern Rules

## 10.1 Hidden Construct Inflation

Bad:
```
Wallet is a fundamental entity
```

Correct:
```
Wallet = Continuant + Relation(holds Value)
```

---

## 10.2 Over-Specialization

Bad:
```
Invoice, Receipt, Bill as separate semantic constructs
```

Correct:
```
Document + Relation + Event mapping
```

---

## 10.3 Execution Leakage

Bad:
```
Domain triggers API calls
Domain sends messages
Domain schedules jobs
```

Correct:
```
Domain emits semantic events only
Execution layer handles actions
```

---

# 11. Domain Validation Requirement

Every domain MUST pass:

- Validation Matrix (031 dependency)
- Core Vocabulary Mapping (030)
- Grammar Compliance (029)

If any concept fails:

→ it is not a valid domain model

---

# 12. Final Rule

> If a domain requires a new core semantic construct, the problem is not the domain.
> The problem is incomplete understanding of Core Grammar.

---

## END OF DOCUMENT