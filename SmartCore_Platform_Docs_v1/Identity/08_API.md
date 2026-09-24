<!--
Document ID: ID-08
Title: SmartCore Identity Platform Blueprint - REST API
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity rest api contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Replaces v1.0.3; prior text remains in Git history.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Conventions

Proposed JSON REST contract; camelCase names, UTC ISO-8601 timestamps, UUID identity references, opaque high-entropy verification/setup identifiers. Optional properties are omitted, never null. Reject unknown request fields. No passwords/codes/tokens in URLs, logs, errors or caches. All endpoints require TLS; authenticated endpoints use `Authorization: Bearer ...`. Responses containing identity/proof data use `Cache-Control: no-store`. Error body: `{ "error": { "code": "...", "message": "..." }, "traceId": "..." }`; messages never reveal secrets or unverified account existence.

# 2. Shared shapes

- Contact input: exactly one `email: string` or `mobile: string` (E.164); neither null. Normalize per 01.
- Person: `personId`, exactly one `email`/`mobile`, `displayName`, `status`, `createdAt`, `updatedAt`. GET/PATCH also return ETag for optimistic updates.
- Organization: `organizationId`, `name`, `category`, `status`, `createdAt`.
- Membership: `membershipId`, `personId`, `organizationId`, `role`, `status`, `createdAt`.
- SessionTokens: `sessionId`, `accessToken`, `refreshToken`, `expiresAt`. Bearer material is never a persistence identifier exposed accidentally.
- RegistrationResult: `registrationId`, `status: PendingCredential|Ready`, `ownershipCommittedAt`; `readyAt` only for Ready. No Person DTO, password, Credential or Session tokens.
- SessionSummary: `sessionId`, optional `deviceInfo`/`ipAddress`, `expiresAt`, `status`, `createdAt`; no tokens.

# 3. RegisterPerson protocol operations

These routes all belong to RegisterPerson, not separate public business Commands. Request binding is a client-generated 256-bit random `bindingSecret`, sent only in request bodies and stored server-side as a keyed verifier. Initiation `Idempotency-Key` is also a client-generated opaque random value. It scopes retries for a limited verification lifetime; it is not authorization. Reuse with changed input returns conflict independently of contact existence. Compare request digests with a server-keyed construction; do not retain a fast unkeyed password hash.

| Method and path | Request / authorization | Success |
|---|---|---|
| POST /auth/register | Contact input, password, displayName, bindingSecret; Idempotency-Key required | 202 `{verificationSessionId, expiresAt, status:"AwaitingVerification"}` for both existing and unused contacts |
| POST /auth/register/verify | verificationSessionId, code, bindingSecret | First committed ownership: 201 RegistrationResult; authorized repeat: 200 current RegistrationResult |
| POST /auth/register/resend | verificationSessionId, bindingSecret | 202 `{status:"Accepted"}` with uniform treatment of unknown/expired/existing-contact cases |
| POST /auth/register/setup | verificationSessionId, code, bindingSecret from a newly verified conflicting attempt | 202 `{setupChallengeId, expiresAt, status:"Accepted"}`; deliver separate setup code only when authorized PendingCredential exists |
| POST /auth/register/complete | setupChallengeId, code, bindingSecret, newPassword; Idempotency-Key required | 200 RegistrationResult if Ready; 202 RegistrationResult while active confirmation/reconciliation is pending |

Verify may be replayed to obtain current status only within the original proof window, with the same proof and binding. No unauthenticated GET-by-registrationId exists. Consuming proof prevents a second commit; it does not remove the bounded, keyed replay verifier. Resend after successful verification never issues a new verification proof or extends replay validity.

After valid proof, a uniqueness conflict returns 409 `CONTACT_UNAVAILABLE` with `error.nextAction:"RequestSetup"` only for a PendingCredential registration, otherwise `error.nextAction:"SignIn"`. This detail is available only to the proven contact holder. The conflicting attempt's password is invalidated immediately and deleted within 10's deadline, never reused for setup. A short-lived authorized setup-request mapping retains only proof/binding and target reference, bounded by the original verification expiry; no password reference.

Repeated authorized setup requests for the same conflicting verification session return the same setupChallengeId and expiry; they do not resend or rotate a consumed code. A lost delivery requires a fresh verification attempt under the same per-contact delivery budget. Setup always requires a distinct code delivered to the stored verified contact. setupChallengeId alone grants no authority. The setup is bound to registration, purpose and the original binding secret, single-use for mutation. Its keyed proof/result verifier allows identical authorized retries until absolute expiry; changed newPassword/idempotency key after consumption is conflict and cannot replace the winner. Invalid IDs/proofs/expiry/attempt exhaustion share `VERIFICATION_FAILED`. A decoy setup response must not grant access or reveal registration state without valid setup proof. After expiry, start fresh contact verification; do not extend consumed windows.

No initial Session is created by registration. Ready means the user may call login. Pending means neither login nor refresh can establish an authenticated Session. Automatic provisioning may win against setup; completion returns the existing outcome without promising that its submitted password won, and never overwrites the winning Credential.

# 4. Remaining Command and Query endpoints

| Method and path | Business operation | Request | Success |
|---|---|---|---|
| POST /auth/login | AuthenticatePerson | Contact input, password, optional deviceInfo | 200 `{person: Person, session: SessionTokens}` |
| POST /auth/logout | LogoutSession | `{sessionId}` + bearer | 204 |
| POST /auth/refresh | RefreshSession | `{refreshToken}` | 200 SessionTokens |
| GET /me | GetCurrentPerson | bearer | 200 Person + ETag |
| PATCH /me | UpdatePersonProfile | `{displayName}` + bearer + If-Match | 200 Person + ETag |
| POST /me/password | ChangePassword | `{currentPassword,newPassword}` + bearer | 204 |
| GET /organizations | GetOrganizationsForPerson | bearer | 200 array of Organization |
| GET /me/memberships | GetMembershipsForPerson | bearer | 200 array of Membership |
| GET /sessions | GetSessionsForPerson | bearer | 200 array of SessionSummary |

No public GetPersonById endpoint. No Email/Mobile mutation through PATCH /me. Request body `null`, duplicate contact fields or neither contact field are invalid. IP is derived from trusted ingress, not body input. Lists follow 05's ordering and scope.

# 5. Failures and retries

400 invalid shape/policy; 401 generic authentication or verification failure; 403 authenticated foreign-resource access; 404 missing own Session; 409 verified uniqueness, terminal Session or idempotency conflict; 412 stale If-Match; 428 missing If-Match; 429 rate limit; 503 unavailable dependency or Session-capacity limit; capacity detail is returned only after valid authentication. Apply status/body/latency/throttling rules uniformly across existence states before proof. Retry-After may expose policy but not existence. Invalid password, Person not found, PendingCredential and no active Credential all map to 401 `AUTHENTICATION_FAILED`.

An uncertain commit is not reported as definitive rollback. Retry the same key/proof; do not switch identity or password in a replay. Local setup acceptance may outlive an HTTP request but cannot authorize a candidate after challenge expiry unless its consumption and candidate binding were already durably committed.

# 6. Compatibility

The companion openapi.yaml defines these operations and capability.machine.yaml indexes their business mapping. Neither is an implemented API. Full OpenAPI/schema conformance validation, consumer migration review and runtime enforcement remain explicit gates in 12; this document does not mark them complete.
