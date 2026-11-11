"""Negative controls before identifying the board or clicks with physical spacetime.

This tool does not fit a metric, relabel a computational step as proper time, or
insert relativistic outcomes. It compares the baseline with the single-edge
experiment and records concrete obstructions to inheriting physical claims.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from ..core import Engine
from ..core.lattice import lattice
from ..demos.one.run_one import build
from ..layers.strict_edge import single_edge_realization
from ..observe.em import lorenz_C
from ..observe.readout import official_clicks
from ..observe.strict_edge import source_coordinate_view
from ..prepare.strict_edge import lift_seed


def reachable_gears(tensor, sources):
    """Over-approximate possible dependencies; absence proves no causal path.

    Forget spatial offsets and include both old-a and old-b reads. Retained local
    state cannot create a missing inter-gear dependency. Presence alone does not
    prove an excited signal or a physical interaction.
    """
    edges = [set() for _ in tensor.gears]
    for m in tensor.monomials:
        for factor in m.factors:
            edges[factor.gear].add(m.target)
    seen = set(sources)
    todo = list(seen)
    while todo:
        for target in edges[todo.pop()]:
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return seen


def check_candidate(tensor, engine, seed, steps, *, source=None, realization=None):
    fields = [i for i,n in enumerate(tensor.names) if n.startswith(('metric.','beta.','bgk.'))]
    readers = [tensor.gear_index('cosmic.M1'),tensor.gear_index('cosmic.M2')]
    path = bool(reachable_gears(tensor,fields).intersection(readers))
    cosmic = {i for i,n in enumerate(tensor.names) if n.startswith('cosmic.')}
    closed = all(all(f.gear in cosmic for f in m.factors)
                 for m in tensor.monomials if m.target in cosmic)
    rows = sorted(cosmic)
    # Two different full seeds, never an intervention in an evolving run.
    perturbed = seed.copy()
    g = tensor.gear_index('metric.h00')
    center = lattice(seed.L).index(0,0,0)
    perturbed.a[g,center] += 20972
    perturbed.b[g,center] += 20972
    initial_C = lorenz_C(seed,tensor)
    mapped_initial_C = (lorenz_C(source_coordinate_view(seed,realization),source)
                        if realization is not None else initial_C)
    state, other = seed, perturbed
    first_defect = None
    failures = largest_defect = clock_records = mapped_failures = mapped_largest = 0
    event_equal = state_equal = True
    for step in range(1,steps+1):
        nxt, alt = engine.step(state),engine.step(other)
        left = official_clicks(engine,state,nxt,step)
        right = official_clicks(engine,other,alt,step)
        def clock_records_only(log):
            return [row for row in log.rows() if row[2] in cosmic]
        a,b = clock_records_only(left),clock_records_only(right)
        clock_records += len(a)
        event_equal = event_equal and a == b
        state_equal = state_equal and all(np.array_equal(getattr(nxt,f)[rows],getattr(alt,f)[rows])
                                         for f in ('a','b','r'))
        delta = np.asarray(lorenz_C(nxt,tensor)-initial_C,dtype=object)
        count = int(np.count_nonzero(delta))
        failures += count
        largest_defect = max(largest_defect,max(abs(int(v)) for v in delta.flat))
        if count and first_defect is None:
            first_defect = step
        mapped_delta = ((lorenz_C(source_coordinate_view(nxt,realization),source)-mapped_initial_C)
                        if realization is not None else delta)
        mapped_failures += int(np.count_nonzero(mapped_delta))
        mapped_largest = max(mapped_largest,max(abs(int(v)) for v in mapped_delta.flat))
        state,other = nxt,alt
    return dict(dynamics_fingerprint=tensor.dynamics_fingerprint,
                gravitational_clock_test=dict(steps=steps,
                    perturbation='initial metric.h00 a and b at (0,0,0) += 20972',
                    metric_to_cosmic_reader_path=path,cosmic_subsystem_closed=closed,
                    cosmic_full_state_identical=state_equal,cosmic_official_records_identical=event_equal,
                    records_compared=clock_records,
                    interpretation='closed subsystem has no gravity-dependent clock response; not calibrated proper time'),
                inherited_em_lorenz_identity=dict(first_failed_update=first_defect,
                    nonzero_site_updates=failures,max_abs_residual=largest_defect,
                    passed=failures==0,
                    interpretation='old state-derived Phi/A diagnostic, not an official-click observable'),
                mapped_em_lorenz_identity=dict(nonzero_site_updates=mapped_failures,
                    max_abs_residual=mapped_largest,passed=mapped_failures==0,
                    interpretation='source-coordinate view uses H for former U; passive partial state diagnostic'),
                einstein_spacetime_established=False)


def run(L=4,steps=40,stiffness=33554432):
    if type(steps) is not int or steps<1:
        raise ValueError('steps must be positive')
    _,source,engine,seed,_=build(L,'jpure',13)
    realization=single_edge_realization(source,stiffness=stiffness)
    lifted=lift_seed(seed,realization)
    result=dict(L=L,steps=steps,stiffness=stiffness,
                baseline=check_candidate(source,engine,seed,steps),
                single_edge=check_candidate(realization.tensor,Engine(realization.tensor,source.Q),lifted,steps,
                                            source=source,realization=realization),
                accepted_as_physics_preserving_replacement=False,
                spacetime_requirements=dict(operational_metric_from_signals_and_clocks='not established',
                    common_lorentzian_causal_cone='not established',
                    local_lorentz_symmetry_in_claimed_limit='not established',
                    universal_gravitational_clock_response='not met by the cosmic clock candidate',
                    einstein_field_equations_with_identified_sources='not derived for the default',
                    observable_agreement_in_clicks='not established'))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--L',type=int,default=4)
    p.add_argument('--steps',type=int,default=40)
    p.add_argument('--stiffness',type=int,default=33554432)
    p.add_argument('--out',default='runs/physics-gate/report.json')
    args=p.parse_args()
    result=run(args.L,args.steps,args.stiffness)
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
