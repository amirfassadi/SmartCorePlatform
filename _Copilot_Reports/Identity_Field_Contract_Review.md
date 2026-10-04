# Identity field and contract review — Slice 0

Status: review evidence, not architectural acceptance or implementation permission.

## Reproducible inputs and scope

Platform input: `add04692a155fc05dfbbb3008326b923bab9b25c`; Identity registration proposal: `ee9ffb767ed84165557793d8583b0750d887027b`. The containing commit identifies the corrected output. Input and output inventories carry artifact hashes. Identity itself was not edited.

Compared active Platform 04/05/06, supporting 01/07/08/09/10, machine specification, OpenAPI and both JSON schemas; checked the Identity proposal workflow/reconciliation against these contracts. This is not an exhaustive equivalence review of the uploaded archive or every Foundation document.

Coverage: 14 REST operations; six Commands; five Queries; ten public Events; seven service-operation mappings (one lookup, three Credential, three recovery). Inventoried 22 OpenAPI, 21 service and ten event definitions, with 401 explicit property occurrences. Occurrences include conditional branches and are not distinct business fields. Inventory required flags describe only the local object, not inherited/composed requiredness.

## Findings and dispositions

| ID | Evidence locations | Behavioral effect | Correction or decision |
|---|---|---|---|
| F01 | 10_Configuration display-name policy; OpenAPI StartRegistration/Person/UpdateProfile and event PersonRegistered/PersonUpdated payloads | Whitespace-only display names were schema-valid despite nonblank policy | Added `\\S` patterns. Padding remains allowed; normalization is not proved. Draft contract versions advanced. Consumer compatibility review remains necessary because accepted input narrows. |
| F02 | 08_API cache convention; OpenAPI operation response headers | Error responses lacked the declared no-store guarantee | Declared `Cache-Control: no-store` for success and error responses. This checks the contract, not actual HTTP responses. |
| F03 / V-002 | 065 Command/Event rule; 04 §4.5; machine RefreshSession | No public result Event; no internal resulting Event is declared in the reviewed package | Explicit public-event index added without inventing an Event. Remains OPEN: design a real resulting fact, govern a rule clarification for operations with no business fact, or approve a specific exception through applicable governance. Empty publicEvents alone does not prove absence of every possible Event. |
| F04 / V-003 | 065 Query/Aggregate rule; 05; machine Queries | DTO subject and referenced data are different concepts; organization listing reads membership scope | Added resultAggregate index as result subject only. Exactly-one-reference interpretation remains OPEN. Decide whether the rule means primary result subject with declared supporting reads, or requires redesign/read-model boundaries; a specific exception also needs governance. |
| F05 | 06 producer/owner table; machine Events | Service producer must not be substituted for owning capability | Indexed existing `owner: Identity` separately from producers; no ownership redesign. |
| F06 | 07 service contracts; services.schema.json root and $defs; machine schema references | Validating the definitions-container root can accept arbitrary data | Documented validation at the operation's indexed $defs entry point. Root acceptance is not operation conformance. |
| F07 / T16 | 07 §5; 09 §6.4; event schemas' closed envelopes | Ordered delivery positions belong to transport metadata; adding them directly to the closed Event envelope would fail schema | No field invented. Decide canonical transport encoding, position representation and atomic persistence responsibilities with T16. Existing at-least-once/dedup commitments do not select a transport option. |
| F08 | 06 §3/§4.6; LoginFailed schema conditional ExecutionContext | When ActorIdentity is absent, the current condition also requires correlation context; unknown-Person correlation handling is not explicit in the narrative exception | Clarify whether every finalized failed attempt requires correlation, including unresolved Person, or scope the condition to a present actor. Do not silently change privacy/audit semantics. |
| F09 / SESSION | 01 Session expiry; 04 refresh; OpenAPI SessionTokens.expiresAt; SESSION candidate | A single expiry field needs an explicit meaning when access-token lifetime and Session absolute deadline differ | Decide access-token versus Session deadline meaning and any distinct wire fields before adopting S2. No rotation, revocation or password-change policy was selected here. |
| F10 | 10 configurable bounds; OpenAPI pinned name/password/contact bounds | Deployment overrides may admit inputs outside the versioned wire contract | Freeze permitted configuration ranges relative to the schema or define versioned policy changes. No arbitrary bounds changed. |
| F11 | 06 canonical ContactValue; event schema; 07 materialOwner bindings; service schemas | Shape-valid messages can still violate normalization, identity equality, authorization, expiry or transaction rules | Explicitly retain runtime obligations. A fixture demonstrates differing materialOwner/registration identities are shape-valid: it is a limitation witness, not a permission. |
| F12 | Identity proposal authority pin and dossier; Platform ADR-0002 draft; Identity main README historical v1.5 | Proposal references the older baseline and separately declares later review; it is not acceptance of the new output | Record selected authoritative version only after governance selection. Do not replace historical pins globally or promote Proposed ADRs. |

