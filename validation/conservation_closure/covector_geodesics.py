"""Same-state Bianchi-I covectors and passive geodesic diagnostics.

Engine advances only the shared sourced background. Probe parameters, metric
readouts and quadrature below never advance a retained worldline or feed Engine.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes

ROOT = Path(__file__).resolve().parents[2]
TARGET = F(1, 8)
RESOLUTIONS = (24, 48, 96)
SOURCES = [
    {"title": "Fleury, Pitrou, Uzan, Light propagation in a homogeneous and anisotropic universe",
     "url": "https://arxiv.org/pdf/1410.8473", "read": "sections II, IV; equations 4.1-4.7"},
    {"title": "Scott A. Hughes, MIT 8.962 Lecture 9, Motion of an unforced body in curved spacetime",
     "url": "https://web.mit.edu/sahughes/www/8.962/lec09.pdf", "read": "sections 9.3-9.4; equations 9.24-9.31"},
]


def number(value):
    """Exact rational conversion to the current passive working precision."""
    if isinstance(value, F):
        return mp.mpf(value.numerator)/value.denominator
    return mp.mpf(value)


def probe_rates(scale_factors, covector=(3, 0, 0), mass=4):
    """Instantaneous metric prediction, with no retained probe allocation.

    `covector` contains constant spatial covariant momenta. `raised` are the
    contravariant four-momentum's spatial entries, not coordinate velocities.
    The null case has zero proper interval; it does not define a photon clock.
    """
    if len(scale_factors) != 3 or len(covector) != 3:
        raise ValueError("Three metric axes and three covector entries are required")
    a, p, m = tuple(map(number, scale_factors)), tuple(map(number, covector)), number(mass)
    if m < 0 or any(x <= 0 for x in a) or (m == 0 and not any(p)):
        raise ValueError("Positive scale factors and a nonzero causal momentum are required")
    raised = tuple(p[i]/a[i]**2 for i in range(3))
    q = sum(p[i]*raised[i] for i in range(3))
    energy = mp.sqrt(m*m+q)
    velocity = tuple(x/energy for x in raised)
    return {"E": energy, "raised": raised, "velocity": velocity,
            "proper_rate": m/energy, "spatial_speed2": q/(energy*energy)}


def symbolic_audit():
    """Independent affine geodesic, mass shell and change-of-basis proof."""
    a = s.symbols("a1:4", positive=True)
    h = s.symbols("H1:4", real=True)
    p = s.symbols("p1:4", real=True)
    mass = s.symbols("m", positive=True)
    energy = s.sqrt(mass**2+sum(p[i]**2/a[i]**2 for i in range(3)))
    momentum = [energy]+[p[i]/a[i]**2 for i in range(3)]
    metric = s.diag(-1, *(x*x for x in a))
    derivative = lambda expr: sum(s.diff(expr, a[i])*h[i]*a[i] for i in range(3))
    connection = [[[s.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(3):
        connection[0][i+1][i+1] = a[i]**2*h[i]
        connection[i+1][0][i+1] = connection[i+1][i+1][0] = h[i]
    geodesic = [s.simplify(energy*derivative(momentum[mu])+
        sum(connection[mu][nu][rho]*momentum[nu]*momentum[rho]
            for nu in range(4) for rho in range(4))) for mu in range(4)]
    assert geodesic == [0, 0, 0, 0]
    norm = s.simplify((s.Matrix(momentum).T*metric*s.Matrix(momentum))[0])
    assert s.simplify(norm+mass**2) == 0
    assert all(s.simplify(a[i]**2*momentum[i+1]-p[i]) == 0 for i in range(3))
    velocity = [x/energy for x in momentum[1:]]
    assert s.simplify(1-sum(a[i]**2*velocity[i]**2 for i in range(3))-(mass/energy)**2) == 0
    energy_rate = -sum(h[i]*p[i]**2/a[i]**2 for i in range(3))/energy
    assert s.simplify(derivative(energy)-energy_rate) == 0
    # Diagonal coordinate scaling x'^i=lambda_i x^i transforms a_i and p_i
    # by the SAME inverse factor, while the contravariant momentum scales up.
    scales = s.symbols("lambda1:4", positive=True)
    ap = [a[i]/scales[i] for i in range(3)]
    pp = [p[i]/scales[i] for i in range(3)]
    assert s.simplify(sum(pp[i]**2/ap[i]**2-p[i]**2/a[i]**2 for i in range(3))) == 0
    assert all(s.simplify(pp[i]/ap[i]**2-scales[i]*momentum[i+1]) == 0 for i in range(3))
    # Holding contravariant momentum constant violates the spatial equation
    # in any expanding occupied axis, even if the mass shell is re-imposed.
    wrong_residual = 2*energy*h[0]*p[0]/a[0]**2
    assert wrong_residual.subs({mass:4, p[0]:3, p[1]:0, p[2]:0,
        a[0]:1, a[1]:1, a[2]:1, h[0]:1}) == 30
    return {"affine_geodesic_components": [str(x) for x in geodesic],
        "mass_shell": "g_munu P^mu P^nu=-m^2", "covector_conservation": True,
        "coordinate_velocity": "dx^i/dt=p_i/(a_i^2 E)",
        "proper_time_rate": "d tau_probe/dt=m/E", "measured_energy": "E=sqrt(m^2+sum p_i^2/a_i^2)",
        "energy_rate": "dE/dt=-sum H_i p_i^2/(a_i^2 E)",
        "dual_coordinate_transform_verified": True,
        "constant_contravariant_momentum_negative_residual": "30"}


def encoding_obstruction():
    """A deliberately narrow exact rational-coordinate obstruction."""
    z = s.symbols("z")
    assert s.Poly(2*z*z-1, z, domain=s.QQ).is_irreducible
    assert s.sqrt(2)/2 not in s.QQ
    flat = probe_rates((1,1,1), (3,0,0), 4)
    assert mp.almosteq(flat["E"], 5) and mp.almosteq(flat["proper_rate"], mp.mpf(4)/5)
    assert mp.almosteq(flat["velocity"][0], mp.mpf(3)/5)
    null = probe_rates((1,1,1), (1,0,0), 0)
    assert null["proper_rate"] == 0 and null["spatial_speed2"] == 1
    rest = probe_rates((2,3,4), (0,0,0), 7)
    assert rest["proper_rate"] == 1 and rest["spatial_speed2"] == 0
    return {"fixed_rational_position_and_clock_encoding": "blocked for exact generic proper-time steps",
        "witness": "Flat a_i=1, m=1, p=(1,0,0): dx/dt=d tau/dt=1/sqrt(2)",
        "proof": "2*z^2-1 is irreducible over Q; a positive rational step has irrational displacement and proper interval, whereas a rational decoder of integer registers remains rational.",
        "scope": "Excludes only exact rational decoded positions/proper times on all rational inputs. It does not exclude approximate, algebraic, implicit or nonlinear encodings.",
        "flat_345_proper_rate": "4/5", "null_proper_interval": "0", "rest_proper_rate": "1",
        "new_retained_probe_channels": 0, "autonomous_worldline_or_detector": "not_implemented"}


def independent_scale_factors(initial, elapsed):
    """Continuum reference from physical constants, never an Engine callback."""
    t = number(elapsed)
    v0, u0, dust = map(number, (initial["V"],initial["U"],initial["D"]))
    shear = tuple(map(number, initial["S"]))
    volume = v0+u0*t+mp.mpf(3)*dust*t*t/4
    speed = u0+mp.mpf(3)*dust*t/2
    k = u0*u0-3*dust*v0
    if not (dust > 0 and k > 0 and u0 > mp.sqrt(k) and t >= 0):
        raise ValueError("This reference is only the declared expanding positive-dust chart")
    root = mp.sqrt(k)
    # log1p form differs from the common readout and avoids subtracting close logs.
    integral = (mp.log1p((speed-u0)/(u0-root))-
                mp.log1p((speed-u0)/(u0+root)))/root
    return tuple(mp.root(volume,3)*mp.exp(si*integral) for si in shear)


def composite_trapezoid(values, step):
    return number(step)*(sum(values[1:-1])+(values[0]+values[-1])/2)


def quadrature_bound():
    """Conservative analytic C² bounds for the declared default probe/interval.

    The expanding exact background has V>=7/3, 4<=U<=67/16 and I>=0.
    Therefore a1>1, 0<q=9/a1²<=9, 0<H1<2 and |H1_dot|<4.
    Differentiate m/E and q/(p E), using E²=16+q and qdot=-2 H1 q.
    """
    assert F(67,16)/3+1 < 2*F(7,3)
    assert F(1,2)/F(7,3)+F(67,16)*2/F(7,3) < 4
    proper_m2 = 4*((4+2*2**2)*F(9,4**3)+3*2**2*F(9**2,4**5))
    r_bound = F(2*9,4)+F(9**2,4**3)
    rq_bound = F(2,4)+F(3*9,4**3)+F(3*9**2,2*4**5)
    position_m2 = (4*r_bound+2*rq_bound*36)/3
    assert proper_m2 == F(675,64) and position_m2 == F(8361,256)
    q = s.symbols('q', positive=True)
    e = s.sqrt(16+q)
    r = -2*q/e+q*q/e**3
    assert s.simplify(s.diff(r,q)-(-2/e+3*q/e**3-s.Rational(3,2)*q*q/e**5)) == 0
    return {"proper_second_derivative_bound":str(proper_m2),
        "x1_second_derivative_bound":str(position_m2),
        "theorem":"For f in C^2[0,T], composite trapezoid error <= T*h^2*sup|f''|/12.",
        "scope":"Default D1,P2,S=(1,-1,0),V0=7/3,U0=4; probe m4,p=(3,0,0); 0<=t<=1/8.",
        "proper_M2":proper_m2,"position_M2":position_m2}


def same_state_audit():
    from . import common
    results = []
    with mp.workdps(70):
        reference = None
        for resolution in RESOLUTIONS:
            program = common.build(N=resolution)
            seed = common.prepare(program)
            engine, state = Engine(program.tensor), seed
            steps = int(TARGET*resolution)
            states = [seed]
            for _ in range(steps):
                old = state
                state = engine.step(old)
                assert state.same_as(common.scalar_step(old))
                assert engine.inverse_step(state).same_as(old)
                states.append(state)
            assert engine.rewind(state,steps).same_as(seed)
            initial = common.read_conserved(program,seed)
            physical = [common.physical(program,x,dps=70) for x in states]
            conserved = [common.read_conserved(program,x) for x in states]
            assert conserved[-1]["tau"]-conserved[0]["tau"] == TARGET
            assert all(x["Q"] == 0 for x in conserved)
            assert all(x["S"] == initial["S"] for x in conserved)
            # The reference gets only physical initial constants, not retained
            # recurrence, tensor coefficients or the common physical readout.
            max_metric_error = mp.mpf(0)
            for record, conserved_record in zip(physical,conserved):
                elapsed = conserved_record["tau"]-initial["tau"]
                ref_a = independent_scale_factors(initial,elapsed)
                max_metric_error = max(max_metric_error,
                    max(abs(number(record["a"][i])-ref_a[i]) for i in range(3)))
            assert max_metric_error < mp.mpf("1e-60")
            probes = [probe_rates(x["a"],(3,0,0),4) for x in physical]
            for record, probe in zip(physical, probes):
                norm = -probe['E']**2+sum(number(record['a'][i])**2*probe['raised'][i]**2 for i in range(3))
                interval = 1-sum(number(record['a'][i])**2*probe['velocity'][i]**2 for i in range(3))
                assert abs(norm+16) < mp.mpf('1e-60')
                assert abs(interval-probe['proper_rate']**2) < mp.mpf('1e-60')
            assert all(0 < x["proper_rate"] < 1 for x in probes)
            assert all(probes[i+1]["E"] < probes[i]["E"] for i in range(steps))
            assert all(probes[i+1]["proper_rate"] > probes[i]["proper_rate"] for i in range(steps))
            proper = composite_trapezoid([x["proper_rate"] for x in probes],F(1,resolution))
            distance = composite_trapezoid([x["velocity"][0] for x in probes],F(1,resolution))
            integrand = lambda t: probe_rates(independent_scale_factors(initial,t),(3,0,0),4)
            tau_ref = mp.quad(lambda t: integrand(t)["proper_rate"],[0,number(TARGET)])
            x_ref = mp.quad(lambda t: integrand(t)["velocity"][0],[0,number(TARGET)])
            assert 0 < tau_ref < number(TARGET)
            bound = quadrature_bound()
            proper_bound = TARGET*F(1,resolution)**2*bound["proper_M2"]/12
            position_bound = TARGET*F(1,resolution)**2*bound["position_M2"]/12
            assert abs(proper-tau_ref) < number(proper_bound)
            assert abs(distance-x_ref) < number(position_bound)
            if reference is not None:
                assert abs(reference[0]-tau_ref) < mp.mpf("1e-60")
                assert abs(reference[1]-x_ref) < mp.mpf("1e-60")
            reference = tau_ref,x_ref
            initial_a, final_a = physical[0]["a"],physical[-1]["a"]
            redshifts = []
            for axis in range(3):
                p = tuple(int(i==axis) for i in range(3))
                e0 = probe_rates(initial_a,p,0)["E"]
                e1 = probe_rates(final_a,p,0)["E"]
                redshifts.append(e0/e1-1)
            assert redshifts[0] > redshifts[2] > redshifts[1] > 0
            max_bits = max(abs(int(v)).bit_length()
                for x in states for arr in (x.a,x.b,x.r) for v in arr.flat)
            row = {"N":resolution,"steps":steps,"target_proper_time":str(TARGET),
                "tensor_sha256":program.tensor.fingerprint,
                "seed_sha256":hashlib.sha256(canonical_bytes(seed.to_dict())).hexdigest(),
                "source_state_constraint_exact":True,"complete_inverse_and_rewind":True,
                "channels":seed.G,"peak_integer_bits":max_bits,
                "metric_vs_independent_exact_solution_error":mp.nstr(max_metric_error,8),
                "passive_trapezoid_proper_time":mp.nstr(proper,30),
                "passive_trapezoid_x1":mp.nstr(distance,30),
                "proper_time_error":mp.nstr(abs(proper-tau_ref),18),
                "x1_error":mp.nstr(abs(distance-x_ref),18),
                "proved_proper_quadrature_error_bound":str(proper_bound),
                "proved_x1_quadrature_error_bound":str(position_bound),
                "proper_rate_initial":mp.nstr(probes[0]["proper_rate"],30),
                "proper_rate_final":mp.nstr(probes[-1]["proper_rate"],30),
                "axis_null_redshifts":list(map(lambda x:mp.nstr(x,30),redshifts))}
            results.append(row)
        orders = []
        for before,after in zip(results,results[1:]):
            orders.append({key:float(mp.log(number(before[key])/number(after[key]),2))
                for key in ("proper_time_error","x1_error")})
        assert all(1.95 < row[key] < 2.05 for row in orders for key in row)
        # A higher-precision repeat bounds numerical reference sensitivity,
        # not the discrete trapezoid error.
        with mp.workdps(90):
            ref90 = mp.quad(lambda t: probe_rates(independent_scale_factors(initial,t),(3,0,0),4)["proper_rate"],
                [0,number(TARGET)])
            reference_gap = abs(ref90-reference[0])
        assert reference_gap < mp.mpf("1e-60")
        return {"status":"passed","runs":results,"observed_diagnostic_orders":orders,
            "reference_proper_time":mp.nstr(reference[0],40),
            "reference_x1":mp.nstr(reference[1],40),
            "reference_70_vs_90_dps_gap":mp.nstr(reference_gap,10),
            "interpretation":"Convergent passive quadrature of a test-particle geodesic on the same exact native background; no retained worldline, signal transport, backreaction or detector.",
            "moving_clock_equals_background_time":"failed, strictly less for nonzero covector",
            "null_redshift_is_direction_dependent":True}


def main():
    from . import common
    bounds = quadrature_bound()
    bounds.pop("proper_M2"); bounds.pop("position_M2")
    report = {"schema":"universe24-conservation-covectors-v1",
        "symbolic":symbolic_audit(),"encoding":encoding_obstruction(),
        "same_state":same_state_audit(),"diagnostic_error_theorem":bounds,"primary_sources":SOURCES,
        "source_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__),Path(common.__file__))}}
    out = ROOT/"runs/conservation_closure/covector_geodesics.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"passed","runs":report["same_state"]["runs"],
        "diagnostic_orders":report["same_state"]["observed_diagnostic_orders"],
        "retained_worldline":"not_implemented"},indent=2))


if __name__ == "__main__":
    main()
