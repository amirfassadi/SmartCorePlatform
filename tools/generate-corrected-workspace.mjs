import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  if (process.argv[index]?.startsWith("--")) args.set(process.argv[index], process.argv[index + 1]);
}

function required(name, fallback) {
  const value = args.get(name) ?? fallback;
  if (!value) throw new Error(`Missing required argument ${name}`);
  return path.resolve(value);
}

const workspaceRoot = required("--workspace-root", process.env.SMARTCORE_WORKSPACE_ROOT);
if (!workspaceRoot) throw new Error("Provide --workspace-root or SMARTCORE_WORKSPACE_ROOT");
const platformRoot = required("--platform-root", path.dirname(workspaceRoot));
const originalIdentityRoot = required("--original-identity-root", path.resolve(workspaceRoot, "../SmartCoreIdentity"));
const originalIotRoot = required("--original-iot-root", path.resolve(workspaceRoot, "../SmartCoreIOT"));
const unifiedRoot = required("--unified-root", path.resolve(root, "../"));
const unifiedIdentityRoot = required("--unified-identity-root", path.join(unifiedRoot, "SmartCoreIdentity"));
const unifiedConsoleRoot = required("--unified-console-root", root);
const legacyServiceBusinessRoot = required("--legacy-service-business-root", path.resolve(workspaceRoot, "../SmartCoreServiceBusiness"));
const output = required("--output", path.join(workspaceRoot, "SmartCorePlatform.corrected.code-workspace"));

const templatePath = path.join(root, "tools", "corrected-workspace.template.json");
let text = fs.readFileSync(templatePath, "utf8");
const replacements = {
  "{{platformRoot}}": relativeOutput(platformRoot, output),
  "{{workspaceRoot}}": relativeOutput(workspaceRoot, output),
  "{{originalIdentityRoot}}": relativeOutput(originalIdentityRoot, output),
  "{{originalIotRoot}}": relativeOutput(originalIotRoot, output),
  "{{unifiedIdentityRoot}}": relativeOutput(unifiedIdentityRoot, output),
  "{{unifiedConsoleRoot}}": relativeOutput(unifiedConsoleRoot, output),
  "{{legacyServiceBusinessRoot}}": relativeOutput(legacyServiceBusinessRoot, output),
};
for (const [placeholder, value] of Object.entries(replacements)) text = text.split(placeholder).join(value.replace(/\\/g, "/"));

const workspace = JSON.parse(text);
for (const folder of workspace.folders) {
  const resolved = path.resolve(path.dirname(output), folder.path);
  if (!fs.existsSync(resolved)) throw new Error(`Workspace root does not exist: ${resolved}`);
}
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, `${JSON.stringify(workspace, null, 2)}\n`, "utf8");
console.log(`Generated corrected workspace: ${output}`);

function relativeOutput(target, output) {
  return path.relative(path.dirname(output), target) || ".";
}
