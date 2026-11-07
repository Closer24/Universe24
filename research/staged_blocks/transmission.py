"""Prospective complete-carrier transmission validation; initial state only."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import assemble, recorded_states, run_experiment
from research.presenter.export import bundle, state_sha256
from . import interactions as base

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/"transmission_protocol.json"


def geometries(p):
    f=p["family"]
    for family,side,delay in itertools.product(f["families"],f["board_sides"],f["packet_delays"]):
        phase=((2 if family=="enable" else 0)-delay)%4
        yield {"id":f"transmission-{family}-L{side}-d{delay}","family":family,"side":side,"delay":delay,
               "phase":phase,"stage":"base","guide_target_channel":0,"clock_remainder":0,"compensation_direction":None}


def base_protocol(case,p):
    result=json.loads(base.PROTOCOL.read_text())
    c=case["side"]//2
    result["board"]={**p["board"],"side":case["side"]}
    result["steps"]=p["steps"]
    result["geometry"]={"row_y":c,"row_z":c,"packet_x":c-16-case["delay"],"clock_x":c,"clock_y":c+1,"clock_z":c,
                        "forward_outlet_x":c+8,"backward_outlet_x":c-8}
    result["budget"].update({k:p["budget"][k] for k in ("max_cells_per_record","max_seconds_per_record")})
    return result


def case_spec(case,p):
    spec=base.case_spec(case,base_protocol(case,p))
    spec["title"]="Prepared clock controls transmission: "+spec["id"]
    spec["question"]=p["question"]
    spec["description"]="Unchanged Rule3 evolves one complete board. A prepared clock's counter state may enable or suppress a guided carrier; complete matched controls and all arithmetic events remain visible. No runtime switch or source is used."
    spec["provenance"]={"protocol_sha256":hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),"initial_only":True,
                        "discovery_source":"research/staged_blocks/evidence/interactions/main"}
    return spec


def node_inputs(states,engine,position):
    donors=[[list(states[0].cube.adjacent((*position,g),d,engine.coupling.ports[d][g])) for d in range(6)] for g in range(48)]
    weights=[[engine.coupling.weights[d][g] for d in range(6)] for g in range(48)]
    rows=[]
    for t,state in enumerate(states[:-1]):
        terms=[[weights[g][d]*state.at(tuple(donors[g][d])).b for d in range(6)] for g in range(48)]
        rows.append({"update":t+1,"six_signed_terms":terms,"input_sums":[sum(row) for row in terms]})
    return {"position":list(position),"donor_addresses":donors,"weights":weights,"trace":rows}


def observe(case,p,prepared,states):
    bp=base_protocol(case,p)
    original=base.observe(bp,case,prepared,states)
    c=case["side"]//2;delay=case["delay"];source=c-16-delay
    incoming=[{"step":t,"origin_x":source+t,"full_template_equal":base.packet_matches(states[t],source+t,c,c,1)}
              for t in range(delay+4,delay+8)]
    start=24+delay
    forward=[{"step":start+k,"origin_x":c+8+k,"full_template_equal":base.packet_matches(states[start+k],c+8+k,c,c,1)}
             for k in range(4)]
    active=[a for a,v in states[0].cells.items() if v.a or v.b]
    edge_distance=min((min(q,case["side"]-1-q) for a in active for q in a[:3]),default=None)
    return {**original,"incoming_fixed":incoming,"forward_fixed":forward,
            "incoming_complete":all(v["full_template_equal"] for v in incoming),
            "forward_complete":all(v["full_template_equal"] for v in forward),
            "clock_node_inputs":node_inputs(states,prepared.engine,(c,c+1,c)),
            "minimum_initial_active_boundary_distance":edge_distance}


def group_assessment(rows,p):
    by={r["case"]["control"]:r for r in rows}
    geometry={k:v for k,v in rows[0]["case"].items() if k!="control"}
    predictions=p["readouts"]["forward_prediction"][geometry["family"]]
    initial={mask:row["states"][0] for mask,row in by.items()}
    addresses=set().union(*(state.cells for state in initial.values()))
    matched=all(len({state.at(a).r for state in initial.values()})==1 for a in addresses)
    # Check that the data and clock source removals commute and only their
    # declared initial counter masks differ; all remainders remain unchanged.
    packet_delta={a for a in addresses if initial["10"].at(a)[:2]!=initial["00"].at(a)[:2]}
    clock_delta={a for a in addresses if initial["01"].at(a)[:2]!=initial["00"].at(a)[:2]}
    declared=rows[0]["assembly"]["sources"]
    declared_packet={tuple(a) for a in declared["packet.packet"]}
    declared_clock={tuple(a) for a in declared["apparatus.clock"]}
    masks_disjoint=not(packet_delta&clock_delta)
    counter_masks=all(initial["11"].at(a)[j]==initial["10"].at(a)[j]+initial["01"].at(a)[j]-initial["00"].at(a)[j]
                      for a in addresses for j in (0,1))
    counter_masks=(counter_masks and packet_delta==declared_packet and clock_delta==declared_clock
                   and all(v.a==v.b==0 for v in initial["00"].cells.values()))
    null_static=all(s==by["00"]["states"][0] for s in by["00"]["states"])
    clock=by["01"]["states"]
    period4=all(clock[t]==clock[t+4] for t in range(len(clock)-4))
    cases={}
    for mask,row in by.items():
        obs=row["observations"]
        incoming=[v["full_template_equal"] for v in obs["incoming_fixed"]]
        incoming_ok=all(incoming) if mask[0]=="1" else not any(incoming)
        forward_scan=[v for v in obs["outgoing_carriers"] if v["direction"]==1]
        backward_scan=[v for v in obs["outgoing_carriers"] if v["direction"]==-1]
        checks={"incoming_prediction":incoming_ok,"fixed_forward_prediction":obs["forward_complete"]==predictions[mask],
                "no_unexpected_late_forward":predictions[mask] or not forward_scan,
                "no_backward_carrier":not backward_scan,"no_active_boundary":not obs["active_boundary_hits"],
                "initial_boundary_margin":obs["minimum_initial_active_boundary_distance"] is None or obs["minimum_initial_active_boundary_distance"]>p["steps"],
                "full_state_inverse":row["experiment"]["provenance"]["full_rewind_equal"]}
        cases[mask]={"checks":checks,"passed":all(checks.values()),"expected_forward":predictions[mask],
                     "observed_forward":obs["forward_complete"],"forward_scan":forward_scan,"backward_scan":backward_scan,
                     "all_C_count":len(obs["all_C"]),"center_C_count":len(obs["center_C"])}
    finals={mask:row["states"][-1] for mask,row in by.items()}
    hashes={mask:state_sha256(state) for mask,state in finals.items()}
    different={a for a in set(finals["11"].cells)|set(finals["10"].cells) if finals["11"].at(a)!=finals["10"].at(a)}
    c=geometry["side"]//2
    outside=[a for a in different if not(c+7<=a[0]<=c+15 and abs(a[1]-c)<=1 and abs(a[2]-c)<=1)]
    checks={"matched_initial_remainders":matched,"source_counter_masks_disjoint":masks_disjoint,
            "source_counter_masks_exact":counter_masks,"null_static":null_static,"clock_only_full_period4":period4,
            "four_final_states_distinct":len(set(hashes.values()))==4,"all_control_predictions":all(v["passed"] for v in cases.values())}
    return {"geometry":geometry,"checks":checks,"passed":all(checks.values()),"controls":cases,
            "full_state_final_hashes":hashes,"clock_control_final_differences":len(different),
            "clock_control_final_differences_outside_outlet_region":len(outside),
            "effective_coupler_supported":all(checks.values()),"splitter_or_payload_release_established":False}


def source_hashes():
    paths=[Path(__file__),PROTOCOL,Path(base.__file__),base.PROTOCOL]
    for folder in ("universe24","research/components","research/experiments","research/presenter"):
        paths.extend((ROOT/folder).rglob("*.py"))
    return {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}


def run(output):
    output=Path(output);raw=PROTOCOL.read_bytes();p=json.loads(raw)
    planned=list(geometries(p));assert4=4*len(planned)
    if assert4!=p["family"]["cases"] or assert4!=p["budget"]["max_cases"]:
        raise ValueError("Registered family/case budget mismatch")
    output.mkdir(parents=True,exist_ok=False);(output/"records").mkdir()
    (output/"protocol.json").write_bytes(raw)
    hashes=source_hashes()
    registration={"format":"universe24-staged-transmission-registration-v1","protocol_sha256":hashlib.sha256(raw).hexdigest(),
                  "source_sha256":hashes,"planned_groups":planned,"registered_cases":assert4,"seed":None,
                  "base_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"registered_before_capture":True}
    base.write_json(output/"registration.json",registration)
    start,cpu=time.monotonic(),time.process_time();groups=[];ledger=[];examples=[];reason=None
    for geometry in planned:
        if time.process_time()-cpu>=p["budget"]["max_cpu_seconds"]-5 or time.monotonic()-start>=p["budget"]["max_wall_seconds"]-5:
            reason="budget_before_next_complete_group";break
        rows=[]
        for mask in p["family"]["controls"]:
            case={**geometry,"control":mask};spec=case_spec(case,p);prepared=assemble(spec)
            captured=run_experiment(spec);states=recorded_states(captured["experiment"])
            obs=observe(case,p,prepared,states)
            rows.append({"case":case,"spec":spec,"assembly":captured["assembly"],"experiment":captured["experiment"],"states":states,"observations":obs})
        assessment=group_assessment(rows,p)
        for row in rows:
            record={"format":"universe24-staged-transmission-record-v1","spec":row["spec"],"case":row["case"],"assembly":row["assembly"],
                    "experiment":row["experiment"],"observations":row["observations"],"assessment":assessment}
            path=output/"records"/(row["spec"]["id"]+".json.gz")
            path.write_bytes(gzip.compress(base.canonical(record).encode(),mtime=0))
            ledger.append({"id":row["spec"]["id"],"case":row["case"],"record":str(path.relative_to(output)),
                           "record_gzip_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"frames":len(row["states"]),
                           "full_state_inverse":row["experiment"]["provenance"]["full_rewind_equal"],
                           "fixed_forward":row["observations"]["forward_complete"],"all_C_count":len(row["observations"]["all_C"])})
            if any(all(geometry[k]==selection[k] for k in selection) for selection in p["presenter_selection"]):
                examples.append(row["experiment"])
        groups.append(assessment)
        print(f"{len(ledger)}/{assert4} {geometry['id']} passed={assessment['passed']}",flush=True)
        if sum(f.stat().st_size for f in output.rglob("*") if f.is_file())>p["budget"]["max_recorded_bytes"]-5000000:
            reason="evidence_budget_before_next_complete_group";break
    if source_hashes()!=hashes or PROTOCOL.read_bytes()!=raw:
        raise RuntimeError("Registered transmission sources changed during the run")
    elapsed_cpu=time.process_time()-cpu
    complete=len(ledger)==assert4 and reason is None
    budget_ok=elapsed_cpu<=p["budget"]["max_cpu_seconds"] and time.monotonic()-start<=p["budget"]["max_wall_seconds"]
    result={"format":"universe24-staged-transmission-result-v1","protocol_sha256":registration["protocol_sha256"],
            "status":"completed" if complete and budget_ok else "budget_stopped","stop_reason":reason,
            "registered_cases":assert4,"completed_cases":len(ledger),"not_run_groups":planned[len(groups):],
            "groups":groups,"cases":ledger,"passed_groups":sum(g["passed"] for g in groups),
            "accepted":bool(complete and budget_ok and all(g["passed"] for g in groups)),
            "family_results":{family:{"groups":sum(g["geometry"]["family"]==family for g in groups),
                                      "passed":sum(g["passed"] and g["geometry"]["family"]==family for g in groups)} for family in p["family"]["families"]},
            "all_full_state_inverses":all(r["full_state_inverse"] for r in ledger),"sources_unchanged":True,
            "cpu_seconds":elapsed_cpu,"wall_seconds":time.monotonic()-start,"displayed_experiments":len(examples),
            "scope":p["scope"],"splitter_or_payload_release_established":False}
    base.write_json(output/"result.json",result)
    (output/"experiments.json").write_text(base.canonical(bundle(examples,title="The Presenter: prepared transmission control"))+"\n")
    if sum(f.stat().st_size for f in output.rglob("*") if f.is_file())>p["budget"]["max_recorded_bytes"]:
        raise RuntimeError("Transmission evidence exceeded its registered size budget")
    print(base.canonical({k:result[k] for k in ("status","completed_cases","passed_groups","accepted","family_results","cpu_seconds")}),flush=True)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",type=Path,required=True)
    return run(parser.parse_args(argv).output)


if __name__=="__main__":main()
