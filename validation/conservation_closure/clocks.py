"""Same-state dust clock, source clock and canonical-click acceptance.

No new oscillator or detector tensor is introduced. Engine advances the shared
eight-channel Bianchi-I candidate; every physical clock readout below is passive.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO
from universe24.system.decoder import make_transition, decode_transition, summarize_clicks
from . import common

ROOT = Path(__file__).resolve().parents[2]
SOURCES = [
    {'title': 'Brown and Kuchar, Dust as a Standard of Space and Time in Canonical Quantum Gravity',
     'url': 'https://arxiv.org/pdf/gr-qc/9409001',
     'read': 'Section II A-C, equations 2.2, 2.6-2.10 and 2.15-2.17'},
    {'title': 'Rovelli, Partial observables',
     'url': 'https://arxiv.org/pdf/gr-qc/0110035',
     'read': 'Sections II-III, especially the two-clock relation in equation 4'},
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def number(value):
    value = F(value)
    return mp.mpf(value.numerator)/value.denominator


def source_clock(program, state):
    """Elapsed dust proper time since the retained velocity reference event.

    No run step, seed trace, proper_tick register or reference ODE is read here.
    This positive-dust chart is not valid at D=0.
    """
    common._check_program(program)
    if not isinstance(state, State) or state.G != 8:
        raise ValueError('source clock requires the complete eight-channel state')
    # Deliberately do not call common.read_conserved: that prepared-domain
    # validator checks the marker as well. This projection reads only these
    # four source/history entries and is not a physical-acceptance validator.
    values = (state.b[0,0],state.a[0,0],state.b[1,0],state.b[3,0])
    if any(isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) for v in values):
        raise TypeError('source clock entries must be exact integers')
    W, previous_W, D, reference = map(int,values)
    if D <= 0:
        raise ValueError('source clock requires the positive-dust chart')
    J = W-previous_W+3*D
    return F(J-reference,6*D*program.N)


def raw_clock_invariant(program, state):
    """Independent integer diagnostic, also usable on deliberately bad markers.

    It does not grant physical acceptance to a state rejected by common.read.
    """
    D = int(state.b[1, 0])
    J = int(state.b[0, 0])-int(state.a[0, 0])+3*D
    reference, tick = int(state.b[3, 0]), int(state.b[5, 0])
    return J-reference-6*D*tick


def symbolic_audit():
    W, J, D, Jref, tick, N = sp.symbols('W J D Jref tick N', integer=True)
    invariant = J-Jref-6*D*tick
    pushed = invariant.subs({J:J+6*D, tick:tick+1}, simultaneous=True)
    require(sp.expand(pushed-invariant) == 0, 'source-clock integer invariant')
    source_tau = (J-Jref)/(6*D*N)
    require(sp.simplify(source_tau.subs(J,J+6*D)-source_tau-1/N) == 0,
            'source clock advances by proper step')
    require(sp.simplify(source_tau-tick/N-invariant/(6*D*N)) == 0,
            'marker and source clock differ only by the preserved origin')
    a1, a2, a3, V, P = sp.symbols('a1 a2 a3 V P', positive=True)
    inverse_metric = sp.diag(-1, a1**-2, a2**-2, a3**-2)
    grad_tau = sp.Matrix([1,0,0,0])
    dust_covector = -grad_tau
    dust_velocity = inverse_metric*dust_covector
    require(dust_velocity == sp.Matrix([1,0,0,0]), 'raise dust covector')
    require((dust_covector.T*inverse_metric*dust_covector)[0] == -1,
            'unit timelike dust covector')
    require((grad_tau.T*dust_velocity)[0] == 1, 'dust proper-time rate')
    grad_phi = sp.Matrix([P/V,0,0,0])
    require((grad_phi.T*inverse_metric*grad_phi)[0] == -P**2/V**2,
            'massless scalar is not a unit-rate proper clock')
    return {'integer_clock_invariant': 'J-Jref-6*D*T',
            'invariant_pushforward_defect': '0',
            'source_time': '(J-Jref)/(6*D*N)=2*(U-Uref)/(3*D)',
            'source_time_step': '1/N',
            'same_state_marker_relation': 'tau_source=tau_marker+C_clock/(6*D*N)',
            'dust_covector': 'u_mu=-d_mu(tau)', 'dust_covector_norm': '-1',
            'dust_material_time_rate': 'u^mu d_mu(tau)=1',
            'scalar_gradient_norm': '-P^2/V^2',
            'domain': 'D>0; shared synchronous comoving dust chart'}


def canonical_clicks(data, *, run_id='same-state-clock-audit'):
    program, states = data['program'], data['states']
    events, per_step = [], []
    for index, (before, after) in enumerate(zip(states,states[1:]), 1):
        record = make_transition(program.tensor, before, after, run_id=run_id, step=index)
        current = decode_transition(record, program.tensor, run_id=run_id)
        # Direct independent implementation of the documented arithmetic rule.
        expected = []
        for node in range(before.N):
            for gear in range(before.G):
                old, new = before.gear(gear,node), after.gear(gear,node)
                quotient = new[1]+old[0]
                if quotient and old != new:
                    expected.append((node, gear, quotient, 'C0', 1 if quotient>0 else -1))
        require([(e['node'],e['channel'],e['quotient'],e['kind'],e['sign'])
                 for e in current] == expected, 'canonical arithmetic click oracle')
        require(all(event['channel'] in (0,5) for event in current),
                'constant source/anchor channels cannot emit this protocol')
        events.extend(current)
        per_step.append(len(current))
    return events, per_step


def resolution_case(N):
    data = common.trace(N)
    program, states = data['program'], data['states']
    reads, physical = data['readouts'], data['physical']
    clocks = [source_clock(program,state) for state in states]
    invariants = [raw_clock_invariant(program,state) for state in states]
    require(invariants == [0]*len(states), 'same-state clock relation holds at every sample')
    require(clocks == [r['tau'] for r in reads], 'source/marker elapsed-time agreement')
    require(clocks[-1] == F(1,8), 'shared fixed proper endpoint')
    phase_bounds = []
    with mp.workdps(60):
        for i in range(len(states)-1):
            before, after = reads[i], reads[i+1]
            lower = before['P']*program.h/after['V']
            upper = before['P']*program.h/before['V']
            delta = physical[i+1]['phi']-physical[i]['phi']
            require(number(lower) < delta < number(upper),
                    'actual passive massless scalar lies between rational integral bounds')
            phase_bounds.append({'lower':str(lower),'upper':str(upper),
                                 'actual':mp.nstr(delta,35)})
        elapsed = clocks[-1]-clocks[0]
        lower = reads[0]['P']*elapsed/reads[-1]['V']
        upper = reads[0]['P']*elapsed/reads[0]['V']
        delta_phi = physical[-1]['phi']-physical[0]['phi']
        require(number(lower) < delta_phi < number(upper) < number(elapsed),
                'massless scalar value is demonstrably not proper elapsed time')
        # The default massless scalar is monotone but approaches a finite value.
        root = mp.sqrt(number(reads[0]['K_flow']))
        scalar_limit = reads[0]['phi_ref'] + reads[0]['P']/root*mp.log(
            (number(reads[0]['Uref'])+root)/(number(reads[0]['Uref'])-root))
        require(delta_phi < scalar_limit, 'finite scalar clock range')
    events, per_step = canonical_clicks(data)
    steps, nodes = len(states)-1, states[0].N
    require(len(events) == nodes*(2*steps-1), 'exact canonical click count at zero origin')
    return {**common.identity(program,data['seed']), 'steps':steps,
            'source_time_by_step':list(map(str,clocks)),
            'clock_invariant_by_step':invariants,
            'source_time_never_reads_tick_or_seed':True,
            'endpoint_volume':str(reads[-1]['V']), 'endpoint_velocity':str(reads[-1]['U']),
            'scalar_increment':mp.nstr(delta_phi,35),
            'scalar_increment_rational_bounds':[str(lower),str(upper)],
            'scalar_interval_bounds':phase_bounds,
            'finite_scalar_future_limit':mp.nstr(scalar_limit,35),
            'clicks':summarize_clicks(events), 'clicks_per_step':per_step,
            'bits':data['bits'], 'all_carries_retained_and_complete_rewind':True,
            'operational_detector':'not implemented'}


def intervention_controls():
    baseline = common.trace(24)
    program, seed = baseline['program'], baseline['seed']
    altered = common.trace(24, remainders=[[(int(x)+1)%6 for x in row] for row in seed.r])
    require(baseline['seed_sha256'] != altered['seed_sha256'], 'carry intervention changes complete provenance')
    for left,right in zip(baseline['states'],altered['states']):
        require(np.array_equal(left.a,right.a) and np.array_equal(left.b,right.b),
                'legal carry cannot alter divisible-by-three physical update')
        require(not np.array_equal(left.r,right.r), 'changed carry must remain retained')
        require(source_clock(program,left) == source_clock(program,right), 'carry-independent physical clock')
    base_clicks, _ = canonical_clicks(baseline)
    changed_clicks, _ = canonical_clicks(altered)
    require(base_clicks == changed_clicks, 'inert carry change does not become detector rate')

    shifted = common.trace(24,tau_tick=7)
    shifted_clicks, _ = canonical_clicks(shifted)
    offsets = []
    with mp.workdps(60):
        for index,(left,right) in enumerate(zip(baseline['states'],shifted['states'])):
            a,b = common.read_conserved(program,left), common.read_conserved(program,right)
            require(source_clock(program,left) == source_clock(program,right), 'source clock ignores coordinate origin')
            require(b['tau']-a['tau'] == F(7,24), 'retained time origin shifts consistently')
            require(raw_clock_invariant(program,right) == -42, 'origin offset is a preserved integer invariant')
            offsets.append(str(b['tau']-source_clock(program,right)))
            require(baseline['physical'][index]['phi'] == shifted['physical'][index]['phi'],
                    'scalar readout must not come from external tick lookup')
            require(baseline['physical'][index]['a'] == shifted['physical'][index]['a'],
                    'one metric cannot change when only time origin shifts')
    require(len(shifted_clicks)-len(base_clicks) == seed.N,
            'click-count origin negative must be nontrivial')

    frozen_marker = seed.copy()
    frozen_marker.a[5] = frozen_marker.b[5].copy()
    engine = Engine(program.tensor)
    current = frozen_marker
    bad_marker = [raw_clock_invariant(program,current)]
    for _ in range(3):
        old = current
        current = engine.step(current)
        require(engine.inverse_step(current).same_as(old), 'bad marker still mechanically reversible')
        require(source_clock(program,current)-source_clock(program,old) == program.h,
                'source clock advances despite a frozen independent marker')
        bad_marker.append(raw_clock_invariant(program,current))
    require(bad_marker == [0,6,12,18], 'free marker false clock rejected by relational invariant')
    try:
        common.read_conserved(program,current)
    except ValueError:
        marker_rejected = True
    else:
        raise AssertionError('zero-slope marker accepted as proper-time marker')
    require(engine.rewind(current,3).same_as(frozen_marker), 'complete bad-marker rewind')

    broken = Tensor([GearType(name,label='audit') for name in common.NAMES],
                    [(name,6,((name,ZERO,'b'),)) for name in common.NAMES], strict_support=True)
    broken_engine, current = Engine(broken), seed.copy()
    bad_source = [raw_clock_invariant(program,current)]
    for _ in range(3):
        old = current
        current = broken_engine.step(current)
        require(broken_engine.inverse_step(current).same_as(old), 'source-disconnected mechanical inverse')
        bad_source.append(raw_clock_invariant(program,current))
    require(bad_source == [0,-6,-12,-18], 'disconnected source breaks source-clock calibration')
    require(broken_engine.rewind(current,3).same_as(seed), 'complete bad-source rewind')
    return {'carry_intervention':{'status':'passed','complete_seed_changed':True,
                'physical_clock_and_canonical_clicks_unchanged':True,'changed_carries_retained':True},
            'time_origin_intervention':{'status':'passed','marker_minus_source':offsets,
                'clock_integer_invariant':-42,'same_scalar_and_metric':True,
                'baseline_clicks':len(base_clicks),'shifted_clicks':len(shifted_clicks),
                'universal_click_count_clock':'failed'},
            'frozen_marker':{'status':'rejected','clock_invariant':bad_marker,
                'common_decoder_rejected':marker_rejected,'complete_rewind':True},
            'disconnected_source':{'status':'rejected','clock_invariant':bad_source,
                'complete_rewind':True}}


def threshold_obstruction():
    """Finite witnesses accompanying the exact quasipolynomial proof in report.

    These checks do not pretend to exhaust all possible programs. The theorem
    is the induction on polynomial/fixed-divisor circuits, stated in the report.
    """
    n = sp.symbols('n',integer=True)
    residuals = []
    polynomial = 2*n**3-7*n*n+5*n-11
    for residue in range(6):
        q = sp.symbols('q',integer=True)
        expression = sp.expand(polynomial.subs(n,6*q+residue))
        constant = expression.subs(q,0)
        quotient = sp.expand((expression-constant)/6+sp.floor(constant/6))
        require(sp.Poly(quotient,q).degree() == 3, 'fixed remainder class is a polynomial')
        for value in (-100,-7,-1,0,1,9,100):
            require(int(quotient.subs(q,value)) == int(polynomial.subs(n,6*value+residue))//6,
                    'signed floor must agree on complete residue classes')
        residuals.append(str(quotient))
    samples = [0,0,0,0,1]
    differences = samples[:]
    for _ in range(4):
        differences = [b-a for a,b in zip(differences,differences[1:])]
    require(differences == [1], 'degree-three sign interpolation witness')
    # A finite alphabet can have a polynomial event encoding. It does not
    # extend to an unrestricted sign detector and is not installed in the law.
    finite = {x:x*(x+1) for x in (-1,0,1,2,-2)}
    require([finite[x] for x in (-1,0,1)] == [0,0,2], 'finite alphabet event code')
    require(finite[2] == 6 and finite[-2] == 2, 'finite alphabet detector fails outside domain')
    return {'status':'proved_scoped_obstruction',
            'claim':'No fixed finite number of polynomial/fixed-six steps gives a global exact sign bit on an unrestricted integer input with other registers fixed.',
            'reason':'Finite-step outputs are quasipolynomial on finitely many residue classes; a globally bounded polynomial on each bi-infinite class is constant there.',
            'floor_residue_polynomials':residuals,'fourth_difference_of_threshold_samples':1,
            'finite_alphabet_code':{str(k):v for k,v in finite.items()},
            'not_excluded':['bounded input domains','variable-time algorithms','unbounded counters','passive canonical click decoding','other physical clock mechanisms'],
            'installed_detector_channels':0}


def main():
    symbolic = symbolic_audit()
    cases = [resolution_case(N) for N in (24,48,96)]
    require(len({row['tensor_sha256'] for row in cases}) == 1, 'one actual tensor across resolutions')
    require(len({row['endpoint_volume'] for row in cases}) == 1, 'same physical endpoint')
    require(len({row['endpoint_velocity'] for row in cases}) == 1, 'same physical endpoint velocity')
    require(len({row['clicks']['events'] for row in cases}) == 3, 'same proper time has distinct arithmetic click counts')
    report = {'schema':'universe24/conservation-closure-clocks/1',
        'symbolic':symbolic,'same_candidate_cases':cases,
        'interventions':intervention_controls(),'threshold':threshold_obstruction(),
        'acceptance':{'same_state_source_dust_proper_time':'passed',
            'massless_scalar_as_unit_rate_periodic_clock':'failed',
            'arithmetic_click_count_as_universal_proper_clock':'failed',
            'transported_material_detector_and_autonomous_record':'not_tested'},
        'source_sha256':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (Path(__file__),Path(common.__file__))},
        'primary_readings':SOURCES,
        'scope':'Homogeneous comoving relational dust clock; no operational detector, moving retained clock or global-sign implementation.'}
    out = ROOT/'runs/conservation_closure/clocks.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'channels':8,'clock_constraint':symbolic['integer_clock_invariant'],
        'proper_endpoint':'1/8','click_counts':[x['clicks']['events'] for x in cases],
        'bits':[max(x['bits']) for x in cases],'acceptance':report['acceptance']},indent=2))


if __name__ == '__main__':
    main()
