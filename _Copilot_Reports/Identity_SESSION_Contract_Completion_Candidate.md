# SESSION — remaining contract choices and failure protocol candidate

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: Proposed / unsigned; SESSION OPEN.
Review input: Platform `630a22da53195a87d780aaf3c867bdd359eab83a`.
Sources: [decision candidate](Identity_SESSION_Decision_Candidate.md), [S2 BFF draft](Identity_SESSION_S2_BFF_Contract_Draft.md), [security ledger](Identity_SESSION_S2_Security_Review_Checklist.md), [propagation map](Identity_SESSION_S2_Propagation_Map.md), Identity/01/04/07/08/09/10/11.

## Preserve previously recorded direction

| Item | Owner-selected direction already in source documents | Remaining review |
|---|---|---|
| Access token | At most 900 seconds, never beyond absolute Session deadline | Issuer clock/validation tolerance and endpoint enforcement |
| Session | Immutable cap of 86400 seconds from login | Wire deadline meaning and BFF cookie alignment |
| Idle timeout | None separately selected | Unattended/shared-device exposure and product mitigation |
| Refresh | S2 one-time rotation; strict consumed-token reuse revokes family/Session and requires login, including response loss | BFF trust, durable storage/serialization and usability trade-off |
| Logout/revocation | Clear BFF cookie; self-contained access may remain usable until bounded expiry | Avoid universal immediate-revocation promise |
| Password change | Close every Session and refresh family, including current | Credential/Session cross-store fencing and acknowledgment |

86400 denotes the absolute Session cap, not a periodic rotation interval. Rotation happens on a successful refresh; it never extends that cap. These directions need architectural/security acceptance and coherent propagation, not another arbitrary choice of numbers. Current active Draft 04 still describes static refresh and unchanged Sessions after password change; it has not been silently replaced.

## 1. Recommended proposed wire resolution

Keep SessionTokens.expiresAt as the immutable Session deadline, consistent with the S2 draft and SessionSummary. Add a separately named accessExpiresAt to SessionTokens to describe the access-token deadline. Both are date-time strings; semantic checks enforce accessExpiresAt <= expiresAt and <= issuance + 900 seconds. Login returns the same nested SessionTokens shape; successful refresh returns a new refresh secret. Existing browser/BFF response handling must be reviewed rather than forwarding bearer material to JavaScript.

This is a new required field in a closed response schema and may break strict existing consumers. Before changing active OpenAPI/machine/examples, choose version/routing and a migration disposition for each consumer; unknown consumers are not a proven greenfield. Do not call this a patch-only correction. Alternative: explicitly rename both deadlines in a new response version; avoid an ambiguous single deadline.

The BFF cookie lifetime is bounded by the absolute Session deadline. Browser cookie/CSRF settings, client authentication and protocol classification need the actual deployment topology; no confidential OAuth status, production BFF implementation or provider is presumed.

## 2. Supporting Session state and strict reuse

Propose Session-owned supporting family storage with current generation/version, current verifier/key reference, consumed predecessor verifiers/tombstones, immutable deadline and revocation state. No raw refresh secret in durable plaintext, logs, public Events or browser storage. The one authoritative transaction consumes the predecessor, records one successor and guards Session/family eligibility. No response precedes commit. Verifier construction, key policy and retention require security review; this document does not choose cryptographic defaults.

Retain spent-generation recognition until the family can no longer refresh at its absolute deadline, plus any approved processing/cleanup boundary; retained audit has its separately approved policy. No unlimited retention or use beyond expiry is authorized. Set finite abuse limits and operational ownership before adoption.

BFF serialization must span instances and reconcile durable state after restarts. After an ambiguous refresh outcome, clear BFF continuation state and require login; do not automatically retry the predecessor. A stale BFF writer must not restore an earlier refresh secret after revocation; specify fencing/compare-and-set in its token store. Identity enforces its own transaction regardless of BFF coordination.

## 3. Cross-store password-change race: concrete proposed protocol

The following is a design candidate to review, not an already selected implementation. It preserves Credential's independent authoritative transaction and ADR-0004 ReadyAcknowledged guard. A Person-scoped coordination/fence record is supporting application state; it is not an attribute silently added to the Person Aggregate.

