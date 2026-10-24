"""The charge is the Wronskian per quantum (ALGEBRA.md, The constants, the owner's word of 2026-10-24, nature's charge universality, "nature is the main thing"; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write times 3 T over its own count unit W_c sin omega_0 (`loader/derived.held_write_of`, the charge factors, the readers' units brought to one wall as the tension lines' dens are; `records.write_sources` on the time line, `bookings.booked_sources` at the start), so that every quantum of every family writes the same charge, T / 2 per count, the proton's and the electron's alike at any masses. Measured here on a small torus with a proton and an electron of different pairs both reading the sign holder, each one quantum laid at the quarter turn (the law's one-Node lay of a plane quantum, now (A, 0), before (0, sense A)): the write per quantum of the two is equal within the lay's rounding of A, exact in the identity factor x count unit; and the one world's universe at nature's den (the proton off the top at (4,859,756, 53,346,867), the electron at (53,567,757, 29,276), Gamma 1,000 kept) loads, which the sentence of 2026-10-23 refused by name."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall, held_write_of
from event_universe.loader.universe import universe_of
from event_universe.world_files import input_digest, load_world

GAMMA, T = 1000, 36_000
DEN = 53_567_765
SIGN = {
    "name": "charge",
    "pair": [GAMMA, GAMMA],
    "reads": {},
    "held": {"sources": ["wronskian"], "level_weight": 1},
}


def universe(proton: list[int], electron: list[int], gamma: int = GAMMA) -> dict:  # type: ignore[type-arg]
    return {
        "integers": {"node_clock": gamma, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {**SIGN, "pair": [gamma, gamma]},
            {"name": "proton", "pair": proton, "reads": {"charge": 1}, "dimension": 2},
            {"name": "electron", "pair": electron, "reads": {"charge": 1}, "dimension": 2},
        ],
    }


def laid(folder: Path, proton: list[int], electron: list[int], senses: tuple[int, int]) -> Lattice:
    """A 5-cube torus with the proton at the centre and the electron beside it, one quantum each, both at the quarter turn at their senses, the levels the engine's own count reading one quantum."""
    (folder / "u.json").write_text(json.dumps(universe(proton, electron)))
    nodes = [[x, y, z] for x in range(5) for y in range(5) for z in range(5)]
    at = {"proton": nodes.index([2, 2, 2]), "electron": nodes.index([2, 2, 1])}
    world = {
        "shape": [5, 5, 5],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": 10,
        "universe": str(folder / "u.json"),
        "bodies": [{"family": name, "nodes": [{"node": nodes[at[name]], "count": 1}]} for name in at],
        "node_detectors": [],
    }
    levels = {"proton": 189, "electron": 189}
    pairs = {"proton": proton, "electron": electron}
    path = folder / "w.json"
    for _round in range(8):
        mode = {"world_digest": input_digest(world), "packets": [], "bodies": []}
        for name, level in levels.items():
            now, im_before = [0] * 125, [0] * 125
            now[at[name]], im_before[at[name]] = level, senses[0 if name == "proton" else 1] * level
            mode["bodies"].append(
                {
                    "family": name,
                    "pair": pairs[name],
                    "moving": {
                        "now": now,
                        "before": [0] * 125,
                        "im_now": [0] * 125,
                        "im_before": im_before,
                    },
                }
            )
        path.write_text(json.dumps(world))
        path.with_suffix(".mode.json").write_text(json.dumps(mode))
        gate, Lattice.gate = Lattice.gate, lambda board: None
        try:
            board = Lattice(load_world(path))
        finally:
            Lattice.gate = gate
        board.output = lambda line: None
        done = True
        for row in board.world.bodies:
            read = int(board.quanta(row.family)[0][board.mask(row.nodes)].sum())
            name = board.families[row.family].name
            if read != 1:
                levels[name] = max(1, int(round(levels[name] * ((1.5 / max(read, 1)) ** 0.5))))
                done = False
        if done:
            return Lattice(load_world(path))
    raise AssertionError(f"the one-quantum levels did not settle: {levels}")


def wronskian_at(board: Lattice, name: str, node: tuple[int, int, int]) -> int:
    index = next(k for k, f in enumerate(board.families) if f.name == name)
    re, im = board.states[index].lines[0], board.states[index].lines[1]
    return int(re.now[node]) * int(im.before[node]) - int(im.now[node]) * int(re.before[node])


