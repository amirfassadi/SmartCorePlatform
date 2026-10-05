# T16 ordered Person stream — concrete decision candidate

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: Proposed / unsigned; T16 OPEN. ADR identifier: UNASSIGNED.
Input: Platform `630a22da53195a87d780aaf3c867bdd359eab83a`; Identity proposal `ee9ffb767ed84165557793d8583b0750d887027b`.
Sources: Identity/03 application workflow, 04 readiness checks, 06 §6, 07 §5, 09 §6.4; [comparison](Identity_T16_Options_Comparison_Draft.md). These sources already propose a shared allocator but do not accept it.

## Proposed decision and rationale

Recommend option A: one durable ordered registration/profile stream per Person, shared by PersonRegistered and PersonUpdated. This is consistent with the project-context direction toward ordered delivery and platform-wide Identity consumption; the branch still contains no attributable formal T16 approval. No actual subscription count or production workload is inferred. Centralize a versioned conformance contract while retaining consumer-owned durable application and deduplication.

Only these two Event types participate. OrganizationCreated, MembershipCreated, authentication/Session events and restricted LoginFailed are outside this stream. No cross-Person ordering is promised. Ready fact timing, ownership transaction, Credential guard/acknowledgment and ADR-0004 accepted scope are unchanged. T16 is not authority to move PersonRegistered to ownership commit.

## Proposed transport encoding

A transport wrapper, separate from the closed public Event envelope, carries the following. This is a reviewable candidate, not an active machine/schema change or broker selection.

| Wrapper field | Proposed shape and constraint |
|---|---|
| contractVersion | Exact string `identity.person-stream/1` |
| personId | UUID; must equal wrapped Event AggregateId and Payload.PersonId |
| position | Canonical positive decimal string, no leading zeros; semantic range 1 through 9223372036854775807; not a JavaScript floating-point number |
| event | Existing complete PersonRegistered or PersonUpdated envelope from events.schema.json, unchanged |

Example skeleton uses symbolic placeholders, not an executable message:

```json
{"contractVersion":"identity.person-stream/1","personId":"<PersonId UUID>","position":"1","event":"<complete existing PersonRegistered envelope>"}
```

Contract owner proposed: Identity owns the stream meaning and Event binding; Messaging/Integration owns transport adapter compliance, delivery operations and compatible routing. Actual accountable individuals remain to be assigned. Version field names and numeric representation are new proposed wire choices requiring compatibility review. Wrapper contains no token, verification proof or new contact field. Existing Event context/privacy restrictions continue to apply.

## Producer and dispatcher invariants

1. Stream starts at position 1 with PersonRegistered at the one-time Ready transition. The counter, stable EventId, wrapper metadata and Outbox fact are committed in that same local Ready transaction; rollback consumes no committed position. Ownership commit does not allocate this public-stream position.
2. PersonUpdated requires the existing authenticated, Ready path and allocates the next position with the Person mutation and Outbox insertion in one transaction. Counter belongs to supporting application persistence, not Person lifecycle/version, and creates no sixth Aggregate.
3. Enforce uniqueness of (PersonId, position) and stable EventId/position binding. Retry/re-drive preserves original payload, EventId, timestamps and position. No resequencing after uncertainty; no new EventId for the same fact.
4. A dispatcher submits unique positions in order for each Person. It may submit N+1 only after durable broker acceptance evidence for N is recorded. If acceptance of N is uncertain, retry the same N; duplicate physical delivery may occur after later deliveries. Broker acknowledgment does not mean any consumer applied the Event.
5. Concurrent dispatchers require durable claim/fencing and an adapter that prevents a stale worker from introducing a new higher-position submission. A lease timeout alone is not proof. Late duplicate copies remain possible and must be safe. Actual broker/adapter fencing design and crash points require review before implementation.
6. Permanent failure at N blocks and alerts later positions for that Person. Dead-lettering does not grant skip permission. Recovery re-drives the same fact or returns a separately reviewed exceptional repair decision. Healthy Persons must continue; shared-partition backpressure must not turn this into global blockage.

## Consumer application invariants

Persist inbox/deduplication, last applied position and projection update in one consumer-owned transaction; every-transition external side effects require a local Outbox or equivalent reviewed idempotent dispatch, not an assertion of exactly-once network delivery.

| Incoming condition | Required proposed action |
|---|---|
| Next expected position, valid binding | Commit inbox, checkpoint and projection/side-effect intent atomically |
| Already committed identical EventId and same position/fact | No-op; preserve checkpoint and original outcome |
| EventId reused with another position or divergent content; position collision | Stop/quarantine that stream and alert; do not overwrite evidence |
| Future position with a gap | Durably defer within approved bounds, request replay/reconciliation; never apply later transition side effects first |
| Older unknown EventId at an already passed position | Treat as inconsistency needing investigation; do not silently classify as a harmless duplicate |
| Malformed/unauthorized Event or permanently failing handler | Block that Person's application stream and escalate; other Persons continue |

Bootstrap/replay for a new consumer starts from retained position 1, or from an explicitly authorized durable snapshot with a trustworthy matching checkpoint. Current IdentityLookup exposes only PersonId/DisplayName and cannot establish Ready, historical transitions or a stream checkpoint. If history is unavailable and no approved snapshot/checkpoint exists, admission remains blocked; do not fabricate a baseline. Retention and replay service/storage ownership must be decided before subscriber admission, independently of long-term Event Store design.

## Required documentary evidence before adoption

- Confirm all PersonUpdated producers obey Ready and use the same allocator; imports/admin/future writers cannot bypass the ordering contract.
- Approve wrapper/schema/version routing and map affected known or planned consumers. Record unknown consumers as unknown; Kimia registration UI/BFF is an API client until a subscription is verified.
- Name producer, transport, consumer contract/library, replay and incident owners. Agree finite buffer/retry/retention and lag/workload thresholds from measured or explicitly forecast inputs. No invented production rates.
- Review durable dispatcher fencing, ambiguous-ack handling, per-Person failure isolation and consumer replay bootstrap.
- Propagate to Identity 03/04/06/07/09/12/13/16, machine transport metadata and a versioned wrapper schema outside the existing closed Event envelope; reconcile Identity proposal authority afterward.

## Planned runtime conformance scenarios — not executed

Concurrent Ready/profile allocation; rollback/no gap; crash before/after enqueue; acknowledgment loss; stale dispatcher; duplicate after a later position; gap and reversed physical delivery; position/EventId collision; projection commit crash; external side-effect redelivery; one stalled Person alongside healthy Persons; replay retention expiry and unauthorized bootstrap. Specify exact code/database/adapter revisions when these run after applicable architecture and implementation gates.

Rejected alternative for this recommendation: unordered version-aware snapshots move convergence and independent registration-fact preservation into every consumer, while some platform consumers may need ordered side effects. This is a design rationale, not evidence that those subscribers are deployed. If workload/consumer review contradicts the premise, revise the choice through governance.

Approval record number, exact accepted SHA, owner/date, consumer inventory/compatibility disposition and accepted transport/replay design: PENDING. Selecting A alone does not close T16; the complete candidate and remaining evidence need approval. No overall gate PASS or implementation permission is granted.
