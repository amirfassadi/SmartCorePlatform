# 047_SmartCore_Reference_Architecture.md

Version: 1.3

Status: Draft

---

# SmartCore Platform Architecture

---

# 1. Purpose

This document defines the Reference Architecture View of the SmartCore Platform beyond the Semantic Foundation Model (SFMM).

While SFMM defines the semantic language used to describe reality, this document defines how the SmartCore ecosystem itself is organized from a reference architecture perspective.

## Scope

This document defines the Reference Architecture View of SmartCore. It does not redefine SFMM semantics. It does not replace the canonical Architecture Layer Taxonomy View in [048_SmartCore_Architecture& Taxonomy_Layer_Model.md](048_SmartCore_Architecture&%20Taxonomy_Layer_Model.md). It depends on [046_SmartCore_Semantic_Glossary.md](046_SmartCore_Semantic_Glossary.md), [048_SmartCore_Architecture& Taxonomy_Layer_Model.md](048_SmartCore_Architecture&%20Taxonomy_Layer_Model.md), and [049_SmartCore_Platform_Taxonomy.md](049_SmartCore_Platform_Taxonomy.md).

Where this document uses taxonomy terminology, it adopts the terminology established by the Architecture Layer Taxonomy View in [048_SmartCore_Architecture& Taxonomy_Layer_Model.md](048_SmartCore_Architecture&%20Taxonomy_Layer_Model.md). It is complementary to the semantic view, the execution boundary view, and the architecture layer taxonomy view.

Its purpose is to clearly separate:

* Semantic Foundation
* Platform Capabilities
* Domain Models
* Solution Modules
* Applications
* Developer Tooling

This separation prevents architectural ambiguity and establishes a stable long-term platform structure.

---

# 2. Platform Ecosystem Composition View

The SmartCore Platform is organized into a Reference Architecture View. The canonical Architecture Layer Taxonomy View is defined in [048_SmartCore_Architecture& Taxonomy_Layer_Model.md](048_SmartCore_Architecture&%20Taxonomy_Layer_Model.md). This document uses that taxonomy terminology as its reference and does not redefine the canonical taxonomy.

**This section describes ecosystem components, not an alternative layer stack.** Per 048§9, 048 is the sole canonical source for the SmartCore architecture layer hierarchy, and no other document SHALL introduce an alternative layer hierarchy. The components below elaborate the composition of the SmartCore ecosystem; they are positioned within — not parallel to — the six canonical layers defined in 048§3. See §2.1 for the explicit mapping.

```
SmartCore Ecosystem Composition

Primary chain:
├── Foundation
├── Capability Platforms
├── Domain Models
└── Solutions

Cross-cutting components (see §2.1):
├── Core Engines
└── Developer Platform
```

Each component has a distinct responsibility.

No component should assume the responsibilities of another.

## 2.1 Mapping to the Canonical Architecture Layer Taxonomy (048)

| 047 Ecosystem Component | Corresponding 048 Canonical Layer |
| --- | --- |
| Foundation | Layer 1 — Semantic Foundation (SFMM) |
| Core Engines | Cross-cutting runtime capability supporting Layers 1–2. Not a distinct top-level layer in 048. |
| Capability Platforms | Architectural elements defined *within* Layer 2 — Platform Taxonomy (see 049§4, Platform Families), not Layer 2 itself. Platform Taxonomy is the classification model; Capability Platforms are the elements it classifies. |
| Domain Models | Layer 3 — Domain Modeling |
| Solutions | Layer 4 — Solution Design |
| Developer Platform | Cross-cutting tooling concern supporting Layers 3–5. Not a distinct top-level layer in 048. |

048 remains the sole canonical source for the layer stack and its dependency rules. This table exists only to reconcile this document's ecosystem composition terminology with that canonical stack; it does not add, reorder, or redefine any 048 layer.

---

# 3. Foundation

The Foundation defines the semantic language of the platform.

It contains no business logic.

It contains no application logic.

It contains no implementation details.

The Foundation consists of:

* SFMM
* Vocabulary
* Modeling Rules
* Validation Rules
* Architecture Decision Records (ADR)

The Foundation describes **how reality is modeled**, not how software behaves.

---

# 4. Core Engines

Core Engines provide the runtime capabilities required by every SmartCore system.

Examples include:

* Semantic Engine
* Rule Engine
* Event Engine
* Workflow Engine
* Automation Engine
* Policy Engine
* Query Engine

Core Engines execute semantic models.

They do not define business concepts.

---

# 5. Capability Platforms

Capability Platforms provide reusable functional capabilities that can be shared across many domains and solutions.

This document uses the term Platform Capability to refer to an architectural capability provided by a platform. This is distinct from Semantic Capability, which is defined in [046_SmartCore_Semantic_Glossary.md](046_SmartCore_Semantic_Glossary.md).

