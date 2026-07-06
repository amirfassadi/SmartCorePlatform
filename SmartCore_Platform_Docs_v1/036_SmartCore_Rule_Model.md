# SmartCore Rule Model
Version: 1.0

Status: Core Semantic Standard

---

# 1. Purpose

This document defines the Rule model of SmartCore.

Rules are one of the core Semantic Constructs of the SmartCore Foundational Meta Model (SFMM).

A Rule represents a semantic constraint or behavioral statement that governs Things, Relations, Events and States.

Rules do not represent execution.

Rules represent truth, obligations, permissions, prohibitions and constraints.

This document is technology-independent.

---

# 2. Definition

A Rule is a declarative semantic statement that defines what is allowed, required, forbidden or expected within a model.

A Rule never performs work.

A Rule only defines valid or invalid behavior.

Examples:

A Person must have exactly one Birth Event.

A Reservation cannot overlap another Reservation.

A Payment must reference an Invoice.

Only Employees may approve Payroll.

A Door may only be opened by authorized Persons.

---

# 3. Fundamental Characteristics

Every Rule is:

- Declarative
- Technology Independent
- Deterministic
- Observable
- Versionable
- Traceable

A Rule is never executable by itself.

Execution engines interpret Rules.

---

# 4. Rule Structure

Conceptually a Rule consists of:

Rule

Condition

Constraint

Target

Optional Action Hint

Optional Severity

Optional Message

Example

Rule:
Only managers may approve expenses.

Condition:
Actor.Role == Manager

Constraint:
Approval Allowed

Target:
ExpenseApproval

Severity:
Error

---

# 5. Rule Targets

Rules may apply to:

Thing

Relation

Occurrent (Event)

State

Property

Lifecycle

Workflow

Composition

Examples

Thing

Person must have BirthDate.

Relation

Employment requires Organization.

Event

PaymentCompleted requires PaymentAmount.

State

Contract cannot become Active before Signature.

Workflow

Shipment cannot start before Payment.

---

# 6. Rule Categories

Rules can be classified into:

Integrity Rules

Business Rules

Authorization Rules

Validation Rules

Calculation Rules

Policy Rules

Temporal Rules

Composition Rules

The Core defines only the categories.

Domains define specific Rules.

---

# 7. Integrity Rules

Integrity Rules preserve model consistency.

Examples

Primary identity uniqueness.

No duplicate Ownership.

Every Payment references one Invoice.

Every Contract has at least two Parties.

---

# 8. Authorization Rules

Authorization determines who is allowed to perform an Action.

Examples

Only Administrators may delete Organizations.

Only Employees may access HR records.

Guests cannot modify Pricing.

Authorization belongs to the semantic layer.

Authentication belongs to Infrastructure.

---

# 9. Obligation Rules

Rules may require actions.

Examples

Invoices must be paid before DueDate.

Inspection must occur before Shipment.

Safety check must be completed before Machine Start.

These describe obligations.

They do not execute them.

---

# 10. Prohibition Rules

Rules may forbid situations.

Examples

Negative Inventory is forbidden.

Expired Contracts cannot be activated.

Duplicate Membership is prohibited.

---

# 11. Permission Rules

Rules may grant permissions.

Examples

Managers may approve Purchases.

Residents may access Building.

Customers may reserve Equipment.

Permissions are semantic facts.

Execution systems enforce them.

---

# 12. Calculation Rules

Rules may define derived values.

Examples

Invoice Total = Sum(Line Items)

Salary = Base + Overtime

Stock = In - Out

These Rules describe meaning.

They do not prescribe algorithms.

---

# 13. Temporal Rules

Rules may depend on Time.

Examples

Membership expires after one year.

Reservations cannot overlap.

Doors unlock only between 08:00 and 18:00.

Temporal semantics belong to Rules.

Scheduling belongs to Runtime.

---

# 14. State Rules

Rules constrain valid States.

Examples

Draft → Approved

Approved → Active

Active → Closed

Illegal transitions are prohibited.

---

# 15. Rule Evaluation

Rule evaluation may produce:

Valid

Warning

Violation

Information

Severity is independent from execution.

---

# 16. Rule Composition

Rules may combine using logic.

AND

OR

NOT

IF

THEN

ELSE

Composition does not change Rule identity.

---

# 17. Rule Versioning

Rules evolve.

Every Rule should support:

Identifier

Version

Effective Date

Expiration Date

Older Rules remain historically valid.

---

# 18. Rule Traceability

Every Rule should be traceable to:

Business Requirement

Policy

Law

Contract

Configuration

This enables governance and auditing.

---

# 19. Rule vs Event

Event:

Something happened.

Rule:

Something must (or must not) happen.

Events describe reality.

Rules describe constraints on reality.

---

# 20. Rule vs Relation

Relation expresses meaning between Things.

Rule constrains that meaning.

Example

Relation:

Employee worksFor Company.

Rule:

Employee salary must be positive.

---

# 21. Rule vs Workflow

Workflow describes execution order.

Rule describes execution validity.

Workflow

Approve → Pay → Archive

Rule

Payment requires Approval.

These are separate concepts.

---

# 22. Rule vs Automation

Automation performs work.

Rule defines correctness.

Automation may use Rules.

Rules never invoke Automation.

---

# 23. Rule Engine Independence

SmartCore Rules are independent from implementation.

Possible implementations include:

Drools

Open Policy Agent (OPA)

Custom Engine

Decision Tables

Source Code

SQL Constraints

No implementation is mandated by the Core.

---

# 24. Architectural Principles

Rules belong to the Semantic Layer.

Rules must never depend on:

Database

Message Broker

Workflow Engine

Programming Language

Framework

Rules define intent.

Runtime defines execution.

Infrastructure defines delivery.

---

# 25. Validation Checklist

Before introducing a new Rule ask:

Is it describing truth rather than execution?

Does it constrain semantics rather than implementation?

Can it be understood without knowing the technology?

Does it remain valid if Runtime changes?

If the answer is yes, it belongs in the Rule Model.

---

# 26. Final Principle

Rules are semantic constraints that preserve correctness across every SmartCore domain.

They define what is valid.

They never define how validity is enforced.

---

## END OF DOCUMENT