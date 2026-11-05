# SmartCore design context

Curated source snapshot. No runtime credentials, environments or customer data.

This is an implemented modular-platform UI, not a KimiaBeauty website.

Canonical tokens are in Platform/packages/design/smartcore.css; copies in apps are generated.

The console is public navigation. Real authentication and organization-scoped permissions are separate.

SmartCoreServiceBusiness content is legacy visual/reference material only; it is not the canonical Business owner or API.

SmartCoreBusiness is the foundation owner; SmartCoreBusinessCapability owns Service and other capability semantics.

The domain slice is in-memory only. No SQL migration, HTTP API, production authorization or Money implementation is approved.

SmartCoreServiceBusiness and legacy Business UI code may inform visual reuse only.


## Platform: packages/design/smartcore.css

```css
/* SmartCore design foundation v1. Canonical source: SmartCorePlatform/packages/design. */
@font-face{font-family:SmartCore;src:url('/fonts/vazirmatn-arabic.woff2') format('woff2');font-style:normal;font-weight:400;font-display:swap;unicode-range:U+0600-06FF,U+0750-077F,U+08A0-08FF,U+200C-200E,U+FB50-FDFF,U+FE70-FEFF;}
@font-face{font-family:SmartCore;src:url('/fonts/vazirmatn-latin.woff2') format('woff2');font-style:normal;font-weight:400;font-display:swap;}
:root{color-scheme:light;--sc-bg:#f7f8fc;--sc-surface:#fff;--sc-soft:#f1f3fa;--sc-text:#17243d;--sc-muted:#6c7890;--sc-border:#e5e9f2;--sc-primary:#6259e8;--sc-primary-hover:#5046cf;--sc-primary-soft:#eeecff;--sc-positive:#187b62;--sc-positive-soft:#e8f6ef;--sc-warning:#9b6520;--sc-warning-soft:#fff5e2;--sc-radius:16px;--sc-font:SmartCore,Tahoma,Arial,sans-serif;--sc-shadow:0 6px 26px #23365305;}
:root[data-theme=dark]{color-scheme:dark;--sc-bg:#101626;--sc-surface:#182033;--sc-soft:#212b40;--sc-text:#edf1fc;--sc-muted:#a1aec8;--sc-border:#2d3850;--sc-primary:#a29aff;--sc-primary-hover:#b7b0ff;--sc-primary-soft:#302b54;--sc-positive:#7ed5b5;--sc-positive-soft:#193c34;--sc-warning:#e3bd7b;--sc-warning-soft:#3d321f;--sc-shadow:none;}

```


## Platform: apps/console/src/lib/platform.ts

```ts
export type Locale = "fa" | "en";
export type Label = Record<Locale, string>;
export const label = (fa: string, en: string): Label => ({ fa, en });
export const isLocale = (value: string): value is Locale =>
  value === "fa" || value === "en";
export type Module = {
  id: string;
  name: Label;
  summary: Label;
  category: "foundation" | "business" | "operations";
  icon: string;
  readiness: "interface" | "planned";
  capabilities: Label[];
  originKey?: "SMARTCORE_IDENTITY_ORIGIN" | "SMARTCORE_BUSINESS_ORIGIN";
};
export const modules: Module[] = [
  {
    id: "identity",
    name: label("هویت و حساب", "Identity & account"),
    summary: label(
      "ورود، ثبت‌نام، بازیابی و امنیت حساب در یک مسیر مشترک.",
      "A shared journey for sign-in, registration, recovery and account security.",
    ),
    category: "foundation",
    icon: "shield",
    readiness: "interface",
    originKey: "SMARTCORE_IDENTITY_ORIGIN",
    capabilities: [
      label("ورود و ثبت‌نام", "Sign-in & registration"),
      label("بازیابی حساب", "Account recovery"),
      label("امنیت و نشست‌ها", "Security & sessions"),
    ],
  },
  {
    id: "business-foundation",
    name: label("بنیان کسب‌وکار", "Business foundation"),
    summary: label(
      "پروفایل محلی‌سازی‌شده، دسته‌بندی و فعال‌سازی صریح قابلیت‌های کسب‌وکار.",
      "Localized profiles, classification and explicit capability activation for a Business.",
    ),
    category: "business",
    icon: "building",
    readiness: "planned",
    capabilities: [
      label("پروفایل کسب‌وکار", "Business profile"),
      label("زبان‌های پیش‌فرض و ترجمه", "Default locale and translations"),
      label("فعالسازی قابلیت‌ها", "Capability activation"),
    ],
  },
  {
    id: "business-capability",
    name: label("قابلیت‌های کسب‌وکار", "Business capabilities"),
    summary: label(
      "ترکیب قابلیت‌های مالکیت‌شده، مانند سرویس و بازرگانی، برای هر کسب‌وکار.",
      "Compose owned capabilities, such as Service and future Commerce, for each Business.",
    ),
    category: "business",
    icon: "layers",
    readiness: "planned",
    capabilities: [
      label("کاتالوگ سرویس و ترجمه", "Service catalog and translations"),
      label("مدیریت حالت فعالیت", "Scoped activation state"),
      label("گسترش آینده بدون پیوند اجباری", "Independent future composition"),
    ],
  },
  {
    id: "reservation",
    name: label("رزرو و نوبت‌دهی", "Reservations"),
    summary: label(
      "مسیر مشترک رزرو خدمات و مدیریت نوبت‌ها.",
      "A consistent home for service bookings and appointments.",
    ),
    category: "business",
    icon: "calendar",
    readiness: "planned",
    capabilities: [
      label("رزرو خدمات", "Service bookings"),
      label("مدیریت نوبت‌ها", "Appointments"),
    ],
  },
  {
    id: "scheduling",
    name: label("زمان‌بندی", "Scheduling"),
    summary: label(
      "تعریف زمان‌های کاری و ظرفیت در دسترس.",
      "Coordinate working hours and available capacity.",
    ),
    category: "operations",
    icon: "clock",
    readiness: "planned",
    capabilities: [
      label("ساعات کاری", "Working hours"),
      label("ظرفیت و دسترس‌پذیری", "Capacity & availability"),
    ],
  },
  {
    id: "inventory",
    name: label("موجودی و منابع", "Inventory & resources"),
    summary: label(
      "فضای مدیریت اقلام، موجودی و منابع عملیاتی.",
      "A workspace for items, inventory and operational resources.",
    ),
    category: "operations",
    icon: "box",
    readiness: "planned",
    capabilities: [
      label("اقلام و موجودی", "Items & inventory"),
      label("منابع عملیاتی", "Operational resources"),
    ],
  },
  {
    id: "communication",
    name: label("ارتباطات", "Communications"),
    summary: label(
      "یک جای مشخص برای مسیرهای ارتباطی پلتفرم.",
      "One place for the platform’s communication capabilities.",
    ),
    category: "foundation",
    icon: "mail",
    readiness: "planned",
    capabilities: [
      label("کانال‌های ارتباطی", "Communication channels"),
      label("تنظیمات ارسال", "Delivery configuration"),
    ],
  },
  {
    id: "talk",
    name: label("گفت‌وگو", "Talk"),
    summary: label(
      "گفت‌وگوهای مرتبط با فضای کار و کسب‌وکار.",
      "Conversations connected to workspaces and businesses.",
    ),
    category: "business",
    icon: "chat",
    readiness: "planned",
    capabilities: [
      label("گفت‌وگوها", "Conversations"),
      label("فضای کار مشترک", "Shared workspace"),
    ],
  },
  {
    id: "iot",
    name: label("دستگاه‌ها و IoT", "Devices & IoT"),
    summary: label(
      "مسیر اتصال دنیای فیزیکی به فضای کار دیجیتال.",
      "Connect physical devices to the digital workspace.",
    ),
    category: "operations",
    icon: "cpu",
    readiness: "planned",
    capabilities: [
      label("دستگاه‌ها", "Devices"),
      label("رویدادهای دستگاه", "Device events"),
    ],
  },
];
export function moduleOrigin(module: Module): string | undefined {
  const value = module.originKey
    ? process.env[module.originKey]?.trim()
    : undefined;
  if (!value) return;
  try {
    const url = new URL(value);
    const local = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
    if (url.protocol !== "https:" && !(url.protocol === "http:" && local))
      return;
    if (
      url.username ||
      url.password ||
      url.pathname !== "/" ||
      url.search ||
      url.hash
    )
      return;
    return url.origin;
  } catch {
    return;
  }
}
export const copy = {
  fa: {
    home: "نمای کلی",
    modules: "همهٔ ماژول‌ها",
    settings: "تنظیمات",
    workspace: "فضای کار پلتفرم",
    platform: "پلتفرم اسمارت‌کور",
    navigation: "منوی اصلی",
    development: "پیش‌نمایش توسعه",
    search: "جست‌وجوی ماژول‌ها…",
    all: "همه",
    foundation: "زیرساخت",
    business: "کسب‌وکار",
    operations: "عملیات",
    interface: "رابط موجود",
    planned: "در انتظار اتصال",
    details: "مشاهدهٔ ماژول",
    launch: "باز کردن",
    back: "بازگشت به ماژول‌ها",
    empty: "ماژولی با این عبارت پیدا نشد.",
    theme: "ظاهر فضای کار",
    light: "روشن",
    dark: "تیره",
    language: "زبان رابط کاربری",
    personal: "تنظیمات این مرورگر",
    openMenu: "باز کردن منو",
    closeMenu: "بستن منو",
    skip: "رفتن به محتوای اصلی",
    favorite: "افزودن به علاقه‌مندی‌ها",
    unfavorite: "حذف از علاقه‌مندی‌ها",
    favorites: "علاقه‌مندی‌ها",
  },
  en: {
    home: "Overview",
    modules: "All modules",
    settings: "Settings",
    workspace: "Platform workspace",
    platform: "SmartCore Platform",
    navigation: "Main navigation",
    development: "Development preview",
    search: "Search modules…",
    all: "All",
    foundation: "Foundation",
    business: "Business",
    operations: "Operations",
    interface: "Interface available",
    planned: "Awaiting integration",
    details: "View module",
    launch: "Open",
    back: "Back to modules",
    empty: "No modules match your search.",
    theme: "Workspace appearance",
    light: "Light",
    dark: "Dark",
    language: "Interface language",
    personal: "This browser’s preferences",
    openMenu: "Open navigation",
    closeMenu: "Close navigation",
    skip: "Skip to main content",
    favorite: "Add to favorites",
    unfavorite: "Remove from favorites",
    favorites: "Favorites",
  },
};

```


