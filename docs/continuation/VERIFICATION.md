# Unified UI verification — 2026-11-05

## Outcome

The isolated continuation contains a running Platform console and matching Identity
and Service Business interfaces. KimiaBeauty and the original checkouts are preserved.
These are review branches, not canonical merges or a production deployment.

## Evidence collected locally

| Check | Result |
| --- | --- |
| Console type checking and production build | Passed, Next.js 16.4.5 |
| Console production Chromium checks | Passed in Persian/English: module filtering/search, persistent favorites, configured links, unavailable modules, 404/BFF boundary, theme persistence, language switching, 320/390px navigation, font loading, nonce CSP, no runtime errors |
| Identity translation/time-zone checks, type checking and build | Passed |
| Existing Identity account UI suite | Passed with synthetic BFF replies and account/registration/recovery flags enabled: anonymous loading, password visibility, registration progress, profile/security navigation, logout, Persian/English, 320/390px layouts, no CSP/runtime errors |
| Final Identity preview | Rebuilt with account/registration/recovery flags disabled; fields disabled and zero BFF dispatch verified |
| Service Business type checking and build | Passed after Next/React/next-intl migration |
| Service Business existing tests + cross-tab regression | 7 files, 46 tests passed |
| Service Business ESLint | Passed, no warnings |
| Actual local cross-app navigation | Passed: console → Identity → console → Business; actual three servers, no API fixtures |
| Business browser checks | Passed: fa/en HTML language/direction, real categories route and active link, locale preserves route, 320/390px widths, no runtime errors |
| Design source drift | Three apps match canonical CSS SHA-256 `a8949b785e149ba86b5480a0bcdfde1c13475e4c6ce99a5b45a7b457892bb293` |
| Runtime dependency audit | `npm audit --omit=dev`: zero reported vulnerabilities in each of the three apps |
| Original working trees | Active Identity and Service Business remain clean. Legacy Identity still has the original ZIP/DOCX untracked files. Original Platform still has its 13 deletions and original untracked artifacts. |

## Corrections made during verification

- Updated Next.js to 16.4.5 across all three apps rather than retaining the
  vulnerable earlier framework versions.
- Patched Service Business source-map-js and moved Zod/resolver together to a
  compatible patched pair. Form tests and schema behavior remain covered.
- Fixed categories navigation pointing to an unimplemented placeholder route.
- Moved the Business document root into its locale layout so English is actually
  emitted as `lang=en dir=ltr`, including the server-rendered document.
- Fixed Business header overflow at narrow widths and included feature directories
  in Tailwind scanning.
- Typed query failures as the actual API error contract, removed redundant policy
  draft state and subscribed business context to its external storage source.

## Practical limits

No local .NET SDK was available. This task did not start the Identity backend,
PostgreSQL, Business API, SMS/email providers or the owner's VPS. The account UI
fixture suite is frontend regression evidence, not real-account acceptance.
Cross-app launch links establish navigation only; SSO, organization selection and
module authorization need their own reviewed contract and real-stack verification.
Only browser preferences are stored locally. No user/session tokens are shared.

The remaining module detail pages describe capability scope and visibly state that
integration is pending. They do not imply implemented services or live business data.
Existing Identity PR/ADR/release gates remain unresolved by this UI work.

## Reproduce

From the Platform worktree, after installing each app's dependencies:

```powershell
node tools/sync-design.mjs --identity ../SmartCoreIdentity --business ../SmartCoreServiceBusiness --check
node tools/build-unified.mjs
node tools/start-unified.mjs
```

In another terminal:

```powershell
npm run test:browser --prefix apps/console
node tools/check-integrated-ui.mjs
```

The existing enabled-account fixture regression is `web/identity/e2e/account-ui.mjs`
in Identity. It requires an enabled-account production build and Playwright browser
installation; the default final preview intentionally keeps account flags off.
