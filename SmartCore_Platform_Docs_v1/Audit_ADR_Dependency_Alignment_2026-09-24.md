# ADR Dependency Alignment Review

Date: 2026-09-24
Status: Partial documentation alignment complete; architecture decisions and full Blueprint validation remain open.
Repository baseline: ff07744e125dcb7624adbc636084a0121ab76c28

## Scope and reviewed revisions

| Document | Baseline | Revision | Result |
| --- | --- | --- | --- |
| 027 SmartCore Command Model | 1.2 | 1.2.1 | Pending approval qualification synchronized with ADR-0002. |
| 057 Tenancy and Ownership Model | 1.3 | 1.3.1 | Owner/Active defaults, full lifecycle transitions, and MVP exclusions synchronized. |
| 059 Identity Platform | 1.1 | 1.1.1 | Explicit ADR references, existing Application Service mapping, and lifecycle/MVP scope added. |
| ADR-0002 | 1.2.1 Proposed | Unchanged | Not accepted by this review. |
| ADR-0003 | 1.2.1 Proposed | Unchanged | Not accepted by this review. |

The three revisions are documentation corrections and propagation of existing
Proposed decisions. They introduce no public Command, Event, API, role, Aggregate,
transaction participant, or implementation authorization. The Normative document
headers do not convert their Proposed ADR dependencies into Accepted decisions.
Historical changelog entries remain historical; current qualification notes
explicitly correct their premature approval wording.

## Focused checks performed

- Confirmed the baseline branch and read all three documents and both ADRs from the same commit.
- Confirmed no AGENTS.md was present in the repository tree at that commit.
- Compared the revised text against the baseline.
- Confirmed 027's general command execution and failure rules are unchanged.
- Confirmed 057's core ownership transaction and post-commit participant list are unchanged.
- Confirmed 059's existing transaction phases, post-commit failure policy, event catalog, event timing, public API list, and authentication descriptions are unchanged.
- Matched the full Organization transition set to ADR-0003: Created → Active, Active → Suspended, Suspended → Active, Suspended → Archived.
- Confirmed Archived and Revoked remain terminal, initial MVP Organization/Membership states remain Active, and transition operations remain outside MVP.
- Confirmed both ADRs remain Proposed; no acceptance checkbox or date was completed.

Result: PASS for these focused documentation checks only. The complete Blueprint
Validator under 065 was not run. This report does not close GOV-01 or grant AI
code-generation readiness.

## Open decision D-01: failed-authentication event classification

Evidence:

- [027 §2, §11 and §14](027_SmartCore_Command_Model.md) permits Domain Events only for successful Commands and states that failure produces no Domain Events; optional System Events may be emitted.
- [059 §9 and §10](059_SmartCore_Identity_Platform.md) lists LoginFailed among the ten Identity-owned Domain Events.
- [ADR-0002 Decision 5](ADR-0002_Identity_Foundation_Clarifications.md) calls these domain events, includes LoginFailed, and defers security/audit classification outside its scope.

These statements are not reconciled by the RegisterPerson multi-Aggregate
exception. A decision is needed before claiming full architectural consistency.

Candidate A: classify LoginFailed as an Identity-owned security/audit event,
retaining the general failed-command rule. This requires deliberate updates to
ADR-0002, the event taxonomy/catalog, consumers/contracts, and the machine spec;
no such updates are made here.

Candidate B: explicitly allow a Domain Event representing a failed business
outcome, with a narrowly defined rule and scope in the governing documents.
This would amend the current Command/Event policy and needs architectural review.

Working recommendation: evaluate Candidate A first, including delivery and
consumer consequences. Neither candidate is approved by this report.

## Open decision D-02: post-commit Credential failure recovery

Evidence:

- [ADR-0002 Decision 1](ADR-0002_Identity_Foundation_Clarifications.md) separates the atomic ownership triple from subsequent Credential/Session operations.
- [059 §6 and Event Timing Note](059_SmartCore_Identity_Platform.md) preserves committed ownership on post-commit failure, requires Credential and initial Session before PersonRegistered publication, and leaves recovery implementation-specific.

A committed Person/Organization/Membership can therefore exist without a usable
Credential. This does not violate the documented ownership invariant. It does
require an explicit recovery and API-response design before implementation.
The Identity review must determine safe retries, proof of ownership, duplicate
email handling, and when the registration result/events become final.

No automatic retry policy, recovery API, new registration state, or expansion of
the core transaction is approved or introduced here. Review the current Identity
Blueprint before choosing the recovery behavior; moving Credential into the
atomic core would be a separate change to the current decision.

## Additional follow-up observations

- 027's historical v1.2 changelog says its promotion to Normative should be confirmed by Architecture Review. This editorial revision does not supply that approval evidence.
- 059 §7 says no domain data changes during login while its flow creates Session; this terminology should be clarified during Identity alignment.
- 059 §14's unqualified Messaging dependency exclusion needs comparison with the Identity Blueprint's Messaging Engine dependency. Establish whether these refer to different architectural components before editing the rule.
- The earlier supplied Identity archive contains a machine filename mismatch, an absent referenced validation-notes file, and inconsistent Domain Model version metadata. Those are observations about that supplied archive, not verified claims about a live Identity repository.

## Remaining closure work

1. Resolve D-01 with the architecture owner and propagate the chosen rule.
2. Read and align the current Identity Blueprint; resolve D-02 before implementation.
3. Reconcile Identity metadata, ADR references, and generation-readiness labels.
4. Verify the current machine package and required validation evidence under 064/065.
5. Record Architecture Validation Review and formal ADR acceptance only after all conditions are met.
6. Re-evaluate GOV-01 and generation readiness after acceptance; do not infer either from this patch.
