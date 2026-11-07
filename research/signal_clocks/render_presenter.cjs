#!/usr/bin/env node
'use strict';

// Captures the unchanged Presenter application's actual Canvas2D output.
// jsdom geometry is explicit: this is not browser CSS or pointer-hit-test proof.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const {TextEncoder, TextDecoder} = require('node:util');
const {JSDOM, VirtualConsole} = require('jsdom');
const {createCanvas} = require('@napi-rs/canvas');
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const copy = data => JSON.parse(JSON.stringify(data));
const stable = data => JSON.stringify(data, (_key, value) => typeof value === 'bigint' ? value.toString() : value);

async function main() {
  const [htmlArg, planArg, outputArg] = process.argv.slice(2);
  assert(htmlArg && planArg && outputArg, 'Usage: render_presenter.cjs HTML RENDER_PLAN NEW_OUTPUT');
  const htmlPath = path.resolve(htmlArg), planPath = path.resolve(planArg), output = path.resolve(outputArg);
  const html = fs.readFileSync(htmlPath, 'utf8'), planRaw = fs.readFileSync(planPath, 'utf8'), plan = JSON.parse(planRaw);
  assert.equal(plan.format, 'universe24-signal-clock-render-v1');
  assert.equal(sha(html), plan.html_sha256, 'Plan must name the exact standalone HTML');
  assert(Array.isArray(plan.sequences) && plan.sequences.length > 0 && plan.sequences.length <= 4);
  assert(!fs.existsSync(output), 'Output must be a new directory');
  fs.mkdirSync(output, {recursive: true});
  const started = Date.now(), initialCPU = process.cpuUsage();
  const wallSeconds = plan.wall_seconds ?? 120;
  assert(Number.isInteger(wallSeconds) && wallSeconds >= 1 && wallSeconds <= 300);
  const verifyAllCases = plan.verify_all_cases !== false;
  const gifWidth = plan.gif_width ?? 960;
  assert(Number.isInteger(gifWidth) && gifWidth >= 480 && gifWidth <= 1280);
  const budget = () => {assert(Date.now() - started < wallSeconds * 1000, `${wallSeconds}-second rendering wall budget exceeded`);};
  const report = {
    format: 'universe24-signal-clock-canvas-v1', passed: false,
    scope: 'Actual unchanged Presenter app in jsdom with native Canvas2D and explicit geometry; no browser CSS, responsive-layout, accessibility or native pointer claim',
    input_sha256: sha(html), plan_sha256: sha(planRaw), source_sha256: sha(fs.readFileSync(__filename)),
    dependencies: {node: process.version, jsdom: require('jsdom/package.json').version, canvas: require('@napi-rs/canvas/package.json').version},
    verification_mode: verifyAllCases ? 'all_case_checks_and_animation' : 'animation_only',
    images: [], sequences: [], checks: [], errors: [],
  };
  const canvases = new WeakMap();
  const size = element => element.id === 'channel-history' ? {width: 600, height: 180} : element.id === 'readout-timeline' ? {width: 600, height: 160} : {width: 1280, height: 720};
  const nativeCanvas = element => {
    if (!canvases.has(element)) canvases.set(element, createCanvas(Math.max(1, element.width), Math.max(1, element.height)));
    return canvases.get(element);
  };
  let dom;
  try {
    const virtualConsole = new VirtualConsole();
    virtualConsole.on('jsdomError', error => report.errors.push(String(error.stack || error)));
    virtualConsole.on('error', (...args) => report.errors.push(args.map(String).join(' ')));
    dom = new JSDOM(html, {
      url: 'https://presenter.invalid/', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole,
      beforeParse(window) {
        window.TextEncoder = TextEncoder; window.TextDecoder = TextDecoder;
        Object.defineProperty(window.crypto, 'subtle', {value: crypto.webcrypto.subtle});
        window.devicePixelRatio = 1;
        window.matchMedia = () => ({matches: true, addEventListener() {}, removeEventListener() {}});
        window.scrollTo = () => {};
        window.HTMLElement.prototype.scrollIntoView = () => {};
        window.HTMLElement.prototype.setPointerCapture = () => {};
        window.HTMLElement.prototype.releasePointerCapture = () => {};
        window.HTMLElement.prototype.getBoundingClientRect = function () {
          const {width, height} = size(this);
          return {x: 0, y: 0, top: 0, left: 0, right: width, bottom: height, width, height, toJSON() {return {width, height};}};
        };
        for (const dimension of ['clientWidth', 'offsetWidth', 'clientHeight', 'offsetHeight']) {
          Object.defineProperty(window.HTMLElement.prototype, dimension, {get() {return size(this)[dimension.endsWith('Width') ? 'width' : 'height'];}});
        }
        window.ResizeObserver = class {
          constructor(callback) {this.callback = callback;}
          observe(target) {window.setTimeout(() => this.callback([{target, contentRect: target.getBoundingClientRect()}]), 0);}
          unobserve() {} disconnect() {}
        };
        for (const dimension of ['width', 'height']) {
          const descriptor = Object.getOwnPropertyDescriptor(window.HTMLCanvasElement.prototype, dimension);
          Object.defineProperty(window.HTMLCanvasElement.prototype, dimension, {
            get: descriptor.get,
            set(value) {descriptor.set.call(this, value); const native = canvases.get(this); if (native) native[dimension] = Math.max(1, this[dimension]);},
          });
        }
        window.HTMLCanvasElement.prototype.getContext = function (type) {assert.equal(type, '2d'); return nativeCanvas(this).getContext(type);};
        window.addEventListener('error', event => report.errors.push(String(event.error || event.message)));
      },
    });
    const window = dom.window, document = window.document;
    const $ = id => {const element = document.getElementById(id); assert(element, 'Missing #' + id); return element;};
    const dispatch = (id, type) => $(id).dispatchEvent(new window.Event(type, {bubbles: true}));
    const waitFor = async predicate => {while (!predicate()) {budget(); if (report.errors.length) throw new Error(report.errors.join('\n')); await sleep(10);}};
    await waitFor(() => window.PresenterUI && window.PresenterUI.experiment && $('loading').hidden);
    const ui = window.PresenterUI;
    const retained = () => sha(stable({frames: ui.experiment.frames, coupling: ui.experiment.coupling, readouts: ui.experiment.readouts}));
    const scrub = async frame => {$('scrub').value = String(frame); dispatch('scrub', 'input'); await waitFor(() => ui.frameIndex === frame);};
    const choose = id => {$('experiment').value = id; dispatch('experiment', 'change'); assert.equal(ui.experiment.id, id);};
    const at = (experiment, frame, address) => {
      const row = experiment.frames[frame].cells.find(cell => address.every((value, i) => cell[i] === value));
      return row ? row.slice(4) : experiment.background;
    };
    const predicates = (experiment, frame) => experiment.readouts.map(readout => ({
      id: readout.id,
      value: readout.clauses.every(clause => BigInt(at(experiment, frame, clause.address)[{a: 0, b: 1, r: 2}[clause.component]]) === BigInt(clause.equals)),
    }));
    const capture = name => {
      budget();
      const canvas = nativeCanvas($('space-canvas'));
      const bytes = canvas.toBuffer('image/png');
      const target = path.join(output, name); fs.mkdirSync(path.dirname(target), {recursive: true}); fs.writeFileSync(target, bytes, {flag: 'wx'});
      const entry = {file: name, sha256: sha(bytes), experiment: ui.experiment.id, frame: ui.frameIndex,
        step: ui.experiment.frames[ui.frameIndex].step, channel: ui.selection.channel,
        selection: copy(ui.selection), field_filter: $('field-filter').value, projection: $('projection').value,
        camera: copy(ui.camera), readouts: predicates(ui.experiment, ui.frameIndex)};
      report.images.push(entry); return entry;
    };
    for (const [index, original] of (verifyAllCases ? window.PRESENTER_BUNDLE.experiments : []).entries()) {
      choose(original.id); const before = retained();
      assert.equal(document.querySelectorAll('#channel-grid button[data-channel]').length, 48);
      const observed = [];
      for (let frame = 0; frame < ui.experiment.frames.length; frame++) {
        budget(); await scrub(frame);
        const expected = predicates(ui.experiment, frame); observed.push(expected);
        for (let start = 0; start < expected.length; start += 8) {
          if (start) $('readouts-next').click();
          for (const item of expected.slice(start, start + 8)) {
            const row = Array.from(document.querySelectorAll('#readouts [data-readout]')).find(node => node.dataset.readout === item.id);
            assert(row, 'Readout missing: ' + item.id); assert.equal(row.dataset.value, String(item.value));
            const previous = frame ? observed[frame - 1].find(entry => entry.id === item.id).value : true;
            assert.equal(row.dataset.edge, String(item.value && !previous));
          }
        }
        while (!$('readouts-prev').disabled) $('readouts-prev').click();
      }
      await scrub(0); capture(`case-${String(index + 1).padStart(2, '0')}-initial.png`);
      await scrub(ui.experiment.frames.length - 1); capture(`case-${String(index + 1).padStart(2, '0')}-final.png`);
      $('space-canvas').dispatchEvent(new window.KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true, cancelable: true}));
      $('space-canvas').dispatchEvent(new window.WheelEvent('wheel', {deltaY: -60, bubbles: true, cancelable: true}));
      $('focus-state').click(); $('fit').click();
      assert.equal(retained(), before, 'Navigation/rendering changed a retained experiment');
      report.checks.push({name: 'Recorded frames, all 48 channels, fixed readouts and passive navigation', experiment: original.id,
        passed: true, frames: ui.experiment.frames.length, state_tensor_readout_sha256: before, readout_history: observed});
    }
    for (const [index, sequence] of plan.sequences.entries()) {
      choose(sequence.experiment); const before = retained();
      const last = sequence.last_frame ?? ui.experiment.frames.length - 1, first = sequence.first_frame ?? 0;
      assert(Number.isInteger(first) && Number.isInteger(last) && first >= 0 && last >= first && last < ui.experiment.frames.length);
      assert(last - first < 120, 'At most 120 consecutive frames per animation');
      $('field-filter').value = sequence.field_filter || 'all'; dispatch('field-filter', 'change');
      if (sequence.view) {
        $('inspect').click();
        for (let axis = 0; axis < 3; axis++) $('node-' + ['x', 'y', 'z'][axis]).value = String(sequence.view.position[axis]);
        $('go-node').click(); $('channel-select').value = String(sequence.view.channel); dispatch('channel-select', 'change');
      }
      const framing = sequence.framing || 'retained';
      assert(['retained', 'whole-cube'].includes(framing), 'Unknown camera framing');
      const rotationSteps = sequence.rotation_steps_per_frame ?? 0;
      assert(Number.isInteger(rotationSteps) && rotationSteps >= 0 && rotationSteps <= 2);
      await scrub(sequence.focus_frame ?? first);
      $(framing === 'whole-cube' ? 'fit' : 'focus-state').click();
      const cubeBounds = [];
      const assertWholeCubeFits = () => {
        const {width, height} = size($('space-canvas')), c = ui.camera;
        const co = Math.cos(c.yaw), si = Math.sin(c.yaw), cp = Math.cos(c.pitch), sp = Math.sin(c.pitch);
        const spanX = Math.abs(co) + Math.abs(si);
        const spanY = Math.abs(cp) + Math.abs(sp) * (Math.abs(si) + Math.abs(co));
        const scale = Math.min(Math.max(40, width - 64) / spanX, Math.max(40, height - 80) / spanY) * .88 * c.zoom;
        const corners = [];
        for (const x of [0, 1]) for (const y of [0, 1]) for (const z of [0, 1]) {
          const v = [x - c.center[0], y - c.center[1], z - c.center[2]];
          const xx = v[0] * co - v[2] * si, zz = v[0] * si + v[2] * co;
          const point = {x: width / 2 + xx * scale, y: height * .46 - (v[1] * cp - zz * sp) * scale};
          assert(point.x >= 0 && point.x <= width && point.y >= 0 && point.y <= height, 'Whole-cube corner outside the canvas');
          corners.push(point);
        }
        cubeBounds.push({frame: ui.frameIndex, camera: copy(c), corners, all_eight_inside: true});
      };
      const folder = `sequence-${String(index + 1).padStart(2, '0')}`;
      capture(`${folder}/detail.png`);
      for (let frame = first; frame <= last; frame++) {
        await scrub(frame);
        for (let i = 0; i < rotationSteps; i++) $('space-canvas').dispatchEvent(new window.KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true, cancelable: true}));
        if (framing === 'whole-cube') assertWholeCubeFits();
        capture(`${folder}/frame-${String(frame - first).padStart(3, '0')}.png`);
      }
      assert.equal(retained(), before, 'Animation changed full recorded state');
      const fps = sequence.fps || 4;
      assert(Number.isInteger(fps) && fps >= 1 && fps <= 24);
      const movie = `${folder}/recorded-clocks.gif`;
      const args = ['-hide_banner', '-loglevel', 'error', '-threads', '1', '-filter_threads', '1', '-framerate', String(fps),
        '-i', path.join(output, folder, 'frame-%03d.png'), '-filter_complex',
        `scale=${gifWidth}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3`,
        '-loop', '0', path.join(output, movie)];
      const result = spawnSync('ffmpeg', args, {encoding: 'utf8', timeout: Math.min(60000, wallSeconds * 1000 - (Date.now() - started))});
      assert.equal(result.status, 0, 'GIF conversion failed: ' + String(result.error || result.stderr));
      report.sequences.push({experiment: sequence.experiment, first_frame: first, last_frame: last, fps,
        file: movie, sha256: sha(fs.readFileSync(path.join(output, movie))), source: 'Actual Presenter Canvas2D output from consecutive saved states',
        state_tensor_readout_sha256: before, camera_framing: framing, rotation_steps_per_frame: rotationSteps,
        cube_bounds: cubeBounds, command: ['ffmpeg', ...args]});
    }
    assert.deepEqual(report.errors, []); budget(); report.passed = true;
  } catch (error) {
    report.failure = {name: error.name, message: error.message, stack: error.stack}; throw error;
  } finally {
    if (dom) dom.window.close();
    const cpu = process.cpuUsage(initialCPU); report.parent_cpu_seconds = (cpu.user + cpu.system) / 1e6;
    report.wall_seconds = (Date.now() - started) / 1000; report.wall_limit_seconds = wallSeconds;
    fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n', {flag: 'wx'});
  }
  process.stdout.write(JSON.stringify({passed: report.passed, cases: report.checks.length, sequences: report.sequences.length,
    images: report.images.length, cpu_seconds: report.parent_cpu_seconds, wall_seconds: report.wall_seconds}) + '\n');
}

main().catch(error => {process.stderr.write(String(error.stack || error) + '\n'); process.exitCode = 1;});
