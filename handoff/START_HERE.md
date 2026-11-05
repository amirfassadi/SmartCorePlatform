# SmartCore: one workspace, two AI roles

## Open this workspace

`E:/miranco.project/SmartCore-unified/SmartCorePlatform/SmartCore-unified.code-workspace`

It contains the three isolated continuation checkouts. Keep using these paths;
the older `E:/miranco.project/SmartCorePlatform` trees are preserved evidence, not
the starting point for the new UI work. KimiaBeauty is postponed.

| Source | Current branch | GitHub review |
| --- | --- | --- |
| Platform and console | `codex/unified-console` | https://github.com/amirfassadi/SmartCorePlatform/pull/12 |
| Identity implementation | `codex/unified-identity-ui` | https://github.com/amirfassadi/SmartCoreIdentity/pull/8 |
| Service Business | `codex/unified-business-ui` | https://github.com/amirfassadi/SmartCoreServiceBusiness/pull/1 |

Identity #8 is based on `review/identity-bff`, not main. All three requests are
Draft; existing Identity and Platform contract/release dependencies still apply.
Do not flatten histories or merge draft stacks to make the workspace look clean.

## What already works

- Shared original design, self-hosted Vazirmatn, Persian/English and RTL/LTR.
- A console with eight capability entries, search, categories, browser favorites,
  light/dark preferences and responsive navigation.
- Matching Identity account and Service Business interfaces with return links.
- Actual local cross-app navigation, tested at desktop and 320/390px widths.
- Production builds/type checks for all three; Business lint and 46 tests pass.
- Identity's account UI fixture regression passes; it does not prove live backend
  acceptance. Account preview is intentionally disabled in the final UI-only build.
- Runtime dependency audits reported no vulnerabilities in the three apps.
- Platform console GitHub Actions completed successfully on the source and PR.
  Recheck current Identity/Business runs before claiming their remote status.

## See the result

Current preview: `http://127.0.0.1:4100/fa`, Identity `:4101`, Business `:4102`.
If the processes have stopped, from the Platform checkout run:

```powershell
node tools/start-unified.mjs
```

For a fresh checkout, install dependencies in `apps/console`,
`../SmartCoreIdentity/web/identity` and `../SmartCoreServiceBusiness/frontend`:

```powershell
npm ci --ignore-scripts
```

Then use `node tools/build-unified.mjs` and `node tools/start-unified.mjs` from
Platform. The scripts launch UIs only. No database or authentication is fabricated.

## Copilot owns implementation

Paste `COPILOT_PROMPT.md` into Copilot Agent in the unified VS Code workspace.
It should inspect the current CI and establish one real private Identity journey
before adding new modules. Use existing Linux CI rather than losing the first
session installing a Windows SDK/container stack. The source private runner
requires Linux, .NET 10, Docker Compose, Python and OpenSSL; the Windows host had
no `dotnet` or `docker` command during this audit. WSL's presence alone does not
prove that a configured Linux distribution or Docker engine exists.

## Google AI Studio owns design proposals

Give it `GOOGLE_AI_STUDIO_PROMPT.md` together with `AI_STUDIO_CONTEXT.md`.
The context is a curated public-source snapshot, not the entire workspace.
Optional current screenshots are in the local visualizations output for this chat.
AI Studio returns a design specification and proposed patches. Copilot reviews,
applies and verifies those patches; both tools must not edit the same files at once.

Regenerate the context after source changes with:

```powershell
python tools/build-ai-context.py
```

Never add `.env.local`, tokens, development inbox codes, customer data, session keys,
database dumps or private deployment configuration to the context bundle.

## Immediate priorities

1. Verify the three PR heads and CI. Fix any newly failing check.
2. Demonstrate real private registration → explicit sign-in → profile → logout
   using the existing Identity/BFF/PostgreSQL runner and acceptance tests, with no
   SMS/email provider. Record the exact commit and test evidence.
3. Define the smallest reviewed console-to-Identity authentication/context contract;
   the current launcher is public and does not provide SSO or select an organization.
4. Connect Service Business to its real API and verify business-scoped permission
   behavior. Then add Reservation/Scheduling, followed by the remaining modules.
5. Connect KimiaBeauty only after the platform paths are stable.
