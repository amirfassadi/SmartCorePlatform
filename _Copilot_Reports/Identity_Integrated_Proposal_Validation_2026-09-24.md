# Identity integrated proposal — limited validation report

Date: 2026-09-24
Status: DRAFT review evidence; NOT a generation approval
Baseline: `9fa0266b381b8f185af54a51747fefff6599fa92` on main

## Scope and provenance

Integrates the reviewed proposals from PR #1 (`725ed58`), #2 (`c90af51`), #3 (`37df22b`) and #4 (`0dc9071`) and completes the surrounding narrative/machine package. Main remains unchanged by this work. The integrated PR is a coherent alternative to merging those overlapping branches individually; rebase/reconcile if they merge first.

The rewritten narrative documents consolidate repeated legacy descriptions into current proposed contracts. Historical versions remain in Git; the persistence companion changelog is explicitly historical. This is a substantive package revision, not a readiness-label-only patch.

## Changes requiring review

- Exact-one verified Email/Mobile in the MVP; DisplayName-only profile changes; optional contact omitted rather than null.
- Multi-step RegisterPerson API with no automatic initial Session, bounded proof replay, distinct setup proof, and explicit login after Ready.
- Authenticated Credential polling and durable initial-winner deduplication; no pre-Ready independent replacement. Ready actor describes the actual transition, separately from candidate provenance.
- Configuration defaults, six-digit challenge with strict budgets, material ownership/disposal, secret/key handling and enumeration testing requirements.
- Existing event names retained; PersonRegistered/PersonUpdated omit Email for mobile-only Persons and do not add Mobile. LoginFailed has selected-contact security payload and internal readiness/inactive reasons.
- ADR v1.7 corrects the previous blanket non-breaking claim. Consumer inventory/version migration is still required.
- Contracts/API responsibilities separated per 064; canonical machine manifest, OpenAPI, event and internal-service schemas added.

## Executed checks

`python tools/check_identity_blueprint.py` (Python 3.12.14, PyYAML 6.0.3 in this workspace): 358/358 limited checks passed. The checker covers required document metadata/status/version mapping, relative file links, command/query/event counts, operation coverage, local schema references, configuration correspondence and selected positive/negative fixtures.

The fixture helper intentionally implements only the schema constructs used by those tests. It is not a general JSON Schema engine, does not validate every format and must not be presented as full OpenAPI/schema validation.

GFM parsed with the available Marked parser: 19 Markdown documents (17 normative package documents plus historical persistence log and ADR), 26 tables, 173 body rows. Every parsed table had consistent column counts. This is parser evidence, not a visual browser review.

`git diff --check`: passed.

## Not established

Full 065 structural/semantic/contract/dependency/machine/MVP/quality-gate compliance; full OpenAPI/JSON Schema conformance; visual rendering; deployed consumer compatibility; any implemented runtime/security/race test; production KDF/service/key configuration; ADR acceptance. See Identity/12_Validation.md and 13_Testing.md for explicit gates.

All 00–16 documents and the machine manifest remain DRAFT; ADR-0002 remains Proposed. No merge or READY_FOR_GENERATION transition is included.
