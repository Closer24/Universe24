"""Optional interacting conformal-clock comparison using one fixed Rule3 law.

Run from the repository root:
    PYTHONPATH=. python experiments/geometry/conformal_nonlinear_clock.py

The fixed n <-> 2n-1 match is determined by quotient time-centering, not fitted.
It uses nominal constant-background proper time; actual Omega drift is measured.
"""
from __future__ import annotations

import json
from pathlib import Path

from universe24.core import Engine
from universe24.core.reciprocity import check_reciprocity

from experiments.geometry.conformal_metric_probe import (
    BACKGROUNDS, build, exact_state_hash, metric_diagnostics, parser_for, prepare,
    provenance, read_samples, trace_hash, validate_refinements, write_report,
)


def run_pair(N):
    tensor, parameters = build(N, interaction=True)
    engine = Engine(tensor, parameters["Q"])
    seeds = [prepare(tensor, parameters, Omega) for Omega in BACKGROUNDS]
    # PREPARATION ONLY: Taylor prior for zero initial velocity, including the
    # quartic acceleration. Nothing writes a counter after evolution starts.
    for state, Omega in zip(seeds, BACKGROUNDS):
        for gear, mass in ((1, 1), (2, 2)):
            numerator = parameters["A"]*Omega**3*(mass*mass+1)
            correction, remainder = divmod(numerator, 2*N*N)
            if remainder:
                raise AssertionError("Taylor prior is not exactly integer")
            state.a[gear] = state.b[gear]-correction
    steps = 10*N+1
    traces, observations = [], []
    for seed, Omega in zip(seeds, BACKGROUNDS):
        state = seed.copy()
        samples = {1: [], 2: []}
        drift, minimum, count = 0, Omega*parameters["P"], 0
        for tick in range(1, steps+1):
            following = engine.step(state)
            recorded, rows = read_samples(engine, state, following, tick, (1, 2))
            count += rows
            for gear, value in recorded.items():
                samples[gear].append(value)
            drift, minimum = metric_diagnostics(
                following, Omega*parameters["P"], drift, minimum)
            state = following
        rewind = engine.rewind(state, steps).same_as(seed)
        if not rewind:
            raise AssertionError("complete-state rewind failed")
        observations.append(dict(
            Omega=Omega, seed_sha256=exact_state_hash(seed), final_sha256=exact_state_hash(state),
            exact_rewind=rewind, max_Omega_counter_drift=drift,
            max_Omega_normalized_drift=drift/parameters["P"], min_Omega_counter=minimum,
            positive_Omega_every_update=True, official_row_count=count,
            official_readout_missing_nonzero=0,
            official_trace_sha256={str(gear): trace_hash(values) for gear, values in samples.items()}))
        traces.append(samples)
    # ell_n = b_n + b_(n-2), centered at time (n-1)/N. Compare the
    # Omega=2 quotient at n with Omega=1 at 2n-1 and divide canonical amplitude.
    numerators = [max(abs(traces[1][gear][n-1]-2*traces[0][gear][2*n-2])
                      for n in range(1, 5*N+1)) for gear in (1, 2)]
    denominator = 4*parameters["A"]
    errors = [numerator/denominator for numerator in numerators]
    # t <= (5N-1)/N in the Omega=2 run; comparison time is 2t in Omega=1.
    mismatch_numerator = ((5*N-1)*(observations[1]["max_Omega_counter_drift"]
                                  + 2*observations[0]["max_Omega_counter_drift"]))
    mismatch_denominator = N*parameters["P"]
    return dict(
        N=N, parameters=parameters, steps_per_run=steps,
        proper_time_matched_max_absolute_trace_errors=errors,
        exact_error_numerators=numerators, exact_error_denominator=denominator,
        nominal_proper_time_mismatch_bound=mismatch_numerator/mismatch_denominator,
        exact_mismatch_bound_numerator=mismatch_numerator,
        exact_mismatch_bound_denominator=mismatch_denominator,
        exact_rewinds=[row["exact_rewind"] for row in observations],
        clock_observations=observations, rank=tensor.rank,
        strict_support=not tensor.support_violations(),
        reciprocity=check_reciprocity(tensor).ok, monomials=len(tensor.monomials),
        tensor_fingerprint=tensor.fingerprint)


def main():
    parser = parser_for(__doc__, "conformal_nonlinear_clock.json")
    args = parser.parse_args()
    try:
        refinements = validate_refinements(args.refinements)
    except ValueError as error:
        parser.error(str(error))
    results = []
    for N in refinements:
        result = run_pair(N)
        results.append(result)
        print(json.dumps(dict(N=N, proper_time_errors=result["proper_time_matched_max_absolute_trace_errors"],
                              nominal_time_mismatch_bound=result["nominal_proper_time_mismatch_bound"])), flush=True)
    report = dict(
        schema="conformal-nonlinear-clock-v1",
        scope="Two coupled nonlinear scalar clocks under a newly chosen reciprocal rank-four tensor. Finite-time temporal refinement and controlled probe limit; not the default law, general geometry, quantum statistics or Einstein gravity.",
        law="Common conformal tensor plus u_clock1-=3A^2 clock1 clock2^2 and u_clock2-=3A^2 clock2 clock1^2. No Omega factor multiplies this canonical quartic; metric source still evolves reciprocally.",
        seed="Base conformal seed; before evolution set a_clock_s=b_clock_s-A*Omega^3*(m_s^2+1)/(2N^2), exactly integer. All other a,b,r unchanged.",
        comparison="For n=1..5N compare official ell_Omega2(n)/(4A) with ell_Omega1(2n-1)/(2A). Missing rows contribute zero. No fitted shift, rescaling, or runtime correction.",
        metric_drift_scope="Nominal constant-background time matching, not integration and retiming of evolving Omega. Actual proper-time mismatch is bounded by t*drift_2+2t*drift_1; t_max=(5N-1)/N.",
        refinements=list(refinements), results=results,
        provenance=provenance([Path(__file__).resolve(), Path(__file__).with_name("conformal_metric_probe.py").resolve()]))
    write_report(args.out, report)
    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
