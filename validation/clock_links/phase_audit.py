"""Run the four-record proposal through the supported runtime and falsify claims.

Usage: python -m validation.clock_links.phase_audit --base-bundle PATH --out NEW_DIR
The input is an explicitly saved 44-channel proposal bundle, not a hidden model.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from pathlib import Path

import numpy as np

from universe24.core import Engine, exact_json
from universe24.core.lattice import link_direction
from universe24.system.bundle import (SystemBundle, create_bundle, load_bundle,
                                      state_from_data, tensor_from_data)
from universe24.system.decoder import decode_transition, make_transition
from universe24.system.runtime import run_bundle, verify_run
from validation.clock_links.model import (CARRIER_NAMES, OBSERVER_NAMES,
                                         append_phase_observers, base_projection,
                                         relation_values)


def with_seed(base: SystemBundle, seed, label: str) -> SystemBundle:
    return create_bundle(base.tensor, seed, channels=base.channels,
                         protocol=base.protocol,
                         model={**base.model, "control_preparation": label})


def events(bundle, before, after, step=1):
    return decode_transition(make_transition(bundle.tensor, before, after,
                                              run_id="phase-audit", step=step),
                             bundle.tensor)


def audit(base: SystemBundle, out: str | Path, *, steps=3) -> dict:
    if base.tensor.G != 44:
        raise ValueError("integrated evidence requires the declared 44-channel source")
    if type(steps) is not int or not 1 <= steps <= 6:
        raise ValueError("predeclared finite audit supports one through six updates")
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("fresh audit directory required")
    out.mkdir(parents=True, exist_ok=True)
    appended = append_phase_observers(base)
    full_engine, base_engine = Engine(appended.tensor), Engine(base.tensor)
    full, original = appended.seed, base.seed
    checked, kinds, max_bits = 0, Counter(), []
    for step in range(1, steps+1):
        next_full, next_original = full_engine.step(full), base_engine.step(original)
        assert base_projection(next_full, 44).same_as(next_original)
        expected = relation_values(full, appended.tensor)
        actual = next_full.b[44:].astype(object) + full.a[44:].astype(object)
        assert np.array_equal(actual, expected)
        assert np.array_equal(next_full.r[44:], full.r[44:])
        checked += expected.size
        for record in events(appended, full, next_full, step):
            if record["channel"] >= 44:
                kinds[record["kind"]] += 1
        max_bits.append(max(abs(int(v)).bit_length() for a in (next_full.a,next_full.b,next_full.r) for v in a.flat))
        full, original = next_full, next_original
    assert full_engine.rewind(full, steps).same_as(appended.seed)
    assert set(kinds) <= {"C0"}

    # Controls use a disclosed changed preparation with all original fields
    # present. They are not asserted to solve continuum Einstein constraints.
    phase_cases = []
    complete_controls = []
    for axis in range(3):
        for origin in (0, base.seed.N-1):
            target = base.seed.lattice.shift_index(link_direction(axis))[origin]
            for other, expected in (((1,0),4),((-1,0),0),((0,1),2)):
                seed = base.seed
                real, imag = (base.tensor.gear_index(n) for n in CARRIER_NAMES)
                seed.b[real,:] = 0; seed.b[imag,:] = 0
                seed.b[real,origin] = 1
                seed.b[real,target],seed.b[imag,target] = other
                control = append_phase_observers(with_seed(base,seed,"local two-site phase control"))
                after = Engine(control.tensor).step(control.seed)
                quotient = int(after.b[45+axis,origin]+control.seed.a[45+axis,origin])
                assert quotient == expected
                phase_cases.append({"axis":axis,"node":origin,"neighbor":int(target),
                                    "neighbor_phase":list(other),"coherent_quotient":quotient})
                complete_controls.append({"kind":"two-site-phase", "steps":1,
                                          "protocol":phase_cases[-1],
                                          "seed":control.seed.to_dict(),"final":after.to_dict()})

    # A common quarter-turn of the complete raw carrier leaves every first-step
    # intensity invariant. A local rotation need not: fixed-gauge limitation.
    seed = base.seed
    real,imag=(base.tensor.gear_index(n) for n in CARRIER_NAMES)
    original_relations=relation_values(seed,base.tensor)
    original_phase_seed=seed.to_dict()
    re,im=seed.b[real,:].copy(),seed.b[imag,:].copy()
    seed.b[real,:],seed.b[imag,:]=-im,re
    assert np.array_equal(original_relations,relation_values(seed,base.tensor))
    quarter_turn_control={"before":original_phase_seed,"after":seed.to_dict(),
                          "role":"Static carrier preparation symmetry, not an evolution step"}

    # Matched apparatus histories: source, tensor, I and carries agree exactly.
    # History can suppress an event when the complete triple is stationary.
    seed=base.seed
    seed.b[real,0]=seed.b[imag,0]=1
    matched=with_seed(base,seed,"matched observer history at local I=2")
    empty=append_phase_observers(matched)
    hist_a=np.zeros((4,seed.N),dtype=object)
    hist_b=hist_a.copy(); hist_a[0,0]=hist_b[0,0]=1
    stationary=append_phase_observers(matched,apparatus_a=hist_a,apparatus_b=hist_b)
    es,ss=empty.seed,stationary.seed
    histories=[]
    for step in range(1,steps+1):
        en,sn=Engine(empty.tensor).step(es),Engine(stationary.tensor).step(ss)
        assert base_projection(en,44).same_as(base_projection(sn,44))
        assert np.array_equal(en.b[44:].astype(object)+es.a[44:].astype(object),
                              sn.b[44:].astype(object)+ss.a[44:].astype(object))
        ec=[r for r in events(empty,es,en,step) if r['channel']==44 and r['node']==0]
        sc=[r for r in events(stationary,ss,sn,step) if r['channel']==44 and r['node']==0]
        histories.append({"step":step,"empty_history_count":len(ec),
                          "stationary_history_count":len(sc),
                          "common_quotient":int(en.b[44,0]+es.a[44,0])})
        es,ss=en,sn
    assert histories[0] == {"step":1,"empty_history_count":1,"stationary_history_count":0,"common_quotient":2}
    assert Engine(empty.tensor).rewind(es,steps).same_as(empty.seed)
    assert Engine(stationary.tensor).rewind(ss,steps).same_as(stationary.seed)
    for label,control,final in (("empty-history",empty,es),("stationary-history",stationary,ss)):
        complete_controls.append({"kind":label,"steps":steps,
                                  "seed":control.seed.to_dict(),"final":final.to_dict()})

    # Every evolved control is independently reproducible from these saved
    # complete inputs. Storing the common tensor once avoids redundant banks.
    controls={"schema":"universe24/validation/clock-links-controls/1",
              "tensor":appended.tensor.to_dict(),"base_bundle_id":base.bundle_id,
              "runs":complete_controls,"quarter_turn_preparation":quarter_turn_control}
    control_path=out/"controls.json.gz"
    control_path.write_bytes(gzip.compress(exact_json.dumps(controls,sort_keys=True).encode(),mtime=0))
    saved=exact_json.loads(gzip.decompress(control_path.read_bytes()))
    saved_engine=Engine(tensor_from_data(saved["tensor"]))
    for case in saved["runs"]:
        initial,final=(state_from_data(case[k]) for k in ("seed","final"))
        assert saved_engine.run(initial,case["steps"]).same_as(final)
        assert saved_engine.rewind(final,case["steps"]).same_as(initial)

    runtime = run_bundle(appended,out/"run",steps=steps)
    verify_run(out/"run")
    report={"schema":"universe24/validation/clock-links/1",
            "base_bundle_id":base.bundle_id,"base_tensor_hash":base.tensor.fingerprint,
            "bundle_id":appended.bundle_id,"tensor_hash":appended.tensor.fingerprint,
            "channels_per_node":48,"retained_integers_per_node":144,
            "base_projection_unchanged":True,"steps":steps,"nodes":base.seed.N,
            "exact_intensity_quotient_comparisons":checked,"apparatus_event_classes":dict(kinds),
            "maximum_integer_bits_by_step":max_bits,
            "coherent_phase_cases":phase_cases,"common_quarter_turn_invariance":True,
            "history_intervention":histories,"complete_rewind":True,
            "saved_control_runs_replayed":len(saved["runs"]),
            "controls_file":"controls.json.gz",
            "controls_sha256":hashlib.sha256(control_path.read_bytes()).hexdigest(),
            "runtime_checks":runtime["checks"],
            "observer_history_changes_source_dynamics":False,
            "observer_history_changes_driving_intensity":False,
            "observer_history_can_change_arithmetic_event_presence":True,
            "physical_gate_status":{
                "shared_metric_proper_clock":"not_tested",
                "apparatus_stress_and_backreaction":"not_supplied",
                "local_gauge_invariant_parallel_transport":"not_supplied",
                "structural_complexity_selection":"not_implemented",
                "Born_probabilities":"not_derived",
                "Bell_violation":"not_derived"},
            "source_sha256":{str(path.relative_to(Path(__file__).resolve().parents[2])):
                              hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in (Path(__file__).resolve(),Path(__file__).with_name("model.py").resolve())},
            "interpretation":"Exact fixed-gauge phase-dependent retained records on one board. Click absence is many-to-one and does not reconstruct zero intensity. No new physical law is inferred."}
    (out/"phase.json").write_text(exact_json.dumps(report,sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle",required=True,type=Path)
    parser.add_argument("--out",default=Path("runs/clock_links/phase"),type=Path)
    parser.add_argument("--steps",type=int,default=3)
    args=parser.parse_args(argv)
    result=audit(load_bundle(args.base_bundle),args.out,steps=args.steps)
    print(exact_json.dumps({k:result[k] for k in ("channels_per_node","exact_intensity_quotient_comparisons","base_projection_unchanged","complete_rewind")}))


if __name__=="__main__":
    main()
