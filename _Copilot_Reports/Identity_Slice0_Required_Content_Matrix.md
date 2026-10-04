# Identity required content: per-instance evidence matrix

Version: 0.2.0 — 2026-10-04. Input: Platform `5ea92766f480fc8d16bc337272b4595078fe3112`; output is the containing commit. Identity input unchanged at `ee9ffb767ed84165557793d8583b0750d887027b`.

All 35 instances / 251 cells required by 064 §§8.3–8.7 are mapped. `DOCUMENTED` means an explicit statement/pointer is present, **not** accepted behavior or a gate PASS. `REVIEW` and `OPEN` remain blocking review/decision work as applicable. Raw cells/status/limitations and source hashes: [evidence JSON](Identity_Required_Content_Evidence.json). Other 064 §8 content classes are mapped separately by tools/slice0_content_inventory.json; this matrix alone is not the complete Structural review.

Status counts: {"DOCUMENTED": 233, "OPEN": 11, "REVIEW": 7}. Counts are documentary coverage, never readiness percentages.

## 064 §8.3 — nine use cases, seven required fields each

| Use case | Goal | Actors | Preconditions | Main flow | Alternative flows | Failure conditions | Postconditions |
|---|---|---|---|---|---|---|---|
| UC-001 Register Person | 02 §6 UC-001 row, Goal column | 02 §6 UC-001 row, Actors column | 02 §6 UC-001 row, Preconditions column | 02 §6 UC-001 row, Main flow column | 02 §6 UC-001 row, Alternative flows column | 02 §6 UC-001 row, Failure conditions column | 02 §6 UC-001 row, Postconditions column |
| UC-002 Create Credential | 02 §6 UC-002 row, Goal column | 02 §6 UC-002 row, Actors column | 02 §6 UC-002 row, Preconditions column | 02 §6 UC-002 row, Main flow column | 02 §6 UC-002 row, Alternative flows column | 02 §6 UC-002 row, Failure conditions column | 02 §6 UC-002 row, Postconditions column |
| UC-003 Authenticate Person | 02 §6 UC-003 row, Goal column | 02 §6 UC-003 row, Actors column | 02 §6 UC-003 row, Preconditions column | 02 §6 UC-003 row, Main flow column | 02 §6 UC-003 row, Alternative flows column | 02 §6 UC-003 row, Failure conditions column | 02 §6 UC-003 row, Postconditions column |
| UC-004 Create Session | 02 §6 UC-004 row, Goal column | 02 §6 UC-004 row, Actors column | 02 §6 UC-004 row, Preconditions column | 02 §6 UC-004 row, Main flow column | 02 §6 UC-004 row, Alternative flows column | 02 §6 UC-004 row, Failure conditions column | 02 §6 UC-004 row, Postconditions column |
| UC-005 Manage Profile | 02 §6 UC-005 row, Goal column | 02 §6 UC-005 row, Actors column | 02 §6 UC-005 row, Preconditions column | 02 §6 UC-005 row, Main flow column | 02 §6 UC-005 row, Alternative flows column | 02 §6 UC-005 row, Failure conditions column | 02 §6 UC-005 row, Postconditions column |
| UC-006 Change Credential | 02 §6 UC-006 row, Goal column | 02 §6 UC-006 row, Actors column | 02 §6 UC-006 row, Preconditions column | 02 §6 UC-006 row, Main flow column | 02 §6 UC-006 row, Alternative flows column | 02 §6 UC-006 row, Failure conditions column | 02 §6 UC-006 row, Postconditions column |
| UC-007 End Session | 02 §6 UC-007 row, Goal column | 02 §6 UC-007 row, Actors column | 02 §6 UC-007 row, Preconditions column | 02 §6 UC-007 row, Main flow column | 02 §6 UC-007 row, Alternative flows column | 02 §6 UC-007 row, Failure conditions column | 02 §6 UC-007 row, Postconditions column |
| UC-008 Create Membership | 02 §6 UC-008 row, Goal column | 02 §6 UC-008 row, Actors column | 02 §6 UC-008 row, Preconditions column | 02 §6 UC-008 row, Main flow column | 02 §6 UC-008 row, Alternative flows column | 02 §6 UC-008 row, Failure conditions column | 02 §6 UC-008 row, Postconditions column |
| UC-009 Refresh Session | 02 §6 UC-009 row, Goal column | 02 §6 UC-009 row, Actors column | 02 §6 UC-009 row, Preconditions column | 02 §6 UC-009 row, Main flow column | 02 §6 UC-009 row, Alternative flows column | 02 §6 UC-009 row, Failure conditions column | 02 §6 UC-009 row, Postconditions column |

## 064 §8.4 — five aggregates, seven required fields each

