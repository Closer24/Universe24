#!/usr/bin/env node
'use strict';

// DOM + native Canvas2D integration, deliberately separate from browser checks.
// jsdom does not lay out CSS or implement browser pointer hit testing. We supply
// explicit element rectangles and ResizeObserver; PNGs are the application's
// actual Canvas2D output, not screenshots and not evidence of responsive layout.
// NODE_PATH=/path/to/scratch/deps/node_modules node dom_checks.cjs PRESENTER.html NEW_OUTPUT_DIR [FIXTURE_DIR]
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const {TextEncoder, TextDecoder} = require('node:util');
const {JSDOM, VirtualConsole} = require('jsdom');
const {createCanvas} = require('@napi-rs/canvas');
const {at, negativeTransition, readoutValues} = require('./browser_checks.cjs');

const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const copy = value => JSON.parse(JSON.stringify(value));
const same = (actual, expected, message) => assert.deepEqual(copy(actual), copy(expected), message);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
  const [htmlArg, outputArg, fixtureArg] = process.argv.slice(2);
  assert(htmlArg && outputArg, 'Usage: dom_checks.cjs PRESENTER.html NEW_OUTPUT_DIR [FIXTURE_DIR]');
  const input = path.resolve(htmlArg), output = path.resolve(outputArg);
  const fixtures = path.resolve(fixtureArg || path.join(__dirname, 'fixtures'));
  const manifest = JSON.parse(fs.readFileSync(path.join(fixtures, 'browser_manifest.json'), 'utf8'));
  const fixtureText = key => fs.readFileSync(path.join(fixtures, manifest[key]), 'utf8');
  const unseenBundle = JSON.parse(fixtureText('unseen_bundle')), unseen = unseenBundle.experiments[0];
  const hugeBundle = JSON.parse(fixtureText('huge_bundle')), huge = hugeBundle.experiments[0];
  const html = fs.readFileSync(input, 'utf8');
  assert(!fs.existsSync(output), 'Evidence directory must be new');
  fs.mkdirSync(output, {recursive: true});
  const report = {
    format: 'universe24-presenter-dom-native-canvas-check-v1', passed: false,
    scope: 'Actual application scripts in jsdom with native Canvas2D; explicit geometry emulation. PNGs composite the actual canvas on its declared solid CSS --navy background. No browser CSS layout, accessibility, hit-testing, responsive-layout, or full-page screenshot claim.',
    input_sha256: sha(html), dependencies: {jsdom: require('jsdom/package.json').version, canvas: require('@napi-rs/canvas/package.json').version},
    test_source_sha256: {dom_checks:sha(fs.readFileSync(__filename)),independent_helpers:sha(fs.readFileSync(path.join(__dirname,'browser_checks.cjs')))},
    node_version: process.version,
    geometry: {viewport_width: 1440, viewport_height: 1100, main_canvas_width: 1280, main_canvas_height: 720},
    fixture_sha256: Object.fromEntries(Object.entries(manifest).map(([key, name]) => [key, sha(fs.readFileSync(path.join(fixtures, name)))])),
    checks: [], errors: [], canvas_images: [],
  };
  const canvases = new WeakMap();
  const dimensions = element => {
    if (element.id === 'space-canvas' || element.classList.contains('canvas-stage')) return {width: 1280, height: 720};
    if (element.id === 'channel-history' || element.classList.contains('history-stage')) return {width: 600, height: 180};
    if (element.id === 'readout-timeline' || element.classList.contains('readout-history-stage')) return {width: 600, height: 160};
    return {width: 1280, height: 720};
  };
  const nativeCanvas = element => {
    if (!canvases.has(element)) canvases.set(element, createCanvas(Math.max(1, element.width), Math.max(1, element.height)));
    return canvases.get(element);
  };
  let dom;
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', error => report.errors.push(String(error.stack || error)));
  virtualConsole.on('error', (...args) => report.errors.push(args.map(String).join(' ')));
  const check = (name, details = {}) => {report.checks.push({name, passed: true, ...details}); process.stdout.write('PASS ' + name + '\n');};
  try {
    dom = new JSDOM(html, {
      url: 'https://presenter.invalid/', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole,
      // No resources loader: there is no network access from this DOM. The input
      // must be the self-contained artifact; missing inline code fails startup.
      beforeParse(window) {
        window.TextEncoder = TextEncoder; window.TextDecoder = TextDecoder;
        Object.defineProperty(window.crypto, 'subtle', {value: crypto.webcrypto.subtle});
        Object.defineProperty(window, 'innerWidth', {value: 1440});
        Object.defineProperty(window, 'innerHeight', {value: 1100});
        window.devicePixelRatio = 1;
        window.matchMedia = () => ({matches: true, addEventListener() {}, removeEventListener() {}});
        window.scrollTo = () => {};
        window.HTMLElement.prototype.scrollIntoView = () => {};
        window.HTMLElement.prototype.setPointerCapture = () => {};
        window.HTMLElement.prototype.releasePointerCapture = () => {};
        window.HTMLElement.prototype.hasPointerCapture = () => true;
        window.HTMLElement.prototype.getBoundingClientRect = function () {
          const {width, height} = dimensions(this);
          return {x: 0, y: 0, top: 0, left: 0, right: width, bottom: height, width, height, toJSON() {return {width, height};}};
        };
        for (const dimension of ['clientWidth', 'offsetWidth', 'clientHeight', 'offsetHeight']) {
          Object.defineProperty(window.HTMLElement.prototype, dimension, {get() {return dimensions(this)[dimension.endsWith('Width') ? 'width' : 'height'];}});
        }
        window.ResizeObserver = class {
          constructor(callback) {this.callback = callback; this.targets = new Set();}
          observe(target) {this.targets.add(target); window.setTimeout(() => {if (this.targets.has(target)) this.callback([{target, contentRect: target.getBoundingClientRect()}]);}, 0);}
          unobserve(target) {this.targets.delete(target);}
          disconnect() {this.targets.clear();}
        };
        for (const dimension of ['width', 'height']) {
          const descriptor = Object.getOwnPropertyDescriptor(window.HTMLCanvasElement.prototype, dimension);
          Object.defineProperty(window.HTMLCanvasElement.prototype, dimension, {
            get: descriptor.get,
            set(value) {descriptor.set.call(this, value); const native = canvases.get(this); if (native) native[dimension] = Math.max(1, this[dimension]);},
          });
        }
        window.HTMLCanvasElement.prototype.getContext = function (type) {assert.equal(type, '2d'); return nativeCanvas(this).getContext(type);};
        window.HTMLCanvasElement.prototype.toDataURL = function () {return nativeCanvas(this).toDataURL('image/png');};
        window.addEventListener('error', event => report.errors.push(String(event.error || event.message)));
      },
    });
    const window = dom.window, document = window.document;
    const $ = id => {const element = document.getElementById(id); assert(element, 'Missing UI element #' + id); return element;};
    const click = id => $(id).click();
    const value = id => $(id).textContent.trim();
    const dispatch = (id, event) => $(id).dispatchEvent(new window.Event(event, {bubbles: true}));
    const waitFor = async predicate => {
      const started = Date.now();
      while (!predicate()) {if (Date.now() - started > 30000) throw new Error('DOM integration timed out; errors: ' + report.errors.join('; ')); await sleep(10);}
    };
    const redraw = () => sleep(40);
    await waitFor(() => window.PresenterUI && window.PresenterUI.experiment && $('loading').hidden);
    const ui = window.PresenterUI;
    const retained = () => JSON.stringify({frames: ui.experiment.frames, coupling: ui.experiment.coupling, readouts: ui.experiment.readouts}, (_key, val) => typeof val === 'bigint' ? val.toString() : val);
    const scrub = async index => {$('scrub').value = String(index); dispatch('scrub', 'input'); await waitFor(() => ui.frameIndex === index); await redraw();};
    const select = async address => {
      click('inspect');
      for (let i = 0; i < 3; i++) $('node-' + ['x', 'y', 'z'][i]).value = String(address[i]);
      click('go-node'); $('channel-select').value = String(address[3]); dispatch('channel-select', 'change');
      same(ui.selection, {position: address.slice(0, 3), channel: address[3]});
      click('show-evidence'); await redraw();
    };
    const assertTriple = triple => {
      assert.equal(value('counter-a'), BigInt(triple[0]).toString());
      assert.equal(value('counter-b'), BigInt(triple[1]).toString());
      assert.equal(value('remainder'), String(triple[2]));
      assert.equal(value('theta'), String(Math.floor(Number(triple[2]) / 2)));
      assert.equal(value('parity'), String(Number(triple[2]) % 2));
    };
    const capture = async name => {
      await redraw();
      const canvas = nativeCanvas($('space-canvas')), pixels = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
      const first = Array.from(pixels.slice(0, 4)); let changed = 0;
      for (let i = 0; i < pixels.length; i += 4) if (pixels[i] !== first[0] || pixels[i+1] !== first[1] || pixels[i+2] !== first[2] || pixels[i+3] !== first[3]) changed++;
      assert(changed > 1000, 'The application canvas must contain a nontrivial rendered cube');
      const background = window.getComputedStyle(document.documentElement).getPropertyValue('--navy').trim() || '#173640';
      const composed = createCanvas(canvas.width,canvas.height), composedContext=composed.getContext('2d');
      composedContext.fillStyle=background;composedContext.fillRect(0,0,canvas.width,canvas.height);composedContext.drawImage(canvas,0,0);
      const bytes = composed.toBuffer('image/png'); fs.writeFileSync(path.join(output, name), bytes);
      const entry = {file: name, sha256: sha(bytes), width: canvas.width, height: canvas.height, differing_pixels: changed, canvas_background: background, experiment: ui.experiment.id, frame: ui.frameIndex, step: ui.experiment.frames[ui.frameIndex].step, channel: ui.selection.channel, projection: $('projection').value, field_filter: $('field-filter').value, camera: copy(ui.camera)};
      report.canvas_images.push(entry); return entry;
    };
    const importText = async text => {await ui.importText(text); await waitFor(() => $('loading').hidden); await redraw();};

    const demos = Array.from($('experiment').options, option => option.value);
    assert(demos.length >= 3); assert(!demos.includes(unseen.id) && !demos.includes(huge.id));
    for (let index = 0; index < demos.length; index++) {
      $('experiment').value = demos[index]; dispatch('experiment', 'change');
      assert.equal(ui.frameIndex, 0);
      assert.equal(document.querySelectorAll('#channel-grid button[data-channel]').length, 48);
      await capture('demo-' + String(index + 1).padStart(2, '0') + '-initial.png');
      await scrub(ui.experiment.frames.length - 1);
      assert.equal(value('step'), String(ui.experiment.frames.at(-1).step));
      assert($('next').disabled);
      await capture('demo-' + String(index + 1).padStart(2, '0') + '-final.png');
      click('rewind'); assert.equal(ui.frameIndex, 0);
    }
    check('Every embedded experiment loads, renders and scrubs to the last recorded state', {experiments: demos});

    // Choose a long recording by horizon, not a hard-coded experiment identity.
    // Every image is drawn by the same app renderSpace function used interactively.
    const sequenceIndex=window.PRESENTER_BUNDLE.experiments.reduce((best,entry,index,entries)=>entry.frames.length>entries[best].frames.length?index:best,0);
    $('experiment').value=demos[sequenceIndex];dispatch('experiment','change');
    const sequenceRetained=retained();
    $('field-filter').value='counters';dispatch('field-filter','change');
    await scrub(Math.min(24,ui.experiment.frames.length-1));
    const focusBefore=copy(ui.camera);click('focus-state');await redraw();
    assert.notEqual(ui.camera.zoom,focusBefore.zoom,'Focusing sparse retained state must change display scale');
    assert.equal(retained(),sequenceRetained,'Focus must preserve the complete trajectory, tensor and observers');
    assert(['yaw','pitch','zoom'].every(key=>Number.isFinite(ui.camera[key])));
    same(ui.camera.center.map(Number.isFinite),[true,true,true]);
    if(ui.camera.zoom<64) {
      const focusedZoom=ui.camera.zoom;
      $('space-canvas').dispatchEvent(new window.WheelEvent('wheel',{bubbles:true,cancelable:true,deltaY:-20}));
      assert(ui.camera.zoom>focusedZoom,'Zooming in after focus must not jump outward to an inconsistent clamp');
      click('focus-state');
      $('space-canvas').dispatchEvent(new window.KeyboardEvent('keydown',{key:'+',bubbles:true,cancelable:true}));
      assert(ui.camera.zoom>focusedZoom,'Keyboard zoom must share the focus zoom range');
      click('focus-state');
    }
    await capture('long-recording-detail.png');
    const sequenceFolder=path.join(output,'recorded-frames');fs.mkdirSync(sequenceFolder);
    for(let frame=0;frame<ui.experiment.frames.length;frame++) {await scrub(frame);await capture('recorded-frames/frame-'+String(frame).padStart(3,'0')+'.png');}
    click('fit');assert.equal(ui.camera.zoom,1);same(ui.camera.center,[.5,.5,.5]);
    assert.equal(retained(),sequenceRetained,'Rendering a demonstration must not alter any recorded state');
    check('Generic focus/reset preserve state and a complete recorded-frame sequence renders at the explicitly focused view', {experiment:ui.experiment.id,frames:ui.experiment.frames.length,folder:'recorded-frames',retained_sha256:sha(sequenceRetained)});

    await importText(JSON.stringify(unseenBundle)); assert.equal(ui.experiment.id, unseen.id);
    const row47 = unseen.frames[0].cells.find(row => row[3] === 47); assert(row47);
    await select(row47.slice(0, 4)); assertTriple(row47.slice(4));
    same(Array.from(document.querySelectorAll('#channel-grid button[data-channel]'), button => Number(button.dataset.channel)).sort((a,b) => a-b), Array.from({length:48}, (_v,i) => i));
    const negative = negativeTransition(unseen);
    await scrub(negative.index); await select(negative.address); assertTriple(negative.transition.next);
    for (const [id, expected] of [['algebra-u', negative.transition.u], ['algebra-numerator', negative.transition.numerator], ['algebra-quotient', negative.transition.quotient], ['algebra-remainder', negative.transition.remainder]]) assert.equal(value(id), expected.toString());
    const neighbors = Array.from(document.querySelectorAll('#neighbor-list button[data-neighbor]')); assert.equal(neighbors.length, 6);
    for (let d = 0; d < 6; d++) {
      const node = neighbors[d], expected = negative.transition.inputs[d], row = node.closest('.neighbor');
      same(JSON.parse(node.dataset.address), expected.address);
      assert.equal(row.querySelector('.neighbor-value').textContent.trim(), expected.b.toString());
      assert.equal(row.querySelector('.neighbor-product').textContent.trim(), expected.product.toString());
    }
    neighbors[0].click(); same(ui.selection, {position: negative.transition.inputs[0].address.slice(0,3), channel:negative.transition.inputs[0].address[3]});
    check('Unseen geometry, channel 47, six signed neighbors and negative division match independent BigInt arithmetic', {address: negative.address, frame: negative.index});

    const completeBefore = retained();
    const readoutsBefore = Array.from(document.querySelectorAll('#readouts [data-readout]'), node => ({id:node.dataset.readout,value:node.dataset.value,edge:node.dataset.edge}));
    assert(readoutsBefore.length > 0);
    for (const expected of readoutValues(unseen, negative.index)) {
      const actual = readoutsBefore.find(item => item.id === expected.id); assert(actual);
      assert.equal(['1','true'].includes(actual.value), expected.value); assert.equal(['1','true'].includes(actual.edge), expected.edge);
    }
    await select([0,0,0,46]); assertTriple(at(unseen, negative.index, [0,0,0,46]));
    for (const projection of ['iso','xy','xz','yz']) {$('projection').value = projection; dispatch('projection', 'change'); await redraw();}
    for (const filter of ['all','counters','remainders']) {$('field-filter').value = filter; dispatch('field-filter','change'); await redraw();}
    $('projection').value='iso'; dispatch('projection','change'); $('field-filter').value='all'; dispatch('field-filter','change'); click('fit');
    const cameraBefore = copy(ui.camera); assert(['yaw','pitch','zoom'].every(key => Number.isFinite(cameraBefore[key])));
    const pointer = (name, x, y, type='mouse', id=7) => {const event = new window.MouseEvent(name, {bubbles:true,cancelable:true,clientX:x,clientY:y,buttons:name==='pointerup'?0:1}); Object.defineProperties(event,{pointerId:{value:id},pointerType:{value:type},isPrimary:{value:id===7}}); $('space-canvas').dispatchEvent(event);};
    pointer('pointerdown',500,300); pointer('pointermove',660,390); pointer('pointerup',660,390); await redraw();
    assert(ui.camera.yaw !== cameraBefore.yaw || ui.camera.pitch !== cameraBefore.pitch);
    const zoomBefore=ui.camera.zoom; $('space-canvas').dispatchEvent(new window.WheelEvent('wheel',{bubbles:true,cancelable:true,deltaY:-160})); await redraw(); assert.notEqual(ui.camera.zoom, zoomBefore);
    const touchBefore=copy(ui.camera); pointer('pointerdown',400,300,'touch'); pointer('pointermove',450,340,'touch'); pointer('pointerup',450,340,'touch'); await redraw(); assert(ui.camera.yaw!==touchBefore.yaw||ui.camera.pitch!==touchBefore.pitch);
    const pinchBefore=ui.camera.zoom; pointer('pointerdown',450,350,'touch',7); pointer('pointerdown',550,350,'touch',8); pointer('pointermove',600,350,'touch',8); pointer('pointerup',450,350,'touch',7); pointer('pointerup',600,350,'touch',8); await redraw(); assert.notEqual(ui.camera.zoom,pinchBefore,'Two-touch pinch must update only display zoom');
    const keyboardBefore=copy(ui.camera); $('space-canvas').dispatchEvent(new window.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true})); await redraw(); assert.notEqual(ui.camera.yaw,keyboardBefore.yaw,'Keyboard arrows must rotate the displayed cube');
    assert.equal(retained(), completeBefore);
    same(Array.from(document.querySelectorAll('#readouts [data-readout]'),node=>({id:node.dataset.readout,value:node.dataset.value,edge:node.dataset.edge})),readoutsBefore);
    assertTriple(at(unseen, negative.index, [0,0,0,46]));
    await capture('unseen-rotated.png');
    check('Camera, synthetic pointer input, zoom, projections, filters and channel selection leave the complete experiment unchanged', {retained_sha256:sha(completeBefore), camera_before:cameraBefore,camera_after:copy(ui.camera)});

    await importText(JSON.stringify(hugeBundle)); assert.equal(ui.experiment.id, huge.id);
    const hugeRow = huge.frames[0].cells.find(row => String(row[4]).replace('-','').length > 4300 || String(row[5]).replace('-','').length > 4300); assert(hugeRow);
    await select(hugeRow.slice(0,4)); assertTriple(hugeRow.slice(4));
    for (const svg of document.querySelectorAll('svg')) assert(!/NaN|Infinity/.test(svg.outerHTML));
    await capture('huge-counter.png');
    check('More than 4300 decimal digits remain exact while native clock/cube drawing remains finite', {decimal_digits:Math.max(String(hugeRow[4]).replace('-','').length,String(hugeRow[5]).replace('-','').length)});

    for (const key of ['native_snapshot','native_trace']) {
      const source=fixtureText(key), records=key==='native_trace'?source.trim().split(/\r?\n/).map(JSON.parse):[JSON.parse(source)];
      await importText(source); assert($('error').hidden);
      await scrub(records.length-1); const cp=records.at(-1); assert.equal(value('step'),String(cp.completed_steps));
      const change=cp.experiment.seed_changes.find(change=>change.channel===47)||cp.experiment.seed_changes[0];
      await select([...change.position,change.channel]); assertTriple(change.state);
      if(records.length===1) {assert($('next').disabled); assert.match(value('status'),/snapshot|no transition|0 transition/i);}
      check('Native '+key+' loads with retained state and absolute step index');
    }

    const backgroundCheckpoint=JSON.parse(fixtureText('native_snapshot'));
    backgroundCheckpoint.experiment.seed_changes=[];
    await importText(JSON.stringify(backgroundCheckpoint));assert($('error').hidden);
    const backgroundAddress=[ui.experiment.side-1,1,ui.experiment.side-1,47];
    await select(backgroundAddress);assertTriple(ui.experiment.background);
    assert.equal(ui.experiment.frames[0].cells.length,0);
    assert.equal(document.querySelectorAll('#channel-grid button[data-channel]').length,48);
    assert($('next').disabled);await capture('all-background-snapshot.png');
    check('An all-background snapshot retains arbitrary coordinates and all 48 inspectable channels');
    await importText(JSON.stringify({format:'universe24-presenter-v1',title:'Empty research workspace',catalog:[],experiments:[]}));
    assert.equal(ui.experiment,null);assert(!$('empty').hidden);assert($('workspace').hidden);assert($('error').hidden);
    check('An empty bundle opens an honest empty workspace without invented frames');

    const hostile=copy(unseenBundle); hostile.experiments[0].id='dom-label-safety'; hostile.experiments[0].title='<img src=x onerror="globalThis.__presenterXSS=1">';hostile.experiments[0].description='<script>globalThis.__presenterXSS=2</script>';
    await importText(JSON.stringify(hostile)); assert.equal(window.__presenterXSS,undefined);assert.equal(document.querySelectorAll('img[src="x"]').length,0);
    const identity=JSON.stringify({id:ui.experiment.id,selection:ui.selection,frame:ui.frameIndex});
    const corrupted=copy(unseenBundle);corrupted.experiments[0].frames[1].cells[0][6]=(corrupted.experiments[0].frames[1].cells[0][6]+1)%6;
    for(const source of ['{"format":"universe24-presenter-v1","format":"universe24-presenter-v1"}','{"format":',JSON.stringify(corrupted)]) {
      try {await importText(source);} catch(error) {assert(error instanceof Error || typeof error.message==='string');}
      assert(!$('error').hidden); assert(value('error').length>0);
      assert.equal(JSON.stringify({id:ui.experiment.id,selection:ui.selection,frame:ui.frameIndex}),identity);
    }
    check('Hostile metadata stays text and malformed imports preserve the prior valid view');
    assert.deepEqual(report.errors,[],'Application scripts must not produce unhandled errors');
    if(process.env.PRESENTER_RENDER_GIF==='1') {
      const movie='recorded-experiment.gif';
      const args=['-hide_banner','-loglevel','error','-framerate','6','-i',path.join(output,'recorded-frames','frame-%03d.png'),'-filter_complex','scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3','-loop','0',path.join(output,movie)];
      const rendered=spawnSync('ffmpeg',args,{encoding:'utf8',timeout:60000});
      assert.equal(rendered.status,0,'Recorded-frame GIF conversion failed: '+String(rendered.error||rendered.stderr));
      report.recorded_animation={file:movie,sha256:sha(fs.readFileSync(path.join(output,movie))),frames_per_second:6,source_folder:'recorded-frames',source:'Actual application Canvas2D output; recorded states only',command:['ffmpeg',...args]};
    }
    report.passed=true;
  } catch(error) {
    report.failure={name:error.name,message:error.message,stack:error.stack};
    throw error;
  } finally {
    if(dom) dom.window.close();
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});
    process.stdout.write('DOM/native-canvas evidence: '+output+'\n');
  }
}
main().catch(error=>{process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;});
