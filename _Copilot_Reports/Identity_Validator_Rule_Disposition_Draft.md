# Identity V-002 / V-003 disposition proposal

Version: 0.1.0 — 2026-10-04 (Asia/Tehran)
Status: Proposed / unsigned. Governance ADR identifier: UNASSIGNED.
Review input: Platform `630a22da53195a87d780aaf3c867bdd359eab83a`.
Authority requested: Amir (@amirfassadi), architecture owner, through 051 §§5–7/9. A change to validator policy requires architectural review and an ADR; classify its version impact before adoption. This report is preparation, not that approval. Active 065 text is unchanged.

## Context

065 §11 V-002 says every Command defines at least one resulting Event; V-003 says every Query references exactly one Aggregate. Both have FAIL severity. Identity/04 §4.5 declares no public Event for RefreshSession, and no internal result Event is declared. Identity/05 organization results are Membership-scoped and all self Queries use Session authorization. Machine publicEvents/resultAggregate annotations are documentary evidence, not satisfaction of these literal rules.

## Recommended proposed decision

Retain event accountability for state-changing business facts and prohibit fabricated Events. Permit a specifically governed no-public-result disposition for RefreshSession, without changing the public ten-Event catalog. Make the exactly-one Query constraint mean one declared primary result Aggregate, with explicit read-only dependencies and separate authorization dependencies. Both changes need explicit approval and propagation into the validator standard; a report annotation cannot override 065.

### Candidate replacement for V-002 — not effective

> Each Command SHALL declare its resulting Event facts and their emission conditions. An empty resulting-Event list SHALL produce FAIL unless an accepted, versioned governance disposition explicitly names that Command, scope, reason, state effects, audit requirements and reviewed alternatives. Invocation failure, rejected input and idempotent no-op paths SHALL NOT fabricate business Events. A public Event index is not the complete inventory of internal resulting facts.

Proposed sole initial exception: Identity RefreshSession, restricted to the reviewed Session continuation contract. Current nonrotation issuance and proposed S2 generation rotation have different state effects: review and record each; approval of one does not cover the other. No exception for other Commands is requested. Internal token-family persistence and reuse audit are mandatory under an accepted S2 contract even if there is no new public Event. This is a deliberate governed exception, not a claim that token rotation is a no-op. V-005 continues to apply to every actual Event.

Alternatives: (a) retain literal V-002 and design a real, commit-backed internal rotation fact only after S2 is adopted, with ownership, envelope, retention, emission and machine catalog fully specified; do not assume 'internal' removes these duties; (b) introduce a public Session event and review all consumers/catalog/version impacts. Neither is adopted here. Prefer the bounded exception over adding a fact only to satisfy the rule. If governance rejects exceptions, retain OPEN/FAIL disposition and evaluate (a), not an invented audit placeholder.

### Candidate replacement for V-003 — not effective

> Every Query SHALL declare exactly one primary result Aggregate, resolving to the capability Aggregate catalog. Any supporting data reads SHALL be declared separately as readDependencies; authorization reads SHALL be separately declared as authorizationDependencies. All dependencies SHALL be read-only and stay within permitted platform/service boundaries. Missing, unknown or multiple primary result Aggregates, undeclared dependencies, mutations or boundary violations SHALL produce FAIL.

This changes the literal meaning of 'reference'; it is not an editorial synonym. Primary result means DTO subject, not a new materialized Aggregate or a multi-Aggregate write exception. The proposal does not widen fields, caller scope or authentication eligibility.

| Query | Proposed primary result | Supporting data reads | Authorization source |
|---|---|---|---|
| GetCurrentPerson | Person | None beyond Person projection | Current authenticated Session; eligible caller checks remain applicable |
| GetPersonById | Person | None beyond Person projection | Allowlisted authenticated service identity, not Person Session |
| GetOrganizationsForPerson | Organization | Membership relationship scoped to caller | Current authenticated Session |
| GetMembershipsForPerson | Membership | None beyond Membership projection | Current authenticated Session |
| GetSessionsForPerson | Session | None beyond Session projection | Current authenticated Session; self scope |

These are the minimum declared narrative dependencies; acceptance requires tracing actual planned reads, including eligibility or policy lookups, rather than assuming this table is exhaustive. Authentication infrastructure is not a sixth Aggregate. The existing resultAggregate field remains a non-normative index until standard/schema naming is selected.

Alternatives: retain literal one-reference rule and redesign the organization query/read model through architectural review, or approve a specifically scoped Query exception. A new read model is not silently a new Aggregate; rebuilding the model solely to avoid documenting legitimate reads is not recommended.

## Propagation and review obligations

| Surface | Required action after decision |
|---|---|
| 065 §11; 064/066 dependent expectations | Publish accepted rule text/version and impact analysis; preserve all four implementation gates and V-008 |
| Identity 04/05/12/13 | Declare Event/no-result dispositions, result/read/auth boundaries, negative scenarios and accepted authority |
| capability.machine.yaml and machine contract | Define required rule fields and identifiers; resolve rule/schema version, not merely insert arbitrary keys |
| Required Content Matrix, examples, checker/validator | Update normative expectations and traceability; add substantive rule checks with invalid/missing references and unauthorized empty lists |
| SmartCoreIdentity proposal | Reconcile accepted authority/notes after Platform acceptance, preserving archived originals |

Validator acceptance scenarios: an unapproved empty Event list FAILS; an exception for RefreshSession cannot authorize RegisterPerson; a S1 exception cannot authorize S2 effects; unknown/multiple primary Aggregates FAIL; undeclared Membership reads FAIL; a Query mutation FAILS; service lookup scope remains narrow. These are planned checks, not executed semantic-validator evidence.

## Consequences and approval fields

A governed exception incurs maintenance responsibility and explicit scope review. Query clarification allows legitimate read composition but makes declarations and boundary validation mandatory. Whether this warrants a major or minor standard revision requires 051 impact review; do not publish it as a patch correction. Neither proposal modifies SFMM semantics, creates a bypass around 064, or closes GOV/T16/SESSION by itself.

Requested dispositions: accept / revise / reject for each rule independently. Owner/date, ADR identifier, accepted standard version, exact source revision, impact review and attributable record: PENDING. Until those exist, both findings remain OPEN and the current literal 065 rules remain authoritative.
