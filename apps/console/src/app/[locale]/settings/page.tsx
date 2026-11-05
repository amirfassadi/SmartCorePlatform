import Link from "next/link";
import { cookies } from "next/headers";
import { notFound } from "next/navigation";
import { isLocale, copy } from "@/lib/platform";
import { ThemeToggle } from "@/components/preferences";
export default async function Settings({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const t = copy[locale];
  const theme =
    (await cookies()).get("smartcore-theme")?.value === "dark"
      ? "dark"
      : "light";
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">{t.personal}</p>
          <h1>{t.settings}</h1>
          <p>
            {locale === "fa"
              ? "فضای کار را مطابق سلیقهٔ خود تنظیم کنید."
              : "Make the workspace feel like yours."}
          </p>
        </div>
      </div>
      <section className="settings-card">
        <div className="setting-row">
          <div>
            <h2>{t.theme}</h2>
            <p>
              {locale === "fa"
                ? "انتخاب شما در همین مرورگر حفظ می‌شود."
                : "Your choice is remembered in this browser."}
            </p>
          </div>
          <ThemeToggle locale={locale} initial={theme} expanded />
        </div>
        <div className="setting-row">
          <div>
            <h2>{t.language}</h2>
            <p>
              {locale === "fa"
                ? "فارسی با چیدمان راست‌به‌چپ یا انگلیسی."
                : "Persian with right-to-left layout, or English."}
            </p>
          </div>
          <div className="language-choices">
            <Link
              href="/fa/settings"
              aria-current={locale === "fa" ? "page" : undefined}
            >
              فارسی
            </Link>
            <Link
              href="/en/settings"
              aria-current={locale === "en" ? "page" : undefined}
            >
              English
            </Link>
          </div>
        </div>
        <p className="settings-note">
          {locale === "fa"
            ? "این تنظیمات فقط ظاهر فضای کار را تغییر می‌دهند. تنظیمات امنیت و حساب در ماژول هویت مدیریت می‌شوند."
            : "These preferences change the workspace appearance. Account and security settings belong to the Identity module."}
        </p>
      </section>
    </>
  );
}
