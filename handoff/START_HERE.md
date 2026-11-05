# SmartCore corrected foundation handoff

## Primary workspace

Open the full workspace:

`E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/SmartCorePlatform.corrected.code-workspace`

It contains the canonical repositories and their labeled legacy, reconstructed and
postponed views. The optional UI review workspace remains a separate three-repo view.

## Canonical owners

- SmartCoreBusiness: foundation, Business/profile/locale and activation data.
- SmartCoreBusinessCapability: capability semantics, Service, ServiceCategory and
  capability-owned read/write contracts.
- SmartCoreIdentity: canonical Identity implementation.
- SmartCoreServiceBusiness: selective reuse and optional visual reference only. Its
  backend and schema are not the new Business foundation.
- KimiaBeauty: postponed.

## Default runnable workflow

Run Console plus the existing Identity UI:

```powershell
node tools/build-unified.mjs
node tools/start-unified.mjs
```

Default navigation:

- Console: `http://127.0.0.1:4100/fa`
- Identity UI: `http://127.0.0.1:4101`

Legacy ServiceBusiness preview is opt-in:

```powershell
node tools/build-unified.mjs --legacy-business-preview
node tools/start-unified.mjs --legacy-business-preview
```

Legacy preview is reference-only and is not a canonical Business operational link.

## Exact implementation bases

- Business review branch `codex/business-domain-validation`, HEAD after domain/projection
  work will be recorded in `COPILOT_RESULT.md`.
- BusinessCapability review branch `codex/business-capability-validation`.
- Console review branch `codex/unified-console`.
- Identity unchanged review SHA `619c7583f94597a5f662704c981ec5d7ebf69816`.
- Legacy UI review worktree SHA `2d087c5c6f7936ec2662a93a25a458efde8c91d4`.
- Original legacy ServiceBusiness checkout remains separate from the UI review head.

## Verified evidence scope

The current local evidence is limited to the in-memory Business and Capability
suites, workspace roots, Console scripts and browser/build checks where source
changed. Identity private-stack acceptance was not rerun. Reuse the unchanged
Identity SHA above only as prior evidence. Do not present it as live-stack evidence
from this task.

## Next bounded milestone

Define and document the concrete persistence ports for this accepted creation
slice only: Business/locale projection read/write, capability/locale projection
read/write and category lookup. Storage technology, SQL migrations, HTTP and
Identity authorization remain separate decisions.
