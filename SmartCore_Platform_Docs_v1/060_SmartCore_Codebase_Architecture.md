# 060_SmartCore_Codebase_Architecture.md

Version: 1.0

Status: Draft

---

# 1. Purpose

This document defines the physical software architecture of the SmartCore Platform.

While the SFMM defines the semantic language and the Platform Architecture defines the conceptual structure of the platform, this document specifies how those concepts are organized in the source code.

It serves as the bridge between architecture and implementation.

---

# 2. Scope

This document defines:

- Repository organization
- Project structure
- Shared libraries
- Core packages
- Capability packages
- Dependency rules
- Code ownership boundaries

This document does NOT define:

- Semantic constructs
- Business domains
- Runtime deployment
- Database schemas

Those concerns are defined in other documents.

---

# 3. Design Principles

The codebase SHALL follow these principles:

- Modular
- Domain-oriented
- Dependency inversion
- Technology independent
- Shared Kernel based
- Package isolation
- Stable contracts
- Independent evolution of capability platforms

---

# 4. Codebase Layers

The SmartCore source code is organized into six logical layers.

```
Applications
        │
Capability Platforms
        │
Core Engines
        │
Shared Kernel
        │
Infrastructure
        │
External Systems
```

---

# 5. Shared Kernel

The Shared Kernel contains reusable platform abstractions.

Examples include:

- Result
- Error
- Value Objects
- Common Interfaces
- Base Classes
- Event Interfaces
- Event Base Classes
- Event Metadata
- Event Contracts
- Common Exceptions

Domain-specific events such as PersonRegistered, DeviceAdded, or InvoiceCreated SHALL belong to their owning Capability Platform.

The Shared Kernel SHALL NOT contain business logic.

---

# 6. Core Engines

Core Engines provide platform-wide services.

Examples:

- Rule Engine
- Workflow Engine
- Event Engine
- Messaging Engine
- Scheduling Engine
- Policy Engine

Core Engines SHALL remain domain-independent.

They SHALL NOT depend on any Capability Platform.

---

# 7. Capability Platforms

Capability Platforms implement business capabilities.

Examples include:

- SmartCore Identity
- SmartCore Business
- SmartCore Finance
- SmartCore IoT
- SmartCore Resource
- SmartCore Workflow
- SmartCore Communication

Each Capability Platform owns:

- Application Services
- Domain Models
- Domain Events
- Repositories
- APIs

---

# 8. Repository Strategy

A Capability Platform MAY be implemented as:

- a module inside the monorepo
- or an independent repository

The architectural rules remain identical.

Repository layout SHALL NOT affect semantic architecture.

---

# 9. Recommended Monorepo Structure

```
smartcore/

    shared/

    core/

        rule_engine/

        event_engine/

        workflow_engine/

        messaging/

    modules/

        identity/

        business/

        finance/

        iot/

        resource/

        workflow/

        communication/

    infrastructure/

    api/

    bootstrap/

    tools/

    tests/
```

---

# 10. Dependency Rules

Dependencies SHALL only point downward.

Allowed:

Application
↓

Capability Platform
↓

Core Engine
↓

Shared Kernel

Forbidden:

Shared Kernel
→ Capability Platform

Core Engine
→ Capability Platform

Capability Platform
→ Capability Platform internal implementation

Cross-platform communication SHALL occur through contracts or events.

---

# 11. Contracts

Every Capability Platform exposes stable contracts.

Contracts may include:

- Commands
- Queries
- Events
- DTOs
- Interfaces

Internal implementation SHALL remain private.

---

# 12. Event Communication

Capability Platforms SHOULD communicate through events whenever possible.

Example:

```
PersonRegistered

↓

Identity Platform publishes event

↓

Business Platform consumes event

↓

IoT Platform consumes event

↓

Finance Platform consumes event
```

Platforms SHOULD avoid direct synchronous coupling.

---

# 13. Technology Independence

This architecture is independent of:

- Python
- C#
- Java
- Go
- Databases
- Frameworks

Only implementation changes.

Architecture remains identical.

---

# 14. Initial Platform Development

The first implementation slice SHALL include:

1. Identity Platform
2. Business Platform
3. Resource Platform
4. IoT Foundation

Additional platforms SHALL be added incrementally.

---

# 15. Relationship with Other Documents

This document builds upon:

- 046 — SmartCore Reference Architecture
- 047 — Architecture & Taxonomy Layer Model
- 048 — Platform Taxonomy
- 049 — Module Standards
- 050 — Governance
- 055 — Platform Development Guideline
- 056 — Tenancy and Ownership Model
- 057 — SmartCore Foundation MVP
- 058 — Identity Platform

---

# 16. Final Principle

The source code organization SHALL reflect the architectural boundaries defined by SmartCore.

No implementation convenience shall violate the dependency rules established in this document.

The codebase SHALL evolve without compromising the architectural integrity of the platform.

---

END OF DOCUMENT