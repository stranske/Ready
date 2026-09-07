import {chromium} from '/Users/teacher/.codex/orchestrator/frontend-verify/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const out='/Users/teacher/.codex/automations/research-program/artifacts/audits/paem-20260907';
const browser=await chromium.connectOverCDP('http://127.0.0.1:9237');
const context=await browser.newContext({viewport:{width:1365,height:900}});
const page=await context.newPage();
const records=JSON.parse(fs.readFileSync(`${out}/browser-flows.json`));
async function capture(name,goal,achieved){
 const a11y=await page.locator('body').ariaSnapshot();
 const screenshot_path=`${out}/${name}.png`;
 await page.screenshot({path:screenshot_path,fullPage:true});
 fs.writeFileSync(`${out}/${name}-a11y.txt`,a11y);
 records.push({name,goal,goal_achieved:achieved,a11y,screenshot_path,url:page.url()});
 fs.writeFileSync(`${out}/browser-flows.json`,JSON.stringify(records,null,2));
}
for(const path of []){
 await page.goto(`http://127.0.0.1:8537/${path}`); await page.waitForTimeout(1800);
 await capture(path+'-initial','Open primary surface',await page.locator('[data-testid="stException"]').count()===0);
}
await page.goto('http://127.0.0.1:8537/Asset_Library');
await page.getByText('Use bundled sample asset data (no upload needed)',{exact:true}).first().click();
await page.waitForTimeout(1200); await capture('asset-sample','Load bundled asset sample',await page.locator('[data-testid="stException"]').count()===0);
await page.goto('http://127.0.0.1:8537/Stress_Lab');
await page.getByText('Use bundled sample data (no upload needed)',{exact:true}).first().click();
await page.getByRole('button',{name:'Run stress test',exact:true}).click();
await page.getByText('Summary (Base vs Stressed)',{exact:true}).waitFor({timeout:45000});
await page.getByRole('button',{name:'Download stress results (Excel)',exact:true}).waitFor({timeout:45000});
await capture('stress-run','Run bundled default stress comparison and expose exports',true);
await context.close(); await browser.close();
