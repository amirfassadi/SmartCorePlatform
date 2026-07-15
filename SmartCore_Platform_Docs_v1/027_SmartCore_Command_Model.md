# 027_SmartCore_Command_Model.md

# SmartCore Command Model

Version: 1.2
Status: Normative
Layer: Core

Related Decision Records:
- ADR-0002_Identity_Foundation_Clarifications.md (Decision 7)

---

# 1. Purpose

This document defines the SmartCore Command Model.

Commands represent an intention to change the system.

Unlike Events, Commands describe **what the caller wants to happen**, not what has already happened.

Every state change inside SmartCore begins with a Command.

---

# 2. Fundamental Principle

A Command expresses an intention.

Examples:

```
Create Contract

Approve Contract

Hire Employee

Transfer Asset

Register Person

Pay Invoice
```

A Command is **not** a fact.

It may succeed.

It may fail.

It may be rejected.

Only successful Commands produce Events.

---

# 3. Command Lifecycle

```
Client

↓

Command

↓

Validation

↓

Authorization

↓

Business Rules

↓

Execution

↓

State Change

↓

Event(s)

↓

Response
```

Commands never skip validation.

---

# 4. Command Characteristics

Every Command is:

- mutable before execution
- immutable after submission
- validated
- authorized
- traceable
- idempotent where applicable

---

# 5. Command Structure

Every Command contains:

```
CommandId

CommandType

Timestamp

ActorId

TenantId

CorrelationId

Payload

Metadata

Version
```

---

# 6. Command Identity

Each Command has a globally unique identifier.

Example:

```
cmd_01HX...
```

CommandId exists for traceability.

It is not a business identifier.

---

# 7. Command Naming

Commands use imperative verbs.

Good

```
CreatePerson

ActivateContract

GrantPermission

TransferOwnership

CompletePayment
```

Avoid

```
PersonCreated

ContractActivated
```

Those are Events.

---

# 8. One Business Intention

A Command should express exactly one business intention.

Good

```
ApproveInvoice
```

Bad

```
ApproveInvoiceAndNotifyUserAndUpdateLedger
```

Secondary actions belong to Event Consumers.

---

# 9. Validation

Validation occurs before execution.

Examples:

- required fields
- format validation
- range validation
- duplicate detection

Invalid Commands never reach the Domain.

---

# 10. Authorization

Authorization is independent from validation.

Example:

A valid Command may still be rejected because:

- insufficient permissions
- tenant isolation
- organization policy

---

# 11. Business Rules

Business Rules determine whether execution is allowed.

Example:

```
Contract must be Draft before Approval.
```

If violated:

```
ContractAlreadyApproved
```

No Event is produced.

---

# 12. Execution

Execution changes business state.

Execution must be atomic.

Partial execution is not allowed.

---

# 13. Events

Successful execution emits one or more Events.

Example:

```
ApproveContract

↓

ContractApproved

↓

InvoiceCreated

↓

NotificationScheduled
```

---

# 14. Failed Commands

Failure does not produce Domain Events.

Failures return Business Errors.

Example:

```
InsufficientBalance

PermissionDenied

InvalidTransition
```

Optional System Events may still be emitted for audit or monitoring.

---

# 15. Idempotency

Some Commands must be idempotent.

Example:

```
PayInvoice
```

Network retry must not create duplicate Payments.

Use:

```
Idempotency-Key
```

---

# 16. Command Ordering

Ordering is guaranteed only inside one Aggregate.

No global ordering assumptions.

---

# 17. Aggregate Target

Every Command targets exactly one Aggregate.

Examples:

```
Contract

Person

Payment

Organization

Device
```

Cross-aggregate work is coordinated through Events.

## 17.1 Command Model Coordination Exception for Identity Registration

`RegisterPerson` is an approved, narrowly-scoped exception to this rule.

RegisterPerson MAY coordinate creation of multiple Identity Aggregates (Person, Organization, Membership) within a single atomic consistency boundary.

This exception:

