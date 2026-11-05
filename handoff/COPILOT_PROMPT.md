# Paste into Copilot Agent in the unified VS Code workspace

You are continuing an existing SmartCore integration. Implement and verify the
next concrete milestone; do not restart the frontend or perform another broad audit.

Read these files first:

- `E:/miranco.project/SmartCore-unified/SmartCorePlatform/handoff/START_HERE.md`
- `E:/miranco.project/SmartCore-unified/SmartCorePlatform/handoff/CI_SNAPSHOT.md`
- `E:/miranco.project/SmartCore-unified/SmartCorePlatform/CONTINUE_HERE.md`
- `E:/miranco.project/SmartCore-unified/SmartCorePlatform/docs/continuation/VERIFICATION.md`
- Applicable AGENTS.md instructions, if any.

Work only in these isolated continuation checkouts:

1. Platform: `E:/miranco.project/SmartCore-unified/SmartCorePlatform`, branch
   `codex/unified-console`, PR amirfassadi/SmartCorePlatform#12.
2. Identity: `E:/miranco.project/SmartCore-unified/SmartCoreIdentity`, branch
   `codex/unified-identity-ui`, PR amirfassadi/SmartCoreIdentity#8, based on
   `review/identity-bff`.
3. Business: `E:/miranco.project/SmartCore-unified/SmartCoreServiceBusiness`, branch
   `codex/unified-business-ui`, PR amirfassadi/SmartCoreServiceBusiness#1.

Verify those branch names, actual HEADs and working changes before editing. Preserve
any new user changes. Older checkouts, unexplained deletions and archives are outside
this task. KimiaBeauty is explicitly postponed. Do not reset, clean, force-push,
delete old copies, merge the existing PR stack or mark proposed ADRs accepted.

The shared original shell already exists and has been browser-tested. Keep it:
Next.js 16.4.5, React 19.3, Persian/English, proper RTL/LTR, shared indigo design tokens,
self-hosted Vazirmatn, module discovery, filters/favorites and a light/dark console.
Do not install a dashboard template, copy template authentication or fabricate
dashboard metrics, users, businesses or operational module readiness.

NEXT MILESTONE: reuse the verified private Identity journey, define the explicit
console-to-Identity account/organization-context contract, and implement the
smallest connection already supported by approved contracts.

Execute in this order:

1. Inspect the current checks and compare the exact source SHAs to CI_SNAPSHOT.md.
   Identity's `619c758` already passed all six source workflows, and Business's
   `2d087c5` passed frontend CI. Reuse valid unchanged-source evidence. Do not rerun
   the whole stack or rebuild a private environment just to repeat these results.
   Fix any new failure and do not apply earlier evidence to changed source.
2. In Identity, read `docs/implementation/PRIVATE_WORKSPACE.md`, `PR_STACK.md`,
   `RELEASE_GATES.md`, `BFF_BROWSER_ACCOUNTS.md`, `BFF_BROWSER_REGISTRATION.md` and
   `BFF_BROWSER_RECOVERY.md`. Reuse their runner and tests; preserve the existing
   generated browser client, same-origin BFF guards, opaque session storage, CSP,
   contact verification and registration-readiness rules.
3. Prefer the existing Linux GitHub Actions environment for initial real-stack
   acceptance. Windows did not have dotnet/docker commands during the handoff;
   check current prerequisites, but do not spend the whole session trying to install
   a global toolchain. If a configured WSL/Linux environment is already available,
   use it with the documented isolated runner. Do not touch an unrelated database,
   production VPS, certificate trust store or operating-system service.
4. Preserve the verified sequence: register a synthetic test account with development
   contact verification, wait for Ready, explicitly sign in, read the profile,
   refresh, and log out. Reuse its passing CI baseline; rerun relevant suites when
   changes affect that sequence. Recovery is already covered by the existing suites.
   Keep Kavenegar and all external SMS/email/voice delivery off. Never log secrets,
   contact codes, recovery codes, session cookies or passwords.
5. Trace the console's existing launch link through to that verified Identity
   deployment. The console currently provides public navigation, not SSO. Do not
   infer authentication from a URL, localStorage or a selected business ID.
6. Where approved contracts already cover the connection, implement the smallest
   integration and test it end-to-end. If shared console authentication or selected
   organization/membership context is not covered, write a short
   `docs/continuation/CONSOLE_AUTH_CONTRACT_CANDIDATE.md` with existing-source
   references, concrete request/response examples, security boundaries, unresolved
   owner decisions and acceptance criteria. Mark it Proposed and continue useful
   independent work; do not invent or silently approve a new authorization model.

Shared styling source: Platform `packages/design/smartcore.css`. Generated copies
must be updated using Platform's `tools/sync-design.mjs`; never edit them by hand.
Each module remains independently buildable. The console may describe pending
modules, but must never label them as connected without evidence.

Google AI Studio may supply a design proposal or unified diff. Treat it as proposed
input, inspect against the current files and apply only relevant changes. You own
the source edits and verification. Keep auth/API work separate from visual changes.

Required checks for affected work:

- Shared design drift check across all three apps.
- Appropriate app typecheck/build; Business tests/lint if it changes.
- Existing Identity account and real-backend suites when account integration changes.
- Actual fa/en browser journeys and 320/390px layouts, with production CSP intact.
- New/changed PR checks at the exact source SHA.

At completion, write `handoff/COPILOT_RESULT.md` in Platform with changed files,
commits/PR links, actual commands/results, what was tested with real services versus
fixtures, any exact remaining prerequisite and the next runnable task. Commit and
push only the task branches; keep PRs Draft until their dependency gates are met.
Report in Persian. Do not ask for routine implementation choices already resolved
by this handoff; surface only missing decisions that materially affect the contract.