## Platform: apps/console/src/components/shell.tsx

```tsx
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect, useRef } from "react";
import { copy, type Locale } from "@/lib/platform";
import { Icon } from "./icon";
import { ThemeToggle } from "./preferences";
export function Shell({
  locale,
  theme,
  children,
}: {
  locale: Locale;
  theme: string;
  children: React.ReactNode;
}) {
  const t = copy[locale];
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!open) return;
    const key = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        menuButton.current?.focus();
      }
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [open]);
  const items = [
    { path: `/${locale}`, name: t.home, icon: "home" },
    { path: `/${locale}/modules`, name: t.modules, icon: "grid" },
    { path: `/${locale}/settings`, name: t.settings, icon: "settings" },
  ];
  const other = locale === "fa" ? "en" : "fa";
  const languagePath = pathname.replace(/^\/(fa|en)(?=\/|$)/, `/${other}`);
  const title = pathname.includes("/modules")
    ? t.modules
    : pathname.endsWith("/settings")
      ? t.settings
      : t.home;
  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-link">
        {t.skip}
      </a>
      <aside
        className={`sidebar ${open ? "is-open" : ""}`}
        id="platform-navigation"
      >
        <Link
          className="brand"
          href={`/${locale}`}
          onClick={() => setOpen(false)}
        >
          <span className="brand-mark">
            S<span />
          </span>
          <span>
            SmartCore
            <small>
              {locale === "fa"
                ? "یک پلتفرم، امکان‌های بیشتر"
                : "ONE PLATFORM. MORE POSSIBILITIES."}
            </small>
          </span>
        </Link>
        <div className="workspace-label">
          <span className="workspace-symbol">
            <Icon name="layers" />
          </span>
          <div>
            <strong>{t.platform}</strong>
            <small>{t.workspace}</small>
          </div>
          <span className="tiny-dot" />
        </div>
        <p className="nav-caption">
          {locale === "fa" ? "فضای اصلی" : "WORKSPACE"}
        </p>
        <nav aria-label={t.navigation}>
          {items.map((item) => (
            <Link
              key={item.path}
              href={item.path}
              onClick={() => setOpen(false)}
              className={`nav-item ${(item.path === `/${locale}` ? pathname === item.path : pathname.startsWith(item.path)) ? "is-active" : ""}`}
              aria-current={
                (
                  item.path === `/${locale}`
                    ? pathname === item.path
                    : pathname.startsWith(item.path)
                )
                  ? "page"
                  : undefined
              }
            >
              <Icon name={item.icon} />
              <span>{item.name}</span>
              {item.icon === "grid" ? <small>8</small> : null}
            </Link>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <Icon name="shield" />
            <strong>
              {locale === "fa" ? "ساخته‌شده برای رشد" : "Room to grow"}
            </strong>
            <p>
              {locale === "fa"
                ? "ماژول‌های مستقل. یک تجربهٔ یکپارچه."
                : "Independent modules. One consistent experience."}
            </p>
          </div>
          <div className="sidebar-footer">
            <span className="brand-mini">S</span>
            <div>
              <strong>SmartCore</strong>
              <small>Platform · 0.1</small>
            </div>
          </div>
        </div>
      </aside>
      {open ? (
        <button
          className="sidebar-backdrop"
          aria-label={t.closeMenu}
          onClick={() => setOpen(false)}
        />
      ) : null}
      <div className="app-body">
        <header className="topbar">
          <div className="breadcrumb">
            <button
              ref={menuButton}
              className="icon-button mobile-menu"
              aria-label={open ? t.closeMenu : t.openMenu}
              aria-expanded={open}
              aria-controls="platform-navigation"
              onClick={() => setOpen(!open)}
            >
              <Icon name={open ? "close" : "menu"} />
            </button>
            <span>SmartCore</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{title}</strong>
          </div>
          <div className="topbar-actions">
            <span className="environment-badge">
              <span />
              {t.development}
            </span>
            <ThemeToggle locale={locale} initial={theme} />
            <Link className="language-button" href={languagePath} lang={other}>
              {other === "en" ? "EN" : "فا"}
            </Link>
          </div>
        </header>
        <main id="main-content" className="main-content" tabIndex={-1}>
          {children}
        </main>
        <footer className="app-footer">
          <span>{t.platform}</span>
          <span>
            {locale === "fa"
              ? "یکپارچه در ظاهر، مستقل در قابلیت‌ها"
              : "Consistent by design. Modular by nature."}
          </span>
        </footer>
      </div>
    </div>
  );
}

```


## Platform: apps/console/src/components/module-directory.tsx

```tsx
"use client";
import Link from "next/link";
import { useState, useSyncExternalStore } from "react";
import { modules, copy, type Locale } from "@/lib/platform";
import { Icon } from "./icon";
const storageKey = "smartcore:favorites:v1";
const emptySnapshot = "[]";
function subscribe(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener("smartcore-favorites", callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener("smartcore-favorites", callback);
  };
}
function snapshot() {
  try {
    return localStorage.getItem(storageKey) ?? emptySnapshot;
  } catch {
    return emptySnapshot;
  }
}
function parse(value: string): string[] {
  try {
    const ids: unknown = JSON.parse(value);
    return Array.isArray(ids)
      ? ids.filter(
          (id): id is string =>
            typeof id === "string" &&
            modules.some((module) => module.id === id),
        )
      : [];
  } catch {
    return [];
  }
}
export function ModuleDirectory({
  locale,
  compact = false,
}: {
  locale: Locale;
  compact?: boolean;
}) {
  const t = copy[locale];
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const stored = useSyncExternalStore(subscribe, snapshot, () => emptySnapshot);
  const favorites = parse(stored);
  const [storageError, setStorageError] = useState(false);
  const visible = modules.filter(
    (module) =>
      (category === "all" ||
        (category === "favorites"
          ? favorites.includes(module.id)
          : module.category === category)) &&
      `${module.name.fa} ${module.name.en} ${module.summary[locale]}`
        .toLocaleLowerCase()
        .includes(query.trim().toLocaleLowerCase()),
  );
  function favorite(id: string) {
    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify(
          favorites.includes(id)
            ? favorites.filter((item) => item !== id)
            : [...favorites, id],
        ),
      );
      window.dispatchEvent(new Event("smartcore-favorites"));
      setStorageError(false);
    } catch {
      setStorageError(true);
    }
  }
  return (
    <section className="directory" aria-label={t.modules}>
      <div className="section-heading">
        <div>
          <h2>{t.modules}</h2>
          <p>
            {locale === "fa"
              ? "هر قابلیت، جای خودش؛ همه در یک فضای کار."
              : "Every capability in its place. Everything in one workspace."}
          </p>
        </div>
        <span className="count-label">
          {new Intl.NumberFormat(locale).format(modules.length)}{" "}
          {locale === "fa" ? "ماژول" : "modules"}
        </span>
      </div>
      <div className="directory-tools">
        <div
          className="filter-tabs"
          role="group"
          aria-label={
            locale === "fa" ? "دسته‌بندی ماژول‌ها" : "Module category"
          }
        >
          {(
            [
              "all",
              "foundation",
              "business",
              "operations",
              ...(compact ? [] : ["favorites"]),
            ] as const
          ).map((id) => (
            <button
              key={id}
              type="button"
              aria-pressed={category === id}
              className={category === id ? "selected" : ""}
              onClick={() => setCategory(id)}
            >
              {t[id as keyof typeof t]}
            </button>
          ))}
        </div>
        <label className="search-field">
          <Icon name="search" />
          <span className="sr-only">{t.search}</span>
          <input
            type="search"
            placeholder={t.search}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
      </div>
      {storageError ? (
        <p role="alert">
          {locale === "fa"
            ? "مرورگر امکان ذخیرهٔ علاقه‌مندی‌ها را نمی‌دهد."
            : "This browser could not save favorites."}
        </p>
      ) : null}
      <div className="module-grid">
        {visible.map((module) => (
          <article
            className={`module-card module-${module.id}`}
            key={module.id}
          >
            <div className="module-card-top">
              <span className="module-icon">
                <Icon name={module.icon} />
              </span>
              <button
                type="button"
                className={`favorite-button ${favorites.includes(module.id) ? "is-favorite" : ""}`}
                aria-label={`${favorites.includes(module.id) ? t.unfavorite : t.favorite}: ${module.name[locale]}`}
                aria-pressed={favorites.includes(module.id)}
                onClick={() => favorite(module.id)}
              >
                <Icon name="star" />
              </button>
            </div>
            <h3>
              <Link href={`/${locale}/modules/${module.id}`}>
                {module.name[locale]}
              </Link>
            </h3>
            <p>{module.summary[locale]}</p>
            <div className="module-card-footer">
              <span
                className={`status-badge ${module.readiness === "interface" ? "available" : ""}`}
              >
                <span />
                {t[module.readiness]}
              </span>
              <Link
                className="module-link"
                href={`/${locale}/modules/${module.id}`}
                aria-label={`${t.details}: ${module.name[locale]}`}
              >
                <Icon name="arrow" />
              </Link>
            </div>
          </article>
        ))}
      </div>
      {visible.length === 0 ? (
        <p className="empty-results" role="status">
          {t.empty}
        </p>
      ) : (
        <span className="sr-only" role="status">
          {visible.length} {locale === "fa" ? "نتیجه" : "results"}
        </span>
      )}
    </section>
  );
}

```


## Platform: apps/console/src/components/preferences.tsx

