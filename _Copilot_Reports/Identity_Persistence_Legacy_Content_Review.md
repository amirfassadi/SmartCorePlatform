# Persistence compression: section-by-section source review

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: documentary comparison, not legacy behavior adoption or runtime verification.
Legacy: Platform main `9fa0266`, Identity/09_Persistence.md v1.0.9; 1448 split lines, 75230 text characters. Review input: `5ea92766f480fc8d16bc337272b4595078fe3112`, current 09 v1.3.1; output updates it to v1.3.2.

Read the full legacy operative body §§1–10, including subclauses, and the entire current 09. Legacy header/history contain earlier claims of approval/readiness; those labels are not adopted. Historical changelog was sampled, not exhaustively adjudicated. This is a section/requirement comparison, not proof of word-for-word equivalence or full architectural gate closure.

| Legacy section | Operative requirement | Current destination / disposition |
|---|---|---|
| 1 / 1.1 / 1.2 | Logical persistence scope; no physical database/ORM/DDL choice; no new semantic types | 09 §§1–2 retained. Old blanket exclusion of Outbox mechanics is superseded by ADR-0002 D8 and accepted ADR-0004 durable work/fact obligations. Event Sourcing/generic Event Store remain outside MVP |
| 2.1 | One Repository owns one root and cannot write another | 09 §§2–3 retained |
| 2.2 | Supporting storage cannot create an implicit Aggregate/command/coordination exception | 03 §9.1 / 09 §§2/5.3 retained with explicit application-owned supporting workflow |
| 3 | Five repositories; Update persists already-valid state; no implicit Delete | Current 09 §3 changes method names/surface to current minimal contact/auth/recovery model. No Delete exists. Update meaning restored explicitly in §12 |
| 3.1 | Read-method demand tied to actual Commands/Queries; own-ID lookup intrinsic | Current methods reviewed against 04/05; demand principle restated in §12. GetByEmail superseded by selected verified contact. Removed GetByPersonIdAndOrganizationId/GetById names are not blindly restored without current demand |
| 3.1.1 | Credential lookup zero-or-one, Sessions zero-or-many | Current 09 §3 explicit cardinality retained. Current Query also filters elapsed Sessions and caps active count, superseding legacy Status-only interpretation |
| 3.2 | Query projection may compose reads without cross-Repository writes | 05/09 read scope retained; literal V-003 and 028 scope/paging remain architectural issues, not closed by this comparison |
| 4 / 4.1 | Mirror model fields; immutable PersonId; unique Email | 01 / 09 §4 retained and updated to exactly one verified Email OR Mobile, both canonical uniqueness constraints |
| 4.2 | Organization identity, Personal category, Active MVP | 01 / 03 / 057 / ADR-0003 preserve proposed direct-Active initialization |
| 4.3 | Membership identity, references, Owner/Active, unique Person/Organization pair | Root/foreign keys and initial Owner/Active retained. Pair uniqueness was not explicit in compressed §4; restored in 09 §12 from legacy §8.3 |
| 4.4 | Session identity/Person/tokens/deadline/device fields | 01 fields retained. Optional IpAddress and Expired-or-Closed terminal alternatives align current narrative/schema; old sequential Expired→Closed diagram is superseded. Token lookup uniqueness restored in §12 |
| 4.5 | Credential identity; previous Replaced instance/new identity; hash protection; future types | Current one-active/winner/guard is stronger. Distinct replacement CredentialId/previous immutable identity restored in §12. Future password-history/types remain out of scope |
| 5 / 5.1 | Atomic three-Repository ownership creation; rollback all | 09 §§5.1–5.1.2 retained, extended with proof-consumption/workflow/material reference and Outbox records under proposed ADR-0002 D8/D9 |
| 5.1.1 | UoW alone commits shared transaction; no independent per-Repository commit | 09 §5.1.1 plus §3 retained explicitly |
| 5.1.2 / 5.3 | No automatic future registration writes join exception; every new exception governed | 09 §§5.1.3/5.3 retained; supporting records do not authorize another Aggregate type |
| 5.2 | Other Commands local; Credential replacement two instances same repository; refresh same Session | 09 §5.2 retained. Replacement identities clarified in §12. Legacy statement that refresh extends ExpiresAt is intentionally superseded by current fixed-cap 04/10; not a gap |
| 6 / 6.1 | Later transactions cannot reopen/rollback/recreate ownership | 09 §6 explicitly restored in earlier publication, retained |
| 6.2 | Recovery left implementation-specific | Superseded by reviewed provisioning/Ready/guard/ack/recovery contracts in 07 and accepted ADR-0004. Recovery is not free-form implementation permission |
| 6.3 | Committed ownership visible while Credential/Session absent | 09 §6.3 retained; minimal lookup can see PendingCredential. Self Queries still need valid Session and cannot infer auth eligibility from ownership |
| 7 / 7.0 | Promotion requires independent lifecycle/invariants/transaction needs and model/governance review | 03 §§11.1/12 and 09 supporting-state rules preserve review obligation. New application records need not become child records of PersonRepository |
| 7.1 | Refresh support belongs to Session; family rules require boundary reevaluation | 03 and SESSION candidates preserve unresolved S2 boundary review; no sixth Aggregate adopted |
| 7.2 | LoginHistory optional projection; failure not authentication ownership transaction | 09 §7 keeps optional audit projection. Required LoginFailed fact/restricted audit commitments are not waived by optional LoginHistory |
| 7.3 | Generic IdentityEvents/Event Store deferred | 09 §§1/7 retained, with mandatory durable Outboxes separately specified |
| 7.4 | Generic AuditLogs deferred; classification future | Generic subsystem remains excluded, but 11 and ADR-0004 now impose concrete restricted audit/privacy duties. Blanket deferment is intentionally superseded |
| 7.5 | No queryable PasswordHistory feature; old Credential rows not automatically deleted | 09 §§4/7/12 retained; lifetime of protected material is distinct from retained non-secret outcome evidence |
| 8.1 / 8.2 | Intra-root consistency, no general cross-root transactions | 03 §9 / 09 §§5–6 retained; proposed password-change fence is not active |
| 8.3 | Hard uniqueness: contact, membership pair, token lookup, one active Credential | Contact and one-active retained/strengthened; pair/token declarations restored in §12. No implementation/DDL claim |
| 8.4 / 8.4.1 | Detect stale updates or serialize; optimistic marker must exist and condition writes | 09 §8 retained; per-entity optimistic marker/write guard made explicit in §12; not a new business field or event-stream position |
| 9 / 9.1–9.6 | Cross-document alignment assertions | Current 09 §9 / content matrix provide source mapping; old check marks/READY_FOR_GENERATION are historical assertions, not current evidence |
| 10 / 10.1 | Checklist and Query-method citations | Current 09 §10 distinguishes draft design from unexecuted tests. Old 'no pending verification' does not certify current package |

Result: the reduced document length includes removed historical commentary and intentionally superseded contracts. It also lost explicit pair/token uniqueness and optimistic-marker/replacement-identity declarations, now restored as Draft requirements in §12. Larger future-scope prose is preserved through current model/governance references rather than copied wholesale. This review does not prove every old sentence has an accepted replacement; accepted authority/version/compatibility and the architectural findings still require owner disposition.
