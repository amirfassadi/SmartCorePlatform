# Identity MVP and Architecture Owner Decision Form

**Version:** 0.3.2 Draft  
**Status:** Unsigned; not effective  
**Purpose:** Prepare owner decisions P01, P04, P05, and P06 and record the MVP scope that those decisions govern.  
**Decision authority:** Amir (@amirfassadi), project and architecture owner, under SmartCorePlatform 051 §7.  
**Encoding:** UTF-8.  
**Review input base (pre-form):** Platform `review/slice0-evidence` at `f3a227c`. This is not the decision pin. The owner record must pin the exact Platform commit containing the accepted form text, plus the separately reviewed Identity commit, in the table below.  

This form does not itself accept an ADR, close a validation gate, permit implementation, set `READY_FOR_GENERATION`, or authorize deployment. Each selected disposition takes effect only when the attributable owner record is completed and the governing repository documents are updated and validated.

## 1. Platform purpose and MVP scope — P01

### Proposed decision

Build a reusable SmartCore platform so any business owner can self-register and later establish a business through the appropriate platform capability. No named business is the product boundary or a target of this Identity MVP.

Maintain one Identity capability Blueprint for the scoped Identity MVP and deliver it in phases. The first implementation delivery is verified-contact registration and atomic ownership creation, followed by authentication/session and profile capabilities. Business registration, booking, and other business workflows belong to later capability modules.

### In-scope Identity MVP capabilities

1. Register a Person with one verified contact (mobile phone or email), display name, and password.
2. Verify the selected contact with a one-time code, expiry, attempt limit, resend limit, and the existing ADR-0002 Decision 9 protections. Resending must not extend the original verification expiry.
3. Atomically create Person, Personal Organization, and Owner Membership. Create Organization and Membership directly in their MVP Active states, consistent with proposed ADR-0003.
4. Permit login and Session issuance only after registration reaches Ready.
5. Support refresh and logout under the SESSION policy once accepted and propagated.
6. Allow a Person to view their profile and own Sessions, edit DisplayName, and change password after verifying the current password; a successful password change closes all Sessions and refresh families.
7. Provide a minimal password-recovery/reset flow before public self-service onboarding. Implement it after core registration and login if delivery phasing requires, but do not treat it as an indefinite post-MVP omission. Require the same verified-contact proof protections, non-enumerating responses, expiry/rate limits, and binding controls; on successful reset, revoke all Sessions and refresh families. Security review must explicitly assess recycled mobile numbers: control of a reassigned number does not prove that its current holder is the former account owner. Define how reset is protected when SMS is the only verified channel; evaluate a bounded cooling/expiry policy, notification to other independently verified channels, and a controlled recovery path where no alternate channel exists. This expands the current Blueprint/ADR scope and requires explicit security, event, and contract review before acceptance. Do not invent a new public event; explicitly decide whether the existing `PasswordChanged` fact covers reset and what non-sensitive reason, if any, may be recorded.

### Out of scope for this Identity MVP

Business creation/profile, appointments/bookings, multiple Organizations per Person, invitations, membership roles beyond Owner, contact changes, social login, MFA, and non-Person identity types. These remain future capability/decision work; do not imply that this Identity MVP implements the business setup flow itself.

### Path from Person to a future business

MVP's Personal Organization is an individual ownership context, not a registered business. A future business capability will associate its business record with a Person through an Organization and active Membership, under the approved tenant/ownership model. This MVP does not choose whether business setup reuses the Personal Organization or creates a separate Organization, and it does not decide the Organization-to-Tenant mapping. Preserve stable Person identity and the ability to represent multiple Organizations/Memberships later; do not make `PersonId` synonymous with a business, Organization, or tenant, or encode “one Organization forever” as a Person-domain invariant. Record the reuse-versus-separate organization choice in the business capability/ADR before implementing business registration.

### Identity, tenant, and client boundaries

