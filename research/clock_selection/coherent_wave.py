"""Full-engine baseline coherent modes with exact passive linear-error checks."""
from __future__ import annotations
import argparse
import gc
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import shutil
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle
from research.staged_blocks import interactions as base
from .provenance import freeze_sources, verify_sources
from .recurrence import source_paths as common_source_paths

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/"coherent_wave_protocol.json"


def arithmetic():
    import mpmath as m
    if m.__version__!="1.3.0":raise ValueError("Preparation requires pinned mpmath1.3.0")
    if m.libmp.BACKEND!="python":raise ValueError("Registered interval oracle uses the Python backend")
    m.iv.dps=80;m.mp.dps=100
    return m


def cases(p):
    for side,n,amplitude in itertools.product(p["sides"],p["wavevectors"],p["amplitudes"]):
        yield {"id":f"coherent-L{side}-n{''.join(map(str,n))}-N{amplitude}","side":side,"n":n,"amplitude":amplitude}


def interval_profile(case):
    m=arithmetic();iv=m.iv;L=case["side"];N=case["amplitude"]
    gamma=sum(iv.cos(2*iv.pi*v/L) for v in case["n"])/3
    sine=iv.sqrt(1-gamma**2);profiles=[];witnesses=[];targets=[]
    def rounded(value):
        lo,hi=m.mp.mpf(value.a),m.mp.mpf(value.b)
        a,b=int(m.floor(lo+m.mpf("0.5"))),int(m.floor(hi+m.mpf("0.5")))
        if a!=b:raise ValueError("Ambiguous interval nearest-integer preparation")
        return a,[m.nstr(lo,100),m.nstr(hi,100)]
    for phase in range(L):
        phi=2*iv.pi*phase/L
        target_b=iv.cos(phi);target_a=target_b*gamma-iv.sin(phi)*sine
        a,ai=rounded(N*target_a);b,bi=rounded(N*target_b)
        profiles.append((a,b,2));targets.append((target_a,target_b))
        witnesses.append({"phase":phase,"a":a,"b":b,"a_scaled_interval":ai,"b_scaled_interval":bi})
    return profiles,witnesses,targets,gamma


