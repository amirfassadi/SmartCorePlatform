# Identity Slice 0: gate coverage and foundation review

Date: 2026-10-04 (Asia/Tehran). Executor: Codex, at owner's request. Status: review evidence, NOT an approval or a full validator PASS.

خلاصه: بررسی پنج سند پایه و تطبیق گیت‌ها انجام شد؛ checker گسترش یافت و سه ناسازگاری متنی با قرارداد فعلی اصلاح شد. چهار گیت هنوز اثبات نشده‌اند. انتخاب T16، پذیرش و انتشار قرارداد SESSION، تصویب دامنهٔ ADR-0002/0003 و تکمیل بررسی معنایی/قراردادی لازم است. تعداد PASSها گواه آمادگی شروع پیاده‌سازی نیست.

## 1. Exact inputs and reading scope

- Platform published input: `59e948d2dd975a9d4ecbf6f32255bc8303b5136c`, tree `f346c33d219097f6564c93445686d2b6107018e3`, branch `review/slice0-evidence`, draft PR #10 targeting `docs/identity-blueprint-completion`.
- Identity proposal: `ee9ffb767ed84165557793d8583b0750d887027b`; main remains `f72a4fdf9f29edd3970b4bd719bfbf8040089534`.
- GitHub API confirmed PR #10 open, Draft and mergeable at the start of this follow-up. Git mergeability is not architectural approval.
- Read all of Foundation documents 001–005 and the normative content of 064, 065, 066 and 051. Read current Identity 00–16 bodies for this review, the limited acceptance form, T16 comparison, SESSION decision candidate, and Identity's pinned registration README, implementation plan and GOV dossier. Historical changelogs were evidence, not current requirements.
- This is a foundation-focused architecture review. It is not a complete Architecture Validation Review against every dependency (026/027/047/048/057/059), field-by-field schema review, deployed consumer inventory, or security/runtime certification.
- The output revision is the commit containing this report. It differs from the input SHA; all checks below were rerun on the output working tree before publication.

## 2. Gate crosswalk

This is an evidence mapping, not a proposal to rewrite the standards. The four gates of 064 and the five quality checks of 065 are complementary views, not a proven contradictory gate count.

| 064 implementation gate | Relevant 065 categories/rules and quality checks | 066 relationship | Result and required closure |
|---|---|---|---|
| 1 Structural (§9.1) | §5 files/sections/headings/references/version/status/package; parts of §9 machine structure; §13 Blueprint Complete | §4 requires complete MVP and validation PASS | NOT ESTABLISHED. Mechanical checks pass, but content sufficiency, per-instance required coverage, semantic section order, full naming and reference applicability remain unclosed. Draft extras need disposition for published package. |
| 2 Semantic (§9.2) | §§6–10 narrative/machine, contracts, dependencies, MVP; V-001–V-010 as applicable; §13 Validation Passed | §§4/8 prohibit generation from incomplete or conflicting behavior | NOT ESTABLISHED. T16/SESSION, query/command/event mappings, consumer/version compatibility and complete schema field comparison remain open. Locating text is not sufficient. |
| 3 Architectural (§9.3) | Foundation compliance, §8 dependency direction, §13 Architecture Complete; §16 authority/governance integration | §§7/9 preserve authority and architecture | REVIEW PERFORMED, PASS NOT ESTABLISHED. See §4. No approval inherited from ADR-0004. ADR-0002/0003 acceptance and wider dependency review remain open. |
| 4 AI Readiness (§9.4) | Complete synchronized machine, explicit concepts/dependencies/no conflicts; §13 Ready For Generation | §4 requires READY FOR GENERATION, validation PASS, governance PASS, complete MVP | BLOCKED. Package is DRAFT, generationAllowed=false; unresolved policy/contract choices and unverified mappings prevent deterministic implementation. |

065 §13 Governance Approved is a separate necessary approval input across this process, not an automatic consequence of a technical PASS. 051 §7 requires approval before implementation; 065 §16 allows governance to reject even a technically passing package. 064 §9 explicitly covers implementation, including manual coding; 066 adds generation-specific preconditions.