- Identity registration, login, profile, and Session operations are Person-scoped. They cannot require a tenant that the Person has not yet selected or established.
- Tenant-scoped business requests must carry the applicable organization/tenant context and authorize it through the Person's active Membership and the consuming capability's policy. Do not equate `OrganizationId` and `TenantId` unless ADR-057 explicitly defines that mapping.
- The MVP's browser contract covers a server-side web client/BFF only. Native mobile, direct browser-to-Identity bearer-token clients, service clients, and device/agent identities need separate client-boundary review before support.
- Use a platform-wide web-session policy for MVP. Leave a documented extension point for future tenant/client policy, but do not add tenant-specific timeout configuration in this MVP.

### Contact and localization direction

Recommended UI default: ask for mobile first in the initial market, while retaining email as an equal valid alternative in the Identity contract. Keep market-specific phone normalization and Persian/RTL message presentation at the appropriate localization boundary; do not make Iran-specific syntax a permanent Person-domain invariant. Put SMS/email delivery behind replaceable provider adapters. Select actual providers and finite delivery/rate budgets before deployment, not as a prerequisite for defining the capability contract.

Contact entry disposition:
- [ ] Mobile-first UI; email remains available as an equivalent registration option.
- [ ] Email-first UI; mobile remains available as an equivalent registration option.
- [ ] Other: ______________________________.

Password recovery disposition:
- [ ] Include minimal verified-contact reset in the Identity MVP product scope, delivered after core registration/login and before public self-service onboarding; successful reset revokes all Sessions/families.
- [ ] Defer beyond MVP release; record release limitation and target milestone: ______________________________.

Security review evidence for reset must address recycled mobile numbers, including accounts with no alternate verified channel: ______________________________.

Password event disposition (no new public event is implied):
- [ ] The existing `PasswordChanged` event covers successful ChangePassword and password reset; update its contract/example and add only a reviewed non-sensitive cause discriminator if needed.
- [ ] `PasswordChanged` covers ChangePassword only; successful reset emits no public event in this MVP unless a separate event decision is approved.
- [ ] Defer the event disposition; no reset contract may be published until resolved.

### Options considered

- **One Identity Blueprint, staged delivery — recommended.** Keeps cross-slice contracts coherent while allowing registration to be the first delivery.
- **A registration-only Blueprint/module.** Rejected for this decision because login, Session, password lifecycle, and recovery are part of a usable person identity capability and affect its contracts. Registration remains the first implementation phase.
- **Build business-specific onboarding into Identity.** Rejected because Identity establishes the Person and initial ownership context; each business capability owns its own business setup flow.

### Compatibility, evidence, and responsibilities

- No implemented/deployed Identity API is evidenced in the readiness report. Finalize Draft schemas before implementation; if a published external contract or client is later found, record its exact compatibility/migration treatment before changing it.
- Evidence reviewed: proposed ADR-0002 v1.8.0 Decisions 1–9; proposed ADR-0003 v1.2.1 lifecycle scope; 051, 057, 064, 065; `Identity_Implementation_Readiness_Status.md`; current Identity 00–16 and schemas. Record exact reviewed versions/SHA below.
- Accountable decision role: platform/architecture owner. Responsible implementation roles to assign: Identity capability owner; Credential/security owner; web/BFF owner; messaging/provider operations owner; consumer capability owners. Names remain unassigned until recorded.

### P01 owner disposition

- [ ] Accept proposed scope and phasing.
- [ ] Accept with changes recorded below.
- [ ] Defer.

Owner changes / rationale: __________________________________________________

Rejected options and reasons, if changed: ____________________________________

## 2. P04 — Person event position and delivery semantics

### Proposed decision

Add a monotonically increasing `position` per Person for `PersonRegistered` and `PersonUpdated`. Allocate it in the same local transaction as the Ready/profile mutation and Outbox fact. Use it for latest-state versioning and duplicate/stale-event detection. Do not require dispatcher N+1 to wait for broker acknowledgment of N, and do not select a broker or manual fencing design here. A verified future consumer requirement for every-transition processing or ordered side effects requires a separate transport decision.

