# ADR-0001b

Version: 1.2 (Amendment to ADR-0001)

Status: ACCEPTED (Revised)

Date: 2026-07-05

Last Updated: 2026-07-14

Authors:
SmartCore Architecture Team

---

# 1. Purpose of this Amendment

This document amends ADR-0001 to clarify the architectural boundary between:

- SFMM (Semantic Foundation Model)
- Platform Taxonomy (SmartCore Architecture Structure)
- Domain Modeling Phase

This amendment does NOT modify SFMM v1.0 semantics.

It only clarifies post-freeze architectural structure.

---

# 2. Clarification of Freeze Scope

The SFMM v1.0 freeze applies strictly to:

- Core Semantic Constructs
- Derived Semantic Constructs
- Vocabulary Layer
- Semantic Modeling Rules
- Semantic Responsibility Model

The SFMM freeze does NOT define:

- Platform architecture structure
- Capability definitions
- Domain-to-platform mapping
- Solution structure
- Application structure

These are explicitly outside SFMM scope.

---

# 3. Corrected Architectural Lifecycle

The SmartCore architecture lifecycle is formally defined as:

SFMM (Semantic Language Layer)
↓
Platform Taxonomy (Structural Layer - 049)
↓
Domain Modeling (Reality Layer)
↓
Solution Design (Composition Layer)
↓
Application Implementation

---

# 4. Introduction of Platform Taxonomy Layer

A missing architectural layer is formally recognized:

## Platform Taxonomy Layer (Document 049)

This layer defines:

- Capability Platforms
- Domain boundaries within platform context
- Structural grouping of SmartCore modules
- Relationship between capabilities and domains
- Separation of system-level vs product-level concepts

### Important clarification:

The Platform Taxonomy Layer is NOT part of SFMM.

It is a structural interpretation layer built on top of SFMM.

---

# 5. Key Architectural Correction

Previous assumption:

> SFMM → Directly enables Domain Modeling

Corrected model:

> SFMM → Defines language only  
> Platform Taxonomy → Defines system structure  
> Domain Modeling → Applies language within structure  

---

# 6. Separation of Concerns (Strict Rule)

## SFMM Responsibility

- Defines how reality is modeled
- Defines semantic primitives
- Defines relationships and rules of meaning

## Platform Taxonomy Responsibility

- Defines how SmartCore is organized
- Defines capability boundaries
- Defines system modularization

## Domain Modeling Responsibility

- Uses SFMM language
- Operates within Platform Taxonomy structure
- Models real-world domains

---

# 7. Impact on Existing ADR-0001

All previous statements in ADR-0001 remain valid EXCEPT:

- Any implication that Domain Modeling follows SFMM directly is now deprecated
- A structural layer (049) is formally inserted between SFMM and Domain Modeling

---

# 8. Consequences

- SFMM v1.0 remains frozen and unchanged
- Platform Architecture (049) is now formally required before Domain Modeling
- Domain modeling cannot begin without Platform Taxonomy definition
- Architecture becomes explicitly layered and non-ambiguous

---

# 9. Governance Update

From this amendment forward:

- SFMM changes require new ADR
- Platform Taxonomy changes require new ADR
- Domain structure changes require new ADR

Each layer evolves independently but must respect dependency order.

---

# 10. Final Resolution

The SmartCore architecture is now formally divided into:

1. Semantic Foundation (SFMM)
2. Structural Platform Taxonomy (049)
3. Domain Modeling Layer
4. Solution Layer
5. Application Layer

This resolves previously observed ambiguity between capability, domain, and application concepts.

---

# 11. Final Statement

SFMM is frozen as a semantic language.

Platform structure is now explicitly defined as a separate architectural layer.

Domain modeling may now proceed with clear structural boundaries.

---

# 12. Change History

## Version 1.2 (2026-07-14)

**Issue Identified:** Throughout this document (§3, §4, §7, §8, §10), the
Platform Taxonomy layer introduced by this amendment was cited as
"Document 046." This was a document-numbering error. Per
048_SmartCore_Architecture& Taxonomy_Layer_Model.md §4 and
049_SmartCore_Platform_Taxonomy.md, Document 046 is the Semantic
Glossary; the Platform Taxonomy document is **049**
(049_SmartCore_Platform_Taxonomy.md). Because this ADR is the
authorizing decision record cited by 048§4 for the introduction of the
Platform Taxonomy layer, the incorrect self-citation broke the
traceability chain between the layer's definition (048) and its
authorizing decision (this document).

**Resolution:** Corrected all five occurrences of "046" referring to
the Platform Taxonomy layer to "049" (§3 lifecycle diagram, §4 section
heading, §7 impact statement, §8 consequences, §10 final resolution
list).

**Scope of Change:** This is a citation/numbering correction only. No
architectural decision, boundary, rationale, or consequence introduced
by this ADR is altered. The substantive decision — that a structural
Platform Taxonomy layer sits between SFMM and Domain Modeling — remains
unchanged.

**Classification:** Level 2 — Documentation clarification per
051_SmartCore_Governance_and_Decision_Model.md §5 (reference/numbering
correction; no change to the decision, its rationale, or its
consequences). No new ADR required for this correction itself.

## Version 1.1 (2026-07-05)

- Initial amendment to ADR-0001: formal introduction of the Platform
  Taxonomy layer between SFMM and Domain Modeling.

---

END OF ADR-0001b