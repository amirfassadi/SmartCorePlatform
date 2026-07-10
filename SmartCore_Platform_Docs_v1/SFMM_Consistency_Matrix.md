# SFMM Consistency Matrix

Version: 1.0
Status: Audit Only

---

| Document | Terminology | Layers | Responsibilities | Dependencies | Cross-References | Overall |
|---|---|---|---|---|---|---|
| [000_SmartCore_Vision.md](000_SmartCore_Vision.md) | Partial | Partial | Partial | Partial | Partial | Partial |
| [001_SmartCore_Foundational_Principles.md](001_SmartCore_Foundational_Principles.md) | Partial | Weak | Partial | Partial | Partial | Partial |
| [002_SmartCore_Meta_Model.md](002_SmartCore_Meta_Model.md) | Strong | Partial | Strong | Partial | Partial | Partial |
| [003_SmartCore_Modeling_Rules.md](003_SmartCore_Modeling_Rules.md) | Strong | Partial | Partial | Partial | Partial | Partial |
| [005_SmartCore_Domain_Layer.md](005_SmartCore_Domain_Layer.md) | Partial | Partial | Partial | Partial | Partial | Partial |
| [031_SmartCore_Core_Vocabulary.md](031_SmartCore_Core_Vocabulary.md) | Partial | Partial | Partial | Partial | Weak | Partial |
| [032_SmartCore_Domain_Modeling_Rules.md](032_SmartCore_Domain_Modeling_Rules.md) | Partial | Partial | Partial | Partial | Partial | Partial |
| [033_SmartCore_Execution_Boundary_Model.md](033_SmartCore_Execution_Boundary_Model.md) | Partial | Strong | Strong | Strong | Partial | Partial |
| [034_SmartCore_Runtime_Model.md](034_SmartCore_Runtime_Model.md) | Partial | Partial | Partial | Partial | Partial | Partial |
| [042_SmartCore_Capability_Model.md](042_SmartCore_Capability_Model.md) | Weak | Weak | Weak | Partial | Partial | Weak |
| [046_SmartCore_Semantic_Glossary.md](046_SmartCore_Semantic_Glossary.md) | Strong | Partial | Strong | Partial | Partial | Partial |
| [046_SmartCore_Platform_Architecture.md](046_SmartCore_Platform_Architecture.md) | Partial | Weak | Weak | Partial | Partial | Weak |
| [ADR-0001b_SFMM_v1_FREEZE.md](ADR-0001b_SFMM_v1_FREEZE.md) | Partial | Weak | Partial | Partial | Partial | Partial |

---

## Interpretation

- Strong: the document is broadly aligned with the rest of the set.
- Partial: the document is understandable but leaves some ambiguity or drift.
- Weak: the document conflicts with the surrounding model or uses terms in a way that is not yet reconciled.

## Key Conclusions

- The semantic core is relatively coherent.
- The architecture layer model is not yet unified.
- Capability, domain, and application responsibilities remain under-specified.
- Cross-document navigation is not yet reliable enough for freeze.
