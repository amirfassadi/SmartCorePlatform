import { cookies } from "next/headers";
import { notFound } from "next/navigation";
import { isLocale } from "@/lib/platform";
import { Shell } from "@/components/shell";
import "../globals.css";
export const dynamic = "force-dynamic";
export const metadata = {
  title: { default: "SmartCore | فضای کار پلتفرم", template: "%s | SmartCore" },
  description: "The shared workspace for the SmartCore modular platform.",
};
export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const theme =
    (await cookies()).get("smartcore-theme")?.value === "dark"
      ? "dark"
      : "light";
  return (
    <html
      lang={locale}
      dir={locale === "fa" ? "rtl" : "ltr"}
      data-theme={theme}
    >
      <body>
        <Shell locale={locale} theme={theme}>
          {children}
        </Shell>
      </body>
    </html>
  );
}
