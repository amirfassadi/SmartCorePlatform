# T16 — Identity event ordering options

- Version: 0.3.1
- Status: Draft comparison; no option selected or accepted
- Date: 2026-09-25
- Repository: amirfassadi/SmartCorePlatform
- Review path: PR #5, docs/identity-blueprint-completion
- Pinned baseline: b82ab197124d0b7936b34597e514e347a9b301e2
- Scope: PersonRegistered / PersonUpdated only; LoginFailed and other authentication/audit outcomes are excluded

> **Re-pin required before acceptance.** PR #5 is open, not merged. Before
> this draft is used as final decision input, every line reference and
> quoted wording above must be re-verified against the exact commit chosen
> as the decision candidate — not assumed to match whatever later lands on
> `main`. If the PR changes before merge, this draft must be re-synced
> against the new candidate commit before proceeding. Once merged, record
> the final merged SHA here as the merged baseline, after verifying the merged text.
> Merge alone does not constitute architectural acceptance.

## 1. Decision to make

Choose an explicit contract for producer publication and consumer application of registration/profile events. Compare ordered publication with version-aware unordered consumption. The current shared allocator remains Proposed until a decision replaces or accepts it. This comparison changes no Blueprint, schema, acceptance record or runtime contract. ADR-0004 is architecturally Accepted within its signed scope; ADR-0002 remains Proposed and T16 remains open.

The leading selection criteria are consumer count/control and consumer semantics, followed by measured per-Person contention and operational failure isolation. Neither absence of consumers nor future external consumers is assumed.

## 2. Baseline evidence and causal boundary

All references below mean the pinned PR #5 baseline, not main or superseded PR #2:

- 04 Commands §4.2 explicitly requires Active Person, Ready workflow and current active Credential before Session creation. §4.3 requires an authenticated Session for UpdatePersonProfile, the currently defined PersonUpdated producer.
- 09 Persistence §6.4 atomically commits Ready and the PersonRegistered Outbox entry. Its shared counter, monotonic positions and blocked-position behavior are the proposed T16 mechanism, not an independently accepted fallback.
- 06 Events §6.1 delegates this proposed ordering to 03/09. Session-ordering prose alone does not establish an alternative dispatcher contract.
- ADR-0004 accepts Credential polling/guard/acknowledgment, not public event publication ordering. Credential can become active before Ready.

Under those current command paths, Ready and PersonRegistered enqueue commit before a Session can authorize PersonUpdated. This is a causal commit-order argument, not a publication/delivery guarantee. It depends on authoritative readiness enforcement and the absence of another producer bypassing Ready. A future pre-Ready profile update, import, admin writer or changed authentication path requires review. Existing wording in 03 that allows profile mutation before Ready conflicts with this command model and must be corrected during propagation.

Candidate explanatory title for 06 §6.5: “Why PersonRegistered Commits Before PersonUpdated”. Add a direct ADR-0002 Decision 8 reference to the existing Ready requirement in 04; do not claim it was previously absent.

**Accompanying correction:** this change set includes 03_Aggregates.md v1.4.1 and its matching machine-manifest version, correcting the pre-Ready profile-update statement. The finding above remains historical evidence about pinned baseline b82ab19. The correction does not select an ordering option or close T16; verify the published change-set commit separately when reviewing it.

## 3. Option A — ordered publication per Person

Define a common order for the two event types, preserve it from committed Outbox facts through publication, and specify consumer application under redelivery. The proposed shared allocator is one possible implementation; any alternative must demonstrate equivalent guarantees rather than assume broker key ordering repairs reversed publisher submission.

Required decisions: owner of ordering metadata, atomic allocation/enqueue, dispatcher concurrency/fencing, ambiguous publish acknowledgment, duplicate delivery, replay and consumer processing order. A permanently failing earlier event blocks later events for that Person and raises an alert; dead-lettering must not silently authorize advancement. Operator recovery, retained evidence and any exceptional skip policy require an explicit contract.

Intended mitigation: blockage is isolated to one Person. This is a requirement to prove: stopping an entire broker partition shared by many Persons would violate that isolation. Admission/backpressure, worker fairness and bounded buffering must prevent a hot or stalled Person from exhausting shared resources. Consumers still need EventId deduplication and safe parallel processing/replay; ordered publishing alone is not exactly-once application.

Contention is primarily per Person, not necessarily a global bottleneck. PersonRegistered occurs once per registration; repeated PersonUpdated writes dominate ongoing load. Profile writes already serialize on Person concurrency control, so compare the allocator's incremental cost rather than attributing all contention to T16.

## 4. Option B — version-aware unordered consumption

Do not require a common transport order. Explicitly expose a committed profile revision and define how each consumer applies snapshots without reverting newer data. The existing expected Person version is a command concurrency input, not an already established event field. EventId deduplication alone cannot reject an older, distinct snapshot.

Before selecting this option, define revision ownership, atomic capture with profile data, equal-version conflicts, missing baseline behavior, replay and deletion/tombstone semantics. Registration readiness is a separate fact from profile freshness: a stale PersonRegistered profile snapshot must not overwrite newer profile data, but its registration fact must not be discarded merely because the profile revision is older. A single highest-version check on the whole event is insufficient.

This option fits latest-state projections only if their merge contract is complete. Consumers needing every intermediate transition or ordered side effects need an additional explicitly designed contract; version comparison is not a substitute for those requirements. Gaps cannot be skipped safely when payloads are patches requiring prior state. Verify snapshot versus patch semantics before selecting.

