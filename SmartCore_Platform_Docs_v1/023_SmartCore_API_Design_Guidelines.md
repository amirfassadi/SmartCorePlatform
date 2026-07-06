# 023_SmartCore_API_Design_Guidelines.md

# SmartCore API Design Guidelines

Version: 1.0
Status: Draft
Layer: Application Architecture

---

# 1. Purpose

This document defines the API design principles of SmartCore.

The objective is to make every API:

- predictable
- versionable
- technology independent
- resource oriented
- event friendly
- automation friendly

The API is not the Core.

The API exposes Core capabilities.

---

# 2. Fundamental Principle

The API must never expose implementation details.

Clients communicate using business concepts.

Never database concepts.

Good:

Create Employment

Bad:

Insert EmployeeRow

---

# 3. API Layers

```
Client
      │
REST / GraphQL / gRPC
      │
Application Service
      │
Domain
      │
Core
```

Only the Application layer owns APIs.

Core never knows HTTP.

---

# 4. Resource Naming

Resources use nouns.

Correct

```
/persons
/contracts
/organizations
/payments
/orders
/devices
/assets
```

Never

```
/createPerson
/doPayment
/runWorkflow
```

Operations belong to HTTP methods.

---

# 5. HTTP Methods

GET

Read data.

POST

Create.

PUT

Replace.

PATCH

Partial update.

DELETE

Archive or delete.

---

# 6. Command vs Query

Commands

Change state.

Examples

```
POST /payments

POST /contracts

PATCH /devices/{id}
```

Queries

Never modify state.

```
GET /payments

GET /devices

GET /organizations
```

---

# 7. Stable Identifiers

Resources expose immutable IDs.

```
id
uuid
slug
```

Never expose database sequence assumptions.

---

# 8. Business Actions

Some actions are verbs.

Example

Approve Contract

Instead of

```
PATCH status=Approved
```

prefer

```
POST

/contracts/{id}/approve
```

because approval is a business action.

Examples

```
approve

cancel

reject

activate

deactivate

pay

refund

lock

unlock
```

---

# 9. Idempotency

Commands that may retry must support idempotency.

Example

```
Idempotency-Key:
```

Multiple retries

↓

single business operation

---

# 10. Pagination

Large collections use pagination.

```
limit

offset
```

or

Cursor pagination.

Never return unlimited datasets.

---

# 11. Filtering

```
GET /persons

?name=Ali

?status=Active

?organization=123

?createdAfter=...
```

Filters must be composable.

---

# 12. Sorting

```
sort=name

sort=-createdAt
```

---

# 13. Field Selection

Support projection.

```
fields=id,name,email
```

Reduces payload.

---

# 14. Expansion

Relationships are expandable.

```
GET

/contracts/15

?expand=parties

?expand=organization

?expand=attachments
```

Avoid deep automatic loading.

---

# 15. Versioning

Never break clients.

```
/v1/

/v2/
```

Prefer additive evolution.

Avoid breaking changes.

---

# 16. Error Model

Standard format.

```
{
  code,
  message,
  details,
  correlationId
}
```

Never expose stack traces.

---

# 17. Validation Errors

Example

```
{
  code:"ValidationFailed",

  errors:[
      {
         field:"salary",
         message:"Required"
      }
  ]
}
```

---

# 18. Business Errors

Business errors differ from technical errors.

Examples

```
ContractAlreadyActive

InsufficientBalance

PermissionDenied

InvalidLifecycleTransition

OrganizationClosed
```

---

# 19. Authentication

Authentication answers

Who are you?

Authorization answers

What may you do?

Never mix them.

---

# 20. Correlation ID

Every request receives

```
CorrelationId
```

Used by

Logs

Events

Audit

Tracing

---

# 21. Event Publication

Commands may publish events.

Example

```
POST Payment

↓

PaymentCreated

↓

LedgerUpdated

↓

NotificationSent
```

Clients never depend on event ordering.

---

# 22. Long Running Operations

Large jobs return

```
202 Accepted
```

with operation id.

Client polls

or

subscribes.

---

# 23. Async APIs

SmartCore supports

REST

GraphQL

gRPC

Message Bus

WebSocket

All expose the same domain behavior.

---

# 24. Hypermedia

Optional.

Useful for discoverability.

Not required.

---

# 25. Bulk Operations

Support

```
bulkCreate

bulkUpdate

bulkDelete
```

when performance requires.

---

# 26. Security

Never trust client input.

Always validate

authorization

ownership

tenant

organization

permissions

---

# 27. Multi-Tenant APIs

Every request executes inside a tenant context.

Never leak resources between tenants.

---

# 28. File Uploads

Files are Resources.

```
POST /attachments
```

returns

AttachmentId

Other entities reference Attachment.

---

# 29. API Documentation

Every endpoint must include

Purpose

Inputs

Outputs

Permissions

Events

Possible Errors

Examples

---

# 30. API Design Checklist

Before exposing an endpoint verify:

✓ Business language

✓ Resource oriented

✓ Stateless

✓ Versionable

✓ Idempotent

✓ Secure

✓ Event friendly

✓ Observable

✓ Documented

✓ Backward compatible

---

# Summary

SmartCore APIs expose business capabilities rather than implementation details.

The API layer is an adapter over the Core.

Clients interact with stable Resources, Commands and Queries while the internal architecture remains independent of transport protocols and infrastructure.