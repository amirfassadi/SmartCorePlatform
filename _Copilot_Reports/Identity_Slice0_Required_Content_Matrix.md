# Identity required content: per-instance evidence matrix

Date: 2026-10-04. Review input: Platform `59e948d2dd975a9d4ecbf6f32255bc8303b5136c`, with this PR's editorial alignment of 03/06. Status: evidence mapping, no requirement or gate PASS granted.

This matrix inventories every item required by 064 §§8.3–8.7. Numbers refer to the current Identity document/section; e.g. `04 §4.2` means `Identity/04_Commands.md` §4.2. `~` marks an inferred/combined rather than explicit named field; it requires review. `OPEN` means the required declaration/mapping is not established. References to common rules must be checked for applicability to the individual item. A source reference is not a certification of semantic completeness.

## 064 §8.3 — nine use cases, seven required fields each

All rows are in 02 §2. The combined table columns are legitimate evidence, but they do not label every required field separately. 02 §3 applies to registration interruptions; do not apply those alternatives to unrelated operations.

| Use case | Goal | Actors | Preconditions | Main flow | Alternative flows | Failure conditions | Postconditions |
|---|---|---|---|---|---|---|---|
| UC-001 Register Person | ~02 row case | 02 row prospective Person | 04 §4.1 proof/shape | 02 row; 04 §4.1 | 02 §3; 04 §4.1 conflict/replay | 02 row; 08 §5 | ~02 result; 04 §4.1 Pending/Ready |
| UC-002 Create Credential | ~02 row case | 02 row authorized worker/completion | 02 row committed registration; 07 §3.1 | 07 §3.1 | 07 §3.1 winner/retry; 02 §3 setup | 07 §3.1 outcomes | 02 row one active; 07 §3.1 guarded winner |
| UC-003 Authenticate Person | ~02 row case | 02 row Person | 04 §4.2 | 04 §4.2 | ~04 §4.2 rejected/outage branches | 04 §4.2; 08 §5 | 02 row; 04 §4.2 Session/events or no Session |
| UC-004 Create Session | ~02 row case | 02 row AuthenticationDomainService | 02 row successful auth | ~02 row; 04 §4.2 | OPEN: explicit applicable alternatives | 02 row unavailable/no tokens | 02 row Active Session or remains Ready |
| UC-005 Manage Profile | ~02 row case | 02 row authenticated self | 04 §4.3 | 04 §4.3 | 04 §4.3 unchanged value/conflict | 04 §4.3; 08 §5 | 04 §4.3 snapshot/event or no-op |
| UC-006 Change Credential | ~02 row case | 02 row authenticated self | 04 §4.6; 02 §5 guard | 04 §4.6 | 02 §5 finalization-pending | 04 §4.6; 08 §7 | 02 row one active/event; Sessions unchanged in active Draft |
| UC-007 End Session | ~02 row case | 02 row self/worker | 02 row Active/elapsed; 04 §4.4 | 02 row CAS | 02 row logout vs expiry | 04 §4.4 missing/foreign/terminal | 02 row one terminal event; 06 §6.4 |
| UC-008 Create Membership | ~02 row case | 02 row registration process | ~02 row internal ownership substep | 09 §5.1 | OPEN: explicit applicable alternatives | 02 row rollback; 09 §5.1.2 | 02 row Owner Membership or complete rollback |
| UC-009 Refresh Session | ~02 row case | 02 row token holder | 04 §4.5 | 04 §4.5 | ~04 §4.5 rejection; SESSION candidate unresolved | 04 §4.5 invalid/expired/revoked | 04 §4.5 access reissue, no expiry extension/event |

A named explicit goal/postcondition reference or clear cross-reference can resolve `~` without duplicating behavior. Where no alternative is applicable, state that explicitly after review rather than inventing a new flow.

## 064 §8.4 — five aggregates, seven required fields each

