"""Correct only the passive product-pair variable collision in frozen captures."""
from __future__ import annotations
import argparse,gzip,hashlib,json,shutil,time
from pathlib import Path
from research.experiments.run import recorded_states
from research.staged_blocks import interactions as shared
from . import structure

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(source,output):
    source=Path(source);output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'observations').mkdir()
    original=json.loads((source/'result.json').read_text());p=json.loads((source/'protocol.json').read_text());inputs={row['record']:sha(source/row['record']) for row in original['cases']}
    registration={'scope':'Passive correction only; native captures immutable.','source_result':str(source/'result.json'),'source_result_sha256':sha(source/'result.json'),'native_record_sha256':inputs,'protocol_sha256':sha(source/'protocol.json'),'observer_sha256':sha(Path(structure.__file__)),'reanalysis_sha256':sha(Path(__file__))}
    shared.write_json(output/'registration.json',registration);shutil.copyfile(source/'protocol.json',output/'protocol.json')
    started_cpu,started_wall=time.process_time(),time.monotonic();groups={};ledger=[];changed=[];frames=0
    for original_case in original['cases']:
        path=source/original_case['record'];row=json.loads(gzip.decompress(path.read_bytes()));states=recorded_states(row['experiment']);frames+=len(states)
        obs=structure.observe(row['case'],states,p);differences=[k for k in set(obs)|set(row['observations']) if obs.get(k)!=row['observations'].get(k)]
        if not set(differences)<={'separated_product_pairs','separated_products_without_parent'}:raise AssertionError(('Unexpected observer change',row['spec']['id'],differences))
        if differences:changed.append({'id':row['spec']['id'],'fields':sorted(differences),'old_product_count':len(row['observations']['isolated_product_templates']),'new_product_count':len(obs['isolated_product_templates'])})
        row['observations']=obs;groups.setdefault(row['case']['id'],[]).append(row)
        observation_path=output/'observations'/(row['spec']['id']+'.json.gz');observation_path.write_bytes(gzip.compress(shared.canonical({'case':row['case'],'native_record':str(path),'native_record_sha256':inputs[original_case['record']],'observations':obs}).encode(),mtime=0))
        ledger.append({'id':row['spec']['id'],'native_record':str(path),'native_record_sha256':inputs[original_case['record']],'observations':str(observation_path.relative_to(output)),'observations_sha256':sha(observation_path)})
    assessments=[]
    for rows in groups.values():assessments.append(structure.assess(rows,p) if len(rows)==4 else {'pristine':True,'incoming_valid':rows[0]['observations']['incoming_valid']})
    assert inputs=={path:sha(source/path) for path in inputs}
    assert registration['source_result_sha256']==sha(source/'result.json')
    assert registration['observer_sha256']==sha(Path(structure.__file__))
    shutil.copyfile(source/'experiments.json',output/'experiments.json')
    result={'status':'completed','scope':'Passive corrected observations; zero new physics trajectories. Original false assessments preserved.','completed_cases':len(ledger),'complete_states_reanalyzed':frames,'new_trajectories':0,'native_records_unchanged':True,'protocol_sha256':registration['protocol_sha256'],'cases':ledger,'groups':assessments,'corrected_fields':changed,'cpu_seconds':time.process_time()-started_cpu,'wall_seconds':time.monotonic()-started_wall,'presenter_native_bundle_unchanged':sha(source/'experiments.json')==sha(output/'experiments.json'),'all_full_rewinds_from_original_capture':original['all_full_rewinds']}
    shared.write_json(output/'result.json',result);print(shared.canonical({k:result[k] for k in ('status','completed_cases','complete_states_reanalyzed','native_records_unchanged','cpu_seconds')}),flush=True);return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
if __name__=='__main__':main()
