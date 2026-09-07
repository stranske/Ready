import {chromium} from '/Users/teacher/.codex/orchestrator/frontend-verify/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const out='/Users/teacher/.codex/automations/research-program/artifacts/audits/paem-20260907';
const browser=await chromium.connectOverCDP('http://127.0.0.1:9237');const context=await browser.newContext({viewport:{width:1365,height:900}});const page=await context.newPage();
async function snap(name){await page.waitForTimeout(1200);fs.writeFileSync(`${out}/${name}-a11y.txt`,await page.locator('body').ariaSnapshot());await page.screenshot({path:`${out}/${name}.png`,fullPage:true});}
await page.goto('http://127.0.0.1:8537/Scenario_Grid');await page.getByRole('tab',{name:'Compute from Config',exact:true}).click();await snap('grid-compute-tab');
await page.goto('http://127.0.0.1:8537/Asset_Library');await page.getByText('Use bundled sample asset data (no upload needed)',{exact:true}).first().click();await page.getByRole('spinbutton',{name:'Min observations per id',exact:true}).fill('24');await page.getByRole('spinbutton',{name:'Min observations per id',exact:true}).press('Enter');await snap('asset-min24-control');
await page.goto('http://127.0.0.1:8537/Portfolio_Builder');await page.getByRole('button',{name:'Load bundled sample portfolio',exact:true}).click();await snap('portfolio-sample');
await context.close();await browser.close();