`PersonUpdated` is a full snapshot in the current MVP Draft. If it changes to a delta/patch, or no longer represents enough current state for latest-state projection, reopen P04 before adopting that contract. Full snapshot plus position does not, by itself, authorize consumers to perform every registration or business side effect from an update.

### Out-of-order facts — required consumer rule

Position orders the Person state stream; it is not a rule for deleting or ignoring distinct facts. If `PersonUpdated` at position 2 arrives before `PersonRegistered` at position 1, the consumer MUST retain and process both unique events. It MUST NOT discard the lower-position `PersonRegistered` merely because its projection checkpoint has advanced, and MUST preserve registration-only facts such as Ready time and `OwnershipCommittedAt` for their authorized purposes.

Consumers therefore need separate durable tracking for (a) receipt/deduplication of each unique `EventId` and (b) the highest `position` reflected in their latest-state projection. A lower-position, different EventId/type can be stale for projection replacement while still being an unprocessed fact. Persist its inbox/fact record and perform its event-specific effect idempotently. Exact duplicate `EventId` with the same bound fact may be a no-op; EventId/position reuse with divergent content is an integrity conflict. If a consumer's ordered side effect cannot safely tolerate this arrival pattern, it must buffer/gate that effect until prerequisites are satisfied or request a separate ordered-delivery decision; it may not silently lose the registration fact.

### Required invariants and transport placement

- Enforce uniqueness of `(PersonId, position)` in supporting persistence.
- Bind a stable `EventId` to the same `PersonId` and `position`; retry/re-drive preserves original EventId, position, payload, and timestamps.
- Store the allocator/counter as supporting application persistence. It does not create a sixth Aggregate and does not redefine Person lifecycle version.
- **Proposed wire choice:** carry `position` and `personId` in a versioned transport wrapper outside the closed public Event envelope. The wrapped `event` remains the existing complete event envelope. This is a transport-schema change and must be versioned/documented; it does not silently add fields to `events.schema.json`'s closed envelope.
- Latest-state consumers commit their projection checkpoint with the projection, separately from the durable event inbox/fact ledger. Their contract must define bootstrap/unseen Person, gaps, duplicate delivery, older positions, and divergent EventId/position reuse. This decision does not claim an event consumer inventory is complete.

### Evidence, alternatives, and limits

- The consumer registry currently marks actual/planned subscribers `UNKNOWN`; no evidenced subscriber requires every transition.
- **Rejected for this MVP decision:** strict dispatcher acknowledgment sequencing plus manual stale-worker fencing. It adds operational complexity without a demonstrated every-transition consumer need. Reconsider only with a named consumer, owner, event-use case, and processing/side-effect evidence.
- **Rejected:** putting `position` directly in the closed public Event envelope at this stage. The wrapper keeps transport ordering metadata distinct from the stable public fact; changing this choice requires compatibility/schema review.
- **Rejected:** a single high-watermark cursor that drops every event below it. That would lose a distinct `PersonRegistered` fact after a later `PersonUpdated` arrives first.
- Broker partitioning by PersonId may be evaluated later; it is not a guarantee selected by P04.
- No ordering between different Persons or for Organization, Membership, authentication, or Session events is established here.

### Compatibility, evidence, and responsibilities

- The wrapper schema/version and routing are new draft contract surface. Finalize before any subscriber is admitted; no deployed API or consumer migration is presumed.
- On P04 acceptance, propagate the receipt-versus-projection rule to the Person event contract (including wrapper/schema documentation), consumer guidance, machine metadata where applicable, and Identity conformance/testing documents in both repositories. Add conformance cases for `PersonUpdated(position=2)` arriving before `PersonRegistered(position=1)`, then receiving/processing both facts without projection rollback, loss of Ready/`OwnershipCommittedAt`, or duplicate side effects. Do not describe this candidate as an active contract before acceptance.
- Evidence reviewed: current `06_Domain_Events.md` full-snapshot statement/history; T16 candidate and options comparison; per-event consumer registry; 03/04/07/09 persistence/readiness material.
- Responsible roles: Identity producer/persistence owner; transport adapter owner; each consuming capability owner for inbox/checkpoint/projection. Assign accountable names before implementation of the wrapper/consumer contract.