Complexity moves to N consumers. Proposed enforceable onboarding gates: inventory with accountable owner and processing semantics; versioned contract acceptance; mandatory conformance fixtures before subscription/upgrade; review enforcement for new subscriptions; monitoring and incident ownership for stale/equal-version conflicts. Fixtures must cover reversed delivery, duplicate EventId, old replay, equal-version divergent payload, missing registration baseline and independent retention of the registration fact. A shared library may help but is not proof that every language/client complies. These gates are requirements of this option, not existing deployed controls.

## 5. Comparison

| Criterion | A: ordered publication | B: version-aware unordered consumption |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Consumer control                                                      | Centralizes ordering responsibility, but consumers still handle dedupe/replay/concurrency         | Requires enforceable merge/version conformance for every consumer                                |
| Consumer semantics                                                    | Better starting point for sequential changes/side effects; durable processing still required      | Better starting point for latest-state projections; cannot silently discard required transitions |
| Throughput                                                            | Additional per-Person allocator/dispatch serialization; incremental cost must be measured         | Avoids common sequence allocation; Person updates still have concurrency control                 |
| Failure isolation                                                     | Must prove a stalled Person does not stop a shared partition; later events for that Person wait   | Other events can proceed; malformed/version-conflict handling still needs bounded recovery       |
| Main correctness risk                                                 | Commit order lost at dispatcher, unsafe advancement after ambiguous delivery, consumer reordering | One consumer misapplies an older snapshot or drops an independent registration fact              |
| Contract change                                                       | Ordering metadata and end-to-end responsibility                                                   | Exposed revision plus precise merge rules and onboarding enforcement                             |

## 6. Evidence needed and capacity scenarios

No observed rate or consumer inventory has been supplied. Collect total PersonUpdated rate, hottest-Person sustained/burst rate, active Person distribution, transaction/allocator lock duration, retry/conflict rate and publication-lag target. For A, the rough single-Person utilization indicator lambda_person × serialized_service_time helps identify saturation risk, but excludes jitter, broker latency and recovery and is not a capacity guarantee. Measure incremental allocator overhead against existing profile-write serialization.

Evaluate normal interactive edits, a hot-Person burst and a stalled Person alongside healthy Persons. Populate numerical rates from measured usage or an explicitly approved workload forecast; do not label arbitrary numbers “expected traffic”. For B measure consumer convergence lag, rejected stale updates, conformance coverage and operational cost across supported implementations.

Inventory fields: consumer/name, owner, internal/external, subscription enforcement authority, latest-state versus every-transition requirement, replay needs, upgrade control, delivery/application lag target and contract version. Unknown entries remain unknown, not “no consumers”.

## 7. Selection and closure gates

Prefer B provisionally when consumers are controlled, require latest state and can be required to pass the merge contract. Prefer A provisionally when ordered transition processing is required or merge conformance is impractical, subject to delivery/application responsibilities and acceptable contention/isolation. Neither condition has yet been established for this project.

Q1: causal commit order is supported by current commands; need for delivery ordering depends on consumer semantics.

Q2: allocator ownership is relevant only if A uses that mechanism; B still needs revision ownership.

Q3: how is a message that cannot be applied handled? Under A, a permanently failing event SHALL block later events for that Person (§3); required ordering SHALL NOT be broken by skipping it, so recovery is an explicit operator action, not an automatic skip. Under B, "cannot be applied" splits into two different cases that need separate answers: a stale-but-valid profile snapshot may be ignored once a newer profile revision is applied; any independent registration fact carried by the event must still be processed (§4), but an unresolved version conflict (e.g. equal-version divergent payloads, missing baseline) is not — it needs its own explicit resolution policy, not a generic skip. This remains necessary under either option, with different retry/replay/failure rules.

- [ ] Inventory and consumer semantics reviewed by accountable owner.
- [ ] Workload assumptions and acceptance thresholds recorded.
- [ ] Selected option and rejected alternative justified; contract owners named.
- [ ] Publication/application/replay/stalled-message behavior fully specified.
- [ ] Explicit architectural approval recorded; no acceptance inherited from ADR-0004.
- [ ] Propagation list covers 03/04/06/07/09, machine/event encodings, tests and old contradictory statements.

Architectural selection can precede runtime tests, but runtime validation and propagation remain separate open obligations. This draft does not close T16 or grant generation/merge readiness.

## Change log

- Version 0.3.1 (2026-09-25): Fixed comparison headers and unchecked gates; limited stale-data discard to the profile snapshot while preserving the registration fact; distinguished merged baseline from acceptance; recorded accompanying 03 v1.4.1 correction.

- Version 0.3.0 (2026-09-25): Re-pin note now ties to the exact decision-candidate commit (re-sync before merge, record final SHA after merge), not merge status alone. Q3 rewritten to remove ambiguous "bounded skip with recovery": A's blocked event requires explicit operator recovery, not skip; B's discardable stale snapshot is distinguished from an unresolved version conflict, which needs its own policy. Added a status note in §2 distinguishing the pinned-baseline finding on 03's contradictory wording from a reported local, unpushed 1.4.1 fix.
- Version 0.2.0 (2026-09-25): Added the re-pin-before-acceptance note in the header (PR #5 is open, not merged). Filled in Q3 with the actual open question (stalled/unresolvable-message handling under either option), rather than only its rationale.
- Version 0.1.0 (2026-09-25): Initial draft comparison.
