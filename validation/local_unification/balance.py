"""Exact kinetic ledgers of the SAME conservative carrier--record law.

These are declared lattice-ray energy/momentum units, not a derivation of
Einstein gravity, a universal speed calibration, or a thermodynamic bit cost.
The four rails in each bank are record+, record-, carrier+, carrier-.
Both complete current banks are counted; one bank transports at each native
tick.  Each population transports one lattice cell per TWO native ticks.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
from pathlib import Path

import numpy as np

from validation.padding import sector_state, sector_tensor
from universe24.core import DIRECTIONS, Engine, State, exact_json, lattice


RAILS = ("record_plus", "record_minus", "carrier_plus", "carrier_minus")
COLLISION_TABLE = tuple(
    (0, 1, 1, 0) if bits == (1, 0, 0, 1) else
    (1, 0, 0, 1) if bits == (0, 1, 1, 0) else bits
    for bits in product(range(2), repeat=4)
)


def _direction(direction):
    direction = tuple(direction)
    if direction not in DIRECTIONS:
        raise ValueError("kinetic ledger requires one unit face direction")
    return direction


def _values(values, L):
    values = np.asarray(values, dtype=object)
    if values.shape != (8, L ** 3):
        raise ValueError("the complete current state must contain both four-rail banks")
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer))
           or int(v) not in (0, 1) for v in values.flat):
        raise ValueError("kinetic occupancy is defined only on the Boolean invariant sector")
    return values


def _collision(values, *, coupled=True):
    """Independent literal truth-table oracle; no candidate polynomial calls."""
    if not coupled:
        return values.copy()
    indices = 8 * values[0] + 4 * values[1] + 2 * values[2] + values[3]
    return np.array([COLLISION_TABLE[int(i)] for i in indices], dtype=object).T


def _stream(values, L, direction, *, inverse=False):
    direction = _direction(direction)
    lat = lattice(L)
    out = values.copy()
    for rail in range(4):
        velocity = 1 if rail in (0, 2) else -1
        if inverse:
            velocity *= -1
        # Pull the population from the incoming site.
        incoming = tuple(-velocity * d for d in direction)
        out[rail] = values[rail, lat.shift_index(incoming)]
    return out


def independent_step(values, L, direction=(1, 0, 0), *, inverse=False, coupled=True):
    """Literal G/stream first-order map, independent of the compiled tensor."""
    values = _values(values, L)
    A, B = values[:4], values[4:]
    if inverse:
        return np.concatenate((_stream(B, L, direction, inverse=True),
                               _collision(A, coupled=coupled)))
    return np.concatenate((_collision(B, coupled=coupled),
                           _stream(A, L, direction)))


def kinetic_densities(values, L):
    """Count every current rail in BOTH banks; no independent old-a energy."""
    v = _values(values, L)
    plus = v[0] + v[2] + v[4] + v[6]
    minus = v[1] + v[3] + v[5] + v[7]
    rec_plus, rec_minus = v[0] + v[4], v[1] + v[5]
    car_plus, car_minus = v[2] + v[6], v[3] + v[7]
    return {"plus": plus, "minus": minus,
            "energy": plus + minus, "momentum": plus - minus,
            "record_energy": rec_plus + rec_minus,
            "record_momentum": rec_plus - rec_minus,
            "carrier_energy": car_plus + car_minus,
            "carrier_momentum": car_plus - car_minus}


def kinetic_stress(values, L, direction=(1, 0, 0)):
    """Declared macro-scale T=n+ k+ k+ + n- k- k-, in c=1 units.

    A macro is two Engine ticks.  This symmetric continuum-target readout does
    not replace the exact staggered face flux used by the per-tick ledger.
    """
    direction = _direction(direction)
    density = kinetic_densities(values, L)
    E, p = density["energy"], density["momentum"]
    result = np.zeros((4, 4, L ** 3), dtype=object)
    result[0, 0] = E
    for i in range(3):
        result[0, i + 1] = result[i + 1, 0] = direction[i] * p
        for j in range(3):
            result[i + 1, j + 1] = direction[i] * direction[j] * E
    return result


def _face_fluxes(values, L, direction):
    """Outgoing net face flux at (x,x+d); only old A moves this tick."""
    direction = _direction(direction)
    v = _values(values, L)
    neighbor = lattice(L).shift_index(direction)
    rp, rm, cp, cm = v[:4]
    return {
        "energy": rp + cp - rm[neighbor] - cm[neighbor],
        "momentum": rp + cp + rm[neighbor] + cm[neighbor],
        "record_energy": rp - rm[neighbor],
        "record_momentum": rp + rm[neighbor],
        "carrier_energy": cp - cm[neighbor],
        "carrier_momentum": cp + cm[neighbor],
    }


def collision_exchange(values, L, *, coupled=True):
    """Signed B-bank collision: +1 forward, -1 reverse, zero otherwise."""
    v = _values(values, L)
    before = v[4:]
    after = _collision(before, coupled=coupled)
    return after[2] - before[2]


def transition_ledgers(before, after, direction=(1, 0, 0), *, coupled=True):
    """Verify full law/sector and exact local balances, including record recoil.

    Raises on a different law or an unprepared history, even if its global
    charge totals happen to match.  Returned arrays are passive diagnostics.
    """
    if not isinstance(before, State) or not isinstance(after, State) or before.L != after.L:
        raise ValueError("provide equal-lattice complete State objects")
    L = before.L
    v, w = _values(before.b, L), _values(after.b, L)
    if not np.array_equal(before.a, independent_step(v, L, direction, inverse=True, coupled=coupled)):
        raise ValueError("old history is outside the proved kinetic sector")
    if not np.array_equal(after.a, before.b) or not np.array_equal(after.r, before.r):
        raise ValueError("the complete native history/carry update differs")
    if not np.array_equal(w, independent_step(v, L, direction, coupled=coupled)):
        raise ValueError("transition differs from the selected conservative kinetic law")
    old, new = kinetic_densities(v, L), kinetic_densities(w, L)
    fluxes = _face_fluxes(v, L, direction)
    incoming = lattice(L).shift_index(tuple(-x for x in _direction(direction)))
    delta = collision_exchange(v, L, coupled=coupled)
    sources = {name: np.zeros(L ** 3, dtype=object) for name in fluxes}
    sources["carrier_momentum"] = 2 * delta
    sources["record_momentum"] = -2 * delta
    residuals = {}
    for name, flux in fluxes.items():
        residuals[name] = new[name] - old[name] + flux - flux[incoming] - sources[name]
        if any(int(x) for x in residuals[name]):
            raise AssertionError(f"local {name} balance failed")
    if any(int(e) < abs(int(p)) for e, p in zip(new["energy"], new["momentum"])):
        raise AssertionError("positive kinetic energy bound failed")
    return {"old": old, "new": new, "fluxes": fluxes, "sources": sources,
            "residuals": residuals, "collision_delta": delta}


def source_transition_ledgers(before, after, tensor, direction=(1, 0, 0)):
    """Check the SAME packet law inside the explicit 12-channel source tensor.

    This verifies the retained eight-rail prefix against the literal oracle.
    It deliberately does not assign additive energy to metric/integration
    coordinates or validate the extra four source equations. Those equations
    require the separate geometry proof and its exact full-state source join.
    """
    from universe24.core import Tensor
    from validation.local_unification.native import build_tensor

    tensor = sector_tensor(tensor, 12)
    before, after = sector_state(before, 12), sector_state(after, 12)
    if tensor.G != 12 or before.G != 12 or after.G != 12:
        raise ValueError("the joined source ledger requires exactly12complete channels")
    prefix_terms = []
    for term in tensor.monomials:
        if term.target >= 8:
            continue
        if any(factor.gear >= 8 for factor in term.factors):
            raise ValueError("extra source coordinates cannot alter the declared packet law")
        prefix_terms.append((term.target, term.coeff,
                             [(f.gear, f.offset, f.field) for f in term.factors]))
    prefix = Tensor(list(tensor.gears[:8]), prefix_terms, strict_support=True)
    if prefix.fingerprint != build_tensor(direction).fingerprint:
        raise ValueError("the source tensor's packet prefix differs from the selected law")
    packets = [State(state.L, state.a[:8], state.b[:8], state.r[:8]) for state in (before, after)]
    return transition_ledgers(*packets, direction)


def regional_balance(ledger, mask, L, direction=(1, 0, 0)):
    """Sum the same local ledger over a region; internal faces cancel."""
    mask = np.asarray(mask, dtype=bool)
    if mask.shape != (L ** 3,):
        raise ValueError("region must include one membership value per node")
    neighbor = lattice(L).shift_index(_direction(direction))
    boundary_weight = mask.astype(object) - mask[neighbor].astype(object)
    results = {}
    for name, flux in ledger["fluxes"].items():
        change = sum(int(x) for x in (ledger["new"][name] - ledger["old"][name])[mask])
        outward = sum(int(x) for x in flux * boundary_weight)
        source = sum(int(x) for x in ledger["sources"][name][mask])
        if change + outward - source:
            raise AssertionError(f"regional {name} balance failed")
        results[name] = {"change": change, "outward_flux": outward, "source": source}
    return results


def collision_proof():
    """Exhaust all16 inputs and prove the cubic formula equals the permutation."""
    table_rows = []
    for a, b, c, d in product(range(2), repeat=4):
        delta = a * d * (1 - b - c) - b * c * (1 - a - d)
        result = (a - delta, b + delta, c + delta, d - delta)
        index = 8 * a + 4 * b + 2 * c + d
        assert result == COLLISION_TABLE[index]
        rev = COLLISION_TABLE[8 * result[0] + 4 * result[1] + 2 * result[2] + result[3]]
        assert rev == (a, b, c, d)
        assert a + c == result[0] + result[2]
        assert b + d == result[1] + result[3]
        assert a + b == result[0] + result[1]
        assert c + d == result[2] + result[3]
        assert (result[2] - result[3]) - (c - d) == 2 * delta
        assert (result[0] - result[1]) - (a - b) == -2 * delta
        table_rows.append({"input": [a, b, c, d], "output": list(result), "delta": delta})
    # A positive record carries the compensating recoil; omitting it fails.
    assert sum(COLLISION_TABLE[9]) == 2
    return {"truth_table": table_rows, "involution": True,
            "directional_occupancy_invariants": ["record_plus+carrier_plus", "record_minus+carrier_minus"],
            "species_number_invariants": ["record_plus+record_minus", "carrier_plus+carrier_minus"],
            "carrier_only_momentum_counterexample": {"input": [1, 0, 0, 1], "carrier_delta": 2,
                                                       "record_delta": -2, "total_delta": 0},
            "positive_energy": "E=record_plus+record_minus+carrier_plus+carrier_minus",
            "no_carrier_creation_in_empty_or_double_cases": True}


def audit_source_prefix(*, L=19, steps=6):
    """Run the actual geometry/source construction and check its packet ledger."""
    from validation.local_unification.geometry import prepare_fixture

    tensor, seed, protocol = prepare_fixture(L=L, steps=steps)
    engine, state = Engine(tensor), seed
    rows = []
    for tick in range(1, steps + 1):
        after = engine.step(state)
        ledger = source_transition_ledgers(state, after, tensor, tuple(protocol["direction"]))
        assert engine.inverse_step(after).same_as(state)
        rows.append({"microstep": tick,
                     "energy": sum(int(v) for v in ledger["new"]["energy"]),
                     "momentum": sum(int(v) for v in ledger["new"]["momentum"]),
                     "forward_collisions": sum(int(v) == 1 for v in ledger["collision_delta"]),
                     "reverse_collisions": sum(int(v) == -1 for v in ledger["collision_delta"]),
                     "local_comparisons": 6 * L ** 3})
        state = after
    assert engine.rewind(state, steps).same_as(seed)
    return {"tensor_hash": tensor.fingerprint,
            "complete_seed_sha256": hashlib.sha256(exact_json.dumps(seed.to_dict(), sort_keys=True).encode()).hexdigest(),
            "L": L, "microsteps": steps, "channels": tensor.G,
            "packet_channels": list(range(8)), "geometry_channels": list(range(8, 12)),
            "rows": rows, "full_source_inverse_and_rewind": True,
            "local_packet_balance_comparisons": 6 * steps * L ** 3,
            "physical_chart": protocol["physical_domain"],
            "scope": "same twelve-channel source run; exact whole-board packet ledgers, not a geometry/metric certificate"}


def audit(out=None, *, steps=12):
    from validation.local_unification.native import build_tensor, prepare_state

    report = {"schema": "universe24/local-unification-balance/1", "collision": collision_proof(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "runs": [], "local_balance_comparisons": 0, "regional_balance_comparisons": 0,
              "complete_state_oracle_comparisons": 0, "source_exchanges": 0}
    for L in (3, 5):
        lat = lattice(L)
        for direction in DIRECTIONS:
            tensor = build_tensor(direction=direction)
            rng = np.random.default_rng(9300 + L + DIRECTIONS.index(direction))
            current = rng.integers(0, 2, size=(8, L ** 3)).astype(object)
            carries = np.array([[(g + n) % 6 for n in range(L ** 3)] for g in range(8)], dtype=object)
            seed = prepare_state(current, L, direction=direction, remainders=carries)
            engine, state = Engine(tensor), seed
            initial = kinetic_densities(seed.b, L)
            totals = {name: sum(int(x) for x in initial[name]) for name in ("energy", "momentum", "record_energy", "carrier_energy")}
            masks = [np.array([sum(lat.coords(n)) % 2 == 0 for n in range(lat.N)]),
                     np.array([lat.coords(n)[0] == 0 for n in range(lat.N)]),
                     np.array([n == 0 for n in range(lat.N)])]
            values = [current.copy()]
            for tick in range(1, steps + 1):
                following = engine.step(state)
                ledger = transition_ledgers(state, following, direction)
                assert engine.inverse_step(following).same_as(state)
                for name, total in totals.items():
                    assert sum(int(x) for x in ledger["new"][name]) == total
                for mask in masks:
                    regional_balance(ledger, mask, L, direction)
                report["source_exchanges"] += sum(int(x) != 0 for x in ledger["collision_delta"])
                report["local_balance_comparisons"] += 6 * L ** 3
                report["regional_balance_comparisons"] += 6 * len(masks)
                report["complete_state_oracle_comparisons"] += 24 * L ** 3
                values.append(following.b.copy())
                state = following
            assert engine.rewind(state, steps).same_as(seed)
            # Each staggered population moves one cell per TWO native ticks.
            for i in range(len(values) - 2):
                earlier, later = kinetic_densities(values[i], L), kinetic_densities(values[i + 2], L)
                assert np.array_equal(later["plus"], earlier["plus"][lat.shift_index(tuple(-x for x in direction))])
                assert np.array_equal(later["minus"], earlier["minus"][lat.shift_index(direction)])
            stress = kinetic_stress(state.b, L, direction)
            assert np.array_equal(stress, stress.swapaxes(0, 1))
            assert np.all(-stress[0, 0] + stress[1, 1] + stress[2, 2] + stress[3, 3] == 0)
            report["runs"].append({"L": L, "direction": list(direction), "steps": steps,
                                   "tensor_hash": tensor.fingerprint, "channels": tensor.G,
                                   "totals": totals, "global_invariant_mass_squared": totals["energy"] ** 2 - totals["momentum"] ** 2,
                                   "full_rewind": True, "macro_transport": True,
                                   "maximum_retained_bits": 3})
    report["timing"] = {"native_ticks_per_macro": 2, "cells_per_macro": 1,
                        "each_native_tick_transports": "old A only; old B collides",
                        "clock_claim": "kinematic stage calibration, not a material proper-time clock"}
    report["interpretation"] = {
        "positive_kinetic_stress": "proved in declared unit-energy massless lattice-rail model",
        "collision_total_source": "zero; species momenta exchange equal opposite recoil",
        "stress_profile": "species-blind directional profiles stream freely at macro times",
        "Einstein_equations": "not established by this ledger",
        "Lorentz_invariance": "not established by finite axial velocity set",
        "thermodynamic_entropy": "not inferred from occupancy or record distinguishability",
        "invariant_mass": "global kinematic invariant; not a proof of a localized bound massive body",
    }
    report["joined_source_prefix"] = audit_source_prefix()
    if out is not None:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(exact_json.dumps(report, sort_keys=True) + "\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/balance.json"))
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args(argv)
    result = audit(args.out, steps=args.steps)
    print(exact_json.dumps({key: result[key] for key in ("local_balance_comparisons", "regional_balance_comparisons", "source_exchanges")}))


if __name__ == "__main__":
    main()
