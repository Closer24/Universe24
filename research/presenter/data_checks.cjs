#!/usr/bin/env node
'use strict';
/* Exact-state tests use fresh reference-engine records, never a demo-ID branch. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {spawnSync}=require('node:child_process');
const Data=require('./data.js');
const root=path.resolve(__dirname,'../..');
const generator=String.raw`
from itertools import product
import random
from research.presenter.export import capture,bundle,canonical
from universe24.core import Coupling,Engine,State
from universe24.core.state import Cube,Channel
experiments=[]
for i,signs in enumerate(product((-1,1),repeat=3)):
    for bg in range(6):
        rng=random.Random(1000+6*i+bg)
        cells={(1,1,1,g):Channel(rng.randint(-7,7),rng.randint(-7,7),(g+bg)%6) for g in range(48)}
        state=State(Cube(3),Channel(0,0,bg),cells)
        experiments.append(capture(Engine(Coupling(signs)),state,2,id=f'generated-{i}-{bg}',view={'position':[1,1,1],'channel':47}))
large=10**5000+1234567
state=State(Cube(5),Channel(0,0,3),{(4,0,0,47):Channel(large,-large-7,5),(0,4,0,13):Channel(0,0,1)})
experiments.append(capture(Engine(Coupling((-1,1,-1))),state,2,id='generated-huge'))
side=2**53-1
state=State(Cube(side),Channel(0,0,5),{(side-1,0,side-1,47):Channel(9,-17,1),(0,0,0,5):Channel(-1,3,0)})
experiments.append(capture(Engine(Coupling((-1,-1,1))),state,2,id='generated-wide'))
state=State(Cube(5),Channel(0,0,2),{(2,2,2,47):Channel(1,0,2)})
readout={'id':'declared-observer','label':'Fixed record','kind':'all_equal','clauses':[{'address':[2,2,2,47],'component':'b','equals':'-1'}]}
experiments.append(capture(Engine(),state,3,id='generated-readout',readouts=[readout]))
print(canonical(bundle(experiments,title='Generated exact-state tests')))
`;
const clone=x=>JSON.parse(JSON.stringify(x));
async function digest(exp,fi){exp.frames[fi].state_sha256=await Data.sha256({side:exp.side,background:exp.background,cells:exp.frames[fi].cells});}
function one(exp,catalog=[]){return {format:'universe24-presenter-v1',title:'Test',catalog,experiments:[exp]};}
function checkpoint(exp,fi){const frame=exp.frames[fi];return {format:'universe24-checkpoint-v1',completed_steps:frame.step,coupling_fingerprint:exp.coupling.fingerprint,experiment:{side:exp.side,coupling_signs:exp.coupling.body_signs,background:exp.background.map(Number),steps:0,seed_changes:frame.cells.map(row=>({position:row.slice(0,3),channel:row[3],state:[row[4],row[5],row[6]]}))}};}
// Preserve literal counters as integer JSON tokens, including 5001 digits.
function nativeText(cp){const token='__RAW_COUNTER_';const counters=[];const object=clone(cp);for(const cell of object.experiment.seed_changes)for(let j=0;j<2;j++){counters.push(String(cell.state[j]));cell.state[j]=token+(counters.length-1)+'__';}return JSON.stringify(object).replace(/"__RAW_COUNTER_(\d+)__"/g,(_,i)=>counters[Number(i)]);}
async function rejectBundle(exp,pattern){await assert.rejects(Data.load(JSON.stringify(one(exp))),pattern);}
const results=[];
async function test(name,fn){const started=Date.now();await fn();results.push({name,passed:true,milliseconds:Date.now()-started});}
(async()=>{
  const produced=spawnSync(process.env.PYTHON||'python',['-c',generator],{cwd:root,encoding:'utf8',maxBuffer:Data.limits.maxBytes,timeout:120000});
  assert.equal(produced.status,0,produced.stderr||produced.error?.message);
  const original=JSON.parse(produced.stdout);let normalized;
  await test('all eight tensors, six remainders and 48 channels validate complete recorded transitions',async()=>{
    normalized=await Data.load(produced.stdout);
    assert.equal(normalized.experiments.length,51);assert.equal(normalized.catalog.length,8);
    for(const exp of normalized.experiments){assert.equal(exp.validation.transitions,exp.frames.length-1);assert.equal(exp.validation.hashes_verified,exp.frames.length);assert.equal(exp.validation.inverse_verified,true);assert.equal(exp.validation.physical_validation,false);for(let fi=0;fi<exp.frames.length;fi++)for(const row of exp.frames[fi].cells){assert.deepEqual(Data.at(exp,fi,row.slice(0,4)),[BigInt(row[4]),BigInt(row[5]),row[6]]);if(fi)assert.equal(Data.transition(exp,fi,row.slice(0,4)).ok,true);}}
  });
  const sample=original.experiments[0], huge=original.experiments[48],wide=normalized.experiments[49],readout=normalized.experiments[50];
  await test('native imports resolve every fixed tensor and keep snapshot scope',async()=>{
    for(let i=0;i<48;i+=6){const imported=await Data.load(nativeText(checkpoint(original.experiments[i],0)),normalized.catalog);assert.deepEqual(imported.experiments[0].coupling.body_signs,original.experiments[i].coupling.body_signs);assert.equal(imported.experiments[0].validation.transitions,0);}
  });
  await test('5001-digit counters and native raw integer tokens stay exact',async()=>{
    const exp=normalized.experiments[48],addr=[4,0,0,47],a=Data.at(exp,0,addr)[0];assert.equal(String(a).length,5001);assert.equal(String(a),huge.frames[0].cells.find(r=>r[3]===47)[4]);
    const snapshot=await Data.load(nativeText(checkpoint(huge,0)),normalized.catalog);assert.equal(Data.at(snapshot.experiments[0],0,addr)[0],a);assert.equal(snapshot.experiments[0].validation.transitions,0);assert.equal(snapshot.experiments[0].validation.inverse_verified,false);assert.equal(snapshot.experiments[0].validation.hashes_verified,0);
    const trace=await Data.load(huge.frames.map((_,i)=>nativeText(checkpoint(huge,i))).join('\n'),normalized.catalog);assert.equal(trace.experiments[0].validation.transitions,2);assert.equal(trace.experiments[0].validation.source,'trace');
    const phase=Data.phase(a,-a);assert(Number.isFinite(phase.x)&&Number.isFinite(phase.y));assert(Math.abs(phase.x-Math.SQRT1_2)<1e-12);assert(Math.abs(phase.y+Math.SQRT1_2)<1e-12);
  });
  await test('negative division uses Euclidean remainder and all six signed inputs',async()=>{
    let count=0;
    for(const exp of normalized.experiments.slice(0,48))for(const row of exp.frames[1].cells){const tr=Data.transition(exp,1,row.slice(0,4));assert.equal(tr.inputs.length,6);assert.equal(tr.u,tr.inputs.reduce((n,x)=>n+x.product,0n));assert.equal(tr.numerator,6n*tr.ell+BigInt(tr.remainder));assert(tr.remainder>=0&&tr.remainder<6);if(tr.numerator<0n&&tr.numerator%6n!==0n){assert.equal(tr.ell,tr.numerator/6n-1n);count++;}}
    assert(count>0);
  });
  await test('maximum safe cube size wraps exactly at both periodic boundaries',async()=>{
    const side=Number.MAX_SAFE_INTEGER;assert.equal(wide.side,side);
    const t0=Data.transition(wide,1,[0,0,0,47]);assert.deepEqual(t0.inputs.map(x=>x.address.slice(0,3)),[[1,0,0],[side-1,0,0],[0,1,0],[0,side-1,0],[0,0,1],[0,0,side-1]]);
    const t1=Data.transition(wide,1,[side-1,side-1,side-1,47]);assert.deepEqual(t1.inputs[0].address.slice(0,3),[0,side-1,side-1]);assert.deepEqual(t1.inputs[1].address.slice(0,3),[side-2,side-1,side-1]);
  });
  await test('fixed readout rising edges do not depend on selected coordinates',async()=>{
    assert.equal(Data.readouts(readout,0)[0].value,false);assert.equal(Data.readouts(readout,1)[0].edge,true);
    const before=Data.readouts(readout,1);for(let g=0;g<48;g++){Data.at(readout,1,[0,0,0,g]);Data.transition(readout,1,[4,3,1,g]);}assert.deepEqual(Data.readouts(readout,1),before);
    assert.equal(Data.transition(readout,0,[0,0,0,0]),null);
  });
  await test('stored remainder-only fields and background channels remain accessible',async()=>{
    const exp=normalized.experiments[48],node=Data.nodes(exp,0).find(n=>n.position.join(',')==='0,4,0');assert.equal(node.remainder_only_channels,1);assert.equal(node.counter_channels,0);assert.equal(node.stored_channels,1);
    for(let g=0;g<48;g++)assert.deepEqual(Data.at(exp,0,[2,2,2,g]),[0n,0n,3]);
  });
  await test('source state, declared readouts and cached nodes cannot be mutated',async()=>{
    assert(Object.isFrozen(normalized));assert(Object.isFrozen(readout.frames[0].cells));assert(Object.isFrozen(readout.readouts[0].clauses[0]));assert.throws(()=>{readout.frames[0].cells[0][4]='999';},TypeError);assert.throws(()=>{Data.at(readout,0,[2,2,2,47])[0]=99n;},TypeError);assert.throws(()=>{Data.nodes(readout,0)[0].channels.push(1);},TypeError);
  });
  await test('hidden remainder corruption is rejected even with a recomputed hash and passing flags',async()=>{
    const exp=clone(huge);const row=exp.frames[1].cells.find(r=>r[0]===0&&r[1]===4&&r[2]===0&&r[3]===13);assert(row);row[6]=(row[6]+1)%6;await digest(exp,1);await rejectBundle(exp,/transition mismatch/);
  });
  await test('omitting an expected nonbackground receiver is detected as full-state corruption',async()=>{
    const exp=clone(sample);exp.frames[1].cells.splice(0,1);await digest(exp,1);await rejectBundle(exp,/transition mismatch/);
  });
  await test('inserting an unexpected distant remainder fails complete-state validation',async()=>{
    const exp=clone(huge);exp.frames[1].cells.push([2,2,2,46,'0','0',0]);exp.frames[1].cells.sort((a,b)=>{for(let j=0;j<4;j++){if(a[j]!==b[j])return a[j]<b[j]?-1:1;}return 0;});await digest(exp,1);await rejectBundle(exp,/transition mismatch/);
  });
  await test('a changed tensor cannot self-authorize through a recomputed fingerprint',async()=>{
    const exp=clone(sample);[exp.coupling.ports[0][0],exp.coupling.ports[0][1]]=[exp.coupling.ports[0][1],exp.coupling.ports[0][0]];exp.coupling.fingerprint=await Data.sha256(JSON.stringify([exp.coupling.model,exp.coupling.ports,exp.coupling.weights]));await rejectBundle(exp,/routing differs/);
    const exp2=clone(sample);exp2.coupling.weights[0][0]*=-1;exp2.coupling.fingerprint=await Data.sha256(JSON.stringify([exp2.coupling.model,exp2.coupling.ports,exp2.coupling.weights]));await rejectBundle(exp2,/weights differ/);
  });
  await test('digest, address, order, remainder and consecutive-step violations fail explicitly',async()=>{
    for(const [mutation,pattern] of [[e=>e.frames[0].state_sha256='0'.repeat(64),/digest mismatch/],[e=>e.frames[0].cells[0][0]=e.side,/exact safe integer/],[e=>e.frames[0].cells[0][3]=48,/exact safe integer/],[e=>e.frames[0].cells[0][6]=6,/exact safe integer/],[e=>e.frames[0].cells.splice(1,0,clone(e.frames[0].cells[0])),/sorted and unique/],[e=>e.frames[1].step+=1,/consecutive/],[e=>e.coupling.fingerprint='0'.repeat(64),/fingerprint/]]){const exp=clone(sample);mutation(exp);await rejectBundle(exp,pattern);}
  });
  await test('strict parser rejects duplicates, nonfinite values and float integer fields',async()=>{
    for(const raw of ['{"x":1,"x":2}','{"nested":{"x":1,"x":2}}','{"x":NaN}','{"x":Infinity}','{"x":1e999}','[01]','[1,]'])assert.throws(()=>Data.parse(raw));
    const raw=JSON.stringify(one(sample));await assert.rejects(Data.load(raw.replace('"side":3','"side":3.0')),/exact safe integer/);
    for(const value of ['01','-0','+1','1.0','1e2']){const exp=clone(sample);exp.frames[0].cells[0][4]=value;await rejectBundle(exp,/canonical decimal/);}
    assert.equal(Data.parse('{"a":123456789012345678901234567890}').a,'123456789012345678901234567890');
    const safe=Data.parse('{"__proto__":{"polluted":true}}');assert.equal(Object.getPrototypeOf(safe),null);assert.equal({}.polluted,undefined);
  });
  await test('native adapters reject unsupported fields, quoted counters and invalid requested steps',async()=>{
    const base=checkpoint(sample,0);
    for(const mutate of [cp=>cp.num=2,cp=>cp.experiment.num=2,cp=>cp.experiment.steps=-1,cp=>cp.experiment.seed_changes[0].gate=true]){const cp=clone(base);mutate(cp);await assert.rejects(Data.load(nativeText(cp),normalized.catalog));}
    await assert.rejects(Data.load(nativeText(base).replace('"steps":0','"steps":1.0'),normalized.catalog),/exact safe integer/);
    await assert.rejects(Data.load(JSON.stringify(base),normalized.catalog),/integer JSON token/);
    const imported=await Data.load('\uFEFF'+nativeText(base),normalized.catalog);assert.equal(imported.experiments[0].validation.transitions,0);
  });
  await test('unknown portable semantic fields cannot silently declare a different model',async()=>{
    for(const mutate of [e=>e.num=2,e=>e.coupling.dynamic=true,e=>e.frames[0].gate=true,e=>e.frames[0].audit.selected=true,e=>e.view.observer_changes_state=true]){const exp=clone(sample);mutate(exp);await rejectBundle(exp,/unsupported fields/);}
    const raw=one(clone(sample));raw.selection_rule='maximize';await assert.rejects(Data.load(JSON.stringify(raw)),/unsupported fields/);
  });
  await test('snapshot audit assertions cannot claim an unrecorded transition',async()=>{
    const exp=clone(sample);exp.frames=exp.frames.slice(0,1);exp.frames[0].audit={forward_equal:true,inverse_equal:true};await rejectBundle(exp,/audit flags/);
  });
  await test('declared resource bounds reject oversized counters and whole JSONL inputs',async()=>{
    const exp=clone(sample);exp.frames[0].cells[0][4]='1'.repeat(Data.limits.maxCounterDigits+1);await rejectBundle(exp,/digit limit/);
    const cp=nativeText(checkpoint(sample,0));await assert.rejects(Data.load(cp+'\n'+' '.repeat(Data.limits.maxBytes)+'\n'+cp,normalized.catalog),/64 MiB/);
    const frames=clone(sample);frames.frames=Array(Data.limits.maxFrames+1).fill(frames.frames[0]);await rejectBundle(frames,/complete frames/);
    const count=one(clone(sample));count.experiments=Array(Data.limits.maxExperiments+1).fill(count.experiments[0]);await assert.rejects(Data.load(JSON.stringify(count)),/Experiment count/);
    const cells=clone(sample);cells.frames=cells.frames.slice(0,1);cells.frames[0].cells=Array(Data.limits.maxStoredCells+1).fill(cells.frames[0].cells[0]);await rejectBundle(cells,/Total stored cells/);
    const empty=await Data.load(JSON.stringify({format:'universe24-presenter-v1',catalog:original.catalog,experiments:[]}));assert.equal(empty.experiments.length,0);assert.equal(empty.catalog.length,8);
  });
  const report={format:'universe24-presenter-data-checks-v1',passed:results.length,generated_experiments:normalized.experiments.length,verified_transitions:normalized.experiments.reduce((n,e)=>n+e.validation.transitions,0),limits:Data.limits,checks:results};
  if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),JSON.stringify(report,null,2)+'\n');
  process.stdout.write(JSON.stringify(report)+'\n');
})().catch(error=>{process.stderr.write(error.stack+'\n');process.exitCode=1;});