### P04 owner disposition

- [ ] Accept proposed versioned wrapper and non-blocking delivery semantics.
- [ ] Accept with changes recorded below.
- [ ] Defer pending a named consumer that requires ordered every-transition processing.

Owner changes / rationale: __________________________________________________

## 3. P05 — SESSION policy and server-side web client

### Scope

P05 in this form covers only the platform's server-side web client/BFF boundary. It does not set native mobile, machine-to-machine, public browser bearer-token, or future identity-client policy. Each future client type requires an explicit trust/storage/session review.

### Existing directions to confirm or amend

- Access token expires no later than 900 seconds after issuance and never later than the absolute Session deadline.
- Absolute Session lifetime is at most 86400 seconds from login; refresh does not extend it.
- One-time refresh rotation; reuse of a consumed predecessor revokes its family/Session and requires reauthentication, including an ambiguous lost-response retry.
- Successful password change closes every Person Session and refresh family, including the current Session.
- Self-contained Access tokens may remain usable until bounded expiry after logout/revocation; universal immediate access revocation is not promised.

Baseline disposition:
- [ ] Accept the five SESSION directions above as the proposed web/BFF baseline.
- [ ] Accept with specific changes recorded below.
- [ ] Defer.

Changes / rationale: ________________________________________________________

The owner previously selected no separate idle timeout as a direction. **Recommendation for reconsideration:** for the MVP server-side web/BFF session, use a platform-wide 30-minute inactivity proxy, evaluated when Refresh is attempted. Persist the time of the last successful, foreground-driven Refresh; do not write durable session state on every application request solely to update activity. Do not run background Refreshes without a qualifying foreground request. The rule is 30 minutes since the last successful foreground Refresh, not a precise measurement of the last user action. Since a live Access token may permit activity for up to 900 seconds after issuance, the observed idle cutoff relative to last authenticated use is approximate by up to 15 minutes (roughly 15–30 minutes, depending on when use occurred within the Access-token lifetime). A tenant cannot override or lengthen the MVP platform default; a future governed extension may introduce tenant/client policies.

When more than 30 minutes have elapsed since the recorded foreground Refresh, deny renewal and require login again. An already issued self-contained Access token may remain usable until its own expiry, for up to 900 seconds after the idle cutoff is detected, just as it may remain usable for that period after logout/revocation. This is a proposed change to the previously recorded no-idle direction and requires explicit acceptance of both the approximate 15–30-minute idle cutoff and residual Access validity. The contract must bind Refresh to the server-side BFF Session and use a durable, shared enforcement point; browser-only timers do not enforce expiry. Security review must confirm whether recording `lastRefreshAt` and checking it at Refresh produces the intended maximum idle exposure for the selected BFF flow.

### API expiry fields

Finalize both fields in the pre-implementation Draft response:

- `accessExpiresAt`: expiry of the current Access token.
- `expiresAt`: immutable absolute Session deadline.

Require `accessExpiresAt <= expiresAt` and no later than issuance plus 900 seconds. The readiness evidence reports no implemented/deployed Identity API, so the Draft can be corrected before first implementation. If a published API/client is discovered, record its compatibility and migration disposition first.

### Credential/Session storage — recommended ADR-0004 reopening

**Recommendation:** reopen ADR-0004 for the MVP to compare a shared transactional persistence boundary for Credential and Session against the currently accepted separate-boundary protocol. ADR-0004 explicitly identifies co-located Credential/Identity persistence as a viable alternative, but did not select it. No shared-store design is adopted by this form.

Password recovery strengthens the reason to compare the options: it is a second Credential-changing path that must coordinate with Session and refresh-family revocation. If stores remain separate, the accepted fence/epoch and reconciliation protocol must cover both authenticated ChangePassword and recovery/reset, serialize against login and refresh, and define lost-result recovery. A protocol that protects only ChangePassword is incomplete.

Any selection of co-location requires a formal amendment/replacement to ADR-0004. The review must decide:

