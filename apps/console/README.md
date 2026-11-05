# SmartCore Console

An original, bilingual fa/en platform shell with a module directory, category and
text filters, browser-local favorites, light/dark appearance and a responsive RTL/LTR
navigation. No paid template is required. Customer sites such as KimiaBeauty are
outside this shell.

## Run

Requires Node 24. From this directory:

```powershell
npm ci --ignore-scripts
npm run typecheck
npm run build
npm run start
```

Open `http://127.0.0.1:4100/fa` or `/en`. Application URLs are optional server-only
configuration in `.env.example`. An origin must be HTTPS, or HTTP on loopback;
credentials, paths, queries and fragments are rejected. Unknown module IDs return
404; unknown capabilities are never shown as operational.

The launcher does not forward cookies, tokens or arbitrary return URLs. It neither
implements SSO nor proves that another service is healthy. Each module owns its
existing authentication and authorization. It displays no invented accounts,
business metrics, notifications or customer data.

The console is public, because it is a capability directory. Actual organization
selection and business permissions require an authenticated BFF contract and are
deliberately not simulated here. Preferences contain only theme and module IDs.

## Design

Canonical tokens live in `../../packages/design`. The generated CSS/font snapshot
and `design-manifest.json` keep the app independently buildable. See that directory
for the synchronization and drift-check commands.

## Browser verification

Start the production server with Identity configured as `http://127.0.0.1:4101`.
Then run `npm run test:browser`. Install Playwright Chromium first if necessary.
Set `SMARTCORE_SCREENSHOTS` to a local output directory to save evidence.

The browser test covers module filters, persisted favorites, direction, configured
launch links, absent-service and 404 behavior, theme persistence, language switching,
mobile navigation/overflow, self-hosted fonts, CSP and browser runtime errors.
It does not certify the Identity backend, Business API or production deployment.
