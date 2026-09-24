<!--
Document ID: ID-13
Title: SmartCore Identity Platform Blueprint - Testing
Version: 1.0.0
Status: DRAFT
Purpose: Define the proposed Identity testing contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

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
