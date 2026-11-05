# SmartCore continuation map — 2026-11-05

## Primary continuation entry

Use the full corrected workspace first:
`E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/SmartCorePlatform.corrected.code-workspace`.
The following three-repository workspace is an optional scoped UI review view only.

## Selected sources

| Repository | Isolated continuation branch | Base |
| --- | --- | --- |
| SmartCorePlatform | `codex/unified-console` | fresh `origin/main`, `9fa0266` |
| SmartCoreIdentity | `codex/unified-identity-ui` | `origin/review/identity-bff`, `7000fba` |
| SmartCoreServiceBusiness legacy/reference UI | `codex/unified-business-ui` | UI review worktree HEAD `2d087c5`; not canonical Business |

These are separate worktrees under `E:/miranco.project/SmartCore-unified`.
They preserve the original checkouts, divergent local commits, untracked files,
and the Platform checkout's 13 locally deleted Identity documents. No reset,
cleanup, canonical branch merge, or deployment is part of this UI integration.
Fetching updates remote references, but does not reconcile the original trees.

## Why these sources

The original Platform checkout is ten commits behind its fetched main. Starting
from fresh main avoids carrying unexplained local deletions into the console.
The active Identity main is documentation-only and diverges by one/three commits.
The legacy Identity checkout is also documentation-only. PR #7's implementation
branch contains the existing account UI, BFF, backend, migrations and tests, so
the UI continuation is stacked there rather than discarding that work.
Service Business remains a legacy implementation/reference: selected UI and utility
patterns may be reviewed, but its data model and backend are not the canonical
Business foundation. SmartCoreBusiness owns the foundation and
SmartCoreBusinessCapability owns capability semantics.

## Boundaries

- Platform owns navigation, capability discovery and the shared design foundation.
- Identity owns account, registration, recovery and the existing secure BFF flows.
- Service Business is legacy reuse/reference material only; it does not own the
  canonical new Business or Service models.
- Original legacy ServiceBusiness HEAD is `6486e68`; the UI review worktree HEAD is
  separately `2d087c5`. The two SHAs must not be assigned to the same checkout/branch.
- The shell does not assert user identity, tenant selection, SSO or API readiness.
- The visible capability entries are navigation proposals, not claims that every
  entry has an implementation or connected production service. Business is shown
  distinctly as the foundation and capability-composition surfaces; ServiceBusiness
  is not their launcher or canonical backend.
- KimiaBeauty remains an independent future example/customer surface.

## Canonical integration still required

Identity PR #7 is Draft and based on `review/identity-password-reset`. Its own
`PR_STACK.md` states that Platform #11, Identity #1/#2 and #4–#6 precede canonical
integration. Keep that dependency order and review contract provenance; do not
merge PR #3 as duplicate implementation. Existing ADR/release gates remain in
force. A successful frontend build does not approve architecture, production
release, external messaging, a VPS or database changes.

## Handoff to another agent

Open `SmartCore-unified.code-workspace`; read `CONTINUE_HERE.md` and the final
verification evidence. Continue in the three `codex/unified-*` branches. Inspect
`git diff` before editing. Preserve the separation of UI and API state, the nonce
CSP in Identity, generated BFF client contracts, and the existing account tests.
Use `node tools/sync-design.mjs --identity ../SmartCoreIdentity --business
../SmartCoreServiceBusiness --check` to check shared-style drift. Do not replace
real account flows with template authentication or fabricated dashboard data.