1. Which accepted ADR-0004 controls remain, simplify, or become unnecessary: Credential-side provisioning guard, `AcknowledgeRegistrationReady`, pending/finalization behavior, recovery, audit, and no-resurrection rules.
2. Whether actual Credential replacement, Session/family revocation, and relevant Identity Ready writes share one enforceable transaction boundary, rather than merely using the same database server.
3. Logical ownership: schemas/modules, migration authority, which service/code may write each table, audit and recovery ownership, and how cross-module writes are prevented.
4. How the revised design preserves the accepted Credential winner, one-active-Credential, Ready, and no-resurrection invariants.

Until that review is accepted, ADR-0004 remains authoritative, including its provisioning guard and Ready acknowledgment. If co-location is rejected, the separate-store password-change fence/epoch and fail-closed recovery protocol must be completed before dependent implementation.

### Options and reasons

- **Reopen ADR-0004 for an MVP shared-transaction alternative — recommended for evaluation.** May reduce the cross-store password-change protocol cost; requires formal architecture change and retained ownership/invariant controls.
- **Retain independent persistence boundaries.** Preserves current accepted ADR-0004 architecture but requires durable serialization/fence, Credential outcome reconciliation, and fail-closed recovery for login and refresh races.
- No option is selected until the owner disposition and ADR record are completed.

### Evidence and responsibilities

- Evidence reviewed: accepted ADR-0004 v1.1.1 and its acceptance record; SESSION policy/BFF/security/contract candidates; Identity 01/04/07/08/09/10/11; readiness report.
- Responsible roles: Credential persistence owner; Identity Session owner; web/BFF owner; security reviewer; database/migration owner; operations/recovery owner. Assign names and authority before implementation.
- Compatibility: no deployed Identity API is evidenced. Complete schema and BFF contract before coding; check for published consumers and pin both repositories before propagation.

### P05 owner disposition

Idle policy:
- [ ] Accept proposed 30 minutes since foreground Refresh as the platform-wide web/BFF inactivity proxy, including up to 15-minute cutoff uncertainty and up to 900-second residual Access validity; future tenant/client policy requires a later governed decision.
- [ ] Retain no idle timeout, with explicit risk rationale.
- [ ] Accept another value/policy: ______________________________.

Storage / ADR-0004:
- [ ] Reopen ADR-0004 to evaluate a shared transactional persistence boundary; no change is effective until accepted.
- [ ] Retain separate boundaries and complete the durable fence/recovery protocol.
- [ ] Defer.

Owner changes / rationale: __________________________________________________

## 4. P06 — scoped acceptance of ADR-0002 and ADR-0003

### Proposed acceptance scope

Accept only after the integrated contracts and architecture review are coherent. This is not blanket acceptance of every future capability or proof that 064/065 gates are complete.

**ADR-0002 v1.8.0, Decisions 1–9:**

1. Initial Person, Personal Organization, and Owner Membership are created atomically.
2. Authentication and capability-specific business authorization remain separate.
3. Membership role is an attribute; Owner is the only v1.0 role.
4. Identity remains Person-centric in v1.x; future Device/Service/Agent identity remains future work.
5. Identity owns the specified event catalog and the current LoginFailed Security Event classification; do not invent or add an event through this form.
6. Future identity types are documented, not implemented in this MVP.
7. RegisterPerson retains the specifically scoped application-service coordination exception.
8. The PendingCredential/Ready, Credential winner/guard/acknowledgment, and recovery rules are evaluated against accepted ADR-0004; any change follows the formal ADR-0004 process.
9. Verified-contact registration follows the specified verification session, expiry, attempt/resend, protected-material, binding, replay, invalidation, and lost-response requirements.

**ADR-0003 v1.2.1, Decisions 1–2:**

1. Organization lifecycle is Created → Active → Suspended → Archived; MVP creates the Personal Organization directly as Active and includes no lifecycle transition commands.
2. Membership lifecycle is Created → Active → Revoked; MVP creates the Owner Membership directly as Active and includes no invite/revoke commands.

