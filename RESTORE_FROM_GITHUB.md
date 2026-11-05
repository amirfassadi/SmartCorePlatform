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
  `f12c16096ba97f3474aefdb4a0ae9e2ac1ca7687`
- Capability repository:
  `codex/business-capability-validation` at
  `9ea30194293a25828bb82d46d7bf8d499a2dab84`

## Clean PowerShell restoration

```powershell
$root = Join-Path $env:TEMP "smartcore-reviewed-restore"
Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue
git clone https://github.com/amirfassadi/SmartCoreBusiness.git "$root/SmartCoreBusiness"
git -C "$root/SmartCoreBusiness" checkout --detach f12c16096ba97f3474aefdb4a0ae9e2ac1ca7687
git clone https://github.com/amirfassadi/SmartCoreBusinessCapability.git "$root/SmartCoreBusinessCapability"
git -C "$root/SmartCoreBusinessCapability" checkout --detach 9ea30194293a25828bb82d46d7bf8d499a2dab84
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
