/* The Presenter: passive views of complete, independently validated recordings. */
(() => {
  'use strict';
  const startup = globalThis.PresenterStartup;
  if (startup && startup.isBlocked()) return;
  const D = globalThis.PresenterData;
  if (!D) {
    if (startup) startup.failed('The Presenter data module is missing. Open the complete standalone HTML file, or keep data.js beside this source page.');
    return;
  }
  const $ = id => document.getElementById(id);
  const text = (id, value) => { $(id).textContent = String(value); };
  const visible = (id, show) => { $(id).hidden = !show; };
  const colors = ['#9fafac','#bdd0b5','#ddc37f','#e29d76','#c99cac','#8dcac5'];
  const camera = {yaw:-0.65,pitch:0.42,zoom:1};
  let viewCenter=[0.5,0.5,0.5];
  let bundle = {experiments:[],catalog:[]}, experimentIndex = 0, frameIndex = 0;
  let selection = {position:[0,0,0],channel:0};
  let timer = null, importing = false, readoutPage = 0, hits = [], activePointers = new Map();
  let pointerStart = null, dragDistance = 0, pinchDistance = null, importSequence = 0;
  let previousFocus = null, evidenceFocus = null, resizePending = false;
  const historyCache = new WeakMap();
  const experiment = () => bundle.experiments[experimentIndex] || null;
  const address = () => [...selection.position, selection.channel];
  const samePosition = (a,b) => a.every((v,i) => v === b[i]);
  const svgNS = 'http://www.w3.org/2000/svg';
  const error = message => { text('error',message); visible('error',true); };
  const announce = message => text('announcement',message);
  const clamp = (n,min,max) => Math.min(max,Math.max(min,n));
  function integerInput(input, max, name) {
    if (!/^(0|[1-9]\d*)$/.test(input.value)) throw new Error(`${name} must be a nonnegative integer.`);
    const n = Number(input.value);
    if (!Number.isSafeInteger(n) || n > max) throw new Error(`${name} must be between 0 and ${max}.`);
    return n;
  }
  function clockSVG(a,b,r,mini=false) {
    const p = D.phase(a,b), cx=50,cy=50,rad=35;
    let marks='';
    for(let k=0;k<12;k++){const t=k*Math.PI/6;marks+=`<line x1="${cx+31*Math.sin(t)}" y1="${cy-31*Math.cos(t)}" x2="${cx+35*Math.sin(t)}" y2="${cy-35*Math.cos(t)}"/>`;}
    const hand=p.atRest?'<circle cx="50" cy="50" r="3" fill="#9aa9a1"/>':`<line x1="50" y1="50" x2="${cx+p.x*27}" y2="${cy-p.y*27}" stroke="#168b88" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="50" r="3.5" fill="#168b88"/>`;
    let gear='';
    if(mini){for(let k=0;k<6;k++){const t=k*Math.PI/3-Math.PI/2;gear+=`<circle cx="${81+9*Math.cos(t)}" cy="${79+9*Math.sin(t)}" r="${k===r?2.9:1.5}" fill="${k===r?'#df8c6f':'#cbd3c6'}"/>`;}gear=`<circle cx="81" cy="79" r="13" fill="#fffaf1" stroke="#d8dacf"/>${gear}`;}
    return `<svg class="counter-clock" viewBox="0 0 100 100" role="img" aria-label="${p.atRest?'Counters at rest':'Counter direction'}${mini?`, remainder ${r}`:''}"><circle cx="50" cy="50" r="40" fill="${mini?'none':'#eef2e9'}" stroke="#cbd6c9" stroke-width="1"/><g stroke="#9aaa9f" stroke-width="1">${marks}</g>${hand}${mini?gear:'<text x="88" y="53" font-size="7" fill="#7d918c">a</text><text x="48" y="6" font-size="7" fill="#7d918c">b</text>'}</svg>`;
  }
  function gearSVG(r) {
    let teeth='',slots='';
    for(let k=0;k<12;k++){const t=k*Math.PI/6;teeth+=`<line x1="${50+33*Math.sin(t)}" y1="${50-33*Math.cos(t)}" x2="${50+41*Math.sin(t)}" y2="${50-41*Math.cos(t)}" stroke="#bb9b79" stroke-width="6"/>`;}
    for(let k=0;k<6;k++){const t=k*Math.PI/3-Math.PI/2,x=50+25*Math.cos(t),y=50+25*Math.sin(t);slots+=`<circle cx="${x}" cy="${y}" r="${k===r?8:6}" fill="${k===r?'#df8c6f':'#efdfc5'}"/><text x="${x}" y="${y+2.8}" text-anchor="middle" font-size="8" fill="${k===r?'#fffaf1':'#927e65'}">${k}</text>`;}
    return `<svg class="remainder-gear" viewBox="0 0 100 100" role="img" aria-label="Retained remainder ${r}, theta ${Math.floor(r/2)}, parity ${r%2}">${teeth}<circle cx="50" cy="50" r="35" fill="#f4e9d6" stroke="#bb9b79" stroke-width="1.5"/>${slots}<circle cx="50" cy="50" r="8" fill="#fffaf1" stroke="#cfba98"/><text x="50" y="53" text-anchor="middle" font-size="9" fill="#a17c54">r</text></svg>`;
  }
  function setPlaying(play) {
    if(timer){clearInterval(timer);timer=null;}
    const e=experiment();
    if(play && e && e.frames.length>1 && !importing){
      if(frameIndex===e.frames.length-1) setFrame(0);
      timer=setInterval(()=>{if(frameIndex>=e.frames.length-1){setPlaying(false);return;}setFrame(frameIndex+1);if(frameIndex===e.frames.length-1)setPlaying(false);},1000/Number($('speed').value));
    }
    $('play').innerHTML=timer?'Ⅱ <span>Pause</span>':'▶ <span>Play</span>';
    $('play').setAttribute('aria-label',timer?'Pause recorded states':'Play recorded states');
    $('play').setAttribute('aria-pressed',String(Boolean(timer)));
  }
  function setFrame(n) {const e=experiment();if(!e)return;frameIndex=clamp(n,0,e.frames.length-1);render();}
  function selectAddress(pos,g,open=false) {
    selection={position:[...pos],channel:g};
    $('channel-select').value=String(g);render();
    if(open)openInspector();
  }
  function openInspector() {
    if(!experiment())return;
    previousFocus=document.activeElement;visible('inspector',true);visible('inspector-backdrop',true);
    $('close-inspector').focus();renderInspection();
  }
  function closeInspector() {visible('inspector',false);visible('inspector-backdrop',false);if(previousFocus&&previousFocus.isConnected)previousFocus.focus();}
  function openEvidence() {
    if(!experiment())return;
    evidenceFocus=document.activeElement;visible('evidence',true);visible('evidence-backdrop',true);
    renderInspection();renderHistory();$('close-evidence').focus();
  }
  function closeEvidence() {visible('evidence',false);visible('evidence-backdrop',false);if(evidenceFocus&&evidenceFocus.isConnected)evidenceFocus.focus();}
  async function importText(source) {
    const sequence=++importSequence;setPlaying(false);importing=true;
    visible('error',false);visible('loading',true);text('loading-text','Checking the complete recorded state…');
    try {
      const next=await D.load(source,bundle.catalog||[],{onProgress(p){if(sequence!==importSequence)return;if(p.phase==='validate')text('loading-text',`Checking experiment ${p.experiment||1}${p.totalExperiments?' of '+p.totalExperiments:''} · frame ${p.frame||0}${p.totalFrames?' of '+p.totalFrames:''}…`);}});
      if(sequence!==importSequence)return false;
      bundle=next;experimentIndex=0;frameIndex=0;readoutPage=0;
      const options=document.createDocumentFragment();
      for(const e of bundle.experiments){const option=document.createElement('option');option.textContent=e.title||e.id;option.value=e.id;options.append(option);}
      $('experiment').replaceChildren(options);
      visible('workspace',bundle.experiments.length>0);visible('empty',bundle.experiments.length===0);
      if(bundle.experiments.length)selectExperiment(0);
      announce(bundle.experiments.length?`Loaded ${bundle.experiments.length} verified recorded experiment${bundle.experiments.length===1?'':'s'}.`:'Ready to open an experiment.');
      if (startup) startup.complete();
      return true;
    } catch(err) {if(sequence===importSequence){error(`Could not open this recording: ${err.message}.${experiment()?' The previous experiment has been kept.':''}`);if(!experiment()){visible('empty',true);if(startup)startup.failed('The recording could not be opened: '+err.message);}}return false;}
    finally{if(sequence===importSequence){importing=false;visible('loading',false);}}
  }
  async function importFile(file) {
    if(!file)return;
    if(file.size>D.limits.maxBytes){error(`File exceeds the ${Math.floor(D.limits.maxBytes/1048576)} MiB import limit. The previous experiment has been kept.`);return;}
    try{await importText(await file.text());}catch(err){error(`Could not read this file: ${err.message}`);}
    $('file-input').value='';
  }
  function selectExperiment(index) {
    setPlaying(false);experimentIndex=index;frameIndex=0;readoutPage=0;
    const e=experiment(),first=e.frames[0].cells[0];
    selection=e.view?{position:[...e.view.position],channel:e.view.channel}:{position:first?first.slice(0,3):[0,0,0],channel:first?first[3]:0};
    $('experiment').value=e.id;$('channel-select').value=String(selection.channel);
    for(const id of ['node-x','node-y','node-z','slice'])$(id).max=String(e.side-1);
    $('slice').value=String(selection.position[2]);$('projection').value='iso';$('field-filter').value='all';
    Object.assign(camera,{yaw:-0.65,pitch:0.42,zoom:1});viewCenter=[0.5,0.5,0.5];
    closeEvidence();closeInspector();render();
  }
  function render() {
    const e=experiment();if(!e)return;
    const frame=e.frames[frameIndex],ns=D.nodes(e,frameIndex),validation=e.validation||{};
    text('run-title',e.title||e.id);text('run-description',e.description||'');
    text('step',frame.step);text('last-step',`of ${e.frames[e.frames.length-1].step}`);text('first-step',e.frames[0].step);text('end-step',e.frames[e.frames.length-1].step);
    $('scrub').max=String(e.frames.length-1);$('scrub').value=String(frameIndex);$('scrub').disabled=e.frames.length===1;
    $('scrub').setAttribute('aria-valuetext',`Recorded step ${frame.step}`);
    $('prev').disabled=frameIndex===0;$('rewind').disabled=frameIndex===0;$('next').disabled=frameIndex===e.frames.length-1;$('play').disabled=e.frames.length===1;
    const snapshot=e.frames.length===1;
    text('status',snapshot?'Snapshot · no transition':`${validation.transitions??e.frames.length-1} checked transitions`);$('status').classList.toggle('snapshot',snapshot);
    text('cube-side',`${e.side}³`);text('stored-count',frame.cells.length.toLocaleString('en-US'));text('node-count',ns.length.toLocaleString('en-US'));
    text('state-hash',frame.state_sha256||'No claimed hash');text('coupling-hash',e.coupling.fingerprint);text('coupling-signs',e.coupling.body_signs.join(', '));text('background',`(${e.background.join(', ')})`);
    const sites=BigInt(e.side)**3n;text('logical-size',`${sites} sites; ${48n*sites} channels`);
    text('validation-detail',snapshot?`Complete snapshot checked; no forward transition is present. ${validation.hashes_verified??0} hashes verified. No physical validation claimed.`:`${validation.transitions??e.frames.length-1} complete forward transitions and inverses checked; ${validation.hashes_verified??0} hashes verified. No physical validation claimed.`);
    text('provenance-json',JSON.stringify(e.provenance||{},null,2));
    const limits=D.limits;text('resource-limits',`Import limits: ${Math.floor(limits.maxBytes/1048576)} MiB, ${limits.maxFrames.toLocaleString('en-US')} frames, ${limits.maxStoredCells.toLocaleString('en-US')} stored cells, ${limits.maxExperiments} experiments and ${limits.maxCounterDigits.toLocaleString('en-US')} decimal digits per counter. Complete states are checked before display. Background positions stay addressable even when not individually drawn.`);
    renderInspection();renderSpace(ns);if(!$('evidence').hidden)renderHistory();
  }
  function renderInspection() {
    const e=experiment();if(!e)return;
    const pos=selection.position,g=selection.channel,now=D.at(e,frameIndex,address());
    text('node-title',`Node (${pos.join(', ')})`);['node-x','node-y','node-z'].forEach((id,i)=>{$(id).value=String(pos[i]);});
    text('selected-channel',g);text('channel-position',`(${pos.join(', ')})`);
    const tiles=document.createDocumentFragment();let counterCount=0,remainderCount=0;
    for(let c=0;c<48;c++){
      const [a,b,r]=D.at(e,frameIndex,[...pos,c]),counters=a!==0n||b!==0n,rem=!counters&&r!==e.background[2];
      if(counters)counterCount++;if(rem)remainderCount++;
      const button=document.createElement('button');button.type='button';button.dataset.channel=String(c);button.className=`channel-tile${c===g?' selected':''}${counters?' has-counters':''}${rem?' remainder-only':''}`;
      button.setAttribute('aria-label',`Channel ${c}, ${counters?'nonzero counters':rem?'remainder-only state':'background'}, remainder ${r}`);button.setAttribute('aria-pressed',String(c===g));
      button.innerHTML=clockSVG(a,b,r,true)+`<span class="tile-g">${c}</span><span class="tile-r">${r}</span>`;
      button.addEventListener('click',()=>selectAddress(pos,c));tiles.append(button);
    }
    $('channel-grid').replaceChildren(tiles);text('node-summary',`${counterCount} channels with nonzero counters · ${remainderCount} remainder-only deviations`);
    $('large-clock').innerHTML=clockSVG(now[0],now[1],now[2]);$('large-gear').innerHTML=gearSVG(now[2]);
    text('counter-a',now[0]);text('counter-b',now[1]);text('remainder',now[2]);text('theta',Math.floor(now[2]/2));text('parity',now[2]%2);
    const rest=now[0]===0n&&now[1]===0n,background=rest&&now[2]===e.background[2];
    text('channel-state-kind',background?'Background state':rest?'Counters at rest · retained remainder differs from background':'Nonzero counters · state recorded exactly');
    $('channel-state-kind').className=`state-kind${background?' background':rest?' remainder':''}`;
    renderAlgebra();renderReadouts();
  }
  function wrapNeighbor(pos,direction,side) {return pos.map((v,i)=>direction[i]===1?(v===side-1?0:v+1):direction[i]===-1?(v===0?side-1:v-1):v);}
  function renderAlgebra() {
    const e=experiment(),tr=D.transition(e,frameIndex,address());let inputs;
    if(tr){
      text('transition-label',`Recorded step ${e.frames[frameIndex-1].step} → ${e.frames[frameIndex].step}`);text('transition-status',tr.ok?'Selected update matches Rule3':'Update mismatch');
      text('algebra-u',tr.u);text('algebra-numerator',tr.numerator);text('algebra-quotient',tr.ell);text('algebra-remainder',tr.remainder);
      text('a-update',`${tr.old[1]} → ${tr.next[0]}`);text('b-update',`${tr.ell} − (${tr.old[0]}) = ${tr.next[1]}`);
      const changed=tr.old.some((v,i)=>v!==tr.next[i]);
      text('arithmetic-event',tr.ell!==0n&&changed?`Arithmetic C${((tr.u%3n)+3n)%3n} event: ℓ ≠ 0 and the full local triple changed. This is an external arithmetic label, not a detector click.`:'No arithmetic C event: the ℓ ≠ 0 and changed-triple guard is not satisfied.');
      text('neighbors-label','Six signed input clocks · previous snapshot');inputs=tr.inputs;
    } else {
      text('transition-label','Snapshot only · no preceding recorded state');text('transition-status','Snapshot · no update claim');
      for(const id of ['algebra-u','algebra-numerator','algebra-quotient','algebra-remainder','a-update','b-update'])text(id,'—');
      text('arithmetic-event','No transition is inferred from the first loaded snapshot.');text('neighbors-label','Six fixed input clocks · current snapshot');
      inputs=e.coupling.directions.map((direction,d)=>{const addr=[...wrapNeighbor(selection.position,direction,e.side),e.coupling.ports[d][selection.channel]],b=D.at(e,frameIndex,addr)[1],weight=e.coupling.weights[d][selection.channel];return {direction,address:addr,weight,b,product:b*BigInt(weight)};});
    }
    const frag=document.createDocumentFragment();
    inputs.forEach((input,i)=>{
      const card=document.createElement('div');card.className='neighbor';
      const top=document.createElement('div');top.className='neighbor-top';
      const button=document.createElement('button');button.type='button';button.dataset.neighbor=String(i);button.dataset.address=JSON.stringify(input.address);
      const values=D.at(e,tr?frameIndex-1:frameIndex,input.address),icon=document.createElement('span');icon.innerHTML=clockSVG(values[0],values[1],values[2],true);
      const caption=document.createElement('span'),name=document.createElement('strong'),small=document.createElement('small');
      const axis=input.direction.findIndex(v=>v!==0);name.textContent=`${input.direction[axis]>0?'+':'−'}${'XYZ'[axis]} · channel ${input.address[3]}`;small.textContent=`(${input.address.slice(0,3).join(', ')})`;caption.append(name,small);button.append(icon,caption);
      button.addEventListener('click',()=>{selectAddress(input.address.slice(0,3),input.address[3]);announce(`Inspecting neighbor channel ${input.address[3]} at ${input.address.slice(0,3).join(', ')}.`);});
      const weight=document.createElement('span');weight.className=`weight${input.weight<0?' negative':''}`;weight.textContent=`× ${input.weight>0?'+':''}${input.weight}`;top.append(button,weight);
      const nums=document.createElement('div');nums.className='neighbor-values';const bl=document.createElement('span'),pl=document.createElement('span'),bv=document.createElement('code'),pv=document.createElement('code');bl.textContent='b';pl.textContent='w·b';bv.className='neighbor-value';pv.className='neighbor-product';bv.textContent=String(input.b);pv.textContent=String(input.product);nums.append(bl,bv,pl,pv);card.append(top,nums);frag.append(card);
    });$('neighbor-list').replaceChildren(frag);
  }
  function renderReadouts() {
    const e=experiment(),values=D.readouts(e,frameIndex),start=readoutPage*8,shown=values.slice(start,start+8),frag=document.createDocumentFragment();
    text('readout-count',values.length);
    if(!values.length){const empty=document.createElement('p');empty.className='readout-list-empty';empty.textContent='No fixed readouts were declared for this experiment.';frag.append(empty);}
    for(const readout of shown){const row=document.createElement('div');row.className=`readout${readout.value?' on':''}`;row.dataset.readout=readout.id;row.dataset.value=String(readout.value);row.dataset.edge=String(readout.edge);const label=document.createElement('span'),bit=document.createElement('strong');label.className='readout-label';label.textContent=readout.label;bit.className='readout-bit';bit.textContent=readout.value?'1':'0';row.append(label,bit);if(readout.edge){const edge=document.createElement('span');edge.className='edge-tag';edge.textContent='rising edge';row.append(edge);}frag.append(row);}
    $('readouts').replaceChildren(frag);$('readouts-prev').disabled=readoutPage===0;$('readouts-next').disabled=start+8>=values.length;text('readout-page',values.length?`${start+1}–${Math.min(start+8,values.length)} of ${values.length}`:'');
  }
  function canvasContext(canvas) {
    const rect=canvas.getBoundingClientRect(),width=Math.max(1,rect.width),height=Math.max(1,rect.height),dpr=Math.min(globalThis.devicePixelRatio||1,2);
    if(canvas.width!==Math.round(width*dpr)||canvas.height!==Math.round(height*dpr)){canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);}
    const ctx=canvas.getContext('2d');ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);return {ctx,width,height};
  }
  function project(pos,width,height,side) {
    const v=pos.map((p,i)=>p/(side-1)-viewCenter[i]),mode=$('projection').value;let x,y,z;
    if(mode==='xy'){[x,y,z]=[v[0],-v[1],v[2]];}else if(mode==='xz'){[x,y,z]=[v[0],-v[2],v[1]];}else if(mode==='yz'){[x,y,z]=[v[1],-v[2],v[0]];}else{
      const co=Math.cos(camera.yaw),si=Math.sin(camera.yaw),cp=Math.cos(camera.pitch),sp=Math.sin(camera.pitch),xx=v[0]*co-v[2]*si,zz=v[0]*si+v[2]*co;x=xx;y=-(v[1]*cp-zz*sp);z=v[1]*sp+zz*cp;
    }
    const spanX=mode==='iso'?Math.abs(Math.cos(camera.yaw))+Math.abs(Math.sin(camera.yaw)):1;
    const spanY=mode==='iso'?Math.abs(Math.cos(camera.pitch))+Math.abs(Math.sin(camera.pitch))*(Math.abs(Math.sin(camera.yaw))+Math.abs(Math.cos(camera.yaw))):1;
    const scale=Math.min(Math.max(40,width-64)/spanX,Math.max(40,height-80)/spanY)*.88*camera.zoom;return {x:width/2+x*scale,y:height*.46+y*scale,z,scale};
  }
  function drawClock(ctx,x,y,r,a,b,rem,alpha,selected) {
    const p=D.phase(a,b);ctx.globalAlpha=alpha;
    if(r<3){ctx.fillStyle=p.atRest?'#d7a17e':'#89d6cc';ctx.fillRect(x-1,y-1,2,2);ctx.globalAlpha=1;return;}
    ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle='#1b3a43';ctx.fill();ctx.strokeStyle=p.atRest?'#738d87':'#75bbb1';ctx.lineWidth=.8;ctx.stroke();
    for(let k=0;k<6;k++){const t=k*Math.PI/3-Math.PI/2;ctx.beginPath();ctx.moveTo(x+Math.cos(t)*r*.86,y+Math.sin(t)*r*.86);ctx.lineTo(x+Math.cos(t)*r*.98,y+Math.sin(t)*r*.98);ctx.strokeStyle='#8ba79e';ctx.stroke();}
    if(!p.atRest){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+p.x*r*.71,y-p.y*r*.71);ctx.strokeStyle='#a0e4d5';ctx.lineWidth=Math.max(1,r*.09);ctx.lineCap='round';ctx.stroke();}
    ctx.beginPath();ctx.arc(x,y,Math.max(.9,r*.08),0,Math.PI*2);ctx.fillStyle=p.atRest?'#8aa39a':'#a0e4d5';ctx.fill();
    const gx=x+r*.76,gy=y+r*.73,gr=Math.max(2.2,r*.36);ctx.beginPath();ctx.arc(gx,gy,gr,0,Math.PI*2);ctx.fillStyle='#26434a';ctx.fill();ctx.strokeStyle='#bb9879';ctx.lineWidth=.7;ctx.stroke();
    for(let k=0;k<6;k++){const t=k*Math.PI/3-Math.PI/2;ctx.beginPath();ctx.arc(gx+Math.cos(t)*gr*.68,gy+Math.sin(t)*gr*.68,k===rem?Math.max(.8,gr*.25):Math.max(.35,gr*.11),0,Math.PI*2);ctx.fillStyle=k===rem?'#efac88':'#987f67';ctx.fill();}
    if(selected){ctx.globalAlpha=1;ctx.beginPath();ctx.arc(x,y,r+5,0,Math.PI*2);ctx.strokeStyle='#f0d8a1';ctx.lineWidth=1.3;ctx.setLineDash([2,3]);ctx.stroke();ctx.setLineDash([]);}ctx.globalAlpha=1;
  }
  function renderSpace(nodes) {
    const e=experiment();if(!e)return;const {ctx,width,height}=canvasContext($('space-canvas'));
    ctx.fillStyle='#173640';ctx.fillRect(0,0,width,height);
    const ns=nodes||D.nodes(e,frameIndex),mode=$('projection').value,filter=$('field-filter').value,side=e.side;
    const sliceAxis=mode==='xy'?2:mode==='xz'?1:0;let slice=Number($('slice').value);if(!Number.isSafeInteger(slice)||slice<0||slice>=side)slice=selection.position[sliceAxis];
    $('slice').disabled=mode==='iso';text('slice-label',mode==='iso'?'Slice':`${'XYZ'[sliceAxis]} slice`);
    const backgroundDrawn=side<=7&&filter==='all';let positions=backgroundDrawn?[]:ns.filter(n=>filter==='counters'?n.counter_channels>0:filter==='remainders'?n.remainder_only_channels>0:true).map(n=>n.position);
    if(backgroundDrawn)for(let x=0;x<side;x++)for(let y=0;y<side;y++)for(let z=0;z<side;z++)positions.push([x,y,z]);
    if(mode!=='iso')positions=positions.filter(p=>p[sliceAxis]===slice);
    const selectionInPlane=mode==='iso'||selection.position[sliceAxis]===slice;
    const selectionAdded=selectionInPlane&&!positions.some(p=>samePosition(p,selection.position));
    if(selectionAdded)positions.push([...selection.position]);
    const nodesByKey=new Map(ns.map(n=>[n.position.join(','),n]));
    const corners=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)corners.push([x*(side-1),y*(side-1),z*(side-1)]);
    ctx.strokeStyle='#52757a';ctx.lineWidth=.7;
    if(mode==='iso'){for(let i=0;i<8;i++)for(let bit=1;bit<=4;bit*=2){const j=i^bit;if(j<i)continue;const a=project(corners[i],width,height,side),b=project(corners[j],width,height,side);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}
    else{const ps=mode==='xy'?[[0,0,slice],[side-1,0,slice],[side-1,side-1,slice],[0,side-1,slice]]:mode==='xz'?[[0,slice,0],[side-1,slice,0],[side-1,slice,side-1],[0,slice,side-1]]:[[slice,0,0],[slice,side-1,0],[slice,side-1,side-1],[slice,0,side-1]];ctx.beginPath();ps.forEach((p,i)=>{const q=project(p,width,height,side);i?ctx.lineTo(q.x,q.y):ctx.moveTo(q.x,q.y);});ctx.closePath();ctx.stroke();}
    const zero=project([0,0,0],width,height,side);ctx.font='9px ui-sans-serif, sans-serif';ctx.textAlign='center';
    [[side-1,0,0],[0,side-1,0],[0,0,side-1]].forEach((p,i)=>{if(mode!=='iso'&&i===sliceAxis)return;const q=project(p,width,height,side);ctx.fillStyle=['#81c4b9','#e1ac8c','#a8bfcc'][i];ctx.fillText('XYZ'[i],q.x+(q.x-zero.x)*.08,q.y+(q.y-zero.y)*.08+3);});
    const pointList=positions.map(pos=>({...project(pos,width,height,side),pos})).sort((a,b)=>a.z-b.z);hits=[];
    const base=Math.min(20,Math.max(5,Math.min(width*.68,height*.78)/(Math.max(side,5)*3.2)))*Math.min(camera.zoom,2.7),dense=positions.length>3000;
    let inView=0,retainedInView=0;
    for(const p of pointList){const chosen=samePosition(p.pos,selection.position),r=chosen?Math.max(10,base):dense?Math.min(2.2,base):base;if(p.x<-r||p.y<-r||p.x>width+r||p.y>height+r)continue;inView++;
      const [a,b,rem]=D.at(e,frameIndex,[...p.pos,selection.channel]),n=nodesByKey.get(p.pos.join(',')),atBackground=a===0n&&b===0n&&rem===e.background[2];
      if(n)retainedInView++;
      drawClock(ctx,p.x,p.y,r,a,b,rem,chosen?1:atBackground?(n&&n.stored_channels?0.7:0.25):0.98,chosen);
      hits.push({x:p.x,y:p.y,r:Math.max(8,r+5),position:p.pos});
    }
    text('camera-label',mode==='iso'?'Drag to rotate · scroll / pinch to zoom':'Select a clock · scroll / pinch to zoom');
    text('space-scale',`Channel ${selection.channel} · ${side} × ${side} × ${side} periodic cube${dense?' · zoom or inspect to resolve clocks':''}`);
    const filterLabel=filter==='all'?'all stored nodes':filter==='counters'?'nodes with nonzero counters':'nodes with remainder-only deviations';
    const hiddenRetained=ns.length-retainedInView;
    text('visible-count',`${inView} clocks in view · ${hiddenRetained} retained nodes hidden${backgroundDrawn?' · background included':selectionAdded?' · selection included':' · background omitted'}`);
    $('visible-count').title=`${filterLabel}. Hidden retained nodes are outside the current filter, slice or viewport; their complete states remain available.`;
  }
  function traceData() {
    const e=experiment();let cached=historyCache.get(e);if(!cached){cached={readouts:e.frames.map((_,i)=>D.readouts(e,i)),channels:new Map()};historyCache.set(e,cached);}
    const key=address().join(',');if(!cached.channels.has(key)){const triples=e.frames.map((_,i)=>D.at(e,i,address()));let max=1n;for(const t of triples){const a=t[1]<0n?-t[1]:t[1];if(a>max)max=a;}const points=triples.map(t=>({b:Number(t[1]*1000000n/max)/1000000,r:t[2]}));cached.channels.set(key,points);if(cached.channels.size>32)cached.channels.delete(cached.channels.keys().next().value);}return {points:cached.channels.get(key),readouts:cached.readouts};
  }
  function renderHistory() {
    const e=experiment();if(!e)return;const {points,readouts}=traceData();
    const {ctx,width,height}=canvasContext($('channel-history')),pad=10,plotHeight=height-40,xx=i=>pad+(width-pad*2)*i/Math.max(1,points.length-1);
    ctx.strokeStyle='#d7dfd3';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad,plotHeight/2);ctx.lineTo(width-pad,plotHeight/2);ctx.stroke();ctx.beginPath();points.forEach((p,i)=>{const x=xx(i),y=plotHeight/2-p.b*(plotHeight/2-8);i?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.strokeStyle='#168c89';ctx.lineWidth=1.6;ctx.stroke();
    if(points.length===1){ctx.beginPath();ctx.arc(xx(0),plotHeight/2-points[0].b*(plotHeight/2-8),3,0,Math.PI*2);ctx.fillStyle='#168c89';ctx.fill();}
    const barWidth=Math.max(1,(width-pad*2)/points.length);points.forEach((p,i)=>{ctx.fillStyle=colors[p.r];ctx.fillRect(pad+i*barWidth,plotHeight+13,barWidth+1,12);});ctx.strokeStyle='#d98564';ctx.beginPath();ctx.moveTo(xx(frameIndex),4);ctx.lineTo(xx(frameIndex),height-6);ctx.stroke();
    const t=canvasContext($('readout-timeline')),pageReadouts=e.readouts.slice(readoutPage*8,readoutPage*8+8),rowH=Math.min(16,t.height/Math.max(pageReadouts.length,1));
    pageReadouts.forEach((r,j)=>{for(let i=0;i<readouts.length;i++){const value=readouts[i][readoutPage*8+j],x=i*t.width/readouts.length,w=t.width/readouts.length;t.ctx.fillStyle=value.value?'#80bba6':'#e4e9df';t.ctx.fillRect(x,j*rowH,w+1,rowH-3);if(value.edge){t.ctx.fillStyle='#d98867';t.ctx.fillRect(x,j*rowH,Math.max(2,w),3);}}});t.ctx.strokeStyle='#d98564';t.ctx.beginPath();t.ctx.moveTo(frameIndex*t.width/Math.max(1,readouts.length-1),0);t.ctx.lineTo(frameIndex*t.width/Math.max(1,readouts.length-1),t.height);t.ctx.stroke();
  }
  function resetCamera(){Object.assign(camera,{yaw:-0.65,pitch:0.42,zoom:1});viewCenter=[0.5,0.5,0.5];renderSpace();}
  function focusState(){
    const e=experiment();if(!e)return;const filter=$('field-filter').value,mode=$('projection').value,axis=mode==='xy'?2:mode==='xz'?1:0,slice=Number($('slice').value);
    let positions=D.nodes(e,frameIndex).filter(n=>(filter==='counters'?n.counter_channels>0:filter==='remainders'?n.remainder_only_channels>0:true)&&(mode==='iso'||n.position[axis]===slice)).map(n=>n.position);
    if(!positions.length)positions=[selection.position];
    const min=[...positions[0]],max=[...positions[0]];for(const pos of positions)for(let i=0;i<3;i++){min[i]=Math.min(min[i],pos[i]);max[i]=Math.max(max[i],pos[i]);}
    viewCenter=min.map((v,i)=>(v/(e.side-1)+max[i]/(e.side-1))/2);camera.zoom=1;
    const rect=canvas.getBoundingClientRect(),corners=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)corners.push(project([x?max[0]:min[0],y?max[1]:min[1],z?max[2]:min[2]],rect.width,rect.height,e.side));
    const xs=corners.map(p=>p.x),ys=corners.map(p=>p.y),spanX=Math.max(...xs)-Math.min(...xs),spanY=Math.max(...ys)-Math.min(...ys);
    camera.zoom=clamp(Math.min(Math.max(40,rect.width-100)/Math.max(50,spanX),Math.max(40,rect.height-130)/Math.max(50,spanY)),.35,64);
    visible('view-options',false);$('view-options-toggle').setAttribute('aria-expanded','false');renderSpace();announce('Camera fitted to retained states in the current filter. Reset view restores the full cube.');
  }
  function pointerDistance(){const p=[...activePointers.values()];return p.length<2?null:Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);}
  function canvasPoint(event){const rect=$('space-canvas').getBoundingClientRect();return {x:event.clientX-rect.left,y:event.clientY-rect.top};}
  const canvas=$('space-canvas');
  canvas.addEventListener('pointerdown',event=>{if(event.button!==0&&event.pointerType!=='touch')return;const p=canvasPoint(event);activePointers.set(event.pointerId,p);pointerStart=p;dragDistance=0;pinchDistance=pointerDistance();if(canvas.setPointerCapture)canvas.setPointerCapture(event.pointerId);});
  canvas.addEventListener('pointermove',event=>{if(!activePointers.has(event.pointerId))return;const previous=activePointers.get(event.pointerId),p=canvasPoint(event);activePointers.set(event.pointerId,p);dragDistance+=Math.hypot(p.x-previous.x,p.y-previous.y);if(activePointers.size>=2){const distance=pointerDistance();if(pinchDistance&&distance)camera.zoom=clamp(camera.zoom*distance/pinchDistance,.35,64);pinchDistance=distance;}else if($('projection').value==='iso'){camera.yaw+=(p.x-previous.x)*.008;camera.pitch=clamp(camera.pitch+(p.y-previous.y)*.008,-1.35,1.35);}renderSpace();});
  function pointerUp(event){if(!activePointers.has(event.pointerId))return;const p=canvasPoint(event),wasMulti=activePointers.size>1;activePointers.delete(event.pointerId);pinchDistance=pointerDistance();if(!wasMulti&&dragDistance<6&&pointerStart){let nearest=null;for(const hit of hits){const d=Math.hypot(hit.x-p.x,hit.y-p.y);if(d<hit.r&&(!nearest||d<nearest.distance))nearest={...hit,distance:d};}if(nearest)selectAddress(nearest.position,selection.channel,true);}pointerStart=null;}
  canvas.addEventListener('pointerup',pointerUp);canvas.addEventListener('pointercancel',event=>{activePointers.delete(event.pointerId);pointerStart=null;pinchDistance=pointerDistance();});
  canvas.addEventListener('wheel',event=>{event.preventDefault();camera.zoom=clamp(camera.zoom*Math.exp(-event.deltaY*.0015),.35,64);renderSpace();},{passive:false});
  canvas.addEventListener('keydown',event=>{let used=true;if(event.key==='ArrowLeft')camera.yaw-=.12;else if(event.key==='ArrowRight')camera.yaw+=.12;else if(event.key==='ArrowUp')camera.pitch=clamp(camera.pitch-.12,-1.35,1.35);else if(event.key==='ArrowDown')camera.pitch=clamp(camera.pitch+.12,-1.35,1.35);else if(event.key==='+'||event.key==='=')camera.zoom=clamp(camera.zoom*1.15,.35,64);else if(event.key==='-')camera.zoom=clamp(camera.zoom/1.15,.35,64);else if(event.key==='Enter')openInspector();else used=false;if(used){event.preventDefault();renderSpace();}});
  $('open-file').addEventListener('click',()=>$('file-input').click());$('empty-open').addEventListener('click',()=>$('file-input').click());$('file-input').addEventListener('change',()=>importFile($('file-input').files[0]));
  $('experiment').addEventListener('change',()=>selectExperiment(bundle.experiments.findIndex(e=>e.id===$('experiment').value)));
  $('play').addEventListener('click',()=>setPlaying(!timer));$('prev').addEventListener('click',()=>{setPlaying(false);setFrame(frameIndex-1);});$('next').addEventListener('click',()=>{setPlaying(false);setFrame(frameIndex+1);});$('rewind').addEventListener('click',()=>{setPlaying(false);setFrame(0);});$('scrub').addEventListener('input',()=>{setPlaying(false);setFrame(Number($('scrub').value));});$('speed').addEventListener('change',()=>{if(timer)setPlaying(true);});
  $('channel-select').addEventListener('change',()=>selectAddress(selection.position,Number($('channel-select').value)));
  $('node-form').addEventListener('submit',event=>{event.preventDefault();try{const e=experiment(),pos=['node-x','node-y','node-z'].map((id,i)=>integerInput($(id),e.side-1,'XYZ'[i]));selectAddress(pos,selection.channel);visible('error',false);}catch(err){error(err.message);}});
  $('inspect').addEventListener('click',openInspector);$('close-inspector').addEventListener('click',closeInspector);$('inspector-backdrop').addEventListener('click',closeInspector);$('show-evidence').addEventListener('click',openEvidence);$('show-evidence-main').addEventListener('click',openEvidence);$('close-evidence').addEventListener('click',closeEvidence);$('evidence-backdrop').addEventListener('click',closeEvidence);
  $('fit').addEventListener('click',resetCamera);$('focus-state').addEventListener('click',focusState);$('projection').addEventListener('change',()=>{const mode=$('projection').value,axis=mode==='xy'?2:mode==='xz'?1:0;$('slice').value=String(selection.position[axis]);renderSpace();});$('field-filter').addEventListener('change',()=>renderSpace());$('slice').addEventListener('change',()=>{try{integerInput($('slice'),experiment().side-1,'Slice');renderSpace();}catch(err){error(err.message);}});
  $('view-options-toggle').addEventListener('click',()=>{const open=$('view-options').hidden;visible('view-options',open);$('view-options-toggle').setAttribute('aria-expanded',String(open));});
  $('readouts-prev').addEventListener('click',()=>{readoutPage=Math.max(0,readoutPage-1);renderReadouts();renderHistory();});$('readouts-next').addEventListener('click',()=>{readoutPage++;renderReadouts();renderHistory();});
  $('channel-history').addEventListener('click',event=>{const rect=$('channel-history').getBoundingClientRect(),e=experiment();setPlaying(false);setFrame(Math.round(clamp((event.clientX-rect.left-10)/(rect.width-20),0,1)*(e.frames.length-1)));});
  document.querySelectorAll('details').forEach(detail=>detail.addEventListener('toggle',()=>{if(detail.open&&!$('evidence').hidden)renderHistory();}));
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(!$('evidence').hidden)closeEvidence();else if(!$('inspector').hidden)closeInspector();else visible('view-options',false);return;}if(event.key==='Tab'){const panel=!$('evidence').hidden?$('evidence'):!$('inspector').hidden?$('inspector'):null;if(panel){const focusable=[...panel.querySelectorAll('button,input,select,summary,[tabindex="0"]')].filter(el=>!el.disabled&&el.getClientRects().length);if(focusable.length){const first=focusable[0],last=focusable[focusable.length-1];if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}}}if(event.code==='Space'&&!['INPUT','SELECT','TEXTAREA','BUTTON','SUMMARY'].includes(event.target.tagName)&&$('evidence').hidden&&$('inspector').hidden){event.preventDefault();setPlaying(!timer);}});
  let dragDepth=0;document.addEventListener('dragenter',event=>{if(event.dataTransfer?.types?.includes('Files')){event.preventDefault();dragDepth++;document.body.classList.add('dragging');}});document.addEventListener('dragleave',()=>{dragDepth--;if(dragDepth<=0)document.body.classList.remove('dragging');});document.addEventListener('dragover',event=>event.preventDefault());document.addEventListener('drop',event=>{event.preventDefault();dragDepth=0;document.body.classList.remove('dragging');if(event.dataTransfer?.files?.length)importFile(event.dataTransfer.files[0]);});
  function resized(){if(resizePending)return;resizePending=true;requestAnimationFrame(()=>{resizePending=false;renderSpace();if(!$('evidence').hidden)renderHistory();});}
  globalThis.addEventListener('resize',resized);if(globalThis.ResizeObserver)new ResizeObserver(resized).observe(canvas);
  for(let g=0;g<48;g++){const option=document.createElement('option');option.value=String(g);option.textContent=String(g);$('channel-select').append(option);}
  for(let r=0;r<6;r++){const swatch=document.createElement('i');swatch.style.background=colors[r];swatch.textContent=String(r);$('r-key').append(swatch);}
  $('open-file').disabled=false;
  const ready=globalThis.PRESENTER_BUNDLE?importText(JSON.stringify(globalThis.PRESENTER_BUNDLE)):Promise.resolve().then(()=>{visible('empty',true);if(startup)startup.complete();return true;});
  globalThis.PresenterUI=Object.freeze({get selection(){return {position:[...selection.position],channel:selection.channel};},get experiment(){return experiment();},get frameIndex(){return frameIndex;},get camera(){return {...camera,center:[...viewCenter]};},get ready(){return ready;},importText});
})();
