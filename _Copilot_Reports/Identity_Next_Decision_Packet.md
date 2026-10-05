# Identity next decision packet

Version: 0.1.0 — Prepared 2026-10-04 (Asia/Tehran)
Status: Review-ready proposals / unsigned. No architectural acceptance, gate closure or implementation permission.
Owner for architectural decisions: Amir (@amirfassadi), per project authority and 051 §7. Operational/security execution roles still need assignment.

## Exact review sources

- Platform input: `630a22da53195a87d780aaf3c867bdd359eab83a`, branch review/slice0-evidence, PR #10. This incorporates prior integration and field-review evidence, not a merge into main.
- Identity input: `ee9ffb767ed84165557793d8583b0750d887027b`, registration reconciliation proposal; fetched again for this review, unchanged.
- This packet's output revision is its containing commit, identifiable through PR #10. At decision time pin the actual reviewed commit independently for each repository. Input pins are not accepted pins.
- Sources read for this step: 051 review/change/version sections, 065 §11 V-002/V-003/V-005/V-008, existing owner summary and acceptance form, SESSION candidate/S2 contract/checklist/map, T16 comparison, Identity 04/05/07/09/10 and SessionTokens schema, Identity GOV dossier. No new claim of full Foundation/legacy audit is made.

## Concrete choices prepared

| Decision | Recommended proposal | What is already directed | What still requires disposition |
|---|---|---|---|
| P01 Blueprint scope | One full human Identity MVP Blueprint, registration-first delivery phases | Identity is first MVP; minimal verified mobile OR email/name/password registration | Adopt this coherent scope and complete all its applicable gates; no silent new sub-Blueprint |
| P02 V-002 | Specifically governed RefreshSession no-result-Event exception; preserve ten public Events | No fabricated Event to satisfy checks | Review standard rule amendment/ADR and scope for current nonrotation versus S2 effects; actual internal fact remains an alternative |
| P03 V-003 | Exactly one primary result Aggregate; separately declare supporting read and authorization dependencies | Existing five Query DTO subjects are indexed | Approve normative meaning/version and machine validation fields; current literal rule remains authoritative |
| P04 T16 | Option A, durable per-Person ordered registration/profile application; concrete wrapper, no skip, stable replay | Project context favors ordered delivery; whole platform depends on Identity | Approve contract details, wrapper/version, dispatcher fencing, replay bootstrap, consumers and owners; no subscriber count invented |
| P05 SESSION | Preserve S2/BFF and recorded 900/86400/no-idle/all-Session password-change directions; distinguish two wire deadlines; durable issuance fence across login/refresh | These owner-selected directions are already documented, including strict reuse/lost-response reauthentication | Review actual BFF trust boundary, wire compatibility, cross-store Credential protocol, policy/keys/retention and operations |
| P06 GOV | Review exact ADR-0002 v1.8.0 sequencing and each decision; ADR-0003 independently; preserve scoped ADR-0004 acceptance | Runtime results cannot be claimed before code exists; approval still precedes implementation | Attributable accepted source/scope and complete documentary gate evidence, without bypassing 064 |

Prepared details:

- [V-002 / V-003 rule disposition](Identity_Validator_Rule_Disposition_Draft.md): candidate normative replacements, bounded exception, alternative designs and required validator failure cases.
- [T16 ordered contract](Identity_T16_Ordered_Contract_Candidate.md): transport fields, counter/enqueue atomicity, ambiguous acknowledgment, consumer checkpoints, collisions/gaps and admission/replay rules.
- [SESSION completion](Identity_SESSION_Contract_Completion_Candidate.md): wire expiry proposal, one-generation persistence, BFF stale-writer protection and explicit password-change/login/refresh fence phases.
- [Field review](Identity_Field_Contract_Review.md) and [stack proposal](Identity_Implementation_Stack_Proposal.md) remain separate evidence/recommendations.

None of P01–P06 is marked Accepted by 'continue'. P04 acknowledges conversation direction without manufacturing an attributable signed T16 record. P05 avoids reopening already recorded policy choices; design acceptance is still incomplete. A new governance ADR identifier is unassigned rather than guessing ADR-0005 availability.

## Remaining issue-to-gate work

