<!--
Document ID: ID-12
Title: SmartCore Identity Platform Blueprint - Validation
Version: 1.1.0
Status: DRAFT
Purpose: Define the proposed Identity validation contract.
Dependencies: ADR-0004_Identity_Credential_Provisioning_Protocol, ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.1.0 (2026-09-25): Propagated architecturally accepted ADR-0004; contracts remain DRAFT, T16/upstream approval and runtime verification remain open.
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Architectural source: [ADR-0004](../ADR-0004_Identity_Credential_Provisioning_Protocol.md) is Accepted within the owner's signed scope. This contract is DRAFT; ADR-0002 remains Proposed, T16 remains open and no runtime/generation readiness is certified.

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Validation order

1. Transport shape/size and required headers; reject null/unknown fields.
2. Canonicalize selected contact consistently, validate password/name policy; apply existence-independent abuse limits.
3. Verify session purpose, absolute expiry, binding and code with atomic attempt counters.
4. Domain rules: contact uniqueness at commit, ownership invariants, single active Credential, self scope, workflow gate.
5. Atomic persistence/concurrency constraints; distinguish retryable infrastructure failure from definitive domain rejection.

No upstream pre-check replaces a storage uniqueness constraint. Contact changes cannot pass as profile changes. Policy (length, retry/time bounds), domain (ownership/readiness) and infrastructure (timeouts/storage failures) validation remain distinguishable internally, without leaking account state externally.

# 2. Package merge gate

Review PR #5's integrated 00–16, event, ADR and machine snapshot together. PRs #1–#4 are closed superseded, not merged. Rebase/revalidate against subsequent main changes. All current package headers stay DRAFT.

# 3. Evidence and acceptance

- [x] Documentary definitions of verified contact, workflow ownership, two-event ordering, service confirmation, disposal and API stages are present in this proposal.
- [ ] ADR-0002 and relevant ADR-0003 decisions accepted by governance.
- [ ] Explicit consumer inventory and compatibility/version migration review completed.
- [x] Owner accepted ADR-0004 v1.1.0 architecture at commit 16b720c (record); metadata v1.1.1 pins that approval.
- [ ] T16 shared event stream accepted separately.
- [ ] Concrete operational configuration/defaults and service/message encoding review approved; architectural acceptance alone does not select those values.
- [ ] OpenAPI/schema artifacts and generated-contract compatibility validated.
- [ ] Full 065 structural, semantic, contract, dependency, machine, MVP and quality-gate validation completed.
- [ ] Runtime/security/failure tests in 13 implemented and passed.
- [ ] KDF parameters, global abuse limits, service/KMS configuration and audit retention approved for deployment.

The repository's lightweight package check, when run, reports only the checks it actually executes. It is not the full 065 validator, does not prove runtime behavior and must not upgrade DRAFT to READY_FOR_GENERATION.

# 4. Scope of the propagation evidence

The signed [acceptance record](../../_Copilot_Reports/Identity_ADR-0004_Acceptance_Decision_Record.md) authorizes ADR-0004 architecture only. The current revision supplies documentary propagation across domain/supporting records, Commands, event attribution, service/API schemas, persistence, required configuration, security, runbook and testing plans. That is not completed implementation or consumer review.

Validation must separate message-shape tests from required semantic/runtime checks: action/target/snapshot/permit equality, current authorization, immutable winner generation, atomic Ready/event/ack Outbox, acknowledgment replay after password replacement, job/audit durability, deadlines/backlog limits and no new effect after permit cleanup. A passing package script proves only its explicitly listed checks. Upstream ADR approvals, T16, full 065, runtime tests and deployment configuration remain gates.
