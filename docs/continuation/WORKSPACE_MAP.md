# SmartCore continuation map — 2026-11-05

## Selected sources

| Repository | Isolated continuation branch | Base |
| --- | --- | --- |
| SmartCorePlatform | `codex/unified-console` | fresh `origin/main`, `9fa0266` |
| SmartCoreIdentity | `codex/unified-identity-ui` | `origin/review/identity-bff`, `7000fba` |
| SmartCoreServiceBusiness | `codex/unified-business-ui` | fresh `origin/main`, `6486e68` |

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
Service Business already contains a phase-one admin interface and tests.

## Boundaries

- Platform owns navigation, capability discovery and the shared design foundation.
- Identity owns account, registration, recovery and the existing secure BFF flows.
- Service Business retains its own business context, API adapters and feature forms.
- The shell does not assert user identity, tenant selection, SSO or API readiness.
- The eight visible capabilities are a product navigation map, not a claim that
  all eight have implemented or connected production services. Business groups
  business/service-business capabilities into one entry point.
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