| Aggregate | Root | Purpose | Owned entities | Value objects | Invariants | Consistency boundary | Relationships |
|---|---|---|---|---|---|---|---|
| Person | 03 §2 | 03 §2 responsibilities | 03 §2 None | 03 §2 Email/Mobile | 01 §§2/6; 09 §4 exactly one contact/unique identity | 03 §9 + 09 §5.2; proposed registration exception §5.1 | 01 Relationships; 03 §2 independence |
| Organization | 03 §3 | 03 §3 responsibilities | 03 §3 None | 03 §3 None | ~01 §6 ownership; 09 §4; root-specific completeness OPEN | 03 §9 + registration exception 09 §5.1 | 01 Relationships; 03 §3 ownership boundary |
| Membership | 03 §4 | 03 §4 participation | 03 §4 None | 03 §4 None/Role plain field | 01 Relationships; 09 §4 foreign keys; root-specific completeness OPEN | 03 §9 + registration exception 09 §5.1 | 03 §4 Person/Organization |
| Session | 03 §5 | 03 §5/7 | 03 §5 None | 03 §5 AccessTokenId/RefreshToken | 01 §6 gates; 04 §§4.2/4.4/4.5; 06 §6.4 | 03 §9; 09 §5.2 local Session/events | 03 §7 no persistence cascade; 01 Relationships |
| Credential | 03 §6 | 03 §§6/8 | 03 §6 None | 03 §6 PasswordHash | 01 §§6/11; 09 §§4/11 C01–C03 | 03 §9.2; 09 §6.1 local winner/guard | 03 §8 independence; 01 Relationships |

Repository declarations are in 09 §3. These pointers do not imply every broad lifecycle transition is an implemented MVP Command.

## 064 §8.5 — six commands, eight required fields each

| Command | Name | Purpose | Input | Validation | Authorization | Aggregate interaction | Resulting events | Failure conditions |
|---|---|---|---|---|---|---|---|---|
| RegisterPerson | 04 §4.1 | ~04 §4.1 process | 04 §4.1 | 04 §4.1; 12 §1 | 04 §4.1 proof/binding; 11 §1 | 04 §3; 09 §5.1 | 04 §5.1 ownership + later Ready | 04 §4.1; 08 §§3/5 |
| AuthenticatePerson | 04 §4.2 | ~04 §4.2 | 04 §4.2 | 04 §4.2; 12 §1 | 04 §4.2 current identity/readiness/Credential | 04 §4.2; 09 §5.2 | LoginSucceeded/SessionCreated; restricted LoginFailed | 04 §4.2; 08 §5 |
| UpdatePersonProfile | 04 §4.3 | ~04 §4.3 DisplayName only | 04 §4.3 | 04 §4.3 | 04 §4.3 self Session | 04 §4.3 Person/version | PersonUpdated; unchanged no event | 04 §4.3; 08 §5 |
| LogoutSession | 04 §4.4 | ~04 §4.4 | 04 §4.4 | 04 §4.4 ownership/state | 04 §4.4 caller | 04 §4.4 Session CAS | LogoutCompleted only winner | 04 §4.4; 08 §5 |
| RefreshSession | 04 §4.5 | ~04 §4.5 | 04 §4.5 | 04 §4.5 current gates/expiry | 04 §4.5 token; 11 §1 | 04 §4.5 Session; SESSION open | Explicit no public event; V-002 disposition OPEN | 04 §4.5; 08 §5 |
| ChangePassword | 04 §4.6 | ~04 §4.6 | 04 §4.6 | 04 §4.6 policy/current password/guard | 04 §4.6 authenticated self | 04 §4.6 Credential replacement | PasswordChanged only on success | 04 §4.6; 08 §7 |

Public wire contracts: 08 §§3–4/OpenAPI; interoperability: 07. V-004 requires a complete command-to-contract verification. V-002's literal at-least-one resulting Event also needs disposition for UpdatePersonProfile no-op and failing branches; do not fabricate events for no mutation.

## 064 §8.6 — five queries, seven required fields each

| Query | Purpose | Input | Output | Filtering | Sorting | Pagination | Security |
|---|---|---|---|---|---|---|---|
| GetCurrentPerson | ~05 row own identity | 05 row Session | 05 row self DTO | 05 §§1/2 self | ~single object; explicit applicability review | 05 row none | 05 §§1/3 |
| GetOrganizationsForPerson | ~05 row own Organizations | 05 row Session | 05 row Organization list | 05 row own Membership/no arbitrary filters | ~one MVP Organization; explicit applicability review | 05 row none | 05 §§1/3 |
| GetMembershipsForPerson | ~05 row own Memberships | 05 row Session | 05 row Membership list | 05 row own Owner Membership/no arbitrary filters | ~one MVP Membership; explicit applicability review | 05 row none | 05 §§1/3 |
| GetSessionsForPerson | ~05 row own active Sessions | 05 row Session | 05 row token-free summaries | 05 row active/unexpired/self | 05 row CreatedAt desc, SessionId asc | 05 row none, bounded cap | 05 §§1/3 |
| GetPersonById | 07 §2 minimal lookup | 05 row PersonId/service | 05 row PersonId/DisplayName | 05 row one target | ~single object; explicit applicability review | ~single object; explicit applicability review | 05 row allowlisted service; 07 §2 |