def case_spec(case,p):
    profile,witnesses,_,gamma=interval_profile(case);L=case["side"];n=case["n"]
    cells=[[x,y,z,g,*profile[(n[0]*x+n[1]*y+n[2]*z)%L]]
           for x,y,z in itertools.product(range(L),repeat=3) for g in range(48)]
    spec={"format":"universe24-assembly-experiment-v1","id":case["id"],
        "title":f"Coherent cube wave: n={tuple(n)}, L={L}, N={case['amplitude']}",
        "description":"All48 channels evolve through the full unchanged engine. Dense periodic mode; not a localized photon or a new rule.",
        "question":p["question"],"board":{"side":L,"body_signs":[1,1,1],"background":[0,0,2]},
        "components":[{"name":"coherent-field","recipe":"Patch","at":[0,0,0],"params":{"kind":"coherent-initial-mode","cells":cells}}],
        "steps":p["horizon"],"detectors":[],"seed":None,
        "view":{"position":[L//2]*3,"channel":0},
        "budget":{"max_frames":p["budget"]["max_frames_per_record"],"max_cells":p["budget"]["max_cells_per_record"],
                  "max_bytes":p["budget"]["max_decoded_record_bytes"],"max_seconds":p["budget"]["max_seconds_per_record"]},
        "provenance":{"protocol_canonical_sha256":base.digest(p),"initial_only":True,"coherent_shortcut_used_for_evolution":False}}
    m=arithmetic()
    certificate={"mpmath_version":m.__version__,"backend":m.libmp.BACKEND,"interval_decimal_digits":80,
        "endpoint_decimal_digits":100,"rounding":"floor(value+1/2), same at both interval endpoints",
        "phase_classes":witnesses,"gamma_interval":[m.nstr(m.mp.mpf(gamma.a),100),m.nstr(m.mp.mpf(gamma.b),100)]}
    return spec,certificate


def adjacency(field,L):
    return {x:sum(field[tuple((x[j]+(delta if j==axis else 0))%L for j in range(3))]
                  for axis in range(3) for delta in (-1,1)) for x in field}


def observe(case,p,states):
    m=arithmetic();iv=m.iv;L=case["side"];N=case["amplitude"];V=L**3;n=case["n"]
    sites=list(itertools.product(range(L),repeat=3));_,_,initial_targets,gamma=interval_profile(case)
    target_old=[a for a,b in initial_targets];target=[b for a,b in initial_targets]
    old_field={x:states[0].at((*x,0)).a for x in sites};w={x:states[0].at((*x,0)).b for x in sites}
    rows=[];events=[];qtrace=[];all_coherent=True;all_equation=True;all_parity=True
    prior_w=None
    for t,state in enumerate(states):
        values={x:state.at((*x,0)) for x in sites}
        coherent=all(state.at((*x,g))==values[x] for x in sites for g in range(48))
        all_coherent &= coherent;all_parity &= all(v.r%2==0 for v in state.cells.values())
        qtrace.append(sum(6*(v.b-v.a)+v.r-2 for v in state.cells.values()))
        scale=3**t;sum_squared=sum((scale*values[x].b-w[x])**2 for x in sites)
        exact_bound=0 if t==0 else V*t*t*(t+1)*(t+1)*3**(2*t-2)
        residuals=[abs(iv.mpf(values[x].b)/N-target[(n[0]*x[0]+n[1]*x[1]+n[2]*x[2])%L])**2 for x in sites]
        ideal_rms=iv.sqrt(sum(residuals)/V);ideal_upper=m.mp.mpf(ideal_rms.b)
        envelope=m.mpf(2*t+1)/(2*N)+m.mpf(t*(t+1))/(3*N);slack=m.mpf("1e-50")
        equation=True
        if t:
            previous=states[t-1];previous_b={x:previous.at((*x,0)).b for x in sites};sums=adjacency(previous_b,L)
            for x in sites:
                before,after=previous.at((*x,0)),values[x]
                ell=after.b+before.a
                equation &= 6*ell==2*sums[x]+before.r-after.r
                if coherent and rows[-1]["all48_coherent"] and ell and before!=after:
                    kind=((after.r-before.r)//2)%3
                    events.extend([[t,*x,g,kind,str(ell)] for g in range(48)])
            if not (coherent and rows[-1]["all48_coherent"]):
                # Failed coherence must still retain every actual channel event.
                for x in sites:
                    for g in range(48):
                        before,after=previous.at((*x,g)),state.at((*x,g))
                        ell=after.b+before.a
                        if ell and before!=after:
                            events.append([t,*x,g,((after.r-before.r)//2)%3,str(ell)])
        all_equation &= equation
        rows.append({"step":t,"all48_coherent":coherent,"exact_equation":equation,
            "rounded_initial_error_squared_numerator":str(sum_squared),"exact_bound_numerator":str(exact_bound),
            "exact_rounded_initial_bound_pass":sum_squared<=exact_bound,
            "rounded_initial_RMS":math.sqrt(sum_squared/V)/(N*scale),
            "rounded_initial_envelope":t*(t+1)/(3*N),
            "ideal_mode_RMS_interval":[m.nstr(m.mp.mpf(ideal_rms.a),90),m.nstr(ideal_upper,90)],
            "ideal_mode_envelope":m.nstr(envelope,90),"fixed_numerical_slack":"1e-50",
            "ideal_mode_bound_pass":ideal_upper<=envelope+slack})
        if t+1<len(states):
            aw=adjacency(w,L)
            next_w={x:aw[x]-3*old_field[x] for x in sites} if t==0 else {x:aw[x]-9*prior_w[x] for x in sites}
            prior_w,w=w,next_w
            target_old,target=target,[2*gamma*target[i]-target_old[i] for i in range(L)]
    return {"frames":rows,"all48_coherent":all_coherent,"exact_reduced_equation":all_equation,
        "remainder_parity_preserved":all_parity,"all_rounded_initial_bounds":all(r["exact_rounded_initial_bound_pass"] for r in rows),
        "all_ideal_mode_bounds":all(r["ideal_mode_bound_pass"] for r in rows),"Q_trace":[str(q) for q in qtrace],
        "Q_conserved":len(set(qtrace))==1,"raw_C_row_format":["step","x","y","z","channel","kind","ell"],
        "all_C":events,"all_C_counts":{str(k):sum(e[5]==k for e in events) for k in range(3)}}


def dependency_snapshot(output):
    m=arithmetic();source=Path(m.__file__).resolve().parent;items={}
    for file in sorted(source.rglob('*.py')):
        relative=file.relative_to(source);target=output/"mpmath"/relative;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(file,target);items[str(relative)]=hashlib.sha256(file.read_bytes()).hexdigest()
    result={"package":"mpmath","version":m.__version__,"backend":m.libmp.BACKEND,"source_sha256":items}
    base.write_json(output/"manifest.json",result);return result


def run(output,protocol_path=PROTOCOL):
    raw=Path(protocol_path).read_bytes();p=json.loads(raw);planned=list(cases(p))
    if len(planned)!=p["budget"]["registered_cases"]:raise ValueError("Case-count mismatch")
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/"records").mkdir();(output/"native").mkdir()
    (output/"protocol.json").write_bytes(raw)
    dependency=dependency_snapshot(output/"dependency_provenance")
    paths=common_source_paths(HERE/"recurrence_protocol.json")+[Path(__file__),Path(protocol_path)]
    snapshot=freeze_sources(output/"source_provenance",[str(x.relative_to(ROOT)) for x in paths],
        metadata={"protocol_sha256":hashlib.sha256(raw).hexdigest(),"cases":planned,"seed":None,"budget":p["budget"],"dependency":dependency})
    base.write_json(output/"registration.json",{"format":"universe24-coherent-wave-registration-v1","cases":planned,
        "protocol_sha256":hashlib.sha256(raw).hexdigest(),"source_sha256":snapshot["source_sha256"],"registered_before_capture":True})
    cpu,wall=time.process_time(),time.monotonic();ledger=[];reason=None
    for case in planned:
        if time.process_time()-cpu>=p["budget"]["max_cpu_seconds"]:reason="cpu_budget";break
        if time.monotonic()-wall>=p["budget"]["max_wall_seconds"]:reason="wall_budget";break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p["budget"]["max_output_bytes"]:reason="byte_budget";break
        spec,rounding=case_spec(case,p)
        try:captured=run_experiment(spec)
        except (TimeoutError,ValueError) as exc:
            reason="capture_incomplete";base.write_json(output/"capture_failure.json",{"case":case,"error":str(exc),"type":type(exc).__name__,"spec":spec});break
        states=recorded_states(captured["experiment"])
        try:obs=observe(case,p,states)
        except (ValueError,ArithmeticError) as exc:
            reason="observation_incomplete"
            failed={"case":case,"spec":spec,"rounding_certificate":rounding,"assembly":captured["assembly"],
                "experiment":captured["experiment"],"observation_failure":{"error":str(exc),"type":type(exc).__name__},
                "scientific_acceptance":False,"native_capture_complete":True}
            (output/(case["id"]+"-observation-failure.json.gz")).write_bytes(gzip.compress(base.canonical(failed).encode(),mtime=0))
            base.write_json(output/"observation_failure.json",{"case":case,"error":str(exc),"type":type(exc).__name__,
                "complete_native_record":case["id"]+"-observation-failure.json.gz"})
            break
        row={"format":"universe24-coherent-wave-record-v1","case":case,"spec":spec,"rounding_certificate":rounding,
            "assembly":captured["assembly"],"experiment":captured["experiment"],"observations":obs}
        encoded=base.canonical(row).encode()
        if len(encoded)>p["budget"]["max_decoded_record_bytes"]:raise ValueError("Complete record exceeds declared decoded byte cap")
        zipped=gzip.compress(encoded,mtime=0);relative="records/"+case["id"]+".json.gz";(output/relative).write_bytes(zipped)
        accepted=all(obs[k] for k in ("all48_coherent","exact_reduced_equation","remainder_parity_preserved","all_rounded_initial_bounds","all_ideal_mode_bounds","Q_conserved")) and captured["experiment"]["provenance"]["full_rewind_equal"]
        item={"id":case["id"],"case":case,"record":relative,"record_sha256":hashlib.sha256(encoded).hexdigest(),
            "record_gzip_sha256":hashlib.sha256(zipped).hexdigest(),"frames":len(states),"transitions":len(states)-1,
            "accepted_comparison":accepted,"full_state_inverse":captured["experiment"]["provenance"]["full_rewind_equal"],
            "complete_sparse_rows":sum(len(f["cells"]) for f in captured["experiment"]["frames"]),"all_C_counts":obs["all_C_counts"],
            "maximum_observed_rounded_initial_RMS":max(f["rounded_initial_RMS"] for f in obs["frames"])}
        if case["side"]==9 and case["amplitude"]==100000:
            native=base.canonical(bundle([captured["experiment"]],title="Complete coherent cube wave")).encode()+b"\n"
            native_path="native/"+case["id"]+".json";(output/native_path).write_bytes(native)
            item.update({"native":native_path,"native_sha256":hashlib.sha256(native).hexdigest()})
            del native
        ledger.append(item);base.write_json(output/"progress.json",{"completed":len(ledger),"registered":len(planned),"last_id":case["id"]})
        print(base.canonical({"completed":len(ledger),"registered":len(planned),"id":case["id"],"accepted":accepted}),flush=True)
        del states,obs,row,encoded,zipped,captured,spec;gc.collect()
    verification=verify_sources(output/"source_provenance");base.write_json(output/"source_verification.json",verification)
    result={"format":"universe24-coherent-wave-result-v1","status":"completed" if reason is None else "incomplete","stop_reason":reason,
        "registered_cases":len(planned),"completed_cases":len(ledger),"cases":ledger,"not_run_cases":planned[len(ledger):],
        "accepted_comparisons":sum(r["accepted_comparison"] for r in ledger),"all_full_state_inverses":all(r["full_state_inverse"] for r in ledger),
        "source_verification":verification,"cpu_seconds":time.process_time()-cpu,"wall_seconds":time.monotonic()-wall,"claim_limits":p["scope_limits"]}
    base.write_json(output/"result.json",result)
    size=sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
    base.write_json(output/"budget_receipt.json",{"bytes":size,"byte_overrun":max(0,size-p["budget"]["max_output_bytes"]),
        "cpu_overrun":max(0,result["cpu_seconds"]-p["budget"]["max_cpu_seconds"]),"wall_overrun":max(0,result["wall_seconds"]-p["budget"]["max_wall_seconds"])})
    print(base.canonical({k:result[k] for k in ("completed_cases","accepted_comparisons","cpu_seconds","status")}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,default=PROTOCOL);args=parser.parse_args(argv);return run(args.output,args.protocol)


if __name__=="__main__":main()
