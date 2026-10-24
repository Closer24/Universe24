"""The flux form of Rule3 and the linear sum L (ALGEBRA.md, The flux form of Rule3; `linear_sum` and `weighted_linear_sum` of tests/laws.py, the tests' own instruments): the one line w a_next + r' = SUM R_ij m_ij + S a_now - w a_before + r, written as w (a_next - 2 a_now + a_before) + r' - r = SUM_j R_ij (m_ij - a_now) - D a_now with D = 2 w - S - SUM_j R_ij; on a board closed on every axis at one rate the Link terms pair off Link by Link and the mass term is 0 for light, so the linear sum of a line of light, L = SUM over the Nodes of [w (now - before) + r], is an exact invariant, remainders included, and at a fixed content profile the rate-weighted sum L'' with the weights scale div p_i^2 is, R_ij / p_i^2 being the same from both ends of a Link. On the bare 3-cube torus of the one universe file and on arrays of its light family."""

import json
import math
from pathlib import Path

import numpy as np
import pytest

from event_universe import flux, node, records, seed, world_files
from event_universe.core import paces
from event_universe.core.ports import LINK_UNIT, Wrap
from event_universe.lattice import Lattice
from event_universe.loader.universe import MASSLESS, universe_of
from event_universe.readings import ports
from event_universe.world_files import load_world
from tests.laws import linear_sum, weighted_linear_sum
from tests.laws_universe import CUBE, UNIVERSE, bare_torus, uniform_sea

BEFORE_THE_BIRTHS = 23  # the births at 24 on the bare 3-cube of the tests' small universe with the massless volume holder (2026-10-24; 30 at the one universe's gapped holder since the close reads the interval's start, 29 when it read the state after the step)


def test_the_linear_sum_of_light_is_constant_on_the_bare_torus_until_the_births(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The seed's light on the bare 3-cube torus: L is the same whole number after every one of the 29 intervals before the births, while the held row's write moves the paces (one content over the board at every interval, so the Link terms pair off) and the levels rise from the seed; at 29 the births' holes take the light and L falls."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        seed, "uniform_seed", uniform_sea
    )  # the uniform sea, the law's seed to 2026-10-24, by name: the sentence is the uniform content's
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(bare_torus(tmp_path)), output=lines.append)
    light = board.world.seed
    assert light is not None
    wall = 6 * board.families[light].pair[1] * board.world.node_clock**2 * board.unit**2
    first = linear_sum(wall, board.states[light].lines[0])
    for _ in range(BEFORE_THE_BIRTHS):
        board.step()
        assert linear_sum(wall, board.states[light].lines[0]) == first, board.interval
    assert (
        board.states[light].lines[0].now > seed.drift_of(board.world.quantum_action)
    ).all()  # the levels rose from the seed's drift, L stood
    board.step()
    assert any(line["event"] == "birth" for line in lines)
    assert linear_sum(wall, board.states[light].lines[0]) != first  # the holes took the light


def test_the_rate_weighted_linear_sum_of_light_is_constant_at_a_fixed_content() -> None:
    """The light family on a 3-cube torus of random levels within 10^6 at the content 0 on two layers and 600 on the third, laid by hand and never stepped: the rule `node.rule_of` at that content, 100 intervals of the engine's own `flux.step_line`, L'' = SUM weight_i [w (now - before) + r] the same whole number after every interval, weight_i = scale div p_i^2 with scale the least common multiple of the two distinct p_i^2, while L moves by exactly the pairing term SUM over the Links of (R_ij - R_ji)(a_j - a_i), the step's own Links' sum."""
    integers, families = universe_of(json.loads(UNIVERSE.read_text(encoding="utf-8")))
    light = next(family for family in families if family.name == MASSLESS)
    gamma, unit, wrap, shape = (
        integers["node_clock"],
        LINK_UNIT,
        Wrap(True, True, True),
        (CUBE,) * 3,
    )
    content = np.zeros(shape, dtype=object)
    content[CUBE - 1] = 600
    rule = node.rule_of(light, gamma, content, None, unit)
    reads = [np.asarray(read, dtype=object) for read in rule[0]]
    squared = np.asarray(paces.node_paces(gamma, content)[1], dtype=object) ** 2
    scale = math.lcm(*{int(v) for v in squared.ravel()})
    weights = np.vectorize(lambda v: scale // int(v), otypes=[object])(squared)
    assert len({int(v) for v in weights.ravel()}) == 2
    draw = np.random.default_rng(5)
    line = records.Record(
        draw.integers(-(10**6), 10**6, shape).astype(object),
        draw.integers(-(10**6), 10**6, shape).astype(object),
        np.zeros(shape, dtype=object),
    )
    wall = 6 * light.pair[1] * gamma**2 * unit**2
    first = weighted_linear_sum(wall, line, weights)
    for _ in range(100):
        a = np.asarray(line.now, dtype=object)
        pairing = sum(
            int((read * (np.asarray(m, dtype=object) - a)).sum())
            for read, m in zip(reads, ports(a, wrap), strict=True)
        )
        before = linear_sum(wall, line)
        line = flux.step_line(line, rule, wrap)
        assert (
            linear_sum(wall, line) - before == pairing
        )  # L moves by the pairing term alone, the mass 0
        assert weighted_linear_sum(wall, line, weights) == first
