"""Prospective finite recurrence of one prepared carrier; no reinjection."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time
from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from research.staged_blocks import interactions as base
from universe24 import State
from .provenance import freeze_sources, verify_sources

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "recurrence_protocol.json"


def cases(p):
    for stage,sides in (("discovery",p["discovery_sides"]),("holdout",p["holdout_sides"])):
        for side in sides:
            common = {"side":side,"stage":stage,"phase":2,"clock_remainder":0,
                      "guide_target_channel":0,"compensation_direction":None}
            yield {**common,"id":f"ring-pristine-L{side}","control":"10","pristine":True}
            for mask in p["controls"]:
                yield {**common,"id":f"ring-L{side}","control":mask,"pristine":False}


def observer_protocol(case,p):
    bp = json.loads(base.PROTOCOL.read_text()); side=case["side"]; c=side//2
    bp.update({"board":{**p["board"],"side":side},"steps":2*side+40,"question":p["question"]})
    bp["geometry"] = {"row_y":c,"row_z":c,"packet_x":c-16,"clock_x":c,
                      "clock_y":c+1,"clock_z":c,"forward_outlet_x":c+8,"backward_outlet_x":c-8}
    bp["readouts"]["eligible_hold_starts"] = []
    bp["budget"].update({k:p["budget"][k] for k in ("max_cells_per_record","max_seconds_per_record")})
    return bp


def case_spec(case,p):
    spec=base.case_spec(case,observer_protocol(case,p))
    if case["pristine"]:
        side=case["side"];c=side//2;source=c-16
        spec["components"][0]["params"]["cells"] = [
            [x,c,c,g,0,0,r] for x in range(side) if x not in range(source,source+4)
            for g,r in ((0,0),(14,4))]
        spec["components"][0]["params"]["kind"] = "pristine-periodic-guide"
        spec["components"][0]["params"]["sources"] = {}
    spec["title"] = "Returning carrier and clock: "+spec["id"]
    spec["description"] = "One prepared carrier, ordinary periodic Rule3; no reinjection. All full states and arithmetic events are retained."
    spec["provenance"] = {"protocol_canonical_sha256":base.digest(p),"initial_only":True,
                          "periodic_boundary_is_intentional":True}
    return spec


def translated(state,offset):
    side=state.cube.side
    return State(state.cube,state.background,{((a[0]+offset)%side,*a[1:]):v for a,v in state.cells.items()})


def packet_matches(state,origin,y,z):
    side=state.cube.side;origin%=side
    xs={(origin+d)%side for d in range(-1,5)}
    ys={(y+d)%side for d in range(-1,2)};zs={(z+d)%side for d in range(-1,2)}
    actual={a:v for a,v in state.cells.items() if a[0] in xs and a[1] in ys and a[2] in zs}
    expected={(a[0]%side,a[1]%side,a[2]%side,a[3]):v
              for a,v in base._expected_packet(origin,y,z,1).items()}
    return actual==expected


def observe(case,p,prepared,states):
    data=base.observe(observer_protocol(case,p),case,prepared,states)
    side=case["side"];c=side//2
    track=[packet_matches(s,c-16+t,c,c) for t,s in enumerate(states)]
    cycles=[]
    for n in p["cycles"]:
        shift=n*side;start,end=(shift+v for v in p["hold_offsets"])
        frames=data["region_trace"][start:end+1];center=data["center_trace"][start:end+1]
        checks={"complete_lag_four":all(frames[t]==frames[t+4] for t in range(len(frames)-4)),
            "unit_clock_r0":all(a*a+b*b==1 and r==0 for a,b,r in center),
            "other_pairs_zero":all(not(v[0] or v[1]) for f in frames for g,v in enumerate(f) if g!=2),
            "individual_external_terms_zero":all(not data["boundary_inputs"][t]["nonzero_external_terms"] for t in range(start,end)),
            "center_u_zero":all(data["center_inputs"][t]["u"]==0 for t in range(start,end)),
            "center_ell_zero":all(data["center_trace"][t+1][1]+data["center_trace"][t][0]==0 for t in range(start,end))}
        lo,hi=(shift+v for v in p["C_signature"]["window_offsets"])
        events=[[e["step"],e["kind"],e["ell"]] for e in data["all_C"]
                if e["address"]==[c+8,c,c,0] and lo<=e["step"]<=hi]
        expected=[[shift+t,k,q] for t,k,q in p["C_signature"]["expected"]]
        cycles.append({"cycle":n,"incoming_matches":[track[shift+t] for t in p["incoming_offsets"]],
            "incoming_complete":all(track[shift+t] for t in p["incoming_offsets"]),
            "outgoing_matches":[track[shift+t] for t in p["outgoing_offsets"]],
            "outgoing_complete":all(track[shift+t] for t in p["outgoing_offsets"]),
            "continuous_return":None if n==0 else all(track[24+(n-1)*side:8+n*side]),
            "hold_start":start,"hold_through":end,"hold_checks":checks,"complete_hold":all(checks.values()),
            "outlet_C":events,"exact_outlet_C_signature":events==expected})
    return {**data,"packet_tracking":track,"cycles":cycles,
            "pristine_full_translation":case["pristine"] and all(s==translated(states[0],t) for t,s in enumerate(states))}


def assess_group(rows,p):
    by={r["case"]["control"]:r for r in rows};side=rows[0]["case"]["side"]
    initial={m:r["states"][0] for m,r in by.items()}
    addresses=set().union(*(s.cells for s in initial.values()))
    matched=all(len({s.at(a).r for s in initial.values()})==1 for a in addresses)
    declared=rows[0]["assembly"]["sources"]
    deltas={m:{a for a in addresses if initial[m].at(a)[:2]!=initial["00"].at(a)[:2]} for m in ("10","01")}
    masks=(deltas["10"]=={tuple(a) for a in declared["packet.packet"]}
        and deltas["01"]=={tuple(a) for a in declared["apparatus.clock"]} and not(deltas["10"]&deltas["01"])
        and all(initial["11"].at(a)[k]==initial["10"].at(a)[k]+initial["01"].at(a)[k]-initial["00"].at(a)[k]
                for a in addresses for k in (0,1)))
    null=all(s==initial["00"] for s in by["00"]["states"]);quiet=by["01"]["states"]
    period=all(quiet[t]==quiet[t+4] for t in range(len(quiet)-4));controls=matched and masks and null and period
    traces={m:r["observations"]["cycles"] for m,r in by.items()};first=traces["11"][0];returns=[]
    for n in (1,2):
        cur,prev=traces["11"][n],traces["11"][n-1]
        returned=bool(first["incoming_complete"] and first["outgoing_complete"] and cur["continuous_return"])
        eligible=returned and cur["incoming_complete"] and prev["complete_hold"]
        comparator_valid=traces["10"][n]["incoming_complete"]
        differs=cur["outgoing_complete"]!=traces["10"][n]["outgoing_complete"]
        returns.append({"cycle":n,"genuine_return":returned,"phase_prediction_eligible":eligible,
            "predicted_output":side%4==2,"observed_output":cur["outgoing_complete"],
            "conditional_prediction_matches":None if not eligible else cur["outgoing_complete"]==(side%4==2),
            "packet_only_input_valid":comparator_valid,"output_differs_from_packet_only":differs,
            "bounded_clock_conditioned_return":bool(controls and eligible and comparator_valid and differs),
            "raw_C_signature":cur["exact_outlet_C_signature"]})
    return {"side":side,"stage":rows[0]["case"]["stage"],"matched_remainders":matched,"exact_source_masks":masks,
        "null_static":null,"clock_only_period_four":period,"control_checks":controls,"returns":returns,
        "all_full_state_inverses":all(r["experiment"]["provenance"]["full_rewind_equal"] for r in rows),
        "full_final_hashes":{m:state_sha256(r["states"][-1]) for m,r in by.items()},"claim_limit":p["claim"]}


def source_paths(protocol_path):
    paths=[Path(__file__),Path(protocol_path),HERE/"provenance.py",HERE/"__init__.py",
           Path(base.__file__),base.PROTOCOL,ROOT/"research/staged_blocks/__init__.py"]
    for folder in ("universe24","research/components","research/experiments","research/presenter"):
        paths.extend((ROOT/folder).rglob("*.py"))
    return sorted(set(paths))


def run(output,protocol_path=PROTOCOL):
    raw=Path(protocol_path).read_bytes();p=json.loads(raw);planned=list(cases(p))
    if len(planned)!=p["budget"]["registered_cases"]:raise ValueError("Registered case count mismatch")
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/"records").mkdir()
    (output/"protocol.json").write_bytes(raw)
    paths=[str(f.relative_to(ROOT)) for f in source_paths(protocol_path)]
    snapshot=freeze_sources(output/"source_provenance",paths,
        metadata={"protocol_sha256":hashlib.sha256(raw).hexdigest(),"cases":planned,"seed":None,
                  "budget":p["budget"],"board":p["board"]})
    registration={"format":"universe24-clock-recurrence-registration-v1","cases":planned,
        "protocol_sha256":hashlib.sha256(raw).hexdigest(),"base_commit":snapshot["base_commit"],
        "source_sha256":snapshot["source_sha256"],"registered_before_capture":True}
    base.write_json(output/"registration.json",registration)
    start_cpu,start_wall=time.process_time(),time.monotonic()
    ledger,groups,examples,current=[],[],[],[];reason=None
    for case in planned:
        if time.process_time()-start_cpu>=p["budget"]["max_cpu_seconds"]:reason="cpu_budget";break
        if time.monotonic()-start_wall>=p["budget"]["max_wall_seconds"]:reason="wall_budget";break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p["budget"]["max_recorded_bytes"]:
            reason="byte_budget";break
        spec=case_spec(case,p);prepared=assemble(spec)
        try:captured=run_experiment(spec)
        except (TimeoutError,ValueError) as exc:
            reason="capture_incomplete"
            base.write_json(output/"capture_failure.json",{"case":case,"spec":spec,"error":str(exc),"type":type(exc).__name__})
            break
        states=recorded_states(captured["experiment"]);obs=observe(case,p,prepared,states)
        row={"format":"universe24-clock-recurrence-record-v1","case":case,"spec":spec,
             "assembly":captured["assembly"],"experiment":captured["experiment"],"observations":obs,
             "protocol_sha256":registration["protocol_sha256"]}
        encoded=base.canonical(row).encode();compressed=gzip.compress(encoded,mtime=0)
        relative="records/"+spec["id"]+".json.gz";(output/relative).write_bytes(compressed)
        ledger.append({"id":spec["id"],"case":case,"record":relative,
            "record_sha256":hashlib.sha256(encoded).hexdigest(),"record_gzip_sha256":hashlib.sha256(compressed).hexdigest(),
            "frames":len(states),"transitions":len(states)-1,"initial_state_sha256":state_sha256(states[0]),
            "final_state_sha256":state_sha256(states[-1]),"full_state_inverse":captured["experiment"]["provenance"]["full_rewind_equal"],
            "pristine_full_translation":obs["pristine_full_translation"]})
        if not case["pristine"]:
            current.append({**row,"states":states})
            if len(current)==4:groups.append(assess_group(current,p));current=[]
        if not case["pristine"] and case["side"] in p["presenter_selection"]["sides"]:
            examples.append(captured["experiment"])
        base.write_json(output/"progress.json",{"completed":len(ledger),"registered":len(planned),"last_id":spec["id"]})
        print(base.canonical({"completed":len(ledger),"registered":len(planned),"id":spec["id"]}),flush=True)
    verification=verify_sources(output/"source_provenance")
    base.write_json(output/"source_verification.json",verification)
    result={"format":"universe24-clock-recurrence-result-v1","status":"completed" if reason is None else "incomplete",
        "stop_reason":reason,"registered_cases":len(planned),"completed_cases":len(ledger),"cases":ledger,
        "not_run_cases":planned[len(ledger):],"groups":groups,
        "pristine_translation_passes":sum(r["pristine_full_translation"] for r in ledger),
        "genuine_returns":sum(r["genuine_return"] for g in groups for r in g["returns"]),
        "bounded_clock_conditioned_returns":sum(r["bounded_clock_conditioned_return"] for g in groups for r in g["returns"]),
        "all_full_state_inverses":all(r["full_state_inverse"] for r in ledger),"source_verification":verification,
        "cpu_seconds":time.process_time()-start_cpu,"wall_seconds":time.monotonic()-start_wall,"claim":p["claim"]}
    base.write_json(output/"result.json",result)
    if examples:(output/"experiments.json").write_text(base.canonical(bundle(examples,title="One prepared carrier: finite clock recurrence"))+"\n")
    size=sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
    base.write_json(output/"budget_receipt.json",{"bytes":size,"byte_overrun":max(0,size-p["budget"]["max_recorded_bytes"]),
        "cpu_overrun":max(0,result["cpu_seconds"]-p["budget"]["max_cpu_seconds"]),
        "wall_overrun":max(0,result["wall_seconds"]-p["budget"]["max_wall_seconds"])})
    print(base.canonical({k:result[k] for k in ("completed_cases","genuine_returns","bounded_clock_conditioned_returns","cpu_seconds")}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,default=PROTOCOL)
    args=parser.parse_args(argv)
    return run(args.output,args.protocol)


if __name__=="__main__":main()