```tsx
"use client";
import { useSyncExternalStore } from "react";
import { copy, type Locale } from "@/lib/platform";
import { Icon } from "./icon";
function subscribe(callback: () => void) {
  window.addEventListener("smartcore-theme", callback);
  return () => window.removeEventListener("smartcore-theme", callback);
}
export function ThemeToggle({
  locale,
  initial,
  expanded = false,
}: {
  locale: Locale;
  initial: string;
  expanded?: boolean;
}) {
  const theme = useSyncExternalStore(
    subscribe,
    () => document.documentElement.dataset.theme ?? initial,
    () => initial,
  );
  const next = theme === "dark" ? "light" : "dark";
  function toggle() {
    document.documentElement.dataset.theme = next;
    document.cookie = `smartcore-theme=${next}; Path=/; Max-Age=31536000; SameSite=Lax${location.protocol === "https:" ? "; Secure" : ""}`;
    window.dispatchEvent(new Event("smartcore-theme"));
  }
  return (
    <button
      type="button"
      className={expanded ? "theme-option" : "icon-button"}
      onClick={toggle}
      aria-label={`${copy[locale].theme}: ${copy[locale][next]}`}
    >
      <Icon name={next === "dark" ? "moon" : "sun"} />
      {expanded ? (
        <span>{copy[locale][theme === "dark" ? "dark" : "light"]}</span>
      ) : null}
    </button>
  );
}

```


## Platform: apps/console/src/app/[locale]/page.tsx

```tsx
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

```


## Platform: apps/console/src/app/globals.css

