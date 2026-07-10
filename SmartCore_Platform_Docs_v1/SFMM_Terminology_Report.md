# SFMM Terminology Report

Version: 1.0
Status: Pre-Freeze Audit

---

## 1. Terminology Consistency Findings

The following terms are used inconsistently across the documentation set:

| Term | Semantic use | Architectural use | Issue |
|---|---|---|---|
| Capability | Defined as a semantic ability of a Thing in [042_SmartCore_Capability_Model.md](042_SmartCore_Capability_Model.md) | Used as a reusable platform capability in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) and [049_SmartCore_Platform_Taxonomy.md](049_SmartCore_Platform_Taxonomy.md) | The same term means both semantic potential and architectural service. |
| Domain | Used as a modeling layer in [005_SmartCore_Domain_Layer.md](005_SmartCore_Domain_Layer.md) | Used as a platform architecture concept in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) | The term shifts between modeling and architecture scope. |
| Solution | Used as a composed business outcome in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) | Not clearly distinguished from Application in the broader architecture package | The boundary between solution and application is not explicit. |
| Module | Used as a governed architectural unit in [050_SmartCore_Module_Standards.md](050_SmartCore_Module_Standards.md) | Not consistently linked to Platform Taxonomy or Reference Architecture | The relationship between module and platform remains under-specified. |
| Application | Described as implementation-specific in [README.md](README.md) | Referenced as an architectural layer in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md) and [047_SmartCore_Architecture& Taxonomy_Layer_Model.md](047_SmartCore_Architecture&%20Taxonomy_Layer_Model.md) | The term is used at both business and implementation levels. |

---

## 2. Ambiguity Notes

The following statements are especially likely to be read in multiple ways:

- “A Capability Platform represents a reusable area of expertise.” in [047_SmartCore_Reference_Architecture.md](047_SmartCore_Reference_Architecture.md)
- “A domain is a consistent set of derived concepts built from the meta model.” in [005_SmartCore_Domain_Layer.md](005_SmartCore_Domain_Layer.md)
- “The API exposes Core capabilities.” in [023_SmartCore_API_Design_Guidelines.md](023_SmartCore_API_Design_Guidelines.md)

---

## 3. Conclusion

Terminology is close to coherent, but several key concepts are overloaded. These ambiguities are material enough to weaken the authority of the documentation package before freeze.
