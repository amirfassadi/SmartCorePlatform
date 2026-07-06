# 025_SmartCore_SDK_Developer_Experience_Layer.md

# SmartCore SDK & Developer Experience Layer

Version: 1.0  
Status: Draft  
Layer: Application / Developer Platform

---

# 1. Purpose

This document defines the SmartCore SDK and Developer Experience (DX) Layer.

Its goal is to make SmartCore:

- easy to integrate
- consistent across languages
- type-safe where possible
- event-aware
- domain-aligned (not infrastructure-driven)

SDK is NOT Core.

SDK is a controlled projection of Core.

---

# 2. Fundamental Principle

SDK is a **facade over the Core API + Events + Commands**.

```
Developer Code → SDK → API Layer → Core
```

SDK never contains business logic.

---

# 3. SDK Responsibilities

SDK is responsible for:

- request construction
- response parsing
- type definitions
- event subscription helpers
- retry handling (basic)
- authentication wrappers
- serialization/deserialization

---

# 4. SDK Must NOT Do

SDK must never:

- implement business rules
- modify domain logic
- decide workflows
- enforce policies
- store authoritative state

Core is the only source of truth.

---

# 5. Supported SDK Languages

SmartCore SDKs must be generated for:

- TypeScript
- Python
- Go
- Java (enterprise systems)
- C# (.NET environments)

Optional:

- Rust (high-performance systems)
- Dart (mobile apps)

---

# 6. SDK Architecture

Each SDK follows same structure:

```
/client
/core-types
/events
/commands
/queries
/auth
/config
```

---

# 7. Core Types Module

SDK exposes core semantic constructs:

- Thing
- Relation
- Event
- Rule
- Time

Plus domain types:

- Person
- Organization
- Contract
- Payment
- Asset

These are generated, not manually written.

---

# 8. Command API Wrapper

Example:

```ts
sdk.contracts.create({
   parties: [...],
   terms: {...}
})
```

Internally:

```
POST /contracts
```

SDK hides transport layer.

---

# 9. Query API Wrapper

Example:

```ts
sdk.payments.getById(id)
sdk.contracts.list({ status: "active" })
```

Queries are:

- cached optionally
- paginated automatically
- typed strongly

---

# 10. Event Subscription Model

SDK provides event listeners:

```ts
sdk.events.on("PaymentCompleted", (event) => {
    console.log(event)
})
```

Or async stream:

```ts
for await (const event of sdk.events.stream("ContractUpdated")) {
    handle(event)
}
```

---

# 11. Event Typing

Events are strongly typed:

```ts
PaymentCompletedEvent {
   paymentId
   amount
   timestamp
   parties
}
```

No raw JSON exposure in typed SDKs.

---

# 12. Authentication Layer

SDK supports:

- API Key
- OAuth2
- JWT
- Service-to-Service tokens

Example:

```ts
new SmartCoreClient({
   apiKey: "xxx"
})
```

---

# 13. Multi-Tenant Support

SDK enforces tenant context:

```ts
sdk.setTenant("tenant_123")
```

All requests automatically scoped.

---

# 14. Error Handling

SDK normalizes errors:

```ts
try {
  await sdk.payments.create(...)
} catch (e) {
  if (e.code === "InsufficientBalance") {
     ...
  }
}
```

Error model is unified across Core.

---

# 15. Retry Strategy

SDK implements safe retries:

- network failure retry
- timeout retry
- idempotent command retry only

Never retry non-idempotent operations.

---

# 16. Idempotency Support

SDK automatically supports:

```
Idempotency-Key
```

Example:

```ts
sdk.payments.create(
  data,
  { idempotencyKey: "abc-123" }
)
```

---

# 17. Pagination Abstraction

SDK hides pagination complexity:

```ts
const payments = await sdk.payments.listAll()
```

Internally streams pages.

---

# 18. Caching Layer (Optional)

SDK may cache:

- static metadata
- reference data
- read-heavy queries

Never cache:

- financial transactions
- state-changing operations

---

# 19. Code Generation Pipeline

SDK is generated from:

- Core Schema
- API Specification
- Event Definitions

Pipeline:

```
Core Model → Schema Registry → SDK Generator → Language Packages
```

---

# 20. Versioning Strategy

SDK versions must match Core API versions:

```
SDK v1.x → Core v1 API
SDK v2.x → Core v2 API
```

No silent breaking changes.

---

# 21. Developer Experience Principles

SmartCore SDK must:

- reduce cognitive load
- hide infrastructure
- expose domain language
- prevent misuse
- guide correct usage

---

# 22. Documentation Integration

SDK must include:

- inline types
- auto-generated docs
- examples per method
- event catalog

---

# 23. Testing Support

SDK provides:

- mock client
- fake event stream
- sandbox mode
- deterministic replay tools

---

# 24. Debug Mode

SDK supports:

- request logging
- event tracing
- correlation ID tracking
- latency inspection

---

# 25. Sandbox Mode

Safe development environment:

- no real ledger writes
- simulated events
- fake integrations

---

# 26. Language Neutrality Principle

All SDKs must behave identically across languages.

No language-specific business logic allowed.

---

# 27. SDK vs API Boundary

| Layer | Responsibility |
|------|----------------|
| SDK | Developer convenience |
| API | Transport layer |
| Core | Business truth |

---

# Summary

SmartCore SDK is not just a wrapper.

It is a **domain-consistent developer interface** that ensures developers interact with SmartCore in a safe, predictable, and strongly-typed way while keeping Core completely isolated from implementation concerns.