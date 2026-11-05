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
