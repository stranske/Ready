import {chromium} from '/Users/teacher/.codex/orchestrator/frontend-verify/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const out=new URL('./',import.meta.url).pathname;
const browser=await chromium.connectOverCDP('http://127.0.0.1:9222');const context=await browser.newContext();const page=await context.newPage();
const data=JSON.parse(fs.readFileSync(out+'synthetic-trip.json','utf8'));
const capture=JSON.parse(fs.readFileSync(out+'ux-capture.json','utf8'));
await page.goto('http://127.0.0.1:38473/portal/draft/new');
for(const [name,value] of Object.entries(data)){const field=page.locator('[name="'+name+'"]');if(!await field.count())continue;const tag=await field.evaluate(e=>e.tagName);if(tag==='SELECT')await field.selectOption(String(value));else await field.fill(String(value));}
await page.getByRole('button',{name:'Save draft and review'}).click();await page.waitForLoadState('networkidle');
let a11y=await page.locator('body').ariaSnapshot();await page.screenshot({path:out+'anonymous-draft-result.png',fullPage:true});
capture.screens.push({name:'anonymous-draft-result',a11y,screenshot_path:out+'anonymous-draft-result.png',url:page.url()});
capture.scenarios.push({name:'Anonymous traveler draft',goal:'Save and review completed travel form',steps:[{action:'Complete all synthetic trip fields and click Save draft and review',observed:a11y}],goal_achieved:!a11y.includes('Missing bearer token')});
await context.setExtraHTTPHeaders({Authorization:'Bearer synthetic-audit-token'});await page.reload();
a11y=await page.locator('body').ariaSnapshot();await page.screenshot({path:out+'authenticated-draft-result.png',fullPage:true});capture.screens.push({name:'authenticated-draft-result',a11y,screenshot_path:out+'authenticated-draft-result.png',url:page.url()});
capture.scenarios.push({name:'Authenticated review control',goal:'Open the same saved draft with credentials',steps:[{action:'Inject synthetic token into test browser context and reload',observed:a11y}],goal_achieved:!a11y.includes('Missing bearer token')});
fs.writeFileSync(out+'ux-capture.json',JSON.stringify(capture,null,2));console.log(JSON.stringify(capture.scenarios));await context.close();await browser.close();
