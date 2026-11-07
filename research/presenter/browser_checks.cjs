#!/usr/bin/env node
'use strict';

// Generic browser acceptance: expected arithmetic is computed directly from
// fixtures here, independently of PresenterData and of the displayed values.
// node research/presenter/browser_checks.cjs PRESENTER.html NEW_OUTPUT_DIR [FIXTURE_DIR]
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');

const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const wrap = (n, side) => (n % side + side) % side;
const addressKey = address => address.join(',');
const clone = value => JSON.parse(JSON.stringify(value));
const exact = value => BigInt(value).toString();

function storedMap(experiment, index) {
  return new Map(experiment.frames[index].cells.map(row => [addressKey(row.slice(0, 4)), row.slice(4)]));
}
function at(experiment, index, address) {
  const row = storedMap(experiment, index).get(addressKey(address)) || experiment.background;
  return [BigInt(row[0]), BigInt(row[1]), Number(row[2])];
}
function expectedTransition(experiment, index, address) {
  assert(index > 0);
  const old = at(experiment, index - 1, address);
  const next = at(experiment, index, address);
  const g = address[3];
  const inputs = experiment.coupling.directions.map((direction, d) => {
    const neighbor = [0, 1, 2].map(axis => wrap(address[axis] + direction[axis], experiment.side));
    neighbor.push(experiment.coupling.ports[d][g]);
    const b = at(experiment, index - 1, neighbor)[1];
    const weight = experiment.coupling.weights[d][g];
    return {address: neighbor, weight, b, product: BigInt(weight) * b};
  });
  const u = inputs.reduce((sum, input) => sum + input.product, 0n);
  const numerator = 2n * u + BigInt(old[2]);
  // JavaScript division truncates toward zero; Rule3 requires floor division.
  let quotient = numerator / 6n;
  let remainder = numerator % 6n;
  if (remainder < 0n) {quotient -= 1n; remainder += 6n;}
  assert.deepEqual(next, [old[1], quotient - old[0], Number(remainder)], 'The browser fixture itself must satisfy Rule3');
  return {old, next, u, numerator, quotient, remainder, inputs};
}
function negativeTransition(experiment) {
  // Search all affected sites/channels, not only a demo's preselected channel.
  const candidates = new Set();
  for (const frame of experiment.frames) {
    for (const row of frame.cells) {
      for (const delta of [[0, 0, 0], ...experiment.coupling.directions]) {
        const position = [0, 1, 2].map(axis => wrap(row[axis] + delta[axis], experiment.side));
        for (let g = 0; g < 48; g++) candidates.add(addressKey([...position, g]));
      }
    }
  }
  for (let index = 1; index < experiment.frames.length; index++) {
    for (const key of candidates) {
      const address = key.split(',').map(Number);
      const transition = expectedTransition(experiment, index, address);
      if (transition.u < 0n && transition.numerator < 0n && transition.remainder > 0n) {
        return {index, address, transition};
      }
    }
  }
  throw new Error('Unseen fixture must include a negative, nondivisible Rule3 numerator');
}
function readoutValues(experiment, index) {
  return (experiment.readouts || []).map(readout => {
    const valueAt = frame => readout.clauses.every(clause => {
      const triple = at(experiment, frame, clause.address);
      const component = {a: 0, b: 1, r: 2}[clause.component];
      return BigInt(triple[component]) === BigInt(clause.equals);
    });
    const value = valueAt(index);
    return {id: readout.id, value, edge: index > 0 && value && !valueAt(index - 1)};
  });
}

