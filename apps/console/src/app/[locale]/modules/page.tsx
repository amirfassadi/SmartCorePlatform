import { notFound } from "next/navigation";
import { isLocale } from "@/lib/platform";
import { ModuleDirectory } from "@/components/module-directory";
export default async function Modules({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">SMARTCORE PLATFORM</p>
          <h1>
            {locale === "fa" ? "قابلیت‌های پلتفرم" : "Platform capabilities"}
          </h1>
          <p>
            {locale === "fa"
              ? "ماژول‌ها را پیدا کنید، بشناسید و مسیر ادامهٔ کار را انتخاب کنید."
              : "Find your modules, explore their scope and choose where to continue."}
          </p>
        </div>
      </div>
      <ModuleDirectory locale={locale} />
    </>
  );
}
