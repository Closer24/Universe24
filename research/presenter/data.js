/* The Presenter: exact read-only state validation and algebra. No simulation API. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PresenterData = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const FORMAT = 'universe24-presenter-v1';
  const MODEL = 'universe24-2O-body-013-v1';
  const DIRECTIONS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
  const limits = Object.freeze({maxBytes:67108864,maxFrames:10000,maxStoredCells:500000,
    maxExperiments:64,maxCounterDigits:100000,maxReadouts:256,maxClauses:1024,maxDepth:96});
  // Audited reference matrices, reconstructed using research/reference/algebra.py.
const REFERENCE_PORTS=[[0,1,15,3,24,9,6,7,34,16,10,19,12,37,14,32,25,17,27,45,28,21,29,23,39,35,26,41,22,38,20,31,4,33,2,44,36,11,46,8,30,13,47,43,42,18,40,5],[0,1,34,3,32,47,6,7,39,5,10,37,12,41,14,2,9,17,45,11,30,21,28,23,4,16,26,18,20,22,40,31,15,33,8,25,36,13,29,24,46,27,44,43,35,19,38,42],[2,22,6,11,4,23,13,42,3,9,20,21,35,14,24,15,31,8,18,19,43,32,26,40,36,25,5,17,28,29,30,38,33,27,34,1,45,37,7,39,12,41,10,16,44,0,46,47],[45,35,0,8,4,26,2,38,17,9,42,3,40,6,13,15,43,27,18,19,10,11,1,5,14,25,22,33,28,29,30,16,21,32,34,12,24,37,31,39,23,41,7,20,44,36,46,47],[25,4,2,29,10,5,44,18,8,33,19,11,39,13,47,7,16,28,12,23,20,46,22,34,24,21,15,27,0,36,6,41,32,30,31,35,9,26,38,43,40,1,42,37,3,45,14,17],[28,41,2,44,1,5,30,15,8,36,4,11,18,13,46,26,16,47,7,10,20,25,22,19,24,0,37,27,17,3,33,34,32,9,23,35,29,43,38,12,40,31,42,39,6,45,21,14]];
const BODY_AXES=[[0,0,2,0,2,1,0,0,2,1,0,2,0,2,0,2,1,0,2,2,1,0,1,0,2,1,0,2,1,1,1,0,2,0,2,1,0,2,1,2,1,2,1,0,1,2,1,1],[0,0,2,0,2,1,0,0,2,1,0,2,0,2,0,2,1,0,2,2,1,0,1,0,2,1,0,2,1,1,1,0,2,0,2,1,0,2,1,2,1,2,1,0,1,2,1,1],[1,2,1,1,0,2,1,2,1,0,2,1,2,1,1,0,2,1,0,0,2,1,2,2,1,0,2,1,0,0,0,2,1,1,0,2,1,0,2,0,2,0,2,2,0,1,0,0],[1,2,1,1,0,2,1,2,1,0,2,1,2,1,1,0,2,1,0,0,2,1,2,2,1,0,2,1,0,0,0,2,1,1,0,2,1,0,2,0,2,0,2,2,0,1,0,0],[2,1,0,2,1,0,2,1,0,2,1,0,1,0,2,1,0,2,1,1,0,2,0,1,0,2,1,0,2,2,2,1,0,2,1,0,2,1,0,1,0,1,0,1,2,0,2,2],[2,1,0,2,1,0,2,1,0,2,1,0,1,0,2,1,0,2,1,1,0,2,0,1,0,2,1,0,2,2,2,1,0,2,1,0,2,1,0,1,0,1,0,1,2,0,2,2]];
  const lexicalFloats = new WeakMap(), rawIntegerStrings = new WeakMap();
  const maps = new WeakMap(), mapQueue = [];
  const nodeCache = new WeakMap();
  function fail(message) { throw new Error('The Presenter: ' + message); }
  function requireValue(condition, message) { if (!condition) fail(message); }
  function bytes(text) { return new TextEncoder().encode(text); }
  function object(value,label) { requireValue(value && typeof value==='object' && !Array.isArray(value),label+' must be an object'); return value; }
  function keys(value,allowed,required,label) { object(value,label);requireValue(Object.keys(value).every(k=>allowed.includes(k)),label+' contains unsupported fields');requireValue(required.every(k=>Object.prototype.hasOwnProperty.call(value,k)),label+' is missing required fields');return value; }
  function array(value,label,length) { requireValue(Array.isArray(value),label+' must be an array'); if(length!==undefined)requireValue(value.length===length,label+' has the wrong length'); return value; }
  function text(value,label,fallback,max=10000) { if(value===undefined&&fallback!==undefined)return fallback;requireValue(typeof value==='string'&&value.length<=max,label+' must be text of at most '+max+' characters');return value; }
  function floating(owner,key) { return owner && lexicalFloats.has(owner) && lexicalFloats.get(owner).has(String(key)); }
  function integer(value,label,min=0,max=Number.MAX_SAFE_INTEGER,owner,key) {
    requireValue(!floating(owner,key)&&typeof value==='number'&&Number.isSafeInteger(value)&&value>=min&&value<=max,label+' must be an exact safe integer in ['+min+','+max+']'); return value;
  }
  function decimal(value,label,owner,key) {
    requireValue(!floating(owner,key),label+' must be an integer, not a floating-point JSON token');
    if(typeof value==='number') { integer(value,label,-Number.MAX_SAFE_INTEGER); value=String(value); }
    requireValue(typeof value==='string'&&/^(?:0|-[1-9][0-9]*|[1-9][0-9]*)$/.test(value),label+' must be a canonical decimal integer');
    requireValue(value.length-(value[0]==='-'?1:0)<=limits.maxCounterDigits,label+' exceeds the '+limits.maxCounterDigits+'-digit limit');return value;
  }
  function deepFreeze(value) { if(value&&typeof value==='object'&&!Object.isFrozen(value)){Object.values(value).forEach(deepFreeze);Object.freeze(value);}return value; }
  function plain(value) { return value===undefined?{}:JSON.parse(JSON.stringify(value)); }
  function stableStringify(value) {
    if(value===null||typeof value!=='object')return JSON.stringify(value);
    if(Array.isArray(value))return '['+value.map(stableStringify).join(',')+']';
    return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+stableStringify(value[k])).join(',')+'}';
  }
  async function sha256(value) {
    const encoded=bytes(typeof value==='string'?value:stableStringify(value));
    let subtle=typeof globalThis.crypto!=='undefined'&&globalThis.crypto.subtle;
    if(!subtle&&typeof require==='function')subtle=require('node:crypto').webcrypto.subtle;
    requireValue(subtle,'SHA-256 is unavailable in this browser; use a browser with Web Crypto support');
    return Array.from(new Uint8Array(await subtle.digest('SHA-256',encoded)),x=>x.toString(16).padStart(2,'0')).join('');
  }

  // Recursive JSON parser tracks lexical float tokens and duplicate names before
  // native parsing could round a long integer or discard a duplicate member.
  function parse(input) {
    requireValue(typeof input==='string','Input must be text');
    requireValue(input.length<=limits.maxBytes&&bytes(input).length<=limits.maxBytes,'Input exceeds the 64 MiB limit; export a smaller complete segment');
    let pos=0; const n=input.length;
    function whitespace(){while(pos<n&&/[\x20\t\r\n]/.test(input[pos]))pos++;}
    function error(message){fail(message+' at character '+pos);}
    function str(){const start=pos++;while(pos<n){const c=input[pos++];if(c==='"'){try{return JSON.parse(input.slice(start,pos));}catch(_){error('Invalid JSON string');}}if(c==='\\'){if(pos>=n)error('Truncated escape');pos++;}else if(c.charCodeAt(0)<32)error('Unescaped control character');}error('Unterminated string');}
    function num(){
      const start=pos;if(input[pos]==='-')pos++;
      if(input[pos]==='0')pos++;else {if(!/[1-9]/.test(input[pos]||''))error('Invalid number');while(pos<n&&/[0-9]/.test(input[pos]))pos++;}
      let float=false;
      if(input[pos]==='.'){float=true;pos++;const begin=pos;while(pos<n&&/[0-9]/.test(input[pos]))pos++;if(pos===begin)error('Missing decimal digits');}
      if(input[pos]==='e'||input[pos]==='E'){float=true;pos++;if(input[pos]==='+'||input[pos]==='-')pos++;const begin=pos;while(pos<n&&/[0-9]/.test(input[pos]))pos++;if(pos===begin)error('Missing exponent digits');}
      const raw=input.slice(start,pos);
      if(float){const value=Number(raw);if(!Number.isFinite(value))error('Non-finite number');return {value,float};}
      if(raw.length<17&&Number.isSafeInteger(Number(raw)))return {value:Number(raw),float:false};
      return {value:raw==='-0'?'0':raw,float:false,integerString:true};
    }
    function value(depth){
      if(depth>limits.maxDepth)error('JSON nesting exceeds the resource limit');whitespace();
      const c=input[pos];
      if(c==='"')return {value:str(),float:false};
      if(c==='{'||c==='['){
        const isObject=c==='{',out=isObject?Object.create(null):[],marked=new Set(),integerStrings=new Set();pos++;whitespace();
        if(input[pos]===(isObject?'}':']')){pos++;return {value:out,float:false};}
        const seen=new Set();
        while(true){
          let key;
          if(isObject){whitespace();if(input[pos]!=='"')error('Expected an object key');key=str();if(seen.has(key))error('Duplicate JSON member '+JSON.stringify(key));seen.add(key);whitespace();if(input[pos++]!==':')error('Expected colon');}
          else key=out.length;
          const parsed=value(depth+1);out[key]=parsed.value;if(parsed.float)marked.add(String(key));if(parsed.integerString)integerStrings.add(String(key));
          whitespace();const close=isObject?'}':']';if(input[pos]===close){pos++;break;}if(input[pos++]!==',')error('Expected comma or closing bracket');
        }
        if(marked.size)lexicalFloats.set(out,marked);if(integerStrings.size)rawIntegerStrings.set(out,integerStrings);return {value:out,float:false};
      }
      for(const [token,result] of [['true',true],['false',false],['null',null]])if(input.startsWith(token,pos)){pos+=token.length;return {value:result,float:false};}
      if(c==='-'||/[0-9]/.test(c||''))return num();error('Invalid JSON value');
    }
    const result=value(0).value;whitespace();if(pos!==n)error('Unexpected trailing data');return result;
  }
  function position(value,side,label) { array(value,label,3);return value.map((v,i)=>integer(v,label+'['+i+']',0,side-1,value,i)); }
  function addressStrict(value,side,label) { array(value,label,4);return value.map((v,i)=>integer(v,label+'['+i+']',0,i===3?47:side-1,value,i)); }
  function key(addr){return addr.join(',');}
  function addressCompare(a,b){for(let i=0;i<4;i++){if(a[i]<b[i])return -1;if(a[i]>b[i])return 1;}return 0;}
  function shift(pos,dir,side,sign=1){return pos.map((v,i)=>{const d=dir[i]*sign;return d===1?(v===side-1?0:v+1):d===-1?(v===0?side-1:v-1):v;});}
  function equalTriple(a,b){return a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2];}
  function divmod(n){let q=n/6n,r=n%6n;if(r<0n){q-=1n;r+=6n;}return [q,Number(r)];}
  function getMap(exp,frameIndex){
    integer(frameIndex,'Frame index',0,exp.frames.length-1);
    const frame=exp.frames[frameIndex];let map=maps.get(frame);
    if(!map){map=new Map(frame.cells.map(row=>[key(row.slice(0,4)),Object.freeze([BigInt(row[4]),BigInt(row[5]),row[6]])]));maps.set(frame,map);mapQueue.push(frame);if(mapQueue.length>8)maps.delete(mapQueue.shift());}
    return map;
  }
  function at(exp,frameIndex,addr){const checked=addressStrict(addr,exp.side,'Selected address');return getMap(exp,frameIndex).get(key(checked))||Object.freeze([BigInt(exp.background[0]),BigInt(exp.background[1]),exp.background[2]]);}
  function rawAt(exp,map,addr){return map.get(key(addr))||[0n,0n,exp.background[2]];}
  function inspectTransition(exp,oldMap,nextMap,addr){
    const old=rawAt(exp,oldMap,addr),next=rawAt(exp,nextMap,addr),g=addr[3];
    const inputs=exp.coupling.directions.map((direction,d)=>{const sender=[...shift(addr.slice(0,3),direction,exp.side),exp.coupling.ports[d][g]];const b=rawAt(exp,oldMap,sender)[1],weight=exp.coupling.weights[d][g];return {direction,address:sender,weight,b,product:BigInt(weight)*b};});
    const u=inputs.reduce((s,x)=>s+x.product,0n),numerator=2n*u+BigInt(old[2]),[ell,remainder]=divmod(numerator);
    return {old,next,u,ell,numerator,remainder,ok:next[0]===old[1]&&next[1]===ell-old[0]&&next[2]===remainder,inputs};
  }
  function transition(exp,frameIndex,addr){addressStrict(addr,exp.side,'Selected address');integer(frameIndex,'Frame index',0,exp.frames.length-1);return frameIndex===0?null:inspectTransition(exp,getMap(exp,frameIndex-1),getMap(exp,frameIndex),addr);}
  function readouts(exp,frameIndex){
    integer(frameIndex,'Frame index',0,exp.frames.length-1);
    function read(readout,index){return readout.clauses.every(c=>String(at(exp,index,c.address)[{a:0,b:1,r:2}[c.component]])===c.equals);}
    return exp.readouts.map(r=>{const value=read(r,frameIndex);return {id:r.id,label:r.label,value,edge:frameIndex>0&&value&&!read(r,frameIndex-1)};});
  }
  function nodes(exp,frameIndex){
    integer(frameIndex,'Frame index',0,exp.frames.length-1);const frame=exp.frames[frameIndex];if(nodeCache.has(frame))return nodeCache.get(frame);
    const grouped=new Map();for(const row of frame.cells){const p=row.slice(0,3),k=p.join(',');let node=grouped.get(k);if(!node){node={position:p,stored_channels:0,counter_channels:0,remainder_only_channels:0,channels:[]};grouped.set(k,node);}node.stored_channels++;node.channels.push(row[3]);if(row[4]!=='0'||row[5]!=='0')node.counter_channels++;else node.remainder_only_channels++;}
    const result=deepFreeze([...grouped.values()].sort((a,b)=>addressCompare([...a.position,0],[...b.position,0])));nodeCache.set(frame,result);return result;
  }
  function phase(a,b){requireValue(typeof a==='bigint'&&typeof b==='bigint','Phase inputs must be BigInt counters');const aa=a<0n?-a:a,bb=b<0n?-b:b,m=aa>bb?aa:bb;if(m===0n)return {x:0,y:0,atRest:true};const x=Number(a*1000000n/m)/1000000,y=Number(b*1000000n/m)/1000000,norm=Math.hypot(x,y);return {x:x/norm,y:y/norm,atRest:false};}

  async function coupling(input,label){
    keys(input,['model','body_signs','directions','ports','weights','fingerprint'],['model','body_signs','directions','ports','weights','fingerprint'],label);requireValue(input.model===MODEL,label+' is not the supported reference model; separate model variants need an explicit adapter');
    const signs=array(input.body_signs,label+' body_signs',3).map((v,i)=>{integer(v,label+' sign',-1,1,input.body_signs,i);requireValue(v===-1||v===1,label+' signs must be +/-1');return v;});
    const directions=array(input.directions,label+' directions',6).map((row,d)=>array(row,label+' direction',3).map((v,i)=>{integer(v,label+' direction component',-1,1,row,i);requireValue(v===DIRECTIONS[d][i],label+' direction ordering differs from the reference');return v;}));
    const ports=array(input.ports,label+' ports',6).map((row,d)=>array(row,label+' port row',48).map((v,g)=>{integer(v,label+' port',0,47,row,g);requireValue(v===REFERENCE_PORTS[d][g],label+' routing differs from the reference tensor');return v;}));
    const weights=array(input.weights,label+' weights',6).map((row,d)=>array(row,label+' weight row',48).map((v,g)=>{integer(v,label+' weight',-1,1,row,g);requireValue(v===signs[BODY_AXES[d][g]],label+' weights differ from the declared body signs');return v;}));
    for(let d=0;d<6;d++)for(let g=0;g<48;g++){const h=ports[d][g];requireValue(ports[d^1][h]===g&&weights[d^1][h]===weights[d][g],label+' tensor is not reciprocal');}
    const fingerprint=await sha256(JSON.stringify([MODEL,ports,weights]));requireValue(input.fingerprint===fingerprint,label+' coupling fingerprint does not match its complete fixed tensor');
    return {model:MODEL,body_signs:signs,directions,ports,weights,fingerprint};
  }
  function normalizeReadouts(input,side){
    if(input===undefined)return [];array(input,'Readouts');requireValue(input.length<=limits.maxReadouts,'Readout count exceeds '+limits.maxReadouts);
    const seen=new Set();let clauses=0;
    return input.map((r,i)=>{keys(r,['id','label','kind','clauses'],['id','label','kind','clauses'],'Readout');requireValue(r.kind==='all_equal','Unsupported readout kind');const id=text(r.id,'Readout ID',undefined,256);requireValue(id.length>0&&!seen.has(id),'Readout IDs must be nonempty and unique');seen.add(id);const items=array(r.clauses,'Readout clauses');requireValue(items.length>0,'Readout conjunction cannot be empty');clauses+=items.length;requireValue(clauses<=limits.maxClauses,'Readout clause count exceeds '+limits.maxClauses);
      return {id,label:text(r.label,'Readout label',id,1000),kind:'all_equal',clauses:items.map(c=>{keys(c,['address','component','equals'],['address','component','equals'],'Readout clause');requireValue(typeof c.equals==='string'&&!(rawIntegerStrings.has(c)&&rawIntegerStrings.get(c).has('equals')),'Readout value must be a canonical decimal string');requireValue(['a','b','r'].includes(c.component),'Readout component must be a, b or r');const equals=decimal(c.equals,'Readout value',c,'equals');if(c.component==='r')requireValue(BigInt(equals)>=0n&&BigInt(equals)<=5n,'Remainder readout must be 0..5');return {address:addressStrict(c.address,side,'Readout address'),component:c.component,equals};})};});
  }
  function nativeCounter(value,owner,k,label) { requireValue(typeof value==='number'||(rawIntegerStrings.has(owner)&&rawIntegerStrings.get(owner).has(String(k))),label+' must be an integer JSON token in a native checkpoint');return decimal(value,label,owner,k); }
  function normalizeBackground(input){array(input,'Background',3);const a=decimal(input[0],'Background a',input,0),b=decimal(input[1],'Background b',input,1),r=integer(input[2],'Background remainder',0,5,input,2);requireValue(a==='0'&&b==='0','Sparse background counters must both be zero');return [a,b,r];}
  function normalizeFrames(input,side,background,budget,source){
    array(input,'Frames');requireValue(input.length>0&&input.length<=limits.maxFrames,'Each experiment needs 1..'+limits.maxFrames+' complete frames');
    let last=-1;
    return input.map((frame,fi)=>{keys(frame,['step','cells','state_sha256','audit'],source==='bundle'?['step','cells','state_sha256','audit']:['step','cells'],'Frame');const step=integer(frame.step,'Frame step',0,Number.MAX_SAFE_INTEGER,frame,'step');if(fi)requireValue(last<Number.MAX_SAFE_INTEGER&&step===last+1,'Recorded frames must be consecutive; export the complete segment');last=step;const rows=array(frame.cells,'Frame cells');budget.cells+=rows.length;requireValue(budget.cells<=limits.maxStoredCells,'Total stored cells exceed '+limits.maxStoredCells+'; export a smaller complete segment');
      let prior=null;const cells=rows.map(row=>{array(row,'Cell row',7);const addr=row.slice(0,4).map((v,i)=>integer(v,'Cell address',0,i===3?47:side-1,row,i));requireValue(!prior||addressCompare(prior,addr)<0,'Cell addresses must be sorted and unique');prior=addr;if(source==='bundle')for(const k of [4,5])requireValue(typeof row[k]==='string'&&!(rawIntegerStrings.has(row)&&rawIntegerStrings.get(row).has(String(k))),'Presenter counters must be canonical decimal strings');const a=decimal(row[4],'Counter a',row,4),b=decimal(row[5],'Counter b',row,5),r=integer(row[6],'Remainder',0,5,row,6);requireValue(a!==background[0]||b!==background[1]||r!==background[2],'Sparse cells must omit background triples');return [...addr,a,b,r];});
      const hash=frame.state_sha256;if(source==='bundle')requireValue(typeof hash==='string'&&/^[0-9a-f]{64}$/.test(hash),'Presenter frames require a complete-state SHA-256');else if(hash!==undefined)requireValue(typeof hash==='string'&&/^[0-9a-f]{64}$/.test(hash),'Invalid state SHA-256');
      let audit={forward_equal:null,inverse_equal:null};if(frame.audit!==undefined){keys(frame.audit,['forward_equal','inverse_equal'],['forward_equal','inverse_equal'],'Audit');for(const k of ['forward_equal','inverse_equal'])requireValue(frame.audit[k]===null||typeof frame.audit[k]==='boolean','Audit flags must be boolean or null');audit={forward_equal:frame.audit.forward_equal,inverse_equal:frame.audit.inverse_equal};}
      if(source==='bundle')requireValue(fi===0?(audit.forward_equal===null&&audit.inverse_equal===null):(audit.forward_equal===true&&audit.inverse_equal===true),'Bundle audit flags must be null on the initial frame and true on completed transitions; actual states are verified independently');
      return {step,cells,state_sha256:hash||null,audit};});
  }
  async function validateExperiment(input,budget,source,options){
    keys(input,['id','title','description','side','background','coupling','frames','readouts','view','provenance'],['side','background','coupling','frames'],'Experiment');if(input.provenance!==undefined)object(input.provenance,'Experiment provenance');array(input.background,'Background',3);requireValue(input.background[0]==='0'&&input.background[1]==='0','Presenter background counters must be decimal strings');const side=integer(input.side,'Cube side',3,Number.MAX_SAFE_INTEGER,input,'side');
    const exp={id:text(input.id,'Experiment ID','experiment',256),title:text(input.title,'Experiment title','Experiment',1000),description:text(input.description,'Experiment description',''),side,background:normalizeBackground(input.background),coupling:await coupling(input.coupling,'Experiment coupling'),frames:[],readouts:normalizeReadouts(input.readouts,side),view:{position:[0,0,0],channel:0},provenance:plain(input.provenance)};
    requireValue(exp.id.length>0,'Experiment ID cannot be empty');exp.frames=normalizeFrames(input.frames,side,exp.background,budget,source);
    if(input.view!==undefined){keys(input.view,['position','channel'],['position','channel'],'Initial view');exp.view={position:position(input.view.position,side,'Initial view position'),channel:integer(input.view.channel,'Initial view channel',0,47,input.view,'channel')};}
    let hashes=0,checks=0;
    for(let fi=0;fi<exp.frames.length;fi++){
      const frame=exp.frames[fi];const actualHash=await sha256({side,background:exp.background,cells:frame.cells});if(frame.state_sha256){requireValue(actualHash===frame.state_sha256,'Full-state digest mismatch in '+exp.id+' at step '+frame.step);hashes++;}else frame.state_sha256=actualHash;
      if(fi){
        const oldMap=getMap(exp,fi-1),nextMap=getMap(exp,fi),addresses=new Map();
        const add=a=>addresses.set(key(a),a);
        for(const row of exp.frames[fi-1].cells){const addr=row.slice(0,4);add(addr);if(row[5]!=='0')for(let d=0;d<6;d++)add([...shift(addr.slice(0,3),DIRECTIONS[d],side,-1),exp.coupling.ports[d^1][addr[3]]]);}
        for(const row of frame.cells)add(row.slice(0,4));
        let checked=0;
        for(const addr of addresses.values()){
          const tr=inspectTransition(exp,oldMap,nextMap,addr);requireValue(tr.ok,'Complete Rule3 transition mismatch in '+exp.id+' at step '+frame.step+', address '+key(addr));
          // Independent inverse construction checks the retained remainder too.
          const inverseInput=tr.inputs.reduce((sum,input)=>sum+BigInt(input.weight)*rawAt(exp,nextMap,input.address)[0],0n);let r=Number((BigInt(tr.next[2])-2n*inverseInput)%6n);if(r<0)r+=6;const oldA=(2n*inverseInput+BigInt(r)-BigInt(tr.next[2]))/6n-tr.next[1];requireValue(r===tr.old[2]&&oldA===tr.old[0]&&tr.next[0]===tr.old[1],'Full inverse mismatch');
          if(++checked%4096===0)await new Promise(resolve=>setTimeout(resolve,0));
        }
        frame.audit={forward_equal:true,inverse_equal:true};checks++;
      }
      if(options.onProgress)options.onProgress({phase:'validate',experiment:options.experiment,totalExperiments:options.totalExperiments,frame:fi+1,totalFrames:exp.frames.length});
      if(fi%20===0)await new Promise(resolve=>setTimeout(resolve,0));
    }
    exp.validation={transitions:checks,hashes_verified:hashes,source,inverse_verified:checks>0,physical_validation:false};return exp;
  }
  async function nativeExperiment(records,catalog){
    requireValue(records.length>0&&records.length<=limits.maxFrames,'Native trace exceeds the frame limit');
    let side,background,fixed,firstStep,totalCells=0;const frames=[];
    for(let i=0;i<records.length;i++){
      const cp=keys(records[i],['format','completed_steps','coupling_fingerprint','experiment'],['format','completed_steps','coupling_fingerprint','experiment'],'Native checkpoint');requireValue(cp.format==='universe24-checkpoint-v1','Expected a complete Universe24 checkpoint, not an initial config or event log');const cfg=keys(cp.experiment,['side','coupling_signs','background','seed_changes','steps'],['side'],'Checkpoint experiment');if(cfg.steps!==undefined)integer(cfg.steps,'Checkpoint requested steps',0,Number.MAX_SAFE_INTEGER,cfg,'steps');
      if(cfg.background!==undefined){array(cfg.background,'Checkpoint background',3);nativeCounter(cfg.background[0],cfg.background,0,'Checkpoint background a');nativeCounter(cfg.background[1],cfg.background,1,'Checkpoint background b');}
      const thisSide=integer(cfg.side,'Checkpoint cube side',3,Number.MAX_SAFE_INTEGER,cfg,'side'),bg=normalizeBackground(cfg.background===undefined?['0','0',2]:cfg.background);
      const signs=cfg.coupling_signs===undefined?[1,1,1]:array(cfg.coupling_signs,'Checkpoint signs',3).map((v,j)=>{integer(v,'Checkpoint sign',-1,1,cfg.coupling_signs,j);requireValue(v===1||v===-1,'Checkpoint sign must be +/-1');return v;});
      const found=catalog.find(c=>c.body_signs.every((v,j)=>v===signs[j]));requireValue(found,'Native checkpoint needs the matching fixed reference tensor in the Presenter catalog');requireValue(cp.coupling_fingerprint===found.fingerprint,'Native checkpoint coupling fingerprint mismatch');
      const step=integer(cp.completed_steps,'Checkpoint completed_steps',0,Number.MAX_SAFE_INTEGER,cp,'completed_steps');
      if(i===0){side=thisSide;background=bg;fixed=found;firstStep=step;}else requireValue(side===thisSide&&equalTriple(background,bg)&&fixed.fingerprint===found.fingerprint,'Trace geometry, background or fixed tensor changed');
      const changes=array(cfg.seed_changes===undefined?[]:cfg.seed_changes,'Checkpoint cells');totalCells+=changes.length;requireValue(totalCells<=limits.maxStoredCells,'Native trace exceeds the stored-cell resource limit');
      const seen=new Set();const cells=changes.map(change=>{keys(change,['position','channel','state'],['position','channel','state'],'Checkpoint cell');const pos=position(change.position,side,'Checkpoint cell position'),g=integer(change.channel,'Checkpoint channel',0,47,change,'channel'),addr=[...pos,g],k=key(addr);requireValue(!seen.has(k),'Duplicate native checkpoint address '+k);seen.add(k);const triple=array(change.state,'Checkpoint triple',3),a=nativeCounter(triple[0],triple,0,'Checkpoint a'),b=nativeCounter(triple[1],triple,1,'Checkpoint b'),r=integer(triple[2],'Checkpoint remainder',0,5,triple,2);return [...addr,a,b,r];}).filter(row=>row[4]!==background[0]||row[5]!==background[1]||row[6]!==background[2]);
      cells.sort(addressCompare);frames.push({step,cells,audit:{forward_equal:null,inverse_equal:null}});
    }
    const first=frames[0].cells[0];return {id:'imported-trace',title:records.length===1?'Imported snapshot':'Imported complete trace',description:'Native full-state checkpoints. All retained channels are available for inspection.',side,background,coupling:fixed,frames,readouts:[],view:{position:first?first.slice(0,3):[0,0,0],channel:first?first[3]:0},provenance:{format:'universe24-checkpoint-v1',first_step:firstStep}};
  }
  async function load(input,catalog=[],options={}){
    requireValue(typeof input==='string','Load expects JSON or JSONL text');requireValue(input.length<=limits.maxBytes&&bytes(input).length<=limits.maxBytes,'Input exceeds the 64 MiB limit; export a smaller complete segment');if(input.charCodeAt(0)===0xFEFF)input=input.slice(1);if(options.onProgress){options.onProgress({phase:'parse'});await new Promise(resolve=>setTimeout(resolve,0));}
    let parsed,source='bundle',nativeRecords=null;
    try{parsed=parse(input);}catch(firstError){
      const lines=input.split(/\r?\n/).filter(line=>line.trim());if(lines.length<=1)throw firstError;
      try{nativeRecords=lines.map(parse);}catch(_){throw firstError;}
      requireValue(nativeRecords.every(x=>x&&x.format==='universe24-checkpoint-v1'),'JSONL must contain complete native checkpoints');source=nativeRecords.length===1?'checkpoint':'trace';
    }
    if(!nativeRecords&&parsed&&parsed.format==='universe24-checkpoint-v1'){nativeRecords=[parsed];source='checkpoint';}
    let incomingCatalog=catalog;
    if(!nativeRecords){keys(parsed,['format','title','catalog','experiments'],['format','experiments'],'Presenter bundle');requireValue(parsed.format===FORMAT,'Unsupported input: use a Presenter bundle or complete native checkpoint/JSONL trace');incomingCatalog=[...array(catalog,'Provided catalog'),...array(parsed.catalog===undefined?[]:parsed.catalog,'Bundle catalog')];}
    else array(incomingCatalog,'Provided catalog');
    requireValue(incomingCatalog.length<=24,'Coupling catalog contains too many entries');
    const bySign=new Map();for(const item of incomingCatalog){const c=await coupling(item,'Catalog coupling'),k=c.body_signs.join(',');if(bySign.has(k))requireValue(bySign.get(k).fingerprint===c.fingerprint,'Conflicting catalog tensors');else bySign.set(k,c);}
    const normalizedCatalog=[...bySign.values()];
    let experiments,title;
    if(nativeRecords){experiments=[await nativeExperiment(nativeRecords,normalizedCatalog)];title='The Presenter';}
    else {experiments=array(parsed.experiments,'Experiments');title=text(parsed.title,'Bundle title','The Presenter',1000);}
    requireValue(experiments.length<=limits.maxExperiments,'Experiment count exceeds '+limits.maxExperiments);
    const normalized=[],ids=new Set(),budget={cells:0};
    for(let i=0;i<experiments.length;i++){const exp=await validateExperiment(experiments[i],budget,source,{...options,experiment:i+1,totalExperiments:experiments.length});requireValue(!ids.has(exp.id),'Experiment IDs must be unique');ids.add(exp.id);normalized.push(exp);}
    const result=deepFreeze({format:FORMAT,title,catalog:normalizedCatalog,experiments:normalized});if(options.onProgress)options.onProgress({phase:'complete',experiments:normalized.length});return result;
  }
  return Object.freeze({parse,load,at,transition,readouts,nodes,phase,stableStringify,sha256,limits});
});
