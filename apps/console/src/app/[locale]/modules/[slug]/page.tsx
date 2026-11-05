import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale, modules, moduleOrigin, copy } from "@/lib/platform";
import { Icon } from "@/components/icon";
export default async function ModulePage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  const module = modules.find((item) => item.id === slug);
  if (!module) notFound();
  const fa = locale === "fa";
  const t = copy[locale];
  const origin = moduleOrigin(module);
  return (
    <>
      <Link href={`/${locale}/modules`} className="back-link">
        <Icon name="arrow" />
        {t.back}
      </Link>
      <section className={`module-detail module-${module.id}`}>
        <span className="module-icon large">
          <Icon name={module.icon} />
        </span>
        <span className="eyebrow">{t[module.category]}</span>
        <h1>{module.name[locale]}</h1>
        <p className="detail-summary">{module.summary[locale]}</p>
        <span
          className={`status-badge ${module.readiness === "interface" ? "available" : ""}`}
        >
          <span />
          {t[module.readiness]}
        </span>
        <div className="detail-divider" />
        <h2>{fa ? "در این ماژول" : "Inside this module"}</h2>
        <ul className="capability-list">
          {module.capabilities.map((item) => (
            <li key={item.en}>
              <Icon name="layers" />
              {item[locale]}
            </li>
          ))}
        </ul>
        <div className="integration-note">
          <Icon name="shield" />
          <p>
            {origin
              ? fa
                ? "نشانی رابط این ماژول تنظیم شده است. بازشدن رابط به معنای اتصال حساب یا آماده‌بودن سرویس نیست؛ وضعیت ورود و داده‌ها در خود ماژول بررسی می‌شود."
                : "The interface URL is configured. Opening it does not establish authentication or service readiness; the module checks its own account and data state."
              : fa
                ? "این ماژول هنوز به فضای کار متصل نشده است. پس از آماده‌شدن و تأیید سرویس، امکان ورود از اینجا اضافه می‌شود."
                : "This module is not connected to the workspace yet. Its entry point will be enabled once the service is ready and verified."}
          </p>
        </div>
        {origin ? (
          <a className="button button-primary" href={`${origin}/${locale}`}>
            {t.launch} {module.name[locale]}
            <Icon name="external" />
          </a>
        ) : (
          <button className="button button-secondary" disabled>
            {fa
              ? "ورود پس از اتصال سرویس"
              : "Available after service integration"}
          </button>
        )}
      </section>
    </>
  );
}
