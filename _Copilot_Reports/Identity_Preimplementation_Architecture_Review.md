# Identity preimplementation architecture review

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: analyst review with open findings, NOT architecture approval or a complete architectural gate PASS.
Reviewer/executor: Codex assistant. Accountable decision owner: Amir (@amirfassadi), not impersonated by this review.
Inputs: Platform `5ea92766f480fc8d16bc337272b4595078fe3112`; Identity registration proposal `ee9ffb767ed84165557793d8583b0750d887027b`. Output is its containing commit.

## Scope and method

Reviewed source clauses rather than checker counts. Read complete 004/026/028/029/030/031/032/041/058/060/061/062/063 core documents, complete legacy 09 operative §§1–10 and current 09; reviewed relevant 027 §17.1, full 057/059 including ownership/registration/lifecycle and dependency clauses and 064 required-content clauses. Related ADR, gate/field/decision reports and earlier foundation review provide additional evidence, explicitly not a substitute for an independent whole-foundation audit. Source details and remaining scope are listed below; no unseen standard is assumed validated.

## Model and execution boundary assessment

| Area | Source and assessed contract | Result / limit |
|---|---|---|
| Identity scope | 059 §§1–4; 01 five roots; 14 MVP | Identity has no Finance/IoT/business permission logic in the reviewed contracts. Non-human identities and lifecycle administration remain future scope; no runtime dependency graph exists yet |
| Ownership | 057 §§3/5/8; 09 §5.1 | Personal Organization/Owner Membership is atomic with Person and supporting registration state. Person-owned Resource shortcut is not introduced; proposed ADR-0002 scope still needs approval |
| Supporting workflow | 03 §9.1 / 01 §11 / 09 §§6/11 | PendingCredential/Ready is application process state, not Person lifecycle or a sixth Aggregate. Ready fact/event/ack is local and guard-protected; no distributed transaction/2PC implied |
| Credential | ADR-0004; 07 §3 / 09 §§4/11 | Winner fixed at Credential commit, durable guard until acknowledged Ready, current eligibility checked again. Prior accepted scope is preserved; runtime guard/concurrency remains unverified |
| Command targets | 027 §17.1; 04/09 | RegisterPerson exception is explicitly proposed, narrow and ineffective until approval. Other active Draft writes remain local; proposed all-Session password-change protocol must receive its own reviewed coordination disposition |
| Events | 026 §§8/17/20; 06/07/09 | Ready-time OccurredAt differs from ownership timestamp; LoginFailed is restricted Security Event. Immutable Event identity/dedup and no speculative facts are preserved. Wrapper T16 and unresolved correlation disposition remain open |
| Reads/security | 028 §§8/19/20; 05 and 07 lookup | Read-only DTOs omit token/password; service lookup is narrow and may see PendingCredential. Cross-Aggregate reads, query paging and tenant scope need the dispositions below |
| Layers/packages | 032 §§4/7; 060 §§5–11; 061 §§7–9; 063 §§2/5 | Runtime adapters/orchestration must stay outside domain semantics. Separate repository layout is permitted; no imports of another capability's internals. Concrete source/project references must be checked after implementation |
| Persistence | Complete legacy body and current 09 | [Legacy comparison](Identity_Persistence_Legacy_Content_Review.md) identifies superseded behaviors and restored explicit constraints. Line reduction is not a validation criterion |
| Consumers | 026 §21; 060/063 examples; 06 §10 | [Registry](Identity_Event_Consumer_Registry.md) declares all Events but all subscriptions remain UNKNOWN. Illustrative consumer names are not deployed inventory or access authorization |

## Open architectural findings

| ID | Two source locations / evidence | Consequence | Proposed resolution and owner |
|---|---|---|---|
| A01 | 065 V-002; 04 §4.5 | No resulting Event declared for RefreshSession under literal rule | Review bounded exception or real commit-backed Event alternative in the rule draft; architecture owner, OPEN |
| A02 | 065 V-003; 05 organization Query / 028 §§8/27 | Exactly-one reference conflicts with legitimate result/authorization/supporting read composition | Review one-primary-result rule and declared dependencies; scope/version change cannot be editorial, OPEN |
| A03 | 028 §13 'all collection queries'; 05 §§2/6 and 08 routes | Three collection Queries omit pagination even though their current results are bounded | Prefer a governed bounded-result exception for single Personal Organization/Membership and the explicitly capped Sessions list; alternatively define versioned pagination contracts consistently. Bounds do not waive current rule; architecture owner, OPEN |
| A04 | 028 §20 mandatory tenant context; 057/059 Person-centric self identity/service lookup and 05 | It is unclear whether Organization TenantId is mandatory for global/self Identity queries or only organization-resource reads | Clarify Identity-owned self/service scope versus organization-resource tenancy through the authoritative model; never invent TenantId or allow unauthorized cross-tenant resource reads, OPEN |
| A05 | 060 §14 'first implementation slice' includes Identity/Business/Resource/IoT; 059 §1 first executable Identity; project Identity-first MVP | 'First implementation slice' may mean a roadmap milestone rather than first executable module; literal reading conflicts with one-capability entry | Proposed disposition: Identity first executable delivery, four-platform Foundation milestone later. Revise scope/sequence through governance if this interpretation is accepted. Do not alter §14 as an editorial fix, OPEN |
| A06 | 032 §11 says Grammar Compliance (029); actual 029 is Glossary | Wrong document identity prevents an unambiguous declared dependency | Vocabulary/validation-number pairs corrected against catalog in 032 v1.0.1; intended grammar authority still requires review; do not guess substitution, OPEN |
| A07 | 060 §15 number/title pairs; current repository document catalog | References consistently one position behind actual document numbers | Nine exact number/title pairs corrected in v1.0.1; titles/meaning unchanged. This fixes reference accuracy only |
| A08 | 064 §7 package extras; schemas/runbook/changelog currently in Identity directory | Draft extras permitted; published package status unresolved | Select standardized companion/package disposition without breaking schema paths; architecture owner, OPEN |
| A09 | 064/065/066 and Proposed ADR-0002/0003 | Coherent draft and limited PASS counts do not confer permission | Complete scope/source/ADR/standard dispositions and all four documentary gates; no signature or gate closure inferred |
| A10 | 06 unknown-actor LoginFailed correlation; events schema; field review F08 | Unknown actor currently still activates required correlation condition | Choose narrative/schema meaning with audit/privacy implications before adoption; security/architecture owner, OPEN |
| A11 | Active 04 static refresh/unchanged Sessions; S2/fence completion candidate | New proposed behavior and wire deadline fields are not active | Review actual BFF trust, both token deadlines, family ownership and cross-store login/refresh fence plus compatible migration; OPEN |
| A12 | 03/09 proposed ordered Person stream; wrapper candidate; consumer registry | Stream position, adapter fencing and bootstrap cannot be inferred from broker key or Person lookup | Review complete T16/transport/replay/consumer ownership and compatibility, OPEN |