Runtime race/crash/security results require implementation and are later verification evidence. 065 §10 requires documented tests; it does not itself say already executed tests must exist before all authoring can finish. Existing acceptance drafts/ADR criteria still need an explicit reviewed sequencing disposition where they impose stronger conditions. This report does not waive those criteria or label unexecuted tests PASS.

The proposed scoped form has been revised to make all applicable 064/065 gates a condition of implementation. It no longer presents owner signature plus a partial structural result as sufficient. No narrowed package or waiver has been adopted.

## 3. Structural coverage delivered

`tools/slice0_content_inventory.json` covers all 17 document content classes in 064 §8, with 96 individual document-level locators. The JSON records exact local evidence, not mandatory title wording. 064 defines required content but does not prescribe the literal heading text.

| Requirement | Method delivered | Evidence limit |
|---|---|---|
| Required package files | Existing 17 Markdown + machine checks | Presence only; additional working documents allowed while drafting |
| Sections/headings | Heading presence in all files; unique ascending numbered top-level headings; specification anchors for 5 Aggregates, 6 Commands, 5 Queries, 10 Events | Does not infer semantic order or sufficiency; per-instance required fields still reviewed separately |
| Required content | Complete 064 §8 locator inventory, explicitly INFO rather than PASS | A literal match confirms a location, not a requirement satisfied; common sections cannot silently replace every-item obligations |
| Required references | Parsed header dependency targets resolve uniquely; relative link paths; recursive machine paths and local JSON pointers resolve | Plain prose references, URL availability, Markdown anchors and conditional authority relevance not fully checked |
| Version/status | Headers/change logs/machine synchronization | Does not prove that a proposed version is accepted |
| Machine identifiers | Nonempty unique documents/aggregate/command/query/event identifiers | Complete required-field semantics and narrative equality remain open |
| Schema syntax | Draft-2020-12 schema self-validity and OpenAPI validity | No full fixture/field compatibility or runtime contract proof |

Current reproducible output: **296 PASS, 6 WARN, 97 INFO, zero executed FAIL**. Of INFO results, 96 are content locators and one is the link-scan completion marker. The six WARNs are the same draft package extras (schemas, runbook, task document, historical changelog). This is not an overall Structural PASS. An exit code of zero means no executed FAIL, not implementation permission.

The prior **88 PASS / 6 WARN** remains valid historical output of a smaller checker. The increased count reflects added checks, not a percentage of readiness.

### Per-instance coverage review under §8.3–8.7

The [required-content matrix](Identity_Slice0_Required_Content_Matrix.md) now inventories all 35 instances and every required field (251 cells). It distinguishes direct references, inferred combined fields and OPEN declarations. The matrix is completed evidence work, not proof all fields are satisfactory.

| Document | Coverage found | Remaining review/action |
|---|---|---|
| 02 Use Cases | Nine rows combine actor, preconditions/main flow and result/failure; interrupted-registration section covers shared alternatives | The matrix records seven-field coverage for each UC. Resolve inferred fields and OPEN alternatives. Goals and postconditions may be inferable from names/results; that inference is not certified. UC-004/008 internal substeps and UC-009 need their own applicable alternative/failure mappings. Do not invent new behavior to fill a template. |
| 03 Aggregates | Five named roots, child entities/VOs, lifecycle; shared consistency section; invariants and relationships split across 01/03/09 | The matrix traces seven required fields per root; resolve root-specific invariant completeness. Shared invariants are not proof every root has complete coverage. Keep references rather than duplicate domain rules. |
| 04 Commands | Six named operations with inputs, validation, coordination, failures/events distributed across local/shared sections | The matrix traces eight required fields per Command; review inferred purposes. RefreshSession explicitly emits no public event, which needs a disposition against literal V-002, not a fabricated event. Public command-to-contract and repository ownership mappings remain to certify. |
| 05 Queries | Five catalogue rows include scope, outputs and explicit pagination choices | Resolve/document V-003's exactly-one Aggregate per Query against Organization/Membership lookups and current machine entries (no aggregate field). Cross-Aggregate read joins must not be silently relabelled. |
| 06 Events | Ten named event blocks with producer/payload and shared envelope/ordering; owner table says Identity | Specify Consumers for each event, including restricted LoginFailed. Generic consumer obligations and “inventory required” are not an actual subscriber inventory. Triggers/order/idempotency need per-event references and proposed/accepted distinctions. Unknown consumer count is not zero. |

