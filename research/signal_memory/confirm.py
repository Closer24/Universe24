"""Prospective confirmation of first record window, preserving v1 failure."""
import hashlib,json,time,platform
from pathlib import Path
from run import ROOT,run_case,Engine,Coupling

def main():
    raw=(ROOT/'protocol_v2.json').read_bytes();p=json.loads(raw);e=Engine(Coupling((1,1,1)));start=time.process_time();wall=time.monotonic();results=[]
    forward_steps=sum(case['steps'] for case in p['cases'])
    if forward_steps>p['budget']['max_forward_steps']:raise RuntimeError('Forward-step budget exceeded')
    for case in p['cases']:
        r=run_case(case,e,start,wall);trace=json.loads((ROOT/'results'/case['id']/'trace.json').read_text());j=case['j'];end=2*(case['N']+1)-j
        r['first_window_exact']=all(row['memory']==int(j<=row['t']<end) for row in trace if row['t']<=end)
        r['record_window']=[j,end];r['record_ticks']=end-j
        r['pass']=r['first_window_exact'] and end-j>=32 and r['clock_exact'] and r['one_step_inverse'] and r['multi_step_inverse'] and all(r['first_activation'].get(k)==k for k in range(1,case['N']+1))
        results.append(r)
    out={'protocol_id':p['protocol_id'],'protocol_sha256':hashlib.sha256(raw).hexdigest(),'source_commit':p['source_commit'],'coupling_fingerprint':e.coupling.fingerprint,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'shared_runner_sha256':hashlib.sha256((ROOT/'run.py').read_bytes()).hexdigest(),'python':platform.python_version(),'cpu_seconds':time.process_time()-start,'wall_seconds':time.monotonic()-wall,'forward_steps':forward_steps,'one_step_inverse_calls':forward_steps,'trajectory_inverse_calls':forward_steps,'results':results,'size_trace_exact':results[0]['normalized_state_hashes']==results[1]['normalized_state_hashes'],'all_pass':all(r['pass'] for r in results) and results[0]['normalized_state_hashes']==results[1]['normalized_state_hashes']}
    (ROOT/'results_v2.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
if __name__=='__main__':main()
