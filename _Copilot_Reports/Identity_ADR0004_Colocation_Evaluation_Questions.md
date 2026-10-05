# ADR-0004 Co-location Evaluation — Owner Question Sheet

**Version:** 0.1.0 Draft  
**Status:** Evaluation worksheet; no architecture selected  
**Purpose:** Decide whether the MVP should formally reopen ADR-0004 to evaluate a shared Credential/Identity persistence transaction boundary.  
**Authority:** SmartCorePlatform governance, 051 §7.  
**Input:** Accepted ADR-0004 v1.1.1 and its scoped acceptance record; Identity SESSION decision form v0.3.2 Draft.  

This worksheet does not amend ADR-0004. Co-location is a candidate to evaluate because the accepted ADR names it as a viable alternative if the separate-service release protocol is not justified for MVP. The current accepted guard/acknowledgment protocol remains authoritative until a formal change is accepted.

## Decision question

For the Identity MVP, should Credential and Session use a single authoritative persistence transaction boundary, or should they retain the separate persistence boundaries assumed by accepted ADR-0004?

**Do not treat “same database server” as proof of atomicity.** The proposal must identify the process/service that owns the transaction and serialization boundary. Separate services or independent transactions remain separate consistency boundaries even if they connect to the same PostgreSQL cluster.

## Questions to answer

### 1. What does “co-location” mean operationally?

- [ ] Same database cluster only, with separate services and independent transactions.
- [ ] Separate logical schemas/modules, but one application transaction owner and one local transaction for the specific Credential + Session operations.
- [ ] One Credential/Identity application and persistence boundary for the relevant operations.
- [ ] Other: ________________________________________________.

Which process can atomically commit Credential replacement, refresh-family revocation, and Session closure? Who owns that transaction? Which module owns each table and migration?

**Decision test:** if the answer is “same database, but separate services/commits,” explain what race is actually removed. If no shared transaction/serialization boundary exists, co-location has not replaced the fence/recovery protocol.

### 2. Which ADR-0004 registration invariants remain?

Record the disposition of each accepted invariant/mechanism; do not assume co-location removes it:

| ADR-0004 item | Why it exists | Keep / revise / remove and evidence |
|---|---|---|
| C01 — at most one active Credential per Person | Uniqueness across all supported mutation paths | ______________________________ |
| C02 — one immutable initial Credential winner per registration | Prevents candidate replacement after initial provisioning | ______________________________ |
| C03 — winner cannot be replaced/revoked before Identity Ready | Protects Ready against stale Credential evidence | ______________________________ |
| `ProvisionedAwaitingReady` guard | Holds C03 until authenticated Ready acknowledgment | ______________________________ |
| `AcknowledgeRegistrationReady` | Releases the pre-Ready Credential guard from a committed Ready fact | ______________________________ |
| Polling and durable idempotent results | Reconciles lost/uncertain provisioning responses | ______________________________ |
| Restricted `AdminRecoverStalledRegistration` and audit | Recovers/records stalled or inconsistent operations | ______________________________ |

Can initial Credential provisioning and Ready become one atomic local transaction in the proposed topology, or does Ready remain a later transaction after contact verification/ownership creation? If Ready remains later, what exact authoritative fact safely releases the guard?

### 3. Does the proposal cover both password-changing paths and authentication races?

The MVP proposal includes both authenticated ChangePassword and password reset. For each path, answer:

- Does the operation atomically replace Credential and close all Sessions/refresh families, including the current one?
- Can any login or refresh commit concurrently using the old Credential or a stale authorization decision?
- What is the serialization point shared by login, refresh, ChangePassword, and reset?
- What happens after a crash, timeout, lost response, or uncertain commit? Can the caller safely query/retry the same operation without repeating the mutation?
- Is issuance denied while an outcome is uncertain? When may login resume against the new Credential?
- How are audit facts committed with the mutation without logging password, OTP, proof, or token material?

If separate stores remain, the accepted fence/epoch protocol must cover **both** ChangePassword and reset, and serialize against login and refresh. If co-located, show the equivalent transaction/race guarantees rather than assuming they follow from table proximity.

### 4. What security and data ownership boundary is preserved?

- Which module/service is the sole writer for Credential state, Session state, and refresh-family state?
- How do DB roles, module APIs, migration ownership, and code review prevent unauthorized cross-module writes?
- Are secrets/verifiers still protected at rest, excluded from logs/events, and covered by key/access controls?
- Does the proposal alter Credential's independent ownership or merely change physical deployment? What is the security review evidence?
- Which separate backup/restore and point-in-time recovery procedures apply? What happens if Credential and Session data are restored to different points?

### 5. What availability and operational cost changes?

Compare the alternatives for:

- Registration/Ready availability when Credential or Identity components are unavailable.
- ChangePassword/reset while dependencies are degraded.
- Recovery from partial work, database outage, restore, and integrity conflict.
- Deployment/scaling/maintenance coupling introduced by one transaction owner.
- Cost of the current separate-store fence, idempotent operation/result lookup, recovery, and testing.

No quantitative workload or reliability benefit should be claimed without a measured or explicitly forecast input.

### 6. What does ADR-0004 Decision 4 still require?

Determine whether co-location actually removes any `AdminRecoverStalledRegistration` actions. Outbox delivery loss, process crashes after commit, audit recovery, and inconsistent restored data may still require controlled recovery even when local writes share a database. Do not delete the recovery design merely because cross-service reconciliation is reduced.

### 7. How will the architecture evolve if services split later?

- Is the shared transaction intentionally an MVP deployment constraint or a long-term platform rule?
- What data ownership/API boundary allows Credential and Identity to separate later without exposing tables or weakening C01–C03?
- What migration and dual-run/consistency plan would be required if the services later gain separate stores?

## Alternatives for owner disposition

- [ ] **Reopen ADR-0004 and select a shared transactional persistence boundary for the scoped MVP operations**, subject to the answers and invariants above. Update ADR-0004 formally; do not treat this worksheet as acceptance.
- [ ] **Retain ADR-0004's separate-boundary architecture** and complete the durable fence/epoch, idempotent Credential operation/outcome, login+refresh serialization, and recovery protocol for both password-changing paths.
- [ ] **Defer** because evidence is insufficient. Record the exact missing evidence and owner.

**Not an acceptable disposition:** “use one database” without naming the transaction owner, write authority, and serialization point.

## Required impact review if co-location is selected

Review and disposition at minimum: ADR-0004 Decisions 1–4 and acceptance record; Identity 01/03/04/07/08/09/10/11/12/13; services schema, OpenAPI, machine specification, PasswordChanged semantics, ChangePassword/reset contracts, Session/refresh persistence, security controls, recovery runbooks, and required race/failure conformance tests. Publish a coordinated Platform + Identity candidate and pin both exact SHAs. Preserve ADR-0004 history; create a governed revision or replacement rather than rewriting the accepted record as if co-location had already been selected.

## Owner record

- Selected disposition: _________________________________________________
- Exact ADR-0004 change/record ID: _______________________________________
- Reviewed Platform SHA: ________________________________________________
- Reviewed Identity SHA: ________________________________________________
- Credential/persistence owner: _________________________________________
- Identity/Session owner: _______________________________________________
- Security reviewer: ___________________________________________________
- Operations/recovery owner: ___________________________________________
- Evidence still required and accountable owner: ________________________
- Owner/date under 051 §7: ______________________________________________

**Status remains proposed until the attributable governance record is completed.**