Other content locators also require sufficiency review: storage uniqueness is not a complete physical index plan; “platform security approval” is not a precise platform-wide security reference; Service test rows are not automatically the Domain Service test matrix. The tool reports locations without upgrading these to content PASS.

## 4. Foundation review: 001–005

| Foundation and rule | Current Identity evidence | Review result |
|---|---|---|
| 001 flat semantics; execution/infrastructure cannot define meaning; Identity derived | 01 separates Person/ownership concepts from durable workflow/material/Outbox records; 00 defines technical delivery as infrastructure | No new foundational construct found in this scope. Capability named Identity is not evidence of promoting derived semantic identity to a new core construct. Explicit concept-to-foundation traceability should be attached before gate closure. |
| 002 constructibility/reification; recorded Event remains Event | 06 completed facts; 09 distinguishes Outbox from historical Event Store; supporting records not Aggregates | Documentary compatibility found after the event-introduction correction below. No event is made a Thing merely because it is persisted. Foundation wording ambiguity on Time remains a source-level review item. |
| 003 composition, time-binding, no business term as new core type | Person/Organization/Membership domain model; timed events and ownership/Ready timestamps; references rather than type conversion | No ontological type conversion found. A complete mapping of each domain concept to Thing/Relation/Event/Rule/derived construct is not currently supplied; absence of mapping is not proof of contradiction. |
| 004 §§8.2/8.6/8.7 boundaries by invariants, references not ownership, storage not boundary authority | Five independent Aggregates in 01/03; separate Credential/Session lifecycle; 09 supports transaction exception without sixth Aggregate | Registration's cross-Aggregate consistency strategy is documented; applicable ADR-0002 approval remains required. T16 position is a supporting record, not a reason to redefine Person's boundary. |
| 004 §§8.3/8.4 intrinsic cross-Aggregate rules vs orchestration; Domain Services do no persistence | 01 §7 domain services; §8 application orchestration; 04/09 repository/UoW responsibilities | Narrow RegisterPerson Application Service exception is Proposed. Review ADR-0002 D7/7.1 precisely; “documented exception” is not an accepted exception. AuthenticationDomainService checks cross-object facts, while application/repository coordination must remain outside it. No runtime separation proof exists yet. |
| 004 §8.5 stable rules vs configurable policy | 01 invariants; 10 policy bounds; 12 explicit domain/policy/infrastructure distinction | Documentary distinction exists. Changing deployment values must not disable ownership/readiness/proof invariants. Unselected policies remain choices, not implementation defaults inferred by this report. |
| 005 domain as composition; common semantics across domains | Reusable Identity; Kimia milestone does not introduce salon/staff rules into registration | No Kimia-specific foundational semantic redefinition found. Wider taxonomy/dependency compliance still needs its own review. |

### Source-standard ambiguities requiring governance interpretation

1. **Time terminology:** 001 §4 lists Time among core constructs while §8 says it is not a core construct; 002 §3 says five core constructs while §3.5 explicitly excludes Time; 004 §3 uses “five foundational semantic constructs.” Identity must not resolve this by inventing a new ontology. Review/correct the source terminology under governance; do not report a fabricated Identity violation or change the Foundation unilaterally.
2. **Authority precedence:** 064 §2 explicitly distinguishes 001–005 content authority from 051 process authority; 051 §18 gives a different global precedence list headed by ADRs and Governance. How an approved ADR interacts with Foundation content needs a scoped interpretation. No generic waiver route or Level-4 authority was verified. 064 §1 does explicitly route deviations through 051; that is not a completed waiver approval.
3. **066 §22 numbering:** its final pipeline cites 063/064/065 while the described Blueprint Standard/Validator/Generation documents are 064/065/066. Editorial source finding; no change to generation preconditions is implied. This report leaves normative source files unchanged.

## 5. Corrections made and prior-report reconciliation

