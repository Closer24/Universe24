"""Bounded, protocol-first search for two independent arrival records.

This is a search over t=0 preparations, never an optimizer acting on evolution.
The finite search can fail without implying a mathematical impossibility.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

from universe24.experiments.config import checkpoint_data
from .preparation import candidate_cases, prepare
from .run import canonical, digest, run_case, waiting_verdict, write_json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
MASKS=((False,False),(True,False),(False,True),(True,True))


def source_hashes(extra_paths=()):
    paths=sorted((ROOT/'universe24').rglob('*.py'))+[
        HERE/'preparation.py',HERE/'run.py',HERE/'search.py',HERE/'protocol.json']+list(extra_paths)
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def compact(result):
    return {key:result[key] for key in ('id','source_mask','initial_sha256','final_sha256',
        'record_event_times','arithmetic_events','entire_board_stationary',
        'initial_boundary_margin','minimum_boundary_margin','max_stored_channels',
        'all_one_step_inverses','complete_rewind')} | {
        'detector_trace':[[r['step'],*r['memory'],*r['next_input']]
                          for r in result['trace']]}


def group_verdict(case, runs):
    windows=case['arrival_windows']; checks={}
    for mask,result in runs.items():
        active=[window for enabled,window in zip(mask,windows) if enabled]
        checks[str(mask)]=waiting_verdict(result,active)
    both=runs[(True,True)]
    counterfactual=[]
    for index,t in enumerate(both['record_event_times'][:2]):
        missing=(False,True) if index==0 else (True,False)
        counterfactual.append(both['trace'][t-1]['next_input']!=runs[missing]['trace'][t-1]['next_input'])
    independent=len(counterfactual)==2 and all(counterfactual)
    stationary=runs[(False,False)]['entire_board_stationary']
    inverses=all(r['all_one_step_inverses'] and r['complete_rewind'] for r in runs.values())
    records=stationary and independent and inverses and all(c['record_milestone_passed'] for c in checks.values())
    guarded=stationary and independent and inverses and all(c['guarded_click_milestone_passed'] for c in checks.values())
    return {'controls':checks,'source_counterfactual_inputs_differ':counterfactual,
            'no_source_full_board_stationary':stationary,'full_inverse_audits':inverses,
            'record_only_criteria_passed':records,'guarded_click_criteria_passed':guarded}


def family_manifest(protocol, protocol_path=HERE/'protocol.json'):
    registered=protocol['search_family']
    family={'side':registered['side'],'extent':40,'steps':registered['horizon'],
            'body_signs':registered['body_signs'],
            'geometries':[s.split(':',1)[0] for s in registered['source_orientations']],
            'distance_pairs':registered['training_distance_pairs'],
            'target_remainder_pairs':registered['detector_remainder_order'],
            'source_phases':registered['source_phase_pairs']}
    if protocol['protocol_id']=='U24-SIGNAL-CLOCK-ENDPOINT-v1':
        family.update(guide_mode='between_sources',id_prefix='endpoint')
    cases=list(candidate_cases(family))
    if len(cases)!=registered['candidate_count']:
        raise ValueError('Candidate enumeration disagrees with frozen count')
    return {'format':'universe24-signal-clock-candidates-v1',
        'protocol_sha256':hashlib.sha256(Path(protocol_path).read_bytes()).hexdigest(),
        'family':family,'candidate_count':len(cases),'candidates':cases,
        'seed':None,'enumeration':'Nested deterministic candidate_cases order; no random sampling.',
        'retention_selection':'First full guarded pass, otherwise first candidate in frozen order. No observer criterion is changed.',
        'cache_policy':'Reuse only byte-identical complete initial checkpoint and equal horizon; source-mask labels do not affect evolution.'}


def search(output,protocol_path=HERE/'protocol.json'):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    protocol_path=Path(protocol_path).resolve()
    protocol=json.loads(protocol_path.read_text())
    if protocol['status']!='frozen_before_search':
        raise ValueError('Protocol is not frozen')
    manifest=family_manifest(protocol,protocol_path)
    write_json(output/'candidate_manifest.json',manifest)
    write_json(output/'protocol.json',protocol)
    hashes=source_hashes([protocol_path]);budget=protocol['budgets']
    started=time.process_time();wall=time.monotonic();deadline=started+budget['search_cpu_seconds']
    cache={}; completed=[]; failure=None; cache_hits=0; candidate=None
    for case in manifest['candidates']:
        runs={}
        try:
            for mask in MASKS:
                if time.monotonic()-wall>budget['search_wall_seconds']:
                    raise TimeoutError('Declared search wall budget exhausted')
                engine,initial,_=prepare(case,mask)
                key=(digest(checkpoint_data(initial,engine,0)),case['steps'])
                if key in cache:
                    result=cache[key];cache_hits+=1
                else:
                    result=run_case(case,mask,deadline_cpu=deadline,
                        max_cells=budget['maximum_stored_channels_per_state'],audit=True)
                    cache[key]=result
                runs[mask]=result
            verdict=group_verdict(case,runs)
            completed.append({'case':case,'verdict':verdict,
                'runs':[compact(runs[m]) for m in MASKS]})
            if verdict['guarded_click_criteria_passed'] and candidate is None:
                candidate=case
                if protocol['search_family']['stop_on_first_full_success']:
                    break
            if len(completed)%16==0:
                print(canonical({'completed':len(completed),'total':len(manifest['candidates']),
                    'guarded_passes':sum(c['verdict']['guarded_click_criteria_passed'] for c in completed),
                    'cpu_seconds':round(time.process_time()-started,3)}),flush=True)
        except (TimeoutError,MemoryError) as exc:
            failure={'candidate_id':case['id'],'type':type(exc).__name__,'message':str(exc),
                     'completed_source_masks':[list(m) for m in runs]}
            break
    summary={'execution_status':'completed' if failure is None else 'inconclusive',
        'candidates_total':len(manifest['candidates']),'candidates_completed':len(completed),
        'guarded_click_candidates':sum(c['verdict']['guarded_click_criteria_passed'] for c in completed),
        'record_only_candidates':sum(c['verdict']['record_only_criteria_passed'] for c in completed),
        'unique_audited_trajectories':len(cache),'cache_hits':cache_hits,
        'audited_forward_steps':sum(r['preparation']['steps'] for r in cache.values()),
        'all_executed_full_inverses':all(r['all_one_step_inverses'] and r['complete_rewind'] for r in cache.values()),
        'failure':failure,'cpu_seconds':time.process_time()-started,'wall_seconds':time.monotonic()-wall,
        'physical_validation':False,'search_is_not_impossibility_proof':True,
        'source_unchanged':hashes==source_hashes([protocol_path])}
    write_json(output/'search_results.json',{'summary':summary,'candidates':completed})
    selected=candidate or (completed[0]['case'] if completed else None)
    write_json(output/'selected_preparation.json',{'selection_reason':'first_guarded_pass' if candidate else 'first_frozen_candidate_negative_evidence',
        'case':selected,'training_guarded_pass':candidate is not None})
    write_json(output/'manifest.json',{'protocol_sha256':manifest['protocol_sha256'],
        'candidate_manifest_sha256':hashlib.sha256((output/'candidate_manifest.json').read_bytes()).hexdigest(),
        'source_sha256':hashes,'checkout_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'working_tree_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),
        'python':platform.python_version(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        'seed':None,'forward_primitive':'Engine.advance only','no_intervention':True})
    print(canonical(summary),flush=True)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--protocol',type=Path,default=HERE/'protocol.json')
    args=parser.parse_args()
    summary=search(args.output,args.protocol)
    return 0 if summary['execution_status']=='completed' and summary['all_executed_full_inverses'] else 2


if __name__=='__main__':
    raise SystemExit(main())