| Aggregate | Root | Purpose | Owned entities | Value objects | Invariants | Consistency boundary | Relationships |
|---|---|---|---|---|---|---|---|
| Person | 03 §2 | 03 §2 responsibilities | 03 §2 None | 03 §2 Email/Mobile | 03 §12 Person row, Invariants column | 03 §12 Person row, Consistency boundary column | 03 §12 Person row, Relationships column |
| Organization | 03 §3 | 03 §3 responsibilities | 03 §3 None | 03 §3 None | 03 §12 Organization row, Invariants column | 03 §12 Organization row, Consistency boundary column | 03 §12 Organization row, Relationships column |
| Membership | 03 §4 | 03 §4 participation | 03 §4 None | 03 §4 None/Role plain field | 03 §12 Membership row, Invariants column | 03 §12 Membership row, Consistency boundary column | 03 §12 Membership row, Relationships column |
| Session | 03 §5 | 03 §5/7 | 03 §5 None | 03 §5 AccessTokenId/RefreshToken | 03 §12 Session row, Invariants column | 03 §12 Session row, Consistency boundary column | 03 §12 Session row, Relationships column |
| Credential | 03 §6 | 03 §§6/8 | 03 §6 None | 03 §6 PasswordHash | 03 §12 Credential row, Invariants column | 03 §12 Credential row, Consistency boundary column | 03 §12 Credential row, Relationships column |

## 064 §8.5 — six commands, eight required fields each

| Command | Name | Purpose | Input | Validation | Authorization | Aggregate interaction | Resulting events | Failure conditions |
|---|---|---|---|---|---|---|---|---|
| RegisterPerson | 04 §4.1 | 04 §9 RegisterPerson row | 04 §4.1 | 04 §4.1; 12 §1 | 04 §4.1 proof/binding; 11 §1 | 04 §3; 09 §5.1 | 04 §5.1 ownership + later Ready | 04 §4.1; 08 §§3/5 |
| AuthenticatePerson | 04 §4.2 | 04 §9 AuthenticatePerson row | 04 §4.2 | 04 §4.2; 12 §1 | 04 §4.2 current identity/readiness/Credential | 04 §4.2; 09 §5.2 | LoginSucceeded/SessionCreated; restricted LoginFailed | 04 §4.2; 08 §5 |
| UpdatePersonProfile | 04 §4.3 | 04 §9 UpdatePersonProfile row | 04 §4.3 | 04 §4.3 | 04 §4.3 self Session | 04 §4.3 Person/version | PersonUpdated; unchanged no event | 04 §4.3; 08 §5 |
| LogoutSession | 04 §4.4 | 04 §9 LogoutSession row | 04 §4.4 | 04 §4.4 ownership/state | 04 §4.4 caller | 04 §4.4 Session CAS | LogoutCompleted only winner | 04 §4.4; 08 §5 |
| RefreshSession | 04 §4.5 | 04 §9 RefreshSession row | 04 §4.5 | 04 §4.5 current gates/expiry | 04 §4.5 token; 11 §1 | 04 §4.5 Session; SESSION open | 04 §§4.5/8; V-002; rule disposition draft **OPEN** | 04 §4.5; 08 §5 |
| ChangePassword | 04 §4.6 | 04 §9 ChangePassword row | 04 §4.6 | 04 §4.6 policy/current password/guard | 04 §4.6 authenticated self | 04 §4.6 Credential replacement | PasswordChanged only on success | 04 §4.6; 08 §7 |

## 064 §8.6 — five queries, seven required fields each

| Query | Purpose | Input | Output | Filtering | Sorting | Pagination | Security |
|---|---|---|---|---|---|---|---|
| GetCurrentPerson | 05 §6 GetCurrentPerson row, Purpose column | 05 row Session | 05 row self DTO | 05 §§1/2 self | 05 §6 GetCurrentPerson row, Sorting column | 05 §6 GetCurrentPerson row, Pagination column | 05 §§1/3 |
| GetOrganizationsForPerson | 05 §6 GetOrganizationsForPerson row, Purpose column | 05 row Session | 05 row Organization list | 05 row own Membership/no arbitrary filters | 05 §6 GetOrganizationsForPerson row, Sorting column | 05 §6 GetOrganizationsForPerson row, Pagination column **REVIEW** | 05 §§1/3 |
| GetMembershipsForPerson | 05 §6 GetMembershipsForPerson row, Purpose column | 05 row Session | 05 row Membership list | 05 row own Owner Membership/no arbitrary filters | 05 §6 GetMembershipsForPerson row, Sorting column | 05 §6 GetMembershipsForPerson row, Pagination column **REVIEW** | 05 §§1/3 |
| GetSessionsForPerson | 05 §6 GetSessionsForPerson row, Purpose column | 05 row Session | 05 row token-free summaries | 05 row active/unexpired/self | 05 §6 GetSessionsForPerson row, Sorting column | 05 §6 GetSessionsForPerson row, Pagination column **REVIEW** | 05 §§1/3 |
| GetPersonById | 05 §6 GetPersonById row, Purpose column | 05 row PersonId/service | 05 row PersonId/DisplayName | 05 row one target | 05 §6 GetPersonById row, Sorting column | 05 §6 GetPersonById row, Pagination column | 05 row allowlisted service; 07 §2 |

