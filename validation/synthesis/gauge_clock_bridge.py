"""Exact readout/transport bridge checks, not a new accepted apparatus law.

Run: python -m validation.synthesis.gauge_clock_bridge --out runs/synthesis/gauge-clock.json
All ratios are passive. The projective source dynamics is unchanged.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice
from validation.geometry.team48 import refinement_integer_projective as projective
from validation.geometry.team48 import temporal_repair_projective as temporal

SOURCE_PIN = "621fc1f55800e50e1db5f6a30ce24bb83716a49a"
EDGE = (1, 0, 0)


def multiply(z, w):
    return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]


def conjugate(z):
    return z[0], -z[1]


def norm(z):
    return z[0]*z[0]+z[1]*z[1]


def coherent(z, w, link=(F(1), F(0))):
    transported = multiply(link, w)
    return norm((z[0]+transported[0], z[1]+transported[1]))


def raw_terms(tensor):
    return [(tensor.gears[m.target].name, m.coeff,
             tuple((tensor.gears[f.gear].name, f.offset, f.field) for f in m.factors))
            for m in tensor.monomials]


def rational_controls():
    rotations = [(F(1), F(0)), (F(0), F(1)), (F(3, 5), F(4, 5)),
                 (F(5, 13), -F(12, 13))]
    cases = 0
    for components in product(range(-2, 3), repeat=4):
        z, w = tuple(map(F, components[:2])), tuple(map(F, components[2:]))
        dot = z[0]*w[0]+z[1]*w[1]
        cross = z[0]*w[1]-z[1]*w[0]
        assert dot*dot+cross*cross == norm(z)*norm(w)
        for gx, gy in product(rotations, repeat=2):
            zp, wp = multiply(gx, z), multiply(gy, w)
            link = multiply(gx, conjugate(gy))
            assert coherent(zp, wp, link) == coherent(z, w)
            assert coherent(multiply(gx, z), multiply(gx, w)) == coherent(z, w)
            cases += 1
    z = w = (F(1), F(0))
    untransported = coherent(z, multiply(rotations[1], w))
    assert coherent(z, w) == 4 and untransported == 2
    assert coherent(z, multiply(rotations[1], w), conjugate(rotations[1])) == 4
    # A rational Cayley link is normalized but is not a polynomial in its parameter.
    t = F(2, 3)
    cayley = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
    assert norm(cayley) == 1
    naive_link_step = (F(1), F(1, 4))
    assert norm(naive_link_step) == F(17, 16)
    return {"signed_rational_gauge_cases": cases,
            "bare_local_rotation_counterexample": {"before": 4, "after": 2,
                                                    "transported_after": 4},
            "cayley_example": list(map(str, cayley)),
            "naive_euler_rotation_norm_squared": str(norm(naive_link_step)),
            "full_source_gauge_covariance": "not_tested"}


def projective_receiver_bridge():
    """Append one audit-only fixed-gauge receiver, compare all source states."""
    program = projective.compile_projective(temporal.NAMES, temporal.BUILDER,
                                            dt=F(1, 8), dx=1, degree=3)
    seed = temporal.prepared(program, 64)
    phi = 1+program.fields.index("phi")
    chi = 1+program.fields.index("chi")
    for node in range(27):
        seed.b[phi, node] = (node % 5-2)*8
        seed.b[chi, node] = (node % 7-3)*8
    receiver = "audit.projective_face_numerator"
    names = [program.tensor.gears[i].name for i in (phi, chi)]
    terms = raw_terms(program.tensor)
    for name in names:
        for offset in (ZERO, EDGE):
            terms.append((receiver, 3, ((name, offset, "b"),)*2))
        terms.append((receiver, 6, ((name, ZERO, "b"), (name, EDGE, "b"))))
    tensor = Tensor([*program.tensor.gears, GearType(receiver, label="audit")],
                    terms, strict_support=True)
    assert tensor.G == 45 and not tensor.support_violations()
    state = State(3, np.vstack((seed.a, np.zeros((1, 27), dtype=object))),
                  np.vstack((seed.b, np.zeros((1, 27), dtype=object))),
                  np.vstack((seed.r, np.array([[n % 6 for n in range(27)]], dtype=object))))
    start = state
    source, source_engine, engine = seed, Engine(program.tensor), Engine(tensor)
    neighbors = lattice(3).shift_index(EDGE)
    checked, wrong_slice_examples, bits = 0, 0, []
    for tick in range(3):
        following, source_next = engine.step(state), source_engine.step(source)
        assert State(3, following.a[:44], following.b[:44], following.r[:44]).same_as(source_next)
        assert engine.inverse_step(following).same_as(state)
        d = int(state.b[0, 0])
        for node, neighbor in enumerate(neighbors):
            z = tuple(F(int(state.b[i, node]), d) for i in (phi, chi))
            w = tuple(F(int(state.b[i, neighbor]), d) for i in (phi, chi))
            quotient = int(following.b[44, node])+int(state.a[44, node])
            assert F(quotient, d*d) == coherent(z, w)
            assert following.r[44, node] == state.r[44, node]
            if quotient and F(quotient, int(following.b[0, node])**2) != coherent(z, w):
                wrong_slice_examples += 1
            checked += 1
        bits.append(following.max_abs().bit_length())
        state, source = following, source_next
    assert engine.rewind(state, 3).same_as(start)
    assert wrong_slice_examples > 0
    return {"channels": 45, "source_channels_unchanged": 44, "steps": 3,
            "node_transition_readouts_checked": checked, "source_projection_exact": True,
            "complete_rewind": True, "all_six_receiver_carries": True,
            "before_denominator_required_counterexamples": wrong_slice_examples,
            "maximum_retained_bits": bits, "tensor_sha256": tensor.fingerprint,
            "scope": "one-way fixed-gauge numerator receiver; no gauge transport/backreaction"}


def cubic_transport_control():
    """Restricted static one-edge transport: explicit cubic numerator, six slots.

    This standalone algebra control is not appended to the physical source.
    A general dynamical normalized-link update is deliberately absent.
    """
    names = ("phi", "chi", "denominator", "link_real", "link_imag", "receiver")
    gears = [GearType(n, label="audit", link=0 if n.startswith("link_") else None)
             for n in names]
    terms = [(n, 6, ((n, ZERO, "b"),)) for n in names[:-1]]
    for name in names[:2]:
        for offset in (ZERO, EDGE):
            terms.append(("receiver", 3, (("denominator", ZERO, "b"),
                                          (name, offset, "b"), (name, offset, "b"))))
    for left, right, link, sign in (("phi", "phi", "link_real", 1),
                                    ("chi", "chi", "link_real", 1),
                                    ("phi", "chi", "link_imag", -1),
                                    ("chi", "phi", "link_imag", 1)):
        terms.append(("receiver", 6*sign, ((link, ZERO, "b"),
                                          (left, ZERO, "b"), (right, EDGE, "b"))))
    tensor = Tensor(gears, terms, strict_support=True)
    assert tensor.rank-1 == 3 and not tensor.support_violations()
    b = np.array([[n % 5-2 for n in range(27)], [n % 7-3 for n in range(27)],
                  [5]*27, [3]*27, [4]*27, [0]*27], dtype=object)
    r = np.array([[int((i*27+n) % 6) for n in range(27)] for i in range(6)], dtype=object)
    state = State(3, b.copy(), b, r)
    following = Engine(tensor).step(state)
    for node, neighbor in enumerate(lattice(3).shift_index(EDGE)):
        z, w = tuple(F(int(b[i, node]), 5) for i in (0, 1)), tuple(F(int(b[i, neighbor]), 5) for i in (0, 1))
        quotient = int(following.b[5, node])+int(state.a[5, node])
        assert F(quotient, 125) == coherent(z, w, (F(3, 5), F(4, 5)))
    assert Engine(tensor).inverse_step(following).same_as(state)
    return {"restricted_control_channels": 6, "degree": 3, "strict_support": True,
            "nodes_checked": 27, "inverse": True, "link_dynamics": "static prepared control only",
            "append_one_axis_to_44": 47, "append_three_axes_plus_one_receiver_to_44": 51,
            "replace_three_existing_A_with_six_links_plus_one_receiver": 48,
            "replacement_dynamics": "not_constructed; rederivation required"}


def proper_time_control():
    velocity = F(3, 5)
    tau_squared = 1-velocity*velocity
    assert tau_squared == F(16, 25) and F(4, 5)**2 == tau_squared
    return {"metric": "Minkowski, lapse 1, zero shift",
            "coordinate_interval": "1", "rest_proper_interval": "1",
            "moving_velocity": str(velocity), "moving_proper_interval": "4/5",
            "equal_coordinate_phase_is_not_equal_proper_phase": True,
            "autonomous_clock_calibration": "not_tested"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("runs/synthesis/gauge-clock.json"))
    args = parser.parse_args()
    report = {"schema": "universe24/gauge-clock-bridge/1", "source_pin": SOURCE_PIN,
              "status": "passed_scoped_algebra_and_bridge_controls",
              "scope": "passive projective scale correction and restricted transport algebra",
              "command": "python -m validation.synthesis.gauge_clock_bridge "+" ".join(sys.argv[1:]),
              "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_sha256": {str(Path(module.__file__).relative_to(Path(__file__).resolve().parents[2])):
                                hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
                                for module in (projective, temporal)},
              "rational_controls": rational_controls(),
              "projective_receiver_bridge": projective_receiver_bridge(),
              "cubic_transport_control": cubic_transport_control(),
              "proper_time_control": proper_time_control(),
              "physical_acceptance": "not_established",
              "limits": ["No dynamic normalized gauge link or reciprocal backreaction",
                         "No full source gauge covariance test",
                         "No operational clock, Born detector, or complexity-selection claim",
                         "One-way fixed-gauge bridge seed is off Einstein constraints"]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
