// Verify real local navigation between independently running UIs. No API fixtures.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {mkdir} from 'node:fs/promises';
const require=createRequire(new URL('../apps/console/package.json',import.meta.url));
const {chromium}=require('playwright');
const screenshotRoot=process.env.SMARTCORE_SCREENSHOTS;
if(screenshotRoot)await mkdir(screenshotRoot,{recursive:true});
const browser=await chromium.launch({headless:true});
try{
  for(const locale of ['fa','en']){
    const context=await browser.newContext({viewport:{width:1440,height:1000}});
    const page=await context.newPage();const faults=[];const accountRequests=[];
    page.on('pageerror',error=>faults.push(error.message));
    page.on('request',request=>{if(new URL(request.url()).pathname.startsWith('/bff/'))accountRequests.push(request.url());});
    await page.goto(`http://127.0.0.1:4100/${locale}`);
    const token=await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--sc-primary').trim());
    await page.locator('.hero-actions a.button').click();await page.waitForURL(`http://127.0.0.1:4101/${locale}`);
    await page.locator('fieldset:disabled').waitFor();
    assert.equal(await page.locator('html').getAttribute('lang'),locale);
    assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--sc-primary').trim()),token);
    await page.evaluate(()=>document.fonts.ready);
    if(screenshotRoot)await page.screenshot({path:`${screenshotRoot}/identity-preview-${locale}.png`,fullPage:true});
    assert.deepEqual(accountRequests,[],'Disabled account preview dispatches no BFF requests');
    await page.locator('.platform-return').click();await page.waitForURL(`http://127.0.0.1:4100/${locale}`);
    await page.goto(`http://127.0.0.1:4100/${locale}/modules/business`);
    await page.locator('.module-detail a.button').click();await page.waitForURL(`http://127.0.0.1:4102/${locale}`);
    assert.equal(await page.locator('html').getAttribute('lang'),locale);
    assert.equal(await page.locator('html').getAttribute('dir'),locale==='fa'?'rtl':'ltr');
    assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--sc-primary').trim()),token);
    await page.locator('nav a[href$="/service-categories"]').click();await page.waitForURL(`http://127.0.0.1:4102/${locale}/service-categories`);
    assert.equal(await page.locator('nav a[aria-current=page]').getAttribute('href'),`/${locale}/service-categories`);
    await page.evaluate(()=>document.fonts.ready);
    if(screenshotRoot)await page.screenshot({path:`${screenshotRoot}/business-${locale}.png`,fullPage:true});
    await page.getByRole('link',{name:locale==='fa'?'EN':'FA',exact:true}).click();await page.waitForURL(`http://127.0.0.1:4102/${locale==='fa'?'en':'fa'}/service-categories`);
    for(const width of [390,320]){
      await page.setViewportSize({width,height:844});
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Business overflow ${locale}/${width}`);
    }
    if(screenshotRoot)await page.screenshot({path:`${screenshotRoot}/business-mobile-${locale}.png`,fullPage:true});
    await page.goto(`http://127.0.0.1:4101/${locale}`);
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Identity preview overflow ${locale}`);
    assert.deepEqual(faults,[],'No cross-app runtime errors');
    await context.close();
  }
  console.log('PASS: real console → Identity → console → Business navigation, shared design tokens/fonts, disabled preview makes no BFF requests, fa/en document direction, categories route, locale-preserving navigation, 320/390px layouts. Backend services were not started or simulated.');
}finally{await browser.close();}
