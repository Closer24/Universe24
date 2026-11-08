"""Bounded full-horizon extension of unresolved periodic clock preparations."""
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
from universe24 import Channel
from . import recurrence as short
from .provenance import freeze_sources, verify_sources

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/"recurrence_long_protocol.json"


def cases(p):
    for stage,sides in (("discovery",p["discovery_sides"]),("holdout",p["holdout_sides"])):
        for side in sides:
            for mask in p["controls"]:
                yield {"id":f"long-ring-L{side}","side":side,"stage":stage,"phase":2,
                    "clock_remainder":0,"guide_target_channel":0,"compensation_direction":None,
                    "control":mask,"pristine":False}


def case_spec(case,p):
    spec=short.case_spec(case,p)
    spec["steps"]=32*case["side"]+40
    spec["budget"]["max_frames"]=spec["steps"]+1
    spec["title"]="Long returning-carrier control: "+spec["id"]
    spec["description"]="Complete registered horizon; unchanged Rule3 and one initially prepared carrier. All32 return opportunities and raw arithmetic events are retained."
    return spec


def whole_board_period(states):
    hashes=[state_sha256(state) for state in states]
    first,repeats={},[]
    for t,digest in enumerate(hashes):
        if digest in first:
            old=first[digest]
            if states[old]!=states[t]:raise ValueError("State hash collision")
            repeats.append([old,t])
        else:first[digest]=t
    period=min((b-a for a,b in repeats),default=None)
    overlaps=None if period is None else all(states[t]==states[t+period] for t in range(len(states)-period))
    closed=period is not None and states[0]==states[period]
    return {"full_state_hashes":hashes,"first_repeat":repeats[0] if repeats else None,
        "smallest_observed_period":period,"all_shifted_overlaps_equal":overlaps,
        "initial_state_closes":closed,"full_board_period_certified":bool(closed and overlaps)}


def supplemental_scan(states,side):
    c=side//2;anchor=Channel(1,0,4)
    # Every exact +X packet has this anchor. It is only a lossless candidate
    # filter; acceptance still compares every channel and retained remainder.
    matches=[[x for x in range(side) if state.at((x,c,c,0))==anchor
              and short.packet_matches(state,x,c,c)] for state in states]
    first_empty=next((t for t in range(28,len(states)) if not matches[t]),None)
    next_match=None if first_empty is None else next((t for t in range(first_empty+1,len(states)) if matches[t]),None)
    return {"origins_at_every_state":matches,"scan_start_for_loss":28,
        "first_empty_state_after_initial_output_window":first_empty,
        "first_subsequent_nonempty_state":next_match,
        "reappearance_after_loss":next_match is not None,
        "interpretation":"Exact matching templates only; discontinuity prevents identifying the later match as uninterrupted transport or an approved trial."}


def observe(case,p,prepared,states):
    result=short.observe(case,p,prepared,states)
    result["whole_board_period"]=whole_board_period(states)
    result["supplemental_template_scan"]=supplemental_scan(states,case["side"])
    result["native_horizon_complete"]=len(states)==32*case["side"]+41
    return result


def assess_group(rows,p):
    base_group=short.assess_group(rows,p)
    by={r["case"]["control"]:r for r in rows}
    trace={m:r["observations"]["cycles"] for m,r in by.items()}
    first=trace["11"][0];returns=[]
    for n in range(1,33):
        cur,prior=trace["11"][n],trace["11"][n-1]
        from_initial=all(by["11"]["observations"]["packet_tracking"][24:8+n*rows[0]["case"]["side"]])
        genuine=bool(first["incoming_complete"] and first["outgoing_complete"] and from_initial)
        eligible=genuine and cur["incoming_complete"] and prior["complete_hold"]
        comparator=trace["10"][n]["incoming_complete"]
        differs=cur["outgoing_complete"]!=trace["10"][n]["outgoing_complete"]
        returns.append({"cycle":n,"genuine_continuous_return":genuine,
            "continuous_from_previous_scheduled_output":cur["continuous_return"],
            "continuous_from_initial_output":from_initial,
            "phase_prediction_eligible":eligible,"predicted_output":False,
            "observed_output":cur["outgoing_complete"],
            "prediction_matches":None if not eligible else not cur["outgoing_complete"],
            "packet_only_input_valid":comparator,"output_differs_from_packet_only":differs,
            "bounded_clock_conditioned_return":bool(base_group["control_checks"] and eligible and comparator and differs),
            "raw_C_signature":cur["exact_outlet_C_signature"]})
    outputs=[row["outgoing_complete"] for row in trace["11"]]
    changes=[n for n in range(1,len(outputs)) if outputs[n]!=outputs[n-1]]
    return {**base_group,"returns":returns,"scheduled_output_by_cycle":outputs,
        "scheduled_output_change_cycles":changes,
        "supplemental_template_reappearance":by["11"]["observations"]["supplemental_template_scan"]["reappearance_after_loss"],
        "whole_board_period_by_control":{m:{k:v for k,v in row["observations"]["whole_board_period"].items() if k!="full_state_hashes"} for m,row in by.items()}}


