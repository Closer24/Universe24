"""Passive, amplitude-independent organization audit for retained clock links.

This is a deliberately limited structural proxy, not a universal complexity
measure. It has no runtime callback and cannot select a future board state.
The preregistration is issue #45 comment 6804437312.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from pathlib import Path
import random

from universe24.core import exact_json
from universe24.core.lattice import lattice
from universe24.system.bundle import load_bundle, state_from_data
from universe24.system.runtime import verify_run

INACTIVE = (2, 2)
PROTOCOL = {
    "schema": "universe24/clock-link-organization/1",
    "preregistered_issue": "https://github.com/Closer24/Universe24/issues/45#issuecomment-6804437312",
    "relation": "(sign(dot),sign(cross)); inactive if either endpoint is zero",
    "checkpoint_rule": "every complete saved state, including seed; no temporal subsampling",
    "minimum_repeat_sites": 2,
    "minimum_persistence_checkpoints": 2,
    "burst_rule": "strict interior local maximum of all four appended detector event counts; count >= 1",
    "minimum_bursts": 4,
    "growth_rule": "strictly increasing current persistent nonuniform motif count at every consecutive detected burst",
    "random_control_seeds": [101, 509, 2027],
    "interpretation": "fixed-gauge carrier phase-sign organization; no gauge-invariant or physical complexity claim",
}


def _sign(value):
    return (value > 0) - (value < 0)


def _vector(value):
    if len(value) != 2 or any(type(x) is not int for x in value):
        raise ValueError("carrier vectors must contain two exact Python integers")
    return tuple(value)


def phase_relation(left, right):
    """Exact directed relation, invariant under positive endpoint rescaling."""
    x, y = _vector(left)
    u, v = _vector(right)
    if (x == 0 and y == 0) or (u == 0 and v == 0):
        return INACTIVE
    return (_sign(x*u + y*v), _sign(x*v - y*u))


def cube_adjacency(side):
    grid = lattice(side)
    return tuple(tuple(grid.neighbour(node, d) for d in range(6)) for node in range(grid.N))


def phase_motifs(vectors, adjacency):
    """Six ordered face relations at each node; caller owns adjacency labels."""
    vectors = tuple(_vector(v) for v in vectors)
    if len(vectors) != len(adjacency):
        raise ValueError("carrier/adjacency lengths differ")
    if any(len(row) != 6 or any(type(n) is not int or not 0 <= n < len(vectors) for n in row)
           for row in adjacency):
        raise ValueError("six valid face neighbors are required for every node")
    return tuple(tuple(phase_relation(vectors[n], vectors[j]) for j in row)
                 for n, row in enumerate(adjacency))


def persistent_organization(previous, current):
    """Current repeated, persistent motifs; never a cumulative novelty counter."""
    if len(previous) != len(current):
        raise ValueError("checkpoint node counts differ")
    persistent = Counter(motif for old, motif in zip(previous, current)
                         if old == motif and len(set(motif)) > 1 and INACTIVE not in motif)
    accepted = {motif: count for motif, count in persistent.items() if count >= 2}
    return {
        "score": len(accepted),
        "persistent_sites": sum(accepted.values()),
        "motif_counts": [{"motif": [list(link) for link in motif], "sites": accepted[motif]}
                         for motif in sorted(accepted)],
    }


def trajectory_scores(vectors_by_checkpoint, adjacency):
    motifs = [phase_motifs(vectors, adjacency) for vectors in vectors_by_checkpoint]
    scores = [{"score": 0, "persistent_sites": 0, "motif_counts": []}]
    scores.extend(persistent_organization(old, new) for old, new in zip(motifs, motifs[1:]))
    previous_accepted = set()
    for score in scores:
        accepted = {tuple(tuple(link) for link in row["motif"]) for row in score["motif_counts"]}
        score["newly_persistent_motif_count"] = len(accepted - previous_accepted)
        previous_accepted = accepted
    return scores


def burst_growth(scores, event_counts):
    """Strict maxima only; endpoints and flat event plateaus are never bursts."""
    if len(scores) != len(event_counts) + 1:
        raise ValueError("one score for seed and every declared event window is required")
    bursts = [i+1 for i in range(1, len(event_counts)-1)
              if event_counts[i] >= 1 and event_counts[i] > event_counts[i-1]
              and event_counts[i] > event_counts[i+1]]
    values = [scores[step]["score"] for step in bursts]
    enough = len(bursts) >= PROTOCOL["minimum_bursts"]
    growth = enough and all(right > left for left, right in zip(values, values[1:]))
    return {"burst_steps": bursts, "scores_at_bursts": values,
            "at_least_four_bursts": enough, "strict_growth": growth,
            "status": "passed" if growth else "failed" if enough else "blocked",
            "reason": "criterion met on finite trace" if growth else
                      "current organization did not strictly increase" if enough else
                      "fewer than four strict interior apparatus-event maxima in declared trace"}


def _multiply(vectors, real, imag):
    return [(real*x-imag*y, imag*x+real*y) for x, y in vectors]


def control_audit():
    side = 7
    adjacent = cube_adjacency(side)
    nodes = side**3
    phases = ((1, 0), (0, 1), (-1, 0), (0, -1))
    # Spatial stripes are organized but stationary; neither organization nor a
    # changing common phase can imply strictly increasing organization.
    striped = [phases[lattice(side).coords(n)[0] % 4] for n in range(nodes)]
    motif = phase_motifs(striped, adjacent)
    scaled = [(x*(n+1), y*(n+1)) for n, (x, y) in enumerate(striped)]
    multiplied = _multiply(striped, 2, -3)
    perm = list(range(nodes)); random.Random(3301).shuffle(perm)
    inverse = {old: new for new, old in enumerate(perm)}
    relabelled_vectors = [striped[old] for old in perm]
    relabelled_adjacent = [tuple(inverse[j] for j in adjacent[old]) for old in perm]
    relabelled_motif = phase_motifs(relabelled_vectors, relabelled_adjacent)
    period = [_multiply(striped, *phases[t % 4]) for t in range(13)]
    periodic_scores = trajectory_scores(period, adjacent)
    synthetic_periodic_events = [0, 1, 0] * 4
    periodic = burst_growth(periodic_scores, synthetic_periodic_events)
    zeros = [(0, 0)] * nodes
    random_controls = []
    for seed in PROTOCOL["random_control_seeds"]:
        rng = random.Random(seed)
        fresh = [[rng.choice(phases) for _ in range(nodes)] for _ in range(8)]
        score = trajectory_scores(fresh, adjacent)
        frozen = trajectory_scores([fresh[0], fresh[0]], adjacent)[1]
        random_controls.append({"seed": seed, "fresh_scores": [s["score"] for s in score],
                                "frozen_random_score": frozen["score"],
                                "frozen_random_persistent_sites": frozen["persistent_sites"]})
    checks = {
        "positive_nodewise_amplitude_invariant": phase_motifs(scaled, adjacent) == motif,
        "common_nonzero_complex_multiplier_invariant": phase_motifs(multiplied, adjacent) == motif,
        "node_relabelling_with_adjacency_invariant": Counter(relabelled_motif) == Counter(motif),
        "zero_source_score_is_zero": persistent_organization(phase_motifs(zeros, adjacent), phase_motifs(zeros, adjacent))["score"] == 0,
        "four_periodic_peaks_do_not_pass_growth": periodic["at_least_four_bursts"] and not periodic["strict_growth"],
        "periodic_common_phase_has_constant_score_after_first_checkpoint": len({s["score"] for s in periodic_scores[1:]}) == 1,
    }
    assert all(checks.values()), checks
    return {"checks": checks, "periodic_scores": [s["score"] for s in periodic_scores],
            "periodic_growth_control": periodic, "random_controls": random_controls,
            "limitation": "Frozen random phase fields can contain repeated persistent motifs and score positively. This proxy is not a universal detector of meaningful organization."}


def audit_saved_run(run_path):
    """Inspect verified saved states; canonical event counts define all windows."""
    run = Path(run_path)
    runtime = verify_run(run)
    bundle = load_bundle(run / "bundle")
    phi, chi = [bundle.tensor.gear_index(name) for name in ("field.phi", "field.chi")]
    detector_indices = {int(c["index"]) for c in bundle.channels if int(c["index"]) >= 44}
    expected_names = ("observer.local_intensity", "observer.link_x", "observer.link_y", "observer.link_z")
    if (bundle.tensor.G != 48 or len(detector_indices) != 4
            or tuple(bundle.tensor.names[44:]) != expected_names
            or bundle.model.get("id") != "proposal-clock-link-records"):
        raise ValueError("expected the declared 44+4 research allocation")
    states = [bundle.seed]
    with gzip.open(run / "full_trace.jsonl.gz", "rt", encoding="utf-8") as stream:
        states.extend(state_from_data(exact_json.loads(line)["after"]) for line in stream)
    vectors = [[(int(state.b[phi, n]), int(state.b[chi, n])) for n in range(state.N)] for state in states]
    scores = trajectory_scores(vectors, cube_adjacency(bundle.seed.L))
    event_counts = [0] * runtime["steps"]
    with gzip.open(run / "clicks.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            event = exact_json.loads(line)
            if event["channel"] in detector_indices:
                event_counts[event["step"]-1] += 1
    feedback_terms = sum(term.target < 44 and any(factor.gear >= 44 for factor in term.factors)
                         for term in bundle.tensor.monomials)
    return {"bundle_id": bundle.bundle_id, "run_id": runtime["run_id"],
            "tensor_hash": bundle.tensor.fingerprint, "steps": runtime["steps"],
            "channels": bundle.tensor.G, "maximum_integer_bits_by_step": runtime["maximum_integer_bits_by_step"],
            "phase_link_scores": scores, "detector_event_counts": event_counts,
            "growth": burst_growth(scores, event_counts),
            "apparatus_to_base_tensor_terms": feedback_terms,
            "causal_selection": {"status": "blocked" if feedback_terms == 0 else "not_tested",
                "reason": "The appended detector channels do not feed carrier evolution. Recorded history is not a complexity-selection law."
                          if feedback_terms == 0 else "Feedback terms exist, but a controlled complexity-selection test has not been supplied."},
            "physical_burst_growth": "not_established",
            "exact_saved_replay": True,
            "gauge_scope": "Raw carrier quadratic signs are interpreted in the prepared common-sign gauge; no local gauge invariance is claimed."}


def audit(out, run_paths=()):
    output = Path(out)
    output.mkdir(parents=True, exist_ok=True)
    report = {"protocol": PROTOCOL, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "controls": control_audit(), "board_runs": [audit_saved_run(path) for path in run_paths],
              "previous_pr43_failures": {"status": "preserved", "rerun_here": False, "failed_cases": 16,
                  "source": "https://github.com/Closer24/Universe24/pull/43"},
              "claim": "Finite phase-sign motif audit only; neither Born, Bell, physical proper time nor complexity selection is derived."}
    (output / "complexity.json").write_text(exact_json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/clock_links/complexity"))
    parser.add_argument("--run", type=Path, action="append", default=[])
    args = parser.parse_args(argv)
    result = audit(args.out, args.run)
    print(exact_json.dumps({"checks": result["controls"]["checks"], "board_runs": len(result["board_runs"])}))


if __name__ == "__main__":
    main()
