# Paste into Copilot Agent

Continue the corrected SmartCore foundation. Do not restart or migrate
SmartCoreServiceBusiness. KimiaBeauty remains postponed.

Primary workspace:

`E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/SmartCorePlatform.corrected.code-workspace`

Read `START_HERE.md`, the locale/profile contracts, creation slice and current
diffs before editing. Preserve candidate versus accepted decision status.

Owner-specific review bases:

1. Business foundation:
   `E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/repos/SmartCoreBusiness`
   branch `codex/business-domain-validation`.
2. Capability semantics:
   `E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/repos/SmartCoreBusinessCapability`
   branch `codex/business-capability-validation`.
3. Console:
   `E:/miranco.project/SmartCore-unified/SmartCorePlatform`
   branch `codex/unified-console`.
4. Identity implementation review:
   `E:/miranco.project/SmartCore-unified/SmartCoreIdentity`
   on the existing review branch; do not relabel the legacy checkout as this branch.

SmartCoreServiceBusiness is visual/reference reuse only. Do not copy its backend
or schema into the canonical foundation.

## Next bounded task

Design persistence ports for the existing executable creation contract:

- Business localized-profile create/read ports.
- Capability and locale data projection create/read/restore ports.
- Category lookup port using the existing same-Business contract.
- An explicit in-memory adapter example and contract-level storage boundary.

Do not implement SQL migration technology or an HTTP API unless separately
approved. Do not add lifecycle transitions, slug uniqueness, Money/currency,
STAFF/CUSTOMER, provider assignment, Organization cardinality or authorization
policy.

Remaining storage decisions must be listed as unresolved: locale/profile table
shape, capability snapshot freshness/ownership, category persistence location,
repository error taxonomy and migration technology.

## Required verification

1. Run both canonical domain suites.
2. Run the actual cross-repository contract test.
3. Re-run Console/Identity browser or build checks only for changed source.
4. Regenerate the corrected workspace context/archive only after handoff text is
   synchronized.

Commit only narrowly scoped review changes on the existing branches. Preserve
all user dirty/untracked work and do not merge, push or deploy directly to main.
