# SFMM Freeze Blockers

Version: 1.0
Status: Pre-Freeze Audit

---

| ID | Document | Section | Description | Severity | Reason | Suggested action |
|---|---|---|---|---|---|---|
| FB-01 | [031_SmartCore_Core_Vocabulary.md](031_SmartCore_Core_Vocabulary.md) | Level 0 (Reference) | References a missing document named “005_SmartCore_Semantic_Grammar.md”. | High | Broken reference weakens the core vocabulary chain and undermines trust in the documentation set. | Replace the reference with the correct existing document or remove it until the target is added. |
| FB-02 | [016_SmartCore_Production_Deployment_and_Scaling_Model.md](016_SmartCore_Production_Deployment_and_Scaling_Model.md) | Section 1 | References “Document 015” but no such document exists in the set. | High | The deployment architecture cannot be verified against a missing dependency. | Replace the reference with the correct document or remove it. |
| FB-03 | [001_SmartCore_Foundational_Principles.md](001_SmartCore_Foundational_Principles.md) | Section 2 | Defines a separate four-layer model for the semantic foundation. | High | It conflicts with the architecture-layer model in [047_SmartCore_Architecture& Taxonomy_Layer_Model.md](047_SmartCore_Architecture&%20Taxonomy_Layer_Model.md) and the reference architecture in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md). | Reconcile the layer definitions into one canonical layer model before freeze. |
| FB-04 | [042_SmartCore_Capability_Model.md](042_SmartCore_Capability_Model.md) | Sections 1–4 | Defines Capability as a semantic property of a Thing. | High | The semantic use of Capability conflicts with the architectural use of Capability Platforms in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) and [049_SmartCore_Platform_Taxonomy.md](049_SmartCore_Platform_Taxonomy.md). | Define one authoritative meaning for Capability and map the semantic and platform usages explicitly. |
| FB-05 | [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) and [047_SmartCore_Architecture& Taxonomy_Layer_Model.md](047_SmartCore_Architecture&%20Taxonomy_Layer_Model.md) | Architecture sections | Both define architectural structure, but their scopes and layer names differ. | Critical | The documentation does not present one authoritative architectural model. | Establish a single canonical architecture layer definition and make the other documents point to it. |
| FB-06 | [016_SmartCore_Production_Deployment_and_Scaling_Model.md](016_SmartCore_Production_Deployment_and_Scaling_Model.md) | Entire document | Uses mixed English and Persian content. | Medium | Editorial inconsistency reduces publication quality and weakens the normative authority of the document. | Normalize the language and style before public release or freeze. |
| FB-07 | [051_SmartCore_Governance_and_Decision_Model.md](051_SmartCore_Governance_and_Decision_Model.md) | Governance policy | Governance text does not fully align with the freeze scope introduced in [ADR-0001b_SFMM_v1_FREEZE.md](ADR-0001b_SFMM_v1_FREEZE.md). | Medium | The governance package and the freeze scope do not yet present a single story. | Align the governance model and the ADR freeze scope before freeze. |

---

## Summary

The documentation set contains multiple blockers that prevent a clean freeze decision. The most severe blocker is the absence of one canonical, non-conflicting layer model and the unresolved split between semantic capability and platform capability.
