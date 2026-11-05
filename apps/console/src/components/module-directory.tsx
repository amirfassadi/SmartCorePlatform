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
