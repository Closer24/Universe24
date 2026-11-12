"""Executable countercontrols for historical gauge candidates.

These checks run the existing fixed-six Engine; they do not change its law,
normalize links, repair charge, or interpret arithmetic click classes as
physical detector outcomes. A reproduced counterexample passes its audit
while the disproved physical claim remains failed.
"""
from __future__ import annotations

from itertools import product
from math import factorial

from universe24.core import Engine
from universe24.core.tensor import LocalityError, compose, vacuum_map
from universe24.layers.gauge import ALGEBRAS, build_u1
from universe24.observe.gauge import GaugeView


def _require(condition, message):
    if not condition:
        raise AssertionError(message)


def _fixture(*, kappa, mass, lam):
    block = build_u1(A=1, kappa=kappa, mass=mass, lam=lam, use_P=False)
    tensor = compose(block, strict_support=True)
    engine = Engine(tensor)
    state = engine.vacuum(3, vacuum_map(block))
    view = GaugeView(tensor, block.params, name="u1")
    _require(tensor.G == 8 and not tensor.support_violations(),
             "countercontrol must remain an eight-channel single-edge tensor")
    return tensor, engine, state, view


def _triple(state, gear, node=0):
    return [int(value) for value in state.gear(gear, node)]


def _scalar_rule(a, b, r, u):
    """Direct scalar oracle, independent of Engine vectorization and observers."""
    quotient, remainder = divmod(2*u+r, 6)
    return [b, quotient-a, remainder]


def _peak_bits(*states):
    return max(abs(int(value)).bit_length()
               for state in states for bank in (state.a, state.b, state.r)
               for value in bank.flat)


def unit_link_drift_control():
    """Two normalized input histories do not make the spring constraint exact."""
    tensor, engine, state, view = _fixture(kappa=0, mass=0, lam=4)
    real = tensor.gear_index("u1.Ux_re")
    imag = tensor.gear_index("u1.Ux_im")
    # Stored links are deviations: physical U = (1 + W_re) + i W_im.
    # U(t-1)=1 and U(t)=i are both exactly unit length. At U(t), the
    # radial spring vanishes, so u=6W and U(t+1)=2i-1.
    state.b[real, 0], state.b[imag, 0] = -1, 1
    _require(all(int(x) == 1 for field in ("a", "b")
                 for x in view.link_norm2(state, field).flat),
             "both complete input link histories must be normalized")
    following = engine.step(state)
    _require(_triple(following, real) == _scalar_rule(0, -1, 2, -6),
             "real link component disagrees with scalar recurrence")
    _require(_triple(following, imag) == _scalar_rule(0, 1, 2, 6),
             "imaginary link component disagrees with scalar recurrence")
    physical = [int(x) for x in view.link_matrix(following, 0)[:, 0]]
    _require(physical == [-1, 2] and sum(x*x for x in physical) == 5,
             "expected explicit unit-link counterexample was not reproduced")
    _require(int(view.link_norm2(following)[0, 0]) == 5,
             "passive norm diagnostic disagrees with independent squared norm")
    _require(engine.inverse_step(following).same_as(state),
             "complete link-drift state must rewind exactly")
    return {
        "audit_status": "passed",
        "claim": "unit-link manifold preserved for every normalized two-history seed",
        "claim_status": "failed",
        "tensor_sha256": tensor.fingerprint,
        "channels": tensor.G,
        "physical_link_previous": [1, 0],
        "physical_link_current": [0, 1],
        "physical_link_next": physical,
        "norm_squared": [1, 1, 5],
        "peak_retained_integer_bits": _peak_bits(state, following),
        "complete_inverse": True,
        "scope": "existing unconstrained complex-link spring; no general no-go theorem",
    }


