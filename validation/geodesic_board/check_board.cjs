#!/usr/bin/env node
'use strict';
// DOM/canvas execution audit, not a browser or screenshot test.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');

const file = process.argv[2];
if (!file || process.argv.length !== 3) {
  console.error('Usage: node validation/geodesic_board/check_board.cjs path/board.html');
  process.exit(2);
}
const html = fs.readFileSync(file, 'utf8');
const scripts = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 2, 'Expected one JSON data element and one executable script');
assert.match(scripts[0][1], /id="report"/);
assert.match(scripts[0][1], /type="application\/json"/);
const data = JSON.parse(scripts[0][2]);
assert.equal(data.schema, 'universe24/geodesic-board/1');
assert.ok(data.snapshots.length >= 2);
const code = scripts[1][2];
let coordinates = 0, strokes = 0, intervalsStarted = 0;
let interval = null, intervalId = 0;
const context2d = new Proxy({}, {
  get: (target, key) => target[key] ?? (() => {}),
  set: (target, key, value) => { target[key] = value; return true; },
});
for (const name of ['moveTo', 'lineTo', 'arc', 'translate', 'scale']) {
  context2d[name] = (...args) => {
    assert.ok(args.every(Number.isFinite), `Nonfinite ${name} arguments: ${args}`);
    coordinates += args.length;
  };
}
context2d.stroke = () => { strokes++; };
const elements = new Map();
function element(id = '') {
  return {
    id, textContent: '', value: 0, children: [], events: {}, className: '',
    getBoundingClientRect: () => ({width: 900, height: 430}),
    getContext: kind => { assert.equal(kind, '2d'); return context2d; },
    append(...children) { this.children.push(...children); },
    addEventListener(name, callback) { this.events[name] = callback; },
  };
}
function get(id) {
  if (!elements.has(id)) elements.set(id, element(id));
  return elements.get(id);
}
get('report').textContent = scripts[0][2];
const sandbox = {
  document: {getElementById: get, createElement: () => element()},
  window: {devicePixelRatio: 1, addEventListener() {}},
  setInterval(callback) {
    assert.equal(interval, null, 'Playback must not duplicate its active timer');
    interval = callback; intervalsStarted++; return ++intervalId;
  },
  clearInterval(id) { assert.equal(id, intervalId); interval = null; },
  console,
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox, {filename: file, timeout: 10000});
const fmt = value => {
  const n = Number(value);
  return Number.isFinite(n) ? (Math.abs(n) < 1e-6 && n !== 0
    ? n.toExponential(3)
    : n.toLocaleString('en-US', {maximumSignificantDigits: 6})) : 'not reported';
};
function assertSlice(index) {
  const s = data.snapshots[index];
  assert.equal(get('energy').textContent, fmt(s.energy_density));
  assert.equal(get('constraint').textContent, fmt(s.hamiltonian_constraint));
  assert.equal(get('step').textContent, `t ${fmt(s.time)} · ${index}/${data.snapshots.length - 1}`);
}
const last = data.snapshots.length - 1;
assertSlice(last);
assert.equal(Number(get('time').max), last);
for (let i = 0; i <= last; i++) {
  get('time').value = i;
  get('time').events.input();
  assertSlice(i);
}
const replayRow = get('gates').children.find(row => row.children[0]?.textContent === 'Exact replay');
assert.ok(replayRow, 'Missing exact replay evidence row');
assert.equal(replayRow.children[1].textContent, 'passed');
assert.equal(replayRow.children[1].className, 'pass');
// Starting from final frame restarts at zero on the first timer callback.
get('play').events.click();
assert.equal(get('play').textContent, 'Ⅱ Pause');
assert.equal(typeof interval, 'function');
interval();
assertSlice(0);
// Pausing must cancel the timer without advancing the selected slice.
get('play').events.click();
assert.equal(interval, null);
assert.equal(get('play').textContent, '▶ Play');
assertSlice(0);
// Resume and complete, with no stale live timer at the final slice.
get('play').events.click();
for (let i = 1; i <= last; i++) {
  assert.equal(typeof interval, 'function');
  interval();
  assertSlice(i);
}
assert.equal(interval, null);
assert.equal(get('play').textContent, '▶ Play');
assert.ok(coordinates > 0 && strokes > 0, 'Drawing code was not exercised');
console.log(JSON.stringify({
  status: 'passed',
  scope: 'JavaScript DOM/canvas smoke; not browser layout or screenshot verification',
  script_source_sha256: crypto.createHash('sha256').update(code).digest('hex'),
  harness_source_sha256: crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'),
  report_identity: {
    schema: data.schema, run_id: data.provenance.run_id,
    bundle_id: data.provenance.bundle_id, tensor_sha256: data.provenance.tensor_sha256,
  },
  tested: {
    saved_slices: data.snapshots.length, selected_state_checks: 2 * data.snapshots.length + 2,
    playback_starts: intervalsStarted, playback_pause: true, playback_completion: true,
    finite_coordinate_arguments: coordinates, canvas_strokes: strokes,
    exact_replay_passed_tag: true, source_energy_and_constraint_text: true,
  },
}, null, 2));
