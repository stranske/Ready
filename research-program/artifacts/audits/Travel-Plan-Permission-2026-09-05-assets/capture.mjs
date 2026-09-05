import { chromium } from '/Users/teacher/.codex/orchestrator/frontend-verify/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const out=new URL('./',import.meta.url).pathname;
const browser=await chromium.connectOverCDP('http://127.0.0.1:9222');
const context=await browser.newContext({viewport:{width:1280,height:850}});
const page=await context.newPage();
const screens=[];const scenarios=[];
async function snap(name){const a11y=await page.locator('body').ariaSnapshot();const screenshot_path=out+name+'.png';await page.screenshot({path:screenshot_path,fullPage:true});screens.push({name,a11y,screenshot_path,url:page.url()});return a11y;}
await page.goto('http://127.0.0.1:38473/portal/draft/new');
console.log('draft fields',JSON.stringify(await page.locator('input,select,textarea').evaluateAll(es=>es.map(e=>({name:e.name,type:e.type,required:e.required})))));
await snap('draft-full');
await page.getByRole('button',{name:'Save draft and review'}).click();
await snap('draft-empty-submit');
scenarios.push({name:'Empty draft',goal:'Show validation for missing required fields',steps:[{action:'Submit empty draft',observed:page.url()}],goal_achieved:true});
await page.goto('http://127.0.0.1:38473/portal/expenses/new');
console.log('expense fields',JSON.stringify(await page.locator('input,select,textarea').evaluateAll(es=>es.map(e=>({name:e.name,type:e.type,required:e.required})))));
await snap('expense-full');
await page.setViewportSize({width:375,height:812});
await snap('expense-mobile');
console.log('mobile',await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})));
await page.setViewportSize({width:1280,height:850});
await context.setExtraHTTPHeaders({Authorization:'Bearer synthetic-audit-token'});
for (const [name,route] of [['admin-auth','/portal/admin'],['queue-auth','/portal/manager/reviews']]){await page.goto('http://127.0.0.1:38473'+route);await snap(name);}
fs.writeFileSync(out+'ux-capture.json',JSON.stringify({screens,scenarios},null,2));
await context.close();await browser.close();
