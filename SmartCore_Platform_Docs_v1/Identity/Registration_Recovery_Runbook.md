<!--
Document ID: ID-OPS-01
Title: Identity Registration Recovery Runbook
Version: 1.0.0
Status: DRAFT
Purpose: Define restricted recovery procedure and unresolved deployment prerequisites.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, 07_Contracts.md, 09_Persistence.md, 10_Configuration.md, 11_Security.md
Change Log:
  - Version 1.0.0 (2026-09-25): Propagated accepted architectural recovery design; execution tooling/configuration and runtime verification remain unimplemented/unverified.
-->

# 1. Authority and readiness

Accountable architecture/security and operations/support owner: @amirfassadi, per the [signed record](../../_Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md). This is accountable ownership, not evidence of provisioned production operator permissions, an on-call rota, deployed tools or successful tests. Assign the executing identity/on-call route and approve all required 10 §4 values before enabling the protocol. All related runtime/security gates remain open.

No manual SQL edit, timer unlock, credential replacement, post-commit cancellation or fabricated Ready fact is part of this procedure. Audit failure cannot be overridden by an operator.

# 2. Detection and preparation

1. Monitor PendingCredential age, Ready acknowledgment age, protected-material cleanup and audit backlog against approved finite thresholds. Thresholds trigger investigation, never state transition authority.
2. Open an incident/ticket with a permitted reasonCode. Use the trusted internal operations view with MFA/step-up and explicit action/environment/target permission. Do not ask the Person for a password, OTP or binding secret.
3. PrepareRegistrationRecovery reads current target/state/version and returns a bound expiring permit and request identity only when eligible. Verify intended action and target. For pre-commit work choose InvalidatePreCommitAttempt; for a committed registration choose ReconcileCommittedRegistration. A consumed session is not a substitute registration identifier.
4. Submit the unchanged prepared descriptor using AdminRecoverStalledRegistration. Preserve recoveryRequestId/correlation for retry and result lookup, never copy the admissionPermit to logs or ticket comments. Accepted means queued, not resolved.

# 3. Follow-up and outcomes

| Result | Support/operator action |
|---|---|
| Accepted / Running | Query current job using GetRegistrationRecoveryResult under current authorization; do not create repeated jobs |
| Invalidated / AlreadyInvalidated | Tell support the pre-commit attempt cannot complete; track cleanupState until CleanupCompleted within policy. User may restart normal verification |
| AlreadyCommitted | No invalidation occurred; inspect authorized registration state and, if needed, prepare a fresh explicit reconciliation request. Do not delete transferred material |
| Reconciled / AlreadyReconciled | Confirm recorded Ready and matching acknowledgment, not merely an enqueued item. Tell support normal login is available subject to current Credential checks; do not promise a losing setup password was installed |
| RequiresNormalProvisioning | Leave the existing normal provisioning path intact; inspect its availability/material policy; do not supply an operator-selected candidate |
| RequiresUserSetup | Direct the user to the ordinary separately verified setup flow. Operator authorization is not proof to set their password |
| StaleTarget / NotEligible | Re-read current state and assess eligibility. Never force the stale snapshot |
| AdmissionExpired / AuthorizationExpired | Obtain fresh authorized preparation only if still required and permitted. Do not extend an old permit/job |
| RetryableUnavailable / BudgetExhausted | Investigate dependency/ack delivery; owner decides a fresh bounded re-drive after cause correction, preserving registration/Ready identities |
| IntegrityConflict | Escalate with non-secret identifiers and durable evidence to owner; preserve guard and ownership. No blind data repair or synthesized Ready |
| AuditUnavailable / backlog beyond bound | Pause administrative mutations and repair audit durability/delivery; no “best effort” bypass |
| Unauthorized / Forbidden | No target detail; audit denial and use normal access-grant escalation |

Job stop does not roll back committed normal workflow effects. Later ordinary completion is a newly observed fact, not proof the stopped job ran beyond its authority. Keep correlation and append outcome updates to the incident rather than rewriting audit.

# 4. Audit and closure

Verify durable job/effect/audit linkage, acknowledgment result when applicable and cleanup milestone. Audit records identify initiating operator and executing service, action, target, reason/ticket, versions/fact IDs, time, attempt and outcome. Exclude secrets and unnecessary contact values. Each store atomically retains evidence for its own effects; external immutable collection may lag only within approved bounds.

Operator/support roles cannot edit/purge the journal, external evidence or retention policy. Corrections are appended with links. Resolve the ticket only on a supported confirmed outcome or explicitly transfer an unresolved integrity/infrastructure incident to the accountable owner; do not label dispatch acceptance as recovery success.

# 5. Enablement checklist (not completed)

- [ ] Executing operator/worker identities, current grants, step-up checks and on-call route configured.
- [ ] All required finite configuration values and admission/audit key/storage policies approved and deployed.
- [ ] Tooling implements 07 §7 and all guarded state/audit transactions; no direct table-write support path.
- [ ] ADR-0004 §4.6 and 13's authorization/race/crash tests implemented and passed.
- [ ] Full applicable validation/upstream approvals completed before rollout.
