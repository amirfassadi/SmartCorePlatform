# Identity SESSION policy — architectural decision candidate

Status: Proposed / unsigned — 2026-09-29 (review revision 0.3)
ADR number: unassigned; allocate through SmartCorePlatform governance, preserving immutable identifiers under 051.
Decision authority: SmartCore architecture/security owner. This document records owner-selected design directions from the project conversation, not a signed Approval step or an active Blueprint amendment.
Sources: [options](Identity_SESSION_Policy_Options_Draft.md), [S2 BFF contract](Identity_SESSION_S2_BFF_Contract_Draft.md), [security checklist](Identity_SESSION_S2_Security_Review_Checklist.md), [propagation map](Identity_SESSION_S2_Propagation_Map.md). Re-pin the integrated candidate commit before architectural approval.

## Context

The uploaded Identity Blueprint has 1-hour access and 7-day refresh TTL values, a Production rotation requirement in 10_Configuration, and a differing optional-policy description in 11_Security/04_Commands. The integrated Platform Identity Draft proposes a 900-second access token, 86400-second absolute Session cap and nonrotating refresh. These are conflicting proposed contracts. Kimia's browser-facing client is intended to use a BFF, but deployment/client authentication remains unverified.

## Proposed decision scope for Kimia human Identity MVP

1. **Client boundary:** Browser uses a protected BFF session cookie. Refresh material remains server-side and is presented only by the authenticated, authorized BFF. Verify the actual topology, cookie/CSRF policy and protocol classification. Other client types require separate review.
2. **Lifetime:** Access token expires no later than 900 seconds and Session absolute expiry. Session expires at most 86400 seconds after login; refresh never moves that deadline. No separate idle timeout is selected for MVP. BFF cookie/session cannot outlive Identity Session.
3. **Refresh replay control:** Use S2 rotating one-time refresh generations. In one durable Session/family transaction, consume current generation and commit one successor. Only one current generation may be valid. A consumed predecessor presented again causes family/Session revocation and explicit reauthentication, including a lost-response retry. BFF serializes refresh per Session across instances; Identity still enforces the authoritative transaction.
4. **Logout and revocation:** BFF immediately clears its browser cookie and current refresh family is disabled. Already issued self-contained access tokens may remain valid until their expiry, bounded by 900 seconds, unless a separately reviewed endpoint performs online Session checks. Do not promise universal immediate access revocation.
5. **Password change:** Successful ChangePassword closes all Sessions for the Person, including the current one, and revokes all refresh families. Reauthentication follows. Cross-store ordering/guards and the exact success acknowledgment must prevent a concurrent refresh from resurrecting a family. Outstanding access tokens follow item 4.
6. **Events and model:** Keep five Aggregates, six business Commands and ten existing public Identity events unless a separate decision changes them. Refresh does not emit a new public event. Token-family state is proposed as Session-owned supporting persistence, not a silently added Aggregate; review this boundary explicitly.

## Rationale and alternatives

S2 retains a fixed maximum login period while detecting use of a consumed refresh generation. S1 static bearer refresh is simpler but provides no comparable reuse signal if stolen; a short access lifetime alone does not repair that. S3 sliding lifetime is not selected because the owner chose a fixed cap without an idle extension. Sender constraint remains an alternative to evaluate for other client types and could complement S2, but is not assumed implemented for this BFF.

Strict predecessor reuse handling intentionally trades occasional forced login under ambiguous network failure or concurrent requests for a simpler fail-closed contract. Measure forced-login frequency in multi-tab and weak-network tests; a grace/replay recovery mechanism would require separate review before adoption.

## Consequences and unresolved evidence

- The current platform nonrotation wording in Identity/04 and its API/machine/schema examples must be replaced coherently after approval. Historical uploaded documents remain archived.
- With no idle timeout, an unattended browser/device may retain a usable BFF cookie until the 24-hour absolute cap. Shared-device and physical-access risk must be explicitly accepted or mitigated through product/device policy; a 15-minute access-token TTL does not shorten the cookie-backed Session.
- BFF authentication, token storage, distributed refresh serialization, cookie/CSRF handling, client/protocol classification and operational owner are not yet evidenced.
- Predecessor-verifier retention, key rotation, rate limits, audit access and cleanup bounds require approved policy.
- Resource-server access-token validation, logout semantics and password-change cross-store consistency require explicit contract review. Before approval, enumerate sensitive Identity operations (at least ChangePassword, and contact/account recovery if later enabled) that require current-Session verification or step-up despite bounded bearer-token lifetime. Restricted administrative recovery follows its separate operator MFA/permit contract, not a Person Session. Financial or other business operations remain owned by their capability; each owner must classify its own sensitive endpoints and authorization requirements rather than inheriting an Identity permission rule.
- A candidate password-change guard is a durable Person-scoped authentication/session revocation epoch checked by every refresh against the authoritative state. If Credential and Session live in separate stores, merely incrementing a Person Aggregate version in one store or publishing an event does not close the race: specify serialization, acknowledgment and fail-closed behavior until every refresh writer observes the new epoch. This is an option for review, not a selected protocol.
- Runtime concurrency, response-loss, theft/replay, expiry, logout and password-change tests are required after architecture approval; none are claimed passed.

## Architectural approval criteria

- [ ] Exact integrated Platform candidate commit and all conflicting sources reviewed, with compatibility/migration disposition.
- [ ] Security/architecture review of the Kimia BFF trust boundary and S2 transaction/reuse semantics completed, including the strict forced-login trade-off.
- [ ] No-idle, 900/86400-second values, unattended/shared-device exposure, residual access validity, sensitive-endpoint list and all-Session password-change scope explicitly accepted with user/security implications.
- [ ] Token-family ownership, cross-store revocation/epoch candidate, concurrent refresh guarantee and public contract/event effects reviewed against 051, 064 and 065.
- [ ] Operational accountability named and required finite policy values/retention decisions recorded or explicitly gated before deployment.
- [ ] An attributable owner approval records the candidate SHA, scope, date, unresolved verification duties and rejected alternatives.

Architectural approval is required under 051 §7; implementation additionally requires all applicable 064/065 code-entry gates. It would not by itself mark Identity READY_FOR_GENERATION, pass full 065 validation, prove runtime behavior, or authorize deployment. T16 and ADR-0002/0003 remain separately governed. Until approval, the Platform's active Draft nonrotation contract is not superseded.

## Post-approval verification and propagation

Propagate to the files in the [map](Identity_SESSION_S2_Propagation_Map.md) as one versioned candidate. Execute the [security checklist](Identity_SESSION_S2_Security_Review_Checklist.md) with exact revision/environment and attach results. Failed scenarios return for architectural/policy correction; do not silently weaken the one-successor, absolute-expiry or no-secret-leak invariants.

Approval/effective date: PENDING
Accepted source commit: PENDING
Signature/attributable record: PENDING

## Contract completion follow-up — 2026-10-04

[Completion candidate](Identity_SESSION_Contract_Completion_Candidate.md) specifies proposed separate access/Session deadlines and a durable password-change fence covering login as well as refresh. These are new unapproved details, not propagation into active contracts. [Decision packet](Identity_Next_Decision_Packet.md) pins the integrated review input; final accepted source remains PENDING. The 86400-second figure is an absolute Session cap, not a periodic rotation interval.