```css
@import "./smartcore.css";
* {
  box-sizing: border-box;
}
body {
  margin: 0;
  font-family: var(--sc-font);
  background: var(--sc-bg);
  color: var(--sc-text);
  font-size: 14px;
  line-height: 1.8;
}
button,
input {
  font: inherit;
}
button,
a {
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
button {
  cursor: pointer;
}
button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}
a {
  color: inherit;
  text-decoration: none;
}
button:focus-visible,
a:focus-visible,
input:focus-visible,
[tabindex]:focus-visible {
  outline: 3px solid var(--sc-primary);
  outline-offset: 4px;
}
h1,
h2,
h3,
p {
  margin: 0;
}
h1,
h2,
h3 {
  font-weight: 600;
}
button {
  color: inherit;
}
.icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}
.skip-link {
  position: fixed;
  inset-block-start: -100px;
  inset-inline-start: 20px;
  z-index: 100;
  background: var(--sc-surface);
  padding: 12px 22px;
}
.skip-link:focus {
  inset-block-start: 12px;
}
.app-shell {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  position: fixed;
  inset-block: 0;
  inset-inline-start: 0;
  z-index: 30;
  width: 256px;
  background: var(--sc-surface);
  border-inline-end: 1px solid var(--sc-border);
  padding: 30px 22px 0;
  display: flex;
  flex-direction: column;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  direction: ltr;
  justify-content: center;
  color: var(--sc-text);
  font:
    600 24px/1.4 Arial,
    sans-serif;
  letter-spacing: -0.6px;
}
.brand small {
  display: block;
  font: 9px/2.2 var(--sc-font);
  letter-spacing: 0;
  color: var(--sc-muted);
  text-align: start;
}
.brand-mark {
  width: 43px;
  height: 43px;
  border-radius: 13px;
  background: var(--sc-primary);
  color: #fff;
  display: grid;
  place-items: center;
  position: relative;
  font: 700 28px/1 Arial;
  box-shadow: 0 5px 12px #6259e824;
}
.brand-mark > span {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 2px;
  background: #c8c3ff;
  right: 7px;
  top: 7px;
}
.workspace-label {
  display: flex;
  gap: 10px;
  align-items: center;
  border: 1px solid var(--sc-border);
  border-radius: 12px;
  padding: 12px 10px;
  margin: 32px 0 28px;
}
.workspace-label strong {
  display: block;
  font-size: 11px;
}
.workspace-label small {
  display: block;
  font-size: 10px;
  color: var(--sc-muted);
}
.workspace-symbol {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: var(--sc-soft);
  display: grid;
  place-items: center;
}
.workspace-symbol .icon {
  width: 17px;
}
.tiny-dot {
  margin-inline-start: auto;
  width: 6px;
  height: 6px;
  background: #aeb8ca;
  border-radius: 50%;
}
.nav-caption {
  font-size: 10px;
  color: var(--sc-muted);
  padding: 0 12px;
  margin-bottom: 12px;
  letter-spacing: 0.06em;
}
.sidebar nav {
  display: grid;
  gap: 6px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 13px;
  border-radius: 9px;
  font-size: 12px;
  color: var(--sc-muted);
  transition:
    background 0.15s,
    color 0.15s;
}
.nav-item.is-active {
  color: var(--sc-primary);
  background: var(--sc-primary-soft);
  font-weight: 600;
}
.nav-item:hover {
  background: var(--sc-soft);
  color: var(--sc-text);
}
.nav-item small {
  margin-inline-start: auto;
  font: 11px Arial;
  min-width: 20px;
  text-align: center;
  border: 1px solid var(--sc-border);
  border-radius: 5px;
}
.nav-item .icon {
  width: 18px;
  height: 18px;
}
.sidebar-bottom {
  margin-top: auto;
  padding-top: 40px;
}
.sidebar-note {
  background: var(--sc-soft);
  border: 1px solid var(--sc-border);
  border-radius: 12px;
  padding: 16px;
  position: relative;
}
.sidebar-note > .icon {
  color: var(--sc-primary);
  margin-bottom: 6px;
}
.sidebar-note strong {
  display: block;
  font-size: 11px;
}
.sidebar-note p {
  font-size: 10px;
  color: var(--sc-muted);
  margin-top: 5px;
  line-height: 1.9;
}
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  border-top: 1px solid var(--sc-border);
  margin-top: 22px;
  padding: 20px 0;
}
.brand-mini {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--sc-primary-soft);
  color: var(--sc-primary);
  font: 600 16px Arial;
}
.sidebar-footer strong {
  display: block;
  font: 600 11px Arial;
}
.sidebar-footer small {
  font: 10px Arial;
  color: var(--sc-muted);
}
.app-body {
  margin-inline-start: 256px;
  min-width: 0;
  flex: 1;
}
.topbar {
  height: 80px;
  padding: 0 38px;
  border-bottom: 1px solid var(--sc-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  background: var(--sc-surface);
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 11px;
  color: var(--sc-muted);
}
.breadcrumb strong {
  font-weight: 400;
  color: var(--sc-text);
}
.breadcrumb-separator {
  color: #c4cbda;
}
.topbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.environment-badge {
  display: flex;
  gap: 7px;
  align-items: center;
  color: var(--sc-muted);
  font-size: 10px;
  margin-inline-end: 10px;
}
.environment-badge > span {
  width: 6px;
  height: 6px;
  background: #d6a859;
  border-radius: 50%;
}
.icon-button {
  width: 34px;
  height: 34px;
  border: 1px solid var(--sc-border);
  background: var(--sc-surface);
  border-radius: 8px;
  display: grid;
  place-items: center;
}
.icon-button .icon {
  width: 16px;
  height: 16px;
}
.language-button {
  display: grid;
  place-items: center;
  border: 1px solid var(--sc-border);
  border-radius: 8px;
  width: 34px;
  height: 34px;
  font-size: 11px;
}
.main-content {
  max-width: 1510px;
  margin: auto;
  padding: 38px 38px 25px;
  min-height: calc(100vh - 145px);
}
.page-intro {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: center;
  margin-bottom: 28px;
}
.eyebrow {
  font-size: 10px;
  color: var(--sc-muted);
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}
.page-intro h1 {
  font-size: 25px;
  letter-spacing: -0.6px;
}
.page-intro p:last-child {
  font-size: 11px;
  color: var(--sc-muted);
  margin-top: 7px;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 42px;
  padding: 10px 17px;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}
.button .icon {
  width: 16px;
  height: 16px;
}
.button-primary {
  background: var(--sc-primary);
  border: 1px solid var(--sc-primary);
  color: #fff;
}
.button-primary:hover {
  background: var(--sc-primary-hover);
}
.button-secondary {
  background: var(--sc-surface);
  border: 1px solid var(--sc-border);
  color: var(--sc-text);
  box-shadow: var(--sc-shadow);
}
.welcome-card {
  border-radius: 20px;
  background: #eeeefe;
  border: 1px solid #e5e3fc;
  min-height: 310px;
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  overflow: hidden;
  position: relative;
}
.welcome-copy {
  padding: 34px 34px 32px;
  position: relative;
  z-index: 1;
}
.hero-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #665cb0;
}
.hero-label > span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #8377ed;
}
.welcome-copy h2 {
  font-size: 35px;
  line-height: 1.65;
  color: #29254f;
  letter-spacing: -0.8px;
  margin: 13px 0 12px;
}
.welcome-copy > p {
  max-width: 400px;
  font-size: 11px;
  line-height: 2.1;
  color: #72708e;
}
.hero-actions {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-top: 23px;
}
.hero-secondary {
  font-size: 10px;
  color: #665ba9;
}
.platform-art {
  position: relative;
  min-width: 0;
  direction: ltr;
  display: grid;
  place-items: center;
  min-height: 300px;
}
.art-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(#b1a9ef18 1px, transparent 1px),
    linear-gradient(90deg, #b1a9ef18 1px, transparent 1px);
  background-size: 30px 30px;
  mask-image: radial-gradient(ellipse, #000, transparent 72%);
}
.art-ring {
  position: absolute;
  border: 1px dashed #aaa0ed60;
  border-radius: 50%;
  width: 260px;
  height: 260px;
}
.ring-inner {
  width: 170px;
  height: 170px;
  border-style: solid;
  border-color: #b7acf142;
}
.art-core {
  width: 103px;
  height: 108px;
  border-radius: 27px;
  background: linear-gradient(145deg, #8275f1, #5846c9);
  box-shadow:
    0 15px 30px #6259e833,
    inset 0 1px 0 #ffffff70;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: rotate(-9deg);
  color: #fff;
  z-index: 1;
}
.art-core > span {
  font: 600 48px/1 Arial;
  letter-spacing: -5px;
  margin-right: 5px;
}
.art-core > small {
  font: 7px/1 Arial;
  letter-spacing: 1.7px;
  margin-top: 9px;
}
.art-chip {
  position: absolute;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 11px 13px;
  background: #ffffffed;
  border: 1px solid #e7e4f8;
  border-radius: 10px;
  box-shadow: 0 7px 20px #5b4caa0a;
  font: 11px Arial;
  color: #62598b;
}
.art-chip > .icon {
  color: #7d6dd6;
  width: 16px;
  height: 16px;
}
.art-chip > i {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #76b79b;
  margin-left: 10px;
}
.chip-identity {
  top: 46px;
  left: 16%;
}
.chip-business {
  right: 9%;
  top: 50%;
}
.chip-operations {
  bottom: 36px;
  left: 10%;
}
.art-spark {
  position: absolute;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #b1a0eb;
  top: 32%;
  right: 26%;
}
.spark-two {
  top: auto;
  bottom: 23%;
  right: 35%;
  width: 5px;
  height: 5px;
  background: #c1b2ed;
}
.overview-strip {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  background: var(--sc-surface);
  border: 1px solid var(--sc-border);
  border-radius: 14px;
  margin: 22px 0 34px;
  box-shadow: var(--sc-shadow);
}
.overview-strip > div {
  display: flex;
  gap: 13px;
  align-items: center;
  padding: 22px 25px;
  min-width: 0;
}
.overview-strip > div + div {
  border-inline-start: 1px solid var(--sc-border);
}
.overview-icon {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 11px;
  background: var(--sc-primary-soft);
  color: var(--sc-primary);
  flex-shrink: 0;
}
.overview-icon.green {
  background: var(--sc-positive-soft);
  color: var(--sc-positive);
}
.overview-icon.amber {
  background: var(--sc-warning-soft);
  color: var(--sc-warning);
}
.overview-strip strong {
  display: block;
  font-size: 12px;
}
.overview-strip small {
  display: block;
  font-size: 9px;
  color: var(--sc-muted);
  margin-top: 3px;
}
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}
.section-heading h2 {
  font-size: 17px;
}
.section-heading p {
  font-size: 10px;
  color: var(--sc-muted);
  margin-top: 4px;
}
.count-label {
  color: var(--sc-muted);
  font-size: 10px;
}
.directory-tools {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap;
}
.filter-tabs {
  display: flex;
  gap: 4px;
  align-items: center;
  flex-wrap: wrap;
}
.filter-tabs button {
  padding: 7px 13px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--sc-muted);
  font-size: 10px;
  border-radius: 7px;
  min-height: 34px;
}
.filter-tabs button.selected {
  background: var(--sc-surface);
  border-color: var(--sc-border);
  color: var(--sc-text);
  box-shadow: var(--sc-shadow);
}
.search-field {
  display: flex;
  align-items: center;
  gap: 9px;
  background: var(--sc-surface);
  border: 1px solid var(--sc-border);
  border-radius: 8px;
  padding: 0 12px;
  min-height: 36px;
  width: 232px;
  color: var(--sc-muted);
}
.search-field > .icon {
  width: 15px;
  height: 15px;
}
.search-field input {
  background: transparent;
  border: 0;
  min-width: 0;
  width: 100%;
  color: var(--sc-text);
  font-size: 10px;
  outline: 0;
}
.search-field:focus-within {
  outline: 2px solid var(--sc-primary);
  outline-offset: 2px;
}
.search-field input:focus-visible {
  outline: none;
}
.module-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}
.module-card {
  background: var(--sc-surface);
  border: 1px solid var(--sc-border);
  border-radius: 13px;
  padding: 20px;
  box-shadow: var(--sc-shadow);
  transition:
    transform 0.15s,
    border-color 0.15s;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.module-card:hover {
  transform: translateY(-3px);
  border-color: #b7b1ec;
}
.module-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 17px;
}
.module-icon {
  width: 43px;
  height: 43px;
  background: var(--sc-primary-soft);
  color: var(--sc-primary);
  border-radius: 12px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}
.module-icon > .icon {
  width: 21px;
  height: 21px;
}
.module-business .module-icon,
.module-scheduling .module-icon {
  background: var(--sc-positive-soft);
  color: var(--sc-positive);
}
.module-reservation .module-icon,
.module-communication .module-icon {
  background: var(--sc-warning-soft);
  color: var(--sc-warning);
}
.module-inventory .module-icon,
.module-iot .module-icon {
  background: #eaf1fb;
  color: #4c80c8;
}
.favorite-button {
  padding: 6px;
  display: grid;
  place-items: center;
  border: 0;
  background: transparent;
  color: #b8c0d0;
  border-radius: 5px;
}
.favorite-button > .icon {
  width: 15px;
  height: 15px;
}
.favorite-button.is-favorite {
  color: #bd851f;
}
.favorite-button.is-favorite > .icon {
  fill: #e5ba4833;
}
.module-card h3 {
  font-size: 12px;
  margin-bottom: 7px;
}
.module-card > p {
  font-size: 10px;
  color: var(--sc-muted);
  line-height: 2;
  min-height: 40px;
  margin-bottom: 18px;
}
.module-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--sc-border);
  padding-top: 12px;
  margin-top: auto;
  gap: 6px;
}
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--sc-muted);
  font-size: 9px;
}
.status-badge > span {
  width: 5px;
  height: 5px;
  background: #a7b0c0;
  border-radius: 50%;
}
.status-badge.available {
  color: var(--sc-positive);
}
.status-badge.available > span {
  background: var(--sc-positive);
}
.module-link {
  width: 25px;
  height: 25px;
  display: grid;
  place-items: center;
  border-radius: 6px;
  background: var(--sc-soft);
  color: var(--sc-muted);
}
.module-link > .icon {
  width: 13px;
  height: 13px;
}
html[dir="rtl"] .module-link > .icon,
html[dir="rtl"] .hero-actions .button .icon:last-child,
html[dir="rtl"] .text-link > .icon {
  transform: rotate(180deg);
}
.continuation-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 22px 24px;
  border: 1px solid var(--sc-border);
  border-radius: 13px;
  background: var(--sc-surface);
  margin-top: 28px;
}
.continuation-card h2 {
  font-size: 12px;
}
.continuation-card p {
  font-size: 10px;
  line-height: 2;
  color: var(--sc-muted);
  max-width: 650px;
  margin-top: 4px;
}
.text-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--sc-primary);
  font-size: 10px;
  white-space: nowrap;
  margin-inline-start: auto;
}
.text-link .icon {
  width: 15px;
  height: 15px;
}
.app-footer {
  max-width: 1510px;
  margin: auto;
  padding: 0 38px 22px;
  display: flex;
  justify-content: space-between;
  gap: 15px;
  color: var(--sc-muted);
  font-size: 9px;
}
.empty-results {
  padding: 50px;
  text-align: center;
  background: var(--sc-surface);
  border: 1px dashed var(--sc-border);
  border-radius: 12px;
}
.back-link {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 11px;
  color: var(--sc-muted);
  margin-bottom: 22px;
}
.back-link .icon {
  width: 15px;
  transform: rotate(180deg);
}
html[dir="rtl"] .back-link .icon {
  transform: none;
}
.module-detail {
  background: var(--sc-surface);
  border: 1px solid var(--sc-border);
  border-radius: 20px;
  padding: 40px;
  max-width: 850px;
}
.module-icon.large {
  width: 62px;
  height: 62px;
  margin-bottom: 20px;
}
.module-icon.large > .icon {
  width: 30px;
  height: 30px;
}
.module-detail h1 {
  font-size: 29px;
}
.detail-summary {
  font-size: 13px;
  color: var(--sc-muted);
  margin: 12px 0 18px;
}
.detail-divider {
  border-top: 1px solid var(--sc-border);
  margin: 30px 0;
}
.module-detail h2 {
  font-size: 16px;
}
.capability-list {
  list-style: none;
  padding: 0;
  margin: 18px 0;
  display: grid;
  gap: 13px;
}
.capability-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
}
.capability-list .icon {
  color: var(--sc-primary);
  width: 17px;
  height: 17px;
}
.integration-note {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px;
  border-radius: 10px;
  background: var(--sc-soft);
  font-size: 11px;
  color: var(--sc-muted);
  margin: 28px 0;
  line-height: 2;
}
.integration-note > .icon {
  color: var(--sc-primary);
  margin-top: 3px;
}
.settings-card {
  max-width: 850px;
  border: 1px solid var(--sc-border);
  border-radius: 16px;
  background: var(--sc-surface);
  padding: 10px 30px 28px;
}
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 26px 0;
  border-bottom: 1px solid var(--sc-border);
}
.setting-row h2 {
  font-size: 14px;
}
.setting-row p {
  font-size: 11px;
  color: var(--sc-muted);
  margin-top: 6px;
}
.theme-option {
  display: flex;
  gap: 10px;
  align-items: center;
  background: var(--sc-soft);
  border: 1px solid var(--sc-border);
  border-radius: 9px;
  padding: 9px 16px;
  font-size: 12px;
}
.language-choices {
  display: flex;
  gap: 5px;
  border: 1px solid var(--sc-border);
  border-radius: 8px;
  padding: 4px;
}
.language-choices a {
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 11px;
}
.language-choices a[aria-current="page"] {
  background: var(--sc-primary-soft);
  color: var(--sc-primary);
}
.settings-note {
  font-size: 11px;
  color: var(--sc-muted);
  line-height: 2;
  margin-top: 24px;
}
.mobile-menu {
  display: none;
}
:root[data-theme="dark"] .welcome-card {
  background: #25233f;
  border-color: #3b365c;
}
:root[data-theme="dark"] .welcome-copy h2 {
  color: #f1eeff;
}
:root[data-theme="dark"] .welcome-copy > p {
  color: #b6b1d1;
}
:root[data-theme="dark"] .hero-label,
:root[data-theme="dark"] .hero-secondary {
  color: #b1a7f0;
}
:root[data-theme="dark"] .art-chip {
  background: #2c2947;
  border-color: #494065;
  color: #d8d1f1;
}
:root[data-theme="dark"] .module-inventory .module-icon,
:root[data-theme="dark"] .module-iot .module-icon {
  background: #23324b;
  color: #91b6ef;
}
@media (min-width: 1600px) {
  .main-content {
    padding-top: 45px;
  }
  .welcome-card {
    min-height: 345px;
  }
  .welcome-copy {
    padding: 40px 44px;
  }
  .welcome-copy h2 {
    font-size: 40px;
  }
  .module-card {
    padding: 24px;
  }
  .module-card h3 {
    font-size: 14px;
  }
  .module-card > p {
    font-size: 12px;
  }
}
@media (max-width: 1240px) {
  .sidebar {
    width: 225px;
    padding-inline: 17px;
  }
  .app-body {
    margin-inline-start: 225px;
  }
  .topbar {
    padding-inline: 26px;
  }
  .main-content {
    padding: 28px 26px;
  }
  .app-footer {
    padding-inline: 26px;
  }
  .module-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .overview-strip > div {
    padding: 18px;
  }
  .overview-strip small {
    font-size: 8px;
  }
  .welcome-copy {
    padding: 28px;
  }
  .art-chip {
    padding: 9px;
    font-size: 10px;
  }
  .chip-identity {
    left: 3%;
  }
  .chip-business {
    right: 1%;
  }
  .chip-operations {
    left: 2%;
  }
}
@media (max-width: 1000px) {
  .module-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .welcome-card {
    grid-template-columns: 1.4fr 1fr;
  }
  .welcome-copy h2 {
    font-size: 29px;
  }
  .welcome-copy > p {
    font-size: 10px;
  }
  .platform-art {
    transform: scale(0.85);
  }
  .overview-strip {
    grid-template-columns: 1fr;
  }
  .overview-strip > div + div {
    border-inline-start: 0;
    border-top: 1px solid var(--sc-border);
  }
  .overview-strip > div {
    padding: 15px 20px;
  }
  .overview-strip small {
    font-size: 10px;
  }
  .continuation-card {
    flex-wrap: wrap;
  }
  .text-link {
    margin-inline-start: 56px;
  }
}
@media (max-width: 760px) {
  .sidebar {
    display: none;
    width: 256px;
  }
  .sidebar.is-open {
    display: flex;
  }
  .sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: 20;
    background: #10152e80;
    border: 0;
  }
  .app-body {
    margin-inline-start: 0;
  }
  .mobile-menu {
    display: grid;
  }
  .topbar {
    height: 68px;
    padding-inline: 20px;
    gap: 10px;
  }
  .breadcrumb {
    gap: 10px;
    font-size: 10px;
  }
  .topbar-actions {
    gap: 7px;
  }
  .environment-badge {
    font-size: 9px;
    margin-inline-end: 2px;
  }
  .main-content {
    padding: 26px 20px;
  }
  .page-intro h1 {
    font-size: 23px;
  }
  .page-intro {
    align-items: flex-start;
  }
  .page-intro > .button {
    display: none;
  }
  .welcome-card {
    grid-template-columns: 1fr 0.8fr;
  }
  .welcome-copy {
    padding: 25px;
  }
  .welcome-copy h2 {
    font-size: 28px;
  }
  .platform-art {
    transform: scale(0.85);
    margin-inline: -30px;
  }
  .hero-actions {
    gap: 14px;
  }
  .hero-secondary {
    display: none;
  }
  .welcome-copy > p {
    font-size: 11px;
  }
  .app-footer {
    padding-inline: 20px;
  }
  .directory-tools {
    align-items: stretch;
  }
  .search-field {
    width: 100%;
  }
  .filter-tabs {
    width: 100%;
  }
  .module-detail {
    padding: 28px;
  }
  .settings-card {
    padding-inline: 22px;
  }
}
@media (max-width: 500px) {
  .main-content {
    padding: 22px 16px;
  }
  .topbar {
    padding-inline: 16px;
  }
  .environment-badge {
    display: none;
  }
  .breadcrumb > span:first-of-type,
  .breadcrumb-separator {
    display: none;
  }
  .page-intro h1 {
    font-size: 22px;
  }
  .page-intro p:last-child {
    font-size: 10px;
  }
  .welcome-card {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  .welcome-copy {
    padding: 26px;
  }
  .welcome-copy h2 {
    font-size: 32px;
  }
  .welcome-copy > p {
    max-width: 100%;
  }
  .platform-art {
    display: none;
  }
  .hero-actions {
    margin-top: 22px;
  }
  .hero-secondary {
    display: inline;
  }
  .overview-strip {
    margin-bottom: 28px;
  }
  .module-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .module-card {
    padding: 14px;
  }
  .module-card h3 {
    font-size: 11px;
  }
  .module-card > p {
    font-size: 9px;
    min-height: 54px;
    margin-bottom: 12px;
  }
  .module-card-top {
    margin-bottom: 13px;
  }
  .module-icon {
    width: 35px;
    height: 35px;
    border-radius: 9px;
  }
  .module-icon > .icon {
    width: 18px;
    height: 18px;
  }
  .status-badge {
    font-size: 8px;
  }
  .module-card-footer {
    gap: 3px;
  }
  .module-link {
    width: 22px;
    height: 22px;
  }
  .section-heading h2 {
    font-size: 16px;
  }
  .section-heading p {
    font-size: 9px;
  }
  .filter-tabs button {
    padding: 6px 10px;
    font-size: 9px;
  }
  .continuation-card {
    padding: 18px;
    gap: 12px;
  }
  .continuation-card > div {
    flex: 1;
    min-width: 180px;
  }
  .continuation-card h2 {
    font-size: 11px;
  }
  .text-link {
    margin-inline-start: 0;
  }
  .app-footer {
    padding-inline: 16px;
    flex-wrap: wrap;
    font-size: 8px;
  }
  .module-detail {
    padding: 24px;
  }
  .module-detail h1 {
    font-size: 23px;
  }
  .detail-summary {
    font-size: 12px;
  }
  .setting-row {
    flex-wrap: wrap;
  }
  .settings-card {
    padding-inline: 20px;
  }
  .page-intro {
    margin-bottom: 22px;
  }
}
@media (max-width: 350px) {
  .module-grid {
    grid-template-columns: 1fr;
  }
  .module-card > p {
    min-height: 0;
  }
  .module-card h3 {
    font-size: 13px;
  }
  .module-card > p {
    font-size: 11px;
  }
  .status-badge {
    font-size: 10px;
  }
  .hero-actions {
    flex-wrap: wrap;
    gap: 12px;
  }
  .topbar {
    gap: 5px;
  }
  .breadcrumb {
    gap: 7px;
  }
}
/* Readable interface scale, shared across desktop and narrow layouts. */
.workspace-label strong,
.sidebar-note strong,
.sidebar-footer strong {
  font-size: 12px;
}
.workspace-label small,
.nav-caption,
.sidebar-note p,
.sidebar-footer small {
  font-size: 11px;
}
.nav-item {
  font-size: 14px;
}
.breadcrumb {
  font-size: 12px;
}
.environment-badge {
  font-size: 11px;
}
.page-intro p:last-child {
  font-size: 13px;
}
.button {
  font-size: 13px;
}
.hero-label {
  font-size: 11px;
}
.welcome-copy > p {
  font-size: 13px;
}
.hero-secondary {
  font-size: 12px;
}
.overview-strip strong {
  font-size: 14px;
}
.overview-strip small {
  font-size: 11px;
}
.section-heading p,
.count-label {
  font-size: 12px;
}
.filter-tabs button,
.search-field input {
  font-size: 12px;
}
.module-card h3 {
  font-size: 14px;
}
.module-card > p {
  font-size: 12px;
  min-height: 48px;
}
.status-badge {
  font-size: 10px;
}
.continuation-card h2 {
  font-size: 14px;
}
.continuation-card p,
.text-link {
  font-size: 12px;
}
.app-footer {
  font-size: 11px;
}
@media (max-width: 500px) {
  .nav-item {
    font-size: 13px;
  }
  .module-card h3 {
    font-size: 12px;
  }
  .module-card > p {
    font-size: 11px;
    min-height: 66px;
  }
  .status-badge {
    font-size: 9px;
  }
  .module-card-footer {
    flex-wrap: wrap;
  }
  .section-heading p {
    font-size: 11px;
  }
  .page-intro p:last-child {
    font-size: 12px;
  }
  .button {
    font-size: 12px;
  }
  .overview-strip small {
    font-size: 11px;
  }
  .continuation-card h2 {
    font-size: 12px;
  }
  .continuation-card p,
  .text-link {
    font-size: 11px;
  }
  .breadcrumb {
    font-size: 11px;
  }
  .app-footer {
    font-size: 10px;
  }
}
@media (max-width: 350px) {
  .module-card h3 {
    font-size: 14px;
  }
  .module-card > p {
    font-size: 12px;
    min-height: 0;
  }
  .status-badge {
    font-size: 11px;
  }
  .hero-actions .button {
    font-size: 11px;
  }
}
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition: none !important;
    animation: none !important;
    scroll-behavior: auto !important;
  }
}

```