def gauss_carry_control():
    """A zero residual of the carry-aware identity is not constant bare charge."""
    tensor, engine, state, view = _fixture(kappa=0, mass=1, lam=0)
    real = tensor.gear_index("u1.psi_re")
    imag = tensor.gear_index("u1.psi_im")
    state.b[real, 0], state.b[imag, 0] = 1, 4
    state.r[real, 0], state.r[imag, 0] = 0, 0
    following = engine.step(state)
    _require(_triple(following, real) == _scalar_rule(0, 1, 0, 1),
             "real matter component disagrees with scalar recurrence")
    _require(_triple(following, imag) == _scalar_rule(0, 4, 0, 4),
             "imaginary matter component disagrees with scalar recurrence")
    # i(x,y)=(-y,x). These values are calculated directly from the two
    # explicit component histories, not inferred from gauss_check's status.
    a0 = [int(state.a[g, 0]) for g in (real, imag)]
    b0 = [int(state.b[g, 0]) for g in (real, imag)]
    b1 = [int(following.b[g, 0]) for g in (real, imag)]
    dr = [int(state.r[g, 0])-int(following.r[g, 0]) for g in (real, imag)]
    before = 6*(-a0[0]*b0[1]+a0[1]*b0[0])
    after = 6*(-b0[0]*b1[1]+b0[1]*b1[0])
    carry = -b0[0]*dr[1]+b0[1]*dr[0]
    _require((before, after, carry) == (0, -6, -6),
             "bare charge/carry witness changed")
    generator = (0, 1)
    _require(int(view.charge(state, generator)[0]) == before and
             int(view.charge(following, generator)[0]) == after and
             int(view.remainder_term(state, following, generator)[0]) == carry,
             "gauge observers disagree with explicit two-component algebra")
    balance = view.gauss_check([state, following])
    _require(balance["checks"] == 27 and balance["failures"] == 0,
             "carry-aware local balance must pass at every node")
    _require(engine.inverse_step(following).same_as(state),
             "complete carry state must rewind exactly")
    return {
        "audit_status": "passed",
        "claim": "bare displayed Gauss charge is unchanged on every legal seed",
        "claim_status": "failed",
        "tensor_sha256": tensor.fingerprint,
        "channels": tensor.G,
        "bare_charge_before": before,
        "bare_charge_after": after,
        "retained_carry_source": carry,
        "local_balance_residual": after-before-carry,
        "carry_balance": balance,
        "peak_retained_integer_bits": _peak_bits(state, following),
        "complete_inverse": True,
        "scope": "exact carry-aware identity passes; no conserved replacement charge is derived",
    }


def finite_group_control():
    """The historical integer action uses finite subgroups, not all Lie elements."""
    gaussian = {v for v in product((-1, 0, 1), repeat=2) if sum(x*x for x in v) == 1}
    quaternion = {v for v in product((-1, 0, 1), repeat=4) if sum(x*x for x in v) == 1}
    _require(set(ALGEBRAS["u1"].group) == gaussian and len(gaussian) == 4,
             "Gaussian integer units must be exactly Z4")
    _require(set(ALGEBRAS["su2"].group) == quaternion and len(quaternion) == 8,
             "integer unit quaternions must be exactly Q8")
    matrices = ALGEBRAS["su3"].group
    # A Gaussian-integer unitary 3x3 matrix has one Gaussian unit in
    # each row and column. The determinant fixes one of its three phases.
    expected_matrices = factorial(3)*4**2
    _require(len(matrices) == len(set(matrices)) == expected_matrices,
             "determinant-one monomial subgroup must contain 96 elements")
    for entries in matrices:
        matrix = [[(entries[2*(3*i+j)], entries[2*(3*i+j)+1])
                   for j in range(3)] for i in range(3)]
        _require(all(sum(re*re+im*im for re, im in row) == 1 for row in matrix),
                 "integer subgroup matrix row is not a unit row")
        _require(all(sum(matrix[i][j][0]**2+matrix[i][j][1]**2 for i in range(3)) == 1
                     for j in range(3)), "integer subgroup matrix column is not a unit column")
        # Determinant, using Gaussian-integer arithmetic rather than floats.
        def mul(z, w):
            return z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0]
        determinant = [0, 0]
        for permutation, sign in (((0, 1, 2), 1), ((1, 2, 0), 1), ((2, 0, 1), 1),
                                  ((0, 2, 1), -1), ((2, 1, 0), -1), ((1, 0, 2), -1)):
            value = mul(mul(matrix[0][permutation[0]], matrix[1][permutation[1]]),
                        matrix[2][permutation[2]])
            for component in range(2):
                determinant[component] += sign*value[component]
        _require(determinant == [1, 0], "integer subgroup determinant must equal one")
    return {
        "audit_status": "passed",
        "exact_integer_group_sizes": {"u1_Z4": 4, "su2_Q8": 8, "su3_monomial": 96},
        "full_continuous_group_action_status": "not_established",
        "scope": "counts existing integer actions; polynomial continuous identities are a separate claim",
    }


def two_path_locality_control():
    """Existing P mediators violate physical single-edge support despite 20 slots."""
    parameters = dict(A=1, kappa=1, mass=1, lam=4, use_P=True, kappa_P=6)
    block = build_u1(**parameters)
    tensor = compose(block)
    violations = tensor.support_violations()
    _require(tensor.G == 20 and len(violations) == 120,
             "historical U1 two-path census changed")
    try:
        compose(block, strict_support=True)
    except LocalityError as error:
        rejection = str(error)
    else:
        raise AssertionError("strict physical support must reject this two-path candidate")
    monomial = violations[0]
    support = tensor.physical_support(monomial)
    _require(len(support) > 2, "counterexample must touch more than a single face edge")
    return {
        "audit_status": "passed",
        "claim": "historical U1 two-path tensor meets strict physical single-edge support",
        "claim_status": "failed",
        "tensor_sha256": tensor.fingerprint,
        "parameters": parameters,
        "channels": tensor.G,
        "support_violation_count": len(violations),
        "strict_constructor_rejected": True,
        "rejection": rejection,
        "witness": {
            "target": tensor.names[monomial.target],
            "factors": [[tensor.names[f.gear], list(f.offset), f.field] for f in monomial.factors],
            "physical_support": [list(point) for point in support],
        },
        "scope": "counterexample to direct reuse; staged legal loop constructions remain possible",
    }


