"""Passive compiler checks on the isolated fixed-six compatibility port."""


def main():
    from pathlib import Path
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True,
                        help='isolated current-core checkout containing the fixed-six ADM compatibility port')
    parser.add_argument('--out', type=Path, default=Path('runs/einstein-review/scheduler-control.json'))
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    if not (source_root/'experiments/geometry/integer_circuit.py').is_file():
        parser.error('the source root must contain the separately fetched ADM compiler; see docs/EINSTEIN_UPDATE_REVIEW.md')
    sys.path.insert(0, str(source_root))
    import numpy as np
    from universe24.core import Engine
    from universe24.tools.audit_contract import scalar_crosscheck
    from experiments.geometry.integer_circuit import Circuit

    c=Circuit(); x=c.input('x'); p=c.compile({'result':(x*x+3)**2})
    seed=p.prepare(3,{'x':np.full((3,3,3),2)})
    e=Engine(p.tensor)
    clocks=[i for i,n in enumerate(p.tensor.names) if n.startswith('clock.')]
    clock_set=set(clocks)
    terms=[m for m in p.tensor.monomials if m.target in clock_set]
    nominal=e.run(seed,p.ticks)
    changed=p.prepare(3,{'x':np.full((3,3,3),3)})
    changed_final=e.run(changed,p.ticks)
    cut=seed.copy();cut.a[clocks,0]=0;cut.b[clocks,0]=0
    cut_final=e.run(cut,p.ticks)
    trace=[]; state=seed
    for tick in range(3*p.period+1):
        trace.append({'tick':tick,'output_node0':str(p.read(state,'result',0)),
                      'max_bits':state.max_abs().bit_length()})
        if tick<3*p.period:state=e.step(state)
    result={'declared_ticks':p.ticks,'clock_period':p.period,'clock_gears_per_node':len(clocks),
            'clock_a_and_b_identical_at_all_nodes':bool(np.all(seed.a[clocks]==seed.a[clocks,0,None]) and np.all(seed.b[clocks]==seed.b[clocks,0,None])),
            'clock_target_has_spatial_neighbor_read':any(any(f.offset!=(0,0,0) for f in m.factors) for m in terms),
            'clock_target_reads_arithmetic':any(any(f.gear not in clock_set for f in m.factors) for m in terms),
            'arithmetic_input_intervention_changes_clocks':not(np.array_equal(nominal.a[clocks],changed_final.a[clocks]) and np.array_equal(nominal.b[clocks],changed_final.b[clocks])),
            'nominal_output':str(p.read(nominal,'result',0)),
            'clock_removed_at_one_node_output':str(p.read(cut_final,'result',0)),
            'clock_removed_other_node_output':str(p.read(cut_final,'result',1)),
            'cut_exact_rewind':e.rewind(cut_final,p.ticks).same_as(cut),
            'beyond_horizon_first_changed_output':next((r for r in trace if r['tick']>p.ticks and r['output_node0']!='49'),None),
            'beyond_horizon_exact_rewind':e.rewind(state,3*p.period).same_as(seed),
            'trace':trace,'small_circuit_scalar_oracle':scalar_crosscheck(p.tensor),
            'scope':'Prepared arithmetic control. Past-horizon outputs are not additional physical snapshots; this is not a burst-model run.'}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='trace'},indent=2))


if __name__=="__main__":
    main()
