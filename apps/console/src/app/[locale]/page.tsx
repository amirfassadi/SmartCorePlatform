import Link from "next/link";
import { notFound } from "next/navigation";
import { isLocale, moduleOrigin, modules, copy } from "@/lib/platform";
import { Icon } from "@/components/icon";
import { ModuleDirectory } from "@/components/module-directory";
export default async function Home({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const fa = locale === "fa";
  const t = copy[locale];
  const identity = moduleOrigin(modules[0]);
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">{fa ? "فضای کار شما" : "YOUR WORKSPACE"}</p>
          <h1>
            {fa ? "یک نگاه به اسمارت‌کور" : "Your SmartCore, at a glance"}
          </h1>
          <p>
            {fa
              ? "از حساب شخصی تا مدیریت کسب‌وکار؛ مسیرتان را از اینجا شروع کنید."
              : "From your personal account to business operations. Start here."}
          </p>
        </div>
        <Link className="button button-secondary" href={`/${locale}/modules`}>
          <Icon name="grid" />
          {t.modules}
        </Link>
      </div>
      <section className="welcome-card">
        <div className="welcome-copy">
          <span className="hero-label">
            <span />
            {fa ? "یکپارچه، از پایه" : "CONNECTED FROM THE CORE"}
          </span>
          <h2>
            {fa ? (
              <>
                همهٔ مسیرها،
                <br />
                یک فضای کار.
              </>
            ) : (
              <>
                Every capability.
                <br />
                One workspace.
              </>
            )}
          </h2>
          <p>
            {fa
              ? "اسمارت‌کور جایی است که هویت، کسب‌وکار و عملیات کنار هم قرار می‌گیرند. ساده شروع کنید و ماژول‌به‌ماژول پیش بروید."
              : "Bring identity, business and operations together. Start simply and grow one module at a time."}
          </p>
          <div className="hero-actions">
            {identity ? (
              <a
                className="button button-primary"
                href={`${identity}/${locale}`}
              >
                <Icon name="shield" />
                {fa ? "رفتن به حساب کاربری" : "Go to your account"}
                <Icon name="arrow" />
              </a>
            ) : (
              <Link
                className="button button-primary"
                href={`/${locale}/modules/identity`}
              >
                <Icon name="shield" />
                {fa ? "آشنایی با حساب کاربری" : "Explore your account"}
                <Icon name="arrow" />
              </Link>
            )}
            <Link className="hero-secondary" href={`/${locale}/modules`}>
              {fa ? "کاوش در ماژول‌ها" : "Explore the modules"}
            </Link>
          </div>
        </div>
        <div className="platform-art" aria-hidden="true">
          <div className="art-grid" />
          <div className="art-ring ring-outer" />
          <div className="art-ring ring-inner" />
          <div className="art-core">
            <span>S</span>
            <small>SMARTCORE</small>
          </div>
          <div className="art-chip chip-identity">
            <Icon name="shield" />
            <span>Identity</span>
            <i />
          </div>
          <div className="art-chip chip-business">
            <Icon name="building" />
            <span>Business</span>
            <i />
          </div>
          <div className="art-chip chip-operations">
            <Icon name="layers" />
            <span>Operations</span>
            <i />
          </div>
          <span className="art-spark spark-one" />
          <span className="art-spark spark-two" />
        </div>
      </section>
      <div className="overview-strip">
        <div>
          <span className="overview-icon">
            <Icon name="grid" />
          </span>
          <div>
            <strong>
              {new Intl.NumberFormat(locale).format(modules.length)}
            </strong>
            <small>
              {fa ? "ماژول در نقشهٔ پلتفرم" : "modules on the platform map"}
            </small>
          </div>
        </div>
        <div>
          <span className="overview-icon green">
            <Icon name="layers" />
          </span>
          <div>
            <strong>{fa ? "یک تجربهٔ مشترک" : "One shared experience"}</strong>
            <small>
              {fa
                ? "ظاهر، پیمایش و الگوهای یکسان"
                : "Consistent design, navigation and patterns"}
            </small>
          </div>
        </div>
        <div>
          <span className="overview-icon amber">
            <Icon name="shield" />
          </span>
          <div>
            <strong>{fa ? "مرزهای روشن" : "Clear boundaries"}</strong>
            <small>
              {fa
                ? "حساب و داده‌های هر ماژول، مستقل"
                : "Independent account and module boundaries"}
            </small>
          </div>
        </div>
      </div>
      <ModuleDirectory locale={locale} compact />
      <section className="continuation-card">
        <span className="overview-icon">
          <Icon name="arrow" />
        </span>
        <div>
          <h2>
            {fa
              ? "قدم بعدی: اتصال به سرویس‌های واقعی"
              : "Next: connect the real services"}
          </h2>
          <p>
            {fa
              ? "این صفحه نمای مشترک پلتفرم است. قابلیت‌های هر ماژول پس از اتصال و آزمون سرویس مربوط فعال می‌شوند."
              : "This is the shared platform workspace. Module capabilities become available after their services are connected and tested."}
          </p>
        </div>
        <Link href={`/${locale}/modules/identity`} className="text-link">
          {fa ? "شروع از هویت" : "Start with Identity"}
          <Icon name="arrow" />
        </Link>
      </section>
    </>
  );
}
