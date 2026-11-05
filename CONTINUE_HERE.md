# ادامهٔ کار اسمارت‌کور

این نسخه محل پیشنهادی ادامهٔ توسعه UI است. پوشه‌ها و تغییرات قبلی محفوظ مانده‌اند.

برای ادامه با کوپایلت و Google AI Studio، ابتدا `handoff/START_HERE.md` را
بخوانید. پرامپت آمادهٔ هر ابزار و بستهٔ متنی منبع در همان پوشه قرار دارد.

## فضای کار

ابتدا workspace اصلاح‌شدهٔ کامل را باز کنید:
`E:/miranco.project/SmartCorePlatform/SmartCorePlatform_VSCode_Workspace/SmartCorePlatform.corrected.code-workspace`.
workspace سه‌مخزنهٔ `SmartCore-unified` فقط نمای اختیاری UI review است.
مالک canonical کسب‌وکار SmartCoreBusiness و مالک قابلیت‌ها SmartCoreBusinessCapability هستند؛
SmartCoreServiceBusiness بک‌اند اصلی نیست.
کیمیا بیوتی، کپی‌های قدیمی و پوشه‌های موقت وارد این فضای کار نشده‌اند.

## نقطهٔ شروع

کنسول پلتفرم داخل `apps/console` است و رابط حساب داخل
`SmartCoreIdentity/web/identity` قرار دارد. پنل old Business فقط در حالت اختیاری
و مرجع بصری است و مسیر رسمی نشده ندارد.

هر سه رابط از رنگ‌ها و فونت مشترک `packages/design` استفاده می‌کنند. طراحی
اصلی اختصاصی است و نیازی به خرید قالب ندارد. نگاشت ماژول‌های کنسول در
`apps/console/src/lib/platform.ts` است.

پس از اجرای `npm ci --ignore-scripts` در کنسول و Identity، از ریشهٔ این مخزن اجرا کنید:

```powershell
node tools/build-unified.mjs
node tools/start-unified.mjs
```

برای پیش‌نمایش فقط بصری ServiceBusiness، حالت اختیاری را صریح اضافه کنید:

```powershell
node tools/build-unified.mjs --legacy-business-preview
node tools/start-unified.mjs --legacy-business-preview
```

کنسول روی `http://127.0.0.1:4100/fa` و هویت روی پورت ۴۱۰۱ باز می‌شوند.
پیش‌نمایش legacy با `--legacy-business-preview` جداگانه روی پورت ۴۱۰۲ فعال می‌شود.
این دستورها فقط رابط‌ها را اجرا می‌کنند؛ دیتابیس و
سرویس‌های واقعی را راه‌اندازی یا تغییر نمی‌دهد. راه‌اندازی واقعی Identity
باید از مسیر آزموده‌شدهٔ `PRIVATE_WORKSPACE.md` در مخزن هویت انجام شود.

## ترتیب ادامه

۱. ظاهر و پیمایش مشترک این نسخه را بررسی کنید.

۲. قراردادهای معلق پلتفرم و ترتیب PRهای Identity را مطابق
`docs/implementation/PR_STACK.md` و `RELEASE_GATES.md` همان مخزن جمع‌بندی کنید.
این مرحله هیچ ADR پیشنهادی را به تصمیم مصوب تبدیل نکرده است.

۳. سرویس Identity و BFF را در محیط خصوصی خودش بالا بیاورید و ورود، ثبت‌نام،
خروج و بازیابی را با سرویس واقعی دوباره آزمایش کنید. سپس قرارداد نشست مشترک
و انتخاب سازمان را برای کنسول مشخص کنید. دادهٔ ساختگی جایگزین آن نشود.

۴. صفحه‌های Business foundation و BusinessCapability را فقط پس از پیاده‌سازی
مالک و contract واقعی متصل کنید. پنل legacy API یا مجوز canonical ندارد.

۵. رزرو و زمان‌بندی را به ترتیب نیاز محصول اضافه کنید؛ سپس موجودی، ارتباطات،
گفت‌وگو و IoT. صفحات این ماژول‌ها فعلاً معرفی قابلیت و وضعیت اتصال هستند.

۶. پس از پایدارشدن پلتفرم، کیمیا بیوتی را به‌عنوان نمونهٔ مصرف‌کننده متصل کنید.

## قاعدهٔ نگهداری

رنگ و فونت را فقط در منبع مشترک تغییر دهید و با `tools/sync-design.mjs`
در سه رابط همگام کنید. قابلیت و دادهٔ هر ماژول در مخزن خودش باقی می‌ماند.
نسخه‌های قدیمی را بدون بررسی تغییرات اختصاصی‌شان حذف یا بازنشانی نکنید.
