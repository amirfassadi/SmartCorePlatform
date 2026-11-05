# Restore and verify the corrected Business implementation

## Required sibling layout

Clone both implementation repositories into sibling directories:

```text
<restore-root>/
  SmartCoreBusiness/
  SmartCoreBusinessCapability/
```

SmartCoreBusinessCapability's suite imports
`../../SmartCoreBusiness/src/domain/business.js`, so Business must remain beside
it rather than being replaced by a hand-maintained imitation.

## Compatible pinned refs

- Business repository:
  `codex/business-domain-validation` at
  `b0dc2391ee801a3ce20080b1933d300fab6d259a`
- Capability repository:
  `codex/business-capability-validation` at
  `b9904e53f85be43b269b6ea56f4661982cec0f76`

## Clean PowerShell restoration

```powershell
$root = Join-Path $env:TEMP "smartcore-reviewed-restore"
Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue
git clone https://github.com/amirfassadi/SmartCoreBusiness.git "$root/SmartCoreBusiness"
git -C "$root/SmartCoreBusiness" checkout --detach b0dc2391ee801a3ce20080b1933d300fab6d259a
git clone https://github.com/amirfassadi/SmartCoreBusinessCapability.git "$root/SmartCoreBusinessCapability"
git -C "$root/SmartCoreBusinessCapability" checkout --detach b9904e53f85be43b269b6ea56f4661982cec0f76
node --version
npm --prefix "$root/SmartCoreBusiness" test
npm --prefix "$root/SmartCoreBusinessCapability" test
git -C "$root/SmartCoreBusiness" rev-parse HEAD
git -C "$root/SmartCoreBusinessCapability" rev-parse HEAD
```

`Remove-Item $root` here is limited to a caller-created temporary restore directory.
Use Node 24. If GitHub access is unavailable or private access blocks cloning,
report the affected repository and clone error; do not expose credentials.
This evidence restores the reviewed in-memory implementation only. It does not
claim SQL, HTTP, production authorization or live backend recovery.

## GitHub Actions credential requirement

The previous workflow failed because the Platform workflow's default
`GITHUB_TOKEN` could not read the sibling Business repositories:
`repository ... not found`.

To restore from Actions, add a repository secret named
`SMARTCORE_REVIEW_TOKEN` to the `SmartCorePlatform` repository. The credential
must be a fine-grained PAT or existing GitHub App installation token with
read-only Contents access to only:

- `amirfassadi/SmartCoreBusiness`
- `amirfassadi/SmartCoreBusinessCapability`

Do not add repository administration, write contents, workflows, packages or
customer secret scopes. Do not place the token value in this guide, workflow,
logs, commits or handoff archive. If the owner has not configured the secret,
the workflow intentionally stops with a named configuration-error before any
sibling checkout or tests.