## Identity: web/identity/src/app/globals.css

```css
@import "tailwindcss";
@import './smartcore.css';
:root {--ink:var(--sc-text);--muted:var(--sc-muted);--paper:var(--sc-bg);--line:var(--sc-border);--accent:var(--sc-primary);--warm:#c65b38;}
* {box-sizing:border-box;}
body {margin:0;background:var(--paper);color:var(--ink);font-family:var(--sc-font);line-height:1.7;}
button,input,a { -webkit-tap-highlight-color:transparent; }
button,a {touch-action:manipulation;}
button {cursor:pointer;transition:background .16s,border-color .16s;}
button:disabled {cursor:wait;opacity:.55;}
a {text-decoration:none;color:inherit;}
button:focus-visible,a:focus-visible,input:focus-visible,[tabindex]:focus-visible {outline:3px solid #d48a47;outline-offset:4px;}
.identity-shell {max-width:1440px;margin:auto;padding:0 5vw;}
.site-header {height:110px;display:flex;align-items:center;justify-content:space-between;gap:20px;}
.brand {display:flex;gap:12px;align-items:center;font-size:21px;font-weight:bold;}
.brand small {display:block;font:9px/1.8 Arial,sans-serif;letter-spacing:2px;direction:ltr;}
.brand-symbol {display:grid;place-items:center;width:44px;height:44px;border-radius:13px 13px 3px 13px;background:var(--ink);color:#e6eea7;font:29px Georgia,serif;}
.language-link {font-size:13px;display:flex;gap:18px;align-items:center;border-bottom:1px solid var(--line);padding:8px 0;}
.identity-layout {display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;min-height:690px;border:1px solid var(--line);border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 20px 60px #173b3606;}
.identity-story {position:relative;overflow:hidden;padding:46px 48px 30px;background:#173b36;color:#faf9ee;display:flex;flex-direction:column;}
.eyebrow {font-size:11px;font-weight:bold;letter-spacing:.08em;display:flex;gap:10px;align-items:center;}
.status-dot {width:7px;height:7px;display:inline-block;background:#d6e8a0;border-radius:50%;}
.identity-story h1 {font-size:clamp(29px,3vw,45px);line-height:1.65;max-width:470px;margin:22px 0 14px;font-weight:600;letter-spacing:-.035em;}
.story-description {font-size:14px;line-height:2.1;color:#ccd9d1;max-width:365px;margin:0;}
.identity-art {height:250px;position:relative;margin-top:18px;display:grid;place-items:center;direction:ltr;}
.orbit {position:absolute;width:255px;height:174px;border:1px solid #a5c7a847;border-radius:50%;transform:rotate(-30deg);}
.orbit-two {transform:rotate(35deg);width:220px;height:220px;}
.core-tile {z-index:1;width:106px;height:117px;border:1px solid #f3f7d94a;border-radius:25px;background:linear-gradient(140deg,#e3ecae,#adcb8f);color:#173b36;font:64px/1 Georgia,serif;display:flex;align-items:center;justify-content:center;flex-direction:column;box-shadow:0 12px 50px #0002;transform:rotate(-8deg);}
.core-tile span {font:7px Arial,sans-serif;letter-spacing:2px;margin-top:10px;}
.art-label {position:absolute;font:8px Arial,sans-serif;letter-spacing:2px;color:#b7cbbc;background:#173b36;padding:8px;border:1px solid #7f9e813d;border-radius:6px;}
.art-label-one {top:38px;left:9%;}.art-label-two {bottom:24px;right:0;}
.art-node {position:absolute;width:10px;height:10px;border-radius:50%;background:#da956d;box-shadow:0 0 0 5px #da956d12;}
.node-one {top:32px;right:26%;}.node-two {bottom:47px;left:20%;width:6px;height:6px;background:#d6e8a0;}
.story-bottom {margin-top:auto;display:flex;gap:18px;border-top:1px solid #bad3b32b;padding-top:20px;align-items:center;}
.story-number {font:12px Arial,sans-serif;color:#c8db9c;white-space:nowrap;direction:ltr;}
.story-bottom p {font-size:12px;color:#c3d0c8;margin:0;}
.account-surface {padding:36px 44px;min-width:0;align-self:center;}
.surface-heading {display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;gap:10px;}
.surface-heading .eyebrow {color:var(--accent);}
.section-number {font:12px Arial,sans-serif;color:#94a59b;}
h2 {font-size:25px;font-weight:600;line-height:1.7;margin:0;}h3 {font-size:16px;font-weight:600;}
.form-intro p,.empty-state p {font-size:13px;color:var(--muted);margin:8px 0 12px;line-height:2;}
.auth-form {display:grid;gap:18px;}
.field-label,.account-surface form label.grid {display:grid;gap:8px;font-size:12px;font-weight:500;}
.account-surface input:not([type=checkbox]) {width:100%;min-width:0;border:1px solid var(--line);border-radius:10px;background:#fafbf8;color:var(--ink);padding:12px 14px;min-height:48px;font-size:15px;}
.account-surface input[aria-invalid=true] {border-color:#b73e37;}
.account-surface input[type=checkbox] {accent-color:var(--accent);width:17px;height:17px;flex-shrink:0;}
.password-field {display:grid;gap:8px;}.password-control {position:relative;}
.password-control input {padding-inline-end:70px!important;}
.password-control button {position:absolute;inset-inline-end:9px;top:7px;bottom:7px;padding:0 9px;font-size:11px;color:var(--accent);border-radius:5px;}
.primary-button,.account-surface form button[type=submit],.account-surface form button:not([type]) {display:flex;align-items:center;justify-content:center;gap:24px;background:var(--accent);color:white;border:1px solid var(--accent);border-radius:10px;padding:13px 18px;font-size:13px;font-weight:600;min-height:48px;}
.primary-button:hover,.account-surface form button[type=submit]:hover {background:#115544;}
.secondary-button {border:1px solid var(--line);border-radius:10px;padding:11px 18px;font-size:12px;min-height:44px;background:white;}
.secondary-button:hover {background:#f2f5ef;}
.text-button {font-size:12px;color:var(--accent);padding:7px 0;text-decoration:underline;text-underline-offset:4px;}
.forgot-button {justify-self:end;margin-top:-12px;}
.form-alternative {border-top:1px solid var(--line);padding-top:20px;display:flex;justify-content:space-between;align-items:center;gap:12px;}
.form-alternative p,.form-footnote {font-size:11px;color:var(--muted);}.form-footnote {text-align:center;margin:0;line-height:1.9;}
.environment-notice,.success-notice,.error-notice,.recovery-reminder {padding:12px 14px;border-radius:10px;font-size:12px;line-height:2;margin:12px 0;}
.environment-notice {background:#fcf3df;color:#795a29;}.success-notice {background:#eff6ec;color:#325b3e;}.error-notice {background:#fff0ed;color:#a4322c;border:1px solid #f3cec7;}
.profile-heading {display:flex;align-items:center;gap:14px;}.profile-heading h2 {font-size:20px;}.profile-contact {font-size:12px;color:var(--muted);overflow-wrap:anywhere;text-align:start;}
.avatar {width:50px;height:50px;flex-shrink:0;display:grid;place-items:center;border-radius:16px;background:#e6eddd;color:var(--accent);font-size:23px;}
.account-navigation {display:flex;gap:24px;border-bottom:1px solid var(--line);margin-top:24px;}.account-navigation button {font-size:12px;padding:12px 0;border-bottom:2px solid transparent;color:var(--muted);}.account-navigation button[aria-pressed=true] {border-color:var(--accent);color:var(--accent);font-weight:bold;}
.overview-panel {padding-top:22px;}.overview-panel[hidden] {display:none;}.account-details {margin:14px 0;}.account-details>div {display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid #edf0ea;font-size:12px;}.account-details dt {color:var(--muted);}.account-details dd {overflow-wrap:anywhere;max-width:100%;margin:0;}
.recovery-reminder {background:#f8f5e9;}.recovery-reminder p {margin:0;}.account-actions {display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-top:22px;margin-top:24px;}
.registration-steps {display:flex;list-style:none;padding:0;margin:5px 0 18px;gap:8px;}.registration-steps li {flex:1;font-size:10px;color:var(--muted);border-top:3px solid var(--line);padding-top:8px;}.registration-steps li[aria-current=step] {color:var(--accent);border-color:var(--accent);font-weight:bold;}
.password-hint,.step-description {font-size:12px;color:var(--muted);line-height:2;}.otp-field {font:24px/1.4 monospace!important;letter-spacing:.3em;text-align:center;}
.site-footer {display:flex;justify-content:space-between;gap:15px;padding:24px 0;font-size:10px;color:var(--muted);}.skip-link {position:absolute;top:-100px;}.skip-link:focus {top:8px;z-index:10;background:white;padding:10px;}.loading-state {min-height:220px;display:grid;place-items:center;font-size:13px;color:var(--muted);}
@media (min-width:1100px) {.account-surface {padding:44px 64px;}}
@media (max-width:760px) {.identity-shell {padding:0 20px;}.site-header {height:84px;}.identity-layout {grid-template-columns:1fr;border-radius:20px;min-height:0;}.identity-story {padding:28px;}.identity-story h1 {font-size:28px;margin:14px 0 10px;}.story-description {font-size:12px;}.identity-art,.story-bottom {display:none;}.account-surface {padding:28px 24px;}.surface-heading {margin-bottom:22px;}.site-footer {flex-wrap:wrap;font-size:9px;}.is-account .identity-story h1 {font-size:24px;}.is-account .identity-story .story-description {display:none;}.account-actions {flex-wrap:wrap;}}
@media (prefers-reduced-motion:reduce) {* {scroll-behavior:auto!important;transition:none!important;}}
.identity-story h1 {white-space:pre-line;}
.password-control {direction:ltr;}
@media (max-width:480px) {.brand {font-size:18px;gap:8px;}.brand-symbol {width:36px;height:38px;font-size:25px;}.brand small {font-size:7px;letter-spacing:1px;white-space:nowrap;}.identity-story {padding:22px 24px;}.identity-story h1 {font-size:24px;line-height:1.6;white-space:normal;margin-bottom:0;}.identity-story .story-description {display:none;}}

/* Shared platform skin. Account state, guards and BFF requests stay unchanged. */
.brand-symbol{background:var(--sc-primary);color:#fff;font:700 27px Arial,sans-serif;border-radius:13px;}
.identity-layout{border-radius:20px;box-shadow:var(--sc-shadow);}
.identity-story{background:#29254f;color:#f5f2ff;}
.story-description,.story-bottom p{color:#cbc6e6;}
.status-dot{background:#b6adff;}
.core-tile{background:linear-gradient(145deg,#9a8ff6,#6555d8);color:#fff;border-color:#c1b8ff80;box-shadow:0 16px 45px #0d063638;}
.orbit{border-color:#aaa0ed60;}.art-label{background:#302b54;color:#d4ceef;border-color:#aaa0ed40;}
.art-node{background:#b9afff;box-shadow:0 0 0 5px #b9afff12;}.node-two{background:#d1c9fc;}
.story-number{color:#b6adff;}.story-bottom{border-color:#aaa0ed30;}
.account-surface input:not([type=checkbox]){background:var(--sc-bg);border-color:var(--sc-border);border-radius:9px;}
.primary-button,.account-surface form button[type=submit],.account-surface form button:not([type]){border-radius:9px;}
.primary-button:hover,.account-surface form button[type=submit]:hover{background:var(--sc-primary-hover);}
button:focus-visible,a:focus-visible,input:focus-visible,[tabindex]:focus-visible{outline-color:var(--sc-primary);}
.avatar{background:var(--sc-primary-soft);color:var(--sc-primary);border-radius:13px;}
.success-notice{background:var(--sc-positive-soft);color:var(--sc-positive);}
.environment-notice,.recovery-reminder{background:var(--sc-warning-soft);color:var(--sc-warning);}
.platform-return{font-size:11px;color:var(--sc-primary);display:inline-flex;gap:8px;align-items:center;}
.header-links{display:flex;align-items:center;gap:24px;}
.preview-fields{border:0;padding:0;margin:24px 0 0;min-width:0;}.preview-fields input{opacity:.65;}.preview-fields button{cursor:not-allowed;opacity:.55;}
@media(max-width:480px){.header-links{gap:10px;}.platform-return{font-size:9px;}.language-link{font-size:10px;gap:4px;}}

```


