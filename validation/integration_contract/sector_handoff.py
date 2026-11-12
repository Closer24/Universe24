"""Compare two independently delivered six-channel symmetry-sector contracts.

Equal evolution polynomials do not imply identical metadata or complete seed
domains. This check keeps the two default carry conventions distinct and only
aligns them by explicit preparation of a new embedding certificate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine, State
from universe24.system.bundle import canonical_bytes
from validation.generic_couplings import sector as specific
from validation.generic_structure import symmetry_sector as generic

ROOT = Path(__file__).resolve().parents[2]


def evolution_signature(tensor):
    """Index-based polynomial identity; names/readout labels remain separate."""
    return tuple((term.target, term.coeff,
                  tuple((factor.gear, factor.offset, factor.field)
                        for factor in term.factors)) for term in tensor.monomials)


def require_rejection(callback):
    try:
        callback()
    except ValueError:
        return
    raise AssertionError('A different complete-state embedding was silently accepted')


def audit():
    left = specific.build_reduction()
    right = generic.common45_sector()
    assert left.full_tensor.fingerprint == right.full.fingerprint
    assert left.aliases == right.mapping
    assert left.representatives == right.representatives
    assert left.tensor.names == ('D', 'B', 'K', 'phi', 'Pi', 'd')
    assert right.reduced.names == ('D', 'B', 'K', 'phi', 'Pi', 'dust')
    assert evolution_signature(left.tensor) == evolution_signature(right.reduced)
    assert left.tensor.fingerprint != right.reduced.fingerprint
    # The metadata mismatch is retained; it affects passive readout authority.
    assert left.tensor.labels == ('official',)*6
    assert right.reduced.labels == ('audit',)*6

    old, current = (3, -2, 4, -1, 5, -3), (4, 2, -1, 3, 1, 2)
    seed = State(3,
        np.array([[value]*27 for value in old], dtype=object),
        np.array([[value]*27 for value in current], dtype=object),
        np.array([[(channel+node) % 6 for node in range(27)]
                  for channel in range(6)], dtype=object))
    left_full, right_full = specific.embed_state(left, seed), right.embed(seed)
    assert np.array_equal(left_full.a, right_full.a)
    assert np.array_equal(left_full.b, right_full.b)
    assert not np.array_equal(left_full.r, right_full.r)
    require_rejection(lambda: specific.project_state(left, right_full))
    require_rejection(lambda: right.project(left_full))

    # This is preparation of a distinct certified domain, never a mutation of
    # either existing full state or a loss of the default domain's frozen r.
    aligned = generic.extract_homogeneous_sector(
        right.full, right.reduced.names, right.mapping,
        omitted_carries=(0,)*right.full.G)
    assert aligned.embed(seed).same_as(left_full)
    bad = left_full.copy()
    omitted = next(index for index, mapped in enumerate(left.aliases) if mapped is None)
    bad.a[omitted, 0] = 1
    require_rejection(lambda: specific.project_state(left, bad))
    require_rejection(lambda: aligned.project(bad))
    bad_history = seed.copy()
    bad_history.a[1, 1] += 1
    require_rejection(lambda: specific.embed_state(left, bad_history))
    require_rejection(lambda: aligned.embed(bad_history))

    engines = [Engine(left.tensor), Engine(right.reduced), Engine(left.full_tensor)]
    small_left, small_right, full_aligned, full_default = seed, seed, left_full, right_full
    maximum_bits = 0
    for _ in range(3):
        previous = (small_left, small_right, full_aligned, full_default)
        small_left = engines[0].step(small_left)
        small_right = engines[1].step(small_right)
        full_aligned = engines[2].step(full_aligned)
        full_default = engines[2].step(full_default)
        assert small_left.same_as(small_right)
        assert full_aligned.same_as(specific.embed_state(left, small_left))
        assert full_aligned.same_as(aligned.embed(small_right))
        assert full_default.same_as(right.embed(small_right))
        assert np.array_equal(full_aligned.a, full_default.a)
        assert np.array_equal(full_aligned.b, full_default.b)
        assert not full_aligned.same_as(full_default)
        maximum_bits = max(maximum_bits, max(abs(int(value)).bit_length()
            for bank in (full_aligned.a, full_aligned.b, full_aligned.r) for value in bank.flat))
        assert specific.project_state(left, full_aligned).same_as(aligned.project(full_aligned))
        for engine, after, before in zip((*engines, engines[2]),
                (small_left, small_right, full_aligned, full_default), previous):
            assert engine.inverse_step(after).same_as(before)
    for engine, after, initial in zip((*engines, engines[2]),
            (small_left, small_right, full_aligned, full_default),
            (seed, seed, left_full, right_full)):
        assert engine.rewind(after, 3).same_as(initial)
    paths = ('validation/generic_couplings/sector.py',
             'validation/generic_structure/symmetry_sector.py',
             'validation/integration_contract/sector_handoff.py')
    return {'schema': 'universe24/sector-handoff/1',
        'full_tensor_sha256': left.full_tensor.fingerprint,
        'reduced_tensor_sha256': {'generic_couplings': left.tensor.fingerprint,
                                  'generic_structure': right.reduced.fingerprint},
        'channel_name_map': dict(zip(left.tensor.names, right.reduced.names)),
        'labels': {'generic_couplings': 'official', 'generic_structure': 'audit'},
        'dynamics_after_explicit_index_mapping': 'equal',
        'default_complete_seed_domains': 'different; cross-projection rejected',
        'omitted_carries': {'generic_couplings': 'zero', 'generic_structure': 'full_index modulo 6'},
        'explicit_zero_carry_domain_alignment': 'passed',
        'arbitrary_old_history_and_three_tick_full_state_comparison': 'passed',
        'inverse_and_complete_rewind': 'passed',
        'off_sector_and_nonhomogeneous_history_rejection': 'passed',
        'nodes': 27, 'steps': 3, 'maximum_retained_integer_bits': maximum_bits,
        'six_channel_retained_integers_per_node': 18,
        'aligned_final_full_state_sha256': hashlib.sha256(canonical_bytes(full_aligned.to_dict())).hexdigest(),
        'source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths},
        'scope': 'Homogeneous isotropic neutral symmetry sector only; no arbitrary45 compression or physical repair.',
        'physical_acceptance': 'not_established'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
