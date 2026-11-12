"""Reversible local preference changes actual transported carrier structure.

The three Boolean channels are a source-only native control, not a mapping of
the non-Boolean Einstein carrier. The generic bridge lives in clocks.py.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import math
from pathlib import Path
import random

import numpy as np

from universe24.core import Engine, exact_json
from universe24.core.lattice import DIRECTIONS, lattice
from universe24.system.bundle import create_bundle, tensor_from_data, state_from_data, load_bundle
from universe24.system.decoder import default_protocol, decode_transition, make_transition
from universe24.system.runtime import run_bundle, verify_run


def sorting_collision(m, x, y):
    """Compute local inversion into reversible memory, then route carriers."""
    if any(type(v) is not int or v not in (0, 1) for v in (m, x, y)):
        raise ValueError("sorting gate is defined only on exact Boolean triples")
    inversion = y * (1-x)
    memory = m + inversion - 2*m*inversion
    return memory, x + memory*(y-x), y + memory*(x-y)


SORT_GATE = tuple(sorting_collision(*bits) for bits in itertools.product(range(2), repeat=3))
IDENTITY_GATE = tuple(itertools.product(range(2), repeat=3))
PROTOCOL = {
    "schema": "universe24/native-local-preference/1",
    "preregistration": "https://github.com/Closer24/Universe24/issues/45#issuecomment-6810761836",
    "channel_order": ["memory", "carrier_x", "carrier_y"],
    "local_feature": "y*(1-x), computed from the actual Boolean carrier lanes",
    "ready_domain": "all current m=0; a=F^-1(b), not a zeroed or discarded history",
    "steps": 24,
    "heldout_seeds": [101, 509, 2027],
    "sides": [3, 5],
    "directions": [list(d) for d in DIRECTIONS],
    "structural_score": "distinct nonuniform axial carrier triples repeated at >=2 sites and unchanged at those sites for two adjacent checkpoints",
    "episode": "strict interior local maximum of complete memory-channel arithmetic-event count, count>=1",
    "growth_gate": "at least four episodes and strictly increasing current structural score at each successive episode",
    "external_runtime_selection": False,
}


def axial_motifs(values, side, direction):
    """Current carrier geometry only; magnitude/time/memory are not the score."""
    grid = lattice(side)
    neg = grid.shift_index(tuple(-d for d in direction))
    pos = grid.shift_index(direction)
    x, y = values[1], values[2]
    if any(not isinstance(v,(int,np.integer)) or isinstance(v,(bool,np.bool_))
           or int(v) not in (0,1) for row in (x,y) for v in row):
        raise ValueError("out-of-domain amplitudes are not Boolean structural evidence")
    labels = [(int(x[n]), int(y[n])) for n in range(grid.N)]
    return tuple((labels[int(neg[n])], labels[n], labels[int(pos[n])]) for n in range(grid.N))


def structure_trace(values_by_step, side, direction):
    motifs = [axial_motifs(v, side, direction) for v in values_by_step]
    rows = [{"score": 0, "persistent_sites": 0}]
    for before, after in zip(motifs, motifs[1:]):
        counts = Counter(m for old, m in zip(before, after) if old == m and len(set(m)) > 1)
        repeated = {motif: count for motif, count in counts.items() if count >= 2}
        rows.append({"score": len(repeated), "persistent_sites": sum(repeated.values())})
    return rows


def episode_gate(structure, counts):
    if len(structure) != len(counts)+1:
        raise ValueError("complete seed plus every event window is required")
    peaks = [i+1 for i in range(1, len(counts)-1)
             if counts[i] > 0 and counts[i] > counts[i-1] and counts[i] > counts[i+1]]
    scores = [structure[p]["score"] for p in peaks]
    enough = len(peaks) >= 4
    growth = enough and all(b > a for a, b in zip(scores, scores[1:]))
    return {"episode_steps": peaks, "scores_at_episodes": scores,
            "at_least_four": enough, "strict_growth": growth,
            "status": "passed" if growth else "failed" if enough else "blocked"}


def _bridge():
    from validation.selection.clocks import build_native_gate, first_order, prepare_gate
    return build_native_gate, first_order, prepare_gate


def _current(side, seed, *, ready=True):
    rng = random.Random(seed)
    rows = [[rng.randrange(2) for _ in range(side**3)] for _ in range(3)]
    if ready:
        rows[0] = [0] * (side**3)
    return np.asarray(rows, dtype=object)


def _run(side, direction, seed_number, steps, gate=SORT_GATE):
    build, first_order, prepare = _bridge()
    law = build(gate, direction=direction, name="selection")
    current = _current(side, seed_number)
    carries = np.asarray([[(n+g)%6 for n in range(side**3)] for g in range(3)], dtype=object)
    seed = prepare(gate, current, side, direction, remainders=carries)
    engine = Engine(law)
    state = seed
    rows, values, counts, ready_counts, port_inversions = [], [current.copy()], [], [], []
    particle_count = sum(int(v) for v in current[1:].flat)
    for step in range(1, steps+1):
        ready_counts.append(sum(int(v)==0 for v in state.b[0]))
        expected = first_order(state.b, gate, side, direction)
        after = engine.step(state)
        assert np.array_equal(after.b, expected)
        assert np.array_equal(after.r, carries)
        assert engine.inverse_step(after).same_as(state)
        assert all(int(v) in (0, 1) for a in (after.a, after.b) for v in a.flat)
        assert sum(int(v) for v in after.b[1:].flat) == particle_count
        events = decode_transition(make_transition(law, state, after, run_id="native-selection", step=step), law)
        counts.append(sum(e["channel"] == 0 for e in events))
        arrived = after.b[1, lattice(side).shift_index(direction)]
        port_inversions.append(sum(int(y)*(1-int(x)) for x,y in zip(arrived,after.b[2])))
        if step == 1:
            # Undo only the declared transport to inspect each gate's two output
            # ports. This is a diagnostic; no value is fed back into evolution.
            assert np.all(arrived >= after.b[2]) if gate == SORT_GATE else True
            rows.append({"input_inversions": sum(int(y)*(1-int(x)) for x,y in zip(current[1],current[2])),
                         "output_port_inversions": sum(int(y)*(1-int(x)) for x,y in zip(arrived,after.b[2]))})
        values.append(after.b.copy())
        state = after
    assert engine.rewind(state, steps).same_as(seed)
    structure = structure_trace(values, side, direction)
    return {"side": side, "direction": list(direction), "seed": seed_number,
            "tensor_hash": law.fingerprint, "steps": steps, "particles": particle_count,
            "first_collision": rows[0], "scores": [r["score"] for r in structure],
            "ready_memory_sites_by_step": ready_counts, "collision_output_inversions_by_step": port_inversions,
            "memory_event_counts": counts, "growth": episode_gate(structure, counts),
            "complete_rewind": True, "native_oracle_agreement": True,
            "maximum_retained_bits": 3, "boolean_carrier_and_memory": True}, law, seed, values


def history_intervention(side, direction, origin):
    """Same complete carrier a,b,r, differing memory; test genuine feedback."""
    build, _, prepare = _bridge()
    grid = lattice(side)
    current = np.zeros((3, grid.N), dtype=object)
    current[1, int(grid.shift_index(direction)[origin])] = 1
    current[2] = current[1, grid.shift_index(direction)]
    other = current.copy(); other[0, origin] = 1
    answer = {"side": side, "direction": list(direction), "origin": origin}
    for label, gate in (("coupled", SORT_GATE), ("disconnected", IDENTITY_GATE)):
        law = build(gate, direction=direction, name="selection")
        left, right = [prepare(gate, v, side, direction) for v in (current, other)]
        assert all(np.array_equal(getattr(left, f)[1:], getattr(right, f)[1:]) for f in ("a", "b", "r"))
        original_left, original_right = left.copy(), right.copy()
        engine = Engine(law); differences = []
        origin_xyz=grid.coords(origin)
        distances=np.asarray([sum(min(abs(a-b),side-abs(a-b)) for a,b in zip(origin_xyz,grid.coords(n)))
                              for n in range(grid.N)])
        for step in range(1,5):
            left, right = engine.step(left), engine.step(right)
            differences.append(int(np.sum(left.b[1:] != right.b[1:])))
            for field in ("a","b","r"):
                assert np.array_equal(getattr(left,field)[:,distances>step],getattr(right,field)[:,distances>step])
        assert engine.rewind(left, 4).same_as(original_left)
        assert engine.rewind(right, 4).same_as(original_right)
        answer[label+"_carrier_component_differences"] = differences
        answer[label+"_raw"] = {"tensor_hash":law.fingerprint,"steps":4,
                                "initial":[original_left.to_dict(),original_right.to_dict()],
                                "final":[left.to_dict(),right.to_dict()]}
    assert any(answer["coupled_carrier_component_differences"])
    assert not any(answer["disconnected_carrier_component_differences"])
    answer["equal_complete_initial_carrier"] = True
    answer["all_retained_outside_cone_equal"] = True
    return answer


def audit(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    collision_rows = [{"input": list(bits), "output": list(sorting_collision(*bits))}
                      for bits in itertools.product(range(2), repeat=3)]
    assert len(set(SORT_GATE)) == 8
    assert all(sorting_collision(0,x,y)[1] >= sorting_collision(0,x,y)[2]
               for x,y in itertools.product(range(2),repeat=2))
    results=[]; representative=None
    for side in PROTOCOL["sides"]:
        for direction in DIRECTIONS:
            for seed in PROTOCOL["heldout_seeds"]:
                result, law, initial, values = _run(side,direction,seed,PROTOCOL["steps"])
                control, _, _, _ = _run(side,direction,seed,PROTOCOL["steps"],IDENTITY_GATE)
                result["disconnected_growth"] = control["growth"]
                result["disconnected_scores"] = control["scores"]
                results.append(result)
                if representative is None:
                    representative=(law,initial,values)
    interventions=[history_intervention(side,direction,origin)
                   for side in PROTOCOL["sides"] for direction in DIRECTIONS for origin in (0,side**3-1)]
    law,initial,values=representative
    channels=[{"index":i,"name":gear.name,"owner":"native_carrier_and_provenance", "label":gear.label,
               "purpose":"Boolean reversible sorting/routing control, no Einstein-source identification"}
              for i,gear in enumerate(law.gears)]
    bundle=create_bundle(law,initial,channels=channels,protocol=default_protocol(),
                         model={"id":"native-selection-control","version":"1",
                                "domain":"Proved Boolean F+inverse sector; 3 retained channels, no physical45 equivalence"})
    saved=run_bundle(bundle,out/"representative-run",steps=PROTOCOL["steps"])
    # Frozen/periodic/random proxy counterexamples remain explicit, not removed
    # when they receive an inconvenient score.
    rng=random.Random(9331)
    fresh=[np.asarray([[0]*125]+[[rng.randrange(2) for _ in range(125)] for _ in range(2)],dtype=object) for _ in range(25)]
    frozen=[fresh[0]]*25
    random_scores=[s["score"] for s in structure_trace(fresh,5,DIRECTIONS[0])]
    frozen_scores=[s["score"] for s in structure_trace(frozen,5,DIRECTIONS[0])]
    constant_growth=episode_gate(structure_trace(frozen,5,DIRECTIONS[0]),[0,1,0]*8)
    assert constant_growth["at_least_four"] and not constant_growth["strict_growth"]
    report={"protocol":PROTOCOL,"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "bridge_source_sha256":hashlib.sha256(Path(__file__).with_name("clocks.py").read_bytes()).hexdigest(),
            "collision_table":collision_rows,"native_runs":results,"history_interventions":interventions,
            "saved_run":saved,"random_scores":random_scores,"frozen_random_scores":frozen_scores,
            "periodic_growth_control":constant_growth,
            "positive_results":{"ready_memory_sorting":True,"retained_history_changes_carrier":True,
                                "no_history_control_removes_response":True,"exact_replay":True},
            "growth_passes":sum(r["growth"]["strict_growth"] for r in results),
            "growth_failures":sum(r["growth"]["status"]=="failed" for r in results),
            "growth_blocked":sum(r["growth"]["status"]=="blocked" for r in results),
            "scope":{"physical45_integration":"not_implemented","Born":"not_derived",
                     "physical_bursts":"not_identified","indefinite_monotonic_growth":"impossible_on_finite_Boolean_board",
                     "previous_PR43_growth_failures":"unchanged, not rerun"}}
    (out/"complexity.json").write_text(exact_json.dumps(report,sort_keys=True)+"\n")
    return report


def projective_phase_relations(state, tensor):
    """Amplitude-independent exact phase directions; not a click-only reader."""
    phi, chi, denominator = [tensor.gear_index(name) for name in
                             ("projective.phi","projective.chi","projective.denominator")]
    def sign(x): return (x>0)-(x<0)
    coarse, precise = [], []
    for n in range(state.N):
        for direction in range(6):
            j=state.lattice.neighbour(n,direction)
            px,py=int(state.b[phi,n]),int(state.b[chi,n])
            qx,qy=int(state.b[phi,j]),int(state.b[chi,j])
            den=int(state.b[denominator,n])*int(state.b[denominator,j])
            if den==0: raise ValueError("current projective phase denominator must be nonzero")
            dot=(px*qx+py*qy)*sign(den)
            cross=(px*qy-py*qx)*sign(den)
            divisor=math.gcd(dot,cross)
            precise.append((dot//divisor,cross//divisor) if divisor else (0,0))
            coarse.append((sign(dot),sign(cross)))
    return coarse,precise


def audit_physical_response(raw_source, out):
    """Replay independently exported47-field controls, then compare phases."""
    raw_source=Path(raw_source); out=Path(out); out.mkdir(parents=True,exist_ok=True)
    with gzip.open(raw_source,"rt",encoding="utf-8") as stream:
        raw=exact_json.loads(stream.read())
    by_name={case["name"]:case for case in raw}
    if len(by_name)!=len(raw): raise ValueError("duplicate source case")
    rows=[]
    for coupling in ("connected","disconnected"):
        names=[coupling+"-texture-+1",coupling+"-texture--1"]
        left,right=[by_name[name] for name in names]
        tensors=[tensor_from_data(case["tensor"]) for case in (left,right)]
        if tensors[0].fingerprint!=tensors[1].fingerprint: raise ValueError("matched pair law differs")
        tensor=tensors[0]
        histories=[]
        for case in (left,right):
            states=[state_from_data(state) for state in case["states"]]
            seed=state_from_data(case["seed"])
            if not seed.same_as(states[0]): raise ValueError("complete source seed mismatch")
            engine=Engine(tensor)
            for before,after in zip(states,states[1:]):
                if not engine.step(before).same_as(after): raise ValueError("source trace replay mismatch")
                if not engine.inverse_step(after).same_as(before): raise ValueError("source trace inverse mismatch")
            if not engine.rewind(states[-1],len(states)-1).same_as(seed): raise ValueError("source rewind mismatch")
            histories.append(states)
        if len(histories[0])!=len(histories[1]): raise ValueError("window count mismatch")
        carrier=[tensor.gear_index(name) for name in ("projective.phi","projective.chi")]
        assert all(np.array_equal(getattr(histories[0][0],field)[carrier],getattr(histories[1][0],field)[carrier])
                   for field in ("a","b","r"))
        steps=[]
        for index,(a,b) in enumerate(zip(*histories)):
            ac,ap=projective_phase_relations(a,tensor);bc,bp=projective_phase_relations(b,tensor)
            steps.append({"step":index,
                          "raw_carrier_component_differences":int(np.sum(a.b[carrier]!=b.b[carrier])),
                          "coarse_phase_link_differences":sum(x!=y for x,y in zip(ac,bc)),
                          "exact_phase_link_direction_differences":sum(x!=y for x,y in zip(ap,bp))})
        if coupling=="disconnected": assert all(s["exact_phase_link_direction_differences"]==0 for s in steps)
        rows.append({"coupling":coupling,"tensor_hash":tensor.fingerprint,"channels":tensor.G,
                     "same_complete_initial_phi_chi":True,"full_replay_and_rewind":True,"steps":steps})
    report={"schema":"universe24/physical-source-phase-response/1",
            "preregistration":"https://github.com/Closer24/Universe24/issues/45#issuecomment-6810892674",
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "raw_source_sha256":hashlib.sha256(raw_source.read_bytes()).hexdigest(),"pairs":rows,
            "coarse_metric_scope":"predeclared phase sign bins; no physical proper-clock claim",
            "exact_metric_scope":"supplementary primitive integer(dot,cross) corrected for denominator signs; amplitude-independent phase response",
            "limitations":["47-field source run, not the3-bit native sorter and not a48-pointer integration test",
                           "No higher-complexity preference, sustained growth, source-constraint or clock calibration is established",
                           "These phase readouts use saved hidden states and are not click-only measurements"]}
    (out/"physical-phase-response.json").write_text(exact_json.dumps(report,sort_keys=True)+"\n")
    return report


def audit_pointer_response(reference_run, history_run, out):
    """Same48-law pointer-history response, read from verified saved traces."""
    paths=list(map(Path,(reference_run,history_run)))
    reports=[verify_run(path) for path in paths]
    bundles=[load_bundle(path/"bundle") for path in paths]
    if bundles[0].tensor.fingerprint!=bundles[1].tensor.fingerprint:
        raise ValueError("pointer history comparison requires exactly the same tensor")
    tensor=bundles[0].tensor
    if tensor.G!=48:raise ValueError("this pointer protocol requires48 retained channels")
    histories=[]
    for path,bundle in zip(paths,bundles):
        states=[bundle.seed]
        with gzip.open(path/"full_trace.jsonl.gz","rt",encoding="utf-8") as stream:
            states.extend(state_from_data(exact_json.loads(line)["after"]) for line in stream)
        histories.append(states)
    if len(histories[0])!=len(histories[1]):raise ValueError("pointer windows differ")
    assert all(np.array_equal(getattr(histories[0][0],field)[:47],getattr(histories[1][0],field)[:47])
               for field in ("a","b","r"))
    carrier=[tensor.gear_index(name) for name in ("projective.phi","projective.chi")]
    steps=[]
    for index,(a,b) in enumerate(zip(*histories)):
        ac,ap=projective_phase_relations(a,tensor);bc,bp=projective_phase_relations(b,tensor)
        steps.append({"step":index,"raw_carrier_component_differences":int(np.sum(a.b[carrier]!=b.b[carrier])),
                      "coarse_phase_link_differences":sum(x!=y for x,y in zip(ac,bc)),
                      "exact_phase_link_direction_differences":sum(x!=y for x,y in zip(ap,bp))})
    report={"schema":"universe24/pointer-phase-response/1","tensor_hash":tensor.fingerprint,
            "bundle_ids":[bundle.bundle_id for bundle in bundles],"run_ids":[r["run_id"] for r in reports],
            "channels":48,"same_complete_initial_original47":True,"saved_replay_and_rewind":True,
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"steps":steps,
            "predeclared_steps":4,"fifth_step_if_present":"explicit exploratory extension, never pooled into four-step physical gate",
            "scope":"raw retained-pointer feedback; reciprocal geometry stress and physical calibration are not established",
            "growth_status":"not_tested; phase response is not preference for higher complexity"}
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/"pointer-phase-response.json").write_text(exact_json.dumps(report,sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=Path("runs/selection/complexity"))
    parser.add_argument("--physical-source",type=Path)
    args=parser.parse_args(argv)
    if args.physical_source:
        result=audit_physical_response(args.physical_source,args.out)
        print(exact_json.dumps(result["pairs"]))
    else:
        result=audit(args.out)
        print(exact_json.dumps({k:result[k] for k in ("positive_results","growth_passes","growth_failures","growth_blocked")}))


if __name__=="__main__":
    main()