def test_one_alpha_per_holder_and_the_charge_per_quantum_equal_across_two_pairs(tmp_path):  # type: ignore[no-untyped-def]
    proton, electron = [0, 6000], [3600, 6000]  # the hydrogen worlds' pairs, the sines 1 and 4 / 5
    _integers, families = universe_of(universe(proton, electron))
    sign = families[0]
    assert (sign.write_weight, sign.write_wall) == (
        36,
        1,
    )  # alpha = E_h T / Gamma = 36,000 / 1,000, no pair in it
    write = held_write_of(families, 0, T)
    units = {k: count_wall(families[k], T) for k in (1, 2)}
    assert units == {
        1: 3 * T * 6000,
        2: 3 * T * 6000 * 4 // 5,
    }  # W_c sin omega_0 = 3 T den sin omega_0: the sines 1 and 4 / 5
    # the identity: factor x count unit is one number for every reader, so a quantum's Wronskian over its unit writes alike
    assert (
        write.factors[1] * units[1] == write.factors[2] * units[2]
    )  # one den here, so the units' ratio alone
    assert (write.factors[1], write.factors[2]) == (4, 5) and write.walls[
        0
    ] == 2 * T * 4  # one over the sines, 1 and 5 / 4, brought to the integers 4 and 5: the walls times 4
    # measured: one quantum of each at the quarter turn, the write's source per quantum equal within the lay's rounding of A
    board = laid(tmp_path, proton, electron, (-1, 1))
    w_p, w_e = wronskian_at(board, "proton", (2, 2, 2)), wronskian_at(board, "electron", (2, 2, 1))
    assert w_p < 0 < w_e  # opposite senses, the charge's sign
    per_quantum = Fraction(-w_p * write.factors[1]), Fraction(w_e * write.factors[2])
    assert abs(per_quantum[0] - per_quantum[1]) <= per_quantum[0] / 10, (
        w_p,
        w_e,
    )  # the integers' rounding of A at one quantum
    assert abs(Fraction(-w_p, units[1]) - Fraction(w_e, units[2])) <= Fraction(-w_p, units[1]) / 10
    for _ in range(3):
        board.step()  # the write runs with the factors, no refusal
    assert board.interval == 3


def test_the_one_world_at_natures_den_loads_with_the_proton_off_the_top():  # type: ignore[no-untyped-def]
    """The universe of $S/arrange/nature_den/universe_nature.json (2026-10-24): the pairs on the circle of den 53,567,765 = 5 x 17 x 73 x 89 x 97 with Gamma 1,000, the proton at (4,859,756, 53,346,867) off the top and the electron at (53,567,757, 29,276), both moving planes reading one holder: refused by name under the sentence of 2026-10-23, loaded under the charge's universality with alpha (36, 1)."""
    document = {
        "integers": {"node_clock": GAMMA, "quantum_action": T, "width": 92, "link_unit": 16},
        "families": [
            {
                "name": "gravity",
                "pair": [53_529_741, DEN],
                "reads": {"gravity": 1},
                "held": {"sources": ["form", "tensions"], "level_weight": 1, "write_weight": 1},
            },
            {
                "name": "charge",
                "pair": [DEN, DEN],
                "reads": {},
                "held": {"sources": ["wronskian"], "level_weight": 1},
            },
            {"name": "matter", "pair": [32_140_659, DEN], "reads": {"gravity": 1}, "dimension": 1},
            {"name": "light", "pair": [DEN, DEN], "reads": {"gravity": 1}, "dimension": 1},
            {
                "name": "proton",
                "pair": [4_859_756, DEN],
                "reads": {"gravity": 1, "charge": 1},
                "dimension": 2,
            },
            {
                "name": "electron",
                "pair": [53_567_757, DEN],
                "reads": {"gravity": 1, "charge": 3},
                "dimension": 2,
            },
            {
                "name": "absorber",
                "pair": [35_564_716, DEN],
                "reads": {"gravity": 1},
                "dimension": [2, 2],
            },
        ],
    }
    _integers, families = universe_of(document)
    sign = next(f for f in families if f.name == "charge")
    assert (sign.write_weight, sign.write_wall) == (36, 1)
    write = held_write_of(families, families.index(sign), T)
    proton, electron = (families.index(f) for f in families if f.name in ("proton", "electron"))
    assert write.factors[proton] * count_wall(families[proton], T) == write.factors[
        electron
    ] * count_wall(families[electron], T)
    assert np.gcd(write.factors[proton], write.factors[electron]) >= 1
