#!/usr/bin/env node
'use strict';

// Independent delivery review of the complete packaged HTML, not a browser test.
// Usage: NODE_PATH=... node tests/presenter_delivery_review.cjs OLD.html NEW.html NEW_REPORT_DIR
// Native Canvas2D supplies actual drawing; jsdom receives explicit geometry.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {TextEncoder, TextDecoder} = require('node:util');
const {JSDOM, VirtualConsole} = require('jsdom');
const {createCanvas} = require('@napi-rs/canvas');
const sha = input => crypto.createHash('sha256').update(input).digest('hex');
const plain = value => JSON.parse(JSON.stringify(value));
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const visible = element => Boolean(element) && !element.closest('[hidden]');

function unpack(html) {
  const dom = new JSDOM(html);
  const scripts = [...dom.window.document.scripts].map(script => script.textContent);
  const code = scripts.find(code => code.startsWith('globalThis.PRESENTER_BUNDLE='));
  assert(code, 'A complete embedded bundle is required');
  const bundle = JSON.parse(code.slice('globalThis.PRESENTER_BUNDLE='.length, -1));
  dom.window.close();
  return {scripts, code, bundle};
}

function start(html, modifyWindow) {
  const errors = [], canvases = new WeakMap(), vc = new VirtualConsole();
  vc.on('jsdomError', error => errors.push(String(error.message)));
  const dom = new JSDOM(html, {
    url: 'https://independent-review.invalid/', runScripts: 'dangerously',
    pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(window) {
      window.TextEncoder = TextEncoder; window.TextDecoder = TextDecoder;
      Object.defineProperty(window.crypto, 'subtle', {value: crypto.webcrypto.subtle, configurable: true});
      window.devicePixelRatio = 1;
      window.HTMLElement.prototype.scrollIntoView = function () {};
      window.HTMLElement.prototype.getBoundingClientRect = function () {
        return {x:0,y:0,left:0,top:0,right:640,bottom:400,width:640,height:400};
      };
      window.ResizeObserver = class {observe() {} disconnect() {}};
      for (const property of ['width','height']) {
        const descriptor = Object.getOwnPropertyDescriptor(window.HTMLCanvasElement.prototype, property);
        Object.defineProperty(window.HTMLCanvasElement.prototype, property, {
          get: descriptor.get,
          set(value) {descriptor.set.call(this,value); const native=canvases.get(this); if(native)native[property]=Math.max(1,this[property]);}
        });
      }
      window.HTMLCanvasElement.prototype.getContext = function (kind) {
        assert.equal(kind,'2d');
        if (!canvases.has(this)) canvases.set(this,createCanvas(Math.max(1,this.width),Math.max(1,this.height)));
        return canvases.get(this).getContext('2d');
      };
      if (modifyWindow) modifyWindow(window);
    }
  });
  return {dom, window:dom.window, document:dom.window.document, errors, canvases};
}

async function until(predicate, timeout=60000) {
  const started=Date.now();
  while(!predicate()) {assert(Date.now()-started<timeout,'Timed out waiting for the packaged viewer');await sleep(15);}
}

function expectedReadouts(experiment,index) {
  const read = (readout,frame) => {
    const map = new Map(experiment.frames[frame].cells.map(row=>[row.slice(0,4).join(','),row.slice(4)]));
    return readout.clauses.every(clause=>{
      const triple=map.get(clause.address.join(','))||experiment.background;
      return String(triple[{a:0,b:1,r:2}[clause.component]])===clause.equals;
    });
  };
  return experiment.readouts.map(readout=>({id:readout.id,label:readout.label,
    value:read(readout,index),edge:index>0&&read(readout,index)&&!read(readout,index-1)}));
}