def click_class_gauge_control():
    """A real local pi gauge transformation exchanges an actual C1 and C2 click."""
    tensor, engine, state, view = _fixture(kappa=1, mass=1, lam=0)
    gear = tensor.gear_index("u1.psi_im")
    state.b[gear, 0], state.r[gear, 0] = 4, 0
    gauge = [(1, 0)]*state.N
    gauge[0] = (-1, 0)
    transformed = view.gauge_map(state, gauge)
    following = engine.step(state)
    transformed_following = engine.step(transformed)
    _require(transformed_following.same_as(view.gauge_map(following, gauge)),
             "the whole retained transition must be locally Z4 covariant")
    _require(view.gauge_map(transformed, gauge).same_as(state),
             "the complete local pi map must be an involution")
    _require(_triple(state, gear) == [0, 4, 0] and
             _triple(transformed, gear) == [0, -4, 4], "pi-transformed seed changed")
    _require(_triple(following, gear) == _scalar_rule(0, 4, 0, 4) and
             _triple(transformed_following, gear) == _scalar_rule(0, -4, 4, -4),
             "click witness disagrees with direct scalar Rule3")

    def witness_click(before, after):
        clicks = engine.clicks(before, after)
        matching = [i for i in range(len(clicks))
                    if int(clicks.gear[i]) == gear and int(clicks.node[i]) == 0]
        _require(len(matching) == 1, "witness must be an actual official Engine click")
        i = matching[0]
        return {"class": f"C{int(clicks.kind[i])}",
                "quotient": int(clicks.quotient[i]), "changed": bool(clicks.changed[i])}

    first = witness_click(state, following)
    second = witness_click(transformed, transformed_following)
    _require(first == {"class": "C1", "quotient": 1, "changed": True} and
             second == {"class": "C2", "quotient": -1, "changed": True},
             "local gauge pi must exchange the actual C1/C2 witness")
    for original, mapped in ((state, transformed), (following, transformed_following)):
        for field in ("a", "b"):
            z = view.phys(getattr(original, field), view.matter)
            gz = view.phys(getattr(mapped, field), view.matter)
            _require(all(int(x) == int(y) for x, y in
                         zip((z*z).sum(axis=0), (gz*gz).sum(axis=0))),
                     "matter norm must be unchanged by the local gauge map")
        for axes in ((0, 1), (0, 2), (1, 2)):
            _require(all(int(x) == int(y) for x, y in
                         zip(view.wilson(original, *axes), view.wilson(mapped, *axes))),
                     "Wilson observables must be gauge invariant")
    _require(engine.inverse_step(following).same_as(state) and
             engine.inverse_step(transformed_following).same_as(transformed),
             "both complete gauge-related transitions must rewind")
    return {
        "audit_status": "passed",
        "claim": "raw C1/C2 arithmetic labels are invariant under the candidate's local gauge action",
        "claim_status": "failed",
        "tensor_sha256": tensor.fingerprint,
        "channels": tensor.G,
        "local_gauge": {"node": 0, "phase": [-1, 0], "other_nodes": [1, 0]},
        "gear": tensor.names[gear],
        "before": _triple(state, gear),
        "after": _triple(following, gear),
        "gauge_before": _triple(transformed, gear),
        "gauge_after": _triple(transformed_following, gear),
        "original_click": first,
        "gauge_click": second,
        "complete_state_covariance": True,
        "matter_norms_and_wilson_invariant": True,
        "peak_retained_integer_bits": _peak_bits(state, following, transformed, transformed_following),
        "complete_inverse": True,
        "scope": "time-independent local Z4 audit; raw classes need a gauge-invariant apparatus interpretation",
    }


def obstruction_audit():
    """Return deterministic evidence; passing audits retain failed claim statuses."""
    return {
        "schema": "universe24/gauge-loop-obstructions/1",
        "audit_status": "passed",
        "unit_link_drift": unit_link_drift_control(),
        "gauss_carry_balance": gauss_carry_control(),
        "finite_integer_groups": finite_group_control(),
        "two_path_locality": two_path_locality_control(),
        "click_class_gauge_swap": click_class_gauge_control(),
        "physical_acceptance": "not_established",
    }
