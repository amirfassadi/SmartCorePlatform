// Default launch is Console + Identity. Legacy Business preview is opt-in.
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve, join } from "node:path";
import { existsSync } from "node:fs";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const apps = [
  {
    name: "console",
    root: join(root, "apps/console"),
    port: 4100,
    env: {
      SMARTCORE_IDENTITY_ORIGIN: "http://127.0.0.1:4101",
    },
  },
  {
    name: "identity",
    root: resolve(root, "../SmartCoreIdentity/web/identity"),
    port: 4101,
    env: { SMARTCORE_CONSOLE_ORIGIN: "http://127.0.0.1:4100" },
  },
];
if (process.argv.includes("--legacy-business-preview")) {
  apps.push({
    name: "business",
    root: resolve(root, "../SmartCoreServiceBusiness/frontend"),
    port: 4102,
    env: { NEXT_PUBLIC_SMARTCORE_CONSOLE_ORIGIN: "http://127.0.0.1:4100" },
  });
}
for (const app of apps)
  if (!existsSync(join(app.root, ".next/BUILD_ID")))
    throw Error(`Build ${app.name} first: ${app.root}`);
const children = [];
let stopping = false;
function stop() {
  if (stopping) return;
  stopping = true;
  for (const child of children) child.kill();
}
for (const app of apps) {
  const child = spawn(
    process.execPath,
    [
      join(app.root, "node_modules/next/dist/bin/next"),
      "start",
      "--hostname",
      "127.0.0.1",
      "--port",
      String(app.port),
    ],
    { cwd: app.root, env: { ...process.env, ...app.env }, stdio: "inherit" },
  );
  children.push(child);
  child.on("error", (error) => {
    console.error(app.name, error.message);
    process.exitCode = 1;
    stop();
  });
  child.on("exit", (code) => {
    if (!stopping) {
      process.exitCode = code ?? 1;
      stop();
    }
  });
}
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, stop);
console.log(
  "SmartCore: http://127.0.0.1:4100/fa · Identity :4101",
);
if (process.argv.includes("--legacy-business-preview")) {
  console.log("Legacy/reference Business preview: http://127.0.0.1:4102 (not a canonical Business link)");
}
console.log(
  "UI preview only. Real account journeys require the existing private Identity stack.",
);