| Phase | Proposed durable requirement | Failure behavior |
|---|---|---|
| Admission | Validate caller/current password/new password and existing Credential provisioning guard. Persist a uniquely bound change intent containing only protected-material references, never plaintext passwords or reusable proof, then acquire a Person-scoped authentication issuance fence in the authoritative Session/coordination store | While fence is pending/active, login and refresh fail closed; no success promise |
| Fence and close | Serialize against every login/refresh writer on the same Person guard. Advance durable revocation epoch and close current Sessions/families with the guard in the local store | Crash leaves fence closed to issuance; recovery resumes the same operation. A refresh committed before the fence is made unusable by closure |
| Credential replacement | Trusted Credential operation checks ReadyAcknowledged and atomically replaces the active Credential under a versioned, idempotent operation binding | Lost result is reconciled from durable operation evidence; do not blindly issue another replacement |
| Acknowledgment | Confirm committed Credential result and completed revocation intent, then resolve the fence so a future login can authenticate against the new Credential | No successful ChangePassword response until all-Session closure is durably enforced. Pending/unavailable remains explicit; success cannot be inferred from an Event alone |
| Recovery | Trusted worker re-reads durable phase and bindings; never lowers epoch, restores old family or creates a new Credential on a conflicting replay | Indeterminate Credential outcome remains fail closed until authoritative reconciliation |

A Session writer must take/check the same authoritative fence in its commit boundary; a cached epoch or asynchronous event is insufficient. Credential validation done before the fence or before an epoch change must be discarded/revalidated before issuing tokens. Login after fence resolution uses the current Credential; proof from the previous epoch cannot create a new Session. This explicitly covers login as well as refresh, which a refresh-only guard would miss.

Credential/Session trust binding and a versioned password-change operation/outcome lookup are prerequisites for this protocol; the currently reviewed Credential registration services do not yet define these password-change messages. Before adoption specify authorization, operation binding, expiry/material protection, terminal/uncertain outcomes and recovery. This proposal does not widen the existing provisioning guard or use an admin-supplied winner/force flag. Outward pending/error mapping requires API review; no HTTP code is invented here.

Consequence: a fenced operation can temporarily deny login/refresh for the Person. If Credential replacement ultimately fails after Session closure, previous Sessions remain closed; no resurrection compensation. Review this availability/usability trade-off explicitly. An accepted atomic co-location design could be an alternative only if it preserves logical ownership and is separately reviewed; do not assume two independent store writes form one transaction.

## 4. Sensitive endpoint and access aftermath

ChangePassword must require a current, eligible Session and the provisioning guard, with current-password verification. In-flight concurrency is governed by the fence above. Restricted administrative recovery keeps its separate operator MFA/permit contract. Future contact/account recovery is not introduced by this proposal. Resource-server self-contained access may remain valid up to its existing 900-second deadline; immediate universal access revocation is not promised. Other capabilities own their sensitive-operation checks and business permission decisions.

## 5. Evidence and propagation to finish

| Item | Documentary acceptance evidence | Later implementation evidence |
|---|---|---|
| BFF boundary | Actual topology, authenticated client, cookie/CSRF/secret ownership and protocol | Browser/token leakage and wrong-client tests |
| S2 | One transaction boundary, strict reuse/failure mapping, predecessor policy | Durable races, theft/reuse, response-loss and cleanup tests |
| Expiry | Both wire deadlines, immutable cap, no-idle risk and clock policy | Exact boundaries and BFF cookie tests |
| Password change | Fence/epoch ownership, login+refresh serialization, Credential operation/reconciliation, fail-closed and migration | Both commit orders, login race, crash at every phase, lost Credential result and stale writer |
| Compatibility | Contract version/routing and affected client inventory | Real consumer integration tests |
| Operations/security | Named roles, finite limits, keys/retention, incident procedures | Deployment configuration and operational checks |

Propagate accepted choices together to 01/03/04/07/08/09/10/11/12/13/14/16, OpenAPI/services/machine and BFF contracts, then reconcile SmartCoreIdentity source pins. V-002 disposition is separate; strict reuse audit is not a fabricated public Event.

No runtime result is claimed. Owner/security dispositions, exact accepted source, protocol/retention policy and complete architecture/gate review remain PENDING. An architecture signature alone does not satisfy all four 064 gates.
