<!--
File: SmartCore_Document_Lineage_Analysis.md
Last modified: 2026-07-14
-->

# SmartCore Document Lineage Analysis

Version: 1.3

Status: Draft — For Architecture Board Review

Classification: Governance Artifact (not an Audit Report)

Supersedes: SFMM_Document_Lineage_Analysis.md v1.0 (retitled; scope was
never limited to SFMM proper — it spans Governance, Identity, Runtime,
Blueprint, and Platform documents as well)

---

## Scope

This analysis evaluates document lineage, forward-reference activity, and
apparent architectural generations only.

It does **not** evaluate the technical correctness, semantic quality, or
implementation fitness of any individual document. A document flagged
"No Active Reference" in this analysis has no demonstrated consumer
within the set defined in §2.1 — that is a citation-graph finding, not a
statement about whether the document's content is sound. A document could
in principle be both well-written and currently unreferenced, or poorly
written and heavily cited; this analysis does not distinguish between
those cases and was not designed to.

---

## 1. Purpose

This document does not restate that documents 009–015 are missing from the
numbering sequence — that gap is already recorded as FB-01/FB-02 in
`SFMM_Freeze_Blockers.md` and in both cross-reference reports.

This document goes one layer deeper. It asks a prior question: **before
deciding whether to author or delete anything, is the surrounding series of
documents (013–022) still part of the canonical architecture at all?**

The method used is a **Forward Reference Graph** check: for each candidate
document, does any document currently treated as Normative or Governance-
authoritative cite it? (The composition of that reference set is not
assumed — it is defined explicitly in §2.1 below, precisely so that the
selection cannot be characterized as arbitrary.) A document with zero
forward citations from that set is not necessarily wrong or obsolete —
but it has no demonstrated consumer in the architecture as it stands
today.

This distinction matters because the evidence collected in this analysis
— specifically, the citation gaps documented in §5 and the same-subject
duplicate pairs documented in §6 — suggests that the project has
progressed through multiple architectural generations (SFMM Freeze →
Platform Taxonomy → Blueprint Standard → Validator → Governance Model →
AI Code Generation → Capability Platform Architecture, per ADR-0001 /
ADR-0001b) without earlier-generation documents ever being given an
explicit lifecycle status.

**All findings below are stated as evidentiary observations, not final
architectural rulings.** Only the Architecture Board can assign a binding
status. Where the evidence is strong, this is noted; where it is
inferential, it is flagged as such rather than presented as settled fact.

---

## 2. Method

For every document in the 009–022 range and its apparent duplicates
elsewhere in the corpus, three questions were asked:

1. **Is it cited by any document in the Normative / Governance-
   authoritative set defined in §2.1?**
2. **Is its subject matter still represented in the current architecture**,
   whether under the same name or a different one?
3. **Does another document appear to cover the same ground**, suggesting a
   second architectural generation was written without formally retiring
   the first?

No document was reclassified, edited, or deleted as part of this analysis.
This is an observation pass only.

### 2.1 Definition of the Reference Set Used in This Analysis

This section selects a **Reference Set** for the purpose of measuring
citation activity in §5 and §7. It is not, and is not intended to be, an
architectural ruling on which documents are Normative — that
determination belongs to the Architecture Board. The distinction matters
because the inclusion test used here and the measurement used later in
this analysis are deliberately different in scope, to avoid the set being
built and then re-validated using the same evidence:

- **Building the Reference Set (this section)** uses a broad test: does
  the document carry external indicators of current authority — a
  Status: Normative (or Stable) header **and** at least one citation by
  name from *any* other document anywhere in the corpus — or does it
  govern an active, unresolved decision (specifically, an ADR currently
  in Proposed status that gates a recorded freeze blocker, GOV-01)?
- **Measuring "Active Reference" in §5 and §7** uses a narrower test: is
  the document under review cited specifically **by a member of the
  Reference Set** produced above, as opposed to being cited anywhere in
  the general corpus?

These are two different questions asked at two different stages, using
two different scopes of "citation" — general-corpus citation to build the
list, and Reference-Set-only citation to evaluate documents against it.
Keeping them distinct is what allows §5 and §7 to report evidence about
016–022 without that evidence being defined in terms of itself.

Applying the broad, general-corpus test, the Reference Set used
throughout the remainder of this analysis is:

