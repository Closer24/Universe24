"""Optional official-click rest-clock gate for the existing scalar lapse reader.

This builds an isolated prescribed-background test-body tensor, NOT one_system.
One fixed law evolves all preparations solely through Engine.step. The primary
comparison is a double ratio of two clock rates, so the computational tick unit
cancels. Sine-transformed rates check the dispersion formula only; they cannot
rescue a failed raw-clock gate. No propagation metric or Einstein equation is
derived by this experiment. There are no runtime freezes, injections or resets.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from ..core import Block, Engine, GearType, State, compose
from ..layers import gravity as gr
from ..observe.gravity import crossing_times, rate_from_crossings
from ..observe.readout import official_clicks


TEST_BODY_REASON = (
    'METRIC GATE: prescribed-background test-body lapse read; reciprocal '
    'sources omitted in this isolated comparison, not self-generated gravity'
)


@dataclass(frozen=True)
class ClockGateConfig:
    Q: int = 2**24+1
    P: int = 2**12
    L: int = 3
    steps: int = 32768
    amplitude: int = 2**24
    mass_multipliers: tuple[int, ...] = (1, 4, 1024, 4096)
    fields: tuple[int, ...] = (0, 32, 128, -128)
    tolerance: float = 1e-5
    counter_limit: int = 2**60

    def validate(self):
        for name in ('Q','P','L','steps','amplitude','counter_limit'):
            value=getattr(self,name)
            if type(value) is not int or value<1:
                raise ValueError(f'{name} must be a positive integer')
        if self.Q<3 or self.Q%2!=1:
            raise ValueError('Q must be odd and at least three')
        if self.amplitude>=self.counter_limit:
            raise ValueError('initial amplitude must be below the counter limit')
        if (len(self.mass_multipliers)<2 or len(set(self.mass_multipliers))!=len(self.mass_multipliers)
            or any(type(n) is not int or n<1 for n in self.mass_multipliers)):
            raise ValueError('at least two distinct positive integer mass multipliers are required')
        if (not self.fields or self.fields[0]!=0 or len(set(self.fields))!=len(self.fields)
            or any(type(F) is not int for F in self.fields)):
            raise ValueError('fields must be distinct integers beginning with the flat control zero')
        if type(self.tolerance) not in (int,float) or not math.isfinite(self.tolerance) or self.tolerance<=0:
            raise ValueError('tolerance must be finite and positive')
        # Exact integer band check for the declared isolated clock backgrounds.
        for F in self.fields:
            if abs(F)>=self.counter_limit:
                raise ValueError('background must be below the counter limit')
            for n in self.mass_multipliers:
                if not 0<2*n*(self.P-F)<12*self.Q:
                    raise ValueError('every prepared scalar clock must be strictly in its linear oscillatory band')


def build_gate_tensor(config: ClockGateConfig):
    """Existing scalar lapse coefficients with declared one-way test-body reads."""
    config.validate()
    Q,P,D=config.Q,config.P,6*config.Q
    field=Block((GearType('h00',label='audit'),),
        (('h00',D,(('h00',(0,0,0),'b'),)),),name='metric',Q=Q)
    specs=[gr.atom_spec(f'clock{n}',2*P*n) for n in config.mass_multipliers]
    blocks=[field]+[gr.build_test_matter(spec,Q=Q) for spec in specs]
    full=gr.build_lapse(Q=Q,P=P,field='metric.h00',matters=specs)
    reads=tuple((term[0],term[1],term[2],{'designated_one_way':TEST_BODY_REASON})
                for term in full.terms if term[0]!='metric.h00')
    blocks.append(Block((),reads,name=None,Q=Q))
    return compose(*blocks)


def prepare_gate(tensor, config: ClockGateConfig, field: int):
    """Identical clock data across cases; only the background a,b value changes."""
    a=np.full((tensor.G,config.L**3),config.amplitude,dtype=object)
    a[tensor.gear_index('metric.h00')]=field
    return State(config.L,a,a.copy(),np.full_like(a,3*config.Q-1))


def _digest(state):
    # Delimited exact integer triples; dimensions are recorded in the manifest.
    h=hashlib.sha256()
    for key in ('a','b','r'):
        h.update(key.encode())
        for value in getattr(state,key).flat:
            h.update(str(int(value)).encode());h.update(b',')
    return h.hexdigest()


def _run_case(tensor, config, field):
    engine=Engine(tensor,config.Q)
    seed=prepare_gate(tensor,config,field);state=seed
    series={n:([],[]) for n in config.mass_multipliers}
    gears={tensor.gear_index(f'clock{n}.c'):n for n in config.mass_multipliers}
    background=tensor.gear_index('metric.h00')
    peak=config.amplitude;static=True;actual=0
    for step in range(1,config.steps+1):
        after=engine.step(state)
        # Public labels and arithmetic-event convention are both enforced.
        log=official_clicks(engine,state,after,step)
        for row in np.flatnonzero(log.node==0):
            n=gears[int(log.gear[row])]
            series[n][0].append(step)
            series[n][1].append(int(log.quotient[row]))
        static &= bool(np.all(after.a[background]==field) and np.all(after.b[background]==field))
        peak=max(peak,int(np.max(np.abs(after.a))),int(np.max(np.abs(after.b))))
        state=after;actual=step
        if peak>=config.counter_limit:
            break  # stop and report; never clamp or alter the trajectory
    clocks={}
    for n,(times,quotients) in series.items():
        crossings=crossing_times(times,quotients)
        raw=rate_from_crossings(crossings)
        expected=math.acos(1-(2*config.P*n/(6*config.Q))*(1-field/config.P))
        windows=[]
        for w in range(4):
            lo=w*config.steps//4;hi=(w+1)*config.steps//4
            subset=[t for t in crossings if lo<t<=hi]
            rate=rate_from_crossings(subset)
            windows.append({'bounds':[lo,hi],'crossings':len(subset),
                            'raw_omega':rate if math.isfinite(rate) else None})
        clocks[str(n)]={'official_records':len(times),'crossings':len(crossings),
            'raw_omega':raw if math.isfinite(raw) else None,'analytic_omega':expected,
            'raw_omega_error':raw-expected if math.isfinite(raw) else None,
            'four_windows':windows}
    return {'F':field,'U':field/(2*config.P),'expected_lapse':math.sqrt(1-field/config.P),
        'steps':actual,'requested_steps':config.steps,'seed_sha256':_digest(seed),
        'final_sha256':_digest(state),'static_field_exact':static,
        'peak_counter_magnitude':peak,'peak_counter_bits':peak.bit_length(),
        'guard_pass':peak<config.counter_limit,
        'stop_reason':'counter_limit' if peak>=config.counter_limit else 'completed',
        'clocks':clocks,'exact_rewind':engine.rewind(state,actual).same_as(seed)}


def run_gate(config: ClockGateConfig | None = None):
    """Run fresh exact trajectories, then compare passive click rates; no cache."""
    config=config or ClockGateConfig()
    tensor=build_gate_tensor(config)
    cases=[_run_case(tensor,config,F) for F in config.fields]
    baseline=cases[0]['clocks']
    flat_complete=(cases[0]['steps']==config.steps and cases[0]['exact_rewind'] and
                   cases[0]['static_field_exact'] and cases[0]['guard_pass'])
    flat_rates_valid=all(item['raw_omega'] is not None and item['raw_omega']>0
                         for item in baseline.values())
    flat_control_valid=flat_complete and flat_rates_valid
    for case in cases:
        complete=(case['steps']==config.steps and case['exact_rewind'] and
                  case['static_field_exact'] and case['guard_pass'])
        comparison_valid=complete and flat_control_valid
        case['flat_control_valid']=flat_control_valid
        ratios={}
        for n,item in case['clocks'].items():
            omega0=baseline[n]['raw_omega'];omega=item['raw_omega']
            valid=omega0 is not None and omega is not None and omega0>0
            ratio=omega/omega0 if valid else None
            sine=math.sin(omega/2)/math.sin(omega0/2) if valid else None
            item.update(raw_ratio=ratio,
                raw_ratio_minus_common_lapse=ratio-case['expected_lapse'] if valid else None,
                sine_dispersion_ratio=sine,
                sine_ratio_minus_common_lapse=sine-case['expected_lapse'] if valid else None)
            ratios[n]=ratio
        pairs=[]
        for i,n in enumerate(config.mass_multipliers):
            for m in config.mass_multipliers[i+1:]:
                valid=ratios[str(n)] is not None and ratios[str(m)] is not None
                R=ratios[str(n)]/ratios[str(m)] if valid else None
                within_tolerance=valid and abs(R-1)<=config.tolerance
                pairs.append({'A':n,'B':m,'double_ratio':R,'minus_one':R-1 if valid else None,
                              'within_tolerance':within_tolerance,
                              'pass':comparison_valid and within_tolerance})
        case['relational_clock_pairs']=pairs
        case['relational_all_clock_gate']=comparison_valid and all(p['pass'] for p in pairs)
        case['relational_first_pair_gate']=comparison_valid and pairs[0]['pass']
        case['sine_dispersion_gate']=comparison_valid and all(
            item['sine_ratio_minus_common_lapse'] is not None and
            abs(item['sine_ratio_minus_common_lapse'])<=config.tolerance for item in case['clocks'].values())
        if not complete:
            case['relational_status']='incomplete_or_guard_failure'
        elif not flat_complete:
            case['relational_status']='invalid_flat_control'
        elif any(p['double_ratio'] is None for p in pairs):
            case['relational_status']='inconclusive_insufficient_crossings'
        else:
            case['relational_status']='pass' if case['relational_all_clock_gate'] else 'measured_disagreement'
    return {'schema':'metric-clock-gate-v3','config':asdict(config),
        'flat_control_valid':flat_control_valid,
        'manifest':{'tensor_fingerprint':tensor.fingerprint,'dynamics_fingerprint':tensor.dynamics_fingerprint,
            'rank':tensor.rank,'gear_count':tensor.G,'support_violations':tensor.support_violations(),
            'designation_count':len(tensor.designations),'same_tensor_all_cases':True},
        'primary':'R_AB=[omega_A(F)/omega_B(F)]/[omega_A(0)/omega_B(0) must be within tolerance of one',
        'readout':'Official-labelled changed-triple nonzero-quotient records at node0; signed crossing interpolation',
        'scope':'Isolated prescribed-background scalar test clocks; not one_system, generated gravity or a complete metric',
        'secondary':'Sine-transformed dispersion diagnostic only; cannot rescue a failed raw-clock gate',
        'cases':cases}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps',type=int,default=32768)
    parser.add_argument('--L',type=int,default=3)
    parser.add_argument('--out',type=Path,default=Path('runs/metric-clock-gate/report.json'))
    args=parser.parse_args()
    report=run_gate(ClockGateConfig(steps=args.steps,L=args.L))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'output':str(args.out),'cases':[
        {'F':c['F'],'steps':c['steps'],'exact_rewind':c['exact_rewind'],
         'all_clock_gate':c['relational_all_clock_gate'],'first_pair_gate':c['relational_first_pair_gate'],
         'dispersion_diagnostic':c['sine_dispersion_gate']} for c in report['cases']]},indent=2))


if __name__=='__main__':
    main()