V-003 Aggregate attribution is not explicit in current machine query entries. For queries joining Membership and Organization, review exactly-one attribution/read-model semantics; do not infer a write consistency boundary from a read join.

## 064 §8.7 — ten events, seven required fields each

| Event | Name | Trigger | Payload | Producer | Consumers | Ordering | Idempotency |
|---|---|---|---|---|---|---|---|
| PersonRegistered | 06 §4.2 | 06 §4.2 Ready, not ownership commit | 06 §4.2 | 06 §4.2/§3 | OPEN: per-event declaration/inventory | 06 §6.1; T16 Proposed | 09 §6.4 stable EventId/unique Ready enqueue |
| OrganizationCreated | 06 §4.3 | 06 §4.3 ownership commit | 06 §4.3 | 06 §4.3/§3 | OPEN: per-event declaration/inventory | 06 §§6.1–6.3 cross-stream limits | 09 §5.1 Outbox; 07 §5 EventId; exact consumer coverage OPEN |
| MembershipCreated | 06 §4.4 | 06 §4.4 ownership commit | 06 §4.4 | 06 §4.4/§3 | OPEN: per-event declaration/inventory | 06 §§6.1–6.3 cross-stream limits | 09 §5.1 Outbox; 07 §5 EventId; exact consumer coverage OPEN |
| LoginSucceeded | 06 §4.5 | 04 §4.2 successful authentication commit | 06 §4.5 | 06 §4.5/§3 | OPEN: per-event declaration/inventory | 06 §6.2 no publish order vs SessionCreated | 07 §5 EventId; not in T16 stream |
| LoginFailed | 06 §4.6 | 06 §5.3 finalized rejection | 06 §4.6 restricted contact/reason | 06 §4.6/§3 | OPEN: restricted audit subscribers | 06 §6.1 excluded T16; audit contract separate | 07 §5 EventId; audit retry/retention review OPEN |
| SessionCreated | 06 §4.7 | 04 §4.2 local Session commit | 06 §4.7 | 06 §4.7/§3 | OPEN: per-event declaration/inventory | 06 §6.1 before terminal Session event | 07 §5 EventId; 09 §5.2 atomic enqueue |
| SessionExpired | 06 §4.8 | 02 UC-007 / 06 §6.4 terminal CAS | 06 §4.8 | 06 §4.8/§3 | OPEN: per-event declaration/inventory | 06 §§6.1/6.4 alternate terminal outcome | 02 UC-007 CAS; 07 §5 EventId |
| LogoutCompleted | 06 §4.9 | 04 §4.4 winning Closed CAS | 06 §4.9 | 06 §4.9/§3 | OPEN: per-event declaration/inventory | 06 §§6.1/6.4 alternate terminal outcome | 04 §4.4 no duplicate event; 07 §5 EventId |
| PersonUpdated | 06 §4.10 | 04 §4.3 changed DisplayName commit | 06 §4.10 | 06 §4.10/§3 | OPEN: per-event declaration/inventory | 06 §6.1 / 09 §6.4 T16 Proposed | 09 §6.4 EventId/position; 04 §4.3 no-op |
| PasswordChanged | 06 §4.11 | 04 §4.6 guarded replacement commit | 06 §4.11 | 06 §4.11/§3 | OPEN: per-event declaration/inventory | 06 §6.1 own Aggregate; no T16 | 07 §5 EventId; 09 §5.2 atomic enqueue |

Owner of all ten events is explicitly Identity in 06 §3. A producing Domain/Application Service is not itself the owning Capability Platform. Current checker producer-presence checks do not prove V-005; its owner declaration is documentary evidence in that table. Neither generic “Consumers SHALL” prose nor unknown subscriptions closes the per-event Consumers requirement.
