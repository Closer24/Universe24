"""Independent complete-state review of The Presenter's generic exporter.

These fixtures intentionally avoid the prior guide geometry and channels0/14
interface. An exact matrix-based dense oracle supplies every expected update.
"""
from contextlib import contextmanager
import copy
from itertools import product
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from research.reference.evolution import advance as reference_advance
from research.reference.evolution import addresses, flatten
from research.reference.algebra import coupling as matrix_coupling
from universe24 import Channel, Coupling, Cube, Engine, State
from universe24.experiments.config import checkpoint_data

ROOT=Path(__file__).resolve().parents[1]


def independently_decode_decimal(value):
    """Read canonical decimal strings without changing Python's digit guard."""
    if not isinstance(value,str) or not value:
        raise ValueError('Expected decimal string')
    sign=-1 if value.startswith('-') else 1
    digits=value[1:] if sign<0 else value
    if not digits.isascii() or not digits.isdecimal():
        raise ValueError('Nondecimal counter')
    if len(digits)>1 and digits[0]=='0' or sign<0 and digits=='0':
        raise ValueError('Noncanonical counter')
    result=0
    for offset in range(0,len(digits),7):
        chunk=digits[offset:offset+7]
        result=result*(10**len(chunk))+int(chunk)
    return sign*result