Examples include:

* SmartCore Identity
* SmartCore Finance
* SmartCore Business
* SmartCore IoT
* SmartCore Security
* SmartCore Communication
* SmartCore Analytics
* SmartCore AI
* SmartCore Workflow

A Capability Platform represents a reusable area of expertise.

It is not an application.

It is not a customer solution.

Multiple solutions may depend on the same capability platform.

---

# 6. Domain Models

Domain Models describe the concepts of the real world.

Examples include:

* Person
* Organization
* Resource
* Asset
* Contract
* Ledger
* Transaction
* Device
* Building
* Location
* Reservation
* Calendar
* Invoice
* Product
* Service

Domain Models are implementation-independent.

They define meaning rather than behavior.

A Domain Model may be reused by multiple Capability Platforms.

---

# 7. Solutions

Solutions combine Domain Models and Capability Platforms to solve a real-world problem.

In this document, a Solution is a composition of platforms and domain models addressing a business problem. An Application is a software implementation that realizes one or more solutions.

Examples include:

* Manufacturing ERP
* Warehouse Management
* Smart Building
* Hospital Management
* Hotel Management
* Salon Management
* School Management
* Property Management

Solutions are composed.

They are not foundational.

They may evolve independently without affecting the Foundation.

---

# 8. Developer Platform

The Developer Platform enables developers to build on SmartCore.

Examples include:

* SDKs
* CLI
* Visual Designer
* Workflow Designer
* Rule Designer
* Code Generator
* Documentation Generator
* Testing Tools
* Migration Tools

Developer tools are consumers of the platform architecture.

They do not define the architecture itself.

---

# 9. Relationship Between Ecosystem Components

The primary compositional dependency among the layer-aligned ecosystem components is strictly one-way, and is nested within — not an alternative to — the canonical top-to-bottom dependency direction defined in 048§5:

```
Foundation
      ↓
Capability Platforms
      ↓
Domain Models
      ↓
Solutions
```

Core Engines and Developer Platform are cross-cutting components (see §2.1) and are intentionally not shown as steps in this chain, since neither is a distinct top-level layer:

```
                Core Engines
        (cross-cutting: executes semantic
         models used by Foundation and
         Capability Platforms)

Foundation → Capability Platforms → Domain Models → Solutions

                Developer Platform
        (cross-cutting: tooling support
         spanning Domain Models, Solutions,
         and Application Implementation)
```

Consistent with the dependency rules defined in 048§5, earlier components in this compositional view do not depend on later components.

Later components may compose earlier components.

No circular dependencies are permitted.

This ordering is descriptive of, and consistent with, the canonical layer dependency direction in 048§5 (Layer 1 → Layer 6); it does not introduce an independent rule. See §2.1 for how each component maps onto that canonical stack.

---

# 10. Architectural Principles

The SmartCore Platform follows these principles:

* Foundation is stable.
* Capabilities are reusable.
* Domains describe reality.
* Solutions solve business problems.
* Applications are compositions, not foundations.
* Tooling supports development but does not influence semantics.

---

# 11. Examples

## Correct

```
SmartCore Finance

    ├── Ledger
    ├── Wallet
    ├── Invoice
    └── Transaction
```

Finance provides reusable financial capabilities.

---

## Correct

```
Manufacturing ERP

    ├── Finance
    ├── Business
    ├── Identity
    ├── Organization
    ├── Inventory
    └── Workflow
```

Manufacturing ERP is a solution built by composing multiple capability platforms and domain models.

---

## Incorrect

```
Finance
Manufacturing ERP
Salon
Hospital

(all treated as peers)
```

Applications and capability platforms must never be modeled at the same architectural level.

---

# 12. Architectural Boundaries

The following concepts are explicitly distinguished.

| Concept             | Responsibility                          |
| ------------------- | --------------------------------------- |
| Foundation          | Defines the semantic language           |
| Core Engine         | Executes semantic models                |
| Capability Platform | Provides reusable platform capabilities |
| Domain Model        | Represents real-world concepts          |
| Solution            | Solves a business problem               |
| Developer Platform  | Supports software development           |

Each concept occupies a unique architectural position.

---

# 13. Future Evolution

New capability platforms may be introduced without modifying the Foundation.

New domain models may be introduced without modifying existing capability platforms.

New solutions may be created by composing existing domains and capabilities.

This ecosystem composition, nested within the canonical layer stack defined in 048, enables long-term scalability while preserving architectural stability.

---

# 14. Final Principle

The SmartCore Platform is **not a collection of applications**.

It is a layered semantic platform for building reusable capabilities, domain models, and complete solutions.

