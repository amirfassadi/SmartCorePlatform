// Keep independently buildable repositories on the same versioned design foundation.
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { resolve, dirname, join } from "node:path";
import { createHash } from "node:crypto";
const platform = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const check = args.includes("--check");
const option = (name) => {
  const index = args.indexOf(name);
  return index < 0 ? undefined : args[index + 1];
};
const identity = option("--identity");
const business = option("--business");
const consoleRoot = join(platform, "apps/console");
const normalize = (buffer) =>
  Buffer.from(buffer.toString("utf8").replace(/\r\n/g, "\n"));
const foundation = normalize(
  await readFile(join(platform, "packages/design/smartcore.css")),
);
const hash = createHash("sha256").update(foundation).digest("hex");
const files = [
  ["arabic", "vazirmatn-arabic-400-normal.woff2"],
  ["latin", "vazirmatn-latin-400-normal.woff2"],
];
const roots = [{ root: consoleRoot, css: "src/app/smartcore.css" }];
if (identity) {
  await readFile(join(resolve(identity), "web/identity/package.json"));
  roots.push({
    root: join(resolve(identity), "web/identity"),
    css: "src/app/smartcore.css",
  });
}
if (business) {
  await readFile(join(resolve(business), "frontend/package.json"));
  roots.push({
    root: join(resolve(business), "frontend"),
    css: "app/smartcore.css",
  });
}
let failures = 0;
async function sync(target, content) {
  let current;
  try {
    current = await readFile(target);
  } catch {}
  if (!target.endsWith(".woff2")) {
    content = normalize(content);
    if (current) current = normalize(current);
  }
  if (current?.equals(content)) return;
  if (check) {
    console.error(`Design drift: ${target}`);
    failures++;
    return;
  }
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, content);
}
for (const item of roots) {
  await sync(join(item.root, item.css), foundation);
  for (const [subset, filename] of files)
    await sync(
      join(item.root, `public/fonts/vazirmatn-${subset}.woff2`),
      await readFile(
        join(consoleRoot, "node_modules/@fontsource/vazirmatn/files", filename),
      ),
    );
  await sync(
    join(item.root, "public/fonts/OFL.txt"),
    await readFile(
      join(consoleRoot, "node_modules/@fontsource/vazirmatn/LICENSE"),
    ),
  );
  await sync(
    join(item.root, "design-manifest.json"),
    Buffer.from(
      JSON.stringify(
        {
          source: "amirfassadi/SmartCorePlatform",
          path: "packages/design/smartcore.css",
          version: 1,
          sha256: hash,
          font: "Vazirmatn, SIL Open Font License 1.1",
        },
        null,
        2,
      ) + "\n",
    ),
  );
}
if (failures) process.exitCode = 1;
else
  console.log(
    `Shared design ${check ? "verified" : "synchronized"} across ${roots.length} app(s). SHA-256 ${hash}`,
  );
