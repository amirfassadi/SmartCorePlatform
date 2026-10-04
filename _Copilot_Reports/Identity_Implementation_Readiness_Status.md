# Identity implementation readiness — current work and remaining entry conditions

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: NOT READY FOR IMPLEMENTATION / generationAllowed remains false.
Platform input: `5ea92766f480fc8d16bc337272b4595078fe3112`; Identity input: `ee9ffb767ed84165557793d8583b0750d887027b`. Reviewed output is the containing Platform commit; subsequent Identity publication references it explicitly. Main branches are not merged.

## Completed preparation in this revision

- Explicit seven-field mapping for all nine use cases, including Session creation and ownership-Membership alternative/failure applicability; Command purpose and Query sorting/pagination applicability declared without new operations.
- Per-root invariant/boundary/relationship mapping for all five Aggregates; explicit application/domain execution boundary against 004/062.
- Full legacy 09 operative-body comparison, separating retained requirements from deliberately replaced sliding expiry/implicit initial login/blanket Outbox deferment. Pair/token uniqueness, optimistic markers and replacement Credential identities restored in Draft 09.
- Consumer register covers all ten Events with actual/planned subscribers UNKNOWN rather than invented identities or zero counts.
- Per-instance 064 matrix revised: 35 instances, 251 cells; **233 DOCUMENTED, 11 OPEN, 7 REVIEW**. DOCUMENTED denotes an explicit declaration, never accepted semantics or readiness PASS.
- Architecture review advances source/grammar/layer/tenancy/scope assessment and records exact unresolved findings. Corrected only unambiguous reference-number/title pairs in 032 and 060; normative scope/policy wording is not changed by those editorial corrections.
- [Foundation alignment candidate](Identity_Foundation_Alignment_Candidate.md) provides explicit recommended clauses for pagination/tenant scope, Identity-first versus IoT milestone, registration overview and Messaging-engine distinction, rather than leaving findings with no proposed resolution.

Evidence: [architecture review](Identity_Preimplementation_Architecture_Review.md), [legacy review](Identity_Persistence_Legacy_Content_Review.md), [matrix](Identity_Slice0_Required_Content_Matrix.md), [consumer registry](Identity_Event_Consumer_Registry.md), [decision packet](Identity_Next_Decision_Packet.md).

## Gates, owners and concrete exit conditions

| Work item | Current result | Owner / next action | Evidence needed to close |
|---|---|---|---|
| Scope/Foundation applicability | Exact candidate clauses prepared, OPEN | Amir: disposition of Identity-first milestone, bounded pagination, tenant scope and exact grammar authority | Attributable source/version/scope disposition; accepted references propagated without waiving gates |
| V-002/V-003 | Rule proposal prepared, current literal rules unresolved | Amir: accept/revise alternatives in rule-disposition draft | Governed normative amendment/exception and complete command/query mapping; substantive validator checks |
| T16 | Ordered wrapper/atomicity/fencing/replay candidate prepared, OPEN | Architecture/transport/consumer owners: review exact contract, name owners and establish subscribers/bootstrap | Accepted versioned transport/schema and consumer compatibility/conformance design |
| SESSION | Existing owner directions preserved; complete expiry/fence proposal prepared, OPEN | Architecture/security/BFF owners: actual topology, retained policy, cross-store Credential operation and migration | Accepted coherent policy/wire/service/persistence contracts, ownership, keys/retention/finite bounds |
| ADR-0002/0003 GOV | Still Proposed; ADR-0004 remains Accepted within previous scope | Amir: criterion-by-criterion sequencing/lifecycle/decision scope, record final candidate SHAs | Architecture review/dispositions, accepted source references and attributable approval, no runtime PASS invented |
| 064 Structural | More explicit fields; partial checker only | Validation executor: complete §8 class/per-instance meaning/reference/package-status review | Full applicable coverage and disposition of all OPEN/REVIEW cells, draft companion status resolved |
| Semantic and Architectural | Field matches and analyst review advance evidence; findings remain | Resolve rule/policy/source/consumer/privacy/compatibility findings and trace all remaining obligations | Complete per-category findings/dispositions on a coherent candidate; not keyword or fixture counts |
| AI Readiness | generationAllowed=false, unresolved policy/standard decisions | Finish preceding documentary/governance gates, then audit 064/065/066 generation criteria | Accountable readiness record; one coherent machine/narrative/API/schema/example package |
| Security/material design | Proposed 10 defaults and protected workflow exist; acceptance/implementation design incomplete | Architecture/security: approve KDF/material/proof/binding/configuration design and required finite values before dependent code | Reviewed design and later benchmark/failure plans; no guessed crypto or operational ownership |
| Code/database/consumer behavior | Not implemented or tested | After all applicable code-entry gates, implement registration-first delivery and run real-store failure/race/security tests | Actual code SHA/environment/results; release/deployment gates separately governed |

The 11 OPEN matrix cells comprise ten unknown Consumers and RefreshSession resulting Event. The seven REVIEW cells comprise three collection pagination declarations, two T16 ordering declarations and restricted LoginFailed ordering/idempotency. This is only the per-instance matrix: other architectural, policy, package and authority findings remain independent and are not hidden by the count.

## Recommended decision grouping

Review the existing rule/T16/SESSION proposals together with the six Foundation applicability clauses as one coherent architecture candidate. Recorded 900-second access, 86400-second absolute cap, no-idle and all-Session password-change directions need no arbitrary reselection. Acceptance of direction with unfinished details must identify those details as gates; it cannot mark the whole package ready.

Once attributable decisions exist, propagate standards/ADRs, 00–16, API/services/events/machine/examples and Identity proposal as a coordinated reviewable revision; complete all documentary gates before runtime scaffold/generation. Retain one full human Identity MVP and use phased delivery, subject to owner adoption of that scope. No duration estimate is justified until remaining scope/contract choices are adopted.

## Verification and practical limits

Current checks: **557/557** focused synthetic contract checks, **433/433** limited package checks, **297 PASS / 6 WARN / 97 INFO** structural subset, four expected isolated negative-control failures. Increase from 430/296 reflects added resolvable references/dependency declarations, not increased readiness percentage. Raw structural output is updated; focused-contract data is unchanged because wire schemas/fixtures are unchanged.

Relative links and changed metadata/versions are checked; git diff --check passes. No runtime security/concurrency/crypto/consumer tests, independent architecture sign-off or full 065/064 gate PASS is asserted. The proposals are unsigned, active SESSION/T16/rule semantics are not silently adopted, and main remains untouched.
