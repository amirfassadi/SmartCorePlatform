# Corrected SmartCore implementation manifest

## Canonical implementation

| Repository | Review branch | Implementation SHA | Role |
| --- | --- | --- | --- |
| https://github.com/amirfassadi/SmartCoreBusiness | `codex/business-domain-validation` | `f12c16096ba97f3474aefdb4a0ae9e2ac1ca7687` | Canonical Business foundation and locale/profile projection |
| https://github.com/amirfassadi/SmartCoreBusinessCapability | `codex/business-capability-validation` | `9ea30194293a25828bb82d46d7bf8d499a2dab84` | Canonical Service/Capability semantics |
| https://github.com/amirfassadi/SmartCorePlatform | `codex/unified-console` | PR #12 final review head | Console, ownership, workspace, restoration and implementation handoff |
| https://github.com/amirfassadi/SmartCoreIdentity | development review branch/commit | `619c7583f94597a5f662704c981ec5d7ebf69816` | Development Identity UI and implementation review evidence |
| https://github.com/amirfassadi/SmartCoreServiceBusiness | optional legacy UI view/branch | `2d087c5c6f7936ec2662a93a25a458efde8c91d4` | Legacy visual/reference UI only |

The Platform SHA is updated after the delivery commit and recorded in the latest
handoff. No manifest entry means `main` is the implementation authority.

## Ownership map

- SmartCoreBusiness owns generic Business data, locale/profile, supported default
  locale and capability activation metadata.
- SmartCoreBusinessCapability owns Service semantics, category lookup boundaries,
  Service creation and Service translation reads.
- SmartCoreIdentity owns canonical Identity implementation and authentication
  boundaries.
- SmartCoreServiceBusiness is not canonical Business infrastructure and does not
  own schema/API decisions for the new model.
- KimiaBeauty is postponed and absent from canonical module implementation.

The full workspace contains 16 roots. It preserves canonical and reconstructed
views, original legacy Identity and both IoT views. The optional UI workspace is
limited to the three isolated UI review checkouts.

## Local-only exclusions

The Git delivery does not claim a full machine backup. It excludes:

- root Platform unexplained deletions;
- unrelated local untracked files and credentials;
- private runtime environments, customer data, database dumps and secrets;
- private Identity stack execution output not committed by the source review;
- dependency/build folders and browser runtime artifacts.

The remaining workspace correction file in the original root checkout is
intentionally untracked. The portable generator recreates it from caller-supplied
roots:

```powershell
node tools/generate-corrected-workspace.mjs `
  --workspace-root <workspace-root> `
  --platform-root <platform-root> `
  --original-identity-root <original-identity-root> `
  --original-iot-root <original-iot-root> `
  --unified-root <unified-root> `
  --output <output-workspace>
```

The template contains labels/placeholders, not machine-specific absolute paths.

## GitHub restoration credential

GitHub Actions cross-repository checkout requires repository-secret
`SMARTCORE_REVIEW_TOKEN` with read-only Contents permission for the two pinned
Business repositories. The secret is an owner configuration, not a source code
deliverable. The workflow stops explicitly until this minimum read credential
is available. No credential is stored in this repository or archive.