def review_preparation(background_r):
    side=3
    background=Channel(0,0,background_r)
    cells={}
    for g in range(48):
        # A distributed three-dimensional preparation, including every channel.
        address=((2*g+1)%3,(g//3)%3,(g//9+2)%3,g)
        cells[address]=Channel((g%7)-3,(g%5)-2,(2*g+background_r+1)%6)
    # Retained information outside the counter-active projection.
    cells[(2,2,2,47)]=Channel(0,0,(background_r+1)%6)
    return State(Cube(side),background,cells)


def decode_frame(frame,background):
    cells={}
    previous=None
    for row in frame['cells']:
        if len(row)!=7:
            raise ValueError('Invalid row size')
        address=tuple(row[:4])
        if previous is not None and address<=previous:
            raise ValueError('Unsorted or duplicate retained address')
        triple=(independently_decode_decimal(row[4]),
                independently_decode_decimal(row[5]),row[6])
        if triple==background:
            raise ValueError('Redundant background row')
        cells[address]=triple
        previous=address
    return cells


def check_state_hash(experiment,frame):
    expected=hashlib.sha256(json.dumps({'side':experiment['side'],
                'background':experiment['background'],'cells':frame['cells']},
                sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return frame['state_sha256']==expected


@contextmanager
def scratch_directory():
    root=ROOT/'runs';root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='presenter-review-',dir=root) as folder:
        yield Path(folder)


class PresenterIndependentReviewTests(unittest.TestCase):
    def test_all_channels_signs_and_backgrounds_match_matrix_oracle(self):
        from research.presenter.export import capture
        for signs in product((-1,1),repeat=3):
            engine=Engine(Coupling(signs))
            for remainder in range(6):
                with self.subTest(signs=signs,background=remainder):
                    initial=review_preparation(remainder)
                    experiment=capture(engine,initial,2,id='unseen-distributed',
                        title='All channels at arbitrary coordinates',
                        view={'position':[2,2,2],'channel':47})
                    self.assertEqual(experiment['side'],3)
                    self.assertEqual(experiment['background'],['0','0',remainder])
                    self.assertEqual(experiment['coupling']['body_signs'],list(signs))
                    independent_tensor=matrix_coupling(signs)
                    self.assertEqual(experiment['coupling']['ports'],[list(r) for r in independent_tensor.ports])
                    self.assertEqual(experiment['coupling']['weights'],[list(r) for r in independent_tensor.weights])
                    self.assertEqual(len(experiment['frames']),3)
                    oracle=flatten(initial.cells,3,tuple(initial.background))
                    for step,frame in enumerate(experiment['frames']):
                        self.assertEqual(frame['step'],step)
                        decoded=decode_frame(frame,tuple(initial.background))
                        dense=flatten(decoded,3,tuple(initial.background))
                        self.assertEqual(dense,oracle)
                        self.assertTrue(check_state_hash(experiment,frame))
                        if step==0:
                            self.assertIsNone(frame['audit']['forward_equal'])
                            self.assertIsNone(frame['audit']['inverse_equal'])
                        else:
                            self.assertIs(frame['audit']['forward_equal'],True)
                            self.assertIs(frame['audit']['inverse_equal'],True)
                        if step<2:
                            oracle=reference_advance(oracle,3,signs)
                    # A remainder-only address is retained even though it has no hand.
                    first=decode_frame(experiment['frames'][0],tuple(initial.background))
                    self.assertEqual(first[(2,2,2,47)],(0,0,(remainder+1)%6))

    def test_arbitrary_size_counter_export_preserves_exact_integer_and_guard(self):
        from research.presenter.export import capture,bundle,write_bundle
        digit_limit=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
        huge=10**5000+7
        initial=State(Cube(3),Channel(0,0,1),{(2,0,1,47):Channel(-huge,huge+13,5),
                                                    (0,2,1,33):Channel(0,0,4)})
        engine=Engine(Coupling((-1,1,-1)))
        experiment=capture(engine,initial,2,id='large-signed-channel47',
                           view={'position':[2,0,1],'channel':47})
        oracle=flatten(initial.cells,3,tuple(initial.background))
        for step,frame in enumerate(experiment['frames']):
            self.assertEqual(flatten(decode_frame(frame,tuple(initial.background)),3,
                                     tuple(initial.background)),oracle)
            self.assertTrue(check_state_hash(experiment,frame))
            if step<2:oracle=reference_advance(oracle,3,(-1,1,-1))
        row=next(row for row in experiment['frames'][0]['cells'] if row[:4]==[2,0,1,47])
        self.assertEqual(len(row[4]),5002)
        self.assertEqual(independently_decode_decimal(row[4]),-huge)
        self.assertEqual(independently_decode_decimal(row[5]),huge+13)
        with scratch_directory() as folder:
            target=folder/'huge.json'
            portable=bundle([experiment])
            write_bundle(target,portable)
            self.assertEqual(json.loads(target.read_text()),portable)
            before=target.read_bytes()
            with self.assertRaises((FileExistsError,ValueError)):
                write_bundle(target,portable)
            self.assertEqual(target.read_bytes(),before)
        if digit_limit is not None:
            self.assertEqual(sys.get_int_max_str_digits(),digit_limit)

    def test_native_huge_snapshot_is_lossless_and_not_a_transition_claim(self):
        from research.presenter.export import from_trace
        digit_limit=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
        engine=Engine(Coupling((1,-1,-1)))
        cp=checkpoint_data(State(Cube(5),Channel(0,0,3),{(4,1,2,47):Channel(1,0,5)}),engine,37)
        cp['experiment']['seed_changes'][0]['state'][0]='COUNTER_PLACEHOLDER'
        digits='1'+'0'*4999+'7'
        raw=json.dumps(cp).replace('"COUNTER_PLACEHOLDER"','-'+digits)
        with scratch_directory() as folder:
            path=folder/'snapshot.json';path.write_text(raw)
            experiment=from_trace(path,id='snapshot-other-channel')
        self.assertEqual(len(experiment['frames']),1)
        frame=experiment['frames'][0]
        self.assertEqual(frame['step'],37)
        self.assertEqual(frame['cells'][0][4],'-'+digits)
        self.assertIsNone(frame['audit']['forward_equal'])
        self.assertIsNone(frame['audit']['inverse_equal'])
        self.assertTrue(check_state_hash(experiment,frame))
        if digit_limit is not None:self.assertEqual(sys.get_int_max_str_digits(),digit_limit)

    def test_full_trace_rejects_hidden_remainder_corruption_and_missing_update(self):
        from research.presenter.export import from_trace
        engine=Engine(Coupling((-1,-1,1)))
        initial=State(Cube(5),Channel(0,0,4),{(3,0,2,31):Channel(2,-3,1),
                                                    (4,4,1,47):Channel(0,0,5)})
        checkpoints=[checkpoint_data(state,engine,t+19)
                     for t,state in enumerate(engine.evolve(initial,2))]
        with scratch_directory() as folder:
            path=folder/'native.jsonl'
            path.write_text('\n'.join(json.dumps(c) for c in checkpoints)+'\n')
            imported=from_trace(path)
            self.assertEqual([f['step'] for f in imported['frames']],[19,20,21])
            mutated=json.loads(json.dumps(checkpoints))
            final=mutated[-1]['experiment']['seed_changes']
            hidden=next((entry for entry in final if entry['position']==[4,4,1] and entry['channel']==47),None)
            if hidden is None:
                final.append({'position':[4,4,1],'channel':47,'state':[0,0,3]})
            else:
                hidden['state'][2]=(hidden['state'][2]+1)%6
            path.write_text('\n'.join(json.dumps(c) for c in mutated)+'\n')
            with self.assertRaises(ValueError):from_trace(path)
            path.write_text(json.dumps(checkpoints[0])+'\n'+json.dumps(checkpoints[2])+'\n')
            with self.assertRaises(ValueError):from_trace(path)

    def test_fixed_observation_and_view_do_not_change_or_alias_trajectory(self):
        from research.presenter.export import capture
        engine=Engine(Coupling((-1,1,1)))
        initial=review_preparation(5)
        saved=dict(initial.cells)
        readout={'id':'off-axis-record','label':'Channel47 remainder',
                 'kind':'all_equal','clauses':[{'address':[2,2,2,47],
                                               'component':'r','equals':'0'}]}
        observed=capture(engine,initial,3,readouts=[readout],
                         view={'position':[0,1,2],'channel':33})
        plain=capture(engine,initial,3,view={'position':[2,2,2],'channel':47})
        self.assertEqual(observed['frames'],plain['frames'])
        self.assertEqual(dict(initial.cells),saved)
        self.assertEqual(observed['readouts'],[readout])
        # Changing a caller-owned description after capture cannot change the
        # registered predicate inside the exported immutable-by-convention run.
        readout['clauses'][0]['address'][3]=0
        self.assertEqual(observed['readouts'][0]['clauses'][0]['address'][3],47)

    def test_self_consistent_hash_does_not_hide_invalid_complete_transition(self):
        from research.presenter.export import capture,bundle,validate_bundle
        initial=State(Cube(5),Channel(0,0,2),{(3,1,4,47):Channel(2,-1,5),
                                                    (1,4,2,33):Channel(0,0,4)})
        legitimate=bundle([capture(Engine(Coupling((1,-1,1))),initial,2)])
        forged=copy.deepcopy(legitimate)
        experiment=forged['experiments'][0]
        frame=experiment['frames'][-1]
        hidden=next(row for row in frame['cells'] if row[:4]==[1,4,2,33])
        hidden[6]=5
        # A fresh digest proves only that bytes agree. This records an invalid
        # update outside the selected node, despite plausible audit metadata.
        frame['state_sha256']=hashlib.sha256(json.dumps({
            'side':experiment['side'],'background':experiment['background'],
            'cells':frame['cells']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
        self.assertTrue(check_state_hash(experiment,frame))
        self.assertTrue(frame['audit']['forward_equal'])
        with self.assertRaisesRegex(ValueError,'Rule3'):
            validate_bundle(forged)
        # Zero-transition snapshots cannot acquire a transition claim merely
        # by setting their imported audit flags.
        forged=copy.deepcopy(legitimate)
        forged['experiments'][0]['frames'][0]['audit']={
            'forward_equal':True,'inverse_equal':True}
        with self.assertRaisesRegex(ValueError,'audit'):
            validate_bundle(forged)

    @unittest.skipUnless(shutil.which('node'),'Node.js is required for the independent browser-data check')
    def test_browser_data_rechecks_fresh_captures_without_precision_or_hidden_state_loss(self):
        from research.presenter.export import capture,bundle
        experiments=[]
        for signs in product((-1,1),repeat=3):
            for remainder in range(6):
                experiments.append(capture(Engine(Coupling(signs)),review_preparation(remainder),2,
                    id=f'signs-{signs}-background-{remainder}',
                    view={'position':[2,2,2],'channel':47}))
        huge=10**5000+7
        experiments.append(capture(Engine(Coupling((-1,1,-1))),
            State(Cube(3),Channel(0,0,1),{(2,0,1,47):Channel(-huge,huge+13,5)}),1,
            id='huge-counter'))
        script=r'''
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const D=require('./research/presenter/data.js');
(async()=>{
  const source=JSON.parse(fs.readFileSync(0,'utf8'));
  const loaded=await D.load(JSON.stringify(source));
  assert.equal(loaded.experiments.length,49);
  let rows=0;
  for(let ei=0;ei<source.experiments.length;ei++){
    const original=source.experiments[ei],exp=loaded.experiments[ei];
    assert.equal(exp.validation.transitions,original.frames.length-1);
    assert.equal(exp.validation.hashes_verified,original.frames.length);
    assert.equal(exp.validation.physical_validation,false);
    assert(Object.isFrozen(exp)&&Object.isFrozen(exp.frames[0].cells));
    for(let fi=0;fi<original.frames.length;fi++){
      assert.deepEqual(exp.frames[fi].cells,original.frames[fi].cells);
      assert.equal(exp.frames[fi].state_sha256,original.frames[fi].state_sha256);
      const stored=new Map(original.frames[fi].cells.map(row=>[row.slice(0,4).join(','),row.slice(4)]));
      for(let x=0;x<3;x++)for(let y=0;y<3;y++)for(let z=0;z<3;z++)for(let g=0;g<48;g++){
        const addr=[x,y,z,g],expected=stored.get(addr.join(','))||original.background;
        assert.deepEqual(D.at(exp,fi,addr),[BigInt(expected[0]),BigInt(expected[1]),expected[2]]);
        if(fi)assert(D.transition(exp,fi,addr).ok);
        rows++;
      }
    }
  }
  const huge=loaded.experiments.at(-1);
  const triple=D.at(huge,0,[2,0,1,47]);
  assert.equal(triple[0].toString().length,5002);
  const phase=D.phase(triple[0],triple[1]);
  assert(Number.isFinite(phase.x)&&Number.isFinite(phase.y)&&!phase.atRest);
  assert.throws(()=>{huge.frames[0].cells[0][4]='0';},TypeError);
  const forged=JSON.parse(JSON.stringify(source));
  const exp=forged.experiments[0],frame=exp.frames[1];
  const row=frame.cells.find(r=>r.slice(0,4).join(',')==='2,2,2,47');
  row[6]=(row[6]+2)%6;
  frame.state_sha256=await D.sha256({side:exp.side,background:exp.background,cells:frame.cells});
  await assert.rejects(D.load(JSON.stringify(forged)),/Rule3/);
  console.log(JSON.stringify({experiments:loaded.experiments.length,exact_addresses:rows,
    forged_transition_rejected:true,immutable:true}));
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
'''
        result=subprocess.run(['node','-e',script],input=json.dumps(bundle(experiments)),
            cwd=ROOT,text=True,capture_output=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(result.stdout)
        self.assertEqual(report['experiments'],49)
        self.assertEqual(report['exact_addresses'],189216)
        self.assertIs(report['forged_transition_rejected'],True)

    @unittest.skipUnless(shutil.which('node'),'Node.js is required for the independent importer check')
    def test_browser_import_scope_rejects_unknown_model_fields_and_false_audit(self):
        from research.presenter.export import capture,bundle
        initial=State(Cube(5),Channel(0,0,3),{(4,1,2,47):Channel(-7,4,5)})
        engine=Engine(Coupling((1,-1,-1)))
        source=bundle([capture(engine,initial,0,start_step=37,id='unproven-preparation')])
        source['experiments'][0]['provenance'].update({
            'preparation':'Unverified metadata from an external search',
            'physical_validation':True,'seed':None})
        payload={'bundle':source,'checkpoint':checkpoint_data(initial,engine,37)}
        script=r'''
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs');
const D=require('./research/presenter/data.js');
(async()=>{
  const {bundle,checkpoint}=JSON.parse(fs.readFileSync(0,'utf8'));
  const catalog=bundle.catalog;
  const clone=x=>JSON.parse(JSON.stringify(x));
  const snapshot=(await D.load(JSON.stringify(bundle))).experiments[0];
  assert.equal(snapshot.validation.transitions,0);
  assert.equal(snapshot.validation.inverse_verified,false);
  assert.equal(snapshot.validation.physical_validation,false);
  assert.equal(D.transition(snapshot,0,[4,1,2,47]),null);
  const native=(await D.load(JSON.stringify(checkpoint),catalog)).experiments[0];
  assert.equal(native.frames[0].step,37);
  assert.equal(native.validation.transitions,0);
  assert.deepEqual(D.at(native,0,[4,1,2,47]),[-7n,4n,5]);
  let rejected=0;
  for(const mutate of [
    cp=>{cp.num=2;},cp=>{cp.experiment.num=2;},
    cp=>{cp.experiment.steps=-1;},
    cp=>{cp.experiment.seed_changes[0].state[0]='-7';},
    cp=>{cp.experiment.seed_changes[0].intervention=true;}
  ]){
    const cp=clone(checkpoint);mutate(cp);
    await assert.rejects(D.load(JSON.stringify(cp),catalog));rejected++;
  }
  await assert.rejects(D.load(JSON.stringify(checkpoint).replace('"steps":0','"steps":0.0'),catalog));rejected++;
  const altered=clone(bundle);altered.experiments[0].coupling.num=2;
  await assert.rejects(D.load(JSON.stringify(altered)),/coupling|tensor|fields/i);rejected++;
  for(const audit of [{forward_equal:true,inverse_equal:true},
                     {forward_equal:false,inverse_equal:false}]){
    const forged=clone(bundle);forged.experiments[0].frames[0].audit=audit;
    await assert.rejects(D.load(JSON.stringify(forged)),/audit/i);rejected++;
  }
  console.log(JSON.stringify({rejected,snapshot_transitions:0,physical_claim_accepted:false}));
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
'''
        result=subprocess.run(['node','-e',script],input=json.dumps(payload),
            cwd=ROOT,text=True,capture_output=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),{
            'rejected':9,'snapshot_transitions':0,'physical_claim_accepted':False})

    def test_packaged_html_preserves_unseen_data_and_pins_verification_sources(self):
        from research.presenter.export import capture,bundle,write_bundle
        from research.presenter.build import build
        initial=State(Cube(4),Channel(0,0,5),{(3,0,2,47):Channel(-9,7,3)})
        marker='Unseen </script><img src="https://example.invalid/injected">'
        original=bundle([capture(Engine(Coupling((-1,-1,1))),initial,1,
            id='not-a-demonstration',title=marker,
            view={'position':[3,0,2],'channel':47})],title=marker)
        with scratch_directory() as folder:
            source=folder/'input.json';write_bundle(source,original)
            html_path,manifest_path=build(source,folder/'Presenter.html')
            html=html_path.read_text()
            manifest=json.loads(manifest_path.read_text())
            bootstrap=html.split('<script>globalThis.PRESENTER_BUNDLE=',1)[1].split(';</script>',1)[0]
            self.assertEqual(json.loads(bootstrap),original)
            self.assertNotIn(marker,html)
            self.assertNotIn('<script src=',html)
            self.assertEqual(manifest['html_sha256'],hashlib.sha256(html_path.read_bytes()).hexdigest())
            self.assertEqual(manifest['bundle_sha256'],hashlib.sha256(source.read_bytes()).hexdigest())
            verifier=manifest['verifier_source_sha256']
            self.assertIn('research/presenter/export.py',verifier)
            for name,digest in json.loads((ROOT/'research/reproducibility/base_engine.json').read_text())['source_sha256'].items():
                self.assertEqual(verifier[name],digest)
            before=html_path.read_bytes()
            with self.assertRaises(FileExistsError):build(source,html_path)
            self.assertEqual(html_path.read_bytes(),before)
            forged=copy.deepcopy(original)
            forged['experiments'][0]['frames'][1]['state_sha256']='0'*64
            source.write_text(json.dumps(forged))
            with self.assertRaises(ValueError):build(source,folder/'invalid.html')
            self.assertFalse((folder/'invalid.html').exists())
            self.assertFalse((folder/'invalid.html.manifest.json').exists())

    def test_resource_limits_reject_incomplete_capture_and_trace(self):
        from research.presenter.export import capture,from_trace
        engine=Engine(Coupling())
        initial=review_preparation(2)
        with self.assertRaises((ValueError,TimeoutError)):
            capture(engine,initial,2,max_frames=2)
        with self.assertRaises((ValueError,TimeoutError)):
            capture(engine,initial,0,max_cells=1)
        with self.assertRaises((ValueError,TimeoutError)):
            capture(engine,initial,0,max_bytes=64)
        with scratch_directory() as folder:
            path=folder/'too-long.jsonl'
            path.write_text('\n'.join(json.dumps(checkpoint_data(s,engine,t))
                          for t,s in enumerate(engine.evolve(initial,2)))+'\n')
            with self.assertRaises((ValueError,TimeoutError)):
                from_trace(path,max_frames=2)

    def test_reference_core_hashes_remain_pinned(self):
        manifest=json.loads((ROOT/'research/reproducibility/base_engine.json').read_text())
        actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((ROOT/'universe24').rglob('*.py'))}
        self.assertEqual(actual,manifest['source_sha256'])


if __name__=='__main__':unittest.main()