## 064 §8.7 — ten events, seven required fields each

| Event | Name | Trigger | Payload | Producer | Consumers | Ordering | Idempotency |
|---|---|---|---|---|---|---|---|
| PersonRegistered | 06 §4.2 | 06 §4.2 Ready, not ownership commit | 06 §4.2 | 06 §4.2/§3 | 06 §10; Identity_Event_Consumer_Registry.md PersonRegistered row **OPEN** | 06 §6.1; T16 Proposed **REVIEW** | 09 §6.4 stable EventId/unique Ready enqueue |
| OrganizationCreated | 06 §4.3 | 06 §4.3 ownership commit | 06 §4.3 | 06 §4.3/§3 | 06 §10; Identity_Event_Consumer_Registry.md OrganizationCreated row **OPEN** | 06 §§6.1–6.3 cross-stream limits | 09 §5.1 Outbox; 07 §5 EventId; exact consumer coverage OPEN |
| MembershipCreated | 06 §4.4 | 06 §4.4 ownership commit | 06 §4.4 | 06 §4.4/§3 | 06 §10; Identity_Event_Consumer_Registry.md MembershipCreated row **OPEN** | 06 §§6.1–6.3 cross-stream limits | 09 §5.1 Outbox; 07 §5 EventId; exact consumer coverage OPEN |
| LoginSucceeded | 06 §4.5 | 04 §4.2 successful authentication commit | 06 §4.5 | 06 §4.5/§3 | 06 §10; Identity_Event_Consumer_Registry.md LoginSucceeded row **OPEN** | 06 §6.2 no publish order vs SessionCreated | 07 §5 EventId; not in T16 stream |
| LoginFailed | 06 §4.6 | 06 §5.3 finalized rejection | 06 §4.6 restricted contact/reason | 06 §4.6/§3 | 06 §10; Identity_Event_Consumer_Registry.md LoginFailed row **OPEN** | 06 §6.1 excluded T16; audit contract separate **REVIEW** | 07 §5 EventId; audit retry/retention review OPEN **REVIEW** |
| SessionCreated | 06 §4.7 | 04 §4.2 local Session commit | 06 §4.7 | 06 §4.7/§3 | 06 §10; Identity_Event_Consumer_Registry.md SessionCreated row **OPEN** | 06 §6.1 before terminal Session event | 07 §5 EventId; 09 §5.2 atomic enqueue |
| SessionExpired | 06 §4.8 | 02 UC-007 / 06 §6.4 terminal CAS | 06 §4.8 | 06 §4.8/§3 | 06 §10; Identity_Event_Consumer_Registry.md SessionExpired row **OPEN** | 06 §§6.1/6.4 alternate terminal outcome | 02 UC-007 CAS; 07 §5 EventId |
| LogoutCompleted | 06 §4.9 | 04 §4.4 winning Closed CAS | 06 §4.9 | 06 §4.9/§3 | 06 §10; Identity_Event_Consumer_Registry.md LogoutCompleted row **OPEN** | 06 §§6.1/6.4 alternate terminal outcome | 04 §4.4 no duplicate event; 07 §5 EventId |
| PersonUpdated | 06 §4.10 | 04 §4.3 changed DisplayName commit | 06 §4.10 | 06 §4.10/§3 | 06 §10; Identity_Event_Consumer_Registry.md PersonUpdated row **OPEN** | 06 §6.1 / 09 §6.4 T16 Proposed **REVIEW** | 09 §6.4 EventId/position; 04 §4.3 no-op |
| PasswordChanged | 06 §4.11 | 04 §4.6 guarded replacement commit | 06 §4.11 | 06 §4.11/§3 | 06 §10; Identity_Event_Consumer_Registry.md PasswordChanged row **OPEN** | 06 §6.1 own Aggregate; no T16 | 07 §5 EventId; 09 §5.2 atomic enqueue |

V-003 exactly-one Aggregate attribution is not among the seven Query fields in 064 §8.6 and remains a separate unresolved semantic rule. Explicit sorting/pagination applicability resolves the prior inferred-declaration cells; it does not waive 028 collection rules. No-public-event is not proof of an internal resulting Event. Consumer unknowns are now explicit but remain OPEN.

Root/owned entity/Value Object definitions in 03 §§2–6 and new §12 map all five roots without introducing Aggregate types. Each Command purpose is explicit in 04 §9. Use-case alternatives are applicability mappings of existing rejection/replay/rollback paths, not invented operations. Current static refresh and unchanged-Sessions-on-password-change behavior remains the Draft baseline; S2 is not adopted.

See [architecture review](Identity_Preimplementation_Architecture_Review.md), [legacy persistence review](Identity_Persistence_Legacy_Content_Review.md) and [decision packet](Identity_Next_Decision_Packet.md). Earlier matrix input and inferred locators remain available in Git history; supersession here is documentary only.
