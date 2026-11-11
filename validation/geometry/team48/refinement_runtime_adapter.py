"""Validation-only handoff of projective44 to the pinned single-system runtime.

This module constructs research inputs, exports them as inert JSON, and invokes
an isolated copy of main's existing create_bundle/run_bundle/verify_run APIs.
It never adds a production model selector or changes physical acceptance gates.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from universe24.core import Engine
from . import refinement_integer_projective as projective
from .temporal_repair_projective import BUILDER, NAMES, prepared

ROOT = Path(__file__).resolve().parents[3]
MAIN_PIN = 'c2d6b05a7b8e32cfad40162df0377335c8dc4577'
EXPECTED_RUNTIME_BLOBS = {
    "universe24/__init__.py": "fe744c2b17527c0581549fda9d3b6bcdcde00b42",
    "universe24/core/__init__.py": "874ed911071259b92a408fd4715dac191554d748",
    "universe24/core/channels.py": "945d9467a38fb416f4c8a1fa2283c422de195592",
    "universe24/core/engine.py": "8655e98d488023a74838c9c5614ed83223c06854",
    "universe24/core/exact_json.py": "13fb6bc9284e92e0662ea8db5ce08fab0b47af11",
    "universe24/core/lattice.py": "6f7d0cb725a1242a1e425c98d4b4125802d4fea8",
    "universe24/core/reciprocity.py": "11a92acf2bd484c68e934fd8d55410cc37c34e33",
    "universe24/core/reversors.py": "d887ca09c82d7114e8eb88df2e2fc9adfc97f321",
    "universe24/core/tensor.py": "ad1d18258b0682bf0ad2225e34f326fe051f69a6",
    "universe24/system/__init__.py": "ce1c2374a89549bc22bf692daa167c2effd69c35",
    "universe24/system/bundle.py": "6d485f5aa65493d0622f4c464c2b27d2ea04264a",
    "universe24/system/decoder.py": "c39d952f002d1c29af3da439aa51536ece6a661d",
    "universe24/system/runtime.py": "b1020c96df415ddf7a054bc6ed3f1424aa0b4bf3"
}



def channel_manifest(program):
    denominator=program.tensor.names[0]
    rows=[]
    for index,name in enumerate(program.tensor.names):
        field=name.removeprefix('projective.')
        if index==0:
            owner='geometry.projective_encoding'
            purpose='Common positive homogeneous denominator and reversible memory; no physical clock'
            dependencies=[name]
        elif field.startswith(('diag_','B','K','G')):
            owner='geometry.shared_frame'
            purpose='Retained numerator of the single metric/frame/curvature field '+field
            if field.startswith('diag_'):
                axis=field[-1]
                dependencies=[denominator,f'projective.diag_p{axis}',f'projective.diag_q{axis}']
            else: dependencies=[denominator,name]
        elif field=='dust_amplitude':
            owner='matter.normal_dust'
            purpose='Signed dust amplitude numerator; density=(P_dust/D)^2'
            dependencies=[denominator,name]
        elif field.startswith(('E','M','A')):
            owner='matter.electromagnetic'
            purpose='Shared-metric electromagnetic field/potential numerator '+field
            dependencies=[denominator,name]
        else:
            owner='matter.charged_scalar'
            purpose='Shared-metric scalar, momentum or covariant-gradient numerator '+field
            dependencies=[denominator,name]
        rows.append({'index':index,'name':name,'owner':owner,'purpose':purpose,
                     'label':program.tensor.labels[index],
                     'readout_dependencies':dependencies,
                     'retained_registers':['a','b','r']})
    assert len(rows)==44 and all(row['readout_dependencies'] for row in rows)
    return rows


# This source string is run by python -I, with exactly the requested runtime
# source inserted. It imports no experiment or parent-checkout module.
ISOLATED_RUNNER = r'''
import gzip
import hashlib
import json
from pathlib import Path
import sys
runtime_source, input_file, expected_file, output, pin = map(str,sys.argv[1:])
runtime_source=Path(runtime_source).resolve()
sys.path.insert(0,str(runtime_source))
from universe24.core import Engine
from universe24.core import exact_json
from universe24.system.bundle import create_bundle, read_json, state_from_data, tensor_from_data
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
import universe24.core.engine as imported_engine
import universe24.system.bundle as imported_bundle
import universe24.system.runtime as imported_runtime
for module in (imported_engine,imported_bundle,imported_runtime):
    assert Path(module.__file__).resolve().is_relative_to(runtime_source)
assert not any(name.startswith('experiments') for name in sys.modules)
data=read_json(input_file)
expected=read_json(expected_file)
tensor=tensor_from_data(data['tensor']);seed=state_from_data(data['seed'])
bundle=create_bundle(tensor,seed,channels=data['channels'],
                     protocol=default_protocol(),model=data['model'])
assert bundle.tensor.G==44 and bundle.seed.to_dict()==expected[0]
report=run_bundle(bundle,output,data['steps'])
assert verify_run(output)==report
observed=[]
with gzip.open(Path(output)/'full_trace.jsonl.gz','rt',encoding='utf-8') as stream:
    for index,line in enumerate(stream):
        transition=exact_json.loads(line)
        assert transition['before']==expected[index]
        assert transition['after']==expected[index+1]
        observed.append(transition['after'])
assert len(observed)==data['steps']
assert all(report['acceptance_gates'][gate]['status']=='not_tested' for gate in 'CDEF')
result={'pinned_main_commit':pin,'runtime_import_source':str(runtime_source),
        'isolated_python':True,'proposal_modules_imported_into_runtime':False,
        'api':'create_bundle -> run_bundle -> verify_run',
        'source_engine_and_saved_runtime_complete_states_equal':True,
        'transitions_compared':len(observed),'all_retained_arrays_compared':['a','b','r'],
        'channels':44,'retained_integers_per_node':132,
        'physical_gates_unchanged':True,'runtime_validation':report}
print(json.dumps(result,sort_keys=True))
'''


def run(runtime_source, out, *, steps=4):
    runtime_source=Path(runtime_source).resolve()
    if type(steps) is not int or not 1<=steps<=4:
        raise ValueError('Validation adapter uses one to four updates; longer physics runs are separate')
    if (runtime_source/'experiments').exists():
        raise ValueError('Use the source-only validation layout, without legacy experiment runtimes')
    required=('AGENTS.md','universe24/core/engine.py','universe24/core/exact_json.py',
              'universe24/system/bundle.py','universe24/system/runtime.py')
    for name in required:
        if not (runtime_source/name).is_file():raise ValueError(f'Missing runtime source {name}')
    for name, expected_sha in EXPECTED_RUNTIME_BLOBS.items():
        data=(runtime_source/name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=expected_sha:raise ValueError(f'Runtime differs from pinned main: {name}')
    runtime_hashes={name:hashlib.sha256((runtime_source/name).read_bytes()).hexdigest()
                    for name in EXPECTED_RUNTIME_BLOBS}
    runtime_hashes['AGENTS.md']=hashlib.sha256((runtime_source/'AGENTS.md').read_bytes()).hexdigest()
    h=F(1,16)
    program=projective.compile_projective(NAMES,BUILDER,dt=h,dx=1,degree=3)
    seed=prepared(program,256,protected=True)
    engine=Engine(program.tensor);state=seed
    expected=[seed.to_dict()]
    for _ in range(steps):
        state=engine.step(state);expected.append(state.to_dict())
    assert engine.rewind(state,steps).same_as(seed)
    model={'id':'team48.projective-positive-source-research',
           'version':'proposal-runtime-handoff-1',
           'domain':'Homogeneous massless charged-scalar sector plus normal dust; constrained initial slice, finite temporal control only',
           'status':'research proposal; no accepted production physical model',
           'physical_step':str(h),'coordinate_convention':'synchronous lapse1, shift0',
           'shared_metric':'upper-triangular B; diagonal=(Pp^2+Pq^2)/D^2; gamma_inverse=B.T*B',
           'metric_readout_dependencies':[program.tensor.names[0]]+
               [f'projective.{name}' for name in NAMES if name.startswith(('B','diag_'))],
           'retained_allocation':{'total_channels':44,'unallocated_below_48':4,
                                  'hidden_state':0,'apparatus_channels':0},
           'memory_boundary':'D_old0, P_old0 except each diagonal q_old1; this is not an earlier physical metric',
           'physical_acceptance':{gate:'not_tested' for gate in 'CDEF'},
           'arithmetic_clicks_are_operational_detectors':False}
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    attempt=Path(tempfile.mkdtemp(prefix='handoff-',dir=out))
    input_file=attempt/'research_inputs.json';expected_file=attempt/'source_expected_states.json'
    payload={'tensor':program.tensor.to_dict(),'seed':seed.to_dict(),
             'channels':channel_manifest(program),'model':model,'steps':steps}
    input_file.write_text(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n')
    expected_file.write_text(json.dumps(expected,sort_keys=True,separators=(',',':'))+'\n')
    completed=subprocess.run([sys.executable,'-I','-c',ISOLATED_RUNNER,
                              str(runtime_source),str(input_file.resolve()),
                              str(expected_file.resolve()),str((attempt/'runtime_run').resolve()),MAIN_PIN],
                             cwd=attempt,check=True,capture_output=True,text=True,timeout=180)
    report=json.loads(completed.stdout)
    report.update({'proposal_tensor_hash':program.tensor.fingerprint,
                   'proposal_seed_sha256':hashlib.sha256(json.dumps(seed.to_dict(),sort_keys=True,
                    separators=(',',':')).encode()).hexdigest(),
                   'runtime_source_sha256':runtime_hashes,
                   'proposal_source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                     for name in ('validation/geometry/team48/refinement_runtime_adapter.py',
                                  'validation/geometry/team48/refinement_integer_projective.py',
                                  'validation/geometry/team48/temporal_repair_projective.py')},
                   'evidence_directory':str(attempt.resolve()),
                   'limitations':['This is runtime compatibility and complete-state equality, not physical acceptance.',
                                  'All proposal channels retain their existing audit labels; no operational detector is added.',
                                  'The source pin is the externally reviewed materialization identifier; exact local runtime hashes are recorded.']})
    (attempt/'adapter_report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'latest_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-source',required=True,type=Path)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/team48/refinement_runtime')
    parser.add_argument('--steps',type=int,default=4)
    args=parser.parse_args()
    result=run(args.runtime_source,args.out,steps=args.steps)
    print(json.dumps({key:result[key] for key in ('pinned_main_commit','channels',
          'transitions_compared','source_engine_and_saved_runtime_complete_states_equal',
          'physical_gates_unchanged','evidence_directory')},indent=2))