| A13 | 004 §8.4 / 062 §5; 01 §7 service responsibility verbs | 'Create Session/check Credential' could be implemented as infrastructure inside Domain Services | Clarified 01 §12: application obtains supplied evidence/objects and persists results; Domain Services perform no repository/API/Engine calls. Runtime boundaries remain unverified |
| A14 | Normative 058 §§1/3/6/9/10; current 059 §6 and Identity 04/08 | Foundation milestone is IoT-focused; old registration flow says return authentication result and lists both contacts | Distinguish later IoT Foundation exit criteria from Identity-first delivery, and explicitly reconcile one verified contact/no registration Session. 'Authentication result' is not necessarily a token guarantee; record intended interpretation/amendment, OPEN |
| A15 | 059 §14 excludes Messaging dependency; 062 Messaging/Event Engines and current Outbox contracts | 'Messaging' may mean a capability dependency or a generic infrastructure port/engine | Clarify architectural naming/applicability; use ports/contracts without importing another capability's internals. Broker selection alone does not resolve the source wording, OPEN |

A03–A06 are newly documented source-scope findings, not a claim that 028/060 are already amended. They may be resolvable by an explicit governed applicability decision; unresolved exact authority remains visible. No new operational consumer/topology/rate/cryptographic policy is invented.

## Remaining architectural evidence

The prior 001–005 review leaves Time dimensional-overlay and source-precedence interpretation pending. 004/029–031/041/058/062 and the remaining 057/059 text have now been read; the semantic reduction below provides explicit candidate mappings. Full foundation/source-precedence disposition and criterion-by-criterion tracing to accepted ADRs still require review; reading is not approval. Complete ADR-0002/0003 acceptance-criterion dispositions, 065 full category coverage, contract compatibility, consumer/operations ownership and security-policy acceptance remain required. This report therefore advances the Architecture Validation Review but does not finish the complete Gate 3.

## Actual work completed versus permission

Use-case seven-field mapping, Aggregate invariant/relationship mapping, Command purposes and Query sorting/paging applicability are explicit in the active Draft. Legacy constraints restored and consumer unknowns declared. The 251-cell matrix is revised with evidence/status per cell. These are documentation changes preserving current behavior, not adoption of the validator/S2/T16 proposals. Tests and concrete database/adapter behavior remain unexecuted.

## Semantic reduction candidate (030 matrix; no new Core construct)

| Identity concept | Candidate semantic classification/composition | Evidence / constitution | Remaining limitation |
|---|---|---|---|
| Person | Continuant with stable identity and profile properties | Human subject represented by identity record | 031 Person and 041 identity independence; one contact is an MVP representation/policy, not definition of a person |
| Personal Organization | Continuant + ownership Relation + Rule | Constitutive ownership boundary | 031 Organization / 057; resources remain Organization-owned |
| Membership | Relation(Person, Organization) + Rule(Role/Status) + Time; reified record is an architectural Aggregate | Constitutive participation | 004 reification does not turn the underlying Relation into a new foundational Thing type |
| Credential | Protected representation/evidence linked to Person + validation Rule | Evidence of authentication material, never Person identity | Cryptographic/verification execution stays outside semantic Core; aggregate boundary follows consistency/guard rules |
| Session | Time-bounded authenticated interaction/relation with Person + eligibility Rules, reified stateful record | Constitutive authenticated context, not business Resource permission | 029 Session / 041 identifiers; temporary tokens do not replace Person identity |
| Domain/Security Event | Completed Occurrent/fact with stable Event identity | Evidence of the completed transition/rejection | PersonRegistered records Ready fact; LoginFailed records a rejection, no fabricated Person |
| Ready/verification/ack records | Representation of process state and immutable facts; workflow execution in application layer | Durable supporting evidence | No sixth business Aggregate, new Core construct, or conversion of Event/Relation type |

This decomposition shows a route to existing constructs without claiming final grammar compliance. 029's Thing-based glossary, 030's Continuant/Occurrent grammar and 004's five-construct wording need the same authoritative interpretation as prior 001–005 findings; Time is a dimension, not a new entity. No aggregate count or Core ontology is changed. Complete architectural sign-off and accepted source precedence remain open.