These proposed ADRs remain `Proposed`. The decision record must identify any clause excluded, amended, or deferred; simply checking “accept ADR” is insufficient. Password reset, the idle-timeout change, P04 wrapper semantics, and any ADR-0004 co-location change need their own explicit scope/propagation entries.

### Alternatives, evidence, and responsibilities

- **Option recommended:** scoped acceptance of the above clauses after architecture validation and contract propagation.
- **Rejected:** blanket ADR acceptance based only on this form or on prior ADR-0004 acceptance; it would exceed the evidence and ADR-0004's scope.
- Evidence required: exact integrated Platform and Identity revisions; architecture validation review; complete relevant 064/065 results; consumer/security evidence as applicable; disposition of OPEN/REVIEW cells; acceptance record meeting 051 §7.
- Responsible roles: architecture owner/decision authority; independent architecture/security reviewer if available; Identity and Credential owners; validator/Blueprint owner; Identity and platform operations owners.

### P06 owner disposition

- [ ] Accept the listed ADR-0002 and ADR-0003 clauses within the stated scope, subject to evidence and propagation gates.
- [ ] Accept with clause-level changes attached.
- [ ] Defer pending evidence/review.

Excluded/amended clause IDs and rationale: __________________________________

## 5. Other open decisions and required order

This form does **not** close these independently governed items from the readiness report:

- **P02 / V-002:** whether `RefreshSession` is an approved exception to the command/event result rule without adding a fabricated public event.
- **P03 / V-003:** whether each Query has exactly one result Aggregate and how read dependencies/authorization are documented.
- **Foundation dispositions:** the reported open/review items include pagination policy, tenant-scope rules, Identity-first versus IoT sequencing, and the distinction between messaging engine and transport. The complete six-item list and exact governing clauses must be carried into a separate Foundation decision packet; no item is accepted by reference here.

These decisions remain prerequisites to full structural/semantic/architecture validation where applicable. Track them in their own owner records with the same evidence, alternatives, compatibility, and responsibility fields required below.

### Recommended decision and publication sequence

`P01 → P05 / P04 → P02 / P03 and Foundation dispositions → coordinated Platform + Identity publication and SHA pinning → P06 → applicable 064/065 gate closure → implementation authorization`

P06 follows publication because its acceptance evidence depends on integrated contracts. Publication alone does not close a gate or authorize code. If a decision changes an upstream standard, amend that source through its governance path before propagating it.

## 6. Decision packet completeness and record

For **each** P01, P04, P05, and P06 disposition, the final owner record must capture:

- Decision ID, exact governing document/version/section, and bounded scope.
- Selected option; rejected options and reasons.
- Reviewed evidence and known limitations.
- API/schema/transport version impact, migration/compatibility plan, and affected consumers (unknown remains unknown).
- Responsible and accountable execution roles, including security, operations, migration, and consumer duties as applicable.
- Required follow-up ADR/decision ID and any conditions that must be met before implementation.

| Pin | Repository | Branch | Exact commit SHA | Verified date |
|---|---|---|---|---|
| Platform | SmartCorePlatform | `review/slice0-evidence` | `________________________________` | `____________` |
| Identity | SmartCoreIdentity | `________________________` | `________________________________` | `____________` |

| Decision | Record / ADR identifier | Owner disposition | Owner and date |
|---|---|---|---|
| P01 | `________________________` | `________________________` | `________________` |
| P04 | `________________________` | `________________________` | `________________` |
| P05 | `________________________` | `________________________` | `________________` |
| P06 | `________________________` | `________________________` | `________________` |
| Password recovery scope | `________________________` | `________________________` | `________________` |
| ADR-0004 review/change | `________________________` | `________________________` | `________________` |

### Remaining gates

Owner acceptance does not close Structural, Semantic, Architectural, or AI Readiness gates; does not certify full 065 validation; and does not authorize implementation or deployment. Record each gate result against exact repository SHAs and governing evidence before code-entry authorization.

**Approval signature / attributable owner record:** PENDING  
**Effective date:** PENDING  
**Implementation authorization:** NOT GRANTED BY THIS DRAFT