## Legacy Business reference: frontend/components/app-shell.tsx

```tsx
"use client";

import { useBusinessContext } from "@/shared/providers/business-context-provider";
import { Building2, BriefcaseBusiness, FolderTree, Home, MapPin, Menu, ShieldCheck, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";
import { useState } from "react";

const navItems = [
  { key: "dashboard", path: "", icon: Home },
  { key: "business", path: "business", icon: Building2 },
  { key: "locations", path: "locations", icon: MapPin },
  { key: "categories", path: "service-categories", icon: FolderTree },
  { key: "services", path: "services", icon: BriefcaseBusiness },
  { key: "policies", path: "policies", icon: ShieldCheck },
] as const;

function localePath(locale: string, path: string) {
  return path ? `/${locale}/${path}` : `/${locale}`;
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const locale = useLocale();
  const pathname = usePathname();
  const t = useTranslations("admin");
  const { businessId, business, isLoading, error, clearBusiness } = useBusinessContext();
  const [menuOpen, setMenuOpen] = useState(false);
  const businessName = business?.profile?.name ?? business?.slug;
  let consoleOrigin: string | undefined;
  try {
    const value = process.env.NEXT_PUBLIC_SMARTCORE_CONSOLE_ORIGIN;
    if (value) {
      const url = new URL(value);
      if ((url.protocol === "https:" || (url.protocol === "http:" && ["localhost", "127.0.0.1"].includes(url.hostname))) && !url.username && !url.password && url.pathname === "/" && !url.search && !url.hash) consoleOrigin = url.origin;
    }
  } catch { /* An invalid optional platform entry point must not create a link. */ }

  return (
    <div className="smartcore-admin min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen flex-col md:flex-row">
        <aside className={`${menuOpen ? "block" : "hidden"} w-full border-b border-slate-200 bg-white md:block md:w-72 md:border-b-0 md:border-e`}>
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
            <div>
              <p className="smartcore-brand">SmartCore</p>
              <h2 className="text-lg font-semibold">{t("product")}</h2>
            </div>
            <button type="button" className="rounded-md p-2 text-slate-600 hover:bg-slate-100 md:hidden" aria-label={t("closeMenu")} onClick={() => setMenuOpen(false)}>
              <X className="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
          <nav aria-label={t("navigation")} className="space-y-1 p-3">
            {navItems.map(({ key, path, icon: Icon }) => {
              const href = localePath(locale, path);
              const active = pathname === href || (path !== "" && pathname.startsWith(`${href}/`));
              return (
                <Link key={key} href={href} aria-current={active ? "page" : undefined} onClick={() => setMenuOpen(false)} className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 ${active ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"}`}>
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {t(`nav.${key}`)}
                </Link>
              );
            })}
          </nav>
          {consoleOrigin && <div className="px-5 pb-5"><a className="smartcore-platform-return" href={`${consoleOrigin}/${locale}`}>{locale === "fa" ? "بازگشت به فضای کار اسمارت‌کور ↗" : "Back to SmartCore workspace ↗"}</a></div>}
        </aside>

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <header className="border-b border-slate-200 bg-white px-4 py-4 sm:px-6">
            <div className="flex flex-col items-stretch justify-between gap-4 sm:flex-row sm:items-center">
              <div className="flex items-center gap-3">
                <button type="button" className="rounded-md p-2 text-slate-600 hover:bg-slate-100 md:hidden" aria-label={t("openMenu")} aria-expanded={menuOpen} onClick={() => setMenuOpen(true)}>
                  <Menu className="h-5 w-5" aria-hidden="true" />
                </button>
                <div>
                  <p className="text-xs uppercase tracking-[0.12em] text-slate-500">{t("section")}</p>
                  <h1 className="text-xl font-semibold">{t("title")}</h1>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Link href={pathname.replace(/^\/(fa|en)(?=\/|$)/, `/${locale === "fa" ? "en" : "fa"}`)} className="rounded-md border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500">
                  {locale === "fa" ? "EN" : "FA"}
                </Link>
                <BusinessSelector name={businessName} businessId={businessId} isLoading={isLoading} errorCode={error?.code} onClear={clearBusiness} t={t} />
              </div>
            </div>
          </header>
          <main className="flex-1">{children}</main>
        </div>
      </div>
    </div>
  );
}