F08 is a precise ambiguity, not a certified semantic FAIL. The schema's `if` properties test does not require ActorIdentity to exist, so omission still satisfies that test. Required correlation is observed in the schema; its intended treatment for unresolved actors needs clarification.

## Command and Query coverage

Public Event lists are possible outcomes, not a requirement to emit every listed Event for every invocation. Failure/no-op cases still follow the narrative.

| Command | Existing public outcome index |
|---|---|
| RegisterPerson | OrganizationCreated, MembershipCreated, PersonRegistered |
| AuthenticatePerson | LoginSucceeded, SessionCreated, LoginFailed |
| UpdatePersonProfile | PersonUpdated |
| LogoutSession | LogoutCompleted |
| RefreshSession | Empty; V-002 disposition OPEN |
| ChangePassword | PasswordChanged |

| Query | Result subject | Review boundary |
|---|---|---|
| GetCurrentPerson | Person | Authentication remains required |
| GetPersonById | Person | Caller scope remains required |
| GetOrganizationsForPerson | Organization | Membership supplies scope; result index does not erase this dependency |
| GetMembershipsForPerson | Membership | Caller scope remains required |
| GetSessionsForPerson | Session | Self-access authorization remains required |

Exact machine identifiers and complete constraints are retained in the inventory; this table uses the narrative operation names. The annotation is not a new Aggregate and does not certify V-003.

All ten Event payload tables match their schema property names and requiredness after handling escaped table delimiters and conditional notes. `Identity_Event_Payload_Comparison.json` contains individual evidence. Equal names/requiredness do not establish equal lifecycle, privacy, delivery, time or causal semantics. REST projections intentionally differ from service and public Event envelopes; no universal field union was imposed.

Recovery reason-code allowlists, ticket validation, endpoint-specific admissible error codes, ownership/material binding, UUID equality, token expiry, source-bound credentials, concurrency, outbox/dedup and crash recovery still need behavioral validation. Schema formats do not prove these rules.

## Validation and limits

- Focused schema/contract checker: **557/557 checks**, zero failures, across 53 named definitions and selected fixtures. Positive fixture per definition; unknown/null field negatives; contact-choice and nonblank-name cases; HTTP no-store declarations; Event payload-name/requiredness comparison. Union/conditional branches are not exhaustively covered.
- Existing package helper: **430/430 limited checks**.
- Structural checker: **296 PASS, 6 WARN, 97 INFO**, zero FAIL; this still does not certify the complete Structural gate.
- Four existing isolated negative controls fail as intended: missing heading, broken dependency, invalid schema pointer and duplicate command.

Reproduce with dependencies from tools/slice0-requirements.txt:

```sh
python tools/inventory_identity_fields.py
python tools/check_identity_contract_fields.py --json
python tools/check_identity_blueprint.py
python tools/slice0_structural_065.py --json
python tools/check_slice0_negative_controls.py
```

No runtime tests, consumer compatibility tests, full Architecture Validation Review, complete 065 Semantic validation, security certification or implementation were performed. All four 064 gates remain unclosed. `generationAllowed=false` remains in force; ADR-0002/0003 remain Proposed, and T16/SESSION remain open. These counts measure specific checks, not readiness percentages.

## Proposed next decisions

Prefer one full Identity MVP Blueprint with registration-first delivery phases; this is a recommendation, not an adopted scope change. Prepare explicit dispositions for V-002/V-003, T16, SESSION and accepted authoritative versions, then review remaining semantic requirements and architectural gates. No decision signature is fabricated. The separate stack proposal can be reviewed in parallel and does not unlock generation.
