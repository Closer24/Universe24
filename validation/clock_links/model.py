"""Four retained phase-relation records attached to a declared carrier bundle.

This source-only proposal constructs data for the existing single runtime. It
does not select a physical model or promote raw carrier phases to proper clocks.
The added apparatus is one-way: the base tensor and all its states are unchanged.
"""
from __future__ import annotations

import numpy as np

from universe24.core.engine import State
from universe24.core.lattice import ZERO, link_direction
from universe24.core.tensor import Factor, GearType, Monomial, Tensor
from universe24.system.bundle import SystemBundle, create_bundle, validate_bundle

VERSION = "clock-links-four-records/1"
CARRIER_NAMES = ("field.phi", "field.chi")
OBSERVER_NAMES = ("observer.local_intensity", "observer.link_x", "observer.link_y", "observer.link_z")


def _record_seed(value, nodes, name):
    if value is None:
        return np.zeros((4, nodes), dtype=object)
    # Use State's exact conversion rather than accepting floats by coercion.
    from universe24.core.engine import exact_array
    return exact_array(value, (4, nodes))


def append_phase_observers(base: SystemBundle, *, apparatus_a=None,
                           apparatus_b=None, apparatus_r=None) -> SystemBundle:
    """Append I0 and |z_x+z_(x+e_k)|² records with complete declared state.

    Input must expose two node carrier channels named field.phi and field.chi.
    At most 44 channels may already be retained. Each appended recurrence has
    u=3I, so ell=I and r'=r for every legal carry; a'=b and b'=I-a preserve
    apparatus history. This says nothing about binary click probabilities.
    """
    base = validate_bundle(base)
    if base.tensor.G > 44:
        raise ValueError("four apparatus channels must fit within 48 total")
    carrier = tuple(base.tensor.gear_index(name) for name in CARRIER_NAMES)
    if any(base.tensor.gears[index].link is not None for index in carrier):
        raise ValueError("carrier ports must be node fields")
    if any(name in base.tensor.names for name in OBSERVER_NAMES):
        raise ValueError("apparatus channels already exist")
    gears = list(base.tensor.gears) + [GearType(name, label="audit") for name in OBSERVER_NAMES]
    terms = list(base.tensor.monomials)
    start = base.tensor.G
    for component in carrier:
        here = Factor(component, ZERO, "b")
        terms.append(Monomial(start, 3, (here, here)))
        for axis in range(3):
            there = Factor(component, link_direction(axis), "b")
            target = start + 1 + axis
            terms.extend((Monomial(target, 3, (here, here)),
                          Monomial(target, 6, (here, there)),
                          Monomial(target, 3, (there, there))))
    # Retain all declared one-way designations on the existing law.
    designations = [(target, factors, why)
                    for (target, factors), why in base.tensor.designations.items()]
    tensor = Tensor(gears, terms, designated_one_way=designations, strict_support=True)
    original = base.seed
    arrays = []
    for field, prepared in (("a", apparatus_a), ("b", apparatus_b), ("r", apparatus_r)):
        extra = _record_seed(prepared, original.N, field)
        arrays.append(np.concatenate((getattr(original, field).astype(object), extra), axis=0))
    seed = State(original.L, *arrays)
    channels = list(base.channels)
    for index, name in enumerate(OBSERVER_NAMES, start):
        channels.append({"index": index, "name": name, "label": "audit",
                         "owner": "phase_relation_test_apparatus",
                         "purpose": "Reversible fixed-gauge carrier intensity record; no physical detector promotion",
                         "readout_dependencies": [name, *CARRIER_NAMES],
                         "coupling": "one-way test apparatus; source/backreaction not supplied"})
    return create_bundle(tensor, seed, channels=channels, protocol=base.protocol,
                         model={"id": "proposal-clock-link-records", "version": VERSION,
                                "domain": "Finite integer one-way phase relation apparatus on a declared base bundle; no operational clock/Born/Einstein acceptance",
                                "base_model": base.model, "base_bundle_id": base.bundle_id,
                                "base_tensor_hash": base.tensor.fingerprint,
                                "base_channels": base.tensor.G,
                                "phase_convention": "raw integer carrier, fixed gauge; a shared quarter turn preserves all records",
                                "apparatus_backreaction": "not supplied"})


def relation_values(state: State, tensor: Tensor) -> np.ndarray:
    """Independent passive formula for the four driving intensities at all nodes.

    This reads complete state and is a diagnostic, never a click-only decoder.
    It is not used by evolution or to generate its expected complete state.
    """
    real, imag = (state.b[tensor.gear_index(name)].astype(object) for name in CARRIER_NAMES)
    values = [real*real + imag*imag]
    for axis in range(3):
        neighbour = state.lattice.shift_index(link_direction(axis))
        re, im = real + real[neighbour], imag + imag[neighbour]
        values.append(re*re + im*im)
    return np.asarray(values, dtype=object)


def base_projection(state: State, base_channels: int) -> State:
    """Retain every original component when comparing the unmodified base law."""
    return State(state.L, *(getattr(state, field)[:base_channels].copy() for field in ("a", "b", "r")))