async function main() {
  const [oldArg,newArg,outputArg]=process.argv.slice(2);
  assert(oldArg&&newArg&&outputArg,'Expected old HTML, new HTML and a new evidence directory');
  const oldPath=path.resolve(oldArg), newPath=path.resolve(newArg), output=path.resolve(outputArg);
  assert(!fs.existsSync(output),'Evidence directory must be new');fs.mkdirSync(output,{recursive:true});
  const oldHtml=fs.readFileSync(oldPath,'utf8'),newHtml=fs.readFileSync(newPath,'utf8');
  const old=unpack(oldHtml),fresh=unpack(newHtml);
  const report={format:'universe24-presenter-independent-delivery-review-v1',passed:false,
    scope:'Packaged source, script-disabled DOM, injected startup faults, and actual application in jsdom with native Canvas2D and explicit geometry. No actual iPad, Safari, browser CSS layout, hit testing or host-preview execution claim.',
    historical_html_sha256:sha(oldHtml),new_html_sha256:sha(newHtml),test_sha256:sha(fs.readFileSync(__filename)),
    dependencies:{node:process.version,jsdom:require('jsdom/package.json').version,canvas:require('@napi-rs/canvas/package.json').version},checks:[]};
  const check=(name,details={})=>{report.checks.push({name,passed:true,...details});console.log('PASS '+name);};
  let active;
  try {
    assert.equal(fresh.code,old.code,'Full embedded payload bytes must be preserved');
    const oldData=old.scripts.find(code=>code.includes('exact read-only state validation and algebra'));
    assert.equal(fresh.scripts.find(code=>code.includes('exact read-only state validation and algebra')),oldData,'Exact arithmetic and data validator must be unchanged');
    check('Exact original complete payload and arithmetic validator preserved',{experiments:fresh.bundle.experiments.length,frames:fresh.bundle.experiments.reduce((sum,e)=>sum+e.frames.length,0),payload_sha256:sha(fresh.code),data_module_sha256:sha(oldData)});

    for (const [name,html] of [['historical',oldHtml],['repaired',newHtml]]) {
      const dom=new JSDOM(html),doc=dom.window.document;
      assert(!visible(doc.getElementById('workspace')));
      if(name==='historical') {
        for(const id of ['loading','error','empty'])assert(!visible(doc.getElementById(id)));
        assert.equal(doc.querySelectorAll('#experiment option').length,0);
        assert.equal(doc.querySelector('noscript'),null);
      } else {
        assert(visible(doc.getElementById('startup')));
        assert(doc.getElementById('open-file').disabled);
        const rows=[...doc.querySelectorAll('#embedded-recordings li')];
        assert.equal(rows.length,fresh.bundle.experiments.length);
        rows.forEach((row,i)=>{assert(visible(row));assert.equal(row.querySelector('strong').textContent,fresh.bundle.experiments[i].title);assert(row.textContent.includes(String(fresh.bundle.experiments[i].frames.length)+' recorded states'));});
        assert(doc.getElementById('startup').textContent.includes('static'));
        assert(doc.getElementById('startup').textContent.includes('cannot enable scripting'));
        assert(doc.querySelector('noscript').textContent.includes('JavaScript is disabled'));
      }
      dom.window.close();check(name+' artifact with scripts not executed');
    }

    const early=w=>{w.ResizeObserver=class {observe(){throw Error('Independent injected early observer exception')}};};
    active=start(oldHtml,early);await sleep(30);
    assert(active.errors.some(message=>message.includes('Independent injected')));
    for(const id of ['loading','error','empty','workspace'])assert(!visible(active.document.getElementById(id)));
    active.dom.window.close();active=null;check('Historical early exception also reproduces blank shell');

    const dataCode=fresh.scripts.find(code=>code.includes('exact read-only state validation and algebra'));
    const appCode=fresh.scripts.find(code=>code.includes('passive views of complete'));
    const cases=[
      {name:'early synchronous exception',modify:early,expect:'Independent injected'},
      {name:'missing Web Crypto',modify:w=>Object.defineProperty(w.crypto,'subtle',{value:undefined,configurable:true}),expect:'Web Crypto'},
      {name:'missing TextEncoder',modify:w=>{w.TextEncoder=undefined;},expect:'TextEncoder'},
      {name:'missing BigInt API',modify:w=>{w.BigInt=undefined;},expect:'BigInt'},
      {name:'missing Canvas2D',modify:w=>{w.HTMLCanvasElement.prototype.getContext=()=>null;},expect:'Canvas'},
      {name:'missing data module',html:newHtml.replace(dataCode,'/* Independent removed data dependency. */'),expect:'data module'},
      {name:'later script syntax failure',html:newHtml.replace(appCode,'const = ;'),expect:'script failed'},
    ];
    for(const fault of cases) {
      active=start(fault.html||newHtml,fault.modify);await sleep(35);
      const panel=active.document.getElementById('startup');
      assert(visible(panel),fault.name+' must preserve the visible fallback');
      assert.equal(panel.dataset.phase,'failed',fault.name);
      assert(panel.textContent.includes(fault.expect),fault.name+' must explain failure');
      assert.equal(active.document.querySelectorAll('#embedded-recordings li').length,fresh.bundle.experiments.length);
      assert(active.document.getElementById('open-file').disabled);
      assert(!active.window.PresenterUI,fault.name+' must not claim initialized interactivity');
      check('Honest visible diagnostic: '+fault.name,{status:active.document.getElementById('startup-status').textContent});
      active.dom.window.close();active=null;
    }

    active=start(newHtml);await until(()=>active.window.PresenterUI);
    assert.equal(await active.window.PresenterUI.ready,true);
    const {window,document,canvases}=active,ui=window.PresenterUI;
    assert.equal(document.getElementById('startup').dataset.phase,'ready');
    assert(!visible(document.getElementById('startup')));
    assert(visible(document.getElementById('workspace')));
    assert(!document.getElementById('open-file').disabled);
    assert.equal(document.querySelectorAll('#experiment option').length,fresh.bundle.experiments.length);
    let readoutFrames=0;
    for(const expected of fresh.bundle.experiments) {
      const select=document.getElementById('experiment');select.value=expected.id;select.dispatchEvent(new window.Event('change'));
      assert.equal(ui.experiment.id,expected.id);
      for(const property of ['side','background','coupling','frames','readouts','view','provenance'])assert.deepEqual(plain(ui.experiment[property]),expected[property],expected.id+' '+property);
      assert.equal(ui.experiment.validation.hashes_verified,expected.frames.length);
      assert.equal(ui.experiment.validation.transitions,expected.frames.length-1);
      expected.frames.forEach((_frame,index)=>{
        assert.deepEqual(plain(window.PresenterData.readouts(ui.experiment,index)),expectedReadouts(expected,index));readoutFrames++;
      });
      const slider=document.getElementById('scrub');slider.value=String(expected.frames.length-1);slider.dispatchEvent(new window.Event('input'));
      assert.equal(ui.frameIndex,expected.frames.length-1);assert.equal(document.getElementById('step').textContent,String(expected.frames.at(-1).step));
      assert.deepEqual(plain(ui.experiment.frames),expected.frames);
    }
    const before=JSON.stringify(ui.experiment),yaw=ui.camera.yaw;
    document.getElementById('space-canvas').dispatchEvent(new window.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
    assert.notEqual(ui.camera.yaw,yaw);assert.equal(JSON.stringify(ui.experiment),before);
    const canvas=canvases.get(document.getElementById('space-canvas'));
    const pixels=canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
    let differences=0;for(let i=4;i<pixels.length;i+=4)if(pixels[i]!==pixels[0]||pixels[i+1]!==pixels[1]||pixels[i+2]!==pixels[2])differences++;
    assert(differences>1000,'Actual application must draw more than a blank canvas');
    assert.deepEqual(active.errors,[]);
    check('All experiments load, retain full state, preserve every readout and support passive navigation',{experiments:fresh.bundle.experiments.length,readout_frames:readoutFrames,canvas_differing_pixels:differences});
    report.passed=true;
  } catch(error) {report.failure=String(error.stack||error);throw error;}
  finally {if(active)active.dom.window.close();fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');}
}
main().catch(error=>{console.error(error.stack||error);process.exitCode=1;});
