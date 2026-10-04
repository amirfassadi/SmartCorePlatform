# Identity per-event consumer registry

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Input: Platform `5ea92766f480fc8d16bc337272b4595078fe3112`; output is the containing commit.
Status: inventory prepared, actual/planned subscriptions UNVERIFIED. This is not permission to subscribe, a consumer compatibility PASS, or satisfaction of the complete Consumers requirement in 064 §8.7.

| Event | Actual/planned subscriber and accountable owner | Verified processing semantics | Admission classification | Current state |
|---|---|---|---|---|
| PersonRegistered | UNKNOWN | UNKNOWN: registration fact versus projection/side effect | Versioned Identity contract; optional Email is personal data; proposed ordered stream | OPEN |
| PersonUpdated | UNKNOWN | UNKNOWN: latest-state versus every-transition | Versioned profile projection/privacy; proposed ordered stream | OPEN |
| OrganizationCreated | UNKNOWN | UNKNOWN | Ownership fact; not proof of completed authentication/Ready | OPEN |
| MembershipCreated | UNKNOWN | UNKNOWN | Participation fact; no business permission inferred | OPEN |
| LoginSucceeded | UNKNOWN | UNKNOWN | Authentication/audit access, 11_Security | OPEN |
| LoginFailed | UNKNOWN | UNKNOWN | Restricted Security Event; ContactValue/ExecutionContext require explicit audit authorization | OPEN |
| SessionCreated | UNKNOWN | UNKNOWN | Auth/session data access, 11_Security | OPEN |
| SessionExpired | UNKNOWN | UNKNOWN | Terminal Session fact; policy-specific access | OPEN |
| LogoutCompleted | UNKNOWN | UNKNOWN | Terminal Session fact; policy-specific access | OPEN |
| PasswordChanged | UNKNOWN | UNKNOWN | Credential-change fact, no credential secret; policy-specific access | OPEN |

Architecture examples in 060/063 name Business/Resource/Finance/IoT as possible consumers. They are not evidence that any module subscribes to a particular Event. Kimia BFF/registration UI is an API client until a real Event subscription is established. Platform-wide dependence on Identity is neither subscription inventory nor authorization to read restricted payloads.

Before admitting each actual/planned subscriber record: name and responsible owner, environment, internal/external client, accepted schema and transport version, fields/purpose/access classification, latest-state or every-transition needs, durable inbox/checkpoint and external-side-effect handling, replay/bootstrap/retention requirements, supported runtime/library, upgrade/migration responsibility, lag/failure thresholds and incident contact. Attach subscription/configuration or explicit owner-confirmed design evidence. Unknown is not a declaration of zero consumers.

No consumer was contacted and no external subscription was created. Decisions/verification remain with architecture/security and the assigned consumer/operations owners.