```
051  Governance and Decision Model      (Status: Normative)
057  Tenancy and Ownership Model        (Status: Normative)
059  Identity Platform                  (Status: Normative)
060  Codebase Architecture              (referenced by 059, 061; foundational to current implementation direction)
062  Core Engine Boundaries             (defines the execution model that superseded the DSL/Compiler/Runtime direction — see §4)
064  Blueprint Standard                 (Status: Stable)
065  Blueprint Validator Specification  (Status: Normative)
066  AI Code Generation Specification   (Status: Normative)
ADR-0002  Identity Foundation Clarifications          (Proposed — gates GOV-01)
ADR-0003  Organization/Membership Lifecycle Standard  (Proposed — gates GOV-01)
```

This set is deliberately narrow. Documents with Status: Draft, or with a
self-declared Status: Normative that no other document in the corpus
cites by name (see 026 vs. 035, §6), were intentionally excluded — under
the broad test above, not the narrow one — since self-declared status
without any external citation is exactly the condition this analysis is
trying to surface, not assume away. If the Architecture Board considers this set incomplete or
overly narrow, that is itself a Board-level decision this analysis does
not have the authority to make — but the set is stated explicitly here so
that any disagreement can be argued against a fixed, visible list rather
than an implicit one.

---

## 3. Findings — Documents 009–012

| Item | Observation |
|---|---|
| Forward references found | None, in any document in the corpus |
| Backward references found | None |
| Subject matter identifiable | No — content cannot be inferred |

**Current evidence: Reserved / Historical Gap.** There is no evidence
available to determine whether these numbers were reserved and never
filled, whether documents once existed and were lost, or whether the
project moved past that architectural branch before writing them. No
document should be authored for 009–012 until evidence surfaces.

---

## 4. Findings — Documents 013–015 (DSL / Compiler / Runtime)

| Doc | Referenced by | Subject matter | Current-architecture successor |
|---|---|---|---|
| 013 (DSL) | Named only in `016§15` as a predecessor label | Not described anywhere | No direct successor identified |
| 014 (Compiler) | Named only in `016§15` as a predecessor label | Not described anywhere | No direct successor identified |
| 015 (Runtime) | Named in `016§15`, `017§16`, `018§17`, `019§19` — all within the same 016–019 series, none of them part of the §2.1 set | Implied: "executes graph deterministically" | Possibly `034_SmartCore_Runtime_Model.md`, though its content (Command/Query/Event/Process/Job) does not match the "DSL → Compiler → executable graph" pipeline described for 015 |

A search across the full corpus for "DSL" and "Compiler" as architectural
terms returns no results outside `016§15`. The pipeline these three
documents imply — DSL → Compiler → Runtime graph execution — is not
described, extended, or referenced by `033_Execution_Boundary_Model.md`,
`034_Runtime_Model.md`, or `062_Core_Engine_Boundaries.md`, all of which
address execution/runtime concerns through a different architecture (Core
Engines: Rule Engine, Event Engine, Workflow Engine, Scheduler, Policy
Engine, Messaging Engine).

**Assessment: No evidence of continued architectural adoption.** This is
an inference from absence, not a confirmed fact — it is possible these
documents were planned but never written, rather than written and later
abandoned. Either way, authoring 013–015 today to satisfy the 016–019
cross-references would risk formalizing a design direction the current
Core Engine architecture does not appear to follow.

---

## 5. Findings — Documents 016–022 Forward-Reference Status

| Doc | Title | Cited by the §2.1 Normative/Governance set? | Current evidence |
|---|---|---|---|
| 016 | Production Deployment & Scaling Model | No | No Active Reference |
| 017 | Failure Model & Recovery Semantics | No | No Active Reference |
| 018 | Security & Permission Semantics | No | No Active Reference |
| 019 | Identity & Session Continuity Model | **Yes** — listed in the References section of both `ADR-0002` and `ADR-0003` | Active Reference |
| 020 | Time & Temporal Model | No | No Active Reference |
| 021 | Value & Economic Semantics | No | No Active Reference |
| 022 | Messaging & Event Communication Model | No | No Active Reference |

None of 016, 017, 018, 020, 021, or 022 is contradicted by current
architecture as far as this pass could determine — they simply have no
demonstrated consumer within the set defined in §2.1. "No Active
Reference" is used deliberately in place of "Legacy": no ADR has yet made
that determination, and this analysis does not have the authority to make
it either.

019 is the one document in this series with a direct, current, citable
tie to active governance work (ADR-0002, ADR-0003 — the same ADRs that
gate GOV-01). Its disposition should be resolved as part of, or before,
the GOV-01 closure, rather than left for a separate pass.

---

## 6. Duplicate Track Findings

Independent of the numbering gap, this pass surfaced same-subject
documents that appear to belong to different architectural generations,
with no ADR establishing a Supersedes / Superseded-By relationship between
them.

