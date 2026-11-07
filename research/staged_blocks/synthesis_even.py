"""Equivalent even-remainder encoding of frozen Pilot A; original files unchanged.

This is an offline solver optimization, not an alternative evolution rule.
For this family's all-even initial remainders, r=2*s is a bijective change
of variables: 6*ell+r_next=2*u+r iff 3*ell+s_next=u+s, with s in0..2.
The physical initial state and every recorded runtime state still use r.
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

from research.staged_blocks import synthesis as base

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DEFAULT_PROTOCOL=HERE/"synthesis_protocol_a_even.json"


def validate_equivalent_family(protocol):
    original=json.loads(base.DEFAULT_PROTOCOL.read_text())
    omitted={"id","status","encoding","equivalent_to"}
    if {k:v for k,v in protocol.items() if k not in omitted}!={k:v for k,v in original.items() if k not in omitted}:
        raise ValueError("The equivalent encoding must preserve the complete original physical family and observer")
    expected=hashlib.sha256(base.DEFAULT_PROTOCOL.read_bytes()).hexdigest()
    if protocol["equivalent_to"]["original_protocol_sha256"]!=expected:
        raise ValueError("Original frozen protocol hash mismatch")
    base.validate_protocol(protocol)
    return original


def add_even_rule3_constraints(solver,old,incoming,name):
    z3=base.require_z3()
    next_b,next_s=z3.Int(name+"_b"),z3.Int(name+"_s")
    solver.add(3*(next_b+old[0])+next_s==incoming+old[2],next_s>=0,next_s<3)
    return old[1],next_b,next_s


class EvenConeEncoding(base.ExactConeEncoding):
    """Only internal symbolic remainder coordinates change; physical r=2*s."""
    def initial_value(self,address):
        z3=base.require_z3()
        a,b,r=self.initial.at(address)
        if r%2:
            raise ValueError("Parity elimination is restricted to all-even initial remainders")
        return z3.IntVal(a),z3.IntVal(b),self.remainders.get(address,z3.IntVal(r//2))

    def physical_state(self,t,address):
        a,b,s=self.state(t,address)
        return a,b,2*s

    def build(self):
        z3=base.require_z3()
        cube=self.initial.cube
        for t in range(1,len(self.needed)):
            for address in sorted(self.needed[t]):
                old=self.state(t-1,address)
                incoming=z3.Sum([self.coupling.weights[d][address[3]]*
                    self.state(t-1,cube.adjacent(address,d,self.coupling.ports[d][address[3]]))[1]
                    for d in range(6)])
                name=self.prefix+"_"+str(t)+"_"+"_".join(map(str,address))
                self.states[(t,address)]=add_even_rule3_constraints(self.solver,old,incoming,name)
                self.updates+=1
        return self


def build_query(protocol,preflight_result=None):
    validate_equivalent_family(protocol)
    z3=base.require_z3()
    prepared,absent,forward,needed,details=preflight_result or base.preflight(protocol)
    if any(v.r%2 for v in prepared.initial.cells.values()) or prepared.initial.background.r%2:
        raise ValueError("A physical initial remainder is odd")
    solver=z3.SolverFor("QF_LIA")
    solver.set(random_seed=protocol["solver"]["random_seed"])
    variables={tuple(a):z3.Int("initial_s_"+"_".join(map(str,a))) for a in protocol["unknown_remainder_addresses"]}
    for value in variables.values():solver.add(value>=0,value<=2)
    encoding=EvenConeEncoding(solver,prepared.initial,prepared.engine.coupling,variables,forward,needed).build()
    low,high=protocol["pending_states"]
    for t in range(protocol["steps"]+1):
        for g in range(48):
            address=(*protocol["receiver"],g)
            a,b,r=encoding.physical_state(t,address)
            solver.add(a==0,b==0)
            if low<=t<=high:
                target=protocol["pending_pair"][(0,14).index(g)] if g in (0,14) else 2
                solver.add(r==target)
            if t:
                old=encoding.physical_state(t-1,address)
                solver.add(z3.Not(z3.And(b+old[0]!=0,z3.Or(old[0]!=a,old[1]!=b,old[2]!=r))))
    for t in range(protocol["steps"]+1):
        for g in range(48):
            a,b,r=absent.initial.at((*protocol["receiver"],g))
            target=protocol["ready_pair"][(0,14).index(g)] if g in (0,14) else 2
            solver.add(z3.IntVal(a)==0,z3.IntVal(b)==0,z3.IntVal(r)==target)
    if encoding.updates!=details["encoded_channel_updates"]:
        raise AssertionError("Equivalent encoding omitted a registered dependency")
    return solver,variables,encoding,details


def source_hashes():
    values=base.source_hashes()
    values[str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return values


def worker(protocol,output):
    cpu_limit=protocol["budget"]["max_cpu_seconds"]
    memory=protocol["budget"]["max_memory_bytes"]
    resource.setrlimit(resource.RLIMIT_CPU,(cpu_limit,cpu_limit))
    resource.setrlimit(resource.RLIMIT_AS,(memory,memory))
    started,cpu=time.monotonic(),time.process_time()
    result={"format":"universe24-staged-synthesis-result-v1","pilot":"A","encoding":"even-remainder-bijection",
            "records":[],"accepted":False,"scope":"Exactly the same physical family and observer as the original Pilot A",
            "physical_light_or_approval_established":False}
    try:
        validate_equivalent_family(protocol)
        z3=base.require_z3()
        z3.set_param(proof=True)
        checked=base.preflight(protocol)
        base.write_json(output/"preflight.json",checked[-1])
        solver,variables,encoding,details=build_query(protocol,checked)
        query_path=output/"query.smt2.gz"
        query_path.write_bytes(gzip.compress(solver.to_smt2().encode(),mtime=0))
        solver.set(timeout=max(1,int(1000*(cpu_limit-time.process_time()-5))))
        answer=solver.check()
        base.write_json(output/"solver_result.json",{"answer":str(answer),"version":z3.get_version_string(),
            "query_sha256":hashlib.sha256(query_path.read_bytes()).hexdigest(),
            "encoded_channel_updates":encoding.updates,"statistics":str(solver.statistics())})
        if answer==z3.sat:
            model=solver.model()
            scaled=[model.eval(variables[tuple(a)],model_completion=True).as_long() for a in protocol["unknown_remainder_addresses"]]
            physical=[2*s for s in scaled]
            base.write_json(output/"witness.json",{"addresses":protocol["unknown_remainder_addresses"],
                "internal_s_values":scaled,"remainders":physical,"physical_relation":"r=2*s",
                "initial_receiver_ready_pair":protocol["ready_pair"],"generated_by":"offline exact integer synthesis"})
            result["records"]=base.record_witness(protocol,physical,output)
            result.update(status="sat_verified",accepted=True,remainder_values=physical)
        elif answer==z3.unsat:
            proof=output/"solver_proof.txt.gz"
            proof.write_bytes(gzip.compress(str(solver.proof()).encode(),mtime=0))
            result.update(status="unsat_bounded",proof=proof.name,proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),
                independent_proof_check=False,finding="No assignment in the unchanged registered Pilot A physical family meets its fixed quiet predicate")
        else:
            result.update(status="inconclusive_solver",reason=solver.reason_unknown())
    except (base.EncodingLimit,MemoryError) as exc:
        result.update(status="inconclusive_resource",reason=str(exc))
    except AssertionError as exc:
        result.update(status="invalid_witness",reason=str(exc))
    except Exception as exc:
        result.update(status="inconclusive_solver",reason=type(exc).__name__+": "+str(exc))
    result.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
                  peak_resident_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
    base.write_json(output/"result.json",result)
    return result


def run_synthesis(output,protocol_path=None):
    path=Path(protocol_path or DEFAULT_PROTOCOL).resolve()
    output=Path(output).resolve()
    raw=path.read_bytes();p=json.loads(raw)
    validate_equivalent_family(p)
    output.mkdir(parents=True,exist_ok=False)
    (output/"protocol.json").write_bytes(raw)
    sources=source_hashes();z3=base.require_z3()
    registration={"protocol_sha256":hashlib.sha256(raw).hexdigest(),"source_sha256":sources,
        "base_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "solver_version":z3.get_version_string(),"solver_package_version":importlib.metadata.version("z3-solver"),
        "source_controls":[True,False],"random_seed":p["solver"]["random_seed"],"initial_choice_seed":None,
        "search_method":"Exact QF_LIA with the bijective even-remainder coordinate s=r/2",
        "original_protocol_sha256":p["equivalent_to"]["original_protocol_sha256"],"frozen_before_solver_process":True}
    base.write_json(output/"registration.json",registration)
    command=[sys.executable,"-m","research.staged_blocks.synthesis_even","--worker","--protocol",str(path),"--output",str(output)]
    try:
        done=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=p["budget"]["max_wall_seconds"])
        (output/"worker.stdout.txt").write_text(done.stdout)
        (output/"worker.stderr.txt").write_text(done.stderr)
        if not (output/"result.json").exists():
            base.write_json(output/"result.json",{"format":"universe24-staged-synthesis-result-v1","pilot":"A",
                "encoding":"even-remainder-bijection","status":"inconclusive_resource","accepted":False,"records":[],
                "reason":"Resource-limited worker terminated before a result","worker_returncode":done.returncode})
    except subprocess.TimeoutExpired:
        base.write_json(output/"result.json",{"format":"universe24-staged-synthesis-result-v1","pilot":"A",
            "encoding":"even-remainder-bijection","status":"inconclusive_resource","accepted":False,"records":[],
            "reason":"Registered wall-time limit reached"})
    result=json.loads((output/"result.json").read_text())
    result["protocol_sha256"]=registration["protocol_sha256"]
    result["sources_unchanged"]=source_hashes()==sources and path.read_bytes()==raw
    if not result["sources_unchanged"]:result.update(status="invalid_witness",accepted=False,reason="Registered sources changed during the search")
    total=sum(f.stat().st_size for f in output.rglob("*") if f.is_file())
    result["evidence_bytes_before_final_summary"]=total
    if total>p["budget"]["max_output_bytes"]:result.update(status="inconclusive_resource",accepted=False,reason="Registered evidence size limit exceeded")
    base.write_json(output/"result.json",result)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--protocol",type=Path,default=DEFAULT_PROTOCOL)
    parser.add_argument("--worker",action="store_true",help=argparse.SUPPRESS)
    args=parser.parse_args(argv)
    result=worker(json.loads(args.protocol.read_text()),args.output) if args.worker else run_synthesis(args.output,args.protocol)
    print(base.canonical({k:v for k,v in result.items() if k!="records"}))


if __name__=="__main__":main()
