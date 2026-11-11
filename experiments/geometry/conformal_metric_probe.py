"""Optional reciprocal conformal-scalar experiment; not the default ONE law.

Run from the repository root:
    PYTHONPATH=. python experiments/geometry/conformal_metric_probe.py

Each refinement constructs a separate fixed rank-four tensor and integer seed.
Only Engine.step evolves the state; all diagnostics and hashes are passive.
See docs/CONFORMAL_METRIC_EXPERIMENT.md for the restricted continuum claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.core.reciprocity import check_reciprocity
from universe24.observe.one import state_hash
from universe24.observe.readout import official_clicks


ROOT = Path(__file__).resolve().parents[2]
REFINEMENTS = (8, 16, 32, 64)
BACKGROUNDS = (1, 2)


def validate_refinements(values):
    """Restrict the public reproducer to the declared finite protocols."""
    values = tuple(values)
    if (not values or any(type(n) is not int or n not in REFINEMENTS for n in values)
            or len(set(values)) != len(values)):
        raise ValueError(f"refinements must be distinct members of {REFINEMENTS}")
    return values


def build(refinement, interaction=False):
    """Return the chosen fixed local tensor and its integer normalization."""
    validate_refinements((refinement,))
    if type(interaction) is not bool:
        raise ValueError("interaction must be a bool")
    N = refinement
    A = N**6
    P = A*A
    Q = P*P*N*N
    D = 6*Q
    w = D//12
    names = ("Omega", "clock1", "clock2", "signal")
    terms = []
    for name in names:
        terms.append((name, D-6*w, ((name, ZERO, "b"),)))
        terms.extend((name, w, ((name, direction, "b"),)) for direction in DIRECTIONS)
    for name, mass in (("clock1", 1), ("clock2", 2)):
        mu = 3*mass*mass
        terms.append((name, -mu, (("Omega", ZERO, "b"),
                                 ("Omega", ZERO, "b"), (name, ZERO, "b"))))
        terms.append(("Omega", -mu, (("Omega", ZERO, "b"),
                                    (name, ZERO, "b"), (name, ZERO, "b"))))
    if interaction:
        # Conformal canonical quartic: lambda=1, with no extra Omega factor.
        gamma = 3*A*A
        terms.append(("clock1", -gamma, (("clock1", ZERO, "b"),
                                        ("clock2", ZERO, "b"), ("clock2", ZERO, "b"))))
        terms.append(("clock2", -gamma, (("clock2", ZERO, "b"),
                                        ("clock1", ZERO, "b"), ("clock1", ZERO, "b"))))
    tensor = Tensor(names, terms, Q=Q, strict_support=True)
    if tensor.rank != 4 or not tensor.b_only or not check_reciprocity(tensor).ok:
        raise AssertionError("chosen conformal tensor failed structural validation")
    return tensor, dict(N=N, A=A, P=P, Q=Q, D=D, w=w,
                       masses=[1, 2], L=3, interaction=interaction)


def prepare(tensor, parameters, Omega):
    """Complete fixed seed; Omega denotes a nominal initial background."""
    if type(Omega) is not int or Omega not in BACKGROUNDS:
        raise ValueError("Omega must be one of the declared backgrounds 1 or 2")
    expected, expected_parameters = build(parameters["N"], parameters["interaction"])
    if parameters != expected_parameters or tensor.fingerprint != expected.fingerprint:
        raise ValueError("seed parameters and tensor do not describe the same fixed law")
    b = np.zeros((4, 27), dtype=object)
    b[0] = parameters["P"]*Omega
    # Same physical scalar amplitude: chi = Omega*phi.
    b[1:3] = parameters["A"]*Omega
    for node in range(27):
        x = node//9
        b[3, node] = parameters["A"]*(1, -1, 0)[x]
    r = np.full((4, 27), parameters["D"]//2-1, dtype=object)
    return State(3, b.copy(), b, r)


def exact_state_hash(state):
    return state_hash(state, list(range(state.G)))


def trace_hash(samples):
    # Matches the original research-run serialization.
    return hashlib.sha256(json.dumps(samples).encode()).hexdigest()


def read_samples(engine, before, after, tick, gears):
    """Decode official rows only, preserving zero slots at missing updates.

    The independent equality audit detects an omitted nonzero raw quotient;
    it never supplies a replacement sample to the decoder.
    """
    log = official_clicks(engine, before, after, tick)
    recorded = {int(g): int(q) for g, node, q in zip(log.gear, log.node, log.quotient)
                if int(node) == 0}
    samples = {gear: recorded.get(gear, 0) for gear in gears}
    for gear, sample in samples.items():
        raw_quotient = int(after.b[gear, 0]) + int(before.a[gear, 0])
        if sample != raw_quotient:
            raise AssertionError("official stream omitted a nonzero observed quotient")
    return samples, len(log)


def metric_diagnostics(state, nominal_counter, old_max_drift, old_min):
    values = [int(value) for value in state.b[0]]
    minimum = min(old_min, min(values))
    if minimum <= 0:
        raise AssertionError("conformal factor left the positive prepared regime")
    return max(old_max_drift, max(abs(value-nominal_counter) for value in values)), minimum


def frequency_from_official_quotients(samples):
    """Positive crossings, linearly interpolated; zero plateaus enter once."""
    crossings = []
    for i in range(1, len(samples)):
        left, right = samples[i-1], samples[i]
        if left < 0 <= right:
            crossings.append(i + float(-left)/float(right-left))
    if len(crossings) < 3:
        raise AssertionError("insufficient observed clock cycles")
    period = (crossings[-1]-crossings[0])/(len(crossings)-1)
    return 2*math.pi/period, crossings


def run_pair(N):
    tensor, parameters = build(N)
    steps = math.ceil(16*math.pi*N)
    engine = Engine(tensor, parameters["Q"])
    seeds = [prepare(tensor, parameters, Omega) for Omega in BACKGROUNDS]
    states = [seed.copy() for seed in seeds]
    samples = [{1: [], 2: [], 3: []} for _ in states]
    counts, drifts = [0, 0], [0, 0]
    minima = [Omega*parameters["P"] for Omega in BACKGROUNDS]
    signal_identical = complete_signal_identical = True
    for tick in range(1, steps+1):
        for index, state in enumerate(states):
            following = engine.step(state)
            recorded, count = read_samples(engine, state, following, tick, (1, 2, 3))
            counts[index] += count
            for gear, value in recorded.items():
                samples[index][gear].append(value)
            drifts[index], minima[index] = metric_diagnostics(
                following, BACKGROUNDS[index]*parameters["P"], drifts[index], minima[index])
            states[index] = following
        signal_identical &= samples[0][3][-1] == samples[1][3][-1]
        complete_signal_identical &= all(
            np.array_equal(getattr(states[0], field)[3], getattr(states[1], field)[3])
            for field in ("a", "b", "r"))
    observations = []
    for index, Omega in enumerate(BACKGROUNDS):
        frequencies = []
        for gear, mass in ((1, 1), (2, 2)):
            omega, crossings = frequency_from_official_quotients(samples[index][gear])
            ideal = math.acos(1-(mass*Omega)**2/(2*N*N))
            frequencies.append(dict(
                mass=mass, angular_frequency_per_step=omega, frequency_physical=N*omega,
                continuum_target=mass*Omega, frozen_discrete_target=ideal,
                relative_continuum_error=N*omega/(mass*Omega)-1,
                relative_frozen_discrete_error=omega/ideal-1,
                official_positive_crossings=crossings,
                official_trace_sha256=trace_hash(samples[index][gear])))
        exact_rewind = engine.rewind(states[index], steps).same_as(seeds[index])
        if not exact_rewind:
            raise AssertionError("complete-state rewind failed")
        observations.append(dict(
            Omega=Omega, frequencies=frequencies, max_Omega_counter_drift=drifts[index],
            max_Omega_normalized_drift=drifts[index]/parameters["P"],
            min_Omega_counter=minima[index], positive_Omega_every_update=True,
            official_row_count=counts[index], official_readout_missing_nonzero=0,
            exact_rewind=exact_rewind, seed_sha256=exact_state_hash(seeds[index]),
            final_sha256=exact_state_hash(states[index]),
            signal_official_trace_sha256=trace_hash(samples[index][3])))
    ratios = []
    for index in range(2):
        ratio = (observations[1]["frequencies"][index]["angular_frequency_per_step"]
                 / observations[0]["frequencies"][index]["angular_frequency_per_step"])
        ratios.append(dict(mass=index+1, measured_clock_rate_ratio=ratio,
                           target_conformal_ratio=2, relative_ratio_error=ratio/2-1))
    if not signal_identical or not complete_signal_identical:
        raise AssertionError("canonical signal history depends on background")
    return dict(parameters=parameters, steps=steps, tensor_fingerprint=tensor.fingerprint,
                rank=tensor.rank, monomials=len(tensor.monomials),
                strict_support=not tensor.support_violations(),
                reciprocity=check_reciprocity(tensor).ok, clock_observations=observations,
                clock_ratios=ratios, massless_official_trace_identical=signal_identical,
                massless_complete_history_identical=complete_signal_identical)


def provenance(paths):
    paths = list(paths) + [ROOT / name for name in (
        "universe24/core/engine.py", "universe24/core/tensor.py", "universe24/observe/readout.py")]
    return dict(method="fresh public Engine runs and complete inverse runs",
                source_sha256={str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in paths},
                python_version=platform.python_version(), numpy_version=np.__version__,
                state_hash_format="universe24-state-values-v2")


def parser_for(description, filename):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--out", type=Path, default=ROOT/"runs"/"geometry"/filename)
    parser.add_argument("--refinements", nargs="+", type=int, choices=REFINEMENTS,
                        default=list(REFINEMENTS))
    return parser


def write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+"\n")


def main():
    parser = parser_for(__doc__, "conformal_metric.json")
    args = parser.parse_args()
    try:
        refinements = validate_refinements(args.refinements)
    except ValueError as error:
        parser.error(str(error))
    results = []
    for N in refinements:
        result = run_pair(N)
        results.append(result)
        print(json.dumps(dict(N=N, ratios=result["clock_ratios"],
                              max_metric_drift=max(row["max_Omega_normalized_drift"]
                                                   for row in result["clock_observations"]))), flush=True)
    report = dict(
        schema="conformal-metric-probe-v1",
        scope="Chosen reciprocal conformally coupled scalar toy in a finite-time probe and temporal-continuum limit; not the default ONE law, minimally coupled scalars, Einstein gravity or quantum mechanics.",
        readout="Positive-crossing periods of signed official quotients at node 0, with zero slots for missing rows; raw click counts are not proper time. Raw quotient equality is checked separately and never replaces the decoder.",
        law="u_chi=D chi+w Delta chi-mu_s H^2 chi; u_H=D H+w Delta H-sum mu_s H chi_s^2; mu_s=3m_s^2. Signal has mu=0. H evolves reciprocally, not as a prescribed background.",
        seed="L=3; b_H=P Omega; b_clock1=b_clock2=A Omega; b_signal=A*(1,-1,0)[x]; a=b; every r=D/2-1; Omega=1 or 2.",
        refinement="dt=1/N,A=N^6,P=A^2,Q=P^2*N^2,D=6Q,w=D/12; normalized Omega=H/P. Each refinement is a separately prepared fixed tensor.",
        signal_scope="Equality of canonical massless a,b,r histories across two homogeneous backgrounds; no emitter-receiver redshift or spatial continuum experiment.",
        refinements=list(refinements), results=results, provenance=provenance([Path(__file__).resolve()]))
    write_report(args.out, report)
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
