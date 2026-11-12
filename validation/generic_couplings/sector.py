"""Exact homogeneous invariant-sector audit of the current massive45 tensor.

This is source-only research. It supplies neither a new runtime nor a general
six-channel physical model. Embedding/projection are guarded preparation and
validation operations; they never alter an evolving full45 trajectory.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import ZERO, lattice
from validation.geodesic_board.run import build_program
from validation.geometry.team48.matter_dust_square import FIELDS_CHARGED


NAMES = ('D', 'B', 'K', 'phi', 'Pi', 'd')
DT = Fraction(1, 64)
DX = Fraction(1, 4)
FULL_NAMES = ('projective.denominator',) + tuple('projective.' + name for name in FIELDS_CHARGED)
DOMAIN = ('Spatially homogeneous a/b banks; equal diagonal B and K triples; '
          'neutral radial scalar and normal dust; every omitted triple zero. '
          'Reduced carries may vary by site and are copied to equal channels. '
          'No anisotropy, charged phase, Maxwell field or spatial packet.')


class SectorError(ValueError):
    """A tensor or complete retained state fails the declared sector contract."""


@dataclass(frozen=True)
class SectorReduction:
    full_tensor: Tensor
    tensor: Tensor
    aliases: tuple[int | None, ...]
    representatives: tuple[int, ...]


def explicit_tensor() -> Tensor:
    """Independent complete 14-term tensor, fixed h=1/64, C=256, mass²=1.

    Symbols in these polynomials are current b registers, not ratios.
    Default official labels reproduce the original audit fingerprint; labels
    are passive metadata and grant no physical acceptance.
    """
    polynomials = {
        'D': ((768, ('D', 'D')),),
        'B': ((768, ('D', 'B')), (12, ('K', 'B'))),
        'K': ((768, ('D', 'K')), (36, ('K', 'K')),
              (-6, ('phi', 'phi')), (-6, ('d', 'd'))),
        'phi': ((768, ('D', 'phi')), (12, ('D', 'Pi'))),
        'Pi': ((768, ('D', 'Pi')), (36, ('K', 'Pi')), (-12, ('D', 'phi'))),
        'd': ((768, ('D', 'd')), (18, ('K', 'd'))),
    }
    return Tensor(NAMES, [(target, coefficient, tuple((name, ZERO, 'b') for name in factors))
                         for target, terms in polynomials.items()
                         for coefficient, factors in terms], strict_support=True)


def build_reduction(source_tensor: Tensor | None = None) -> SectorReduction:
    """Prove coefficient closure and equality to the independent small law.

    The default source is the existing board's massive45 builder. Supplying a
    tensor enables independent falsification: changed surviving polynomials,
    nonzero omitted updates, or unequal grouped outputs are rejected. Changes
    which vanish identically on this sector may legitimately pass, and the
    caller must retain the reported source fingerprint rather than transfer
    any off-sector claims.
    """
    if source_tensor is None:
        source_tensor = build_program(dt=DT, dx=DX, mass_squared=1).tensor
    if not isinstance(source_tensor, Tensor):
        raise TypeError('A validated Tensor is required')
    if source_tensor.names != FULL_NAMES or source_tensor.G != 45:
        raise SectorError('Expected the current full45 channel order and names')
    if source_tensor.support_violations():
        raise SectorError('The full source must have strict physical face support')
    mapping = {'projective.denominator': 'D', 'projective.phi': 'phi',
               'projective.Pi_phi': 'Pi', 'projective.dust_amplitude': 'd'}
    for axis in range(3):
        mapping[f'projective.B{axis}{axis}'] = 'B'
        mapping[f'projective.K{axis}{axis}'] = 'K'
    aliases = tuple(NAMES.index(mapping[name]) if name in mapping else None
                    for name in source_tensor.names)
    restricted = [defaultdict(int) for _ in source_tensor.names]
    for term in source_tensor.monomials:
        mapped = [aliases[factor.gear] for factor in term.factors]
        if any(index is None for index in mapped):
            continue
        # Homogeneity identifies shifted values in BOTH retained time banks.
        factors = tuple(sorted((NAMES[index], ZERO, factor.field)
                               for index, factor in zip(mapped, term.factors)))
        restricted[term.target][factors] += term.coeff
    restricted = [{factors: value for factors, value in terms.items() if value}
                  for terms in restricted]
    representatives = [None] * len(NAMES)
    for full_index, reduced_index in enumerate(aliases):
        if reduced_index is None:
            if restricted[full_index]:
                raise SectorError(f'Omitted channel has nonzero restricted update: {source_tensor.names[full_index]}')
        elif representatives[reduced_index] is None:
            representatives[reduced_index] = full_index
        elif restricted[full_index] != restricted[representatives[reduced_index]]:
            raise SectorError(f'Grouped channel updates disagree: {source_tensor.names[full_index]}')
    terms = [(NAMES[index], coefficient, factors)
             for index, representative in enumerate(representatives)
             for factors, coefficient in restricted[representative].items()]
    extracted = Tensor(NAMES, terms, strict_support=True)
    expected = explicit_tensor()
    if extracted.to_dict() != expected.to_dict():
        raise SectorError('Restricted source differs from the independent 14-term law')
    return SectorReduction(source_tensor, extracted, aliases, tuple(representatives))


def _checked_state(state: State, channels: int) -> State:
    if not isinstance(state, State):
        raise TypeError('A complete State is required')
    # State arrays are mutable, so recheck exact types and all shapes here.
    checked = State(state.L, state.a, state.b, state.r)
    if checked.G != channels:
        raise SectorError(f'Expected {channels} complete channels')
    if any(not 0 <= int(value) < 6 for value in checked.r.flat):
        raise SectorError('Every retained carry must lie in 0..5')
    return checked


def _checked_reduced(state: State) -> State:
    checked = _checked_state(state, len(NAMES))
    for field in ('a', 'b'):
        bank = getattr(checked, field)
        if not np.all(bank == bank[:, :1]):
            raise SectorError(f'Reduced {field} history must be spatially homogeneous')
    return checked


def embed_state(reduction: SectorReduction, reduced_state: State) -> State:
    """Inject six complete channels into the declared invariant full45 domain."""
    state = _checked_reduced(reduced_state)
    banks = []
    for field in ('a', 'b', 'r'):
        bank = getattr(state, field)
        banks.append(np.array([bank[index].copy() if index is not None else [0] * state.N
                               for index in reduction.aliases], dtype=object))
    return State(state.L, *banks)


def project_state(reduction: SectorReduction, full_state: State) -> State:
    """Invert embedding, rejecting information outside its complete domain.

    No projection onto a nearby admissible state is performed. In particular,
    unequal old histories or frozen carries fail even when current readouts
    agree. General discarded carry patterns would need a separate declared
    reconstruction and are deliberately unsupported here.
    """
    state = _checked_state(full_state, 45)
    for field in ('a', 'b', 'r'):
        bank = getattr(state, field)
        for full_index, reduced_index in enumerate(reduction.aliases):
            if reduced_index is None:
                if np.any(bank[full_index] != 0):
                    raise SectorError(f'Omitted channel {reduction.full_tensor.names[full_index]} has nonzero {field}')
            elif not np.array_equal(bank[full_index], bank[reduction.representatives[reduced_index]]):
                raise SectorError(f'Equal diagonal channels have different {field} histories/carries')
    result = State(state.L, *(getattr(state, field)[list(reduction.representatives)].copy()
                              for field in ('a', 'b', 'r')))
    result = _checked_reduced(result)
    if not embed_state(reduction, result).same_as(state):
        raise SectorError('Complete state is outside the exact embedding image')
    return result


def prepare_seed(L: int = 3, denominator: int = 100) -> State:
    """Declare the original finite audit seed; not generic initial-data solving."""
    if type(denominator) is not int or denominator < 2:
        raise ValueError('An integer denominator >=2 is required')
    nodes = lattice(L).N
    current = (denominator, denominator, -denominator, 2 * denominator, 0, denominator)
    return State(L, np.zeros((6, nodes), dtype=object),
                 np.array([[value] * nodes for value in current], dtype=object),
                 np.array([[index] * nodes for index in range(6)], dtype=object))


def _bits(state: State) -> int:
    return max(abs(int(value)).bit_length()
               for bank in (state.a, state.b, state.r) for value in bank.flat)


def _compare_orbit(reduction: SectorReduction, seed: State, steps: int) -> list[int]:
    small, full = seed, embed_state(reduction, seed)
    original_full = full
    small_engine, full_engine = Engine(reduction.tensor), Engine(reduction.full_tensor)
    bits = []
    for tick in range(steps + 1):
        if not full.same_as(embed_state(reduction, small)) or not project_state(reduction, full).same_as(small):
            raise AssertionError(f'Complete-state sector equivalence failed at update {tick}')
        bits.append(_bits(full))
        if tick == steps:
            break
        next_small, next_full = small_engine.step(small), full_engine.step(full)
        if not small_engine.inverse_step(next_small).same_as(small) or not full_engine.inverse_step(next_full).same_as(full):
            raise AssertionError('A complete inverse failed')
        small, full = next_small, next_full
    if not small_engine.rewind(small, steps).same_as(seed) or not full_engine.rewind(full, steps).same_as(original_full):
        raise AssertionError('A full rewind failed')
    return bits


def audit() -> dict:
    """Return finite source-only evidence suitable for the common audit runner."""
    reduction = build_reduction()
    seed = prepare_seed()
    bits = _compare_orbit(reduction, seed, 8)
    rng = np.random.default_rng(2026111206)
    random_cases = 8
    random_peak = 0
    for _ in range(random_cases):
        old = np.repeat(rng.integers(-4, 5, size=(6, 1)).astype(object), 27, axis=1)
        current = np.repeat(rng.integers(-4, 5, size=(6, 1)).astype(object), 27, axis=1)
        carry = rng.integers(0, 6, size=(6, 27)).astype(object)
        random_peak = max(random_peak, max(_compare_orbit(reduction, State(3, old, current, carry), 3)))
    return {'schema': 'universe24/generic-couplings/sector/1',
            'status': 'passed', 'domain': DOMAIN,
            'full_channels': reduction.full_tensor.G, 'full_terms': len(reduction.full_tensor),
            'full_tensor_sha256': reduction.full_tensor.fingerprint,
            'reduced_channels': reduction.tensor.G, 'reduced_terms': len(reduction.tensor),
            'reduced_tensor_sha256': reduction.tensor.fingerprint,
            'retained_integers_per_node': {'full': 135, 'reduced_sector': 18},
            'parameters': {'dt': str(DT), 'dx': str(DX), 'mass_squared': 1, 'multiplier': 256},
            'coefficient_closure_and_independent_tensor': 'passed',
            'complete_state_equality_and_both_rewinds': 'passed',
            'finite_fixture': {'updates': 8, 'nodes': 27, 'all_six_carries': True,
                               'maximum_integer_bits_by_step': bits},
            'random_history_controls': {'cases': random_cases, 'updates_each': 3,
                                        'spatially_varying_carries': True,
                                        'maximum_integer_bits': random_peak},
            'arbitrary_state_compression': 'not_claimed',
            'physical_acceptance': 'not_established',
            'limitations': ['The invariant sector removes spatial, anisotropic and charged/Maxwell modes.',
                            'The original constraint and time-stability failures are inherited.',
                            'The denominator bit-growth obstruction remains.',
                            'No operational clock, detector or supported runtime model is added.']}
