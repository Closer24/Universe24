"""The receive's folder: the Port's angle, the table's triple and the rotation of the Link's pair are Rule3's read acts; the identity at angle zero, the refusals and the declaration, bound to the loop."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.primitives import compose_triples, mirror_triple
from event_universe.features.receive import (
    DECLARATION,
    Link,
    ReceiveStart,
    ReceiveTerm,
    TwistRead,
    apply,
    rotated,
    triple,
)
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
TOWARD = ROOT / "examples" / "events" / "toward_nature"


def test_the_angle_zero_is_the_identity_and_the_composed_triple_is_the_tables():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    term = simulation._receive_term
    table = simulation.twist_table
    assert table is not None
    generator = np.random.default_rng(7)
    for k in (0, 1, -1, 1023, 1024, -1025, 5703478, -5703478):
        found = triple(term, np.array(k), 0)
        composed = compose_triples(table.fine[abs(k) & 1023], table.coarse[abs(k) >> 10])
        assert tuple(int(v) for v in found) == (mirror_triple(composed) if k < 0 else composed)
        re, im = generator.integers(-(1 << 20), 1 << 20, size=(2, 5))
        t_re, t_im = rotated(found, re, im)
        if k == 0:
            assert np.array_equal(t_re, re) and np.array_equal(t_im, im)
        c, s, d = found
        assert np.array_equal(t_re, (2 * (c * re - s * im) + d) // (2 * d))
        assert np.array_equal(t_im, (2 * (s * re + c * im) + d) // (2 * d))


def test_the_refusals_name_the_port():
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    term = simulation._receive_term
    beyond = np.array([len(simulation.twist_table.coarse) << simulation.twist_table.fine_bits])
    with pytest.raises(ValueError, match=r"toward -y .* beyond the twist table"):
        triple(term, beyond, 3)
    with pytest.raises(ValueError, match=r"toward \+z .*no table"):
        triple(ReceiveTerm(None, None, simulation.twist_table.fine_bits), np.array([1]), 4)
    level = np.zeros((1, 1, 1), dtype=np.int64)
    link = Link(level, None, ())
    with pytest.raises(ValueError, match="six Links"):
        apply(term, ReceiveStart(level, None, (), (link,)))
    with pytest.raises(ValueError, match=r"toward \+x carries 0 vector parts for 1"):
        apply(term, ReceiveStart(level, None, (TwistRead(1, (level, level, level)),), (link,) * 6))


def test_the_declaration_is_the_registers_row():
    assert DECLARATION.name == "the receive" and folder_of(DECLARATION.name) == "receive"
    assert DECLARATION.place == "(i)" and DECLARATION.word == "the step"
    assert DECLARATION.function is apply and DECLARATION.writes == ("the arrivals",)
    document = json.loads((TOWARD / "lorentz_moving.json").read_text(encoding="utf-8"))
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    registered = simulation.register.declarations["the receive"]
    assert registered.binder is None and registered.function is apply  # bound: the loop calls apply