The diagram below is illustrative, not authoritative — it exists only to
make the lineage pattern visible at a glance. Each row is an independent
subject track; there is no claim that these tracks share a single global
"Generation A / B / C" timeline, only that within each row, a later
document appears to cover the same ground as an earlier one without any
recorded Supersedes relationship.

```
ILLUSTRATIVE ONLY — dotted arrows denote apparent conceptual succession,
NOT a confirmed or formal Supersedes relationship.

Identity        019  ⋯⋯⋯⋯▶  041  ⋯⋯⋯⋯▶  059 (Normative, in §2.1 set)
Time            020  ⋯⋯⋯⋯▶  038
Value/Economic  007  ⋯⋯⋯⋯▶  021
Event Model     026  ⋯⋯ same title, no ordering evidence ⋯⋯▶  035
Governance      045  ⋯⋯⋯⋯▶  051 (Normative, in §2.1 set)
```

| Subject | Earlier-generation document | Later-generation document | Evidence of formal reconciliation? |
|---|---|---|---|
| Identity | `019_Identity_and_Session_Continuity_Model.md` | `041_Identity_Model.md`, `059_Identity_Platform.md` (Normative) | None found. Content is conceptually aligned across all three (persistent identity, session ≠ identity, delegated/future identity types), but no document states this relationship explicitly. |
| Time | `020_Time_and_Temporal_Model.md` | `038_Time_Model.md` | None found. Both define the same four temporal dimensions (Occurrence/Recording/Validity/Processing) in near-parallel structure. |
| Value / Economic | `007_SmartCore_Economic_Model.md`, `021_Value_and_Economic_Semantics.md` | (no clearly Normative later version identified) | None found. Two earlier-generation documents cover the same ground (Value as derived, Ownership as Relation, Ledger as projection) without one citing the other. |
| Event Model | `026_SmartCore_Event_Model.md` | `035_SmartCore_Event_Model.md` | None found. **Both documents carry the identical title.** They differ in structural emphasis (026: event categories/versioning/consumers; 035: event vs. command/state/record/message distinctions) but overlap substantially. Neither is cited by the §2.1 set, despite 026's own header declaring Status: Draft and 035's declaring Status: "Core Semantic Standard" — a self-declared status not corroborated by external citation, which is the exact pattern this analysis treats as evidence-only rather than authoritative (see §2.1). |
| Governance | `045_SmartCore_Governance_Model.md` | `051_SmartCore_Governance_and_Decision_Model.md` (Normative) | No formal supersession recorded, though 051 is the document cited throughout the current corpus and is part of the §2.1 set; 045 has no forward references from any document in that set. |

This is characterized here as a **Document Lineage** problem rather than a
Cross-Reference problem: the issue is not a broken link, but the absence
of any record of which generation of a concept is currently authoritative
when two full documents describe the same thing.

*Note for future work:* if the project's document count continues to
grow, this table is a reasonable candidate to be split out into its own
standalone tracking artifact (e.g. a running Migration/Reconciliation
Log) rather than remaining a section of this analysis. That decision is
left to the Architecture Board and is not acted on here.

---

## 7. Consolidated Disposition Table

| Document | Current Evidence | Referenced By | Replacement Candidate | Decision Needed |
|---|---|---|---|---|
| 009–012 | Unknown | — | — | Architecture Board (evidence-gathering only) |
| 013 (DSL) | No Active Reference | 016 (outside §2.1 set) | None identified | Architecture Board |
| 014 (Compiler) | No Active Reference | 016 (outside §2.1 set) | None identified | Architecture Board |
| 015 (Runtime) | No Active Reference | 016–019 (outside §2.1 set) | Possibly 034, unconfirmed | Architecture Board |
| 016 | No Active Reference | — | None identified | Architecture Board |
| 017 | No Active Reference | — | None identified | Architecture Board |
| 018 | No Active Reference | — | None identified | Architecture Board |
| 019 | **Active Reference** | ADR-0002, ADR-0003 | 041 + 059 (conceptually aligned, not confirmed as formal replacement) | Architecture Board — coordinate with GOV-01 |
| 020 | No Active Reference | — | 038 (conceptually aligned) | Architecture Board |
| 021 | No Active Reference | — | None identified; overlaps 007 | Architecture Board |
| 022 | No Active Reference | — | Partial overlap with 026/035 | Architecture Board |
| 007 | No Active Reference | — | Overlaps 021 | Architecture Board |
| 026 | Ambiguous (self-declared status, uncited) | — | Overlaps 035 (same title) | Architecture Board |
| 035 | Ambiguous (self-declared status, uncited) | — | Overlaps 026 (same title) | Architecture Board |
| 045 | No Active Reference | — | 051 (Active Reference, in §2.1 set) | Architecture Board |

