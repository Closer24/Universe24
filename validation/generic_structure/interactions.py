"""Source-only compiler: one local polynomial potential -> every response.

Run: python -m validation.generic_structure.interactions
No runtime solver, extra channel, energy theorem or Einstein default is added.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
from typing import Mapping, Sequence

import numpy as np

from universe24.core import Engine, GearType, State, Tensor, check_reciprocity


ROOT = Path(__file__).resolve().parents[2]
ZERO = (0, 0, 0)
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


@dataclass(frozen=True, order=True)
class Variable:
    gear: str
    offset: tuple[int, int, int] = ZERO


@dataclass(frozen=True)
class PotentialTerm:
    coefficient: int | Fraction
    factors: tuple[Variable, ...] = ()


@dataclass(frozen=True)
class CompiledInteraction:
    tensor: Tensor
    potential: tuple[PotentialTerm, ...]
    certificate: dict


def _offset(offset):
    if not isinstance(offset, (tuple, list)) or len(offset) != 3 or any(type(v) is not int for v in offset):
        raise TypeError("offset must contain three exact integers")
    return tuple(offset)


def _add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def _subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def _support(gears, factors):
    points = set()
    for factor in factors:
        points.add(factor.offset)
        gear = gears[factor.gear]
        if gear.link is not None:
            points.add(_add(factor.offset, AXES[gear.link]))
    points = sorted(points)
    if len(points) > 2 or (len(points) == 2 and sum(abs(v) for v in _subtract(points[1], points[0])) != 1):
        raise ValueError("potential physical support must be one node or one face, including link endpoints")
    return points


def _term_record(term):
    coefficient = Fraction(term.coefficient)
    return {"coefficient": [coefficient.numerator, coefficient.denominator],
            "factors": [[v.gear, list(v.offset)] for v in term.factors]}


def compile_potential(gears: Sequence, potential: Sequence[PotentialTerm], *,
                      owners: Mapping[str, str] | None = None,
                      add_inertial: bool = True) -> CompiledInteraction:
    """Compile u_i=6b_i+s_i*dPhi/db_i, or omit 6b when requested.

    Phi is the sum of supplied translated unit-cell monomials over all nodes.
    Rational construction coefficients are allowed only when the complete
    response coefficients are exact integers. All factors are current b.
    Each term is normalized up to translation before derivative collection.
    Link metadata contributes both endpoints to physical-support checks.
    """
    if type(add_inertial) is not bool:
        raise TypeError("add_inertial must be bool")
    shell = Tensor(gears, [], strict_support=True)
    if shell.G > 48:
        raise ValueError(f"complete channel budget exceeded: {shell.G} > 48")
    gear_map = {g.name: g for g in shell.gears}
    if owners is None:
        owners = {name: "interaction" for name in shell.names}
    if set(owners) != set(shell.names) or any(type(value) is not str or not value for value in owners.values()):
        raise ValueError("one explicit nonempty owner required for every supplied channel")

    normalized = defaultdict(Fraction)
    for term in potential:
        if not isinstance(term, PotentialTerm):
            raise TypeError("potential entries must be PotentialTerm values")
        if type(term.coefficient) not in (int, Fraction):
            raise TypeError("potential coefficients must be exact int or Fraction")
        if len(term.factors) > 4:
            raise ValueError("potential degree exceeds four")
        factors = []
        for variable in term.factors:
            if not isinstance(variable, Variable) or variable.gear not in gear_map:
                raise ValueError("every potential variable must name a declared channel")
            factors.append(Variable(variable.gear, _offset(variable.offset)))
        points = _support(gear_map, factors)
        anchor = points[0] if points else ZERO
        key = tuple(sorted(Variable(v.gear, _subtract(v.offset, anchor)) for v in factors))
        normalized[key] += Fraction(term.coefficient)
    canonical = tuple(PotentialTerm(coefficient, factors)
                      for factors, coefficient in sorted(normalized.items()) if coefficient)

    responses = defaultdict(Fraction)
    occurrence_count = 0
    for term in canonical:
        for index, target in enumerate(term.factors):
            # Removing each occurrence handles repeated variables and their
            # exact multiplicity. Shift the selected target's storage node to 0.
            factors = tuple(sorted((v.gear, _subtract(v.offset, target.offset), "b")
                                   for j, v in enumerate(term.factors) if j != index))
            responses[(target.gear, factors)] += gear_map[target.gear].sign * term.coefficient
            occurrence_count += 1
    if add_inertial:
        for name in shell.names:
            responses[(name, ((name, ZERO, "b"),))] += 6
    terms = []
    for (target, factors), coefficient in sorted(responses.items()):
        if not coefficient:
            continue
        if coefficient.denominator != 1:
            raise ValueError(f"noninteger response coefficient for {target}: {coefficient}")
        terms.append((target, coefficient.numerator, factors))
    tensor = Tensor(shell.gears, terms, strict_support=True)
    reciprocal = check_reciprocity(tensor)
    reciprocal.raise_if_failed()
    if reciprocal.designated or reciprocal.skipped_two_time:
        raise AssertionError("compiled force has an exempted or old-a term")
    used = {v.gear for term in canonical for v in term.factors}
    certificate = {
        "schema": "universe24/generic-structure/interaction-compiler/1",
        "input_meaning": "Phi=sum_over_periodic_nodes(unit_cell_polynomial)",
        "response": "u_i=6*b_i+sign_i*dPhi/db_i" if add_inertial else "u_i=sign_i*dPhi/db_i",
        "potential": [_term_record(t) for t in canonical],
        "max_potential_degree": max((len(t.factors) for t in canonical), default=0),
        "differentiated_occurrences": occurrence_count,
        "tensor_fingerprint": tensor.fingerprint,
        "tensor": tensor.to_dict(),
        "response_monomials": len(tensor.monomials),
        "max_response_degree": tensor.rank - 1,
        "integer_response_coefficients": True,
        "strict_physical_single_face_support": not tensor.support_violations(),
        "reciprocity": {"status": "passed", "checked": reciprocal.checked,
                        "linear_potential_constant_responses": reciprocal.skipped_constants,
                        "exemptions": 0, "old_a_terms": 0},
        "retained_channels_per_node": tensor.G,
        "retained_integer_entries_per_node": 3 * tensor.G,
        "added_workspace_channels": 0,
        "added_clock_channels": 0,
        "channel_ledger": [{"index": i, "name": g.name, "owner": owners[g.name],
                            "retained": ["a", "b", "r"], "link_axis": g.link,
                            "field_sign": g.sign, "in_potential": g.name in used}
                           for i, g in enumerate(tensor.gears)],
        "energy_conservation": "not_implied",
        "einstein_and_shared_metric_physics": "not_established",
    }
    return CompiledInteraction(tensor, canonical, certificate)


def _node(L, xyz):
    x, y, z = (v % L for v in xyz)
    return (x * L + y) * L + z


def potential_value(compiled, field, L):
    """Independent scalar global potential; no compiled derivative is read."""
    names = {name: i for i, name in enumerate(compiled.tensor.names)}
    total = Fraction(0)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for term in compiled.potential:
                    value = Fraction(term.coefficient)
                    for variable in term.factors:
                        j = _node(L, _add((x, y, z), variable.offset))
                        value *= int(field[names[variable.gear], j])
                    total += value
    return total


def independent_gradient(compiled, field, L):
    """Exact 4-point derivative of a degree<=4 polynomial in each coordinate.

    [f(-2)-8f(-1)+8f(1)-f(2)]/12 equals f'(0) exactly for degree<=4.
    This uses only evaluations of the global scalar potential, not symbolic
    occurrence differentiation, the compiled tensor or Engine input routines.
    """
    out = np.empty_like(field, dtype=object)
    varied = field.astype(object).copy()
    for gear in range(field.shape[0]):
        for node in range(field.shape[1]):
            original = int(varied[gear, node])
            numerator = Fraction(0)
            for delta, weight in ((-2, 1), (-1, -8), (1, 8), (2, -1)):
                varied[gear, node] = original + delta
                numerator += weight * potential_value(compiled, varied, L)
            varied[gear, node] = original
            derivative = numerator / 12
            if derivative.denominator != 1:
                raise AssertionError("independent oracle found a fractional derivative")
            out[gear, node] = derivative.numerator
    return out


def example():
    gears = [GearType("phi"), GearType("chi")]
    gears += [GearType("link_" + str(i), link=i) for i in range(3)]
    p, q = Variable("phi"), Variable("chi")
    potential = [PotentialTerm(Fraction(-1, 2), (p, p)),
                 PotentialTerm(Fraction(-1, 2), (q, q)),
                 PotentialTerm(Fraction(1, 4), (p,) * 4),
                 PotentialTerm(Fraction(1, 2), (p, p, q, q)),
                 PotentialTerm(2, (q,)), PotentialTerm(Fraction(7, 3))]
    for axis, offset in enumerate(AXES):
        neighbor = Variable("phi", offset)
        # -(phi_neighbor-phi)^2/2.
        potential += [PotentialTerm(Fraction(-1, 2), (neighbor, neighbor)),
                      PotentialTerm(1, (p, neighbor)),
                      PotentialTerm(Fraction(-1, 2), (p, p))]
        link, neighbor = Variable("link_" + str(axis)), Variable("chi", offset)
        # link^2*(chi_neighbor-chi)^2/2: the link and endpoint fields
        # all receive reciprocal responses from the same quartic interaction.
        potential += [PotentialTerm(Fraction(1, 2), (link, link, neighbor, neighbor)),
                      PotentialTerm(-1, (link, link, q, neighbor)),
                      PotentialTerm(Fraction(1, 2), (link, link, q, q))]
    owners = {g.name: "shared_interaction" for g in gears}
    return compile_potential(gears, potential, owners=owners)


def engine_audit(compiled):
    tensor, L = compiled.tensor, 3
    engine = Engine(tensor)
    rng = random.Random(202611120101)
    a = np.array([[rng.randrange(-1, 2) for _ in range(L ** 3)] for _ in range(tensor.G)], dtype=object)
    b = np.array([[rng.randrange(-1, 2) for _ in range(L ** 3)] for _ in range(tensor.G)], dtype=object)
    r = np.array([[(g + node) % 6 for node in range(L ** 3)] for g in range(tensor.G)], dtype=object)
    seed = State(L, a, b, r)
    state, rows, complete_triples = seed, [], 0
    for tick in range(1, 4):
        gradient = independent_gradient(compiled, state.b, L)
        scalar_a, scalar_b, scalar_r = (np.empty_like(a, dtype=object) for _ in range(3))
        input_values = np.empty_like(a, dtype=object)
        for g, gear in enumerate(tensor.gears):
            for node in range(L ** 3):
                aa, bb, rr = state.gear(g, node)
                u = 6 * bb + gear.sign * int(gradient[g, node])
                input_values[g, node] = u
                quotient, rn = divmod(2 * u + rr, 6)
                scalar_a[g, node], scalar_b[g, node], scalar_r[g, node] = bb, quotient - aa, rn
                complete_triples += 1
        assert np.array_equal(engine.inputs(state), input_values)
        before = state
        state = engine.step(before)
        assert state.same_as(State(L, scalar_a, scalar_b, scalar_r))
        assert engine.inverse_step(state).same_as(before)
        rows.append({"step": tick, "potential": str(potential_value(compiled, state.b, L)),
                     "max_retained_bits": max(abs(int(v)).bit_length() for array in (state.a, state.b, state.r) for v in array.flat),
                     "official_clicks": len(engine.clicks(before, state, tick))})
    assert engine.rewind(state, 3).same_as(seed)
    return {"status": "passed", "nodes": L ** 3, "steps": 3,
            "independent_quartic_derivative_and_complete_triple_checks": complete_triples,
            "complete_seed": seed.to_dict(), "complete_final_state": state.to_dict(),
            "all_six_remainders": True, "complete_rewind": True, "rows": rows}


def rejection_controls():
    p, q = Variable("p"), Variable("q")
    rows = {}
    def reject(name, operation):
        try:
            operation()
        except (ValueError, TypeError) as error:
            rows[name] = {"status": "rejected", "reason": str(error)}
        else:
            raise AssertionError(f"negative control was accepted: {name}")
    reject("degree_five", lambda: compile_potential(["p"], [PotentialTerm(1, (p,) * 5)]))
    reject("fractional_response", lambda: compile_potential(["p", "q"], [PotentialTerm(Fraction(1, 2), (p, q))]))
    reject("three_storage_nodes", lambda: compile_potential(["p"], [PotentialTerm(1, (p, Variable("p", AXES[0]), Variable("p", (-1, 0, 0))))]))
    reject("non_face_neighbor", lambda: compile_potential(["p"], [PotentialTerm(1, (p, Variable("p", (2, 0, 0))))]))
    reject("crossed_link_endpoints", lambda: compile_potential([GearType("lx", link=0), GearType("ly", link=1)], [PotentialTerm(1, (Variable("lx"), Variable("ly")))]))
    reject("49_retained_channels", lambda: compile_potential([f"q{i}" for i in range(49)], []))
    reject("missing_owner", lambda: compile_potential(["p", "q"], [], owners={"p": "owner"}))
    reject("floating_coefficient", lambda: compile_potential(["p"], [PotentialTerm(0.5, (p, p))]))
    reject("undeclared_variable", lambda: compile_potential(["p"], [PotentialTerm(1, (q,))]))
    compiled = compile_potential(["p", "q"], [PotentialTerm(1, (p, p, q))], add_inertial=False)
    # Deliberately omit q's response. A legal local tensor alone does not
    # guarantee that the other side of the interaction was actually included.
    bad = Tensor(compiled.tensor.gears, [m for m in compiled.tensor.monomials if m.target == 0], strict_support=True)
    report = check_reciprocity(bad)
    assert not report.ok and report.missing_partners
    rows["removed_partner_response"] = {"status": "failed_reciprocity_as_expected",
                                         "missing_partners": len(report.missing_partners)}
    return rows


def representation_controls(compiled):
    translated = [PotentialTerm(term.coefficient,
                               tuple(Variable(v.gear, _add(v.offset, (7, -2, 3))) for v in reversed(term.factors)))
                  for term in reversed(compiled.potential)]
    other = compile_potential(compiled.tensor.gears, translated)
    assert other.tensor.same_dynamics(compiled.tensor)
    p, q = Variable("p"), Variable("q")
    combined = compile_potential(["p", "q"], [PotentialTerm(Fraction(1, 2), (p, q)),
                                               PotentialTerm(Fraction(1, 2), (q, p))], add_inertial=False)
    direct = compile_potential(["p", "q"], [PotentialTerm(1, (p, q))], add_inertial=False)
    assert combined.tensor.same_dynamics(direct.tensor)
    negative = compile_potential([GearType("p", sign=-1, sign_why="formal signed-gradient control, not a physical ghost claim")],
                                 [PotentialTerm(Fraction(1, 4), (p,) * 4)])
    engine = Engine(negative.tensor)
    seed = State(3, [[0] * 27], [[2] * 27], [[i % 6 for i in range(27)]])
    nxt = engine.step(seed)
    assert all(nxt.gear(0, i) == (2, (8 + i % 6) // 6, (8 + i % 6) % 6) for i in range(27))
    assert engine.inverse_step(nxt).same_as(seed)
    big = 2 ** 100 + 17
    large_seed = State(3, [[-big] * 27], [[big] * 27], [[i % 6 for i in range(27)]])
    large_next = engine.step(large_seed)
    for i in range(27):
        quotient, remainder = divmod(2 * (6 * big - big ** 3) + i % 6, 6)
        assert large_next.gear(0, i) == (big, quotient + big, remainder)
    assert engine.inverse_step(large_next).same_as(large_seed)
    return {"translation_factor_order_and_term_order": "passed",
            "rational_terms_combine_to_integer_response": "passed",
            "signed_gradient_actual_engine_checks": 27,
            "signed_100_bit_scalar_oracle_checks": 27,
            "no_real_rotation_assumption": True}


def shift_charge_audit():
    """An exact native charge from a shared shift-invariant edge potential.

    Phi=-1/2 sum_edges (1+eta_x^2+eta_y^2)*(psi_y-psi_x)^2.
    Both material eta and transported psi receive their compiled responses.
    The diagonal psi shift is an exact polynomial identity, not a floating
    rotation or a claim that this charge is physical spatial momentum.
    """
    psi, eta = Variable("psi"), Variable("eta")
    terms = []
    for offset in AXES:
        neighbor, material = Variable("psi", offset), Variable("eta", offset)
        for weight in ((), (eta, eta), (material, material)):
            for coefficient, pair in ((Fraction(-1, 2), (neighbor, neighbor)),
                                      (1, (psi, neighbor)),
                                      (Fraction(-1, 2), (psi, psi))):
                terms.append(PotentialTerm(coefficient, weight + pair))
    compiled = compile_potential(["psi", "eta"], terms)
    tensor, L = compiled.tensor, 3
    engine = Engine(tensor)
    rng = random.Random(202611120102)
    a = np.array([[rng.randrange(-2, 3) for _ in range(27)] for _ in range(2)], dtype=object)
    b = np.array([[rng.randrange(-2, 3) for _ in range(27)] for _ in range(2)], dtype=object)
    r = np.array([[(g * 27 + n) % 6 for n in range(27)] for g in range(2)], dtype=object)
    seed, charges = State(L, a, b, r), []
    def charge(state):
        return sum(6 * (int(state.b[0, i]) - int(state.a[0, i])) + int(state.r[0, i]) for i in range(27))
    state, initial = seed, charge(seed)
    shifts = []
    for shift in (-7, -1, 1, 11):
        shifted = seed.b.astype(object).copy()
        shifted[0] += shift
        assert potential_value(compiled, shifted, L) == potential_value(compiled, seed.b, L)
        shifts.append(shift)
    # Independent four-point scalar derivative confirms the exact sum before
    # the actual Engine run; the proof in the report covers all integer seeds.
    gradient = independent_gradient(compiled, seed.b, L)
    assert sum(int(x) for x in gradient[0]) == 0
    local_balance_checks, regional_fluxes = 0, []
    region = set(range(9))  # x=0 slab; periodic face-boundary accounting.
    for tick in range(1, 5):
        old = state
        state = engine.step(old)
        assert charge(state) == initial
        regional_change, inward_boundary_flux = 0, 0
        for node in range(27):
            x, yz = divmod(node, 9)
            y, z = divmod(yz, 3)
            psi_x, eta_x = int(old.b[0, node]), int(old.b[1, node])
            local_flux = 0
            for axis in AXES:
                for direction in (-1, 1):
                    neighbor = _node(L, _add((x, y, z), tuple(direction * v for v in axis)))
                    psi_y, eta_y = int(old.b[0, neighbor]), int(old.b[1, neighbor])
                    incoming = 2 * (1 + eta_x ** 2 + eta_y ** 2) * (psi_y - psi_x)
                    local_flux += incoming
                    if node in region and neighbor not in region:
                        inward_boundary_flux += incoming
            before_p = 6 * (psi_x - int(old.a[0, node])) + int(old.r[0, node])
            after_p = 6 * (int(state.b[0, node]) - int(state.a[0, node])) + int(state.r[0, node])
            assert after_p - before_p == local_flux
            local_balance_checks += 1
            if node in region:
                regional_change += after_p - before_p
        assert regional_change == inward_boundary_flux
        regional_fluxes.append({"step": tick, "regional_charge_change": regional_change,
                                "incoming_boundary_flux": inward_boundary_flux})
        assert engine.inverse_step(state).same_as(old)
        charges.append(charge(state))
    assert engine.rewind(state, 4).same_as(seed)

    # A nonuniform material and perfectly uniform psi should produce no psi
    # force. Remove exactly one of the compiled endpoint-response monomials.
    wanted = sorted((("eta", ZERO), ("eta", ZERO), ("psi", AXES[0])))
    omitted = [m for m in tensor.monomials if m.target == 0 and
               sorted((tensor.names[f.gear], f.offset) for f in m.factors) == wanted]
    assert len(omitted) == 1 and omitted[0].coeff == 1
    bad_tensor = Tensor(tensor.gears, [m for m in tensor.monomials if m is not omitted[0]], strict_support=True)
    bad_reciprocity = check_reciprocity(bad_tensor)
    assert not bad_reciprocity.ok
    positive_material = np.array([[1] * 27, [1 + i % 5 for i in range(27)]], dtype=object)
    uniform_seed = State(L, positive_material.copy(), positive_material.copy(), r)
    good_next = engine.step(uniform_seed)
    bad_engine = Engine(bad_tensor)
    bad_next = bad_engine.step(uniform_seed)
    assert charge(good_next) == charge(uniform_seed)
    expected_defect = -2 * sum(int(x) ** 2 for x in positive_material[1])
    assert charge(bad_next) - charge(uniform_seed) == expected_defect != 0
    assert bad_engine.inverse_step(bad_next).same_as(uniform_seed)
    return {"status": "passed", "tensor_fingerprint": tensor.fingerprint,
            "channels": tensor.G, "retained_integers_per_node": 3 * tensor.G,
            "response_monomials": len(tensor.monomials),
            "source_potential": "-1/2 sum_edges (1+eta_x^2+eta_y^2)*(psi_y-psi_x)^2",
            "invariant": "sum_nodes [6*(b_psi-a_psi)+r_psi]",
            "scope": "all valid integer seeds; periodic graph; exact diagonal psi-shift symmetry",
            "independent_shift_evaluations": shifts,
            "independent_gradient_sum": 0,
            "initial_charge": initial, "charges_after_each_step": charges,
            "independent_local_flux_balance_checks": local_balance_checks,
            "regional_flux_balances": regional_fluxes,
            "all_six_remainders": True, "complete_rewind": True,
            "complete_seed": seed.to_dict(),
            "negative_control": {"removed_monomial": {"target": "psi", "coefficient": omitted[0].coeff,
                                                        "factors": [[tensor.names[f.gear], list(f.offset)] for f in omitted[0].factors]},
                                 "charge_defect": expected_defect,
                                 "reciprocity": "failed_as_expected", "complete_rewind": True},
            "physical_energy_momentum_or_einstein_constraint": "not_identified"}


def run():
    compiled = example()
    output = {
        "schema": "universe24/generic-structure/interactions-audit/1",
        "baseline_commit": "8c53e69f4b466dcbd2da7dab7e3c365bd9731766",
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in (Path(__file__), ROOT / "universe24/core/tensor.py",
                                       ROOT / "universe24/core/engine.py", ROOT / "universe24/core/reciprocity.py")},
        "compiler_certificate": compiled.certificate,
        "actual_engine": engine_audit(compiled),
        "negative_controls": rejection_controls(),
        "representation_controls": representation_controls(compiled),
        "exact_native_shift_charge": shift_charge_audit(),
        "production_changes": False,
        "einstein_acceptance": "not_established",
    }
    path = ROOT / "runs/generic-structure/interactions.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    return output


if __name__ == "__main__":
    evidence = run()
    print(json.dumps({"status": "passed_with_preserved_negative_controls",
                      "channels": evidence["compiler_certificate"]["retained_channels_per_node"],
                      "response_monomials": evidence["compiler_certificate"]["response_monomials"],
                      "actual_engine": {k: v for k, v in evidence["actual_engine"].items()
                                        if k not in ("complete_seed", "complete_final_state")},
                      "negative_controls": evidence["negative_controls"]}, indent=2))
