# SESSION S2 propagation map

Version: 0.2.0 — 2026-09-29 — DRAFT work list, no active contract changed
Source: [S2 BFF contract draft](Identity_SESSION_S2_BFF_Contract_Draft.md), Kimia owner-selected 900-second access TTL and 86400-second absolute Session cap. All figures and failure semantics still require architecture/security contract review. Baseline: SmartCorePlatform PR #5 at `91375b192dd0ec778529c4c7d8a785c94231269a`; re-pin before applying.

## Documentary delta by owner

| File or surface | Current proposal | Required S2 change before active adoption |
|---|---|---|
| Identity/01_Domain_Model | Session lists AccessTokenId, RefreshTokenId, ExpiresAt, Status; RefreshToken is protected continuation credential | Define Session-owned family/generation and absolute deadline semantics, and distinguish internal token identity from bearer secret. Do not add a sixth Aggregate by implication. |
| Identity/03_Aggregates | RefreshToken storage/ownership re-evaluation deferred | Decide whether family state is supporting Session persistence, with atomic one-current-generation guard; document revocation and concurrency invariant. Any Aggregate promotion requires separate governance. |
| Identity/04_Commands §4.5 | Keeps refresh token and Session expiry unchanged; rotation/reuse detection deferred | Replace nonrotation behavior with atomic consume/successor and strict consumed-predecessor family revocation. Keep absolute deadline unchanged and no new public event; define invalid/uncertain outcomes. |
| Identity/07_Contracts and services.schema.json | Current service contracts do not specify a BFF token-family operation | Define client authentication/binding, internal result and failure contract if service boundary is separate; do not expose verifier/family internals to general consumers. |
| Identity/08_API and openapi.yaml | POST /auth/refresh accepts refreshToken and returns SessionTokens; registration never returns a Session | State every successful refresh returns a different refresh token; distinguish access expiry from absolute Session expiry; generic failures; BFF owns bearer response and forwards only cookie/session state to browser. Review current login response too. |
| Identity/09_Persistence | SessionRepository Refresh/GetByRefreshToken; no documented family one-current-generation CAS | Store token verifier/generation, consumed predecessor retention and family/Session revocation atomically; specify lost-response and cleanup/key rotation. |
| Identity/10_Configuration | 900-second access, 86400-second absolute Session proposed; no S2 policy parameters | Retain selected numbers after approval; add finite token-family retention, rate/abuse and key settings, with no guessed defaults. Record owner-selected no separate idle timeout; align BFF cookie/session expiry. |
| Identity/11_Security | Stolen refresh token identified as threat, rotation contract not specified | Add BFF trust/cookie/CSRF model, server-side protected storage, client binding, reuse audit and revocation, concurrent-worker and network-loss analysis. Review bounded residual access validity up to 900 seconds and all-Session closure on password change. |
| Identity/13_Testing | Session refresh/expiry test plan is sparse | Add durable concurrency, lost-response, replay/theft, wrong-client, logout/expiry, all-Session password-change and access-token residual-validity tests. |
| Identity/14_MVP, 16_Examples, capability.machine.yaml | RefreshSession in MVP; machine marks Draft | Keep six Commands/five Aggregates/ten public events; update policy/operation metadata and examples without claiming generation readiness. |
| KimiaBeauty BFF | Existence and topology not verified by this documentation | Verify actual server boundary; use protected cookie, serialize per-Session refresh across BFF instances, protect server token store, handle reauthentication on ambiguity. |

## Acceptance order

1. Confirm BFF deployment/client authentication, token owner and OAuth versus custom protocol. Document cookie/CSRF and cross-origin behavior.
2. Review S2 invariants and strict reuse/relogin trade-off, especially legitimate concurrent tabs and lost response. Set finite retention/rate limits; review selected residual access validity and all-Session password-change closure. Review selected no-idle policy and cookie deadline; absolute cap remains 86400 seconds.
3. Accept a versioned SESSION architecture record with rejected alternatives, 900/86400 values and accountable security/operations owner. If made a GOV prerequisite, update ADR-0002's architecture gate explicitly.
4. Propagate the accepted contract in one coherent Platform Blueprint/machine/OpenAPI/service schema revision, then reconcile SmartCoreIdentity references. Do not edit archived uploaded source files.
5. Validate applicable 065 categories and implement/run security/concurrency tests on an exact revision before generation or release readiness.

Until steps 1–3 have review evidence, this map is a work plan. It does not replace the current Draft nonrotation contract or close SESSION.
