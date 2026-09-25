<!--
Document ID: ID-10
Title: SmartCore Identity Platform Blueprint - Configuration
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity configuration contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Proposed defaults

These are reviewable MVP defaults, not measured operational guarantees. Production changes require security review and remain bounded; environment overrides cannot disable proof, uniqueness, readiness or atomicity.

| Setting | Default | Rule |
|---|---|---|
| verificationLifetimeSeconds | 600 | Absolute from creation; no resend/read extension |
| verificationMaxAttempts | 5 | Cumulative per session, including replay; atomic across workers |
| verificationMaxResends | 3 | Rotate code without resetting expiry/attempt count |
| resendMinIntervalSeconds | 60 | Applies independently of account existence |
| setupLifetimeSeconds | 600 | Absolute; separate purpose/proof from registration |
| setupMaxAttempts | 5 | Includes authorized replay attempts |
| secretDeletionDeadlineSeconds | 300 | Physical/cryptographic disposal after invalidation |
| provisioningMaterialLifetimeSeconds | 3600 | Absolute from ownership commit; never renewed by retries |
| provisioningMaxAttempts | 8 | Includes initial attempt; reconcile uncertain result before retry |
| provisioningInitialBackoffSeconds | 2 | Exponential with jitter |
| provisioningMaxBackoffSeconds | 300 | Cap; no infinite retry loop |
| dependencyTimeoutSeconds | 5 | Fail closed; classify uncertain writes and reconcile |
| reconciliationIntervalSeconds | 30 | Poll pending uncertain outcomes within bounded automated policy |
| maxActiveSessionsPerPerson | 20 | New login at cap fails with capacity error; no unbounded session query |
| sessionLifetimeSeconds | 86400 | Absolute; refresh does not extend |
| accessTokenLifetimeSeconds | 900 | Never beyond Session expiry |
| minPasswordLength | 15 | No silent truncation; allow spaces/Unicode |
| maxPasswordLength | 128 | Bound KDF abuse; explicit validation before staging |
| maxDisplayNameLength | 100 | Nonblank normalized text; output escaping remains mandatory |
| maxInitiationsPerContactPerHour | 5 | Applied to all canonical contacts, existing or not |
| maxInitiationsPerIpPerHour | 30 | Trusted ingress IP; combine with contact/device/global budgets |
| maxSetupDeliveriesPerContactPerHour | 3 | Distinct setup deliveries share a contact budget across fresh verification attempts |
| maxLoginAttemptsPerContactPer15Minutes | 10 | All existence states; shared distributed counter |

# 2. Deployment configuration

Require secret-store/KMS references, current and retiring HMAC key IDs, delivery provider credentials, service trust identities, Outbox destination and alert routing. No secret values in YAML/docs. Startup rejects missing security configuration or unsafe negative/unbounded values. Key retirement must allow valid bounded proof verification until expiry; retired keys cannot keep old proofs usable.

# 3. Operational policy gates

A global abuse budget and per-provider delivery caps must be sized before deployment and tested without existence-dependent behavior. Audit/event retention and legal deletion policy are deployment governance inputs, not guessed by these defaults. Secret disposal deadlines are independent and mandatory. Feature flags must not expose password login for PendingCredential or enable unreviewed contact changes.

# 4. ADR-0004 required operational settings (no implicit defaults)

The owner approved architecture, not numerical operational policy. The following keys are REQUIRED positive integers in machine.requiredConfiguration; their values remain unset until approved for the deployment. Startup/admission must fail closed for an unconfigured recovery feature; no missing value means unlimited. The acknowledgment worker also requires its own finite budget. A disabled/unconfigured recovery feature blocks rollout of this protocol; it is not a way to waive the accepted administrative design.

| Setting | Purpose |
|---|---|
| readyAcknowledgmentMaxAttempts | Finite automatic delivery budget before alert/re-drive |
| readyAcknowledgmentInitialBackoffSeconds | Initial retry delay |
| readyAcknowledgmentMaxBackoffSeconds | Cap, at least initial delay |
| recoveryAdmissionPermitLifetimeSeconds | Absolute admission validity |
| recoveryExecutionLifetimeSeconds | Fixed at admission; not extended by retries |
| recoveryMaxAttempts | Finite effectful dispatch budget per job |
| recoveryMaxAdmissionsPerOperatorPerHour | Rate limit on accepted jobs |
| recoveryMaxAdmissionsPerTargetPerHour | Shared target limit across operators |
| recoveryResultRetentionSeconds | Retention after both permit expiry and execution termination |
| administrativeAuditMaxBacklogCount | Maximum undelivered audit backlog before pausing new admin effects |
| administrativeAuditMaxBacklogAgeSeconds | Maximum undelivered audit age before pausing new admin effects |
| administrativeAuditRetentionDays | Retention-protected audit policy; separate from job/secret retention |
| stalledRegistrationAlertAfterSeconds | Detection/escalation threshold, never guard-release authority |

Require configured operator identity provider, MFA/step-up verification, action/environment/target grant policy, admission signing key reference, executor service identity, immutable audit destination, incident routing and accountable on-call assignment. Runtime grant provisioning and chosen values require operational sign-off; repository owner approval is not evidence those accounts or systems exist. Key retirement must not admit expired/revoked permits or destroy audit integrity.
