'use strict';
// Optional real-Chromium check of an unchanged, already exported Presenter.
// It never records or evolves the model. Browser launch failures are retained.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium:playwright} = require('playwright');
const chromium = require('@sparticuz/chromium');

async function main() {
  const [inputArg, outputArg] = process.argv.slice(2);
  assert(inputArg && outputArg, 'Usage: browser_smoke.cjs HTML NEW_OUTPUT_DIR');
  const input=path.resolve(inputArg), output=path.resolve(outputArg);
  fs.mkdirSync(output,{recursive:false});
  const hash=buffer=>crypto.createHash('sha256').update(buffer).digest('hex');
  const report={format:'universe24-clock-presenter-real-browser-smoke-v1',passed:false,
    input,input_sha256:hash(fs.readFileSync(input)),source_sha256:hash(fs.readFileSync(__filename)),
    node:process.version,errors:[],checks:[],scope:'Real headless Chromium only; no Safari, iPad or attachment-preview claim'};
  let browser;
  try {
    const executablePath=await chromium.executablePath();
    report.executable=executablePath;
    browser=await playwright.launch({executablePath,args:chromium.args,headless:true,timeout:20000});
    const page=await browser.newPage({viewport:{width:1280,height:900},deviceScaleFactor:1});
    page.on('pageerror',error=>report.errors.push(String(error)));
    await page.goto(pathToFileURL(input).href,{waitUntil:'load'});
    await page.waitForFunction(()=>window.PresenterUI?.experiment && document.querySelector('#loading').hidden,{timeout:20000});
    const options=await page.locator('#experiment option').evaluateAll(nodes=>nodes.map(n=>({id:n.value,title:n.textContent,disabled:n.disabled,hidden:n.hidden})));
    assert(options.length>0 && options.every(o=>!o.disabled&&!o.hidden));
    assert(await page.locator('#experiment').isVisible());
    report.selector_entries=options;
    for(const item of options) {
      await page.selectOption('#experiment',item.id);
      const initial=await page.evaluate(()=>({id:PresenterUI.experiment.id,frames:PresenterUI.experiment.frames.length,index:PresenterUI.frameIndex,hash:document.querySelector('#state-hash').textContent.trim()}));
      assert.equal(initial.id,item.id);assert.equal(initial.index,0);
      await page.locator('#scrub').fill(String(initial.frames-1));
      await page.locator('#scrub').dispatchEvent('input');
      const final=await page.evaluate(()=>({index:PresenterUI.frameIndex,hash:document.querySelector('#state-hash').textContent.trim(),expected:PresenterUI.experiment.frames.at(-1).state_sha256,channelButtons:document.querySelectorAll('#channel-grid button[data-channel]').length}));
      assert.equal(final.index,initial.frames-1);assert.equal(final.hash,final.expected);assert.equal(final.channelButtons,48);
      report.checks.push({id:item.id,complete_final_frame:true,all48channels:true});
    }
    await page.selectOption('#experiment',options[0].id);
    await page.screenshot({path:path.join(output,'desktop.png'),fullPage:true});
    await page.setViewportSize({width:820,height:1180});
    assert(await page.locator('#experiment').isVisible());
    await page.screenshot({path:path.join(output,'tablet-size.png'),fullPage:true});
    assert.deepEqual(report.errors,[]);report.passed=true;
  } catch(error) { report.failure={message:String(error.message),stack:String(error.stack)};process.exitCode=1; }
  finally { if(browser)await browser.close(); fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n'); }
  console.log(JSON.stringify({passed:report.passed,experiments:report.checks.length,failure:report.failure?.message?.slice(0,300)}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
