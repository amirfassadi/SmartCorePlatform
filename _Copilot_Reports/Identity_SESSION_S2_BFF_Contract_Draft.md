# SESSION S2 — proposed BFF refresh contract

Version: 0.3.1 — 2026-09-29 — DRAFT, owner-selected failure direction; unapproved wire and persistence design
Parent comparison: [Identity_SESSION_Policy_Options_Draft.md](Identity_SESSION_Policy_Options_Draft.md). Propagation: [S2 map](Identity_SESSION_S2_Propagation_Map.md).
Scope: Kimia's owner-selected BFF direction and S2 rotating refresh with a fixed absolute Session deadline. No endpoint, implementation or security test is asserted to exist. This proposal does not alter the current Draft Identity/04, OpenAPI or machine specification.

## 1. Security and client boundary

The browser receives a protected BFF session cookie, never an Identity refresh token in JavaScript. The BFF is the only intended presenter of the refresh credential for this Kimia flow; Identity authenticates/authorizes the BFF service and binds the token family to the authorized client context. The BFF must protect cookie use against CSRF and use appropriate HttpOnly/Secure/SameSite/domain settings after the actual deployment topology is known. A BFF is not automatically a confidential OAuth client merely by being called one: verify its client authentication, key storage and network boundary.

Other future clients require separate policy; do not use the Kimia BFF decision as permission to issue static bearer refresh tokens to browser/native clients.

## 2. Session and token-family invariants

- A Session has immutable `SessionId`, PersonId, CreatedAt and absolute `ExpiresAt` after login. The owner selected 86400 seconds (24 hours) as the Kimia MVP design value for this cap on 2026-09-29; rotation never extends ExpiresAt. Access tokens issued at login/refresh expire no later than both the owner-selected 900-second (15-minute) design TTL and Session ExpiresAt.
- Exactly one current refresh generation is valid for an active Session family at a time. Each successful refresh atomically consumes generation N and records one successor N+1 under the same Session. The predecessor remains represented by a non-secret verifier/tombstone sufficient to recognize reuse until the approved family/audit retention bound. No raw refresh secret is logged or stored as plaintext.
- A token is unguessable, purpose-bound to refresh and protected in transit/at rest. Store only a keyed verifier or equivalent protected representation, with key version and rotation plan. An exposed SessionId, token generation or request id is never sufficient to refresh.
- The family cannot outlive the Session. Closed/Expired/revoked Sessions have no usable refresh generation. Normal refresh does not create a new Session, Person or Credential and does not publish a new public Identity event.
- Registration PendingCredential remains ineligible. Every refresh checks current Session status/deadline, Person status, registration Ready and active Credential gate as required by Identity/04 §4.5; a previously issued token does not waive these checks.

The authoritative transaction boundary for consumption, successor creation, family version and Session state is one durable Session/refresh store. A process-local lock or BFF-only mutex cannot enforce one active successor across Identity workers.

## 3. Refresh outcomes and concurrency

| Condition | Proposed authoritative outcome |
|---|---|
| Current valid generation N, active eligible Session, before absolute deadline | Atomically consume N, commit successor N+1, issue access token bounded by Session expiry and return new refresh secret to BFF. No response precedes the durable commit. |
| Two concurrent presentations of N | One transaction may win. The other observes consumed N; treat as reuse and revoke the family/Session under the policy below. BFF serializes refresh per browser Session to avoid legitimate parallel requests; distributed instances need a shared coordination mechanism. This client measure is not the server correctness guard. |
| Consumed predecessor presented again, whether attacker or legitimate lost-response retry | Fail closed, revoke the affected refresh family/Session, audit restricted identifiers, require explicit reauthentication. Do not return an old or newly generated secret. This can cause a forced login after network loss; it is the chosen safe baseline, not evidence of theft by itself. |
| Response lost after commit | BFF cannot safely infer whether N was consumed. A blind retry of N follows the consumed-token rule and may revoke the family. BFF clears its local token state and sends the user through login; a future bounded recovery mechanism requires a separate reviewed design. |
| Unknown, malformed, wrong-client, expired or revoked token | Uniform outward unauthorized response without confirming account/Session existence; audit internally with minimal necessary detail and rate limit attempts. Wrong-client attempts must not permit a third party to revoke an unrelated family merely by guessing identifiers. |
| Logout/absolute expiry | Atomically close/expire Session and disable current generation. A concurrent refresh and close serialize on the same authoritative Session state; close wins or the resulting successor is immediately unusable under the final Session state. |

