# SESSION — Identity refresh and lifetime policy review

Version: 0.1.0 — 2026-09-29 — DRAFT, no option selected
Decision authority: SmartCore architecture/security owner under 051; no approval or runtime evidence is recorded here.
Candidate source: SmartCorePlatform PR #5 at `91375b192dd0ec778529c4c7d8a785c94231269a`; SmartCoreIdentity PR #1 archived uploaded Blueprint. Re-pin both before decision.

## Decision boundary

Choose the refresh-token replay control, Session lifetime and access-token lifetime for the human Identity MVP. These are three independent dimensions. Rotation does **not** imply sliding expiry: a new refresh token can be issued on every refresh while every descendant remains bound to the original absolute Session deadline. A short access-token TTL does not detect replay of a stolen refresh token.

The OAuth security best-current-practice [RFC 9700 §4.14](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14) requires sender-constrained refresh tokens or rotation for *public OAuth clients*. Apply that conditional rule only after the client/protocol topology is confirmed; a confidential server-side client has different authentication/binding properties. If the implementation is not OAuth, use the same threat analysis as design input rather than claiming direct RFC conformance.

## Conflicting documentary inputs

| Concern | Uploaded Identity reference (historical, non-active) | Integrated platform proposal (Draft) |
|---|---|---|
| Access token lifetime | 10_Configuration §2.1: 1 hour | Identity/10: 900 seconds, never beyond Session expiry |
| Refresh token lifetime / Session expiry | 10_Configuration §2.1: 7 days refresh TTL; its exact relationship to a Session deadline needs reconciliation | Identity/10: 86400-second absolute Session lifetime, refresh does not extend |
| Rotation | 10_Configuration §2.1 requires rotation in Production; 11_Security §8.4 says the Domain Model does not require it and treats rotation as policy; 04_Commands §4.5 allows preserved or refreshed ID | Identity/04 §4.5 keeps the same refresh token in MVP; rotation/reuse detection deferred |
| Replay consequence | Archived 03/11 discuss a future token-family/reuse model; no unified active rule | Current proposed 04 has no rotation/reuse-detection contract |

The uploaded package itself contains a 10-versus-11 policy tension. Do not infer a single authoritative “local sliding policy” from the 7-day TTL alone; a refresh TTL, idle timeout, sliding extension and absolute Session deadline are different quantities. The old source remains evidence, not an automatically adopted active contract.

## Options for review

| Option | Replay control | Lifetime | Primary trade-off |
|---|---|---|---|
| S1: static bearer refresh | No rotation; only expiry/revocation and server-side Session check | Absolute cap, e.g. current proposed 24 hours | Simplest state transition, but a stolen bearer refresh token remains usable until revocation/expiry and reuse is not detected. Requires a separately justified client/topology threat assessment; unsuitable as an unexamined public OAuth default. |
| S2: rotating refresh family | Atomic one-time exchange, invalidation of predecessor, family reuse detection and revocation | Independent absolute Session cap; no automatic sliding | Detects replay, permits a predictable maximum login period; needs durable family state, concurrent-refresh handling and client recovery from lost responses. |
| S3: rotating refresh family with sliding idle window | Same replay control as S2 | Idle extension bounded by a separate maximum absolute lifetime | Better continuity, but more policy/state complexity and clear maximum lifetime still needed. |
| S4: sender-constrained refresh | Cryptographic binding to a client instance and proof validation | Independent absolute/idle policy | Alternative replay protection for suitable clients/protocols; key lifecycle and browser threat model must be reviewed. |

A protected server-side session/BFF may change whether a browser directly possesses refresh tokens. Choose the client topology before selecting S1–S4. Do not assert that rotation alone prevents all token theft or that a 15-minute access token compensates for an unprotected refresh token.

## Required contract if S2 or S3 is selected

- Define the atomic Session/refresh-family transaction, predecessor invalidation, stable token identity, hashed/otherwise protected storage, family generation, one-active-successor invariant and revocation on confirmed reuse.
- Specify two simultaneous legitimate refresh requests, an uncertain/lost response after server commit, changed request replay and user-visible reauthentication. A permissive grace window must not silently defeat reuse detection; any bounded exception needs an explicit threat review.
- Bind descendants to the original absolute deadline if absolute lifetime is selected. No refresh may issue an access token beyond that deadline. Define idle timeout separately if adopted.
- Specify logout, expiry, credential change, security incident and session-cap effects on the family and access-token validity. Clarify whether access-token revocation is immediate or bounded by token expiry.
- Define error shapes, no token leakage in URLs/logs/events, cookie or secure storage strategy by client type, CSRF/XSS defenses where applicable, audit data minimization and recovery/operations.
- Update 01/03/04/07/08/09/10/11/13, machine/OpenAPI and any Session examples consistently; validate concurrency, theft/replay, crash and clock-boundary scenarios.

## Evidence and decision record fields

1. Identify Kimia and other planned clients: browser SPA, BFF/server-rendered confidential client, native mobile, service client, and actual OAuth versus custom session protocol. Record which principal holds the refresh secret.
2. Threat model: XSS/CSRF, token exfiltration, device loss, replay, simultaneous tabs, provider/storage compromise, offline/revocation limits and acceptable forced-login frequency.
3. Choose replay control (S1–S4), access TTL, Session absolute cap and optional idle timeout independently. Record rationale and rejected alternatives, owner and compatibility/migration effect.
4. Run security/architecture review on the exact proposal. Only then amend the normative Blueprint and close the SESSION decision; runtime tests and deployment values remain later verification gates.
5. If SESSION selection is made an ADR-0002 pre-approval requirement, amend that ADR's architecture gate explicitly. This draft does not create such a prerequisite itself.

Status remains OPEN. No candidate option, number or client type is approved by this comparison.
