#!/usr/bin/env node
'use strict';

// Read-only browser checks for an already populated, exact-state replay.
// Usage: node research/clockwork/browser_check.cjs REPLAY.html NEW_OUTPUT_DIR
// Install Playwright separately (CI pins 1.56.1); NODE_PATH may locate it.
// PLAYWRIGHT_CHROMIUM_EXECUTABLE optionally selects an installed Chromium.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

async function main() {
  const [inputArg, outputArg] = process.argv.slice(2);
  assert(inputArg && outputArg, 'Usage: browser_check.cjs REPLAY.html NEW_OUTPUT_DIR');
  const input = path.resolve(inputArg);
  const output = path.resolve(outputArg);
  const html = fs.readFileSync(input, 'utf8');
  assert(!html.includes('const DATA = /*__U24_DATA__*/ null;'), 'Replay data must be embedded; the empty template is not a test fixture');
  assert(!fs.existsSync(output), 'Browser evidence directory must be new');
  fs.mkdirSync(output, {recursive: true});

  const report = {
    schema_version: 'u24-clockwork-browser-check-v1',
    input_sha256: crypto.createHash('sha256').update(html).digest('hex'),
    playwright_version: require('playwright/package.json').version,
    scope: 'Rendering and replay controls; no new dynamics or physical validation',
    passed: false,
    checks: [],
    page_errors: [],
    console_errors: [],
    external_requests: [],
    screenshots: [],
  };
  let browser;
  let context;
  let page;
  const check = (name, details = {}) => {
    report.checks.push({name, passed: true, ...details});
    process.stdout.write('PASS ' + name + '\n');
  };
  const text = async selector => (await page.locator(selector).innerText()).trim();
  const scrub = async value => {
    await page.locator('#scrub').evaluate((element, step) => {
      element.value = String(step);
      element.dispatchEvent(new Event('input', {bubbles: true}));
    }, value);
    assert.equal(await text('#time'), String(value), 'Time label must match the selected recorded frame');
  };
  const selectScenario = async value => {
    await page.locator('#scenario').selectOption(String(value));
    assert.equal(await text('#time'), '0', 'Changing scenario must load its initial state');
  };
  const selectSite = async value => page.locator('#site').selectOption(String(value));
  const assertTriples = async (first, second) => {
    assert.deepEqual(await page.locator('#twins .counter-values').nth(0).locator('b').allTextContents(), first.map(String));
    assert.deepEqual(await page.locator('#twins .counter-values').nth(1).locator('b').allTextContents(), second.map(String));
    assert.equal(await page.locator('#twins .gear').nth(0).getAttribute('aria-label'), 'Six-position remainder gear, r ' + first[2]);
    assert.equal(await page.locator('#twins .gear').nth(1).getAttribute('aria-label'), 'Six-position remainder gear, r ' + second[2]);
  };
  const checkWidth = async (name, width, height) => {
    await page.setViewportSize({width, height});
    const dimensions = await page.evaluate(() => ({
      body: document.body.scrollWidth,
      document: document.documentElement.scrollWidth,
      viewport: document.documentElement.clientWidth,
    }));
    assert(dimensions.body <= dimensions.viewport + 1, `${name}: body must not overflow horizontally (${JSON.stringify(dimensions)})`);
    assert(dimensions.document <= dimensions.viewport + 1, `${name}: document must not overflow horizontally (${JSON.stringify(dimensions)})`);
    check(name + ' has no body overflow', dimensions);
  };

  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox'],
      ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? {executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE} : {}),
    });
    report.browser_version = browser.version();
    context = await browser.newContext({
      viewport: {width: 1440, height: 1100},
      reducedMotion: 'reduce',
      recordVideo: {dir: path.join(output, 'video'), size: {width: 1440, height: 1100}},
    });
    page = await context.newPage();
    page.setDefaultTimeout(10000);
    page.on('pageerror', error => report.page_errors.push(String(error)));
    page.on('console', message => {if (message.type() === 'error') report.console_errors.push(message.text());});
    await page.route('**/*', route => {
      const url = route.request().url();
      if (/^https?:/i.test(url)) {
        report.external_requests.push(url);
        return route.abort();
      }
      return route.continue();
    });
    await page.goto(pathToFileURL(input).href, {waitUntil: 'load'});
    assert(await page.locator('#app').isVisible(), 'Populated replay must render the app');
    assert(!(await page.locator('#empty').isVisible()), 'Populated replay must not display the empty-template warning');
    const options = await page.locator('#scenario option').allTextContents();
    assert.equal(options.length, 7, 'Frozen replay protocol has seven scenarios');
    for (let index = 0; index < options.length; index++) {
      await selectScenario(index);
      assert.equal(await text('#run-title'), options[index]);
      assert(await page.locator('#rail .site-glyph').count() >= 25, 'Each scenario must display the whole prepared guide projection');
      const last = Number(await page.locator('#scrub').getAttribute('max'));
      assert(last >= 56, 'Frozen replay scenarios retain the declared horizon');
      await scrub(Math.floor(last / 2));
      assert.match(await text('#digest'), /^[a-f0-9]{64}$/, 'Every rendered frame must expose its complete-state SHA-256');
      await scrub(last);
      assert(await page.locator('#forward').isDisabled(), 'Next-step button must stop at the retained horizon');
      await page.locator('#restart').click();
      assert.equal(await text('#time'), '0');
      assert(await page.locator('#back').isDisabled(), 'Previous-step button must stop at the initial frame');
    }
    check('All seven scenarios load, scrub and reset', {scenario_titles: options});

    await selectScenario(0);
    await selectSite(6);
    await scrub(6);
    assert.equal(await text('#memory-bit'), '1');
    assert(await page.locator('#click-tag').isVisible(), 'Receiver 6 must have a readout rising edge at t=6');
    await assertTriples([0, 1, 0], [0, -1, 4]);
    assert.equal((await text('#formula')).replace(/\s+/g, ' '), '2 × 1 + 4 = 6 × 1 + 0');
    assert.equal(await text('#old-state'), '(0, 0, 4)');
    assert.equal(await text('#new-state'), '(0, 1, 0)');
    check('Receiver 6 at t=6 displays the exact counters, gears and Rule3 identity');

    await page.locator('#forward').click();
    assert.equal(await text('#time'), '7');
    await assertTriples([1, 0, 0], [-1, 0, 4]);
    assert.equal((await text('#formula')).replace(/\s+/g, ' '), '2 × 0 + 0 = 6 × 0 + 0');
    assert(!(await page.locator('#click-tag').isVisible()), 'A maintained memory bit is not another rising edge');
    await page.locator('#back').click();
    assert.equal(await text('#time'), '6');
    await page.locator('#speed').selectOption('8');
    await page.locator('#play').click();
    await page.waitForFunction(() => Number(document.getElementById('time').textContent) > 6);
    await page.locator('#play').click();
    assert.equal(await text('#play'), 'Play');
    const paused = await text('#time');
    // Two 8-step/s intervals establish that pause actually stops the timer.
    await page.waitForTimeout(300);
    assert.equal(await text('#time'), paused);
    check('Forward, backward, playback speed, play and pause operate on recorded frames');

    await selectScenario(5);
    await selectSite(12);
    await scrub(32);
    assert.match(await text('#outcome'), /Declared criterion failed/);
    assert(await page.locator('#outcome').isVisible());
    assert.match(await page.locator('#outcome').getAttribute('class'), /failed/);
    assert.equal(await text('#memory-bit'), '1');
    assert(await page.locator('#click-tag').isVisible());
    await assertTriples([0, 1, 0], [0, -1, 4]);
    check('Failed gap-control criterion stays visible when delayed activation reaches receiver 12 at t=32');

    await selectScenario(6);
    await selectSite(6);
    await scrub(6);
    assert.equal(await text('#memory-bit'), '0');
    await assertTriples([0, 1, 1], [0, -1, 4]);
    assert(!(await page.locator('#click-tag').isVisible()));
    assert.match(await text('#outcome'), /limitation/);
    assert.doesNotMatch(await page.locator('#twins .dial').nth(0).getAttribute('aria-label'), /at rest/);
    check('Odd-remainder control shows an active counter clock with the fixed memory bit still zero');

    await selectScenario(3);
    await selectSite(6);
    await scrub(20);
    assert.equal(await text('#memory-bit'), '0');
    await assertTriples([0, 0, 4], [0, 0, 0]);
    const dialLabels = await page.locator('#twins .dial').evaluateAll(nodes => nodes.map(node => node.getAttribute('aria-label')));
    assert(dialLabels.every(label => label.includes('at rest')));
    const guideLabels = await page.locator('#rail .site-glyph').evaluateAll(nodes => nodes.map(node => node.getAttribute('aria-label')));
    assert(guideLabels.every(label => /a 0, b 0,/.test(label)), 'No-source guide counters must remain zero');
    check('No-source preparation remains at rest at t=20 while remainder gears remain visible');

    await selectScenario(0);
    await selectSite(6);
    await scrub(12);
    await checkWidth('Desktop 1440px', 1440, 1100);
    await page.screenshot({path: path.join(output, 'desktop.png'), fullPage: true});
    report.screenshots.push('desktop.png');
    await checkWidth('Mobile 390px', 390, 844);
    await page.screenshot({path: path.join(output, 'mobile.png'), fullPage: true});
    report.screenshots.push('mobile.png');
    await checkWidth('Narrow mobile 360px', 360, 800);

    assert.deepEqual(report.page_errors, [], 'Replay must have no uncaught JavaScript errors');
    assert.deepEqual(report.console_errors, [], 'Replay must have no browser console errors');
    assert.deepEqual(report.external_requests, [], 'Replay must work without external network resources');
    check('No JavaScript errors, console errors or external resource requests');
    report.passed = true;
  } catch (error) {
    report.failure = {name: error.name, message: error.message, stack: error.stack};
    if (page) {
      try {
        await page.screenshot({path: path.join(output, 'failure.png'), fullPage: true});
        report.screenshots.push('failure.png');
      } catch (captureError) {
        report.failure_screenshot_error = String(captureError);
      }
    }
    throw error;
  } finally {
    if (context) await context.close();
    if (browser) await browser.close();
    fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n', {flag: 'wx'});
    process.stdout.write('Browser evidence: ' + output + '\n');
  }
}

main().catch(error => {
  process.stderr.write(String(error.stack || error) + '\n');
  process.exitCode = 1;
});