function BusinessSelector({ name, businessId, isLoading, errorCode, onClear, t }: { name?: string; businessId: string | null; isLoading: boolean; errorCode?: string; onClear: () => void; t: ReturnType<typeof useTranslations> }) {
  let label = t("noBusiness");
  if (isLoading) label = t("loading");
  else if (errorCode === "BUSINESS_NOT_FOUND") label = t("errors.notFound");
  else if (errorCode === "BUSINESS_ACCESS_DENIED") label = t("errors.accessDenied");
  else if (name) label = name;
  else if (businessId) label = businessId;

  return (
    <div className="flex max-w-[12rem] items-center gap-2 rounded-md border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm" aria-label={t("selector")}>
      <Building2 className="h-4 w-4 shrink-0 text-slate-500" aria-hidden="true" />
      <span className="truncate text-slate-700">{label}</span>
      {businessId && <button type="button" onClick={onClear} className="shrink-0 text-xs text-slate-500 underline hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-500">{t("clear")}</button>}
    </div>
  );
}

```


## Legacy Business reference CSS: frontend/app/globals.css

```css
@import './smartcore.css';
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: var(--sc-bg);
  --foreground: var(--sc-text);
}

html {
  color-scheme: light;
}

body {
  margin: 0;
  background: var(--background);
  color: var(--foreground);
  font-family: var(--sc-font);
}

.smartcore-admin aside {background:var(--sc-surface);}
.smartcore-admin .smartcore-brand {color:var(--sc-primary);font-size:18px;letter-spacing:-.04em;font-weight:700;}
.smartcore-admin nav a[aria-current=page] {background:var(--sc-primary-soft);color:var(--sc-primary);}
.smartcore-admin button:focus-visible,.smartcore-admin a:focus-visible,.smartcore-admin input:focus-visible {outline:3px solid var(--sc-primary);outline-offset:3px;}
.smartcore-platform-return {display:inline-flex;font-size:11px;color:var(--sc-primary);margin-top:12px;}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

```


## Business canonical foundation: src/domain/business.js

```ts
export class DomainValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "DomainValidationError";
  }
}

export function normalizeLocale(locale) {
  if (typeof locale !== "string") throw new DomainValidationError("locale must be a string");
  const value = locale.trim();
  if (!value) throw new DomainValidationError("locale must not be empty");
  try {
    const canonical = Intl.getCanonicalLocales(value.replace(/_/g, "-"));
    if (canonical.length !== 1) throw new DomainValidationError(`malformed locale key: ${locale}`);
    return canonical[0];
  } catch (error) {
    if (error instanceof DomainValidationError) throw error;
    throw new DomainValidationError(`malformed locale key: ${locale}`);
  }
}

export function createBusiness(input) {
  if (!input || typeof input !== "object") throw new DomainValidationError("business input is required");
  const defaultLocale = normalizeLocale(input.defaultLocale);
  if (!Array.isArray(input.supportedLocales)) throw new DomainValidationError("supportedLocales must be an array");

  const supportedLocales = [];
  const supportedSet = new Set();
  for (const locale of input.supportedLocales) {
    const canonical = normalizeLocale(locale);
    if (supportedSet.has(canonical)) throw new DomainValidationError(`duplicate supported locale: ${canonical}`);
    supportedSet.add(canonical);
    supportedLocales.push(canonical);
  }
  if (!input.id || !input.organizationId) throw new DomainValidationError("id and organizationId are required");
  if (!supportedSet.has(defaultLocale)) throw new DomainValidationError("default locale must be supported");

  const translations = {};
  if (!Array.isArray(input.translations)) throw new DomainValidationError("translations must be an array for this creation slice");
  for (const translation of input.translations) {
    if (!translation || typeof translation !== "object") throw new DomainValidationError("invalid profile translation");
    const locale = normalizeLocale(translation.locale);
    if (!supportedSet.has(locale)) throw new DomainValidationError(`unsupported locale: ${locale}`);
    if (Object.prototype.hasOwnProperty.call(translations, locale)) {
      throw new DomainValidationError(`duplicate profile translation locale: ${locale}`);
    }
    if (!translation.displayName || typeof translation.displayName !== "string") {
      throw new DomainValidationError(`displayName is required for locale: ${locale}`);
    }
    translations[locale] = Object.freeze({ ...translation, locale });
  }
  if (!Object.prototype.hasOwnProperty.call(translations, defaultLocale)) {
    throw new DomainValidationError("restricted creation/public configuration requires the default-locale translation");
  }

  const capabilityKeys = new Set();
  if (input.capabilities !== undefined) {
    if (!Array.isArray(input.capabilities)) throw new DomainValidationError("capabilities must be an array of canonical activation keys");
    for (const key of input.capabilities) {
      if (typeof key !== "string" || !/^[A-Z][A-Z0-9_]*$/.test(key)) {
        throw new DomainValidationError("malformed capability activation key");
      }
      capabilityKeys.add(key);
    }
  }
  const activation = Object.freeze({
    values: Object.freeze([...capabilityKeys]),
    has: (key) => capabilityKeys.has(key),
  });

  return Object.freeze({
    id: input.id,
    organizationId: input.organizationId,
    slug: input.slug,
    classificationId: input.classificationId ?? null,
    defaultLocale,
    supportedLocales: Object.freeze(supportedLocales),
    profile: Object.freeze({ id: input.profile?.id ?? null, contact: input.profile?.contact ?? null }),
    translations: Object.freeze(translations),
    capabilities: activation,
  });
}

