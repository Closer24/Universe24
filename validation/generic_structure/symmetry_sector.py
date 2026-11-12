"""Extract an exact homogeneous channel-identification sector from a tensor.

This source-only lab proves full-state conjugacy on an explicitly restricted
image. It does not compress arbitrary 45-channel data or repair its physics.
Run: python -m validation.generic_structure.symmetry_sector
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO
from validation.completion import common45, formulation

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PIN = "8c53e69f4b466dcbd2da7dab7e3c365bd9731766"


@dataclass(frozen=True)
class HomogeneousSector:
    full: Tensor
    reduced: Tensor
    mapping: tuple[int | None, ...]
    representatives: tuple[int, ...]
    omitted_carries: tuple[int, ...]
    certificate: dict

    def _check_reduced(self, state):
        if state.G != self.reduced.G:
            raise ValueError("Wrong reduced allocation")
        if any(isinstance(value, (bool, np.bool_))
               or not isinstance(value, (int, np.integer))
               or not 0 <= value < 6 for value in state.r.flat):
            raise ValueError("Every reduced carry must be an exact integer in 0..5")
        for field in ("a", "b"):
            array = getattr(state, field)
            if not np.all(array == array[:, :1]):
                raise ValueError("Both reduced histories must be spatially homogeneous")

    def embed(self, state):
        """Copy mapped triples; omitted a,b are zero and their r is fixed."""
        self._check_reduced(state)
        arrays = [np.zeros((self.full.G, state.N), dtype=object) for _ in range(3)]
        for target, source in enumerate(self.mapping):
            if source is None:
                arrays[2][target] = self.omitted_carries[target]
            else:
                for array, values in zip(arrays, (state.a, state.b, state.r)):
                    array[target] = values[source]
        return State(state.L, *arrays)

    def project(self, state):
        """Inverse on the certified image; reject any unrepresented history."""
        if state.G != self.full.G:
            raise ValueError("Wrong full allocation")
        reduced = State(state.L, *(getattr(state, field)[list(self.representatives)].copy()
                                   for field in ("a", "b", "r")))
        self._check_reduced(reduced)
        if not self.embed(reduced).same_as(state):
            raise ValueError("Full state is outside the declared a,b,r embedding image")
        return reduced


def extract_homogeneous_sector(full: Tensor, reduced_names, mapping, *, omitted_carries=None):
    """Certify arbitrary channel identifications/zeros in a homogeneous sector.

    Scope: b-only tensors with u-coefficients divisible by three. Exact sparse
    substitution proves equality of identified target polynomials and zero
    input on omitted targets. Carries are then frozen, including nonzero ones.
    The restrictions make both forward and inverse closure transparent.
    """
    names, mapping = tuple(reduced_names), tuple(mapping)
    if not names or len(set(names)) != len(names) or len(mapping) != full.G:
        raise ValueError("Supply unique names and one mapping entry per source channel")
    if any(i is not None and (type(i) is not int or not 0 <= i < len(names)) for i in mapping):
        raise ValueError("Mapping entries must be valid reduced indices or None")
    if set(i for i in mapping if i is not None) != set(range(len(names))):
        raise ValueError("Every retained reduced channel needs a source representative")
    if any(f.field != "b" for term in full.monomials for f in term.factors):
        raise ValueError("This certificate supports b-only tensors")
    if any(term.coeff % 3 for term in full.monomials):
        raise ValueError("This carry-transparent certificate requires every u coefficient divisible by 3")
    carries = tuple(0 for _ in mapping) if omitted_carries is None else tuple(omitted_carries)
    if len(carries) != full.G or any(type(r) is not int or not 0 <= r < 6 for r in carries):
        raise ValueError("Specify a legal fixed carry for every omitted channel")

    rows = [dict() for _ in mapping]
    for term in full.monomials:
        factors = [mapping[f.gear] for f in term.factors]
        if any(i is None for i in factors):
            continue
        key = tuple(sorted(factors))
        rows[term.target][key] = rows[term.target].get(key, 0) + term.coeff
    rows = [{key: value for key, value in row.items() if value} for row in rows]
    representatives = tuple(mapping.index(i) for i in range(len(names)))
    for channel, reduced in enumerate(mapping):
        expected = {} if reduced is None else rows[representatives[reduced]]
        if rows[channel] != expected:
            raise ValueError(f"Polynomial closure fails at {full.names[channel]}")
    terms = [(names[target], coefficient, tuple((names[f], ZERO, "b") for f in factors))
             for target, representative in enumerate(representatives)
             for factors, coefficient in rows[representative].items()]
    reduced = Tensor([GearType(name, label="audit") for name in names], terms, strict_support=True)
    embedding = [{"full_index": i, "full_name": name,
                  "reduced_index": mapping[i],
                  "reduced_name": None if mapping[i] is None else names[mapping[i]],
                  "a_b": "fixed zero" if mapping[i] is None else "copy reduced histories",
                  "r": carries[i] if mapping[i] is None else "copy reduced carry at the same node"}
                 for i, name in enumerate(full.names)]
    certificate = {
        "source_tensor_sha256": full.fingerprint,
        "reduced_tensor_sha256": reduced.fingerprint,
        "full_channels": full.G, "reduced_channels": reduced.G,
        "embedding": embedding,
        "symbolic_checks": {"all_target_polynomials_match": True,
                            "omitted_target_polynomials_zero": True,
                            "b_only": True, "all_u_coefficients_divisible_by_three": True},
        "domain": "Both a,b histories spatially homogeneous; identified channels equal in a,b,r; omitted a,b zero and r fixed as declared. Reduced carries may vary by node.",
        "theorem": "E is injective, P E=identity, F_full E=E F_reduced and F_full^(-1) E=E F_reduced^(-1) on the declared image.",
        "scope": "Exact reduced symmetry sector, not compression of arbitrary full states.",
    }
    return HomogeneousSector(full, reduced, mapping, representatives, carries, certificate)


def common45_sector(program=None):
    program = common45.build45() if program is None else program
    names = ("D", "B", "K", "phi", "Pi", "dust")
    mapping = []
    for name in program.tensor.names:
        field = name.removeprefix("projective.")
        if field == "denominator":
            mapped = 0
        elif field in ("B00", "B11", "B22"):
            mapped = 1
        elif field in ("K00", "K11", "K22"):
            mapped = 2
        else:
            mapped = {"phi": 3, "Pi_phi": 4, "dust_amplitude": 5}.get(field)
        mapping.append(mapped)
    return extract_homogeneous_sector(program.tensor, names, mapping,
        omitted_carries=tuple(i % 6 for i in range(program.tensor.G)))


def seed_from_rows(sector, old, current, *, L=3, shift=0):
    a = np.array([[int(value)]*(L**3) for value in old], dtype=object)
    b = np.array([[int(value)]*(L**3) for value in current], dtype=object)
    r = np.array([[(g+node+shift) % 6 for node in range(L**3)]
                  for g in range(sector.reduced.G)], dtype=object)
    return State(L, a, b, r)


def peak_bits(state):
    return max(abs(int(v)).bit_length() for array in (state.a, state.b, state.r) for v in array.flat)


def physical_constraint(state):
    D, _, K, phi, pi, dust = map(int, state.b[:, 0])
    if not D:
        raise ValueError("Zero projective denominator has no physical readout")
    return F(6*K*K-pi*pi-phi*phi-2*dust*dust, D*D)


def rejected(callback):
    try:
        callback()
    except ValueError as error:
        return str(error)
    raise AssertionError("Malformed sector/state unexpectedly accepted")


def audit():
    program = common45.build45()
    sector = common45_sector(program)
    assert sector.reduced.G == 6 and len(sector.reduced) == 14
    full_engine, small_engine = Engine(sector.full), Engine(sector.reduced)
    rng = random.Random(121120265)
    comparisons, maxbits = 0, 0
    for trial in range(12):
        old = [rng.randint(-4, 4) for _ in range(6)]
        current = [rng.randint(-4, 4) for _ in range(6)]
        small = initial = seed_from_rows(sector, old, current, shift=trial)
        full = initial_full = sector.embed(small)
        assert sector.project(full).same_as(small)
        # Backwards closure is tested before following any forward trajectory,
        # so it is not only an undo check on already-generated successors.
        assert full_engine.inverse_step(full).same_as(sector.embed(small_engine.inverse_step(small)))
        for _ in range(3):
            oldsmall, oldfull = small, full
            small = small_engine.step(small)
            full = full_engine.step(full)
            assert full.same_as(sector.embed(small))
            assert sector.project(full).same_as(small)
            assert full.same_as(formulation.previous.scalar_oracle(sector.full, oldfull))
            assert small.same_as(formulation.previous.scalar_oracle(sector.reduced, oldsmall))
            assert full_engine.inverse_step(full).same_as(oldfull)
            assert small_engine.inverse_step(small).same_as(oldsmall)
            assert np.array_equal(full.r, initial_full.r) and np.array_equal(small.r, initial.r)
            comparisons += 3*full.G*full.N
            maxbits = max(maxbits, peak_bits(full))
        assert full_engine.rewind(full, 3).same_as(initial_full)
        assert small_engine.rewind(small, 3).same_as(initial)

    initial = seed_from_rows(sector, [3, -2, 4, -1, 5, -3], [4, 2, -1, 3, 1, 2])
    full = sector.embed(initial)
    malformed = {}
    for field, name, node in (("a", "projective.B11", 0),
                              ("b", "projective.K22", 0),
                              ("r", "projective.B22", 0),
                              ("a", "projective.chi", 0),
                              ("r", "projective.chi", 0)):
        bad = full.copy()
        arr = getattr(bad, field)
        idx = sector.full.gear_index(name)
        arr[idx, node] = (int(arr[idx, node])+1) % 6 if field == "r" else int(arr[idx, node])+1
        malformed[f"changed_{field}_{name}"] = rejected(lambda: sector.project(bad))
    nonuniform = initial.copy()
    nonuniform.b[3, 1] += 1
    malformed["nonuniform_reduced_history"] = rejected(lambda: sector.embed(nonuniform))
    for invalid in (-1, 6):
        bad_carry = initial.copy()
        bad_carry.r[0, 0] = invalid
        malformed[f"illegal_reduced_carry_{invalid}"] = rejected(lambda: sector.embed(bad_carry))
    broken_map = list(sector.mapping)
    broken_map[sector.full.gear_index("projective.B11")] = 2
    malformed["wrong_channel_identification"] = rejected(lambda: extract_homogeneous_sector(
        sector.full, sector.reduced.names, broken_map))
    changed = Tensor(sector.full.gears, [*sector.full.monomials, ("projective.chi", 3, ())], strict_support=True)
    malformed["forcing_omitted_channel"] = rejected(lambda: extract_homogeneous_sector(
        changed, sector.reduced.names, sector.mapping))
    changed = Tensor(sector.full.gears, [*sector.full.monomials, ("projective.chi", 1, ())], strict_support=True)
    malformed["carry_transparency_removed"] = rejected(lambda: extract_homogeneous_sector(
        changed, sector.reduced.names, sector.mapping))

    # Same physical strong initial data as the published C_after=-7 h^2
    # obstruction. Its carry choice is this lab's declared embedding image;
    # all carries are frozen and cannot change the physical counterexample.
    physical = seed_from_rows(sector, [0]*6, [4, 4, -4, 8, 0, 4])
    assert physical_constraint(physical) == 0
    next_small = small_engine.step(physical)
    next_full = full_engine.step(sector.embed(physical))
    assert next_full.same_as(sector.embed(next_small))
    defect = physical_constraint(next_small)
    assert defect == -7*program.dt**2
    decoded = common45.decode_fields(program, next_full)
    _, constraints, _ = formulation.equations(decoded, lambda *_: F(0))
    assert constraints["H"] == defect
    state, bit_history = physical, []
    for tick in range(6):
        state = small_engine.step(state)
        bit_history.append({"tick": tick+1, "denominator_bits": abs(int(state.b[0, 0])).bit_length(),
                            "max_retained_bits": peak_bits(state)})
    assert small_engine.rewind(state, 6).same_as(physical)
    paths = (Path(__file__), ROOT/"validation/completion/common45.py",
             ROOT/"validation/completion/formulation.py",
             ROOT/"validation/geometry/team48/refinement_integer_projective.py",
             ROOT/"universe24/core/engine.py", ROOT/"universe24/core/tensor.py")
    return {"schema": "universe24/generic-structure/symmetry-sector/1",
            "published_source_pin": SOURCE_PIN, "source_pr": "https://github.com/Closer24/Universe24/pull/52",
            "certificate": sector.certificate, "reduced_tensor": sector.reduced.to_dict(),
            "source_parameters": {"dt": str(program.dt), "dx": str(program.dx),
                                  "mass_squared": 1, "static_multiplier": program.multiplier},
            "mechanical": {"status": "passed", "random_trials": 12, "steps_per_trial": 3,
                           "nodes": 27, "integer_entry_comparisons": comparisons,
                           "independent_scalar_oracles": True, "forward_and_inverse_commutation": True,
                           "all_six_carries": True, "mixed_nonzero_signed_histories": True,
                           "random_trial_peak_bits": maxbits},
            "malformed_controls": malformed,
            "retained_physical_failure": {"initial_H": "0", "first_step_H": str(defect),
                                          "identity": "H_after=-7 h^2", "status": "failed",
                                          "full45_reconstruction_matches": True},
            "bit_cost": {"rows": bit_history, "recurrence": "D_next=C D^2-D_old",
                         "lower_bound": "For D_old=0,D0>=2,C>=2: D_n>=D0^(2^n)",
                         "status": "inherited exponential bit growth; not repaired"},
            "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            "limitations": ["Homogeneous isotropic neutral sector only; no spatial gradients, charge, Maxwell or anisotropic modes.",
                            "Exact embedding fixes relationships among every retained a,b,r; arbitrary45 states cannot be projected.",
                            "Reduction preserves the source's constraint failure and projective bit-growth cost.",
                            "Six-channel lab is source-only validation; no new supported physical model or 45-channel compression."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT/"runs/generic-structure/symmetry_sector.json")
    args = parser.parse_args()
    report = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.out), "channels": 6, "monomials": 14,
                      "mechanical": "passed", "source_constraint_gate": "failed"}))


if __name__ == "__main__":
    main()
