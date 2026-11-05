# SmartCore design foundation

The console, Identity account interface and Service Business admin share these
tokens, self-hosted Vazirmatn font assets and a generated SHA-256 manifest.
This original design does not depend on a paid template or copy a third-party dashboard.

`smartcore.css` is the canonical source. Each consuming repository commits an exact
copy so it can build independently, including in its existing CI and VPS bundle.
Do not hand-edit generated copies. After installing console dependencies, run:

```powershell
node tools/sync-design.mjs --identity ../SmartCoreIdentity --business ../SmartCoreServiceBusiness
node tools/sync-design.mjs --identity ../SmartCoreIdentity --business ../SmartCoreServiceBusiness --check
```

Use indigo for primary actions, semantic success/warning colors for actual state,
logical CSS properties for direction, 8/12/16px spacing, visible keyboard focus,
and native form controls. Keep dark theme tokens in this file. Do not introduce
customer-specific branding into the platform shell.

The console is a public capability directory and launcher, not an authenticated
dashboard. Never infer authentication from a configured app URL or from local
preferences. Module APIs must enforce their own identity and authorization.