export function activateCapability(business, capabilityKey) {
  if (!business || typeof business !== "object" || Array.isArray(business)) {
    throw new DomainValidationError("valid Business context is required");
  }
  if (typeof business.id !== "string" || !business.id.trim()) {
    throw new DomainValidationError("valid Business context requires id");
  }
  if (!Array.isArray(business.supportedLocales) || typeof business.defaultLocale !== "string") {
    throw new DomainValidationError("malformed Business locale context");
  }
  normalizeLocale(business.defaultLocale);
  if (!business.capabilities || typeof business.capabilities !== "object" || Array.isArray(business.capabilities)) {
    throw new DomainValidationError("malformed Business capability context");
  }
  if (!Array.isArray(business.capabilities.values) || typeof business.capabilities.has !== "function") {
    throw new DomainValidationError("malformed Business capability context");
  }
  if (!capabilityKey || typeof capabilityKey !== "string") throw new DomainValidationError("capabilityKey is required");
  if (!/^[A-Z][A-Z0-9_]*$/.test(capabilityKey)) throw new DomainValidationError("malformed capability activation key");
  const values = new Set(business.capabilities.values);
  values.add(capabilityKey);
  return Object.freeze({
    ...business,
    capabilities: Object.freeze({
      values: Object.freeze([...values]),
      has: (key) => values.has(key),
    }),
  });
}

export function toBusinessCapabilityProjection(business) {
  if (!business || typeof business !== "object" || typeof business.id !== "string" || !business.id.trim()) {
    throw new DomainValidationError("valid Business context is required for capability projection");
  }
  if (!Array.isArray(business.supportedLocales) || typeof business.defaultLocale !== "string") {
    throw new DomainValidationError("malformed Business capability projection");
  }
  if (!business.capabilities || !Array.isArray(business.capabilities.values)) {
    throw new DomainValidationError("malformed Business capability projection");
  }
  const supportedLocales = business.supportedLocales.map(normalizeLocale);
  const values = [...new Set(business.capabilities.values)];
  return Object.freeze({
    version: 1,
    businessId: business.id,
    defaultLocale: normalizeLocale(business.defaultLocale),
    supportedLocales: Object.freeze(supportedLocales),
    capabilities: Object.freeze({
      values: Object.freeze(values),
    }),
  });
}

export function fromBusinessCapabilityProjection(projection) {
  if (!projection || typeof projection !== "object" || projection.version !== 1) {
    throw new DomainValidationError("unsupported or malformed Business capability projection");
  }
  if (typeof projection.businessId !== "string" || !projection.businessId.trim()) {
    throw new DomainValidationError("Business capability projection requires businessId");
  }
  if (!Array.isArray(projection.supportedLocales) || typeof projection.defaultLocale !== "string") {
    throw new DomainValidationError("malformed Business locale projection");
  }
  if (!projection.capabilities || !Array.isArray(projection.capabilities.values) || projection.capabilities.has !== undefined) {
    throw new DomainValidationError("malformed Business capability projection");
  }
  const supportedLocales = [];
  const supportedSet = new Set();
  for (const locale of projection.supportedLocales) {
    const canonical = normalizeLocale(locale);
    if (supportedSet.has(canonical)) throw new DomainValidationError(`duplicate supported locale: ${canonical}`);
    supportedSet.add(canonical);
    supportedLocales.push(canonical);
  }
  const defaultLocale = normalizeLocale(projection.defaultLocale);
  if (!supportedSet.has(defaultLocale)) throw new DomainValidationError("default locale must be supported");
  for (const key of projection.capabilities.values) {
    if (typeof key !== "string" || !/^[A-Z][A-Z0-9_]*$/.test(key)) {
      throw new DomainValidationError("malformed Business capability activation key");
    }
  }
  const values = Object.freeze([...projection.capabilities.values]);
  return Object.freeze({
    id: projection.businessId,
    defaultLocale,
    supportedLocales: Object.freeze(supportedLocales),
    capabilities: Object.freeze({
      values,
      has: (key) => values.includes(key),
    }),
  });
}

export function resolveProfileTranslation(business, requestedLocale) {
  if (!business || typeof business !== "object") throw new DomainValidationError("Business context is required");
  const defaultLocale = normalizeLocale(business.defaultLocale);
  const translations = business.translations;
  if (!translations || typeof translations !== "object" || Array.isArray(translations)) {
    throw new DomainValidationError("invalid Business default-translation configuration");
  }
  if (!Object.prototype.hasOwnProperty.call(translations, defaultLocale)) {
    throw new DomainValidationError("invalid Business default-translation configuration: default locale is missing");
  }
  const requested = requestedLocale === undefined || requestedLocale === null
    ? defaultLocale
    : normalizeLocale(requestedLocale);
  return translations[requested] ?? translations[defaultLocale];
}

```


## Business capability canonical owner: src/domain/service.js

```ts
export class CapabilityValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "CapabilityValidationError";
  }
}

export function normalizeLocale(locale) {
  if (typeof locale !== "string") throw new CapabilityValidationError("locale must be a string");
  const value = locale.trim();
  if (!value) throw new CapabilityValidationError("locale must not be empty");
  try {
    const canonical = Intl.getCanonicalLocales(value.replace(/_/g, "-"));
    if (canonical.length !== 1) throw new CapabilityValidationError(`malformed locale key: ${locale}`);
    return canonical[0];
  } catch (error) {
    if (error instanceof CapabilityValidationError) throw error;
    throw new CapabilityValidationError(`malformed locale key: ${locale}`);
  }
}

function requireActiveServiceSnapshot(business) {
  const snapshot = business?.capabilities;
  if (!snapshot || typeof snapshot !== "object" || Array.isArray(snapshot)) {
    throw new CapabilityValidationError("missing or malformed Business capability activation snapshot");
  }
  if (!Array.isArray(snapshot.values) || typeof snapshot.has !== "function") {
    throw new CapabilityValidationError("malformed Business capability activation snapshot");
  }
  const allValuesValid = snapshot.values.every((value) => typeof value === "string" && /^[A-Z][A-Z0-9_]*$/.test(value));
  if (!allValuesValid) throw new CapabilityValidationError("malformed Business capability activation keys");
  if (!snapshot.values.includes("SERVICE") || snapshot.has("SERVICE") !== true) {
    throw new CapabilityValidationError("SERVICE capability is inactive");
  }
}

function requireCategory(categoryLookup, categoryId, businessId) {
  if (!categoryLookup || typeof categoryLookup.lookup !== "function") {
    throw new CapabilityValidationError("category lookup boundary is required");
  }
  const category = categoryLookup.lookup(categoryId, businessId);
  if (!category || typeof category !== "object") throw new CapabilityValidationError("category does not exist");
  if (category.id !== categoryId) throw new CapabilityValidationError("category identity mismatch");
  if (category.businessId !== businessId) throw new CapabilityValidationError("category belongs to a foreign Business");
  return Object.freeze({ ...category });
}

export function createService(input, business, categoryLookup) {
  if (!input || typeof input !== "object") throw new CapabilityValidationError("service input is required");
  if (!input.id) throw new CapabilityValidationError("service id is required");
  if (!input.businessId) throw new CapabilityValidationError("businessId is required");
  if (!business || typeof business !== "object" || !business.id) throw new CapabilityValidationError("Business context is required");
  if (input.businessId !== business.id) throw new CapabilityValidationError("cross-business service is not allowed");
  requireActiveServiceSnapshot(business);

  if (!Array.isArray(business.supportedLocales)) throw new CapabilityValidationError("malformed Business supportedLocales");
  if (!business.defaultLocale) throw new CapabilityValidationError("Business defaultLocale is required");
  const supported = new Set();
  for (const locale of business.supportedLocales) {
    const canonical = normalizeLocale(locale);
    if (supported.has(canonical)) throw new CapabilityValidationError(`duplicate Business supported locale: ${canonical}`);
    supported.add(canonical);
  }
  const defaultLocale = normalizeLocale(business.defaultLocale);
  if (!supported.has(defaultLocale)) throw new CapabilityValidationError("Business default locale is not supported");

  if (!Number.isInteger(input.durationMinutes) || input.durationMinutes <= 0) {
    throw new CapabilityValidationError("durationMinutes must be a positive integer");
  }
  if (typeof input.categoryId !== "string" || !input.categoryId.trim()) {
    throw new CapabilityValidationError("categoryId is required");
  }
  requireCategory(categoryLookup, input.categoryId, business.id);

  if (!Array.isArray(input.translations)) throw new CapabilityValidationError("translations must be an array");
  const translations = {};
  for (const translation of input.translations) {
    if (!translation || typeof translation !== "object") throw new CapabilityValidationError("invalid service translation");
    const locale = normalizeLocale(translation.locale);
    if (!supported.has(locale)) throw new CapabilityValidationError(`unsupported locale: ${locale}`);
    if (Object.prototype.hasOwnProperty.call(translations, locale)) {
      throw new CapabilityValidationError(`duplicate service translation locale: ${locale}`);
    }
    if (!translation.name || typeof translation.name !== "string") {
      throw new CapabilityValidationError(`name is required for locale: ${locale}`);
    }
    translations[locale] = Object.freeze({ ...translation, locale });
  }
  if (!Object.prototype.hasOwnProperty.call(translations, defaultLocale)) {
    throw new CapabilityValidationError("service requires the Business default-locale translation");
  }
  return Object.freeze({
    id: input.id,
    businessId: business.id,
    categoryId: input.categoryId,
    slug: input.slug,
    durationMinutes: input.durationMinutes,
    priceContext: input.priceContext ?? null,
    translations: Object.freeze(translations),
  });
}

export function resolveServiceTranslation(service, business, requestedLocale) {
  if (!service || !business) throw new CapabilityValidationError("service and Business context are required");
  if (!service.businessId || !business.id) throw new CapabilityValidationError("service and Business identifiers are required");
  if (service.businessId !== business.id) {
    throw new CapabilityValidationError("service belongs to a foreign Business context");
  }
  const defaultLocale = normalizeLocale(business.defaultLocale);
  if (!service.translations || typeof service.translations !== "object" || Array.isArray(service.translations)) {
    throw new CapabilityValidationError("invalid Service default-translation configuration");
  }
  if (!Object.prototype.hasOwnProperty.call(service.translations, defaultLocale)) {
    throw new CapabilityValidationError("invalid Service default-translation configuration: default locale is missing");
  }
  const requested = requestedLocale === undefined || requestedLocale === null
    ? defaultLocale
    : normalizeLocale(requestedLocale);
  return service.translations[requested] ?? service.translations[defaultLocale];
}

```