async function main() {
  const {chromium} = require('playwright');
  const [inputArg, outputArg, fixturesArg] = process.argv.slice(2);
  assert(inputArg && outputArg, 'Usage: browser_checks.cjs PRESENTER.html NEW_OUTPUT_DIR [FIXTURE_DIR]');
  const input = path.resolve(inputArg);
  const output = path.resolve(outputArg);
  const fixtures = path.resolve(fixturesArg || path.join(__dirname, 'fixtures'));
  const manifest = JSON.parse(fs.readFileSync(path.join(fixtures, 'browser_manifest.json'), 'utf8'));
  const file = name => path.join(fixtures, manifest[name]);
  const fixtureText = name => fs.readFileSync(file(name), 'utf8');
  const unseenBundle = JSON.parse(fixtureText('unseen_bundle'));
  const unseen = unseenBundle.experiments[0];
  const hugeBundle = JSON.parse(fixtureText('huge_bundle'));
  const huge = hugeBundle.experiments[0];
  const html = fs.readFileSync(input, 'utf8');
  assert(!fs.existsSync(output), 'Browser evidence directory must be new');
  fs.mkdirSync(output, {recursive: true});
  const report = {
    format: 'universe24-presenter-browser-check-v1',
    input_sha256: sha(html),
    test_source_sha256: sha(fs.readFileSync(__filename)),
    node_version: process.version,
    playwright_version: require('playwright/package.json').version,
    fixture_sha256: Object.fromEntries(Object.entries(manifest).map(([name, filename]) => [name, sha(fs.readFileSync(path.join(fixtures, filename)))])),
    scope: 'Generic rendering, exact inspection, local imports and navigation; no dynamics changes or physical validation',
    passed: false,
    execution_status: 'not_started',
    checks: [], page_errors: [], console_errors: [], external_requests: [], screenshots: [],
  };
  let browser, context, page;
  const check = (name, details = {}) => {
    report.checks.push({name, passed: true, ...details});
    process.stdout.write('PASS ' + name + '\n');
  };
  const text = async selector => (await page.locator(selector).textContent()).trim();
  const numeric = async selector => page.locator(selector).evaluate(element => {
    const value = /^(INPUT|TEXTAREA)$/.test(element.tagName) ? element.value : element.textContent;
    return value.trim();
  });
  const loaded = async () => {
    await page.waitForFunction(() => globalThis.PresenterUI && PresenterUI.experiment && document.getElementById('loading').hidden);
  };
  const openInspector = async () => {
    if (!(await page.locator('#node-x').isVisible())) await page.locator('#inspect').click();
  };
  const openEvidence = async () => {
    await openInspector();
    if (!(await page.locator('#counter-a').isVisible())) await page.locator('#show-evidence').click();
  };
  const closeDetails = async () => {
    if (await page.locator('#close-evidence').isVisible()) await page.locator('#close-evidence').click();
    if (await page.locator('#close-inspector').isVisible()) await page.locator('#close-inspector').click();
  };
  const retainedState = async () => page.evaluate(() => JSON.stringify({
    frames: PresenterUI.experiment.frames,
    coupling: PresenterUI.experiment.coupling,
    readouts: PresenterUI.experiment.readouts,
  }, (_key, value) => typeof value === 'bigint' ? value.toString() : value));
  const scrub = async index => {
    await page.locator('#scrub').evaluate((element, value) => {
      element.value = String(value);
      element.dispatchEvent(new Event('input', {bubbles: true}));
    }, index);
    await page.waitForFunction(value => PresenterUI.frameIndex === value, index);
  };
  const selectExperiment = async index => {
    const value = await page.locator('#experiment option').nth(index).getAttribute('value');
    await page.locator('#experiment').selectOption(value);
    await page.waitForFunction(() => PresenterUI.frameIndex === 0);
  };
  const selectAddress = async address => {
    if (await page.locator('#close-evidence').isVisible()) await page.locator('#close-evidence').click();
    await openInspector();
    for (const [axis, value] of ['x', 'y', 'z'].map((axis, i) => [axis, address[i]])) {
      await page.locator('#node-' + axis).fill(String(value));
    }
    await page.locator('#go-node').click();
    await page.locator('#channel-select').selectOption(String(address[3]));
    await page.waitForFunction(addr => JSON.stringify(PresenterUI.selection) === JSON.stringify({position: addr.slice(0, 3), channel: addr[3]}), address);
  };
  const assertTriple = async triple => {
    await openEvidence();
    assert.equal(await numeric('#counter-a'), exact(triple[0]), 'The complete a integer must be available in the UI');
    assert.equal(await numeric('#counter-b'), exact(triple[1]), 'The complete b integer must be available in the UI');
    assert.equal(await numeric('#remainder'), String(triple[2]));
    assert.equal(await numeric('#theta'), String(Math.floor(Number(triple[2]) / 2)));
    assert.equal(await numeric('#parity'), String(Number(triple[2]) % 2));
  };
  const importBundle = async (name, bundle) => {
    await page.locator('#file-input').setInputFiles({name, mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(bundle))});
    await page.waitForFunction(id => globalThis.PresenterUI && PresenterUI.experiment && PresenterUI.experiment.id === id && document.getElementById('loading').hidden, bundle.experiments[0].id);
    assert(!(await page.locator('#error').isVisible()), 'Valid imported data must not leave an error banner');
  };
  const checkWidth = async (name, width, height) => {
    await page.setViewportSize({width, height});
    const dimensions = await page.evaluate(() => ({body: document.body.scrollWidth, document: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth}));
    assert(dimensions.body <= dimensions.viewport + 1 && dimensions.document <= dimensions.viewport + 1, `${name} must not overflow horizontally: ${JSON.stringify(dimensions)}`);
    check(name + ' has no body overflow', dimensions);
  };
  const assertNoInvalidGeometry = async () => {
    const invalid = await page.locator('svg').evaluateAll(nodes => nodes.some(node => /(?:NaN|Infinity)/.test(node.outerHTML)));
    assert(!invalid, 'Clock geometry must stay finite even when counters exceed Number range');
    const canvases = await page.locator('canvas').evaluateAll(nodes => nodes.map(node => ({width: node.width, height: node.height})));
    assert(canvases.every(canvas => Number.isFinite(canvas.width) && Number.isFinite(canvas.height)), 'Canvas dimensions must stay finite');
  };

  try {
    browser = await chromium.launch({headless: true, args: ['--no-sandbox'], ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? {executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE} : {})});
    report.browser_version = browser.version();
    report.execution_status = 'running';
    context = await browser.newContext({viewport: {width: 1440, height: 1100}, hasTouch: true, reducedMotion: 'reduce', recordVideo: {dir: path.join(output, 'video'), size: {width: 1440, height: 1100}}});
    page = await context.newPage();
    page.setDefaultTimeout(20000);
    page.on('pageerror', error => report.page_errors.push(String(error)));
    page.on('console', message => {if (message.type() === 'error') report.console_errors.push(message.text());});
    await page.route('**/*', route => {
      const url = route.request().url();
      if (/^https?:/i.test(url)) {report.external_requests.push(url); return route.abort();}
      return route.continue();
    });
    await page.goto(pathToFileURL(input).href, {waitUntil: 'load'});
    await loaded();
    assert(!(await page.locator('#node-x').isVisible()), 'The initial view must keep the all-channel inspector optional');
    assert(!(await page.locator('#counter-a').isVisible()), 'Exact arithmetic must remain optional in the initial cube view');
    await page.screenshot({path: path.join(output, 'initial-cube.png'), fullPage: true});
    report.screenshots.push('initial-cube.png');
    check('The initial view is a simple cube with details opened on demand');
    const demos = await page.evaluate(() => PRESENTER_BUNDLE.experiments.map(experiment => ({id: experiment.id, frames: experiment.frames.length, steps: experiment.frames.map(frame => frame.step)})));
    assert(demos.length >= 3, 'Show several structurally different bundled experiments');
    assert(!demos.some(experiment => experiment.id === unseen.id || experiment.id === huge.id), 'Import fixtures must not be members of the built-in demo collection');
    for (let index = 0; index < demos.length; index++) {
      await selectExperiment(index);
      assert.equal(await page.locator('#channel-grid button[data-channel]').count(), 48, 'Every selected node exposes all 48 channels');
      await scrub(demos[index].frames - 1);
      assert.equal(await numeric('#step'), String(demos[index].steps.at(-1)));
      assert.match(await text('#state-hash'), /^[a-f0-9]{64}$/);
      assert(await page.locator('#next').isDisabled());
      await page.locator('#rewind').click();
      assert.equal(await page.evaluate(() => PresenterUI.frameIndex), 0);
    }
    check('Every bundled experiment exposes a complete 48-channel node and its full recorded timeline', {experiments: demos.map(experiment => experiment.id)});

    const playbackIndex = demos.findIndex(experiment => experiment.frames >= 5);
    assert(playbackIndex >= 0, 'At least one demonstration needs a playback horizon');
    await selectExperiment(playbackIndex);
    await page.locator('#next').click();
    assert.equal(await page.evaluate(() => PresenterUI.frameIndex), 1);
    await page.locator('#prev').click();
    assert.equal(await page.evaluate(() => PresenterUI.frameIndex), 0);
    const speeds = await page.locator('#speed option').evaluateAll(options => options.map(option => option.value));
    const playbackRate = speeds.includes('2') ? '2' : speeds[0];
    await page.locator('#speed').selectOption(playbackRate);
    await page.locator('#play').click();
    await page.waitForFunction(() => PresenterUI.frameIndex > 0);
    await page.locator('#play').click();
    const stopped = await page.evaluate(() => PresenterUI.frameIndex);
    await page.waitForTimeout(Math.max(300, 1100 / Number(playbackRate)));
    assert.equal(await page.evaluate(() => PresenterUI.frameIndex), stopped, 'Pause must stop recorded-frame advancement');
    check('Playback, stepping, speed and pause work on recorded states');

    await importBundle('unseen-experiment.json', unseenBundle);
    const row47 = unseen.frames[0].cells.find(row => row[3] === 47);
    assert(row47, 'Unseen fixture must prepare channel 47');
    await selectAddress(row47.slice(0, 4));
    await page.locator('#channel-grid button[data-channel="47"]').click();
    assert.match(await text('#selected-channel'), /47/);
    await assertTriple(row47.slice(4));
    const channelNumbers = await page.locator('#channel-grid button[data-channel]').evaluateAll(buttons => buttons.map(button => Number(button.dataset.channel)).sort((a, b) => a - b));
    assert.deepEqual(channelNumbers, Array.from({length: 48}, (_, i) => i));
    check('An unseen imported geometry and channel 47 render without a channel-pair or guide assumption', {side: unseen.side, signs: unseen.coupling.body_signs, address: row47.slice(0, 4)});

    const negative = negativeTransition(unseen);
    await scrub(negative.index);
    await selectAddress(negative.address);
    await assertTriple(negative.transition.next);
    assert.equal(await numeric('#algebra-u'), negative.transition.u.toString());
    assert.equal(await numeric('#algebra-numerator'), negative.transition.numerator.toString());
    assert.equal(await numeric('#algebra-quotient'), negative.transition.quotient.toString());
    assert.equal(await numeric('#algebra-remainder'), negative.transition.remainder.toString());
    const neighborButtons = page.locator('#neighbor-list button[data-neighbor]');
    assert.equal(await neighborButtons.count(), 6, 'Every inspected channel shows exactly six signed spatial input ports');
    for (let d = 0; d < 6; d++) {
      const button = neighborButtons.nth(d);
      const address = JSON.parse(await button.getAttribute('data-address'));
      assert.deepEqual(address, negative.transition.inputs[d].address);
      const row = button.locator('xpath=ancestor::*[contains(concat(" ",normalize-space(@class)," ")," neighbor ")][1]');
      assert.equal((await row.locator('.neighbor-value').textContent()).trim(), negative.transition.inputs[d].b.toString());
      assert.equal((await row.locator('.neighbor-product').textContent()).trim(), negative.transition.inputs[d].product.toString());
    }
    await neighborButtons.nth(0).click();
    assert.deepEqual(await page.evaluate(() => PresenterUI.selection), {position: negative.transition.inputs[0].address.slice(0, 3), channel: negative.transition.inputs[0].address[3]});
    check('Six signed neighbors, negative Euclidean quotient/remainder and neighbor navigation match an independent BigInt calculation', {selected_address: negative.address, frame: negative.index, u: negative.transition.u.toString()});

    const fixedBefore = await page.locator('#readouts [data-readout]').evaluateAll(nodes => nodes.map(node => ({id: node.dataset.readout, value: node.dataset.value, edge: node.dataset.edge})));
    assert(fixedBefore.length > 0, 'Unseen fixture must declare at least one fixed generic readout');
    const expectedReadouts = readoutValues(unseen, negative.index);
    for (const expected of expectedReadouts) {
      const actual = fixedBefore.find(readout => readout.id === expected.id);
      assert(actual, 'Every declared observer remains visible');
      assert.equal(['1', 'true'].includes(actual.value), expected.value);
      assert.equal(['1', 'true'].includes(actual.edge), expected.edge);
    }
    const digestBefore = await text('#state-hash');
    const completeBefore = await retainedState();
    let empty;
    const occupied = new Set(unseen.frames[negative.index].cells.map(row => addressKey(row.slice(0, 4))));
    for (let x = 0; x < unseen.side && !empty; x++) {
      for (let y = 0; y < unseen.side && !empty; y++) {
        const candidate = [x, y, 0, 46];
        if (!occupied.has(addressKey(candidate))) empty = candidate;
      }
    }
    assert(empty, 'Fixture must contain at least one background address');
    await selectAddress(empty);
    await assertTriple(unseen.background);
    await closeDetails();
    const cameraBefore = await page.evaluate(() => PresenterUI.camera);
    assert(cameraBefore && ['yaw', 'pitch', 'zoom'].every(key => Number.isFinite(cameraBefore[key])), 'The displayed camera must expose finite coordinates');
    const cube = await page.locator('#space-canvas').boundingBox();
    assert(cube && cube.width > 100 && cube.height > 100, 'The main cube must have a useful visible area');
    await page.mouse.move(cube.x + cube.width * .45, cube.y + cube.height * .45);
    await page.mouse.down();
    await page.mouse.move(cube.x + cube.width * .64, cube.y + cube.height * .6, {steps: 8});
    await page.mouse.up();
    const cameraDragged = await page.evaluate(() => PresenterUI.camera);
    assert(cameraDragged.yaw !== cameraBefore.yaw || cameraDragged.pitch !== cameraBefore.pitch, 'Dragging the cube must rotate its camera');
    await page.mouse.wheel(0, -160);
    await page.waitForFunction(zoom => PresenterUI.camera.zoom !== zoom, cameraDragged.zoom);
    const cameraZoomed = await page.evaluate(() => PresenterUI.camera);
    assert(['yaw', 'pitch', 'zoom'].every(key => Number.isFinite(cameraZoomed[key])), 'Camera navigation must remain finite');
    assert.equal(await retainedState(), completeBefore, 'Camera rotation and zoom must not rotate the tensor or change frames or observers');
    await assertTriple(unseen.background);
    check('Mouse orbit and wheel zoom change the camera only', {before: cameraBefore, after: cameraZoomed, retained_sha256: sha(completeBefore)});
    await closeDetails();
    if (!(await page.locator('#projection').isVisible())) await page.locator('#view-options-toggle').click();
    for (const mode of ['iso', 'xy', 'xz', 'yz']) await page.locator('#projection').selectOption(mode);
    for (const filter of ['all', 'counters', 'remainders']) await page.locator('#field-filter').selectOption(filter);
    await page.locator('#focus-state').click();
    const focusedCamera = await page.evaluate(() => PresenterUI.camera);
    assert(['yaw', 'pitch', 'zoom'].every(key => Number.isFinite(focusedCamera[key])) && focusedCamera.center.every(Number.isFinite));
    assert.equal(await retainedState(), completeBefore, 'Focusing retained state must be display-only');
    await page.locator('#fit').click();
    const resetCamera = await page.evaluate(() => PresenterUI.camera);
    assert.equal(resetCamera.zoom, 1); assert.deepEqual(resetCamera.center, [.5, .5, .5]);
    const fixedAfter = await page.locator('#readouts [data-readout]').evaluateAll(nodes => nodes.map(node => ({id: node.dataset.readout, value: node.dataset.value, edge: node.dataset.edge})));
    assert.deepEqual(fixedAfter, fixedBefore, 'Viewport/channel changes must not redefine the fixed scientific observers');
    assert.equal(await text('#state-hash'), digestBefore, 'Display navigation must not alter a retained state');
    assert.equal(await retainedState(), completeBefore, 'Projections, filters and selected channels must not change any complete frame, tensor entry or readout');
    await assertTriple(unseen.background);
    check('Arbitrary background coordinates, all spatial projections and field filters preserve state and declared readouts');

    await importBundle('huge-counter.json', hugeBundle);
    const hugeRow = huge.frames[0].cells.find(row => String(row[4]).replace('-', '').length > 4300 || String(row[5]).replace('-', '').length > 4300);
    assert(hugeRow, 'Huge-integer fixture must exceed Python default decimal conversion limits and JS Number precision');
    await selectAddress(hugeRow.slice(0, 4));
    await assertTriple(hugeRow.slice(4));
    await assertNoInvalidGeometry();
    await checkWidth('Huge-integer desktop 1440px', 1440, 1100);
    await checkWidth('Huge-integer mobile 390px', 390, 844);
    check('More than 4,300 decimal digits stay exact and dials remain finite', {decimal_digits: Math.max(String(hugeRow[4]).replace('-', '').length, String(hugeRow[5]).replace('-', '').length)});

    // Native formats are imported through the actual file input, not the test API.
    for (const key of ['native_snapshot', 'native_trace']) {
      const source = fixtureText(key);
      const records = key === 'native_trace' ? source.trim().split(/\r?\n/).map(line => JSON.parse(line)) : [JSON.parse(source)];
      await page.locator('#file-input').setInputFiles(file(key));
      await page.waitForFunction(expected => PresenterUI.experiment && PresenterUI.experiment.frames.length === expected.length && PresenterUI.experiment.frames[0].step === expected.firstStep && document.getElementById('loading').hidden, {length: records.length, firstStep: records[0].completed_steps});
      const lastIndex = records.length - 1;
      await scrub(lastIndex);
      const cp = records[lastIndex];
      assert.equal(await numeric('#step'), String(cp.completed_steps));
      const change = cp.experiment.seed_changes.find(change => change.channel === 47) || cp.experiment.seed_changes[0];
      assert(change, 'Native fixture needs a nonbackground address');
      await selectAddress([...change.position, change.channel]);
      await assertTriple(change.state);
      if (lastIndex === 0) {
        assert(await page.locator('#next').isDisabled(), 'A snapshot must not invent later frames');
        assert.match(await text('#status'), /snapshot|no transition|0 transition/i);
      }
      check(key === 'native_trace' ? 'Native complete-checkpoint JSONL imports with absolute step indices' : 'A single native checkpoint opens as an honest snapshot');
    }

    const hostile = clone(unseenBundle);
    hostile.experiments[0].id = 'metadata-safety-fixture';
    hostile.experiments[0].title = '<img src=x onerror="globalThis.__presenterXSS=1">';
    hostile.experiments[0].description = '<script>globalThis.__presenterXSS=2</script>';
    await importBundle('metadata-safety.json', hostile);
    assert.equal(await page.evaluate(() => globalThis.__presenterXSS), undefined);
    assert.equal(await page.locator('img[src="x"]').count(), 0, 'Metadata must be rendered as text, not markup');
    const identityBefore = await page.evaluate(() => ({id: PresenterUI.experiment.id, selection: PresenterUI.selection, frameIndex: PresenterUI.frameIndex}));
    const malformed = [
      ['duplicate-keys.json', '{"format":"universe24-presenter-v1","format":"universe24-presenter-v1"}'],
      ['truncated.json', '{"format":"universe24-presenter-v1",'],
    ];
    const corrupted = clone(unseenBundle);
    corrupted.experiments[0].frames[1].cells[0][6] = (corrupted.experiments[0].frames[1].cells[0][6] + 1) % 6;
    malformed.push(['corrupted-state.json', JSON.stringify(corrupted)]);
    for (const [name, contents] of malformed) {
      await page.locator('#file-input').setInputFiles({name, mimeType: 'application/json', buffer: Buffer.from(contents)});
      await page.waitForFunction(() => !document.getElementById('error').hidden && document.getElementById('loading').hidden);
      assert(await page.locator('#error').isVisible());
      assert((await text('#error')).length > 0);
      assert.deepEqual(await page.evaluate(() => ({id: PresenterUI.experiment.id, selection: PresenterUI.selection, frameIndex: PresenterUI.frameIndex})), identityBefore, 'Rejected input must preserve the prior valid experiment and view');
    }
    assert.equal(await page.evaluate(() => globalThis.__presenterXSS), undefined);
    check('Hostile labels remain text; duplicate, truncated and corrupted imports are rejected without losing the valid experiment');

    await importBundle('unseen-final.json', unseenBundle);
    await scrub(negative.index);
    await selectAddress(negative.address);
    await closeDetails();
    if (!(await page.locator('#projection').isVisible())) await page.locator('#view-options-toggle').click();
    await page.locator('#projection').selectOption('iso');
    await page.locator('#field-filter').selectOption('all');
    await page.locator('#view-options-toggle').click();
    await closeDetails();
    await checkWidth('Desktop 1440px', 1440, 1100);
    await page.screenshot({path: path.join(output, 'desktop.png'), fullPage: true});
    report.screenshots.push('desktop.png');
    await checkWidth('Mobile 390px', 390, 844);
    await page.screenshot({path: path.join(output, 'mobile.png'), fullPage: true});
    report.screenshots.push('mobile.png');
    // Deliver a real emulated touch sequence through this local test browser;
    // synthetic DOM pointerdown cannot legitimately capture a native pointer.
    const touchBefore = await page.evaluate(() => PresenterUI.camera);
    const mobileCube = await page.locator('#space-canvas').boundingBox();
    const touchSession = await context.newCDPSession(page);
    await touchSession.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: mobileCube.x + 80, y: mobileCube.y + 80, id: 11}]});
    await touchSession.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: mobileCube.x + 130, y: mobileCube.y + 110, id: 11}]});
    await touchSession.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
    await touchSession.detach();
    const touchAfter = await page.evaluate(() => PresenterUI.camera);
    assert(touchAfter.yaw !== touchBefore.yaw || touchAfter.pitch !== touchBefore.pitch, 'Touch pointer dragging must rotate the cube');
    assert.equal(await retainedState(), completeBefore, 'Touch navigation must preserve all frames, tensor entries and readouts');
    check('Mobile touch pointer navigation preserves the complete experiment', {before: touchBefore, after: touchAfter});
    await openEvidence();
    await checkWidth('Expanded mobile inspector 390px', 390, 844);
    await page.screenshot({path: path.join(output, 'mobile-inspector.png'), fullPage: true});
    report.screenshots.push('mobile-inspector.png');
    await checkWidth('Narrow mobile 360px', 360, 800);
    await page.screenshot({path: path.join(output, 'mobile-360-inspector.png'), fullPage: true});
    report.screenshots.push('mobile-360-inspector.png');
    await assertNoInvalidGeometry();
    assert.deepEqual(report.page_errors, [], 'No uncaught application errors are permitted');
    assert.deepEqual(report.console_errors, [], 'No browser console errors are permitted');
    assert.deepEqual(report.external_requests, [], 'Presenter must work entirely offline');
    check('No page errors, console errors or external network dependencies');
    report.passed = true;
    report.execution_status = 'passed';
  } catch (error) {
    report.execution_status = browser ? 'failed' : 'browser_launch_failed';
    report.failure = {name: error.name, message: error.message, stack: error.stack};
    if (page) {
      try {await page.screenshot({path: path.join(output, 'failure.png'), fullPage: true}); report.screenshots.push('failure.png');}
      catch (captureError) {report.failure_capture_error = String(captureError);}
    }
    throw error;
  } finally {
    if (context) await context.close();
    if (browser) await browser.close();
    fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n', {flag: 'wx'});
    process.stdout.write('Browser evidence: ' + output + '\n');
  }
}

module.exports = {at, expectedTransition, negativeTransition, readoutValues};
if (require.main === module) main().catch(error => {process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1;});
