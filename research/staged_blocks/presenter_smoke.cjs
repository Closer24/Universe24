#!/usr/bin/env node
'use strict';

// Derived from research/message_mechanism/presenter_smoke.cjs.
// Exercise unchanged Presenter scripts and native Canvas2D with explicit geometry.
// This is not a browser CSS layout, native pointer hit test, Safari or iPad test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {TextEncoder, TextDecoder} = require('node:util');
const {JSDOM, VirtualConsole} = require('jsdom');
const {createCanvas,loadImage} = require('@napi-rs/canvas');
const zlib = require('node:zlib');
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const stable = data => JSON.stringify(data, (_key, value) => typeof value === 'bigint' ? value.toString() : value);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function inspect(input, output, index, imagePlan, animationPlan) {
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
      // Independently derive every stored arithmetic event, then inspect one
      // representative of each class actually present in this recording.
      const key = a => a.join(','), representatives = new Map();
      let rawEvents = 0;
      const maps = original.frames.map(f => new Map(f.cells.map(row => [key(row.slice(0,4)), row.slice(4)])));
      const at = (frame, a) => { const v = maps[frame].get(key(a)) || original.background; return [BigInt(v[0]),BigInt(v[1]),Number(v[2])]; };
      for(let frame=1;frame<original.frames.length;frame++) {
        const addresses = new Set([...maps[frame-1].keys(),...maps[frame].keys()]);
        for(const addressKey of addresses) {
          const a=addressKey.split(',').map(Number), before=at(frame-1,a), after=at(frame,a);
          const ell=after[1]+before[0], changed=before.some((v,i)=>v!==after[i]);
          if(ell===0n || !changed) continue;
          let u=0n;
          for(let direction=0;direction<6;direction++) {
            const offset=original.coupling.directions[direction];
            const neighbor=a.slice(0,3).map((v,i)=>(v+offset[i]+original.side)%original.side);
            neighbor.push(original.coupling.ports[direction][a[3]]);
            u+=BigInt(original.coupling.weights[direction][a[3]])*at(frame-1,neighbor)[1];
          }
          assert.equal(6n*ell+BigInt(after[2]),2n*u+BigInt(before[2]));
          const kind=Number((u%3n+3n)%3n);rawEvents++;
          if(!representatives.has(kind)) representatives.set(kind,{frame,a,ell,u});
        }
      }
      for(const [kind, sample] of representatives) {
        for(const [i,id] of ['node-x','node-y','node-z'].entries()) get(id).value=String(sample.a[i]);
        event('node-form','submit');get('channel-select').value=String(sample.a[3]);event('channel-select','change');
        get('scrub').value=String(sample.frame);event('scrub','input');
        get('inspect').click();get('show-evidence').click();
        assert.match(get('arithmetic-event').textContent,new RegExp('Arithmetic C'+kind+' event'));
        assert.equal(get('algebra-quotient').textContent.trim(),String(sample.ell));
        assert.equal(get('algebra-u').textContent.trim(),String(sample.u));
        assert.equal(get('neighbor-list').children.length,6);
        assert(!get('evidence').hidden,'Exact arithmetic evidence panel is hidden');
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
      checks.push({experiment:original.id,frames:original.frames.length,all48_channels:true,all_saved_steps_and_hashes:true,raw_arithmetic_events:rawEvents,inspected_C_classes:Array.from(representatives.keys()),raw_C_labels_preserved:true,stepping:true,synthetic_drag_rotation:true,reset_whole_cube:true,eight_corners_inside:true,corners,retained_state_sha256:before});
    }
    get('experiment').value=source[0].id;event('experiment','change');get('speed').value='2';event('speed','change');get('play').click();
    await wait(()=>ui.frameIndex>0);get('play').click();const paused=ui.frameIndex;await sleep(550);assert.equal(ui.frameIndex,paused,'Pause did not stop playback');
    get('rewind').click();get('fit').click();
    const canvas=native(get('space-canvas')),composite=createCanvas(canvas.width,canvas.height),ctx=composite.getContext('2d');
    const background=w.getComputedStyle(d.documentElement).getPropertyValue('--navy').trim();assert(background);
    ctx.fillStyle=background;ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(canvas,0,0);
    const image=`bundle-${index+1}-whole-cube.png`,bytes=composite.toBuffer('image/png');fs.writeFileSync(path.join(output,image),bytes,{flag:'wx'});
    const additionalImages=[];
    for(const item of imagePlan.filter(item=>source.some(e=>e.id===item.experiment))) {
      assert(/^[a-z0-9-]+\.png$/.test(item.name),'Image name must be a plain PNG filename');
      get('experiment').value=item.experiment;event('experiment','change');
      assert(Number.isInteger(item.frame)&&item.frame>=0&&item.frame<ui.experiment.frames.length,'Invalid recorded image frame');
      get('scrub').value=String(item.frame);event('scrub','input');get('fit').click();
      const painted=native(get('space-canvas')),still=createCanvas(painted.width,painted.height),context=still.getContext('2d');
      context.fillStyle=background;context.fillRect(0,0,painted.width,painted.height);context.drawImage(painted,0,0);
      const raw=still.toBuffer('image/png');fs.writeFileSync(path.join(output,item.name),raw,{flag:'wx'});
      additionalImages.push({...item,step:ui.experiment.frames[item.frame].step,state_sha256:ui.experiment.frames[item.frame].state_sha256,image_sha256:sha(raw),scope:'Static native Canvas2D rendering of a recorded state; explicit geometry; not browser layout or interactive playback'});
    }
    const animations=[];
    for(const item of animationPlan.filter(item=>source.some(e=>e.id===item.experiment))) {
      assert(/^[a-z0-9-]+$/.test(item.name),'Animation name must be a plain identifier');
      const recordBytes=fs.readFileSync(item.source_record);
      assert.equal(sha(recordBytes),item.source_record_sha256,'Animation role source changed');
      const sourceRecord=JSON.parse(item.source_record.endsWith('.gz')?zlib.gunzipSync(recordBytes):recordBytes);
      assert.equal(sourceRecord.experiment.id,item.experiment);
      for(const panel of item.panels||[])assert.deepEqual(panel.address,sourceRecord.assembly.ports[panel.port][panel.index],'Panel address must come from its saved assembly port');
      const framesDirectory=path.join(output,item.name+'-frames');fs.mkdirSync(framesDirectory);
      get('experiment').value=item.experiment;event('experiment','change');get('fit').click();
      const original=source.find(e=>e.id===item.experiment), frames=[];
      const maps=original.frames.map(f=>new Map(f.cells.map(row=>[row.slice(0,4).join(','),row.slice(4)])));
      for(let frame=0;frame<original.frames.length;frame++) {
        for(const [i,id] of ['node-x','node-y','node-z'].entries())get(id).value=String(original.view.position[i]);
        event('node-form','submit');get('channel-select').value=String(original.view.channel);event('channel-select','change');
        get('scrub').value=String(frame);event('scrub','input');
        let count=0;
        if(frame>0)for(const key of new Set([...maps[frame-1].keys(),...maps[frame].keys()])) {
          const old=maps[frame-1].get(key)||original.background, next=maps[frame].get(key)||original.background;
          if(BigInt(next[1])+BigInt(old[0])!==0n && old.some((v,i)=>String(v)!==String(next[i])))count++;
        }
        const painted=native(get('space-canvas')),panelWidth=item.panels?.length?500:0,still=createCanvas(painted.width+panelWidth,painted.height+74),context=still.getContext('2d');
        context.fillStyle=background;context.fillRect(0,0,still.width,still.height);context.drawImage(painted,0,74);
        context.fillStyle='#eef2e9';context.font='20px sans-serif';context.fillText(original.title,24,28);
        context.font='15px sans-serif';context.fillStyle='#c4d2d0';
        context.fillText('Recorded board state '+original.frames[frame].step+' / '+original.frames.at(-1).step+' | Raw arithmetic C this update: '+(frame===0?'no preceding transition':count)+' | Prepared-clock rotation is not a click',24,55);
        const panelStates=[];
        for(const [index,panel] of (item.panels||[]).entries()) {
          for(const [i,id] of ['node-x','node-y','node-z'].entries())get(id).value=String(panel.address[i]);
          event('node-form','submit');get('channel-select').value=String(panel.address[3]);event('channel-select','change');
          get('inspect').click();get('show-evidence').click();
          const x=painted.width+16,y=74+index*240;
          context.strokeStyle='#526f76';context.strokeRect(x-8,y,panelWidth-24,232);
          context.fillStyle='#eef2e9';context.font='18px sans-serif';context.fillText(panel.label,x+6,y+28);
          const svgImage=async id=>loadImage(Buffer.from(get(id).innerHTML.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ')));
          context.drawImage(await svgImage('large-clock'),x+12,y+43,140,140);
          context.drawImage(await svgImage('large-gear'),x+165,y+56,114,114);
          const a=get('counter-a').textContent.trim(),b=get('counter-b').textContent.trim(),r=get('remainder').textContent.trim();
          const expected=maps[frame].get(panel.address.join(','))||original.background;
          assert.deepEqual([a,b,r],Array.from(expected,String),'Panel shows exact saved counter/remainder triple');
          const eventText=get('arithmetic-event').textContent.trim();
          const kind=(eventText.match(/Arithmetic C([012]) event/)||[])[1];
          context.font='17px sans-serif';context.fillText('a = '+a+'   b = '+b+'   r = '+r,x+292,y+83);
          context.fillText('Raw C: '+(frame===0?'snapshot':kind===undefined?'none':'C'+kind),x+292,y+119);
          let inputTerms=null;
          if(panel.show_inputs && frame>0) {
            const transition=w.PresenterData.transition(ui.experiment,frame,panel.address);
            inputTerms=Array.from(transition.inputs,input=>String(input.product));
            assert.equal(inputTerms.reduce((sum,v)=>sum+BigInt(v),0n).toString(),get('algebra-u').textContent.trim());
            context.font='16px sans-serif';context.fillText('u = '+transition.u,x+292,y+151);
            context.fillText('ell = '+transition.ell,x+292,y+176);
            context.font='14px sans-serif';context.fillText('Terms from previous state: ['+inputTerms.join(', ')+']',x+12,y+193);
          }
          context.font='14px sans-serif';context.fillStyle='#c4d2d0';context.fillText('Node '+panel.address.slice(0,3).join(', ')+' | channel '+panel.address[3],x+12,y+210);
          panelStates.push({port:panel.port,address:panel.address,a,b,r,raw_C:kind===undefined?null:Number(kind),six_signed_input_terms:inputTerms,input_terms_source_step:inputTerms===null?null:original.frames[frame-1].step});
        }
        let comparison=null;
        if(item.comparison) {
          assert.equal(item.comparison.kind,'counter_dot_cross');
          assert.equal(panelStates.length,2,'The comparison layout needs two declared panels');
          const [target,reference]=item.comparison.panels.map(index=>panelStates[index]);
          const a=BigInt(target.a),b=BigInt(target.b),c=BigInt(reference.a),d0=BigInt(reference.b);
          const D=a*c+b*d0,X=a*d0-b*c;
          const recorded=sourceRecord.observations[item.comparison.trace_field][frame];
          assert.equal(String(D),String(recorded.D));assert.equal(String(X),String(recorded.X));
          comparison={D:String(D),X:String(X),passive:true,recorded_trace_verified:true};
          const x=painted.width+16,y=574;
          context.strokeStyle='#526f76';context.strokeRect(x-8,y,panelWidth-24,190);
          context.fillStyle='#eef2e9';context.font='20px sans-serif';context.fillText('Passive relative-phase record',x+10,y+33);
          context.font='30px sans-serif';context.fillText('D = '+D+'     X = '+X,x+10,y+83);
          context.fillStyle='#c4d2d0';context.font='15px sans-serif';
          context.fillText('D = a(target) a(ref) + b(target) b(ref)',x+10,y+121);
          context.fillText('X = a(target) b(ref) - b(target) a(ref)',x+10,y+146);
          context.fillText('Readout only; no implemented comparison gate',x+10,y+172);
        }
        const name='frame-'+String(frame).padStart(4,'0')+'.png',raw=still.toBuffer('image/png');
        fs.writeFileSync(path.join(framesDirectory,name),raw,{flag:'wx'});
        frames.push({file:item.name+'-frames/'+name,frame,step:original.frames[frame].step,state_sha256:original.frames[frame].state_sha256,png_sha256:sha(raw),raw_arithmetic_C:frame===0?null:count,panels:panelStates,comparison});
      }
      animations.push({...item,frames,scope:'Every image is one saved native state rendered by unchanged Presenter Canvas2D with an emulated viewport; no interpolated states or new evolution; replay restarts after the final state'});
    }
    assert.deepEqual(errors,[]);
    return {input:path.relative(process.cwd(),input),input_sha256:sha(html),selector_entries:options,checks,play_and_pause:true,errors,canvas_image:image,canvas_image_sha256:sha(bytes),canvas_image_scope:'Actual native Canvas2D composited over its declared CSS navy; no browser layout screenshot',additional_images:additionalImages,animations};
  } finally {dom.window.close();}
}

async function main(){
  const [outputArg,...inputs]=process.argv.slice(2);assert(outputArg&&inputs.length,'Usage: presenter_smoke.cjs NEW_OUTPUT_DIR HTML...');
  const output=path.resolve(outputArg);fs.mkdirSync(output,{recursive:false});
  const planPath=process.env.STAGED_PRESENTER_IMAGE_PLAN;
  const imagePlan=planPath?JSON.parse(fs.readFileSync(planPath,'utf8')):[];
  assert(Array.isArray(imagePlan),'Image plan must be an array');
  assert.equal(new Set(imagePlan.map(item=>item.name)).size,imagePlan.length,'Image names must be unique');
  const animationPlanPath=process.env.STAGED_PRESENTER_ANIMATION_PLAN;
  const animationPlan=animationPlanPath?JSON.parse(fs.readFileSync(animationPlanPath,'utf8')):[];
  assert(Array.isArray(animationPlan),'Animation plan must be an array');
  assert.equal(new Set(animationPlan.map(item=>item.name)).size,animationPlan.length,'Animation names must be unique');
  const report={format:'universe24-staged-presenter-smoke-v1',passed:false,scope:'Unchanged application JavaScript and native Canvas2D with explicit geometry. DOM options and synthetic event handlers tested. No actual browser CSS, native pointer hit testing, Safari, iPad or attachment preview execution claim.',source_sha256:sha(fs.readFileSync(__filename)),dependencies:{node:process.version,jsdom:require('jsdom/package.json').version,canvas:require('@napi-rs/canvas/package.json').version},bundles:[]};
  if(planPath)report.image_plan={path:path.relative(process.cwd(),planPath),sha256:sha(fs.readFileSync(planPath))};
  if(animationPlanPath)report.animation_plan={path:path.relative(process.cwd(),animationPlanPath),sha256:sha(fs.readFileSync(animationPlanPath))};
  try{for(const [index,input]of inputs.entries())report.bundles.push(await inspect(path.resolve(input),output,index,imagePlan,animationPlan));assert.equal(report.bundles.reduce((n,b)=>n+b.additional_images.length,0),imagePlan.length,'Every requested recorded image must be produced exactly once');assert.equal(report.bundles.reduce((n,b)=>n+b.animations.length,0),animationPlan.length,'Every requested animation must be produced exactly once');report.passed=true;}
  catch(error){report.failure={message:error.message,stack:error.stack};throw error;}
  finally{fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');}
  process.stdout.write(JSON.stringify({passed:report.passed,bundles:report.bundles.length,experiments:report.bundles.reduce((n,b)=>n+b.checks.length,0)})+'\n');
}
main().catch(error=>{process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;});