def run(output,protocol_path=PROTOCOL):
    raw=Path(protocol_path).read_bytes();p=json.loads(raw);planned=list(cases(p))
    if len(planned)!=p["budget"]["registered_cases"]:raise ValueError("Registered case count mismatch")
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/"records").mkdir();(output/"native").mkdir()
    (output/"protocol.json").write_bytes(raw)
    paths=short.source_paths(short.PROTOCOL)+[Path(__file__),Path(protocol_path)]
    snap=freeze_sources(output/"source_provenance",[str(f.relative_to(ROOT)) for f in paths],
        metadata={"protocol_sha256":hashlib.sha256(raw).hexdigest(),"cases":planned,"seed":None,"budget":p["budget"],"board":p["board"]})
    registration={"format":"universe24-clock-long-recurrence-registration-v1","cases":planned,
        "protocol_sha256":hashlib.sha256(raw).hexdigest(),"base_commit":snap["base_commit"],
        "source_sha256":snap["source_sha256"],"registered_before_capture":True}
    base.write_json(output/"registration.json",registration)
    cpu,wall=time.process_time(),time.monotonic();ledger=[];groups=[];current=[];reason=None
    for case in planned:
        if time.process_time()-cpu>=p["budget"]["max_cpu_seconds"]:reason="cpu_budget";break
        if time.monotonic()-wall>=p["budget"]["max_wall_seconds"]:reason="wall_budget";break
        if sum(f.stat().st_size for f in output.rglob('*') if f.is_file())>=p["budget"]["max_recorded_bytes"]:reason="byte_budget";break
        spec=case_spec(case,p);prepared=assemble(spec)
        try:captured=run_experiment(spec)
        except (TimeoutError,ValueError) as exc:
            reason="capture_incomplete"
            base.write_json(output/"capture_failure.json",{"case":case,"spec":spec,"error":str(exc),"type":type(exc).__name__,"completed_prefix_available":False})
            break
        states=recorded_states(captured["experiment"]);obs=observe(case,p,prepared,states)
        row={"format":"universe24-clock-long-recurrence-record-v1","case":case,"spec":spec,
            "assembly":captured["assembly"],"experiment":captured["experiment"],"observations":obs,
            "protocol_sha256":registration["protocol_sha256"]}
        encoded=base.canonical(row).encode();compressed=gzip.compress(encoded,mtime=0)
        relative="records/"+spec["id"]+".json.gz";(output/relative).write_bytes(compressed)
        native=base.canonical(bundle([captured["experiment"]],title="Long recurrence: one complete control")).encode()+b"\n"
        if len(native)>p["budget"]["max_native_bundle_bytes"]:raise ValueError("Complete native bundle exceeds registered Presenter byte limit")
        native_path="native/"+spec["id"]+".json";(output/native_path).write_bytes(native)
        ledger.append({"id":spec["id"],"case":case,"record":relative,"record_sha256":hashlib.sha256(encoded).hexdigest(),
            "record_gzip_sha256":hashlib.sha256(compressed).hexdigest(),"native":native_path,"native_sha256":hashlib.sha256(native).hexdigest(),
            "frames":len(states),"transitions":len(states)-1,"complete_sparse_rows":sum(len(f["cells"]) for f in captured["experiment"]["frames"]),
            "full_state_inverse":captured["experiment"]["provenance"]["full_rewind_equal"]})
        current.append({**row,"states":states})
        if len(current)==4:groups.append(assess_group(current,p));current=[]
        base.write_json(output/"progress.json",{"completed":len(ledger),"registered":len(planned),"last_id":spec["id"]})
        print(base.canonical({"completed":len(ledger),"registered":len(planned),"id":spec["id"]}),flush=True)
    verification=verify_sources(output/"source_provenance");base.write_json(output/"source_verification.json",verification)
    result={"format":"universe24-clock-long-recurrence-result-v1","status":"completed" if reason is None else "incomplete",
        "stop_reason":reason,"registered_cases":len(planned),"completed_cases":len(ledger),"cases":ledger,"not_run_cases":planned[len(ledger):],
        "groups":groups,"all_full_state_inverses":all(r["full_state_inverse"] for r in ledger),"source_verification":verification,
        "genuine_continuous_returns":sum(r["genuine_continuous_return"] for g in groups for r in g["returns"]),
        "bounded_clock_conditioned_returns":sum(r["bounded_clock_conditioned_return"] for g in groups for r in g["returns"]),
        "supplemental_joint_reappearances":sum(g["supplemental_template_reappearance"] for g in groups),
        "cpu_seconds":time.process_time()-cpu,"wall_seconds":time.monotonic()-wall,"claim":p["claim"]}
    base.write_json(output/"result.json",result)
    size=sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
    base.write_json(output/"budget_receipt.json",{"bytes":size,"byte_overrun":max(0,size-p["budget"]["max_recorded_bytes"]),
        "cpu_overrun":max(0,result["cpu_seconds"]-p["budget"]["max_cpu_seconds"]),"wall_overrun":max(0,result["wall_seconds"]-p["budget"]["max_wall_seconds"])})
    print(base.canonical({k:result[k] for k in ("completed_cases","genuine_continuous_returns","bounded_clock_conditioned_returns","supplemental_joint_reappearances","cpu_seconds")}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,default=PROTOCOL)
    args=parser.parse_args(argv);return run(args.output,args.protocol)


if __name__=="__main__":main()
