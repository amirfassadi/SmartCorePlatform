# 049_SmartCore_Platform_Taxonomy.md

Version: 1.0

Status: Normative

---

# 1. Purpose

This document defines the canonical taxonomy of the SmartCore Platform.

## Scope

This document defines the platform taxonomy of SmartCore. It identifies platform families, platform modules, platform responsibilities, and platform boundaries. It does not define SFMM semantics, domain models, solution architecture, or implementation details. It depends on [046_SmartCore_Semantic_Glossary.md](046_SmartCore_Semantic_Glossary.md), [048_SmartCore_Architecture& Taxonomy_Layer_Model.md](048_SmartCore_Architecture&%20Taxonomy_Layer_Model.md), and [050_SmartCore_Module_Standards.md](050_SmartCore_Module_Standards.md).

It specifies how SmartCore is organized into platform families and architectural modules.

This document is concerned with platform organization only.

It does **not** define semantic meaning, domain models, solution architecture, or implementation details.

---

# 2. Scope

This document defines:

- Platform Families
- Platform Modules
- Platform Boundaries
- Platform Responsibilities
- Relationships between platform modules

This document does **not** define:

- SFMM semantics
- Core Semantic Constructs
- Derived Semantic Constructs
- Domain Models
- Solution Design
- Runtime Architecture

Those concerns are defined in their respective documents.

---

# 3. Relationship to SFMM

The SmartCore Semantic Foundation Model (SFMM) defines the language used to describe reality.

The Platform Taxonomy defines how SmartCore organizes reusable platform capabilities that are built using that language.

Therefore:

```
Reality
      │
      ▼
SFMM
(Semantic Language)

      │
      ▼
Platform Taxonomy
(Platform Organization)

      │
      ▼
Domain Models

      │
      ▼
Solutions

      │
      ▼
Applications
```

Platform Taxonomy SHALL NOT redefine any semantic concepts established by SFMM.

---

# 4. Platform Families

The SmartCore Platform is organized into the following platform families.

## Core Platforms

These provide fundamental services shared across the entire ecosystem.

- SmartCore Identity
- SmartCore Business
- SmartCore Resource
- SmartCore Finance
- SmartCore Communication
- SmartCore Workflow

---

## Physical World Platforms

These interact with physical environments.

- SmartCore IoT
- SmartCore Building
- SmartCore Access
- SmartCore Asset
- SmartCore Reservation

---

## Commerce Platforms

These support commercial activities.

- SmartCore Commerce
- SmartCore Billing
- SmartCore Subscription
- SmartCore Marketplace

---

## Industrial Platforms

These support industrial operations.

- SmartCore Manufacturing
- SmartCore Inventory
- SmartCore Supply Chain
- SmartCore Maintenance
- SmartCore Quality

---

## Intelligence Platforms

These provide higher-level capabilities.

- SmartCore Automation
- SmartCore Analytics
- SmartCore AI
- SmartCore Notifications

---

# 5. Platform Responsibility

Each platform represents an architectural boundary.

A platform:

- owns its business responsibilities;
- exposes reusable capabilities;
- collaborates with other platforms through defined interfaces;
- remains independent from application-specific implementations.

Platforms SHALL NOT duplicate responsibilities assigned to another platform.

---

# 6. Capability Definition

Within Platform Taxonomy, a Platform Capability is an architectural capability.

A Platform Capability:

- groups reusable platform services;
- exposes reusable business functions;
- is implemented using SFMM semantic models;
- is independent of any specific application.

This definition is distinct from the semantic concept of Capability defined within SFMM.

---

# 7. Relationship Between Semantic Capability and Platform Capability

The term "Capability" is used in two architectural contexts.

## Semantic Capability (SFMM)

Represents the inherent potential or ability of a semantic construct.

Examples:

- A Person can drive.
- A Device can measure temperature.

This is a semantic concept.

---

## Platform Capability

Represents a reusable architectural service offered by a platform.

Examples:

- Identity Management
- Payment Processing
- Reservation Engine
- Device Management

This is an architectural concept.

---

These concepts share terminology but belong to different architectural layers.

They SHALL NOT be interpreted as equivalent.

---

# 8. Dependency Rules

Platform modules:

- MAY collaborate with one another.
- SHALL respect published interfaces.
- SHALL NOT violate semantic definitions established by SFMM.
- SHALL remain independent from application implementations.

---

# 9. Governance

Changes to the Platform Taxonomy require:

- Architecture review.
- An approved ADR if architectural boundaries change.
- Backward compatibility analysis for affected platforms.

Platform evolution SHALL preserve architectural consistency across the SmartCore ecosystem.

---

# 10. Cross References

Related documents:

- 002_SmartCore_Meta_Model.md
- 047_SmartCore_Reference_Architecture.md
- 047_SmartCore_Architecture_Layer_Model.md
- ADR-0001_SFMM_v1_FREEZE.md

---

# 11. Normative Statements

- This document defines the canonical organization of SmartCore platform modules.
- Platform Taxonomy SHALL NOT redefine SFMM semantics.
- Platform modules SHALL expose reusable architectural capabilities.
- Platform modules SHALL remain technology-independent.
- Platform modules SHALL preserve clear architectural boundaries.

---

END OF DOCUMENT