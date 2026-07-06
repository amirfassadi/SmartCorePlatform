# 028_SmartCore_Query_Model.md

# SmartCore Query Model

Version: 1.0  
Status: Draft  
Layer: Core / Application Boundary

---

# 1. Purpose

This document defines the SmartCore Query Model.

Queries represent **read-only access to system state**.

Unlike Commands, Queries:

- do not change state
- do not produce Events
- do not trigger business rules
- are safe to repeat

Queries exist to retrieve **truth projections** of the system.

---

# 2. Fundamental Principle

A Query is a request for information.

```
Get Contracts
Get Payments
Get Person By Id
Get Active Organizations
```

Queries never mutate data.

---

# 3. Command vs Query Separation (CQRS)

SmartCore strictly separates:

| Commands | Queries |
|----------|--------|
| Change state | Read state |
| Produce Events | No Events |
| Business logic | Read logic |
| Write model | Read model |

---

# 4. Query Characteristics

Every Query is:

- side-effect free
- repeatable
- cacheable
- optimizable
- composable (within constraints)

---

# 5. Query Structure

Each Query contains:

```
QueryId

QueryType

Timestamp

ActorId

TenantId

CorrelationId

Filters

Pagination

Sorting

Fields (projection)

Metadata
```

---

# 6. Query Naming

Queries use descriptive forms.

Good:

```
GetPersonById

ListContracts

FindActivePayments

SearchOrganizations
```

Avoid:

```
FetchData

RunQuery

GetStuff
```

---

# 7. Query Types

## 7.1 Point Queries

Single entity retrieval.

```
GetPersonById(id)
```

---

## 7.2 Collection Queries

Multiple entities.

```
ListContracts
```

---

## 7.3 Search Queries

Flexible filtering.

```
SearchPayments?status=failed&dateRange=...
```

---

## 7.4 Analytical Queries

Aggregations.

```
GetTotalRevenueByMonth

GetActiveContractsCount
```

---

# 8. Read Model Principle

Queries do NOT access domain logic directly.

They read from:

- projections
- read models
- denormalized views
- indexed storage

---

# 9. Read Model Independence

Read models may differ from write models.

Example:

Write Model:

```
Contract → Person + Organization + Terms
```

Read Model:

```
ContractView → flat structure optimized for UI
```

---

# 10. Projections

Projections are derived from Events.

```
ContractCreated
ContractApproved
ContractTerminated
```

↓

```
ContractReadModel
```

---

# 11. Eventual Consistency

Query results may be slightly delayed.

Reason:

- projection lag
- async processing
- distributed systems

SmartCore accepts eventual consistency for reads.

---

# 12. Query Optimization

Queries may use:

- indexes
- caching
- materialized views
- precomputed aggregates

Optimization is implementation detail.

Core does not depend on it.

---

# 13. Pagination

All collection queries must support pagination.

```
limit
offset
cursor
```

Avoid unbounded queries.

---

# 14. Filtering

Queries support structured filters.

Example:

```
status = "Active"
createdAt > "2025-01-01"
amount >= 1000
```

Filters must be safe and validated.

---

# 15. Sorting

```
sort=createdAt
sort=-amount
```

Multiple sorting keys supported.

---

# 16. Field Selection (Projection)

Clients may request specific fields:

```
fields=id,name,status
```

Reduces payload size and improves performance.

---

# 17. Query Execution Flow

```
Client
   ↓
Query API
   ↓
Read Model Resolver
   ↓
Projection Store / Cache / DB
   ↓
Result
```

No Domain logic is executed.

---

# 18. Query Isolation

Queries must not:

- trigger commands
- write logs that affect state
- modify projections

They are read-only by design.

---

# 19. Security

Query results are subject to:

- tenant isolation
- permission filtering
- field-level security

Unauthorized data must never be returned.

---

# 20. Multi-Tenant Queries

Every Query executes in a tenant context.

```
tenant_id is mandatory
```

No cross-tenant reads allowed.

---

# 21. Query Caching

Queries may be cached if:

- data is read-heavy
- consistency requirements allow it

Never cache:

- sensitive financial states (without encryption rules)
- real-time critical values

---

# 22. Real-Time Queries

Some queries bypass cache:

- dashboards
- monitoring systems
- live status tracking

---

# 23. Query vs Event Projection

| Queries | Event Projections |
|--------|------------------|
| Read API | Internal models |
| Client-facing | System-facing |
| Stable schema | Evolving schema |

---

# 24. Query Versioning

Queries evolve safely:

- add optional filters
- extend response fields
- deprecate old queries gradually

---

# 25. Error Handling

Query errors:

- NotFound
- PermissionDenied
- ValidationError

Queries never return business failure states (those belong to Commands).

---

# 26. Performance Considerations

Query layer must:

- avoid N+1 queries
- minimize joins in hot paths
- use projections instead of joins when possible

---

# 27. Query Composition

Complex queries are composed at read-model level, not at API level.

Avoid:

```
Client chaining multiple queries for one view
```

Prefer:

```
Single optimized query endpoint
```

---

# 28. Analytics Queries

Analytics are derived from read models or event streams.

Examples:

```
TotalPaymentsPerMonth
ActiveContractsByRegion
AverageResponseTime
```

---

# 29. Testing

Query layer must be tested for:

- correctness
- permission enforcement
- pagination correctness
- projection consistency
- performance regression

---

# 30. Design Checklist

Before introducing a Query verify:

✓ Read-only

✓ No side effects

✓ Tenant-safe

✓ Permission-aware

✓ Paginated if needed

✓ Optimized via projection

✓ No domain logic execution

---

# 31. Summary

Queries provide safe, optimized, and structured access to SmartCore state.

They are strictly separated from Commands and Events.

Commands change reality.

Events describe reality.

Queries observe reality.