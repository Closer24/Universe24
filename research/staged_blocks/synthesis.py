"""Exact offline synthesis of initial preparations, followed by full Rule3 replay.

The solver is never part of runtime evolution. Public API:
    run_synthesis(output, protocol_path=None) -> result dictionary
    main(["--output", "NEW_DIRECTORY"])
Install the pinned optional dependency with: python -m pip install z3-solver==4.15.4.0
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

from research.experiments.run import assemble, run_experiment
from research.light_approval.compute import local_trace
from research.presenter.export import bundle, write_bundle
from research.component_review import audit as matrix_audit
from universe24 import Coupling
from universe24.core.group_2o import DIRECTIONS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_PROTOCOL = HERE / "synthesis_protocol_a.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def require_z3():
    try:
        import z3
    except ImportError as exc:
        raise RuntimeError("Optional exact synthesis requires z3-solver==4.15.4.0") from exc
    return z3


class EncodingLimit(RuntimeError):
    """A complete encoding exceeds the registered resource budget."""


def add_rule3_constraints(solver, old, incoming, name):
    """Exact signed Euclidean Rule3, expressed only with linear integer terms."""
    z3 = require_z3()
    next_b, next_r = z3.Int(name + "_b"), z3.Int(name + "_r")
    solver.add(6 * (next_b + old[0]) + next_r == 2 * incoming + old[2],
               next_r >= 0, next_r < 6)
    return old[1], next_b, next_r


def forward_cones(side, ports, active, steps):
    """Conservative possible influence, including retained local state.

    Outside F[t], no initial active counter can have influenced the channel;
    its counters remain zero and its remainder is its exact initial value.
    Unknown initial remainders alone do not generate activity.
    """
    inverse = [{sender: receiver for receiver, sender in enumerate(row)} for row in ports]
    cones = [set(active)]
    for _ in range(steps):
        following = set(cones[-1])
        for x, y, z, channel in cones[-1]:
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                following.add(((x-dx) % side, (y-dy) % side, (z-dz) % side, inverse[d][channel]))
        cones.append(following)
    return cones


def dependency_cones(side, ports, forward, observations):
    """Every old a,b,r and signed-neighbor b dependency is retained.

    Intersect only with the proved possible-influence sets. An omitted
    dependency reads its exact initial triple, not an absorbing boundary.
    """
    steps = len(forward)-1
    needed = [set() for _ in forward]
    needed[steps] = set(observations.get(steps, ())) & forward[steps]
    for t in range(steps-1, -1, -1):
        parents = set(observations.get(t, ()))
        for x, y, z, channel in needed[t+1]:
            parents.add((x, y, z, channel))
            for d, (dx, dy, dz) in enumerate(DIRECTIONS):
                parents.add(((x+dx) % side, (y+dy) % side, (z+dz) % side, ports[d][channel]))
        needed[t] = parents & forward[t]
    return needed


def spec_for(protocol, remainder_values, present):
    """A data-only generic assembly; values are chosen before runtime starts."""
    addresses = [tuple(a) for a in protocol["unknown_remainder_addresses"]]
    if len(remainder_values) != len(addresses):
        raise ValueError("One initial remainder is required per declared address")
    if any(type(r) is not int or r not in protocol["allowed_remainders"] for r in remainder_values):
        raise ValueError("An initial apparatus remainder is outside the registered domain")
    values = dict(zip(addresses, remainder_values))
    p = protocol
    source, receiver = p["source"], p["receiver"]
    row_x = p["apparatus_row_x"]
    components = [
        {"name": "guide", "recipe": "GuideSegment", "at": [0, receiver[1], receiver[2]],
         "params": {"start": 0, "stop": p["board"]["side"]-1, "remainder_pair": p["guide_pair"],
                    "sockets": list(range(source[0], source[0]+4))+row_x+[receiver[0]]}},
        {"name": "source", "recipe": "GuidedPacketSource", "at": source, "params": {"present": present}},
        {"name": "receiver", "recipe": "Receiver", "at": receiver,
         "params": {"remainders": p["ready_pair"]}},
    ]
    row_addresses = set()
    for x in row_x:
        pair_addresses = [(x, receiver[1], receiver[2], g) for g in (0,14)]
        row_addresses.update(pair_addresses)
        components.append({"name": "apparatus-"+str(x), "recipe": "Receiver", "at": [x, receiver[1], receiver[2]],
                           "params": {"remainders": [values[a] for a in pair_addresses]}})
    sides = [a for a in addresses if a not in row_addresses]
    components.append({"name": "transverse-apparatus", "recipe": "Patch", "at": [0,0,0],
                       "params": {"kind": "receiver", "cells": [[*a,0,0,values[a]] for a in sides]}})
    return {"format": "universe24-assembly-experiment-v1", "id": "synthesis-a-"+("on" if present else "off"),
            "title": "Exact synthesized pending interface: source " + ("present" if present else "absent"),
            "description": "The apparatus was chosen offline by exact integer constraints. Every recorded update is unchanged full-board Rule3; the solver and readouts do not participate in runtime.",
            "board": p["board"], "steps": p["steps"], "components": components,
            "detectors": ["receiver.node"], "view": {"port": "receiver.memory"},
            "controls": {"source_present": present, "apparatus_remainders": list(remainder_values)},
            "provenance": {"protocol_id": p["id"], "canonical_protocol_sha256": digest(p)},
            "budget": {"max_frames": p["steps"]+1, "max_cells": 500000, "max_bytes": 67108864, "max_seconds": 60}}


def validate_protocol(p):
    if p["format"] != "universe24-staged-synthesis-v1":
        raise ValueError("Unsupported synthesis protocol")
    if p["pilot"] != "A" or p["steps"] != 12 or p["pending_states"] != [4,12]:
        raise ValueError("This implementation encodes the registered Pilot A observer only")
    if p["ready_pair"] != [4,2] or p["pending_pair"] != [2,4] or p["allowed_remainders"] != [0,2,4]:
        raise ValueError("The registered receiver or apparatus domain was changed")
    addresses = [tuple(a) for a in p["unknown_remainder_addresses"]]
    if len(addresses) != 22 or len(set(addresses)) != 22:
        raise ValueError("Pilot A needs exactly 22 distinct initial remainder addresses")
    coupling = Coupling(tuple(p["board"]["body_signs"]))
    if p["tensor"]["fingerprint"] != coupling.fingerprint:
        raise ValueError("Registered tensor fingerprint mismatch")
    if p["tensor"]["ports"] != [list(row) for row in coupling.ports] or p["tensor"]["weights"] != [list(row) for row in coupling.weights]:
        raise ValueError("Registered complete tensor mismatch")
    if any(a[:3] == tuple(p["receiver"]) for a in addresses):
        raise ValueError("The receiver cannot be an unknown preparation variable")
    expected = [(x,*p["receiver"][1:],g) for x in p["apparatus_row_x"] for g in (0,14)]
    for x in p["apparatus_transverse_x"]:
        for d in range(2,6):
            dx,dy,dz = DIRECTIONS[d]
            expected.extend((x+dx,p["receiver"][1]+dy,p["receiver"][2]+dz,coupling.ports[d][g]) for g in (0,14))
    if addresses != expected:
        raise ValueError("The explicit address list differs from the declared apparatus geometry")
    return coupling


def preflight(protocol):
    coupling = validate_protocol(protocol)
    prepared = assemble(spec_for(protocol,[2]*22,True))
    absent = assemble(spec_for(protocol,[2]*22,False))
    if any(v.a or v.b for v in absent.initial.cells.values()):
        raise ValueError("Stationary source-off reduction requires every initial counter to be zero")
    if any(prepared.initial.at(a)[:2] != (0,0) for a in map(tuple,protocol["unknown_remainder_addresses"])):
        raise ValueError("Apparatus variables must have zero initial counters")
    active = {a for a,v in prepared.initial.cells.items() if v.a or v.b}
    observations = {t:{(*protocol["receiver"],g) for g in range(48)} for t in range(protocol["steps"]+1)}
    forward = forward_cones(protocol["board"]["side"],coupling.ports,active,protocol["steps"])
    needed = dependency_cones(protocol["board"]["side"],coupling.ports,forward,observations)
    count = sum(map(len,needed[1:]))
    details = {"source_active_addresses": [list(a) for a in sorted(active)],
               "forward_counts": list(map(len,forward)), "dependency_counts": list(map(len,needed)),
               "encoded_channel_updates": count, "source_off_nontrivial_updates": 0,
               "observed_receiver_channels": 48, "observed_states": list(range(protocol["steps"]+1)),
               "forward_sets_sha256": [digest(sorted(s)) for s in forward],
               "dependency_sets_sha256": [digest(sorted(s)) for s in needed],
               "source_off_all_initial_counters_zero": True,
               "source_off_reduction": "For all initial remainders0..5, a=b=u=0 implies ell=0 and unchanged remainder. Thus the entire source-off board is exactly stationary, including every apparatus and source-halo remainder.",
               "omitted_dependencies": "Outside the exact possible-influence sets, read the exact initial triple and shared remainder variable. No absorbing or clamped boundary is introduced."}
    if count > protocol["budget"]["max_channel_updates"]:
        raise EncodingLimit(f"Complete encoding needs {count} channel updates; cap is {protocol['budget']['max_channel_updates']}")
    return prepared, absent, forward, needed, details


class ExactConeEncoding:
    """Exact full-triple dependency encoding; all six inputs use time t-1."""
    def __init__(self, solver, initial, coupling, remainder_variables, forward, needed, prefix="on"):
        self.solver, self.initial, self.coupling = solver,initial,coupling
        self.remainders, self.forward, self.needed = remainder_variables,forward,needed
        self.prefix, self.states, self.updates = prefix,{},0

    def initial_value(self, address):
        z3 = require_z3()
        a,b,r = self.initial.at(address)
        return z3.IntVal(a),z3.IntVal(b),self.remainders.get(address,z3.IntVal(r))

    def state(self,t,address):
        address=tuple(address)
        if t==0 or address not in self.forward[t]:
            return self.initial_value(address)
        if address not in self.needed[t]:
            raise AssertionError("An actual dependency is missing from the exact encoding")
        return self.states[(t,address)]

    def build(self):
        z3=require_z3()
        cube=self.initial.cube
        for t in range(1,len(self.needed)):
            for address in sorted(self.needed[t]):
                old=self.state(t-1,address)
                incoming=z3.Sum([self.coupling.weights[d][address[3]] *
                    self.state(t-1,cube.adjacent(address,d,self.coupling.ports[d][address[3]]))[1]
                    for d in range(6)])
                name=self.prefix+"_"+str(t)+"_"+"_".join(map(str,address))
                self.states[(t,address)]=add_rule3_constraints(self.solver,old,incoming,name)
                self.updates+=1
        return self


def build_query(protocol, preflight_result=None):
    z3=require_z3()
    prepared,absent,forward,needed,details=preflight_result or preflight(protocol)
    solver=z3.SolverFor("QF_LIA")
    solver.set(random_seed=protocol["solver"]["random_seed"])
    variables={tuple(a):z3.Int("initial_r_"+"_".join(map(str,a))) for a in protocol["unknown_remainder_addresses"]}
    for value in variables.values():
        solver.add(z3.Or(*[value==r for r in protocol["allowed_remainders"]]))
    encoding=ExactConeEncoding(solver,prepared.initial,prepared.engine.coupling,variables,forward,needed).build()
    low,high=protocol["pending_states"]
    for t in range(protocol["steps"]+1):
        for g in range(48):
            address=(*protocol["receiver"],g)
            a,b,r=encoding.state(t,address)
            solver.add(a==0,b==0)
            if low<=t<=high:
                target=protocol["pending_pair"][(0,14).index(g)] if g in (0,14) else 2
                solver.add(r==target)
            if t:
                old=encoding.state(t-1,address)
                ell=b+old[0]
                changed=z3.Or(old[0]!=a,old[1]!=b,old[2]!=r)
                solver.add(z3.Not(z3.And(ell!=0,changed)))
    # Shared-apparatus absent trajectory: exact static solution at every site.
    # The source-off premise was checked globally during preflight. No unknown
    # initial remainder is removed. The static-board theorem holds for every
    # assignment to the same apparatus variables; the observed absent receiver
    # itself is fixed, so its reduced constraints below contain only constants.
    for t in range(protocol["steps"]+1):
        for g in range(48):
            address=(*protocol["receiver"],g)
            a,b,r=absent.initial.at(address)
            expected=protocol["ready_pair"][(0,14).index(g)] if g in (0,14) else 2
            solver.add(z3.IntVal(a)==0,z3.IntVal(b)==0,z3.IntVal(r)==expected)
    if encoding.updates!=details["encoded_channel_updates"]:
        raise AssertionError("Preflight and encoding transition counts differ")
    return solver,variables,encoding,details


def assess_record(protocol,experiment,trace,present):
    events=[]
    for t in range(1,len(trace)):
        for g,(old,new) in enumerate(zip(trace[t-1],trace[t])):
            ell=new[1]+old[0]
            if ell and old!=new:
                events.append({"step":t,"channel":g,"ell":ell})
    target=[[0,0,2] for _ in range(48)]
    for g,r in zip((0,14),protocol["pending_pair"]):target[g][2]=r
    ready=[[0,0,2] for _ in range(48)]
    for g,r in zip((0,14),protocol["ready_pair"]):ready[g][2]=r
    quiet=all(all(a==b==0 for a,b,r in state) for state in trace)
    low,high=protocol["pending_states"]
    stationary=len({f["state_sha256"] for f in experiment["frames"]})==1
    checks={"initial_receiver_ready":trace[0]==ready,"full48_zero_counters":quiet,"no_receiver_C":not events,
            "source_condition":all(state==target for state in trace[low:high+1]) if present else stationary and all(state==ready for state in trace)}
    return {"checks":checks,"accepted":all(checks.values()),"receiver_C":events,"stationary_full_board":stationary}


def independent_replay(spec,experiment):
    expected=matrix_audit.from_state(assemble(spec).initial)
    signs=tuple(spec["board"]["body_signs"])
    steps=0
    for t,frame in enumerate(experiment["frames"]):
        actual=matrix_audit.Snapshot(experiment["side"],tuple(map(int,experiment["background"])),
            {tuple(row[:4]):tuple(map(int,row[4:])) for row in frame["cells"]})
        if t:
            prior=expected
            expected=matrix_audit.advance(prior,signs)
            if expected!=actual or matrix_audit.rewind(actual,signs)!=prior:
                raise AssertionError("Independent matrix replay mismatch")
            steps+=1
        elif actual!=expected:
            raise AssertionError("Independent initial-state reconstruction mismatch")
    return {"all_full_states_equal":True,"independent_forward_inverse_steps":steps,
            "oracle":"research.component_review.audit, exact matrix-derived routing"}


def record_witness(protocol,values,output):
    records,experiments=[],[]
    (output/"records").mkdir()
    for present in (True,False):
        spec=spec_for(protocol,values,present)
        outcome=run_experiment(spec)
        experiment=outcome["experiment"]
        trace=local_trace(experiment,protocol["receiver"])
        assessment=assess_record(protocol,experiment,trace,present)
        replay=independent_replay(spec,experiment)
        if not assessment["accepted"]:
            raise AssertionError("A solver witness failed the predeclared full-engine observer")
        item={"spec":spec,"assembly":outcome["assembly"],"experiment":experiment,"detector_trace":trace,
              "detector_input_trace":[r["next_input"] for r in outcome["observations"]["receiver.node"]["trace"]],
              "detector_observations":outcome["observations"],"assessment":assessment,"matrix_replay":replay}
        path=output/"records"/(spec["id"]+".json.gz")
        path.write_bytes(gzip.compress(canonical(item).encode(),mtime=0))
        records.append({"id":spec["id"],"record":str(path.relative_to(output)),"record_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                        "assessment":assessment,"matrix_replay":replay,"full_rewind_equal":experiment["provenance"]["full_rewind_equal"]})
        experiments.append(experiment)
    write_bundle(output/"experiments.json",bundle(experiments,title="Staged blocks: exact synthesized pending interface"))
    return records


def source_hashes():
    files=[Path(__file__)]
    for folder in ("universe24","research/components","research/experiments","research/presenter","research/reference"):
        files.extend((ROOT/folder).rglob("*.py"))
    files.extend([ROOT/"research/light_approval/compute.py",ROOT/"research/component_review/audit.py"])
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}


def worker(protocol,output):
    # A separate process limits the optional solver without modifying the
    # integrator process or the reference engine's runtime environment.
    cpu_limit=protocol["budget"]["max_cpu_seconds"]
    memory=protocol["budget"]["max_memory_bytes"]
    resource.setrlimit(resource.RLIMIT_CPU,(cpu_limit,cpu_limit))
    resource.setrlimit(resource.RLIMIT_AS,(memory,memory))
    started,cpu=time.monotonic(),time.process_time()
    result={"format":"universe24-staged-synthesis-result-v1","pilot":"A","records":[],"accepted":False,
            "scope":"Only the frozen22-remainder apparatus family, fixed complete tensor, source and horizon12",
            "physical_light_or_approval_established":False}
    try:
        z3=require_z3()
        z3.set_param(proof=True)
        checked=preflight(protocol)
        write_json(output/"preflight.json",checked[-1])
        solver,variables,encoding,details=build_query(protocol,checked)
        query=solver.to_smt2()
        query_path=output/"query.smt2.gz"
        query_path.write_bytes(gzip.compress(query.encode(),mtime=0))
        remaining=max(1,int(1000*(cpu_limit-time.process_time()-5)))
        solver.set(timeout=remaining)
        answer=solver.check()
        solver_info={"answer":str(answer),"version":z3.get_version_string(),"query_sha256":hashlib.sha256(query_path.read_bytes()).hexdigest(),
                     "encoded_channel_updates":encoding.updates,"statistics":str(solver.statistics())}
        write_json(output/"solver_result.json",solver_info)
        if answer==z3.sat:
            model=solver.model()
            values=[model.eval(variables[tuple(a)],model_completion=True).as_long() for a in protocol["unknown_remainder_addresses"]]
            write_json(output/"witness.json",{"addresses":protocol["unknown_remainder_addresses"],"remainders":values,
                      "initial_receiver_ready_pair":protocol["ready_pair"],"generated_by":"offline exact integer synthesis"})
            result["records"]=record_witness(protocol,values,output)
            result.update(status="sat_verified",accepted=True,remainder_values=values)
        elif answer==z3.unsat:
            proof_path=output/"solver_proof.txt.gz"
            proof_path.write_bytes(gzip.compress(str(solver.proof()).encode(),mtime=0))
            result.update(status="unsat_bounded",proof=str(proof_path.relative_to(output)),
                          proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
                          independent_proof_check=False,
                          finding="No apparatus in the registered finite family meets the unchanged Pilot A predicate within12 updates")
        else:
            result.update(status="inconclusive_solver",reason=solver.reason_unknown())
    except (EncodingLimit,MemoryError) as exc:
        result.update(status="inconclusive_resource",reason=str(exc))
    except AssertionError as exc:
        result.update(status="invalid_witness",reason=str(exc))
    except Exception as exc:
        result.update(status="inconclusive_solver",reason=type(exc).__name__+": "+str(exc))
    result.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
                  peak_resident_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    write_json(output/"result.json",result)
    return result


def run_synthesis(output,protocol_path=None):
    """Freeze metadata, run one resource-limited solver process, retain outcome."""
    path=Path(protocol_path or DEFAULT_PROTOCOL).resolve()
    output=Path(output).resolve()
    raw=path.read_bytes()
    protocol=json.loads(raw)
    validate_protocol(protocol)
    output.mkdir(parents=True,exist_ok=False)
    (output/"protocol.json").write_bytes(raw)
    sources=source_hashes()
    z3=require_z3()
    registration={"protocol_sha256":hashlib.sha256(raw).hexdigest(),"source_sha256":sources,
                  "base_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
                  "solver_version":z3.get_version_string(),"solver_package_version":importlib.metadata.version("z3-solver"),
                  "source_controls":[True,False],"random_seed":protocol["solver"]["random_seed"],
                  "initial_choice_seed":None,"search_method":"Exact QF_LIA satisfiability; no randomized initial sampling",
                  "frozen_before_solver_process":True}
    write_json(output/"registration.json",registration)
    command=[sys.executable,"-m","research.staged_blocks.synthesis","--worker","--protocol",str(path),"--output",str(output)]
    try:
        completed=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=protocol["budget"]["max_wall_seconds"])
        (output/"worker.stdout.txt").write_text(completed.stdout)
        (output/"worker.stderr.txt").write_text(completed.stderr)
        if not (output/"result.json").exists():
            write_json(output/"result.json",{"format":"universe24-staged-synthesis-result-v1","pilot":"A","status":"inconclusive_resource",
                       "accepted":False,"records":[],"reason":"Resource-limited worker terminated before a result","worker_returncode":completed.returncode})
    except subprocess.TimeoutExpired:
        write_json(output/"result.json",{"format":"universe24-staged-synthesis-result-v1","pilot":"A","status":"inconclusive_resource",
                   "accepted":False,"records":[],"reason":"Registered wall-time limit reached"})
    result=json.loads((output/"result.json").read_text())
    result["protocol_sha256"]=registration["protocol_sha256"]
    result["sources_unchanged"]=source_hashes()==sources and path.read_bytes()==raw
    if not result["sources_unchanged"]:
        result.update(status="invalid_witness",accepted=False,reason="Registered sources changed during the search")
    total_bytes=sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
    result["evidence_bytes_before_final_summary"]=total_bytes
    if total_bytes>protocol["budget"]["max_output_bytes"]:
        result.update(status="inconclusive_resource",accepted=False,reason="Registered evidence size limit exceeded")
    write_json(output/"result.json",result)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,default=DEFAULT_PROTOCOL)
    parser.add_argument("--worker",action="store_true",help=argparse.SUPPRESS)
    args=parser.parse_args(argv)
    if args.worker:
        result=worker(json.loads(args.protocol.read_text()),args.output)
    else:
        result=run_synthesis(args.output,args.protocol)
    print(canonical({k:v for k,v in result.items() if k!="records"}))


if __name__=="__main__":
    main()
