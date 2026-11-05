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
