import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve, join } from "node:path";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const apps = [
  { name: "console", root: join(root, "apps/console"), env: {} },
  {
    name: "identity",
    root: resolve(root, "../SmartCoreIdentity/web/identity"),
    env: {
      SMARTCORE_CONSOLE_ORIGIN: "http://127.0.0.1:4100",
      NEXT_PUBLIC_BFF_ACCOUNTS_ENABLED: "false",
      NEXT_PUBLIC_BFF_REGISTRATION_ENABLED: "false",
      NEXT_PUBLIC_BFF_RECOVERY_ENABLED: "false",
      NEXT_PUBLIC_PRIVATE_TEST_MODE: "false",
    },
  },
  {
    name: "business",
    root: resolve(root, "../SmartCoreServiceBusiness/frontend"),
    env: { NEXT_PUBLIC_SMARTCORE_CONSOLE_ORIGIN: "http://127.0.0.1:4100" },
  },
];
for (const app of apps) {
  console.log(`Building ${app.name} UI preview`);
  const child = spawn(
    process.execPath,
    [join(app.root, "node_modules/next/dist/bin/next"), "build", "--webpack"],
    { cwd: app.root, env: { ...process.env, ...app.env }, stdio: "inherit" },
  );
  const code = await new Promise((resolve, reject) => {
    child.on("error", reject);
    child.on("exit", resolve);
  });
  if (code !== 0) {
    process.exitCode = 1;
    break;
  }
}
