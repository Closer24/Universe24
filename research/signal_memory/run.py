"""Reproduce a prepared finite guide record; no dynamical modifications."""
from __future__ import annotations
import hashlib,json,platform,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from universe24 import Channel,Coupling,Cube,Engine,State
from universe24.experiments.config import checkpoint_data
ROOT=Path(__file__).resolve().parent

def memory(state,position):
    return int(state.at((*position,0)).r==0 and state.at((*position,14)).r==4)

def prepare(case):
    n,L=case['N'],case['L']; origin=(L//2-n//2,L//2,L//2)
    cells={}
    if case['control']!='source_only':
        for j in range(1,n+1):
            if case['control']=='gap' and j==3:continue
            x,y,z=origin; cells[(x+j,y,z,0)]=Channel(0,0,4);cells[(x+j,y,z,14)]=Channel(0,0,0)
    if case['control']!='no_source':
        x,y,z=origin;cells[(x,y,z,0)]=Channel(0,1,2);cells[(x,y,z,14)]=Channel(0,-1,2)
    if case['control']=='r_plus_one':
        x,y,z=origin;cells[(x+2,y,z,0)]=Channel(0,0,5)
    return State(Cube(L),cells=cells),origin

def normalized(state,origin):
    return sorted([[a[0]-origin[0],a[1]-origin[1],a[2]-origin[2],a[3],*s] for a,s in state.cells.items()])

def run_case(case,engine,budget_start,budget_wall_start=None):
    if budget_wall_start is None:budget_wall_start=time.monotonic()
    def check_budget():
        if time.process_time()-budget_start>120:raise RuntimeError('CPU budget exceeded')
        if time.monotonic()-budget_wall_start>300:raise RuntimeError('Wall budget exceeded')
    initial,origin=prepare(case);s=initial;target=(origin[0]+case['j'],origin[1],origin[2]);trace=[];hashes=[];first={};inverse_ok=True;max_cells=0
    out=ROOT/'results'/case['id'];out.mkdir(parents=True,exist_ok=True)
    (out/'initial.json').write_text(json.dumps(checkpoint_data(initial,engine,0),indent=2)+'\n')
    for t in range(case['steps']+1):
        check_budget()
        if len(s.cells)>100000:raise RuntimeError('Cell budget exceeded')
        max_cells=max(max_cells,len(s.cells))
        for j in range(1,case['N']+1):
            if s.at((origin[0]+j,origin[1],origin[2],0)).b and j not in first:first[j]=t
        trace.append({'t':t,'g0':list(s.at((*target,0))),'g14':list(s.at((*target,14))),'memory':memory(s,target)})
        hashes.append(hashlib.sha256(json.dumps(normalized(s,origin),separators=(',',':')).encode()).hexdigest())
        if t<case['steps']:
            new=engine.advance(s);inverse_ok &= engine.rewind(new)==s;s=new
    (out/'final.json').write_text(json.dumps(checkpoint_data(s,engine,case['steps']),indent=2)+'\n')
    (out/'trace.json').write_text(json.dumps(trace,indent=2)+'\n')
    clicks=[row['t'] for a,row in zip(trace,trace[1:]) if a['memory']==0 and row['memory']==1]
    j=case['j'];end=2*(case['N']+1)-j
    clock=[(0,1),(1,0),(0,-1),(-1,0)]
    record_exact=all(row['memory']==int(j<=row['t']<end) for row in trace)
    clock_exact=all(tuple(row['g0'][:2])==clock[(row['t']-j)%4] and tuple(row['g14'][:2])==tuple(-q for q in clock[(row['t']-j)%4]) for row in trace if j<=row['t']<end)
    reconstructed=s
    for _ in range(case['steps']):
        check_budget();reconstructed=engine.rewind(reconstructed)
    return {'case':case,'first_activation':first,'clicks':clicks,'record_exact':record_exact,'clock_exact':clock_exact,'predicted_record_ticks':end-j,'observed_record_ticks':sum(r['memory'] for r in trace),'one_step_inverse':inverse_ok,'multi_step_inverse':reconstructed==initial,'max_explicit_cells':max_cells,'normalized_state_hashes':hashes}

def main():
    raw=(ROOT/'protocol.json').read_bytes();protocol=json.loads(raw);engine=Engine(Coupling((1,1,1)));start=time.process_time();wall=time.monotonic()
    results=[]
    forward_steps=sum(case['steps'] for case in protocol['cases'])
    if forward_steps>protocol['budget']['max_forward_steps']:raise RuntimeError('Forward-step budget exceeded')
    for case in protocol['cases']:
        results.append(run_case(case,engine,start,wall));print(case['id'],results[-1]['clicks'],results[-1]['record_exact'],results[-1]['clock_exact'],flush=True)
    summary={'protocol_id':protocol['protocol_id'],'protocol_sha256':hashlib.sha256(raw).hexdigest(),'source_commit':protocol['source_commit'],'coupling_fingerprint':engine.coupling.fingerprint,'python':platform.python_version(),'random_seed':None,'preparation_generator':'run.py:prepare','runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'forward_steps':forward_steps,'one_step_inverse_calls':forward_steps,'trajectory_inverse_calls':forward_steps,'cpu_seconds':time.process_time()-start,'wall_seconds':time.monotonic()-wall,'results':results}
    summary['size_trace_exact']=results[0]['normalized_state_hashes']==results[1]['normalized_state_hashes']
    summary['all_inverse']=all(r['one_step_inverse'] and r['multi_step_inverse'] for r in results)
    summary['ideal_cases_pass']=all(r['record_exact'] and r['clock_exact'] and all(r['first_activation'].get(j)==j for j in range(1,r['case']['N']+1)) for r in results[:3])
    summary['negative_controls_pass']=all(not r['clicks'] for r in results[3:6])
    (ROOT/'results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
if __name__=='__main__':main()
