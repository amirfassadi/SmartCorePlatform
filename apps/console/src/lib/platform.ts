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
