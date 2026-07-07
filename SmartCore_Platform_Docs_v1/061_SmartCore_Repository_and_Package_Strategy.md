# 061_SmartCore_Repository_and_Package_Strategy.md

Version: 1.0

Status: Draft

---

# 1. Purpose

This document defines the physical organization of the SmartCore source code, repositories, packages, and shared libraries.

It specifies how architectural modules are translated into software packages while preserving the dependency rules defined by the SmartCore architecture.

---

# 2. Scope

This document defines:

- Repository strategy
- Package strategy
- Shared Kernel packaging
- Contracts packaging
- Versioning strategy
- Package dependency rules

It does NOT define business logic or platform capabilities.

---

# 3. Repository Strategy

SmartCore SHALL support both:

- Monorepo
- Multi-repository

The architectural rules remain identical regardless of repository layout.

---

# 4. Recommended Initial Layout

```
smartcore/

    shared/

    core/

    modules/

    infrastructure/

    api/

    bootstrap/

    tools/

    tests/
```

---

# 5. Shared Packages

The following packages SHALL remain platform-wide.

- SmartCore.Shared
- SmartCore.Contracts
- SmartCore.Core
- SmartCore.Infrastructure

---

# 6. Capability Packages

Each Capability Platform owns an independent package.

Examples:

- SmartCore.Identity
- SmartCore.Business
- SmartCore.Resource
- SmartCore.IoT
- SmartCore.Workflow
- SmartCore.Finance
- SmartCore.Communication

---

# 7. Dependency Rules

Allowed:

Capability
↓

Core

↓

Shared

Forbidden:

Shared
→ Capability

Core
→ Capability

Capability
→ Internal implementation of another Capability

---

# 8. Contracts

Each capability exposes only Contracts.

Contracts include:

- Commands
- Queries
- Events
- DTOs
- Interfaces

Internal implementation SHALL remain private.

---

# 9. Versioning

All shared packages SHALL follow semantic versioning.

Breaking changes require architectural approval.

---

# 10. Final Principle

Repository layout is an implementation concern.

Architecture SHALL remain independent from repository organization.

---

END OF DOCUMENT