Applications are outcomes of the platform—not the platform itself.

---

# Change Log

## Version 1.3 (2026-07-13)

**Refinement (review feedback):** §9 previously stated "Earlier
components in the primary chain must never depend on later components,"
which read as an independent normative rule issued by this Reference
Architecture View document, rather than a restatement of the dependency
rule already established as canonical and normative in
048_SmartCore_Architecture& Taxonomy_Layer_Model.md §5. Reworded to:
"Consistent with the dependency rules defined in 048§5, earlier
components in this compositional view do not depend on later
components," and added an explicit closing statement that this ordering
"does not introduce an independent rule." This keeps 048 as the sole
source of normative dependency rules and this document strictly
descriptive/reference in nature, consistent with its Draft status and
its Scope statement that it does not redefine 048's canonical taxonomy.

**Classification:** Level 1 — Editorial per 051§5 (wording precision
only; no change to which rules govern dependency direction).

## Version 1.2 (2026-07-13)

**Refinements to the v1.1 correction (review feedback):**

- **Capability Platforms mapping corrected.** §2.1 previously mapped
  Capability Platforms directly to "Layer 2 — Platform Taxonomy." This
  conflated the classification model with the elements it classifies.
  Per 049§4 (Platform Families), Platform Taxonomy is the classification
  layer; Capability Platforms are architectural elements defined *within*
  it. §2.1 now states this distinction explicitly.
- **Core Engines / Developer Platform no longer shown inline in a single
  vertical chain.** §2 and §9 previously displayed all six ecosystem
  components as one arrow-connected vertical sequence, which visually
  read as a seventh layer stack despite §2.1 already classifying Core
  Engines and Developer Platform as cross-cutting, non-layer components.
  Both sections now separate the four layer-aligned components (primary
  chain) from the two cross-cutting components (shown alongside, not
  in-line).
- **Change Log wording precision.** "No architectural content changed"
  (v1.1 entry) replaced with "No normative architectural rule changed,"
  since the v1.1 correction did change this document's presentation and
  structure, just not any binding rule.

**Classification:** Level 1 — Editorial per 051§5 (wording precision and
diagram clarity; no conceptual or normative change beyond what v1.1
already introduced).

## Version 1.1 (2026-07-13)

**Issue Identified:** §2 previously presented an independent six-item
"Architectural Layers" stack (Foundation, Core Engines, Capability
Platforms, Domain Models, Solutions, Developer Platform) with its own
top-to-bottom dependency rules in §9. This stack did not correspond to,
and was not reconciled with, the canonical six-layer stack defined in
048_SmartCore_Architecture& Taxonomy_Layer_Model.md §3 (Semantic
Foundation, Platform Taxonomy, Domain Modeling, Solution Design,
Application Implementation, Infrastructure & Runtime). 048§9 states that
048 is the only canonical architecture layer model and that no other
document SHALL introduce an alternative layer hierarchy; §2 as previously
written did exactly that, despite this document's own Scope stating it
does not replace or redefine 048's canonical taxonomy.

**Additional defect corrected:** §2 also self-referenced itself
incorrectly, citing "047_SmartCore_Architecture&Taxonomy_Layer_Model.md"
as the source of the canonical Architecture Layer Taxonomy View. The
correct source is 048_SmartCore_Architecture& Taxonomy_Layer_Model.md,
as already correctly cited elsewhere in this document's own Scope
section.

**Resolution:**
- Renamed §2 from "Architectural Layers" to "Platform Ecosystem
  Composition View" and added an explicit statement that this section
  describes ecosystem components nested within 048's canonical layers,
  not an alternative layer hierarchy.
- Added §2.1, an explicit mapping table reconciling each of this
  document's six ecosystem components to their corresponding 048
  canonical layer (or noting where a component is a cross-cutting
  concern with no direct 048 layer counterpart, namely Core Engines and
  Developer Platform).
- Renamed §9 from "Relationship Between Layers" to "Relationship Between
  Ecosystem Components" and clarified that its dependency direction is
  nested within, not an alternative to, the canonical dependency
  direction defined in 048§5.
- Corrected the self-reference defect in §2 (047 → 048).
- Adjusted §13 wording to avoid implying an independently layered
  architecture.

**Classification:** Level 2 — Documentation clarification per
051_SmartCore_Governance_and_Decision_Model.md §5. No normative
architectural rule changed in either document; no ADR required. The
presentation of this document's ecosystem composition changed (§2/§9
restructured, §2.1 mapping added), but the underlying architectural
substance — including the canonical layer stack defined in 048 — is
unchanged.

**Note:** This document's Status remains Draft. No other content in
this document was changed.

## Version 1.0

- Initial Reference Architecture View definition.

---

**END OF DOCUMENT**