| Finding | Correction published in this follow-up | Effect |
|---|---|---|
| 03 Session rationale showed Expired→Closed as a chain, contrary to 01 §5 and 06 §6.4 | 03 v1.4.2 uses alternative terminal states; Suspended remains future | Alignment only; no lifecycle Command added |
| 03 unqualified “Person changes do not invalidate Sessions” could bypass current auth/refresh checks | Clarified no automatic row cascade while preserving 04's current-state gates | Does not accept S2 or all-Session password-change behavior |
| 06 overview universal Aggregate-state-change framing contradicted Ready workflow and LoginFailed | 06 v1.3.1 explicitly describes nine Domain Events + Security Event and completed-fact conditions | No new event or earlier PersonRegistered timestamp |
| 06 §1.2/5.5 excluded delivery obligations wholesale despite 07/09 obligations | Distinguishes physical implementation choices from proposed delivery/dedup/application duties | T16 remains Proposed; no ordered option accepted |
| Limited acceptance form's permission language conflicted with 064 | Draft v5 makes all applicable implementation gates necessary | No owner signature or narrowed package assumed |

Machine document versions synchronized to 03 v1.4.2 and 06 v1.3.1. Other active package versions/statuses are unchanged by this follow-up.

Prior report conclusions preserved: no proven P4b/P15 semantic loss; explicit post-commit isolation/non-goal/recovery clarification already restored in 09 v1.3.1; pre-Ready profile assertion intentionally corrected; shrinking 09 line count is not a loss metric. Full legacy requirement reconciliation remains open. ADR version references must be classified historically/contractually, not replaced globally. Identity remains intentionally pinned to its older proposed review baseline until an accepted coherent revision is selected.

## 6. Verification

From repository root, with dependencies in `tools/slice0-requirements.txt` installed:

```sh
python tools/check_identity_blueprint.py
python tools/slice0_structural_065.py --json
python tools/check_slice0_negative_controls.py
```

Local environment used `PYTHONPATH=../review-deps` for the dependency-using commands. Raw evidence: [structural result](Identity_Slice0_Structural_Result.json) and [negative controls](Identity_Slice0_Negative_Controls.json). Results: 430/430 limited package checks; 296 PASS / 6 WARN / 97 INFO from the expanded subset checker. `git diff --check` passed.

Four isolated copies retained the complete unmodified baseline dependencies. Each mutation produced its specific FAIL, exit 1, no traceback: remove all Query headings; replace a dependency with missing 064 target; replace an event schema JSON pointer with missing definition; duplicate a command identifier. The producer-presence check was renamed from the misleading V-005 label to S9; V-005 concerns owning Capability Platform, not producing service. Negative controls verify these detector paths, not all architectural rules. No implementation/runtime tests were run.

## 7. Remaining work and decisions

| Item | Next concrete deliverable | Who can close |
|---|---|---|
| Content coverage | Resolve OPEN/inferred cells in the completed per-instance field-to-authority matrix; full structural-reference/naming/ordering review | Documentation/validation work, with architecture review for new behavior |
| Contract/semantic equality | Field-level narrative/OpenAPI/service/event/machine diff; V-001–V-012 dispositions; explicit consumer/migration register | Technical review + accountable consumer owners |
| GOV | Reviewed ADR-0002 v1.8 sequencing and D1–D9 dispositions; ADR-0003 criteria/scope; Foundation ambiguity dispositions | Architecture owner, attributable record under 051 |
| T16 | Selected A/B with versioned producer/consumer guarantees, forecast/inventory and failure/replay ownership | Architecture owner; no option selected by this report |
| SESSION | Review owner-selected S2/BFF direction; close cross-store password-change/refresh race, residual access validity, boundary/security tradeoffs; propagate one coherent version | Architecture/security owner; direction exists, approval does not |
| Four gates | Exact output revision, coverage/results/exclusions and reviewed gate closure for the defined package | Validator/reviewer plus governance |
| Implementation setup | Stack/database choice, reproducible dev environment and concrete adapters after applicable gate closure | Engineering choice; can be proposed now without implementation permission |
| Runtime/release | Real DB race/crash/security tests, deployed trust/KMS/delivery/finite policy configuration | Implementer and operational owners after approved architecture |

No new 3–6 day estimate is justified until the decisions and required contract scope are closed. The work delivered here completes this follow-up's foundation reading, gate mapping, coverage inventory and checker extension; it does not claim completion of every remaining validation category.
