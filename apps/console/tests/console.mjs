// Production-browser checks. This launcher does not claim live module/API acceptance.
import assert from "node:assert/strict";
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
const origin =
  process.env.SMARTCORE_CONSOLE_TEST_URL ?? "http://127.0.0.1:4100";
const screenshots = process.env.SMARTCORE_SCREENSHOTS;
if (screenshots) await mkdir(screenshots, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  for (const locale of ["fa", "en"]) {
    const context = await browser.newContext({
      baseURL: origin,
      viewport: { width: 1440, height: 1100 },
    });
    const page = await context.newPage();
    const faults = [];
    page.on("pageerror", (error) => faults.push(error.message));
    await page.addInitScript(() => {
      window.__violations = [];
      document.addEventListener("securitypolicyviolation", (event) =>
        window.__violations.push(event.effectiveDirective),
      );
    });
    const response = await page.goto(`/${locale}`);
    assert.equal(response.status(), 200);
    assert.equal(
      await page.locator("html").getAttribute("dir"),
      locale === "fa" ? "rtl" : "ltr",
    );
    await page.locator(".module-card").first().waitFor();
    assert.equal(await page.locator(".module-card").count(), 8);
    await page.evaluate(() => document.fonts.ready);
    assert(
      await page.evaluate(() => document.fonts.check("14px SmartCore")),
      "Self-hosted font loads",
    );
    const nonce = response
      .headers()
      ["content-security-policy"].match(/'nonce-([^']+)'/)[1];
    for (const script of await page
      .locator("script[src]")
      .evaluateAll((nodes) => nodes.map((node) => node.nonce)))
      assert.equal(script, nonce);
    if (screenshots)
      await page.screenshot({
        path: `${screenshots}/console-${locale}.png`,
        fullPage: true,
      });
    await page.locator("input[type=search]").fill("identity");
    assert.equal(await page.locator(".module-card").count(), 1);
    await page.locator("input[type=search]").fill("not-a-module");
    await page.getByRole("status").last().waitFor();
    assert.equal(await page.locator(".module-card").count(), 0);
    await page.locator("input[type=search]").fill("");
    await page.locator(".module-identity .favorite-button").click();
    await page.goto(`/${locale}/modules`);
    await page
      .getByRole("button", {
        name: locale === "fa" ? "علاقه‌مندی‌ها" : "Favorites",
        exact: true,
      })
      .click();
    assert.equal(await page.locator(".module-card").count(), 1);
    await page.reload();
    await page
      .getByRole("button", {
        name: locale === "fa" ? "علاقه‌مندی‌ها" : "Favorites",
        exact: true,
      })
      .click();
    assert.equal(await page.locator(".module-card").count(), 1);
    await page.goto(`/${locale}/modules/identity`);
    const entry = page.locator(".module-detail a.button");
    assert.equal(
      new URL(await entry.getAttribute("href")).pathname,
      `/${locale}`,
    );
    assert.equal(new URL(await entry.getAttribute("href")).port, "4101");
    await page.goto(`/${locale}/modules/inventory`);
    assert.equal(
      await page.locator(".module-detail button:disabled").count(),
      1,
    );
    assert.equal(
      (await page.goto(`/${locale}/modules/not-a-module`)).status(),
      404,
    );
    assert.equal((await page.request.post("/bff/login")).status(), 404);
    await page.goto(`/${locale}/settings`);
    await page.locator(".theme-option").click();
    assert.equal(await page.locator("html").getAttribute("data-theme"), "dark");
    await page.reload();
    assert.equal(await page.locator("html").getAttribute("data-theme"), "dark");
    await page
      .getByRole("link", {
        name: locale === "fa" ? "English" : "فارسی",
        exact: true,
      })
      .click();
    await page.waitForURL(`/${locale === "fa" ? "en" : "fa"}/settings`);
    await page.waitForFunction(
      (expected) => document.documentElement.lang === expected,
      locale === "fa" ? "en" : "fa",
    );
    assert.equal(
      await page.locator("html").getAttribute("lang"),
      locale === "fa" ? "en" : "fa",
    );
    await page.goto(`/${locale}`);
    if (screenshots)
      await page.screenshot({
        path: `${screenshots}/console-dark-${locale}.png`,
        fullPage: true,
      });
    await page
      .getByRole("button", {
        name: new RegExp(
          locale === "fa" ? "ظاهر فضای کار" : "Workspace appearance",
        ),
      })
      .click();
    for (const width of [390, 320]) {
      await page.setViewportSize({ width, height: 844 });
      assert(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
        `${locale}/${width} overflow`,
      );
      const menu = page.getByRole("button", {
        name: locale === "fa" ? "باز کردن منو" : "Open navigation",
      });
      await menu.click();
      assert.equal(await page.locator(".sidebar").isVisible(), true);
      await page.keyboard.press("Escape");
      assert.equal(await menu.getAttribute("aria-expanded"), "false");
      await menu.click();
      await page.locator(".sidebar nav a").nth(1).click();
      await page.waitForURL(`/${locale}/modules`);
      await page.locator(".sidebar").waitFor({ state: "hidden" });
      await page.goto(`/${locale}`);
      if (screenshots && width === 390)
        await page.screenshot({
          path: `${screenshots}/console-mobile-${locale}.png`,
          fullPage: true,
        });
    }
    assert.deepEqual(faults, [], "No browser runtime errors");
    assert.deepEqual(
      await page.evaluate(() => window.__violations),
      [],
      "Production CSP",
    );
    await context.close();
  }
  console.log(
    "PASS: fa/en direction, 8 modules, search, persisted favorites, configured launch URL, unavailable modules, 404 boundaries, dark-theme persistence, language navigation, 320/390px menu and layout, self-hosted fonts, nonce CSP, no runtime errors.",
  );
} finally {
  await browser.close();
}
