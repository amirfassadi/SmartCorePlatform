<!--
Document ID: ID-13
Title: SmartCore Identity Platform Blueprint - Testing
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity testing contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Test plan, not execution evidence

The following are required implementation tests. Their presence here does not imply an implementation or passing result.

| Layer | Scenario | Required observation |
|---|---|---|
| Domain/unit | Email-only and mobile-only, neither/both/null, canonical collisions | Exactly one verified contact; same uniqueness/delivery normalization |
| Aggregate | Pending Person, zero Credential; provisioning race | No sixth Aggregate; at most one active Credential |
| Application | Inject failure at every ownership write/Outbox/bind | Entire ownership UoW rolls back, no committed dangling secret reference |
| Integration | Commit response lost, replay within expiry | Same registration and outcome; no second triple; proof+binding required |
| Security | Replay after expiry or changed binding/input | Uniform denial; no lifetime reset; keyed verifier disposed |
| Security | Leak stored OTP verifier in isolated test | No plain hash; key/purpose/session separation; online attempts atomically limited |
| Security | Parallel guessing/resend, valid/invalid/nonexistent contact | Cumulative limits, code rotation, no existence-dependent body/status/latency distribution |
| Integration | Cleanup races owner transfer | Live post-commit material survives pre-commit sweep; abandoned material deleted on deadline |
| Service | Credential commit succeeds but response lost | Poll finds same winner; retry never replaces Credential |
| Service | Automatic vs setup race, duplicate setup with changed password | One winner; loser no replacement; one Ready/event |
| Application | Local Ready/event transaction fails after service success | Retry reconciles then creates one Ready/event/position |
| Security | Second registration after expired replay | No duplicate Person; second password invalidated; distinct setup proof required |
| Event | Credential recovery hours later or never | Ownership events at commit; PersonRegistered at Ready or absent; immutable timestamps |
| Event | System reconciliation vs Person completion | Correct actor/current context; no copied original IP/device |
| Event | PersonUpdated races Ready; duplicate/out-of-order delivery | Shared unique ordered apply for two-event stream; stable EventId; no audit allocator contention |
| Authentication | Pending, missing Credential, inactive Person, outage | No tokens; generic external failure; restricted internal reason |
| API | Null/omit, unknown fields, self/service projection | Required shapes; no Mobile in public event snapshot; no contact in service lookup |
| Session | Refresh expiry/cap, logout-expiry race | No session extension, no tokens in list, one terminal event |
| Compatibility | Existing consumers and old payload fixtures | Explicit migration decision; no assumption of zero consumers |

# 2. Observability and acceptance

Assert no proof/password/token appears in logs, traces, metrics labels or event payloads. Measure cleanup deadlines and rate-limit fairness with concurrency, not only happy-path unit tests. Record exact implementation revision, environment, test commands/results and unmet gates before changing readiness status. Test fixtures contain synthetic contacts and no real credentials.

# 3. ADR-0004 required implementation verification — NOT executed

| Area | Scenario | Required observation |
|---|---|---|
| C01/C02/C03 | Concurrent initial candidates then attempted replacement before acknowledgment | One active immutable winner; every supported writer checks guard |
| Ready commit | Crash between local writes | ReadyFactId, event and acknowledgment Outbox all commit or all roll back |
| Acknowledgment | Lost response, duplicate after ChangePassword, different ReadyFactId | Matching replay succeeds without restoring old Credential; mismatches rejected |
| Confirmation | Historical AlreadyCompleted while Identity PendingCredential | Integrity conflict; never manufacture Ready from historical result |
| Public API | Setup candidate loses; Ready response; pending acknowledgment during ChangePassword | Explicit credentialOutcome; finalization-pending returns no password change/event |
| Admin auth | Missing step-up/scope, grant revoked, forged/expired permit | No new effects or existence leak; audit outcome |
| Admission | Same-key changed descriptor, stale snapshot, two operators | Binding conflict or guarded no-op; no forced stale effect |
| Pre-commit race | Admin invalidation vs ownership bind/material transfer | Exactly one guarded outcome; transferred material survives |
| Post-commit race | Admin vs ordinary Ready/ack worker | Same winner/fact/event/ack; no new candidate supplied by admin |
| Audit | Local audit write failure or external backlog threshold | Atomic denial or bounded durable buffering; no unaudited mutation |
| Crash | Remote acknowledgment commits before job result | Reconcile durable facts; no duplicate mutation or false success |
| Job lifecycle | Expiry/revocation/budget exhaustion; signed request replay after cleanup | Stop new dispatches; no expiry-based guard release or re-admission |
| Support | NotProvisioned, IntegrityConflict, permanent outage | Typed non-success result, ticketed escalation; no database-unlock instruction |

Schema fixtures may check message shape only. They do not execute any of these integration/security/concurrency scenarios.