---

## 8. Recommended Governance Actions

1. **Introduce a formal document status field.** Every SmartCore
   architecture document should declare exactly one of: `Canonical`,
   `Legacy`, `Superseded`, `Archived`, `Draft`. This status is currently
   absent from the documentation model entirely —
   `051_Governance_and_Decision_Model.md` defines versioning and decision
   levels but not document lifecycle status.

2. **Introduce a Supersession rule.** Any document that replaces another
   should carry an explicit `Supersedes: <doc>` reference, and the
   replaced document should carry `Superseded By: <doc>`. This closes the
   exact gap responsible for the 019/041/059, 020/038, 026/035, 045/051,
   and 007/021 pairs identified in §6.

3. **Resolve the Duplicate Track items through explicit Architecture
   Board decision**, not through silent deprecation. Each pair in §6
   should receive its own disposition record (which document is
   authoritative, what happens to the other).

4. **Close the 009–015 gap through architectural decision, not document
   authoring.** Do not write 013, 014, or 015 to satisfy the 016–019
   cross-references until the Board has determined whether 016–019
   themselves remain Canonical, and whether the DSL/Compiler/Runtime
   pipeline they imply still reflects current architecture (as opposed
   to the Core Engine model in 060/062). If the Architecture Board
   ultimately classifies 016–019 as Legacy, the broken references in
   FB-01/FB-02 are resolved by that reclassification alone, without new
   authoring.

5. **Prioritize 019's disposition alongside GOV-01.** Because 019 is the
   only document in the 016–022 series with a live citation from ADR-0002
   and ADR-0003, its status should be settled as part of — or immediately
   before — those ADRs' move from Proposed to Accepted, so that
   acceptance does not silently ratify an unresolved lineage question.

---

## 9. Explicit Non-Findings

To keep this document's claims falsifiable, the following are noted as
things this analysis did **not** establish:

- Whether 013–015 were ever written and lost, or never written at all.
- Whether 016–019's absence from the §2.1 set reflects a deliberate
  architectural decision or simple oversight during later drafting
  phases.
- Whether 041/059 were intentionally written as 019's replacement, or
  independently, with the overlap being coincidental convergence rather
  than a planned succession.
- Whether the §2.1 selection criteria themselves are the correct
  criteria — they are stated explicitly so they can be challenged, not
  presented as beyond dispute.

These require input from whoever authored the later-generation documents,
not further textual analysis.

---

## 10. Change Log

### Version 1.3

- Rewrote §2.1 to eliminate an apparent circularity: the section now
  explicitly separates the broad, general-corpus citation test used to
  build the Reference Set from the narrower, Reference-Set-only citation
  test used to evaluate documents in §5 and §7, and is retitled
  "Definition of the Reference Set Used in This Analysis" to make clear
  it selects a measurement baseline rather than adjudicating Normativity.
- Moved the "illustrative only, not a confirmed Supersedes relationship"
  caveat onto the §6 diagram itself (previously it appeared only in the
  surrounding prose) and changed solid arrows to dotted arrows to reduce
  the risk of the diagram being read as asserting formal succession.

### Version 1.2

- Added a Scope section clarifying that this analysis evaluates lineage
  and reference activity only, not technical or semantic quality.
- Added an illustrative per-subject lineage diagram at the start of §6.
- Bumped version per the versioning convention recommended in §8, Action 1.

### Version 1.1

- Retitled from `SFMM_Document_Lineage_Analysis.md` to
  `SmartCore_Document_Lineage_Analysis.md` to match actual scope
  (Governance, Identity, Runtime, Blueprint, and Platform documents, not
  SFMM alone).
- Added §2.1, an explicit definition of the Normative / Governance-
  authoritative reference set, so the set is stated rather than assumed.
- Replaced the binary `Canonical: Yes/No` column with an evidence-scaled
  `Current Evidence: Active Reference / No Active Reference / Ambiguous`
  column in both §5 and §7, to avoid presenting a citation-graph finding
  as an architectural ruling.
- Softened conditional language in §8, Action 4, to explicitly attribute
  the Legacy classification decision to the Architecture Board rather
  than presenting it as a foregone conclusion.
- Added §9, Explicit Non-Findings, including an entry noting that the
  §2.1 selection criteria are themselves open to challenge.

### Version 1.0

- Initial analysis: identified the 009–015 numbering gap, assessed
  forward-reference status for 013–022, and surfaced five same-subject
  Duplicate Track pairs (019/041/059, 020/038, 007/021, 026/035,
  045/051).

---

## End of Document

<!--
File: SmartCore_Document_Lineage_Analysis.md
-->