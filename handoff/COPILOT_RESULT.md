# Copilot corrected-foundation contract handoff result

## Review branches and commits

- SmartCoreBusiness: `codex/business-domain-validation`, commit
  `f12c16096ba97f3474aefdb4a0ae9e2ac1ca7687`.
- SmartCoreBusinessCapability:
  `codex/business-capability-validation`, commit
  `9ea30194293a25828bb82d46d7bf8d499a2dab84`.
- Unified console: `codex/unified-console`, base/head before this contract result commit
  `21951b04b7d0f3a1d6ef6d636162627834baf717`.
- Unified console ownership correction commit:
  `03c5ba5` (to be followed by the result-record commit listed in Git status).
- Identity implementation review remains `codex/unified-identity-ui`, unchanged
  exact SHA `619c7583f94597a5f662704c981ec5d7ebf69816`.
- Legacy ServiceBusiness UI review remains `codex/unified-business-ui`, unchanged
  exact SHA `2d087c5c6f7936ec2662a93a25a458efde8c91d4`. Original legacy checkout HEAD:
  `6486e6888a13b53e83a39b1e20cfef301545710a`.

Verified remote main:

- SmartCoreBusiness: `bc6e668b306ef3a9a97067ab7a258ea60e3dd4e4`
- SmartCoreBusinessCapability: `671f37dee1907e3e703dab04ee1b7ddb48883e2f`
- SmartCorePlatform: `9fa0266b381b8f185af54a51747fefff6599fa92`

## Changes

- Added normalized locale parsing without an fa/en whitelist; malformed locales
  and normalized duplicate supported/translation keys fail explicitly.
- Business creation now requires the restricted default-locale translation and
  exposes frozen translations and copy-producing capability activation.
- Service creation strictly validates the external capability snapshot, category
  lookup boundary, cross-Business ownership, duration and identifiers.
- Added missing-category, foreign-category, capability snapshot, locale fallback,
  duplicate locale and corrupt default configuration regressions.
- Added the original SmartCoreIdentity checkout to the corrected workspace.
- Default Console workflow now builds/starts Console + Identity only.
- ServiceBusiness preview requires `--legacy-business-preview`; it is not linked
  by canonical module navigation and remains a visual/reference checkout.
- Updated AI Studio and continuation prompts to distinguish SmartCoreBusiness
  from SmartCoreBusinessCapability and label ServiceBusiness as reference only.
- Replaced loose positional locale parsing with Node `Intl.getCanonicalLocales`
  in both domains; `iw`/`he`, malformed tags, scripts, regions and extensions are
  covered consistently.
- Added strict `activateCapability` Business-context preconditions and a
  versioned JSON-safe capability/locale projection with validating restore.
- Added Service read-context same-Business enforcement and same-Business category,
  inactive snapshot, missing default translation and foreign category coverage.
- Added an executable cross-repository integration test using the actual
  SmartCoreBusiness and SmartCoreBusinessCapability implementations.
- Added a parameterized workspace generator/template preserving all 16 roots.

## Commands and results

- Business domain suite: `npm test` from `SmartCoreBusiness`, 10/10 passed.
- BusinessCapability domain suite: `npm test` from
  `SmartCoreBusinessCapability`, 9/9 passed, including the actual implementation
  cross-repository integration test.
- Standards matrix covered canonical scripts/regions/extensions, `iw`/`he`,
  malformed tags and JSON-safe projection restoration.
- Workspace generator syntax:
  `node tools/generate-corrected-workspace.mjs ...`; generated 16 roots with
  labels/path semantics matching the local corrected workspace.
- Added `REPRODUCIBILITY.md`, `RESTORE_FROM_GITHUB.md`, and a pinned
  GitHub Actions restoration workflow for the Business/Capability sibling layout.
- Fresh GitHub-backed clean restore completed with Node `v24.20.0`.
  Business restored at `f12c160...` and passed 10/10 tests.
  Capability restored at `9ea3019...` and passed 9/9 tests, including the actual
  cross-repository integration contract.
- Console and workflow scripts passed `node --check`.
- Corrected workspace: 16 folders, JSON valid, all resolved roots exist.
- `node tools/build-unified.mjs`: Console and Identity production builds passed.
- Default `node tools/start-unified.mjs`: Console and Identity started.
- Console Playwright suite: passed fa/en, RTL/LTR, favorites/search, unavailable
  foundation/capability states, CSP nonce, dark theme, fonts, 320/390px.
- Integrated browser suite: passed Console → Identity → Console and unavailable
  Business states. Legacy preview was not run.
- Identity private stack was not rerun. SHA `619c7583...` evidence remains prior
  CI evidence only and is reused at exact source SHA.
- Handoff ZIP regenerated with a five-file explicit allowlist. The archive was
  byte-verified against its current source files.

## Limitations

These are in-memory creation helpers, not a migration, HTTP API or production
backend. ServiceCategory persistence, base-price/Money decisions, Identity
authorization, database migration and external SMS/email providers remain out of
scope. No production database, VPS or external provider was touched.

## Decision status

Confirmed invariant: Business owns locale/profile and activation metadata;
BusinessCapability owns Service catalog semantics. Restricted creation currently
requires a default-locale translation; this is not an approved universal lifecycle
rule. Platform neutral implementation choices are reversible.

Unresolved: Organization-to-Business cardinality, slug uniqueness, lifecycle
transitions, Money/currency representation, capability dependencies, account/
organization authorization context, STAFF/CUSTOMER policy and service-provider
assignment.

## Uncommitted and out-of-repository files

- Root Platform correction workspace file is untracked in the large root checkout:
  `SmartCorePlatform_VSCode_Workspace/SmartCorePlatform.corrected.code-workspace`.
- Platform root local deletions and unrelated untracked files were preserved.
- Unified worktree changes listed in Git status before the next commit must be
  committed or remain explicitly dirty; they are not merged or pushed.

## Next runnable milestone

Implement one accepted persistence contract for Business creation and localized
profile only: choose a repository port, migration technology and real category
lookup adapter, without adding lifecycle transitions or Identity authorization
before those decisions are approved.
