<!--
Document ID: ID-12
Title: SmartCore Identity Platform Blueprint - Validation
Version: 1.0.0
Status: DRAFT
Purpose: Define the proposed Identity validation contract.
Dependencies: ADR-0002_Identity_Foundation_Clarifications, 064_SmartCore_Blueprint_Standard, 065_SmartCore_Blueprint_Validator_Specification
Change Log:
  - Version 1.0.0 (2026-09-24): Integrated verified-contact registration, PendingCredential/Ready, security and contract alignment. Initial proposed specification.
-->

> Proposed package. ADR-0002 is not accepted. Documentary alignment does not authorize generation or establish implementation/test compliance. See [validation gates](12_Validation.md).

# 1. Validation order

1. Transport shape/size and required headers; reject null/unknown fields.
2. Canonicalize selected contact consistently, validate password/name policy; apply existence-independent abuse limits.
3. Verify session purpose, absolute expiry, binding and code with atomic attempt counters.
4. Domain rules: contact uniqueness at commit, ownership invariants, single active Credential, self scope, workflow gate.
5. Atomic persistence/concurrency constraints; distinguish retryable infrastructure failure from definitive domain rejection.

No upstream pre-check replaces a storage uniqueness constraint. Contact changes cannot pass as profile changes. Policy (length, retry/time bounds), domain (ownership/readiness) and infrastructure (timeouts/storage failures) validation remain distinguishable internally, without leaking account state externally.

# 2. Package merge gate

Review the integrated 00–16, event, ADR and machine snapshot together. Partial merging of PRs #1–#4 or this replacement package leaves a mixed generation state. Rebase/revalidate after any overlapping merge. All current package headers stay DRAFT.

# 3. Evidence and acceptance

- [x] Documentary definitions of verified contact, workflow ownership, two-event ordering, service confirmation, disposal and API stages are present in this proposal.
- [ ] ADR-0002 and relevant ADR-0003 decisions accepted by governance.
- [ ] Explicit consumer inventory and compatibility/version migration review completed.
- [ ] Credential-service polling/winner protocol and proposed configuration defaults approved.
- [ ] OpenAPI/schema artifacts and generated-contract compatibility validated.
- [ ] Full 065 structural, semantic, contract, dependency, machine, MVP and quality-gate validation completed.
- [ ] Runtime/security/failure tests in 13 implemented and passed.
- [ ] KDF parameters, global abuse limits, service/KMS configuration and audit retention approved for deployment.

The repository's lightweight package check, when run, reports only the checks it actually executes. It is not the full 065 validator, does not prove runtime behavior and must not upgrade DRAFT to READY_FOR_GENERATION.