-   Applies ONLY to the RegisterPerson operation.
-   Is authorized by ADR-0002_Identity_Foundation_Clarifications.md, Decision 7 (Command Model Coordination Exception for Identity Registration).
-   Exists because Person, Personal Organization, and Membership represent a single business invariant that must not exist in a partial state; an event-driven Saga would permit temporarily invalid intermediate states.
-   SHALL NOT be treated as a general precedent. Any future request for a similar cross-Aggregate atomic coordination exception SHALL require its own independent architectural review.

All other Commands SHALL target exactly one Aggregate per this section.

---

# 18. Command Payload

Payload contains only required business data.

Avoid:

- calculated values
- duplicated state
- transport metadata

---

# 19. Command Handler

Every Command has exactly one Handler.

```
ApproveContractCommand

↓

ApproveContractHandler
```

One Command

↓

One Handler

---

# 20. Handler Responsibilities

Handler performs:

- validation coordination
- authorization coordination
- loading Aggregate
- invoking Domain logic
- persisting changes
- publishing Events

Handler does not contain business rules.

Business rules belong to the Domain.

---

# 21. Side Effects

Commands never directly send:

- emails
- SMS
- notifications
- webhooks

Instead:

```
Command

↓

Event

↓

Consumer

↓

Side Effect
```

---

# 22. Long Running Commands

Long operations may return:

```
Accepted
```

Execution continues asynchronously.

Completion is communicated through Events.

---

# 23. Retry Strategy

Safe retries are allowed only when:

- idempotency is guaranteed
- duplicate execution is prevented

---

# 24. Auditing

Every Command execution records:

- Actor
- Time
- Tenant
- Result
- CorrelationId

Audit exists independently from Event storage.

---

# 25. Security

Commands are untrusted input.

Never trust:

- payload
- client timestamps
- client permissions
- client identities

Everything must be verified.

---

# 26. Versioning

Commands evolve through versioning.

Rules:

- add optional fields
- preserve compatibility
- introduce new Command types for breaking changes

---

# 27. Testing

Each Command should be tested for:

- validation
- authorization
- business rules
- event generation
- failure scenarios
- idempotency

---

# 28. Design Checklist

Before introducing a new Command verify:

✓ Represents one business intention

✓ Uses imperative naming

✓ Targets one Aggregate

✓ Has one Handler

✓ Validates input

✓ Enforces authorization

✓ Executes atomically

✓ Produces correct Events

✓ Supports idempotency where required

---

# 29. Command vs Event

| Command | Event |
|----------|-------|
| Intent | Fact |
| Future | Past |
| May Fail | Already Happened |
| Mutable before execution | Immutable |
| One Handler | Many Consumers |

---

# 30. Summary

Commands are the entry point for every business state change inside SmartCore.

They represent intentions, enforce validation and authorization, invoke domain behavior, and produce immutable Events upon successful execution.

Commands never describe history.

They initiate it.

---

# Change Log

## Version 1.2 (2026-07-12)

**Decision**: Status promoted from Draft to Normative.

**Rationale**: 057_SmartCore_Tenancy_and_Ownership_Model.md (v1.3,
Normative) and, transitively, 059_SmartCore_Identity_Platform.md
(Normative) now explicitly cite this document as the authoritative
baseline rule from which RegisterPerson is a documented exception.
A Normative document cannot coherently except itself from a rule
defined in a document that has not itself reached binding status.
This document's content has used SHALL-level normative language
throughout since v1.0 and was already being treated as binding by
dependent Blueprints; this change aligns its declared Status with
its actual role in the architecture.

**Note**: This is a maturity/status decision, not a content change to
Sections 1-30. As with any Level 3+ change per
051_SmartCore_Governance_and_Decision_Model.md §5, this promotion
should be confirmed through the standard Architecture Review process
before being treated as final.

## Version 1.1 (2026-07-12)

**Decisions Implemented:** - Documented the approved RegisterPerson
exception to the single-Aggregate Command rule.

**Authorizing Decision Records:** -
ADR-0002_Identity_Foundation_Clarifications.md, Decision 7

**Changes:** - Added §17.1 Command Model Coordination Exception for
Identity Registration under §17 Aggregate Target - Added Related
Decision Records reference to document header

## Version 1.0

- Initial Command Model definition

---

End of Document