| Issue / gate | Current evidence | Next documentary action | Completion observation |
|---|---|---|---|
| Structural / 064 Gate 1 | Subset 296 PASS, 6 WARN, 97 INFO; content matrix includes open/inferred cells | Resolve all required-content cells, package companion status under 064 §7 and exact version/dependency closure | Complete coverage report on the accepted coherent candidate; subset count alone is insufficient |
| Semantic / Gate 2 | 557 focused checks and ten payload-table matches; V-002/V-003, expiry/correlation/transport/runtime-boundary findings | Adopt or revise rule/policy dispositions; propagate one candidate; inspect every remaining narrative/schema/machine obligation | No undeclared contradiction or missing MVP contract; requirements mapped to design and applicable checks, not invented runtime PASS |
| Architectural / Gate 3 | Existing ADR/traceability reviews are partial; full Architecture Validation Review not done | Evaluate pinned model against foundations and platform/lifecycle ownership; close source-priority/Time interpretations where applicable; review legacy 09 requirements and governance changes | Explicit review findings, scope, resolved dispositions and responsible owner; no sign-off inferred from merge |
| AI Readiness / Gate 4 | generationAllowed=false; unresolved policy/standard TODOs | After preceding contract/governance work, audit consistent model, dependencies, examples, machine spec and accepted statuses against 064/065/066 | Required gate and quality evidence complete; only then change generation status through an accountable record |
| GOV ADR-0002/0003 | Proposed; ADR-0004 separately Accepted within signed scope | Criterion-by-criterion architecture/runtime sequencing, lifecycle review, exact accepted sources and decision dispositions | Owner's attributable decision and coherent authority references; signature alone does not certify all gates |
| Cross-repository propagation | Identity proposal intentionally pins older baseline with later amendments separately disclosed | After Platform disposition, update active proposal sources/notes and implementation plan; preserve uploaded archive and historical pins | Both commits pinned; chosen authority/consumer compatibility documented |
| Implementation/release verification | No runtime code/test evidence | After applicable architecture and code-entry gates, implement and run planned crash/race/security/consumer scenarios | Real code/environment/result reports; production/deployment approval stays separate |

Other remaining field decisions are not hidden: LoginFailed unknown-actor correlation, configurable bounds versus pinned schemas, endpoint-specific service errors and identity/time binding behavior remain in the field report. Selecting T16/S2 does not automatically close them. Security parameters and material handling need architectural review before dependent code; operational sizing may remain an explicit release prerequisite only when it does not leave MVP behavior undefined.

## Order of work after dispositions

1. Record rule/scope/T16/SESSION/GOV architectural dispositions, including required revisions rather than pretending every proposal is final. Name security/operations and consumer owners; distinguish project authority from verified deployment roles.
2. Prepare one coherent proposed Platform propagation: normative standards/ADR impact, narrative, wire/service/event and machine contracts, examples, test plan and compatibility. Review it before acceptance; do not change schemas based on a generic 'continue'.
3. Finish complete structural/semantic/architecture/readiness documentary evidence on that candidate; no required gate is waived. Update the Identity proposal in step with selected authoritative references and verify both trees.
4. After adopted architecture and all applicable code-entry gates, implement registration delivery first, then dependent provisioning/Ready/Session/event-consumer phases. Required runtime verification is executed on code, not backfilled into this document.

## Attributable disposition form

Record for each P01–P06: accepted/revised/rejected/deferred; exact clauses and scope; selected alternative/reason; version/migration impact; evidence reviewed and unresolved obligations; decision capacity/date; final reviewed Platform and Identity SHAs; governance ADR/record identifier; accountable execution roles. Accepted-source SHAs, signature/effective date and record identifier remain PENDING. A decision accepting design direction while requiring further detail must state those gates and cannot claim completed readiness.

## Check results on this publication

The change set updates review documentation only; active Blueprint, schemas, machine and standards are unchanged. Existing checks rerun: 557/557 focused contract checks; 430/430 limited package checks; 296 PASS / 6 WARN / 97 INFO structural subset; four isolated negative controls fail as intended. Relative links in changed review documents and git diff --check are checked. No complete Semantic/Architecture/AI gate PASS or runtime result is asserted.

## Readiness preparation follow-up — 2026-10-04

[Readiness status](Identity_Implementation_Readiness_Status.md) records completed legacy/content work and remaining gates. [Architecture review](Identity_Preimplementation_Architecture_Review.md) and [Foundation alignment candidate](Identity_Foundation_Alignment_Candidate.md) add precise pagination, tenant/scope, IoT milestone and dependency-name dispositions; none is silently accepted. Previous 557/430/296 counts above are historical results for that publication, not the updated subset totals.