On 2026-09-29 the owner selected the strict consumed-token response (family/Session revocation and explicit login) as the desired failure direction, including lost-response retries. Review denial-of-service trade-offs, retention and client concurrency before final architecture acceptance. Any grace/idempotent response replay must explain how a second presenter cannot obtain the successor and how bearer material is protected; this proposal selects no grace window.

## 4. Public and internal contract consequences

The existing proposed `POST /auth/refresh` takes `{refreshToken}` and returns `SessionTokens`. S2 requires a new refresh token in every successful response and invalidates the request token. The BFF must replace its protected stored secret only after a successful response, serialize use per Session, and clear it on ambiguous failure/reuse. The browser sees only its BFF cookie and an appropriate reauthentication state. Define whether access tokens are ever exposed to the browser in the final Kimia topology; do not assume current Identity/08 response shape is safe to forward unchanged.

A fixed absolute deadline is returned as Session `expiresAt`; distinguish access-token expiry from Session expiry in wire names and examples. Error shapes should not leak whether the attempted token belonged to a particular Person. Refresh has no new public Identity event in the current catalog; restricted security audit of reuse is an internal policy to specify, not an invented public event.

On family revocation, outstanding self-contained access tokens may remain usable until their short expiry unless resource servers check revocation/current Session. Choose and document that enforcement boundary; do not promise instant invalidation without it. Logout and password/credential-change effects on other Sessions require explicit existing-command reconciliation.

## 5. Required persistence, propagation and tests

- Review whether the durable refresh-family state is a Session-owned record or a separately governed Aggregate. Do not silently promote the archived `RefreshToken` storage concept into a sixth Identity Aggregate; preserve the five-Aggregate MVP unless a new architectural decision authorizes otherwise.
- Propagate to Identity 01/03/04/07/08/09/10/11/13, `openapi.yaml`, `capability.machine.yaml`, BFF contract and examples as one candidate. Remove the existing nonrotation text only after architecture/security approval; update version references and compatibility/migration plan.
- Test concurrent BFF instances and Identity workers, same-token racing requests, lost response after commit, reuse revocation, unknown/wrong-client abuse, logout/expiry race, PendingCredential, inactive Person, Credential change, key rotation and time-boundary behavior with durable persistence. Verify tokens are absent from logs/events and the browser.
- Record access TTL, absolute Session lifetime, retention window, rate limits, key policy, client authentication and cookie/CSRF policy after product/security review. The owner selected the platform's proposed 900-second access and 86400-second absolute Session values as Kimia design directions on 2026-09-29. They remain subject to contract/security review and are not approved active Blueprint configuration by this document.
- Attach exact revision/environment, reproducible test results, consumer/BFF compatibility and applicable 065 validation before implementation or deployment readiness claims.

## 6. Open approval questions

1. Confirm the selected strict consumed-token family revocation in architecture/security review, including forced login on lost response; specify alert thresholds and BFF concurrency controls. No bounded replay/grace protocol is selected.
2. Confirm owner-selected 86400-second absolute Session cap and 900-second access TTL in product/security review. Decide whether an idle timeout is desired *without* extending the absolute cap; none is selected here.
3. Does password change close this Session or all Sessions? How quickly must existing access tokens stop working after logout/revocation?
4. Who operates the BFF and Identity token store, owns incident response, and approves retention/key rotation?
5. Does the final client protocol use OAuth or a custom Identity session model? Verify confidential-client properties rather than assuming them.

Status: OPEN. BFF, S2, strict consumed-token revocation and 900/86400-second values are owner-selected design directions; this contract, idle policy and security/operational review require explicit acceptance.
