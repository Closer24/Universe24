#!/usr/bin/env node
'use strict';

// Exercise unchanged Presenter scripts and native Canvas2D with explicit geometry.
// This is not a browser CSS layout, native pointer hit test, Safari or iPad test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {TextEncoder, TextDecoder} = require('node:util');
const {JSDOM, VirtualConsole} = require('jsdom');
const {createCanvas} = require('@napi-rs/canvas');
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const stable = data => JSON.stringify(data, (_key, value) => typeof value === 'bigint' ? value.toString() : value);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function inspect(input, output, index) {
  const html = fs.readFileSync(input, 'utf8');
  const errors = [], canvases = new WeakMap();
  const geometry = element => element.id === 'space-canvas' ? {width:1280,height:720} : {width:600,height:180};
  const native = element => {
    if (!canvases.has(element)) canvases.set(element, createCanvas(Math.max(1,element.width),Math.max(1,element.height)));
    return canvases.get(element);
  };
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', error => errors.push(String(error.stack || error)));
  virtualConsole.on('error', (...args) => errors.push(args.map(String).join(' ')));
  const dom = new JSDOM(html, {url:'https://presenter.invalid/', runScripts:'dangerously', pretendToBeVisual:true, virtualConsole,
    beforeParse(window) {
      window.TextEncoder=TextEncoder; window.TextDecoder=TextDecoder;
      Object.defineProperty(window.crypto,'subtle',{value:crypto.webcrypto.subtle});
      window.devicePixelRatio=1;
      window.matchMedia=()=>({matches:true,addEventListener(){},removeEventListener(){}});
      window.scrollTo=()=>{};
      for (const name of ['scrollIntoView','setPointerCapture','releasePointerCapture']) window.HTMLElement.prototype[name]=()=>{};
      window.HTMLElement.prototype.getBoundingClientRect=function(){const {width,height}=geometry(this);return {x:0,y:0,left:0,top:0,right:width,bottom:height,width,height};};
      for (const name of ['clientWidth','clientHeight','offsetWidth','offsetHeight']) Object.defineProperty(window.HTMLElement.prototype,name,{get(){return geometry(this)[name.endsWith('Width')?'width':'height'];}});
      window.ResizeObserver=class {constructor(callback){this.callback=callback;}observe(target){window.setTimeout(()=>this.callback([{target,contentRect:target.getBoundingClientRect()}]),0);}unobserve(){}disconnect(){}};
      for (const name of ['width','height']) {
        const descriptor=Object.getOwnPropertyDescriptor(window.HTMLCanvasElement.prototype,name);
        Object.defineProperty(window.HTMLCanvasElement.prototype,name,{get:descriptor.get,set(value){descriptor.set.call(this,value);if(canvases.has(this))native(this)[name]=Math.max(1,this[name]);}});
      }
      window.HTMLCanvasElement.prototype.getContext=function(kind){assert.equal(kind,'2d');return native(this).getContext(kind);};
      window.addEventListener('error',event=>errors.push(String(event.error||event.message)));
    }
  });
  try {
    const w=dom.window, d=w.document, get=id=>{const e=d.getElementById(id);assert(e,'Missing '+id);return e;};
    const wait=async predicate=>{const deadline=Date.now()+20000;while(!predicate()){assert(Date.now()<deadline,'Presenter startup/playback timeout');assert.deepEqual(errors,[]);await sleep(10);}};
    const event=(id,type)=>get(id).dispatchEvent(new w.Event(type,{bubbles:true}));
    await wait(()=>w.PresenterUI?.experiment && get('loading').hidden);
    const ui=w.PresenterUI, source=w.PRESENTER_BUNDLE.experiments;
    const options=Array.from(get('experiment').options).map(o=>({id:o.value,title:o.textContent.trim(),hidden:o.hidden,disabled:o.disabled}));
    assert.deepEqual(options.map(o=>o.id),Array.from(source,e=>e.id));
    assert(options.every(o=>o.title && !o.hidden && !o.disabled));
    assert(!get('experiment').closest('[hidden]'),'Experiment selector is hidden in the DOM');
    const checks=[];
    for (const original of source) {
      get('experiment').value=original.id;event('experiment','change');
      assert.equal(ui.experiment.id,original.id);assert.equal(ui.frameIndex,0);
      const before=sha(stable({frames:ui.experiment.frames,coupling:ui.experiment.coupling,readouts:ui.experiment.readouts}));
      assert.equal(d.querySelectorAll('#channel-grid button[data-channel]').length,48);
      for (let frame=0;frame<original.frames.length;frame++) {
        get('scrub').value=String(frame);event('scrub','input');assert.equal(ui.frameIndex,frame);
        assert.equal(get('step').textContent.trim(),String(original.frames[frame].step));
        assert.equal(get('state-hash').textContent.trim(),original.frames[frame].state_sha256);
      }
      get('rewind').click();assert.equal(ui.frameIndex,0);
      get('next').click();assert.equal(ui.frameIndex,1);
      get('prev').click();assert.equal(ui.frameIndex,0);
      const reset=stable(ui.camera), canvas=get('space-canvas');
      const pointer=(type,x,y)=>{const e=new w.Event(type,{bubbles:true,cancelable:true});Object.assign(e,{pointerId:1,pointerType:'mouse',button:0,clientX:x,clientY:y});canvas.dispatchEvent(e);};
      pointer('pointerdown',100,100);pointer('pointermove',145,125);pointer('pointerup',145,125);
      assert.notEqual(stable(ui.camera),reset,'Synthetic drag did not rotate the cube');
      canvas.dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));
      get('focus-state').click();get('fit').click();assert.equal(stable(ui.camera),reset,'Reset did not restore whole cube');
      const c=ui.camera,{width,height}=geometry(canvas),co=Math.cos(c.yaw),si=Math.sin(c.yaw),cp=Math.cos(c.pitch),sp=Math.sin(c.pitch);
      const scale=Math.min((width-64)/(Math.abs(co)+Math.abs(si)),(height-80)/(Math.abs(cp)+Math.abs(sp)*(Math.abs(si)+Math.abs(co))))*.88*c.zoom;
      const corners=[];
      for(const x of [0,1])for(const y of [0,1])for(const z of [0,1]){
        const v=[x-c.center[0],y-c.center[1],z-c.center[2]],xx=v[0]*co-v[2]*si,zz=v[0]*si+v[2]*co;
        const p={x:width/2+xx*scale,y:height*.46-(v[1]*cp-zz*sp)*scale};
        assert(p.x>=0&&p.x<=width&&p.y>=0&&p.y<=height,'Whole-cube corner clipped');corners.push(p);
      }
      assert.equal(sha(stable({frames:ui.experiment.frames,coupling:ui.experiment.coupling,readouts:ui.experiment.readouts})),before,'Presentation mutated a retained experiment');
      checks.push({experiment:original.id,frames:original.frames.length,all48_channels:true,all_saved_steps_and_hashes:true,stepping:true,synthetic_drag_rotation:true,reset_whole_cube:true,eight_corners_inside:true,corners,retained_state_sha256:before});
    }
    get('experiment').value=source[0].id;event('experiment','change');get('speed').value='2';event('speed','change');get('play').click();
    await wait(()=>ui.frameIndex>0);get('play').click();const paused=ui.frameIndex;await sleep(550);assert.equal(ui.frameIndex,paused,'Pause did not stop playback');
    get('rewind').click();get('fit').click();
    const canvas=native(get('space-canvas')),composite=createCanvas(canvas.width,canvas.height),ctx=composite.getContext('2d');
    const background=w.getComputedStyle(d.documentElement).getPropertyValue('--navy').trim();assert(background);
    ctx.fillStyle=background;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(canvas,0,0);
    const image=`bundle-${index+1}-whole-cube.png`,bytes=composite.toBuffer('image/png');fs.writeFileSync(path.join(output,image),bytes,{flag:'wx'});
    assert.deepEqual(errors,[]);
    return {input:path.relative(process.cwd(),input),input_sha256:sha(html),selector_entries:options,checks,play_and_pause:true,errors,canvas_image:image,canvas_image_sha256:sha(bytes),canvas_image_scope:'Actual native Canvas2D composited over its declared CSS navy; no browser layout screenshot'};
  } finally {dom.window.close();}
}

async function main(){
  const [outputArg,...inputs]=process.argv.slice(2);assert(outputArg&&inputs.length,'Usage: presenter_smoke.cjs NEW_OUTPUT_DIR HTML...');
  const output=path.resolve(outputArg);fs.mkdirSync(output,{recursive:false});
  const report={format:'universe24-message-presenter-smoke-v1',passed:false,scope:'Unchanged application JavaScript and native Canvas2D with explicit geometry. DOM options and synthetic event handlers tested. No actual browser CSS, native pointer hit testing, Safari, iPad or attachment preview execution claim.',source_sha256:sha(fs.readFileSync(__filename)),dependencies:{node:process.version,jsdom:require('jsdom/package.json').version,canvas:require('@napi-rs/canvas/package.json').version},bundles:[]};
  try{for(const [index,input]of inputs.entries())report.bundles.push(await inspect(path.resolve(input),output,index));report.passed=true;}
  catch(error){report.failure={message:error.message,stack:error.stack};throw error;}
  finally{fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');}
  process.stdout.write(JSON.stringify({passed:report.passed,bundles:report.bundles.length,experiments:report.bundles.reduce((n,b)=>n+b.checks.length,0)})+'\n');
}
main().catch(error=>{process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;});
